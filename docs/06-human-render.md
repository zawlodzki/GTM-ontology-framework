# Human Render

Principle: **the sales team never reads YAML.** The ontology is the single source of truth;
humans get renders. One place to edit, no drifting copies.

Tooling: `python tools/render_ontology.py <ontology-dir>` generates everything below
into `<ontology-dir>/render/`: per-process table + Mermaid funnel (`process-<id>.md`),
field dictionary (`fields.md`), action catalog (`actions.md`), artifact reference graph
(`graph.md`; loops render as nodes with edges to their actions, prompts, and process),
and a self-contained interactive `explorer.html` (funnel with per-stage
business logic, objects, actions, automations with fingerprints, KPIs, graph view).

## Renders

### 1. Process table (from A8)

Markdown table: **columns = stages, rows = keys**. Row order:

definition, entry criteria, exit criteria, what does NOT suffice (`bad_examples`),
customer verifier, probability, required fields (labels, not ids), mandatory tasks,
SLA (target / rotting), owner, automations (names), KPIs, loss reasons, tips.

Skip empty rows. Use property/automation display `name`s, never ids or field keys.

### 2. Kanban (from A8)

Mermaid flowchart: one node per stage (`name` + probability), arrows = `transitions.allowed`,
terminal stages styled by `outcome`. Gives the sales team the shape of the funnel at a glance.

### 3. Field dictionary (from A3 + A6)

Per object, a table: label | type | required (from stage) | who fills it (`filled_by`) |
options (enum labels). Physical field keys and bindings stay out; they are implementation detail.

## Rules

- Renders are **generated, never hand-edited**; regenerate after every ontology version bump.
- Render language follows the sales team (labels/values may be Polish while ontology ids stay English).
- Renders carry a footer: ontology id, version, `updated` date, so a stale printout is detectable.
- The agent-facing view is the ontology itself (manifest + artifacts); renders are for humans only.
