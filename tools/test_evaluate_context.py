from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVALUATOR_PATH = ROOT / "tools" / "evaluate_context.py"
SUITE_PATH = ROOT / "evals" / "context-competency.yaml"
FIXTURES = ROOT / "evals" / "fixtures"


def load_evaluator():
    spec = importlib.util.spec_from_file_location("evaluate_context", EVALUATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load context evaluator")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@unittest.skipUnless(
    importlib.util.find_spec("yaml") and importlib.util.find_spec("jsonschema"),
    "PyYAML and jsonschema are required",
)
class ContextCompetencyEvaluationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.evaluator = load_evaluator()
        cls.suite = cls.evaluator.yaml.safe_load(SUITE_PATH.read_text(encoding="utf-8"))

    def evaluate_fixture(self, name: str) -> dict:
        responses, errors = self.evaluator.read_jsonl(FIXTURES / name)
        self.assertEqual(errors, [])
        return self.evaluator.evaluate(self.suite, responses)

    def failed_dimensions(self, report: dict) -> dict[str, set[str]]:
        return {
            case["case_id"]: {
                dimension
                for dimension, result in case["dimensions"].items()
                if not result["passed"]
            }
            for case in report["cases"]
            if not case["passed"]
        }

    def test_golden_fixture_passes_every_hard_check(self) -> None:
        report = self.evaluate_fixture("golden.jsonl")
        self.assertTrue(report["passed"])
        self.assertEqual(report["summary"]["passed_cases"], 9)
        for dimension in self.evaluator.DIMENSIONS:
            self.assertEqual(
                report["summary"]["dimensions"][dimension],
                {"passed": 9, "total": 9},
            )
        self.assertEqual(report["summary"]["tokens"]["reported_cases"], 9)

    def test_routing_fixture_fails_only_routing(self) -> None:
        report = self.evaluate_fixture("fail-routing.jsonl")
        self.assertFalse(report["passed"])
        self.assertEqual(
            self.failed_dimensions(report),
            {"commerce-analytics-icp": {"routing"}},
        )

    def test_governance_action_fixture_fails_expected_dimensions(self) -> None:
        report = self.evaluate_fixture("fail-governance-action.jsonl")
        self.assertFalse(report["passed"])
        self.assertEqual(
            self.failed_dimensions(report),
            {
                "draft-action": {"action", "governance"},
                "missing-action-input": {"action", "governance"},
                "advance-deal-stage": {"action"},
            },
        )

    def test_provenance_privacy_fixture_fails_expected_dimensions(self) -> None:
        report = self.evaluate_fixture("fail-provenance-privacy.jsonl")
        self.assertFalse(report["passed"])
        self.assertEqual(
            self.failed_dimensions(report),
            {
                "stale-claim": {"provenance"},
                "conflicting-claims": {"provenance"},
                "missing-action-input": {"privacy"},
                "advance-deal-stage": {"privacy"},
                "qualify-with-pii": {"privacy"},
            },
        )

    def test_duplicate_missing_and_unexpected_responses_are_structural_failures(self) -> None:
        responses, errors = self.evaluator.read_jsonl(FIXTURES / "golden.jsonl")
        self.assertEqual(errors, [])
        altered = [*responses[:-1], responses[0], {**responses[0], "case_id": "unexpected-case"}]
        report = self.evaluator.evaluate(self.suite, altered)
        self.assertFalse(report["passed"])
        self.assertEqual(
            report["structural_failures"],
            [
                "duplicate response for commerce-analytics-icp",
                "unexpected response for unexpected-case",
                "missing response for qualify-with-pii",
            ],
        )

    def test_schemas_accept_the_published_suite_and_responses(self) -> None:
        schema_dir = ROOT / "schemas"
        suite_errors = self.evaluator.validation_errors(
            self.suite,
            self.evaluator.load_schema(schema_dir / "context-eval-suite.schema.json"),
        )
        responses, jsonl_errors = self.evaluator.read_jsonl(FIXTURES / "golden.jsonl")
        response_schema = self.evaluator.load_schema(
            schema_dir / "context-eval-response.schema.json"
        )
        response_errors = [
            error
            for response in responses
            for error in self.evaluator.validation_errors(response, response_schema)
        ]
        self.assertEqual(suite_errors, [])
        self.assertEqual(jsonl_errors, [])
        self.assertEqual(response_errors, [])


if __name__ == "__main__":
    unittest.main()
