from __future__ import annotations

import json
import os
import tempfile
import unittest
import zipfile
from pathlib import Path

from tools import sync_skill_distributions as sync


class SyncSkillDistributionsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.repo = Path(self.temporary_directory.name)
        for skill_name in sync.SKILL_NAMES:
            source = self.repo / "skills" / skill_name
            source.mkdir(parents=True)
            (source / "SKILL.md").write_text(f"# {skill_name}\n", encoding="utf-8")

        self.claude_manifest = self.repo / "plugin/.claude-plugin/plugin.json"
        self.codex_manifest = self.repo / "plugins/gtm-ontology-builder/.codex-plugin/plugin.json"
        self._write_manifest(self.claude_manifest, "1.4.0")
        self._write_manifest(self.codex_manifest, "1.4.0+codex.previous")

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    @staticmethod
    def _write_manifest(path: Path, version: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps({"name": "gtm-ontology-builder", "version": version}, indent=2) + "\n",
            encoding="utf-8",
        )

    @staticmethod
    def _version(path: Path) -> str:
        return json.loads(path.read_text(encoding="utf-8"))["version"]

    def test_sync_mirrors_sources_and_removes_stale_or_cache_files(self) -> None:
        source = self.repo / "skills/gtm-ontology-builder"
        (source / "nested").mkdir()
        (source / "nested/data.txt").write_text("payload\n", encoding="utf-8")
        (source / ".DS_Store").write_bytes(b"ignored")
        (source / "nested/__pycache__").mkdir()
        (source / "nested/__pycache__/module.pyc").write_bytes(b"ignored")

        stale_target = self.repo / "plugin/skills/gtm-ontology-builder"
        stale_target.mkdir(parents=True)
        (stale_target / "stale.txt").write_text("remove me", encoding="utf-8")

        result = sync.sync_distributions(self.repo)

        self.assertIn("plugin/skills/gtm-ontology-builder", result.changed)
        for target in sync._distribution_targets(self.repo, "gtm-ontology-builder"):
            self.assertEqual((target / "nested/data.txt").read_text(encoding="utf-8"), "payload\n")
            self.assertFalse((target / "stale.txt").exists())
            self.assertFalse((target / ".DS_Store").exists())
            self.assertFalse((target / "nested/__pycache__").exists())

    def test_archives_are_reproducible_and_have_one_top_level_directory(self) -> None:
        source_file = self.repo / "skills/company-context-builder/SKILL.md"
        first_result = sync.sync_distributions(self.repo)
        archive_path = self.repo / "company-context-builder.skill"
        first_archive = archive_path.read_bytes()

        os.utime(source_file, (1_900_000_000, 1_900_000_000))
        second_result = sync.sync_distributions(self.repo)

        self.assertIn("company-context-builder.skill", first_result.changed)
        self.assertNotIn("company-context-builder.skill", second_result.changed)
        self.assertEqual(first_archive, archive_path.read_bytes())
        with zipfile.ZipFile(archive_path) as archive:
            names = archive.namelist()
            self.assertTrue(names)
            self.assertTrue(all(name.startswith("company-context-builder/") for name in names))
            self.assertNotIn(".DS_Store", "\n".join(names))
            self.assertNotIn("__pycache__", "\n".join(names))

    def test_context_evaluator_is_packaged_as_plugin_skills_and_archive(self) -> None:
        source = self.repo / "skills/gtm-context-evaluator"
        (source / "scripts").mkdir()
        (source / "scripts/evaluate_context.py").write_text("print('ok')\n", encoding="utf-8")

        result = sync.sync_distributions(self.repo)

        self.assertIn("gtm-context-evaluator.skill", result.changed)
        for target in sync._distribution_targets(self.repo, "gtm-context-evaluator"):
            self.assertEqual(
                (target / "scripts/evaluate_context.py").read_text(encoding="utf-8"),
                "print('ok')\n",
            )
        with zipfile.ZipFile(self.repo / "gtm-context-evaluator.skill") as archive:
            names = archive.namelist()
            self.assertIn(
                "gtm-context-evaluator/scripts/evaluate_context.py",
                names,
            )

    def test_check_detects_drift_without_writing(self) -> None:
        sync.sync_distributions(self.repo)
        target = self.repo / "plugin/skills/company-context-builder/SKILL.md"
        target.write_text("drift\n", encoding="utf-8")

        drift = sync.check_distributions(self.repo)

        self.assertIn("plugin/skills/company-context-builder", drift)
        self.assertEqual(target.read_text(encoding="utf-8"), "drift\n")

    def test_seed_preserves_core_and_patch_bumps_only_once_per_revision(self) -> None:
        first_revision = "6f4f858e3cd6b84adcede82c728b92eb75b4b3d5"
        next_revision = "0123456789abcdef0123456789abcdef01234567"

        sync.sync_distributions(
            self.repo, version_mode="seed", source_revision=first_revision
        )
        self.assertEqual(self._version(self.claude_manifest), "1.4.0")
        self.assertEqual(self._version(self.codex_manifest), "1.4.0+codex.6f4f858e3cd6")

        no_bump = sync.sync_distributions(
            self.repo, version_mode="patch", source_revision=first_revision
        )
        self.assertNotIn("plugin/.claude-plugin/plugin.json", no_bump.changed)
        self.assertEqual(self._version(self.claude_manifest), "1.4.0")

        bumped = sync.sync_distributions(
            self.repo, version_mode="patch", source_revision=next_revision
        )
        self.assertIn("plugin/.claude-plugin/plugin.json", bumped.changed)
        self.assertEqual(self._version(self.claude_manifest), "1.4.1")
        self.assertEqual(self._version(self.codex_manifest), "1.4.1+codex.0123456789ab")

        sync.sync_distributions(
            self.repo, version_mode="patch", source_revision=next_revision
        )
        self.assertEqual(self._version(self.claude_manifest), "1.4.1")

    def test_check_can_require_the_packaged_source_revision(self) -> None:
        revision = "6f4f858e3cd6b84adcede82c728b92eb75b4b3d5"
        sync.sync_distributions(self.repo, version_mode="seed", source_revision=revision)

        self.assertEqual(sync.check_distributions(self.repo, source_revision=revision), ())
        drift = sync.check_distributions(
            self.repo, source_revision="0123456789abcdef0123456789abcdef01234567"
        )
        self.assertIn("plugins/gtm-ontology-builder/.codex-plugin/plugin.json", drift)

    def test_mismatched_manifest_versions_are_rejected_before_writing(self) -> None:
        self._write_manifest(self.codex_manifest, "1.3.0+codex.previous")

        with self.assertRaisesRegex(sync.DistributionError, "version cores differ"):
            sync.sync_distributions(self.repo)

        self.assertFalse((self.repo / "gtm-ontology-builder.skill").exists())

    def test_source_symlinks_are_rejected(self) -> None:
        source = self.repo / "skills/company-context-builder"
        try:
            (source / "linked.md").symlink_to(source / "SKILL.md")
        except (OSError, NotImplementedError):
            self.skipTest("symlinks are not available on this platform")

        with self.assertRaisesRegex(sync.DistributionError, "symlinks are not supported"):
            sync.sync_distributions(self.repo)


if __name__ == "__main__":
    unittest.main()
