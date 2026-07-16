from __future__ import annotations

import importlib.util
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LINTER = ROOT / "tools" / "lint_ontology.py"
PYTHON = sys.executable


@unittest.skipUnless(importlib.util.find_spec("yaml"), "PyYAML is not installed")
class ActionContextLintTests(unittest.TestCase):
    def copy_instance(self, directory: str) -> tuple[Path, Path]:
        root = Path(directory)
        ontology = root / "gtm-ontology"
        context = root / "company-context"
        shutil.copytree(ROOT / "gtm-ontology", ontology)
        shutil.copytree(ROOT / "company-context", context)
        return ontology, context

    def run_linter(self, ontology: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [PYTHON, str(LINTER), str(ontology)],
            capture_output=True,
            text=True,
        )

    def rewrite(self, path: Path, old: str, new: str) -> None:
        text = path.read_text(encoding="utf-8")
        self.assertIn(old, text)
        path.write_text(text.replace(old, new, 1), encoding="utf-8")

    def test_current_example_has_valid_action_contexts(self) -> None:
        result = self.run_linter(ROOT / "gtm-ontology")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("action-context", result.stdout)

    def test_confirmed_agent_action_without_context_warns(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            ontology, _ = self.copy_instance(directory)
            action = ontology / "dynamic" / "actions" / "qualify-lead.yaml"
            text = action.read_text(encoding="utf-8")
            start, end = text.index("context:\n"), text.index("\npreconditions:\n", text.index("context:\n"))
            action.write_text(text[:start] + text[end + 1 :], encoding="utf-8")
            result = self.run_linter(ontology)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("WARNINGS", result.stdout)
        self.assertIn("action-context", result.stdout)

    def test_unknown_protected_input_is_an_error(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            ontology, _ = self.copy_instance(directory)
            action = ontology / "dynamic" / "actions" / "qualify-lead.yaml"
            self.rewrite(action, "    - input:transcript\n", "    - input:missing-input\n")
            result = self.run_linter(ontology)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unknown input:missing-input", result.stdout)

    def test_unknown_protected_property_is_an_error(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            ontology, _ = self.copy_instance(directory)
            action = ontology / "dynamic" / "actions" / "qualify-lead.yaml"
            self.rewrite(action, "    - property:deal.stage\n", "    - property:deal.missing\n")
            result = self.run_linter(ontology)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unknown property:deal.missing", result.stdout)

    def test_non_mapping_context_is_reported_without_crashing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            ontology, _ = self.copy_instance(directory)
            action = ontology / "dynamic" / "actions" / "qualify-lead.yaml"
            text = action.read_text(encoding="utf-8")
            start = text.index("context:\n")
            end = text.index("\npreconditions:\n", start)
            action.write_text(text[:start] + "context: invalid\n" + text[end + 1 :], encoding="utf-8")
            result = self.run_linter(ontology)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("context must be an object", result.stdout)
        self.assertNotIn("Traceback", result.stderr)

    def test_object_type_without_id_is_reported_without_crashing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            ontology, _ = self.copy_instance(directory)
            object_type = ontology / "semantic" / "objects" / "deal.yaml"
            self.rewrite(object_type, "id: deal\n", "")
            result = self.run_linter(ontology)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("schema", result.stdout)
        self.assertNotIn("Traceback", result.stderr)

    def test_unknown_live_property_is_an_error(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            ontology, _ = self.copy_instance(directory)
            action = ontology / "dynamic" / "actions" / "advance-deal-stage.yaml"
            self.rewrite(action, "    - property:deal.amount\n", "    - property:deal.missing\n")
            result = self.run_linter(ontology)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unknown property:deal.missing", result.stdout)

    def test_live_only_property_must_be_forbidden_to_persist(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            ontology, _ = self.copy_instance(directory)
            action = ontology / "dynamic" / "actions" / "qualify-lead.yaml"
            marker = "  forbidden_to_persist:\n    - input:transcript\n    - property:deal.stage\n"
            self.rewrite(action, marker, "  forbidden_to_persist:\n    - input:transcript\n")
            result = self.run_linter(ontology)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("property:deal.stage is pii/live-only", result.stdout)


if __name__ == "__main__":
    unittest.main()
