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
Worked example: `examples/gtm-ontology/` — a complete validated ontology (fictional
B2B SaaS on Pipedrive), exactly what these phases produce — linked via
`context_root` to `examples/company-context/`, a worked company-context tree
(product groups, segments, ICPs, personas, motions, positioning).

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
├── manifest.yaml              may declare context_root -> ../company-context
├── context/glossary.yaml      optional
├── semantic/objects/*.yaml
├── binding/{systems/*.yaml, discovery/<system>/*.yaml, mappings/*.yaml, identity.yaml}
├── dynamic/{processes/*.yaml, automations/*.yaml, actions/*.yaml, loops/*.yaml, prompts/*.md, drafts/*.md}
├── measurement/kpis/*.yaml
├── governance/agent-policy.yaml
└── CHANGELOG.md
```

## Steps

### Phase 0: Scoping

1. Company context first. Look for a company-context tree: a directory whose
   `manifest.yaml` has `kind: company-context-manifest` (conventionally
   `company-context/` at the workspace root; ask if unsure). Present → read its
   manifest and the relevant product-group manifests per `load_when`; do NOT
   re-interview facts it already states (what is sold, to whom, ICP, motions,
   pricing); you will record its path as `context_root` in Phase 5. Absent →
   interview: what is sold, to whom (ICP + disqualifiers), pricing/ACV, cycle
   length, GTM motion, team roles — and distill it into the manifest
   `business_summary`. (A separate context-builder skill for producing the full
   tree is planned; its interim authoring spec is the tree's ARTIFACT-GUIDE.md.)
2. Systems: every GTM app, its role, available access (MCP server? API creds? warehouse?).
   For platform CRMs (Salesforce, HubSpot, Dynamics) also agree WHICH modules/objects
   are in scope and record it in the system profile's `scope` block; the ontology
   covers the CRM module (e.g. Salesforce Sales Cloud: Lead, Account, Contact,
   Opportunity, Task/Event), never the whole platform.
3. Use cases: what should agents ANSWER and DO? These are the ontology's competency questions; they define scope.

Scaffold the `gtm-ontology/` directory tree (layout above), then write
`binding/systems/<id>.yaml` per in-scope system and, when useful, an initial
`context/glossary.yaml`.

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
   triggered; allowed transitions, skip/backward policy. When a company-context
   tree is linked, also ask which product group the pipeline sells and which
   motions feed it → `product_groups` / `gtm_motions` refs (motion ids from the
   motions artifact's `motions:` list).
4. **Every automation**: ask explicitly "what runs OUTSIDE the CRM (n8n, Zapier,
   Make, scripts)?" → `dynamic/automations/<id>.yaml` with trigger, effects, and a
   **data fingerprint** (acting user, field patterns, markers, timing) + failure modes.
5. **KPIs** at company/process/stage level → `measurement/kpis/*.yaml`: formula in
   ontology terms, every term defined, grain, target, owner, source of truth.

**GATE:** confirm per artifact; flip `status: draft` → `confirmed`.

### Phase 4: Agent actions, loops & policy

1. From use cases, propose agent actions. Per action (`templates/action.yaml`):
   preconditions (checkable), inputs, ORDERED workflow with `on_failure` per step,
   effects, **side_effects** (cross-check automations: which will fire? empty list
   = explicit none), approval (`none/required/conditional`), **abstain_when**
   (when the agent stops and asks instead of guessing: missing inputs, low
   confidence, prices/contracts; recommended for every write action), idempotency,
   implementations (MCP tool / endpoint per system).
2. Write `governance/agent-policy.yaml` (`templates/agent-policy.yaml`): the
   **permission ladder** (levels 1–3, promotion criteria — "2 weeks stable
   read-only", "9/10 runs without correction" — and the ceiling: prices, contracts,
   decisions about people never go autonomous), per agent: allowed actions,
   approval overrides, hard prohibitions, rate limits, optional
   `max_permission_level`; defaults incl. `missing_data: stop-and-ask`.
3. Wrap each recurring delegated job in a **loop** (`templates/loop.yaml` →
   `dynamic/loops/<id>.yaml`): steward (`owner` — no steward, no production),
   starting `permission_level: 1`, refs to its actions/prompts/process, weekly
   metrics (share of runs accepted without correction, steward time), journal
   pointer (git commit history is the journal).

**GATE:** user confirms every action contract, the policy, and each loop's
steward + level.

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
10. Every loop has an owner; its levels exist in the agent-policy ladder and
    respect the agent's `max_permission_level`.
11. Every `pii: true` property has `allowed_in_context: false` + `freshness: live-only`.
12. Nothing is past `valid_until`; facts past `last_verified + verify_every` are re-verified.
13. When `context_root` is set: the linked tree exists and every `product-group:` /
    `gtm-motion:` / other context ref resolves (the bundled linter follows
    `context_root` and validates both trees in one run).

Most of the list runs in one call — this skill bundles the linter:

```
python <path-to-this-skill>/tools/lint_ontology.py gtm-ontology/
```

Errors block shipping; warnings are the review list. Checks 3, 5–7 stay manual.

Compile `manifest.yaml` (template: `templates/ontology-manifest.yaml`): business
summary ≤1 paragraph, agent instructions, `context_root` when a company-context
tree exists (relative path, e.g. `../company-context`), every artifact with
≤140-char summary + `load_when` hint. Keep the manifest under ~2k tokens. Add
`CHANGELOG.md` entry, set version.

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

**Rendering (for the user).** This skill bundles the renderer at
`tools/render_ontology.py`. To generate human-facing views of the ontology:

- Prerequisite (once): `pip install pyyaml` (add `jsonschema` for the linter's schema checks).
- Run: `python <path-to-this-skill>/tools/render_ontology.py gtm-ontology/`
  (pass the ontology folder as the argument).
- Output: written to `gtm-ontology/render/` — a process table, a Mermaid funnel, a
  field dictionary, an action catalog, and an interactive `explorer.html`.
- `render/` is GENERATED. Never hand-edit it; regenerate after any ontology change.

See `examples/gtm-ontology/render/` for what the output looks like.

**GATE:** present validation report; user signs off.

### Phase 6: Extension & maintenance (on later invocations)

- **New system:** run Phases 0–5 scoped to it; map onto EXISTING object types first
  (add aliases); extend `identity.yaml`; new objects only for genuinely new concepts.
- **Drift check:** re-run Phase 1, diff snapshots, classify changes (breaking /
  semantic / cosmetic), update bindings, mini-interview for new enum values, bump version.
- **Care mode** (recurring upkeep, 1–2 days a month): run the bundled linter for
  the mechanical health report, then the semantic passes only an LLM can do —
  glossary vs enum definitions, property `semantics` vs business context, prompt
  text vs current field definitions. Review each loop's journal (git history),
  update its metrics, promote or demote it on the ladder per the agent-policy
  criteria. Corrections land as `source: learned` facts with `evidence`, committed.
- **Updates:** prompt or automation changed → update artifact + fingerprint + changelog.

## Elicitation question bank

Use these verbatim when interviewing (Phase 0/3):

- Enum value: "What must be true about the record for this value? Who or what sets
  it: a person (which role), an automation (which one), AI? Can it move backwards?"
- AI field: "What exactly produces this content, with what prompt (verbatim), from
  what inputs? When does it rerun? What does an empty value mean?"
- Pipeline: "Which product group does this pipeline sell? Which GTM motions feed
  it?" (when a company-context tree is linked → `product_groups` / `gtm_motions`)
- Stage: "What must be true before a record ENTERS this stage? What must be true to
  LEAVE it forward? Which fields must be filled? Who owns it? How long before it's
  stuck? What fires automatically here? Which transitions are forbidden?"
- Automation: "What triggers it, what does it write, under which user does it act,
  how do we recognize its output, how does it fail, who notices?"
- KPI: "Exact formula in terms of your data? Grain? Target? Owner? Where do you
  look at it today? What decision does it drive?"
- Action: "Should an agent do this autonomously, with approval, or never? What must
  be verified first, in what order? When should it stop and ask instead of
  proceeding? What must an agent NEVER do here?"
- Loop: "Who stewards this loop? What does an acceptable run look like, and what
  share of runs is acceptable without correction today? What may never be
  automated here? What would promotion to the next ladder level require, and who
  decides? Where do corrections from the weekly review go?"
