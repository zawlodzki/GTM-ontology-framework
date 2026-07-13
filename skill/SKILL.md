---
name: gtm-ontology-builder
description: >
  Build an agent-ready business ontology for GTM systems (Pipedrive, HubSpot, Attio,
  Salesforce, email marketing, ERP). Use when the user wants to create, extend, or update an
  ontology of their CRM/GTM stack: map objects and custom fields with business
  semantics, define lifecycle/dropdown value conditions, document AI-filled fields
  and their prompts, model pipelines with entry/exit criteria, catalogue automations,
  define agent actions and KPIs. Triggers: "ontology", "zbuduj ontologię", "map my
  CRM", "model my sales process", "document my pipeline for agents".
---

# GTM Ontology Builder

Build an ontology per the GTM Ontology Framework (GOF): a 4-layer, machine-readable
model of the business: semantic (what exists), binding (where data lives), dynamic
(what happens / what agents may do), measurement & governance (KPIs, policy).

Artifact formats: `references/artifact-formats.md` (field-by-field spec).
Starter templates: `templates/`. Copy a template, fill it, keep the structure.

Core rules (apply throughout):

1. **Discover → propose → confirm → record.** Never mark anything `status: confirmed`
   without explicit user confirmation. Facts introspected from a system are
   `source: discovered`; your proposals are `inferred`; user statements are `declared`.
2. **No invention.** Only model properties that exist in a system or that the user
   explicitly declares. Missing concepts = semantic gaps, recorded, not fabricated.
3. **Scope = agent use cases.** Model what the stated use cases need, nothing more.
4. **One gate per phase.** Present results, wait for explicit confirmation, then write.

All output goes to a **`gtm-ontology/` folder at the workspace root** (create it in
Phase 0), using this instance layout:

```
gtm-ontology/
├── CLAUDE.md                  agent navigation file (written in Phase 5)
├── manifest.yaml
├── context/{business-context.md, glossary.yaml}
├── semantic/objects/*.yaml
├── binding/{systems/*.yaml, discovery/<system>/*.yaml, mappings/*.yaml, identity.yaml}
├── dynamic/{processes/*.yaml, automations/*.yaml, actions/*.yaml, prompts/*.md, drafts/*.md}
├── measurement/kpis/*.yaml
├── governance/agent-policy.yaml
└── CHANGELOG.md
```

## Steps

### Phase 0: Scoping

Interview the user:
1. Business: what is sold, to whom (ICP + disqualifiers), pricing/ACV, cycle length, GTM motion, team roles.
2. Systems: every GTM app, its role, available access (MCP server? API creds? warehouse?).
   For platform CRMs (Salesforce, HubSpot, Dynamics) also agree WHICH modules/objects
   are in scope and record it in the system profile's `scope` block; the ontology
   covers the CRM module (e.g. Salesforce Sales Cloud: Lead, Account, Contact,
   Opportunity, Task/Event), never the whole platform.
3. Use cases: what should agents ANSWER and DO? These are the ontology's competency questions; they define scope.

Scaffold the `gtm-ontology/` directory tree (layout above), then write
`context/business-context.md` (template: `templates/business-context.md`),
`binding/systems/<id>.yaml` per in-scope system, initial `context/glossary.yaml`.

**GATE:** user confirms scope, systems, use cases.

### Phase 1: Discovery

Scope guard first: if the system profile has a `scope` block, introspect ONLY
`objects_in_scope` (a full Salesforce describe returns hundreds of objects; never
enumerate them all) and record the skipped-object count in the snapshot.

Per system, introspect via the declared access method:
- MCP: enumerate available tools; prefer metadata/schema tools (`list_*_fields`,
  `list_stages`, `get_properties`); sample records where no metadata tool exists.
- API: metadata endpoints (Pipedrive `/dealFields`, `/stages`; HubSpot `/properties/*`;
  Attio `/objects`; Salesforce `/sobjects/{object}/describe` + Tooling API for flows
  and validation rules).
- Warehouse: information schema.

Record into `binding/discovery/<system>/snapshot-<date>.yaml`: entities + fields
(with PHYSICAL keys: custom-field hashes/internal names), enum options with IDs,
pipelines/stages with IDs, users (flag bots/API users), automations found, fill-rate
profiling of key fields.

Report anomalies (unused fields, duplicates, empty pipelines). No gate; these are raw facts.

### Phase 2: Semantic modeling

1. Propose canonical object types; collapse synonyms across systems (contact/subscriber → Person). Present the mapping table: discovered entity → object type → confidence.
2. Map fields → properties; propose canonical names for cross-system conflicts.
3. Infer `filled_by` per property from profiling (bot user writes → `automation`); mark `inferred`.
4. List every enum property with values; definitions stay `null` (gaps for Phase 3).
5. Propose links between objects; flag semantic gaps (use case needs X, no data).

Write draft `semantic/objects/*.yaml` (template: `templates/object-type.yaml`) and
`binding/mappings/<system>.yaml` (template: `templates/binding.yaml`; every
`field_key` must exist in the snapshot). If >1 system: `binding/identity.yaml`
(natural keys, master source, conflict strategy; ask, don't assume).

**GATE:** user confirms objects, mappings, collapses, gaps.

### Phase 3: Business logic elicitation

The human layer: interview, one topic at a time, record as `source: declared`:

1. **Every enum value** (incl. lifecycle stages): "What must be TRUE for this value?
   Who/what sets it? Reversible?" → `enum[].definition`, `set_by`, `entry_conditions`.
2. **Every AI-filled field**: "What produces it? Exact prompt? Inputs? Trigger?
   Failure behavior?" → `ai:` block + verbatim prompt in `dynamic/prompts/<id>.md`
   (never paraphrase production prompts).
3. **Every pipeline/lifecycle** → `dynamic/processes/<id>.yaml`: per stage:
   definition, entry criteria, exit criteria (pair prose `description` with
   machine-checkable `check` where possible), **bad_examples** (what does NOT
   suffice to exit; ask for common rep mistakes), **customer_verifier** (objective
   proof on the customer side, not rep opinion), **probability** (forecast weight
   0.0–1.0), required properties, tasks (mandatory/optional), drafts (email/SMS
   templates; collect verbatim → `dynamic/drafts/<id>.md`), tips, loss_reasons,
   owner, SLA (`target_duration_days` + `rotting_threshold_days`), automations
   triggered; allowed transitions, skip/backward policy.
4. **Every automation**: ask explicitly "what runs OUTSIDE the CRM (n8n, Zapier,
   Make, scripts)?" → `dynamic/automations/<id>.yaml` with trigger, effects, and a
   **data fingerprint** (acting user, field patterns, markers, timing) + failure modes.
5. **KPIs** at company/process/stage level → `measurement/kpis/*.yaml`: formula in
   ontology terms, every term defined, grain, target, owner, source of truth.

**GATE:** confirm per artifact; flip `status: draft` → `confirmed`.

### Phase 4: Agent actions & policy

1. From use cases, propose agent actions. Per action (`templates/action.yaml`):
   preconditions (checkable), inputs, ORDERED workflow with `on_failure` per step,
   effects, **side_effects** (cross-check automations: which will fire? empty list
   = explicit none), approval (`none/required/conditional`), idempotency,
   implementations (MCP tool / endpoint per system).
2. Write `governance/agent-policy.yaml`: per agent: allowed actions, approval
   overrides, hard prohibitions, rate limits. Default: unlisted actions forbidden.

**GATE:** user confirms every action contract + policy.

### Phase 5: Validation & compilation

Run all checks; fix failures before shipping:
1. Every artifact parses and matches its format spec.
2. Every `kind:id` reference resolves.
3. Every bound `field_key` exists in the latest snapshot.
4. Every enum value has a definition (or explicit `null` gap marker).
5. Every stage has ≥1 entry criterion.
6. Action preconditions/side effects reference confirmed artifacts only.
7. KPI formula terms resolve.
8. Every `filled_by: ai` property has an existing `prompt_ref`.
9. No confirmed artifact references a draft.

Compile `manifest.yaml` (template: `templates/ontology-manifest.yaml`): business
summary ≤1 paragraph, agent instructions, every artifact with ≤140-char summary +
`load_when` hint. Keep the manifest under ~2k tokens. Add `CHANGELOG.md` entry,
set version.

**Wire up agent discovery** (how any future agent finds and navigates the ontology):

1. Write `gtm-ontology/CLAUDE.md` from `templates/ontology-claude.md`; fill the
   company name, the concrete `writable: false` field list, and key action names.
   If the repo uses the AGENTS.md convention, mirror identical content to
   `gtm-ontology/AGENTS.md`.
2. Register the ontology in the workspace root:
   - root `CLAUDE.md` exists → insert the block below; on re-runs REPLACE the
     content between the markers (idempotent), never duplicate it;
   - root `AGENTS.md` exists → do the same there (update both if both exist);
   - neither exists → create root `CLAUDE.md` containing the block.

```markdown
<!-- gtm-ontology:start -->
## GTM Ontology
The business ontology of our GTM stack lives in `gtm-ontology/`. Before working
with CRM data, sales processes, pipelines, or agent actions, read
`gtm-ontology/CLAUDE.md` (navigation rules), then `gtm-ontology/manifest.yaml`
(artifact index). Never act on artifacts with `meta.status: draft`; check
`gtm-ontology/governance/agent-policy.yaml` before executing any action.
<!-- gtm-ontology:end -->
```

Optionally generate human-facing views (process table, funnel, explorer.html) with
the framework's `tools/render_ontology.py gtm-ontology/` when the framework repo
is available.

**GATE:** present validation report; user signs off.

### Phase 6: Extension & maintenance (on later invocations)

- **New system:** run Phases 0–5 scoped to it; map onto EXISTING object types first
  (add aliases); extend `identity.yaml`; new objects only for genuinely new concepts.
- **Drift check:** re-run Phase 1, diff snapshots, classify changes (breaking /
  semantic / cosmetic), update bindings, mini-interview for new enum values, bump version.
- **Updates:** prompt or automation changed → update artifact + fingerprint + changelog.

## Elicitation question bank

Use these verbatim when interviewing (Phase 0/3):

- Enum value: "What must be true about the record for this value? Who or what sets
  it: a person (which role), an automation (which one), AI? Can it move backwards?"
- AI field: "What exactly produces this content, with what prompt (verbatim), from
  what inputs? When does it rerun? What does an empty value mean?"
- Stage: "What must be true before a record ENTERS this stage? What must be true to
  LEAVE it forward? Which fields must be filled? Who owns it? How long before it's
  stuck? What fires automatically here? Which transitions are forbidden?"
- Automation: "What triggers it, what does it write, under which user does it act,
  how do we recognize its output, how does it fail, who notices?"
- KPI: "Exact formula in terms of your data? Grain? Target? Owner? Where do you
  look at it today? What decision does it drive?"
- Action: "Should an agent do this autonomously, with approval, or never? What must
  be verified first, in what order? What must an agent NEVER do here?"
