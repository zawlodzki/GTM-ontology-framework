#!/usr/bin/env python3
"""Initialize a company-context tree from the bundled starter assets."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
from pathlib import Path
from urllib.parse import urlparse


TOKEN_RE = re.compile(r"\{\{([A-Z0-9_]+)\}\}")
CANONICAL_ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def nonempty(value: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise argparse.ArgumentTypeError("value cannot be empty")
    return normalized


def iso_date(value: str) -> str:
    try:
        return dt.date.fromisoformat(value).isoformat()
    except ValueError as exc:
        raise argparse.ArgumentTypeError("date must use YYYY-MM-DD") from exc


def http_url(value: str) -> str:
    parsed = urlparse(value.strip())
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise argparse.ArgumentTypeError("company domain must be an absolute HTTP(S) URL")
    return value.strip()


def slug(value: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    if not normalized:
        raise argparse.ArgumentTypeError("identifier must contain a letter or digit")
    return normalized


def parse_group(value: str) -> tuple[str, str]:
    raw_id, separator, raw_name = value.partition(":")
    group_id = slug(raw_id)
    name = raw_name.strip() if separator else raw_id.replace("-", " ").title()
    if not name:
        raise argparse.ArgumentTypeError("product group name cannot be empty")
    return group_id, name


def parse_motion(value: str) -> tuple[str, str, str, str]:
    parts = value.split(":", 3)
    if len(parts) != 4:
        raise argparse.ArgumentTypeError(
            "motion must use GROUP_ID:MOTION_ID:NAME:SUMMARY"
        )
    raw_group_id, motion_id, name, summary = (part.strip() for part in parts)
    group_id = slug(raw_group_id)
    if not CANONICAL_ID_RE.fullmatch(motion_id):
        raise argparse.ArgumentTypeError("motion id must use lowercase kebab-case")
    if not name:
        raise argparse.ArgumentTypeError("motion name cannot be empty")
    if not summary:
        raise argparse.ArgumentTypeError("motion summary cannot be empty")
    if len(summary) > 140:
        raise argparse.ArgumentTypeError("motion summary cannot exceed 140 characters")
    return group_id, motion_id, name, summary


def render_text(source: Path, target: Path, values: dict[str, str]) -> None:
    text = source.read_text(encoding="utf-8")

    def replace(match: re.Match[str]) -> str:
        key = match.group(1)
        if key not in values:
            raise ValueError(f"unknown template token {key} in {source}")
        return values[key]

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(TOKEN_RE.sub(replace, text), encoding="utf-8")


def copy_template(
    source: Path,
    target: Path,
    values: dict[str, str],
    skip: set[Path] | None = None,
) -> None:
    skipped = skip or set()
    for path in sorted(source.rglob("*")):
        if path.is_dir():
            continue
        relative = path.relative_to(source)
        if relative in skipped:
            continue
        rendered_parts: list[str] = []
        for part in relative.parts:
            def replace(match: re.Match[str]) -> str:
                key = match.group(1)
                if key not in values:
                    raise ValueError(f"unknown path template token {key} in {source}")
                return values[key]
            rendered_parts.append(TOKEN_RE.sub(replace, part))
        destination = target.joinpath(*rendered_parts)
        render_text(path, destination, values)


def product_groups_block(groups: list[tuple[str, str]]) -> str:
    if not groups:
        return "product_groups: []"
    lines = ["product_groups:"]
    for group_id, group_name in groups:
        summary = json.dumps(f"Context for the {group_name} product group.", ensure_ascii=False)
        load_when = json.dumps(
            f"Working on {group_name} audiences, products, positioning, or GTM.",
            ensure_ascii=False,
        )
        lines.extend(
            [
                f"  - id: {group_id}",
                f"    path: product-groups/{group_id}/manifest.yaml",
                f"    summary: {summary}",
                f"    load_when: {load_when}",
            ]
        )
    return "\n".join(lines)


def motions_manifest_block(
    group_id: str, motions: list[tuple[str, str, str]]
) -> str:
    if not motions:
        return ""
    return "\n".join(
        [
            f"  - id: {group_id}-motions",
            "    kind: gtm-motions",
            "    path: go-to-market/motions.md",
            "    summary: Channels, journey execution, qualification, routing, handoffs, and measures.",
            "    load_when: Planning demand, sales routing, handoffs, adoption, or motion review.",
        ]
    )


def motions_frontmatter_block(motions: list[tuple[str, str, str]]) -> str:
    lines = ["motions:"]
    for motion_id, name, summary in motions:
        lines.extend(
            [
                f"  - id: {motion_id}",
                f"    name: {json.dumps(name, ensure_ascii=False)}",
                f"    summary: {json.dumps(summary, ensure_ascii=False)}",
            ]
        )
    return "\n".join(lines)


def build_context(args: argparse.Namespace) -> Path:
    skill_root = Path(__file__).resolve().parents[1]
    template_root = skill_root / "assets" / "company-context"
    group_template = template_root / "product-groups" / "_group"
    if not template_root.is_dir() or not group_template.is_dir():
        raise FileNotFoundError("bundled company-context starter assets are missing")

    output = Path(args.output).resolve()
    if output.exists() and (not output.is_dir() or any(output.iterdir())):
        raise FileExistsError(f"refusing to overwrite existing path: {output}")
    output.mkdir(parents=True, exist_ok=True)

    groups = [parse_group(value) for value in args.product_group]
    if len({group_id for group_id, _ in groups}) != len(groups):
        raise ValueError("product group identifiers must be unique")
    parsed_motions = [parse_motion(value) for value in args.motion]
    group_ids = {group_id for group_id, _ in groups}
    unknown_groups = sorted({group_id for group_id, *_ in parsed_motions} - group_ids)
    if unknown_groups:
        raise ValueError(f"motions reference unknown product groups: {', '.join(unknown_groups)}")
    motion_ids = [motion_id for _, motion_id, _, _ in parsed_motions]
    if len(set(motion_ids)) != len(motion_ids):
        raise ValueError("motion identifiers must be unique across company-context")
    motions_by_group: dict[str, list[tuple[str, str, str]]] = {
        group_id: [] for group_id in group_ids
    }
    for group_id, motion_id, name, summary in parsed_motions:
        motions_by_group[group_id].append((motion_id, name, summary))

    company_id = slug(args.company_id)
    base_values = {
        "COMPANY_ID": company_id,
        "COMPANY_NAME": args.company_name.strip(),
        "COMPANY_NAME_YAML": json.dumps(args.company_name.strip(), ensure_ascii=False),
        "COMPANY_DOMAIN": args.company_domain.strip(),
        "COMPANY_DOMAIN_YAML": json.dumps(args.company_domain.strip(), ensure_ascii=False),
        "LANGUAGE": args.language.strip(),
        "LANGUAGE_YAML": json.dumps(args.language.strip(), ensure_ascii=False),
        "UPDATED": args.updated,
        "PRODUCT_GROUPS_BLOCK": product_groups_block(groups),
    }

    for path in sorted(template_root.rglob("*")):
        if path.is_dir() or group_template in path.parents or path == group_template:
            continue
        relative = path.relative_to(template_root)
        render_text(path, output / relative, base_values)

    product_groups = output / "product-groups"
    product_groups.mkdir(parents=True, exist_ok=True)
    for group_id, group_name in groups:
        group_motions = motions_by_group[group_id]
        values = dict(
            base_values,
            PRODUCT_GROUP_ID=group_id,
            PRODUCT_GROUP_NAME=group_name,
            PRODUCT_GROUP_NAME_YAML=json.dumps(group_name, ensure_ascii=False),
            MOTIONS_MANIFEST_BLOCK=motions_manifest_block(group_id, group_motions),
            MOTIONS_FRONTMATTER_BLOCK=motions_frontmatter_block(group_motions),
        )
        skip = set() if group_motions else {Path("go-to-market/motions.md")}
        copy_template(group_template, product_groups / group_id, values, skip=skip)

    return output


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="company-context", help="target directory")
    parser.add_argument("--company-id", required=True)
    parser.add_argument("--company-name", required=True, type=nonempty)
    parser.add_argument("--company-domain", required=True, type=http_url)
    parser.add_argument("--language", default="en", type=nonempty)
    parser.add_argument("--updated", required=True, type=iso_date, help="YYYY-MM-DD")
    parser.add_argument(
        "--product-group",
        action="append",
        default=[],
        metavar="ID[:NAME]",
        help="repeat for each approved product group",
    )
    parser.add_argument(
        "--motion",
        action="append",
        default=[],
        metavar="GROUP_ID:MOTION_ID:NAME:SUMMARY",
        help="repeat for each approved canonical GTM motion",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        output = build_context(args)
    except (FileExistsError, FileNotFoundError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 1
    print(f"Initialized {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
