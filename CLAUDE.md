# GTM Ontology Framework: project guide

This repo contains the GOF framework (docs, schemas, templates, tools), the
`gtm-ontology-builder` skill (`skill/`), and a complete example ontology instance
(`gtm-ontology/`). Framework spec: `README.md` and `docs/`.

<!-- gtm-ontology:start -->
## GTM Ontology

The business ontology of the GTM stack lives in `gtm-ontology/`. Before working
with CRM data, sales processes, pipelines, or agent actions, read
`gtm-ontology/CLAUDE.md` (navigation rules), then `gtm-ontology/manifest.yaml`
(artifact index). Never act on artifacts with `meta.status: draft`; check
`gtm-ontology/governance/agent-policy.yaml` before executing any action.
<!-- gtm-ontology:end -->

## Commit Message Format

Scope-prefixed commits: **`scope: description`**. Scope = the area that changed,
not the type of change. Scopes: `gtm-ontology:`, `skill:`, `docs:`, `templates:`,
`tools:`. Example: `gtm-ontology: add new-business process with lead scoring`.

## Working Agreement

### Plan and Build Are Separate Steps

When asked to plan, output only the plan — no edits until approval. When given a
written plan, follow it exactly; if you spot a problem, flag it and wait rather
than improvising. For non-trivial work (3+ steps — a new process, a schema
change, a multi-artifact edit), plan first and confirm intent before editing.

### Phased Execution

Never refactor many artifacts in one response. Work in phases of max 5 files:
complete a phase, validate, get approval before the next.

### Follow References, Not Descriptions

When the user points to an existing artifact, schema, or skill template, match
its patterns exactly. Existing artifacts under `gtm-ontology/` and `templates/`
are a better spec than an English description.

### Work From Raw Data

Trace actual errors — a validator message, a `render_ontology.py` traceback, the
failing YAML/JSON — don't guess. If a report has no output, ask for it.

### One-Word Mode

When the user says "yes," "do it," or "push," execute without repeating the plan
or adding commentary.

### Sub-Agent Swarming for External Research

When a task needs sweeping external documentation — vendor CRM/API docs
(Salesforce, HubSpot, …), schema standards, or several unrelated sources — launch
parallel sub-agents, one per source, each with its own context window. A single
agent reading dozens of external pages decays; parallel agents keep each search
focused and return only the conclusion you need.

## Artifact & Schema Conventions

- Artifacts reference each other by typed refs (`object:...`, `process:...`,
  `action:...`, etc.), never by file path. Preserve that form when editing.
- Every artifact must validate against its schema in `schemas/`. Ontology
  artifacts also obey the rules in `gtm-ontology/CLAUDE.md`.
- Renders under `gtm-ontology/render/` are GENERATED. Never hand-edit them;
  regenerate after any ontology change.
- Never act on artifacts with `meta.status: draft`, and check
  `gtm-ontology/governance/agent-policy.yaml` before executing any action.
- Write human prose in docs and artifact descriptions — no robotic comment
  blocks or filler section headers. Simple and correct beats elaborate; don't
  model for scenarios the ontology doesn't have.

## Verification

Never report a task complete until you have, as applicable:

- Validated changed YAML/JSON artifacts against their schema in `schemas/`
  (`manifest.schema.json`, `process.schema.json`, `object-type.schema.json`, …).
- Regenerated renders after an ontology change:
  `python tools/render_ontology.py gtm-ontology` — and confirmed it runs clean.

There is no automated test suite or build step; when a change has no runnable
surface (docs, prose), say so explicitly instead of claiming it was verified.

## Edit Safety

- Re-read a file right before editing it, especially after 10+ messages or an
  auto-compaction — you may be working from stale state. The Edit tool fails on a
  stale `old_string`. Read files over ~500 lines in chunks with offset/limit.
- When renaming an artifact id, search separately for: its typed refs
  (`type:id`) across all artifacts, its `manifest.yaml` entry, bindings, and any
  string literals in `docs/`, `skill/`, and `templates/`.
- Never delete an artifact without confirming no refs point to it. Never push
  unless explicitly told to.
