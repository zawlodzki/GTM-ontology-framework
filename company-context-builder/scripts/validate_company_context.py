#!/usr/bin/env python3
"""Validate company-context manifests, artifacts, references, and freshness."""

from __future__ import annotations

import argparse
import calendar
import datetime as dt
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

try:
    import yaml
except ImportError as exc:  # pragma: no cover - exercised by CLI environments
    raise SystemExit("PyYAML is required: python -m pip install pyyaml") from exc

try:
    from jsonschema import Draft202012Validator, FormatChecker
    from jsonschema.exceptions import SchemaError
except ImportError as exc:  # pragma: no cover - exercised by CLI environments
    raise SystemExit("jsonschema is required: python -m pip install jsonschema") from exc


SOURCES = {"declared", "discovered", "inferred", "learned", "synthetic"}
STATUSES = {"draft", "confirmed", "example"}
REF_KEY = re.compile(r"(?:^|_)(?:ref|refs)$")
VERIFY_EVERY = re.compile(r"^(\d+)([dwmy])$")
FRONTMATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", re.DOTALL)

REQUIRED_REFS: dict[str, tuple[str, ...]] = {
    "product-group-strategy": (
        "company_strategy_ref", "primary_segment_ref", "primary_use_case_ref", "primary_icp_ref"
    ),
    "segment": ("strategy_ref", "primary_use_case_ref", "icp_ref", "persona_ref"),
    "use-case": ("strategy_ref", "segment_ref", "persona_ref", "product_refs"),
    "icp": ("strategy_ref", "segment_ref", "use_case_ref"),
    "personas": ("strategy_ref", "segment_ref", "use_case_ref", "icp_ref"),
    "buying-context": (
        "strategy_ref", "segment_ref", "use_case_ref", "icp_ref", "persona_ref", "product_refs"
    ),
    "product-context": (
        "strategy_ref", "segment_ref", "use_case_ref", "audience_refs",
        "buying_context_ref", "positioning_ref", "gtm_motion_refs"
    ),
    "positioning": (
        "strategy_ref", "segment_ref", "use_case_ref", "icp_ref", "persona_ref",
        "buying_context_ref", "product_refs"
    ),
    "value-propositions": (
        "strategy_ref", "segment_ref", "use_case_ref", "persona_ref",
        "buying_context_ref", "positioning_ref", "product_refs"
    ),
    "messaging": (
        "strategy_ref", "segment_ref", "use_case_ref", "persona_ref",
        "buying_context_ref", "positioning_ref", "value_proposition_ref", "product_refs"
    ),
    "gtm-motions": (
        "strategy_ref", "segment_ref", "use_case_ref", "icp_ref", "persona_ref",
        "buying_context_ref", "positioning_ref", "value_proposition_ref",
        "messaging_ref", "product_refs"
    ),
}


@dataclass
class Finding:
    level: str
    code: str
    path: Path
    message: str


@dataclass
class Artifact:
    path: Path
    data: dict[str, Any]

    @property
    def typed_id(self) -> str:
        return f"{self.data.get('kind')}:{self.data.get('id')}"


class Validator:
    def __init__(self, root: Path, today: dt.date | None = None) -> None:
        self.root = root.resolve()
        self.today = today or dt.date.today()
        self.findings: list[Finding] = []
        self.artifacts: list[Artifact] = []
        self.manifest_paths: set[Path] = set()
        self.schema_root = Path(__file__).resolve().parents[1] / "schemas"
        self.schemas: dict[str, dict[str, Any]] = {}

    def add(self, level: str, code: str, path: Path, message: str) -> None:
        self.findings.append(Finding(level, code, path, message))

    def load_yaml(self, path: Path) -> dict[str, Any] | None:
        try:
            value = yaml.safe_load(path.read_text(encoding="utf-8"))
        except (OSError, yaml.YAMLError) as exc:
            self.add("ERROR", "yaml", path, str(exc))
            return None
        if not isinstance(value, dict):
            self.add("ERROR", "yaml", path, "expected a YAML mapping")
            return None
        return value

    def load_frontmatter(self, path: Path) -> dict[str, Any] | None:
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            self.add("ERROR", "read", path, str(exc))
            return None
        match = FRONTMATTER.match(text)
        if not match:
            self.add("ERROR", "frontmatter", path, "missing YAML frontmatter")
            return None
        try:
            value = yaml.safe_load(match.group(1))
        except yaml.YAMLError as exc:
            self.add("ERROR", "frontmatter", path, str(exc))
            return None
        if not isinstance(value, dict):
            self.add("ERROR", "frontmatter", path, "frontmatter must be a mapping")
            return None
        return value

    def validate_schema(self, data: dict[str, Any], path: Path, name: str) -> None:
        schema = self.schemas.get(name)
        if schema is None:
            schema_path = self.schema_root / name
            try:
                schema = json.loads(schema_path.read_text(encoding="utf-8"))
                Draft202012Validator.check_schema(schema)
            except (OSError, json.JSONDecodeError, SchemaError) as exc:
                self.add("ERROR", "schema-load", schema_path, str(exc))
                return
            self.schemas[name] = schema
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        errors = sorted(validator.iter_errors(schema_value(data)), key=lambda item: list(item.absolute_path))
        for error in errors:
            location = ".".join(str(part) for part in error.absolute_path) or "<root>"
            self.add("ERROR", "schema", path, f"{location}: {error.message}")

    def validate_manifest(self, path: Path, expected_kind: str) -> dict[str, Any] | None:
        data = self.load_yaml(path)
        if data is None:
            return None
        for field in ("kind", "id", "version", "updated", "language"):
            if data.get(field) in (None, ""):
                self.add("ERROR", "manifest-field", path, f"missing {field}")
        if data.get("kind") != expected_kind:
            self.add("ERROR", "manifest-kind", path, f"expected kind {expected_kind}")
        schema_name = (
            "company-context-manifest.schema.json"
            if expected_kind == "company-context-manifest"
            else "product-group-manifest.schema.json"
        )
        self.validate_schema(data, path, schema_name)
        return data

    def add_manifest_entries(self, manifest: Path, data: dict[str, Any]) -> None:
        entries: list[Any] = []
        for key in ("artifacts", "products"):
            value = data.get(key, [])
            if not isinstance(value, list):
                self.add("ERROR", "manifest-list", manifest, f"{key} must be a list")
                continue
            entries.extend(value)
        for entry in entries:
            if not isinstance(entry, dict):
                self.add("ERROR", "manifest-entry", manifest, "entry must be a mapping")
                continue
            for field in ("id", "kind", "path", "summary", "load_when"):
                if entry.get(field) in (None, ""):
                    self.add("ERROR", "manifest-entry", manifest, f"entry missing {field}")
            relative = entry.get("path")
            if not isinstance(relative, str):
                continue
            artifact_path = (manifest.parent / relative).resolve()
            self.manifest_paths.add(artifact_path)
            if not artifact_path.is_file():
                self.add("ERROR", "missing-artifact", manifest, f"missing {relative}")
                continue
            frontmatter = self.load_frontmatter(artifact_path)
            if frontmatter is None:
                continue
            if entry.get("id") != frontmatter.get("id") or entry.get("kind") != frontmatter.get("kind"):
                self.add("ERROR", "manifest-mismatch", artifact_path, "manifest id/kind differs from frontmatter")
            self.artifacts.append(Artifact(artifact_path, frontmatter))

    def validate_artifact(self, artifact: Artifact, apply_schema: bool = True) -> None:
        data, path = artifact.data, artifact.path
        if apply_schema:
            self.validate_schema(data, path, "context-artifact.schema.json")
        for field in ("kind", "id", "scope", "meta"):
            if data.get(field) in (None, ""):
                self.add("ERROR", "artifact-field", path, f"missing {field}")
        meta = data.get("meta")
        if not isinstance(meta, dict):
            return
        for field in ("source", "status", "updated"):
            if meta.get(field) in (None, ""):
                self.add("ERROR", "meta-field", path, f"meta missing {field}")
        if meta.get("source") not in SOURCES:
            self.add("ERROR", "source", path, f"invalid source {meta.get('source')!r}")
        if meta.get("status") not in STATUSES:
            self.add("ERROR", "status", path, f"invalid status {meta.get('status')!r}")
        if meta.get("source") == "learned" and not meta.get("evidence"):
            self.add("WARN", "evidence", path, "source learned has no evidence")
        self.validate_freshness(path, meta)

        required = REQUIRED_REFS.get(str(data.get("kind")), ())
        for field in required:
            if data.get(field) in (None, "", []):
                level = "ERROR" if meta.get("status") in {"confirmed", "example"} else "WARN"
                self.add(level, "required-ref", path, f"missing {field}")

    def validate_freshness(self, path: Path, meta: dict[str, Any]) -> None:
        last_verified, verify_every = meta.get("last_verified"), meta.get("verify_every")
        if last_verified is None and verify_every is None:
            return
        if last_verified is None or verify_every is None:
            self.add("WARN", "freshness", path, "last_verified and verify_every must be paired")
            return
        try:
            verified = as_date(last_verified)
        except ValueError as exc:
            self.add("ERROR", "freshness", path, str(exc))
            return
        match = VERIFY_EVERY.fullmatch(str(verify_every))
        if not match:
            self.add("ERROR", "freshness", path, f"invalid verify_every {verify_every!r}")
            return
        due = add_period(verified, int(match.group(1)), match.group(2))
        if due < self.today:
            self.add("WARN", "overdue", path, f"verification overdue since {due.isoformat()}")

    def validate_references(self) -> None:
        index: dict[str, Artifact] = {}

        def register(typed_id: str, artifact: Artifact) -> None:
            if typed_id in index:
                self.add("ERROR", "duplicate-id", artifact.path, f"duplicate {typed_id}")
            index[typed_id] = artifact

        for artifact in self.artifacts:
            register(artifact.typed_id, artifact)
            if artifact.data.get("kind") != "gtm-motions":
                continue
            motions = artifact.data.get("motions", [])
            if not isinstance(motions, list):
                continue
            for motion in motions:
                if isinstance(motion, dict) and isinstance(motion.get("id"), str):
                    register(f"gtm-motion:{motion['id']}", artifact)

        for artifact in self.artifacts:
            source_status = artifact.data.get("meta", {}).get("status")
            for key, value in artifact.data.items():
                if not REF_KEY.search(key):
                    continue
                refs = value if isinstance(value, list) else [value]
                for ref in refs:
                    if not isinstance(ref, str) or ":" not in ref:
                        self.add("ERROR", "typed-ref", artifact.path, f"{key} contains invalid ref {ref!r}")
                        continue
                    target = index.get(ref)
                    if target is None:
                        self.add("ERROR", "unresolved-ref", artifact.path, f"{key} -> {ref}")
                        continue
                    target_status = target.data.get("meta", {}).get("status")
                    if source_status == "confirmed" and target_status == "draft":
                        self.add("ERROR", "confirmed-to-draft", artifact.path, f"{key} -> {ref}")

    def validate_completeness(self) -> None:
        excluded = {"CLAUDE.md", "AGENTS.md", "README.md", "ARTIFACT-GUIDE.md", "GAPS.md"}
        for base in (self.root / "company", self.root / "product-groups"):
            if not base.exists():
                continue
            for path in base.rglob("*.md"):
                if path.name not in excluded and path.resolve() not in self.manifest_paths:
                    self.add("ERROR", "orphan", path, "artifact is not indexed by a manifest")

    def validate_gaps_report(self, path: Path) -> None:
        data = self.load_frontmatter(path)
        if data is None:
            return
        self.validate_artifact(Artifact(path, data), apply_schema=False)
        expected = {
            "kind": "company-context-gaps",
            "id": "company-context-gaps",
            "scope": "company-context",
        }
        for field, value in expected.items():
            if data.get(field) != value:
                self.add("ERROR", "gaps-contract", path, f"{field} must be {value}")
        if data.get("meta", {}).get("status") != "draft":
            self.add("ERROR", "gaps-contract", path, "unresolved gaps report must remain draft")

    def run(self) -> list[Finding]:
        root_manifest = self.root / "manifest.yaml"
        if not root_manifest.is_file():
            self.add("ERROR", "manifest", root_manifest, "root manifest is missing")
            return self.findings
        root_data = self.validate_manifest(root_manifest, "company-context-manifest")
        if root_data is None:
            return self.findings
        if not isinstance(root_data.get("company"), dict):
            self.add("ERROR", "manifest-company", root_manifest, "company must be a mapping")
        self.add_manifest_entries(root_manifest, root_data)

        gaps = root_data.get("gaps_report")
        gaps_path = self.root / "GAPS.md"
        if gaps is not None:
            if gaps != "GAPS.md":
                self.add("ERROR", "gaps", root_manifest, "gaps_report must be GAPS.md")
            if not gaps_path.is_file():
                self.add("ERROR", "gaps", root_manifest, "gaps_report points to a missing file")
            else:
                self.validate_gaps_report(gaps_path)
        elif gaps_path.exists():
            self.add("WARN", "gaps", gaps_path, "GAPS.md exists but manifest has no gaps_report")
            self.validate_gaps_report(gaps_path)

        groups = root_data.get("product_groups", [])
        if not isinstance(groups, list):
            self.add("ERROR", "product-groups", root_manifest, "product_groups must be a list")
            groups = []
        for entry in groups:
            if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
                self.add("ERROR", "product-group-entry", root_manifest, "invalid product group entry")
                continue
            manifest = (self.root / entry["path"]).resolve()
            if not manifest.is_file():
                self.add("ERROR", "product-group-manifest", root_manifest, f"missing {entry['path']}")
                continue
            data = self.validate_manifest(manifest, "product-group-manifest")
            if data is not None:
                if entry.get("id") != data.get("id"):
                    self.add("ERROR", "product-group-id", manifest, "root entry id differs from manifest id")
                self.add_manifest_entries(manifest, data)

        for artifact in self.artifacts:
            self.validate_artifact(artifact)
        self.validate_references()
        self.validate_completeness()
        return self.findings


def as_date(value: Any) -> dt.date:
    if isinstance(value, dt.datetime):
        return value.date()
    if isinstance(value, dt.date):
        return value
    try:
        return dt.date.fromisoformat(str(value))
    except ValueError as exc:
        raise ValueError(f"invalid date {value!r}") from exc


def schema_value(value: Any) -> Any:
    if isinstance(value, dt.datetime):
        return value.isoformat()
    if isinstance(value, dt.date):
        return value.isoformat()
    if isinstance(value, dict):
        return {key: schema_value(item) for key, item in value.items()}
    if isinstance(value, list):
        return [schema_value(item) for item in value]
    return value


def add_period(value: dt.date, amount: int, unit: str) -> dt.date:
    if unit == "d":
        return value + dt.timedelta(days=amount)
    if unit == "w":
        return value + dt.timedelta(weeks=amount)
    months = amount if unit == "m" else amount * 12
    month_index = value.month - 1 + months
    year, month = value.year + month_index // 12, month_index % 12 + 1
    day = min(value.day, calendar.monthrange(year, month)[1])
    return dt.date(year, month, day)


def relative(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("context", nargs="?", default="company-context")
    parser.add_argument("--today", help="override today's date for deterministic checks")
    args = parser.parse_args(argv)
    today = dt.date.fromisoformat(args.today) if args.today else None
    validator = Validator(Path(args.context), today=today)
    findings = validator.run()
    for finding in sorted(findings, key=lambda item: (item.level, str(item.path), item.code)):
        print(f"{finding.level} [{finding.code}] {relative(finding.path, validator.root)}: {finding.message}")
    errors = sum(item.level == "ERROR" for item in findings)
    warnings = sum(item.level == "WARN" for item in findings)
    print(f"Validation complete: {errors} error(s), {warnings} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
