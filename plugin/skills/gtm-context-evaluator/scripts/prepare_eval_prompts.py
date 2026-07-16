#!/usr/bin/env python3
"""Create expectation-free JSONL prompts from a GOF context evaluation suite.

Usage:
    python scripts/prepare_eval_prompts.py <cases.yaml> <prompts.jsonl> [--workspace-root PATH]
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

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from evaluate_context import load_schema, validation_errors  # noqa: E402


TRACE_INSTRUCTIONS = (
    "Work only in the supplied local workspace. Inspect manifests first and load "
    "the smallest artifact set needed for the task. Do not mutate files or live "
    "systems. Return one JSON object matching response_contract and report the "
    "artifacts and refs actually used, not an intended or reconstructed trace."
)

RESPONSE_CONTRACT = {
    "required": ["case_id", "loaded_artifacts", "cited_refs", "decision"],
    "optional": [
        "action_ref",
        "provenance_refs",
        "persisted_refs",
        "input_tokens",
        "output_tokens",
    ],
    "decision_values": ["answer", "abstain", "act", "propose", "refuse"],
}


def load_and_validate_suite(path: Path) -> dict[str, Any]:
    suite = yaml.safe_load(path.read_text(encoding="utf-8"))
    schema_path = SCRIPT_DIR.parent / "schemas" / "context-eval-suite.schema.json"
    errors = validation_errors(suite, load_schema(schema_path))
    if errors:
        raise ValueError("invalid suite:\n" + "\n".join(f"- {error}" for error in errors))
    case_ids = [case["id"] for case in suite["cases"]]
    duplicates = sorted({case_id for case_id in case_ids if case_ids.count(case_id) > 1})
    if duplicates:
        raise ValueError(f"duplicate case ids: {', '.join(duplicates)}")
    return suite


def build_prompt(case: dict[str, Any], workspace_root: str) -> dict[str, Any]:
    return {
        "case_id": case["id"],
        "workspace_root": workspace_root,
        "task": case["prompt"],
        "instructions": TRACE_INSTRUCTIONS,
        "response_contract": RESPONSE_CONTRACT,
    }


def write_prompt_pack(suite: dict[str, Any], output: Path, workspace_root: str) -> None:
    rows = [build_prompt(case, workspace_root) for case in suite["cases"]]
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cases", type=Path)
    parser.add_argument("prompts", type=Path)
    parser.add_argument("--workspace-root", default=".")
    args = parser.parse_args(argv)

    try:
        suite = load_and_validate_suite(args.cases)
        write_prompt_pack(suite, args.prompts, args.workspace_root)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(f"wrote {len(suite['cases'])} prompts to {args.prompts}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
