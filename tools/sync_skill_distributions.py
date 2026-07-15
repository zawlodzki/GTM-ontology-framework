#!/usr/bin/env python3
"""Synchronize source skills into plugin payloads and deterministic .skill files."""

from __future__ import annotations

import argparse
import io
import json
import os
import re
import shutil
import stat
import sys
import tempfile
import zipfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Iterable


SKILL_NAMES = ("gtm-ontology-builder", "company-context-builder")
EXCLUDED_NAMES = {".DS_Store", "__pycache__"}
EXCLUDED_SUFFIXES = {".pyc"}
ARCHIVE_TIMESTAMP = (1980, 1, 1, 0, 0, 0)
SEMVER_CORE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
SOURCE_REVISION = re.compile(r"^[0-9a-fA-F]{12,64}$")
VERSION_FIELD = re.compile(r'(?m)^(\s*"version"\s*:\s*")([^"]+)("\s*,?\s*)$')


class DistributionError(RuntimeError):
    """Raised when a distribution cannot be generated safely."""


@dataclass(frozen=True)
class TreeEntry:
    kind: str
    mode: int
    data: bytes | None = None


@dataclass(frozen=True)
class VersionPlan:
    claude_version: str
    codex_version: str
    claude_changed: bool
    codex_changed: bool


@dataclass(frozen=True)
class SyncResult:
    changed: tuple[str, ...]


def default_repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _is_excluded(name: str) -> bool:
    return name in EXCLUDED_NAMES or Path(name).suffix in EXCLUDED_SUFFIXES


def _normalized_file_mode(mode: int) -> int:
    return 0o755 if mode & 0o111 else 0o644


def _collect_tree(root: Path) -> dict[str, TreeEntry]:
    if not root.is_dir():
        raise DistributionError(f"missing source skill directory: {root}")
    if not (root / "SKILL.md").is_file():
        raise DistributionError(f"source skill has no SKILL.md: {root}")

    entries: dict[str, TreeEntry] = {}

    def visit(directory: Path, relative: PurePosixPath) -> None:
        for child in sorted(os.scandir(directory), key=lambda item: item.name):
            if _is_excluded(child.name):
                continue
            child_relative = relative / child.name
            key = child_relative.as_posix()
            if child.is_symlink():
                raise DistributionError(f"symlinks are not supported in source skills: {child.path}")
            if child.is_dir(follow_symlinks=False):
                entries[key] = TreeEntry("dir", 0o755)
                visit(Path(child.path), child_relative)
            elif child.is_file(follow_symlinks=False):
                source_mode = stat.S_IMODE(child.stat(follow_symlinks=False).st_mode)
                entries[key] = TreeEntry(
                    "file",
                    _normalized_file_mode(source_mode),
                    Path(child.path).read_bytes(),
                )
            else:
                raise DistributionError(f"unsupported source entry: {child.path}")

    visit(root, PurePosixPath())
    return entries


def _collect_target(root: Path) -> dict[str, TreeEntry] | None:
    if not root.exists() and not root.is_symlink():
        return None
    if root.is_symlink() or not root.is_dir():
        return {".": TreeEntry("unsupported", 0)}

    entries: dict[str, TreeEntry] = {}

    def visit(directory: Path, relative: PurePosixPath) -> None:
        for child in sorted(os.scandir(directory), key=lambda item: item.name):
            child_relative = relative / child.name
            key = child_relative.as_posix()
            if child.is_symlink():
                entries[key] = TreeEntry("symlink", 0)
            elif child.is_dir(follow_symlinks=False):
                entries[key] = TreeEntry("dir", 0o755)
                visit(Path(child.path), child_relative)
            elif child.is_file(follow_symlinks=False):
                target_mode = stat.S_IMODE(child.stat(follow_symlinks=False).st_mode)
                entries[key] = TreeEntry(
                    "file",
                    _normalized_file_mode(target_mode),
                    Path(child.path).read_bytes(),
                )
            else:
                entries[key] = TreeEntry("unsupported", 0)

    visit(root, PurePosixPath())
    return entries


def _write_tree(target: Path, entries: dict[str, TreeEntry]) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    staging_root = Path(tempfile.mkdtemp(prefix=f".{target.name}.tmp-", dir=target.parent))
    staging_target = staging_root / target.name
    try:
        staging_target.mkdir(mode=0o755)
        for relative, entry in sorted(entries.items()):
            path = staging_target / Path(relative)
            if entry.kind == "dir":
                path.mkdir(parents=True, exist_ok=True, mode=entry.mode)
                path.chmod(entry.mode)
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(entry.data or b"")
                path.chmod(entry.mode)

        if target.is_symlink() or (target.exists() and not target.is_dir()):
            target.unlink()
        elif target.exists():
            shutil.rmtree(target)
        staging_target.replace(target)
    finally:
        shutil.rmtree(staging_root, ignore_errors=True)


def _zip_info(name: str, mode: int, is_directory: bool) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(name, ARCHIVE_TIMESTAMP)
    info.create_system = 3
    if is_directory:
        info.compress_type = zipfile.ZIP_STORED
        info.external_attr = ((stat.S_IFDIR | mode) << 16) | 0x10
    else:
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = (stat.S_IFREG | mode) << 16
    return info


def _build_archive(skill_name: str, entries: dict[str, TreeEntry]) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        archive.writestr(_zip_info(f"{skill_name}/", 0o755, True), b"")
        for relative, entry in sorted(entries.items()):
            archive_name = f"{skill_name}/{relative}"
            if entry.kind == "dir":
                archive.writestr(_zip_info(f"{archive_name}/", entry.mode, True), b"")
            else:
                archive.writestr(_zip_info(archive_name, entry.mode, False), entry.data or b"")
    return buffer.getvalue()


def _read_manifest_version(path: Path) -> tuple[str, str]:
    try:
        text = path.read_text(encoding="utf-8")
        payload = json.loads(text)
    except (OSError, json.JSONDecodeError) as error:
        raise DistributionError(f"cannot read plugin manifest {path}: {error}") from error
    version = payload.get("version")
    if not isinstance(version, str):
        raise DistributionError(f"plugin manifest has no string version: {path}")
    return text, version


def _parse_versions(claude_version: str, codex_version: str) -> tuple[tuple[int, int, int], str]:
    claude_match = SEMVER_CORE.fullmatch(claude_version)
    if not claude_match:
        raise DistributionError(f"Claude plugin version must be X.Y.Z, got: {claude_version}")
    codex_core, separator, codex_metadata = codex_version.partition("+")
    codex_match = SEMVER_CORE.fullmatch(codex_core)
    if not codex_match or not separator or not codex_metadata.startswith("codex."):
        raise DistributionError(
            f"Codex plugin version must be X.Y.Z+codex.<token>, got: {codex_version}"
        )
    if codex_core != claude_version:
        raise DistributionError(
            f"plugin version cores differ: Claude={claude_version}, Codex={codex_core}"
        )
    return tuple(int(part) for part in claude_match.groups()), codex_metadata.removeprefix("codex.")


def _normalize_revision(source_revision: str | None) -> str:
    if not source_revision or not SOURCE_REVISION.fullmatch(source_revision):
        raise DistributionError("source revision must be a hexadecimal Git revision of at least 12 characters")
    return source_revision[:12].lower()


def _plan_versions(repo_root: Path, mode: str, source_revision: str | None) -> VersionPlan:
    claude_path = repo_root / "plugin/.claude-plugin/plugin.json"
    codex_path = repo_root / "plugins/gtm-ontology-builder/.codex-plugin/plugin.json"
    _, claude_version = _read_manifest_version(claude_path)
    _, codex_version = _read_manifest_version(codex_path)
    (major, minor, patch), current_token = _parse_versions(claude_version, codex_version)

    if mode == "keep":
        if source_revision is not None:
            raise DistributionError("--source-revision requires version mode seed or patch")
        return VersionPlan(claude_version, codex_version, False, False)

    token = _normalize_revision(source_revision)
    if mode == "seed":
        next_codex = f"{claude_version}+codex.{token}"
        return VersionPlan(claude_version, next_codex, False, next_codex != codex_version)
    if mode == "patch":
        if current_token == token:
            return VersionPlan(claude_version, codex_version, False, False)
        next_core = f"{major}.{minor}.{patch + 1}"
        return VersionPlan(next_core, f"{next_core}+codex.{token}", True, True)
    raise DistributionError(f"unsupported version mode: {mode}")


def _replace_version(path: Path, version: str) -> None:
    text, _ = _read_manifest_version(path)
    replaced, count = VERSION_FIELD.subn(lambda match: f"{match.group(1)}{version}{match.group(3)}", text)
    if count != 1:
        raise DistributionError(f"expected exactly one version field in {path}, found {count}")
    path.write_text(replaced, encoding="utf-8")


def _distribution_targets(repo_root: Path, skill_name: str) -> tuple[Path, Path]:
    return (
        repo_root / "plugin/skills" / skill_name,
        repo_root / "plugins/gtm-ontology-builder/skills" / skill_name,
    )


def _expected_state(repo_root: Path) -> dict[str, dict[str, TreeEntry]]:
    return {
        skill_name: _collect_tree(repo_root / "skills" / skill_name)
        for skill_name in SKILL_NAMES
    }


def sync_distributions(
    repo_root: Path,
    *,
    version_mode: str = "keep",
    source_revision: str | None = None,
) -> SyncResult:
    repo_root = repo_root.resolve()
    expected = _expected_state(repo_root)
    version_plan = _plan_versions(repo_root, version_mode, source_revision)
    changed: list[str] = []

    for skill_name, entries in expected.items():
        for target in _distribution_targets(repo_root, skill_name):
            if _collect_target(target) != entries:
                _write_tree(target, entries)
                changed.append(target.relative_to(repo_root).as_posix())

        archive_path = repo_root / f"{skill_name}.skill"
        archive_bytes = _build_archive(skill_name, entries)
        if not archive_path.is_file() or archive_path.read_bytes() != archive_bytes:
            archive_path.write_bytes(archive_bytes)
            changed.append(archive_path.relative_to(repo_root).as_posix())

    claude_manifest = repo_root / "plugin/.claude-plugin/plugin.json"
    codex_manifest = repo_root / "plugins/gtm-ontology-builder/.codex-plugin/plugin.json"
    if version_plan.claude_changed:
        _replace_version(claude_manifest, version_plan.claude_version)
        changed.append(claude_manifest.relative_to(repo_root).as_posix())
    if version_plan.codex_changed:
        _replace_version(codex_manifest, version_plan.codex_version)
        changed.append(codex_manifest.relative_to(repo_root).as_posix())

    return SyncResult(tuple(changed))


def check_distributions(
    repo_root: Path,
    *,
    source_revision: str | None = None,
) -> tuple[str, ...]:
    repo_root = repo_root.resolve()
    expected = _expected_state(repo_root)
    version_plan = _plan_versions(repo_root, "keep", None)
    drift: list[str] = []

    for skill_name, entries in expected.items():
        for target in _distribution_targets(repo_root, skill_name):
            if _collect_target(target) != entries:
                drift.append(target.relative_to(repo_root).as_posix())
        archive_path = repo_root / f"{skill_name}.skill"
        if not archive_path.is_file() or archive_path.read_bytes() != _build_archive(skill_name, entries):
            drift.append(archive_path.relative_to(repo_root).as_posix())

    if source_revision is not None:
        expected_token = _normalize_revision(source_revision)
        _, codex_version = _read_manifest_version(
            repo_root / "plugins/gtm-ontology-builder/.codex-plugin/plugin.json"
        )
        _, current_token = _parse_versions(version_plan.claude_version, codex_version)
        if current_token != expected_token:
            drift.append("plugins/gtm-ontology-builder/.codex-plugin/plugin.json")
    return tuple(drift)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=default_repo_root())
    subparsers = parser.add_subparsers(dest="command", required=True)

    sync_parser = subparsers.add_parser("sync", help="write generated distributions")
    sync_parser.add_argument(
        "--version-mode", choices=("keep", "seed", "patch"), default="keep"
    )
    sync_parser.add_argument("--source-revision")

    check_parser = subparsers.add_parser("check", help="check without writing")
    check_parser.add_argument("--source-revision")
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        if args.command == "sync":
            result = sync_distributions(
                args.repo_root,
                version_mode=args.version_mode,
                source_revision=args.source_revision,
            )
            if result.changed:
                print("updated distributions:")
                for path in result.changed:
                    print(f"  {path}")
            else:
                print("distributions already synchronized")
            return 0

        drift = check_distributions(args.repo_root, source_revision=args.source_revision)
        if drift:
            print("distribution drift detected:", file=sys.stderr)
            for path in drift:
                print(f"  {path}", file=sys.stderr)
            return 1
        print("distributions are synchronized")
        return 0
    except DistributionError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
