---
name: gtm-context-evaluator
description: >
  Evaluate whether an AI agent uses a local GOF company-context and GTM ontology
  correctly, with deterministic checks for minimal routing, claim provenance,
  freshness and conflicts, governance and abstention, action selection, and PII or
  live-only data protection. Use when Codex needs to create or run competency evals
  for company-context/ and gtm-ontology/, verify an agent before deployment, compare
  context-loading strategies, or diagnose a failed GOF context evaluation without
  depending on GitHub Actions or a checkout of the framework repository.
---

# GTM Context Evaluator

Evaluate structured traces of agent behavior against project-specific competency
cases. Work entirely in the user's local workspace. Do not require GitHub, a plugin
checkout, or network access.

## Core contract

Treat the evaluator as a test harness, not as the agent being tested. Keep case
expectations out of the tested agent's prompt. Record one response per case with:

- `case_id`, `loaded_artifacts`, `cited_refs`, and `decision`;
- optional `action_ref`, `provenance_refs`, and `persisted_refs`;
- optional `input_tokens` and `output_tokens` for reporting only.

Decisions are `answer`, `abstain`, `act`, `propose`, or `refuse`. A loaded artifact
is a file actually read for the case. A persisted ref is live input or property data
copied into a durable artifact, note, log, or outbound payload; reading it ephemerally
does not count as persistence.

## Run an existing suite

Install the two runtime dependencies when unavailable:

```bash
python -m pip install pyyaml jsonschema
```

Run the evaluator from the installed skill directory:

```bash
python <path-to-this-skill>/scripts/evaluate_context.py <cases.yaml> <responses.jsonl>
```

Require exit code zero for a golden run. Intentionally incorrect fixtures must exit
non-zero and fail only their intended dimensions. The JSON report separates routing,
provenance, governance, action, and privacy checks. Token totals have no blocking
threshold unless the context owner explicitly approves one.

## Build a project-specific suite

Inventory the local trees before writing cases:

1. Read `company-context/manifest.yaml` and each relevant product-group manifest.
2. Read `company-context/claims.yaml` only when the manifest declares a registry.
3. Read `gtm-ontology/manifest.yaml`, `gtm-ontology/CLAUDE.md`, and the agent policy.
4. Resolve the actions, processes, prompts, bindings, properties, and inputs needed
   by the intended cases.
5. Copy `assets/context-competency.template.yaml` into the user's workspace and
   replace every `replace-*` id, ref, path, and prompt with confirmed local values.

Include only applicable cases. Aim to cover product-group routing and distractors,
ICP separation, stale or conflicting claims, draft governance, missing action input,
stage transitions, action choice, and PII/live-only protection. Omit a category when
the local trees contain no confirmed basis for it, and report that coverage gap.

Validate the tailored suite and create a prompt pack that does not expose case
descriptions or expectations:

```bash
python <path-to-this-skill>/scripts/prepare_eval_prompts.py \
  evals/context-competency.yaml evals/prompts.jsonl \
  --workspace-root .
```

Run each prompt-pack line in a fresh local agent context when possible. Give the
agent access only to the named workspace root and any explicit ephemeral inputs for
that scenario. Collect the agent's actual structured trace in `responses.jsonl`,
then score it with `scripts/evaluate_context.py`.

## Evaluation integrity

- Build cases from the actual local manifests and artifact contracts. Never assume
  example ids, product groups, actions, properties, or paths exist.
- Give the tested agent the task and admissible runtime inputs, never the expectation
  block or golden answer.
- Use a fresh context for each case when the environment supports isolated agents.
- Keep scenario-only draft artifacts and conflicting claims in isolated fixtures;
  never insert them into confirmed company context or ontology.
- Do not mutate CRM systems or other live sources while evaluating.
- Preserve raw response traces so failures can be reproduced.

## Authoring rule

Keep `required_artifacts` as the minimum correct load and `allowed_artifacts` as
the maximum acceptable load. A golden trace must pass every hard check; a negative
trace must demonstrate that the intended failure is detected. Report coverage gaps
instead of inventing expectations that cannot be derived from confirmed artifacts.
