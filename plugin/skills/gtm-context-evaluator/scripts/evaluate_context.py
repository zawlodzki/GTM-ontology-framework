#!/usr/bin/env python3
"""Evaluate structured agent responses against GOF context competency cases.

Usage:
    python scripts/evaluate_context.py <cases.yaml> <responses.jsonl>

The evaluator is deterministic. It validates both input contracts, reports each
hard dimension separately, reports token totals when supplied, and exits 1 when
any response is missing, invalid, duplicated, unexpected, or fails a hard check.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Iterable

try:
    import yaml
except ImportError as exc:  # pragma: no cover - CLI environment guard
    raise SystemExit("PyYAML is required: python -m pip install pyyaml") from exc

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError as exc:  # pragma: no cover - CLI environment guard
    raise SystemExit("jsonschema is required: python -m pip install jsonschema") from exc


DIMENSIONS = ("routing", "provenance", "governance", "action", "privacy")


def load_schema(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validation_errors(value: Any, schema: dict[str, Any]) -> list[str]:
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(value), key=lambda item: list(item.absolute_path))
    return [
        f"{'.'.join(str(part) for part in error.absolute_path) or '<root>'}: {error.message}"
        for error in errors
    ]


def read_jsonl(path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    rows: list[dict[str, Any]] = []
    errors: list[str] = []
    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not raw.strip():
            continue
        try:
            value = json.loads(raw)
        except json.JSONDecodeError as exc:
            errors.append(f"line {number}: invalid JSON: {exc.msg}")
            continue
        if not isinstance(value, dict):
            errors.append(f"line {number}: response must be a JSON object")
            continue
        rows.append(value)
    return rows, errors


def difference(required: Iterable[str], actual: set[str]) -> list[str]:
    return sorted(set(required) - actual)


def intersection(forbidden: Iterable[str], actual: set[str]) -> list[str]:
    return sorted(set(forbidden) & actual)


def score_case(case: dict[str, Any], response: dict[str, Any]) -> dict[str, Any]:
    expected = case["expectations"]
    loaded = set(response["loaded_artifacts"])
    cited = set(response["cited_refs"])
    provenance = set(response.get("provenance_refs") or [])
    persisted = set(response.get("persisted_refs") or [])
    action_ref = response.get("action_ref")

    checks: dict[str, list[str]] = {dimension: [] for dimension in DIMENSIONS}

    missing_artifacts = difference(expected["required_artifacts"], loaded)
    excess_artifacts = sorted(loaded - set(expected["allowed_artifacts"]))
    forbidden_artifacts = intersection(expected["forbidden_artifacts"], loaded)
    if missing_artifacts:
        checks["routing"].append(f"missing artifacts: {', '.join(missing_artifacts)}")
    if excess_artifacts:
        checks["routing"].append(f"excess artifacts: {', '.join(excess_artifacts)}")
    if forbidden_artifacts:
        checks["routing"].append(f"forbidden artifacts: {', '.join(forbidden_artifacts)}")
    missing_refs = difference(expected["required_refs"], cited)
    if missing_refs:
        checks["routing"].append(f"missing cited refs: {', '.join(missing_refs)}")

    missing_provenance = difference(expected["required_provenance_refs"], provenance)
    forbidden_provenance = intersection(expected["forbidden_provenance_refs"], provenance)
    if missing_provenance:
        checks["provenance"].append(f"missing provenance refs: {', '.join(missing_provenance)}")
    if forbidden_provenance:
        checks["provenance"].append(f"forbidden provenance refs: {', '.join(forbidden_provenance)}")

    if response["decision"] not in expected["allowed_decisions"]:
        checks["governance"].append(
            f"decision {response['decision']!r} not in {expected['allowed_decisions']}"
        )

    expected_action = expected.get("expected_action_ref")
    if expected_action is not None and action_ref != expected_action:
        checks["action"].append(f"expected {expected_action}, got {action_ref or '<none>'}")
    forbidden_actions = set(expected.get("forbidden_action_refs") or [])
    if action_ref in forbidden_actions:
        checks["action"].append(f"forbidden action: {action_ref}")
    if expected_action is None and action_ref is not None and response["decision"] not in {"act", "propose"}:
        checks["action"].append(f"unexpected action for decision {response['decision']}: {action_ref}")

    forbidden_persisted = intersection(expected["forbidden_persisted_refs"], persisted)
    if forbidden_persisted:
        checks["privacy"].append(f"forbidden persisted refs: {', '.join(forbidden_persisted)}")

    dimensions = {
        dimension: {"passed": not messages, "failures": messages}
        for dimension, messages in checks.items()
    }
    return {
        "case_id": case["id"],
        "passed": all(item["passed"] for item in dimensions.values()),
        "dimensions": dimensions,
        "tokens": {
            "input": response.get("input_tokens"),
            "output": response.get("output_tokens"),
        },
    }


def evaluate(suite: dict[str, Any], responses: list[dict[str, Any]]) -> dict[str, Any]:
    case_index: dict[str, dict[str, Any]] = {}
    structural: list[str] = []
    for case in suite["cases"]:
        case_id = case["id"]
        if case_id in case_index:
            structural.append(f"duplicate case id: {case_id}")
            continue
        case_index[case_id] = case
    response_index: dict[str, dict[str, Any]] = {}
    for response in responses:
        case_id = response["case_id"]
        if case_id in response_index:
            structural.append(f"duplicate response for {case_id}")
        response_index[case_id] = response
        if case_id not in case_index:
            structural.append(f"unexpected response for {case_id}")
    for case_id in case_index:
        if case_id not in response_index:
            structural.append(f"missing response for {case_id}")

    results = [
        score_case(case_index[case_id], response_index[case_id])
        for case_id in case_index
        if case_id in response_index
    ]
    dimension_totals = {
        dimension: {
            "passed": sum(result["dimensions"][dimension]["passed"] for result in results),
            "total": len(results),
        }
        for dimension in DIMENSIONS
    }
    token_rows = [result["tokens"] for result in results]
    return {
        "suite_id": suite["id"],
        "passed": not structural and len(results) == len(case_index) and all(result["passed"] for result in results),
        "structural_failures": structural,
        "summary": {
            "passed_cases": sum(result["passed"] for result in results),
            "total_cases": len(case_index),
            "dimensions": dimension_totals,
            "tokens": {
                "input": sum(row["input"] for row in token_rows if row["input"] is not None),
                "output": sum(row["output"] for row in token_rows if row["output"] is not None),
                "reported_cases": sum(
                    row["input"] is not None or row["output"] is not None for row in token_rows
                ),
            },
        },
        "cases": results,
    }


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cases", type=Path)
    parser.add_argument("responses", type=Path)
    args = parser.parse_args(argv)

    schema_dir = Path(__file__).resolve().parents[1] / "schemas"
    suite = yaml.safe_load(args.cases.read_text(encoding="utf-8"))
    suite_errors = validation_errors(suite, load_schema(schema_dir / "context-eval-suite.schema.json"))
    responses, jsonl_errors = read_jsonl(args.responses)
    response_schema = load_schema(schema_dir / "context-eval-response.schema.json")
    response_errors = [
        f"response {index}: {message}"
        for index, response in enumerate(responses, start=1)
        for message in validation_errors(response, response_schema)
    ]
    input_errors = [*(f"suite: {error}" for error in suite_errors), *jsonl_errors, *response_errors]
    if input_errors:
        report = {"passed": False, "input_failures": input_errors}
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1

    report = evaluate(suite, responses)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
