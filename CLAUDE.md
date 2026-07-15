# GTM Ontology Framework: project guide

This repo contains the GOF framework (docs, schemas, templates, tools), the
`gtm-ontology-builder` skill source (`skills/gtm-ontology-builder/`), the
`company-context-builder` skill source (`skills/company-context-builder/`), a
complete example ontology instance (`gtm-ontology/`), and its linked
company-context tree (`company-context/`). Framework spec: `README.md` and
`docs/`.

<!-- gtm-ontology:start -->
## GTM Ontology

The business ontology of the GTM stack lives in `gtm-ontology/`. Before working
with CRM data, sales processes, pipelines, or agent actions, read
`gtm-ontology/CLAUDE.md` (navigation rules), then `gtm-ontology/manifest.yaml`
(artifact index). The static company context (product groups, segments, ICPs,
personas, motions, positioning) lives in `company-context/`, linked from the
manifest via `context_root`; follow it only when the task concerns audiences,
market, or products. Never act on artifacts with `meta.status: draft`; check
`gtm-ontology/governance/agent-policy.yaml` before executing any action.
<!-- gtm-ontology:end -->

## Commit Message Format

Scope-prefixed commits: **`scope: description`**. Scope = the area that changed,
not the type of change. Scopes: `gtm-ontology:`, `company-context:`, `skill:`,
`docs:`, `templates:`, `tools:`. Example: `gtm-ontology: add new-business
process with lead scoring`.

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

## Skill Sources and Distribution

The two source skills live under `skills/`. Root framework copies bundled into
`skills/gtm-ontology-builder/` must still be updated there in the same commit.
Plugin payloads and root `.skill` archives are generated downstream artifacts:
never edit or propagate them by hand. GitHub Actions synchronizes them after
changes reach `main`; use `python tools/sync_skill_distributions.py check` for a
read-only drift check. Read `docs/07-skill-distribution.md` for the complete
mapping, automation contract, version policy, and release checks.

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
- Run the linter after any ontology change:
  `python tools/lint_ontology.py gtm-ontology` — 0 errors required (schema
  validation, ref resolution, manifest completeness, pii/temporality, loop/ladder).
  The linter follows the manifest's `context_root` and validates the
  company-context tree in the same run — there is no separate lint command for
  it; run it after `company-context/` changes too.
- Regenerated renders after an ontology change:
  `python tools/render_ontology.py gtm-ontology` — and confirmed it runs clean.

The distribution generator has a standard-library unittest suite under `tools/`.
When a different change has no runnable surface (docs, prose), say so explicitly
instead of claiming it was verified.

## Edit Safety

- Re-read a file right before editing it, especially after 10+ messages or an
  auto-compaction — you may be working from stale state. The Edit tool fails on a
  stale `old_string`. Read files over ~500 lines in chunks with offset/limit.
- When renaming an artifact id, search separately for: its typed refs
  (`type:id`) across all artifacts, its `manifest.yaml` entry, bindings, and any
  string literals in `docs/`, `skills/gtm-ontology-builder/`, and `templates/`.
  Product-group and motion ids are cross-tree identifiers — search both
  `gtm-ontology/` and `company-context/` (motion ids live in the `motions:`
  frontmatter lists) before renaming, then re-run the linter.
- Never delete an artifact without confirming no refs point to it. Never push
  unless explicitly told to.
