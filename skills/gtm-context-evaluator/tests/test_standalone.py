from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = SKILL_ROOT / "scripts"
TEMPLATE = SKILL_ROOT / "assets" / "context-competency.template.yaml"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@unittest.skipUnless(
    importlib.util.find_spec("yaml") and importlib.util.find_spec("jsonschema"),
    "PyYAML and jsonschema are required",
)
class StandaloneContextEvaluatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.evaluator = load_module("standalone_evaluator", SCRIPTS / "evaluate_context.py")
        cls.preparer = load_module("standalone_preparer", SCRIPTS / "prepare_eval_prompts.py")

    def test_template_validates(self) -> None:
        suite = self.evaluator.yaml.safe_load(TEMPLATE.read_text(encoding="utf-8"))
        schema = self.evaluator.load_schema(
            SKILL_ROOT / "schemas" / "context-eval-suite.schema.json"
        )
        self.assertEqual(self.evaluator.validation_errors(suite, schema), [])

    def test_prompt_pack_does_not_leak_expectations_or_descriptions(self) -> None:
        suite = self.preparer.load_and_validate_suite(TEMPLATE)
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "prompts.jsonl"
            self.preparer.write_prompt_pack(suite, output, ".")
            raw = output.read_text(encoding="utf-8")
            rows = [json.loads(line) for line in raw.splitlines()]
        self.assertEqual(len(rows), len(suite["cases"]))
        self.assertNotIn("expectations", raw)
        self.assertNotIn("description", raw)
        self.assertNotIn("allowed_decisions", raw)
        self.assertEqual(rows[0]["case_id"], suite["cases"][0]["id"])
        self.assertEqual(rows[0]["workspace_root"], ".")

    def test_duplicate_case_ids_are_rejected(self) -> None:
        suite = self.evaluator.yaml.safe_load(TEMPLATE.read_text(encoding="utf-8"))
        suite["cases"].append(dict(suite["cases"][0]))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "duplicate.yaml"
            path.write_text(self.evaluator.yaml.safe_dump(suite), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "duplicate case ids"):
                self.preparer.load_and_validate_suite(path)

    def test_runner_passes_self_contained_golden_trace(self) -> None:
        suite = {
            "kind": "context-eval-suite",
            "id": "standalone-smoke",
            "version": "0.1.0",
            "cases": [
                {
                    "id": "minimal-routing",
                    "description": "Load exactly the manifest.",
                    "prompt": "Read the local manifest.",
                    "expectations": {
                        "required_artifacts": ["company-context/manifest.yaml"],
                        "allowed_artifacts": ["company-context/manifest.yaml"],
                        "forbidden_artifacts": [],
                        "required_refs": [],
                        "required_provenance_refs": [],
                        "forbidden_provenance_refs": [],
                        "allowed_decisions": ["answer"],
                        "expected_action_ref": None,
                        "forbidden_action_refs": [],
                        "forbidden_persisted_refs": [],
                    },
                }
            ],
        }
        response = {
            "case_id": "minimal-routing",
            "loaded_artifacts": ["company-context/manifest.yaml"],
            "cited_refs": [],
            "decision": "answer",
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            cases = root / "cases.yaml"
            responses = root / "responses.jsonl"
            cases.write_text(self.evaluator.yaml.safe_dump(suite), encoding="utf-8")
            responses.write_text(json.dumps(response) + "\n", encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SCRIPTS / "evaluate_context.py"), str(cases), str(responses)],
                capture_output=True,
                text=True,
            )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue(json.loads(result.stdout)["passed"])


if __name__ == "__main__":
    unittest.main()
