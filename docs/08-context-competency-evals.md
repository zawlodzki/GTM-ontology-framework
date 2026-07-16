# Context competency evaluations

The context competency suite tests whether an agent selects the smallest useful
context, preserves claim provenance, respects governance, chooses the right action,
and keeps live or personal data out of durable output. It evaluates a structured
trace of the response, not the quality of its prose.

Run the checked-in golden responses with:

```bash
python tools/evaluate_context.py evals/context-competency.yaml evals/fixtures/golden.jsonl
```

The command exits zero only when every hard check passes. It prints a deterministic
JSON report with per-case results, per-dimension totals, and token usage. Input and
output tokens are reported for comparison but do not currently have a blocking
threshold.

## Response contract

Provide one JSON object per line and one line per case:

```json
{"case_id":"advance-deal-stage","loaded_artifacts":["gtm-ontology/manifest.yaml"],"cited_refs":["action:advance-deal-stage"],"decision":"propose","action_ref":"action:advance-deal-stage","provenance_refs":[],"persisted_refs":[],"input_tokens":620,"output_tokens":65}
```

`case_id`, `loaded_artifacts`, `cited_refs`, and `decision` are required.
`action_ref`, `provenance_refs`, `persisted_refs`, `input_tokens`, and
`output_tokens` are optional. `persisted_refs` identifies inputs or properties
copied to a durable artifact, note, log, or outbound payload; merely reading a live
value does not put it in this list.

Schemas for suites and responses live in `schemas/context-eval-suite.schema.json`
and `schemas/context-eval-response.schema.json`.

## Hard dimensions

- `routing`: required artifacts and refs are present; forbidden or excess artifacts
  were not loaded.
- `provenance`: required claim provenance is retained and forbidden provenance is
  not used.
- `governance`: the decision is allowed, including abstention and refusal cases.
- `action`: the expected governed action is selected and forbidden actions are not.
- `privacy`: inputs and properties marked as unsafe to persist remain ephemeral.

The suite covers two product groups, the ban on merging their ICPs, an overdue
claim, conflicting claims, a draft action, missing action input, stage advancement,
PII protection, and distractor artifacts. Scenario-only refs such as conflicting
claims and a draft action describe supplied test state; they do not make those
artifacts part of the confirmed example ontology.

## Adding a case

Add the case expectations, then add one response to every fixture. The golden
response must pass all dimensions. A deliberately bad response must fail only the
dimension or dimensions it is intended to exercise. Keep `allowed_artifacts` tight:
it defines the maximum acceptable load, while `required_artifacts` defines the
minimum.

Run the unit suite before committing:

```bash
python -m unittest tools.test_evaluate_context -v
```

CI runs the unit tests, checks the golden fixture, and confirms that each negative
fixture exits non-zero.
