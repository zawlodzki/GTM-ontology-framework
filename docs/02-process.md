# The Process

Seven phases. Each has inputs, steps, outputs, and a **gate** — an explicit user confirmation before proceeding. The process is system-agnostic; Phase 1 adapts to whatever access method exists (MCP server, API, warehouse).

Principle throughout — the standard ontology-elicitation loop: **discover → propose → confirm → record.** The AI does the drafting; the human confirms; nothing inferred becomes `confirmed` without a human.

---

## Phase 0 — Scoping

**Goal:** understand the business and decide what the ontology must cover.

Steps:
1. Business context interview (see Question Bank Q0). Capture: what the company sells, to whom (ICP), GTM motion (inbound/outbound/PLG/partner), team roles, sales cycle length, ACV range.
2. Systems inventory: every app in the GTM stack, its role, access method available (MCP / API / warehouse / none).
3. Use cases: what agents should be able to *answer* and *do* — the ontology's **competency questions**. They drive scope: model only what they need (see anti-patterns).
4. Scope decision: which systems and which processes are in scope for this iteration.

**Outputs:** `context/business-context.md`, `context/glossary.yaml` (initial), `binding/systems/<id>.yaml` (one per in-scope system, access section filled).
**Gate:** user confirms scope, systems list, and use cases.

## Phase 1 — Discovery (binding, bottom-up)

**Goal:** a raw, timestamped snapshot of everything each system can tell us.

Per system, introspect via the declared access method and record:
- entities/collections and standard fields
- custom fields **with physical keys** (e.g. Pipedrive 40-char hashes, HubSpot internal names) and types
- enum/dropdown options with option IDs and labels
- pipelines and stages (IDs, order, names)
- users/owners (needed later for automation fingerprints)
- native automations/workflows list (names, triggers if readable)
- record counts and basic profiling (fill rates of key fields — reveals which fields are actually used)

Via MCP: enumerate available tools first; use schema/metadata tools where the server provides them; otherwise sample records and infer. Via API: use metadata endpoints (`/dealFields`, `/properties`, `/stages`…). Via warehouse: information schema (optionally exported as DBML).

**Outputs:** `binding/discovery/<system>/snapshot.yaml` (meta: `retrieved_at`, `via`; body: normalized sections above). Immutable.
**Gate:** none (raw facts), but report anomalies (unused fields, empty pipelines, duplicate-looking fields).

## Phase 2 — Semantic modeling

**Goal:** canonical object model, grounded in discovery + use cases.

Steps:
1. Propose canonical object types; collapse synonyms across systems (`contact`/`subscriber`/`person` → `Person`). Ground every object in discovered entities or an explicit use-case need (a *semantic gap* — record it, don't invent data for it).
2. Map discovered fields to properties; propose canonical names where sources disagree.
3. Draft property semantics: type, description, `filled_by` (infer from profiling: e.g. field always written by user "n8n bot" → `automation`), lifecycle.
4. Enumerate every enum property and list its values — definitions stay empty (`status: draft`) until Phase 3.
5. Define links between objects (from FKs/relations in discovery).
6. Flag semantic gaps: use cases needing concepts with no data anywhere.

**Outputs:** `semantic/objects/<id>.yaml` (drafts), updated glossary.
**Gate:** user confirms object list, property mapping, synonym collapses, and gap list.

## Phase 3 — Business logic elicitation (the human layer)

**Goal:** capture everything that lives outside the systems. This is the phase that turns a schema dump into an ontology. Interview-driven; use the Question Banks below. Everything recorded here is `source: declared`.

Elicit, per artifact:

1. **Enum value definitions** (→ object properties). For each dropdown value: the conditions for it, who/what sets it, whether transitions are ordered. *This includes lifecycle stage fields.*
2. **AI-filled fields** (→ prompts + property `ai:` block). The exact prompt, inputs (e.g. call transcript source), trigger, model, failure behavior. If the prompt lives in n8n/Zapier — extract it verbatim into `dynamic/prompts/<id>.md`.
3. **Processes** (→ `processes/<id>.yaml`). For each pipeline/lifecycle, per stage: entry criteria, exit criteria, **bad examples** (what does NOT suffice — common rep mistakes), **customer verifier** (objective proof on the customer side), forecast **probability**, required properties, tasks (mandatory/optional), communication **drafts** (→ A14 files, verbatim like prompts), tips, valid loss reasons, SLA (target duration + rotting threshold), owner role, automations firing; plus allowed transitions & skip policy.
4. **Automations** (→ `automations/<id>.yaml`). For each workflow found in Phase 1 *plus* any living outside the CRM (n8n, Zapier, Make, custom scripts — ask!): trigger, conditions, effects, **data fingerprint**, failure modes.
5. **KPIs** (→ `kpis/`). Company, process, and stage level; formula in ontology terms; grain; target; owner; where it's reported today.

**Outputs:** filled semantic enum/AI blocks, `dynamic/processes/`, `dynamic/automations/`, `dynamic/prompts/`, `measurement/kpis/`.
**Gate:** per-artifact confirmation; statuses flip to `confirmed`.

## Phase 4 — Agent action layer

**Goal:** define what agents may do, as contracts.

Steps:
1. From the Phase 0 use cases, list candidate actions (create/update records, qualify leads, advance stages, log activities, send sequences…).
2. For each action define: preconditions (in ontology terms — e.g. "all exit criteria of current stage met"), inputs, ordered workflow, effects, side effects (automations it will trigger — cross-check `automations/`!), approval requirement, idempotency, error handling, and per-system implementation (MCP tool name / endpoint).
3. Write `governance/agent-policy.yaml`: agent roles → allowed actions, approval gates, hard prohibitions (e.g. never delete, never email without approval), rate limits.

**Outputs:** `dynamic/actions/<id>.yaml`, `governance/agent-policy.yaml`.
**Gate:** user confirms every action contract and the policy. Actions referencing draft artifacts are invalid.

## Phase 5 — Validation & compilation

**Goal:** internal consistency + the agent entry point.

Checks (automatable; fail = fix before shipping):
1. Every YAML artifact validates against its JSON Schema.
2. Every `kind:id` reference resolves.
3. Every bound physical field exists in the latest discovery snapshot.
4. Every enum value has a definition or an explicit `definition: null # gap` marker.
5. Every process stage has ≥ 1 entry criterion and ≥ 1 required property or an explicit waiver.
6. Every action's preconditions reference confirmed properties/processes; its side effects reference defined automations.
7. Every KPI formula's terms resolve to properties/processes.
8. Every AI-filled property (`filled_by: ai`) has a `prompt_ref` that exists.
9. No confirmed artifact references a draft artifact.
10. Manifest lists every artifact; summaries ≤ 140 chars; manifest under token budget.
11. Every `draft:` reference resolves to an A14 file; every stage `probability` is in [0,1] and non-decreasing along the happy path (terminal: won=1.0, lost=0.0).

Then compile the agent entry points:

1. `manifest.yaml` (Tier 0 index).
2. `gtm-ontology/CLAUDE.md` — the navigation file (template: `templates/ontology-claude.md`):
   reading order (CLAUDE.md → manifest → artifacts per `load_when`), hard rules (drafts,
   policy check, `writable: false`, fingerprints), directory map. Mirror to
   `gtm-ontology/AGENTS.md` if the repo uses that convention.
3. Root registration: insert a marker-delimited block (`<!-- gtm-ontology:start/end -->`)
   into the workspace root `CLAUDE.md` and/or `AGENTS.md` (whichever exist; create root
   `CLAUDE.md` if neither does) pointing to `gtm-ontology/CLAUDE.md`. Replace the block
   on re-runs — idempotent, never duplicated.
4. Optionally human renders via `tools/render_ontology.py` (see `06-client-render.md`).

**Outputs:** `manifest.yaml`, `gtm-ontology/CLAUDE.md`, root registration, validation report, `CHANGELOG.md` entry.
**Gate:** user sign-off on the validation report → version bump.

## Phase 6 — Maintenance & extension

- **Drift detection** (scheduled): re-run Phase 1, diff snapshots. New/renamed/deleted fields, new stages, new automations → open items; bindings referencing removed fields → validation failures.
- **New system** (email marketing, ERP…): run Phases 0–5 scoped to that system; extend `identity.yaml` with cross-system natural keys; add links from new objects to existing ones. Details in `04-extending.md`.
- **Prompt/automation changes**: update artifact + fingerprint, bump version, changelog.

---

# Question Banks

Use verbatim or adapt. Record answers directly into artifacts (`source: declared`, `status: draft` until confirmed).

## Q0 — Business context
- What do you sell, and how is it priced? Typical deal size and sales cycle?
- Who is your ICP (industry, size, geography, buyer persona)? What disqualifies?
- How do leads arrive (channels)? Inbound/outbound/PLG mix?
- Who is on the GTM team and what does each role own?
- What should an AI agent be able to answer or do for you? (drives scope)

## Q1 — Per enum/dropdown value (incl. lifecycle stage)
- What must be TRUE about the record for this value? (conditions, in checkable terms)
- Who or what sets it — a person (which role?), an automation (which?), AI?
- Is it set manually or derived? Can it move backwards (e.g. SQL → MQL)?
- What typically goes wrong with this field? (stale values, misuse)

## Q2 — Per AI-filled field
- What exactly produces the content? (tool, workflow, model)
- What is the exact prompt? (extract verbatim → `prompts/<id>.md`)
- What inputs does it read (transcript source, fields, docs)?
- When does it run / re-run? What happens on failure — empty, stale, or error marker?
- May an agent regenerate it? Under what conditions?

## Q3 — Per pipeline/process stage
- ENTRY: what must be true before a record may enter this stage? Which fields must be filled?
- EXIT: what must be true to leave forward? What sends it to lost/disqualified?
- BAD EXAMPLES: what do reps typically (wrongly) treat as enough to move forward?
- CUSTOMER VERIFIER: what objective proof on the CUSTOMER side confirms this stage is real (booked slot, signed doc, replied email) — not the rep's opinion?
- What win probability does a deal at this stage carry for the forecast (0–100%)?
- Who owns records here? Expected time in stage? After how many days without activity is it rotting?
- Which tasks are mandatory here, which optional? Any standard email/SMS templates used? (collect verbatim → drafts)
- Valid loss reasons when a deal dies at this stage?
- What automations fire on entering/leaving?
- Can stages be skipped? Which transitions are forbidden?
- How do you measure this stage? (conversion, dwell time → KPIs)
- Any tips you give a new rep working this stage?

## Q4 — Per automation (ask also: "what runs OUTSIDE the CRM?")
- Trigger and conditions? Platform (CRM-native / n8n / Zapier / Make / script)?
- What does it write or create? Under which user/API token does it act?
- How can we recognize its output in the data? (→ fingerprint)
- What are its known failure modes? Who notices when it breaks?

## Q5 — Per KPI
- Definition and exact formula — in terms of ontology objects/properties?
- Level (company/process/stage), grain (weekly/monthly/quarterly), segment splits?
- Target? Owner? Where is it reported today (dashboard, spreadsheet)?
- Which decisions does it drive? (kills vanity metrics)

## Q6 — Per agent action
- Should an agent do this autonomously, with approval, or never?
- What must be verified before executing? Correct order of operations?
- What does "done" look like? How do we detect partial failure?
- What must an agent NEVER do in this area?
