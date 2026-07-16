# Artifact Formats

Field-by-field specification. JSON Schemas in `schemas/` are normative for structure; this doc is normative for meaning. Commented starter files in `templates/`.

Shared rules:
- Encoding UTF-8, YAML 1.2, 2-space indent.
- Every YAML artifact: `kind`, `id`, `meta` (provenance envelope; see `01-concepts.md` §3).
- References: `kind:id` strings (`object:deal`, `property:deal.lifecycle_stage`, `automation:lead-scoring`).
- `R` = required, `O` = optional.

---

## A0: `manifest.yaml` (Tier 0 index)

| Field | R/O | Type | Notes |
|---|---|---|---|
| `kind` | R | `manifest` | |
| `ontology` | R | string | kebab-case instance id |
| `version` | R | semver string | |
| `updated` | R | date | |
| `business_summary` | R | string | ≤ 1 paragraph. The only prose an agent always has. |
| `agent_instructions` | O | string | how to navigate tiers |
| `context_root` | O | string | relative path to a company-context tree (see "Context artifacts" below); lint/render resolve refs across both trees |
| `systems[]` | R | list | `{id, role, access}`; role: crm/email-marketing/erp/…; access: mcp/api/warehouse |
| `artifacts[]` | R | list | `{path, kind, summary (≤140 chars), load_when}` |

`load_when` is an agent hint: *"working with deals, stages, forecasting"*.

(A1 `business-context.md` is retired — the company-context tree plus the manifest `business_summary` replaced it.)

## A2: `glossary.yaml`

```yaml
kind: glossary
id: glossary
meta: {...}
terms:
  - term: MQL
    definition: >
      Marketing-qualified lead: ...        # in checkable business terms
    synonyms: [marketing qualified lead]
    maps_to: property:person.lifecycle_stage=mql   # optional ontology ref
```

## A3: `objects/<id>.yaml` (object type)

| Field | R/O | Type | Notes |
|---|---|---|---|
| `kind` | R | `object-type` | |
| `id`, `name`, `description` | R | | id kebab-case, name PascalCase |
| `meta` | R | envelope | |
| `aliases[]` | O | strings | source-system synonyms collapsed into this type |
| `properties[]` | R | list | see below |
| `links[]` | O | list | `{id, label (UPPER_SNAKE), target (object:ref), cardinality (one-to-one/one-to-many/many-to-one/many-to-many), semantics}` |

**Property object:**

| Field | R/O | Notes |
|---|---|---|
| `id` | R | snake_case |
| `name` | R | display name |
| `type` | R | `string/text/number/currency/boolean/date/datetime/enum/set/reference/json/phone/email/url/user/address` (`set` = multi-select; per-CRM mapping in `05-crm-type-mapping.md`) |
| `semantics` | R | what the value MEANS; when it changes; how to interpret edge cases |
| `filled_by` | R | `human / automation / ai / integration / system / mixed` |
| `filled_by_detail` | O | ref or prose: which role/automation/integration |
| `user_access` | O | `editable / read-only / mixed` — is a **user** meant to fill it, or is it read-only because a machine writes it? Orthogonal to `filled_by` (the source) and to binding `writable` (agent write per system). Omit if implied by `filled_by`; state it explicitly when `filled_by: mixed` or when a machine-sourced value must never be hand-edited |
| `required` | O | boolean or `from_stage: <process stage ref>` |
| `default` | O | default value on record creation |
| `validation` | O | validation rule, e.g. `regex:^[0-9]{10}$` (tax id) or expression; agents validate before write |
| `enum[]` | R if type=enum | see below |
| `ai` | R if filled_by=ai | `{prompt_ref (prompt:id), inputs[], trigger, regenerate_policy}` |
| `quality_notes` | O | known issues (stale, misused) |
| `pii` | O | `true` = personal data. Forces `allowed_in_context: false` and `freshness: live-only` (schema-enforced): the value stays in the source system, read live, never copied into the repo, a prompt, or long-lived context |
| `allowed_in_context` | O | may the VALUE appear in repo files / prompts / agent context? `false` for pii. Independent of read access via bindings |
| `retention` | O | retention rule enforced in the source system, in prose (e.g. "delete 24 months after last activity") |
| `freshness` | O | `live-only / static`. `live-only` = never materialize the value into a file (pipeline stage, scores, pii) — the "CRM export in the repo" anti-pattern becomes machine-checkable; `static` = a cached copy is fine between verifications (enrichment fields) — pair with `last_verified` / `verify_every` in the property `meta` |
| `meta` | O | per-property provenance override; also carries `last_verified` / `verify_every` / `valid_from` / `valid_until` for facts with a shelf life |

**Enum value object:** `{value, label, definition (R, business conditions for this value), set_by (R, who/what sets it), entry_conditions[] (O, checkable conditions), reversible (O bool)}`.

The `lifecycle_stage` pattern: model as an enum property AND, if it has ordered transitions/criteria, also as a `process` of type `lifecycle` referencing the property. The enum holds per-value definitions; the process holds transition logic.

## A4: `systems/<id>.yaml`

| Field | R/O | Notes |
|---|---|---|
| `kind` | R | `system` |
| `id`, `name`, `meta` | R | |
| `role` | R | `crm / email-marketing / erp / billing / support / enrichment / automation-platform / other` |
| `vendor` | O | |
| `scope` | O, **required for platform CRMs** (Salesforce, HubSpot, Dynamics) | `{modules_in_scope[], objects_in_scope[], excluded[], notes}`; limits discovery and bindings to the CRM module; see `05-crm-type-mapping.md` |
| `access[]` | R | list of methods, each: `{via: mcp/api/warehouse, ...}`; mcp: `{server, key_tools[]}`; api: `{base_url, auth, docs_url}`; warehouse: `{dataset, loaded_by}` |
| `write_access` | R | `none / limited / full` + notes |
| `rate_limits` | O | |
| `environment_notes` | O | sandboxes, admin contacts |

## A5: `discovery/<system>/snapshot.yaml`

Envelope is normative; body sections normalized but system-flavored:

```yaml
kind: discovery-snapshot
id: pipedrive-2026-07-06
system: system:pipedrive
meta: {source: discovered, status: confirmed, retrieved_at: ..., via: mcp}
entities: []        # {name, kind, record_count, fields: [{key, name, type, custom (bool), enum_options: [{id, label}]}]}
pipelines: []       # {id, name, stages: [{id, name, order}]}
users: []           # {id, name, email, is_bot_or_api (bool)}
automations_found: []  # {id?, name, trigger_hint, platform}
profiling: []       # {field, fill_rate, distinct_values_sample}
```

Immutable once written. New run = new file; keep at least the previous one for diffs.

## A6: `mappings/<system>.yaml`

Maps semantic → physical. One file per system.

```yaml
kind: binding
id: pipedrive
system: system:pipedrive
meta: {...}
objects:
  - object: object:deal
    entity: deals                      # physical collection
    id_field: id
    properties:
      - property: lifecycle_stage     # semantic property id
        field_key: "9f1a...c3"        # PHYSICAL key (custom-field hash / internal name)
        transform: enum_options        # none | enum_options | currency | datetime_tz | expression
        enum_map: {123: mql, 124: sql} # option-id → canonical value
        writable: true                 # may an agent write it via this system?
        visibility:                    # optional CRM UI config (binding concern)
          pipelines: [New Business]    # where the field is shown; [] = all
          important_on_stage: qualified # stage where CRM highlights it
        notes: ...
```

Every `field_key` must exist in the latest discovery snapshot (validation check #3).

## A7: `identity.yaml`

Cross-system identity resolution (record linkage with MDM-style survivorship) **and**
intra-base deduplication (which records are the same real-world entity, which merely
look alike):

```yaml
kind: identity
id: identity
meta: {...}
resolutions:
  - object: object:person
    natural_keys: [email]              # ordered by preference
    sources:                           # systems contributing this object
      - {system: "system:pipedrive", role: master}
      - {system: "system:mailerlite", role: secondary}
    inclusion: union                   # union | intersection
    conflict_strategy: master_wins     # master_wins | most_recent | per_field
    per_field: []                      # if per_field: [{property, winner: system ref}]
    match: {...}                       # dedup rules, see below (optional)
```

### `match`: deduplication rules (optional per resolution)

`natural_keys` answer "what *joins* two records"; `match` answers the harder question:
"what proves two records are the **same** entity, and what proves they are genuinely
**different**." Without it, a naive dedup on a shared key merges records that should stay
apart — e.g. two branch offices of one company: same `name`, same `domain`, different
`address` are **not** duplicates.

```yaml
    match:
      keys:                            # combinations that assert "same record"; strongest first
        - {fields: [vat_id], type: deterministic}                 # one field, exact
        - {fields: [domain, address_locality], type: deterministic} # combination, ALL equal (after normalize)
        - {fields: [name, address_postal_code], type: probabilistic,
           similarity: {name: 0.9}, on_match: review}             # fuzzy → never auto-merge
      distinguishing_fields:           # differ ⇒ records are DISTINCT; vetoes an auto-merge even if a key matches
        - {field: address, reason: "branch offices share domain+name but are separate sites"}
        - {field: vat_id,  reason: "distinct legal entities never merge"}
      never_match_on:                  # forbidden as a whole/sole key: non-unique or shared across legit-distinct records
        - {fields: [domain], reason: "every branch shares one domain"}
        - {fields: [name],   reason: "non-unique; parent and subsidiary collide"}
      merge:
        auto: "a deterministic key matches AND no distinguishing_field differs"
        review: "a probabilistic key matches OR any distinguishing_field differs"
        loser: redirect_refs           # fate of the merged-away record: redirect_refs | soft_delete | keep_linked
```

**Rules for choosing fields** (the whole point of this block):

- **A match key must be unique per real entity.** A national tax/VAT id or a personal
  email is a valid single-field key. A `domain`, company `name`, or generic
  `info@`-style email is **not** — put those in `never_match_on`, or use them only
  inside a *combination* that adds a distinguishing dimension (`[domain, address_locality]`).
- **`distinguishing_fields` are the veto.** If any of them differs beyond its tolerance,
  the records are different entities regardless of what the keys say. This is what keeps
  branches, franchises, `ship-to`/`bill-to` sites, and namesakes from collapsing into one.
- **Deterministic vs. probabilistic.** Deterministic keys (exact match after
  normalization) may auto-merge. Probabilistic keys (`similarity` thresholds, fuzzy name
  match) must route to `review` — they surface candidates, they never merge on their own.
- **Normalization is assumed.** Compare lower-cased, trimmed, punctuation-stripped values
  (domains without `www.`/scheme, phones in E.164). State non-obvious normalization in the
  field's `semantics` or a `reason`.
- **`merge.loser`** declares what happens to the record that loses survivorship, so refs
  (`object:` links, deal history) are not orphaned.

## A8: `processes/<id>.yaml`

| Field | R/O | Notes |
|---|---|---|
| `kind` | R | `process` |
| `id`, `name`, `description`, `meta` | R | |
| `type` | R | `pipeline / lifecycle / workflow` |
| `operational_status` | O | `active / deprecated / archived` — state **in the CRM**, distinct from `meta.status` (ontology confirmation). `active` = new records enter it; `deprecated` = closed to new records, open ones still finish; `archived` = read-only history, agents route nothing here |
| `object` | R | `object:` ref the process moves |
| `state_property` | R | `property:` ref holding current state (stage field, lifecycle enum) |
| `product_groups[]` | O | `product-group:` refs — which product group(s) this pipeline sells; requires manifest `context_root` |
| `gtm_motions[]` | O | `gtm-motion:` refs — which motion(s) feed this pipeline; motion ids come from the motions artifact's `motions:` list |
| `stages[]` | R | see below |
| `transitions` | R | `{allowed: [[from,to],...], skip_policy: forbidden/allowed/approval, backward_policy: ...}` |
| `kpis[]` | O | process-level `kpi:` refs |

**Stage object:**

| Field | R/O | Notes |
|---|---|---|
| `id`, `name`, `order` | R | |
| `definition` | R | what being in this stage MEANS |
| `entry_criteria[]` | R | `{description (R, business terms), check (O, machine-checkable expression over properties)}` |
| `exit_criteria[]` | R | same shape; criteria to leave *forward* |
| `bad_examples[]` | O | what does NOT suffice to exit; negative guard for AI classification and rep discipline |
| `customer_verifier` | O | `{description (R), check (O)}`; objective proof on the CUSTOMER side (booked slot, signed doc), not rep opinion; anti-sandbagging |
| `probability` | O | 0.0–1.0 forecast weight (pipeline processes; maps to `deal_probability` / HubSpot `metadata.probability`) |
| `required_properties[]` | O | property ids that must be non-empty in this stage |
| `owner_role` | O | |
| `sla` | O | `{target_duration_days (expected time, feeds stage-time KPI), rotting_threshold_days (no activity for N days → rotting alert; Pipedrive `rotten_days`), stuck_action}` |
| `tasks` | O | `{mandatory[], optional[]}`; rep checklists; agents verify completeness / create activities |
| `drafts` | O | `{email: draft:<id> or null, sms: draft:<id> or null}`; refs to A14 communication templates |
| `tips` | O | short guidance for the rep working this stage |
| `loss_reasons[]` | O | valid loss reasons when exiting to a negative terminal stage; keep consistent with a `lost_reason` enum property if one exists |
| `automations_triggered[]` | O | `automation:` refs firing on entry/exit |
| `kpis[]` | O | stage-level `kpi:` refs |
| `terminal` | O | bool (`won`, `lost`) + `outcome: positive/negative` |

`check` expressions: simple boolean expressions over `property` ids (`budget_confirmed == true && amount != null`). Not executed by the framework; they exist so agents/validators can evaluate them.

## A9: `automations/<id>.yaml`

| Field | R/O | Notes |
|---|---|---|
| `kind` | R | `automation` |
| `id`, `name`, `description`, `meta` | R | |
| `platform` | R | `crm-native / n8n / zapier / make / custom-script / other` |
| `status_live` | R | `active / paused / unknown` |
| `trigger` | R | `{event, object (ref), conditions[]}` |
| `effects[]` | R | `{target (property/object ref), operation: write/create/delete/notify/external, detail}` |
| `data_fingerprint` | R | how to recognize its output: `{acting_user, field_patterns[], marker (e.g. note prefix), timing}`; at least one |
| `failure_modes[]` | O | `{symptom, impact, detection}` |
| `owner` | O | who maintains it |
| `definition_url` | O | link to n8n workflow / CRM automation |

## A10: `actions/<id>.yaml`

| Field | R/O | Notes |
|---|---|---|
| `kind` | R | `action` |
| `id`, `name`, `description`, `meta` | R | |
| `object` | R | primary `object:` ref |
| `intent` | R | when an agent should reach for this action |
| `executor` | R | `agent / human / either` |
| `approval` | R | `none / required / conditional` (+ `approval_condition`) |
| `context` | O schema / R for new `agent` or `either` actions | Minimal context contract: `required_static_refs[]`, property-only `required_live_refs[]`, `optional_refs[]`, `forbidden_to_persist[]` (`input:<id>` or `property:<object>.<property>`), and `response_mode: concise / detailed / file-reference`. Do not repeat workflow. Confirmed legacy actions without it lint as a warning. Every required live PII or `freshness: live-only` property must be forbidden to persist. |
| `preconditions[]` | R | `{description, check (O)}`; must be verifiable from ontology terms |
| `abstain_when[]` | O | `{description, check (O)}`; when the agent STOPS and asks the loop steward instead of proceeding: missing inputs, low confidence, price/contract territory. Never fill the gap with a guess. Recommended for every action with write effects; actions without it fall back to `defaults.missing_data` in agent-policy |
| `inputs[]` | R | `{id, type, required, description}` |
| `workflow[]` | R | ORDERED steps: `{step, description, on_failure (abort/skip/compensate + detail)}` |
| `effects[]` | R | what changes: `{target, operation, detail}` |
| `side_effects[]` | R | `automation:` refs this will trigger + external effects (emails!). Empty list = explicit "none". |
| `postconditions[]` | O | how to verify success |
| `idempotency` | R | `safe_to_retry / not_idempotent / conditional` + notes |
| `implementations[]` | R | `{system (ref), via (mcp/api), tool_or_endpoint, notes}` |
| `error_handling` | O | prose fallback |

## A11: `prompts/<id>.md`

YAML frontmatter: `kind: prompt`, `id`, `meta`, `used_by[]` (property/action refs), `model`, `inputs[]` (`{id, description, source}`), `output_contract` (format + where it's written), `version`. Body = the verbatim prompt. Never paraphrase a production prompt: extract it exactly; it's provenance.

## A12: `kpis/<id>.yaml` (grouping into one file allowed)

| Field | R/O | Notes |
|---|---|---|
| `kind` | R | `kpi` |
| `id`, `name`, `meta` | R | |
| `level` | R | `company / process / stage` |
| `scope` | R if level≠company | `process:` or `process:id/stage` ref |
| `definition` | R | prose meaning |
| `formula` | R | in ontology terms: `count(deal where ...) / count(deal where ...)` |
| `terms` | R | map: every formula term → definition with property/process refs |
| `grain` | R | `daily/weekly/monthly/quarterly` |
| `segments[]` | O | split dimensions (property refs) |
| `target` | O | `{operator, value, unit}` |
| `owner` | R | role |
| `source_of_truth` | O | where reported today |

## A13: `agent-policy.yaml`

```yaml
kind: agent-policy
id: agent-policy
meta: {...}
permission_ladder:                    # the trust progression for loops (A15)
  levels:
    - {level: 1, name: read-only, description: "reads live data and reports; no writes"}
    - {level: 2, name: propose-then-approve, description: "prepares every write; a human approves"}
    - {level: 3, name: autonomous-with-log, description: "acts alone; steward reviews the log"}
  promotion:                          # default criteria; a loop may override
    - {from: 1, to: 2, criteria: ["min. 2 weeks of stable read-only, zero unauthorized writes"]}
    - {from: 2, to: 3, criteria: ["9/10 weekly runs need no correction, 4 consecutive weeks"]}
  ceiling:                            # what never goes autonomous
    - {description: "Prices, contracts, and decisions about people always go through a human.",
       max_level: 2, applies_to: [property:deal.amount]}
agents:
  - id: sdr-agent
    description: ...
    allowed_actions: [action:qualify-lead, action:advance-deal-stage]
    approval_overrides: []            # {action, approval: required, condition}
    prohibitions:                     # hard NOs, in prose; override everything
      - Never delete any record.
      - Never contact a person outside declared channels.
    rate_limits: {actions_per_hour: 30}
    max_permission_level: 2           # cap across every loop this agent runs
defaults:
  unlisted_actions: forbidden         # actions not granted are forbidden
  draft_artifacts: read-as-hypothesis-only
  missing_data: stop-and-ask          # no data = stop, never invent (schema-enforced const)
  pii_data: read-live-only-never-copy # default handling of pii-flagged properties
```

The ladder is defined once, here. Each loop carries its **current** `permission_level` (A15); the lint checks the level exists on the ladder and respects the agent's cap. `missing_data: stop-and-ask` is a schema-enforced constant — the one non-negotiable containment rule.

## A14: `drafts/<id>.md` (communication template)

YAML frontmatter: `kind: draft`, `id`, `meta`, `channel` (`email/sms/linkedin/other`),
`used_by[]` (process-stage refs), `language`, `variables[]` (`{id, source}`; where each
placeholder value comes from, in ontology terms), `approval` (`required` by default;
agents never send external communication autonomously unless agent-policy explicitly
grants it). Body = the template with `{{placeholders}}`.

Referenced from stages via `drafts: {email: draft:<id>, sms: draft:<id>}`.

## A15: `loops/<id>.yaml` (loop)

The loop ("obieg") is the unit of delegated work and of trust: someone starts it, the agent does the work on live data, someone checks, something closes. Trust grows per loop, not per agent. The ladder (A13) gates the loop as a whole: level 1 — the loop runs no write actions at all; level 2 — every write waits for human approval, regardless of the action's own `approval`; level 3 — action contracts apply as written, the steward reviews the journal.

| Field | R/O | Notes |
|---|---|---|
| `kind` | R | `loop` |
| `id`, `name`, `description`, `meta` | R | |
| `owner` | R | the steward. A loop without a steward does not go to production |
| `agent` | O | agent id from agent-policy running this loop; lint cross-checks it |
| `permission_level` | R | current rung on the A13 ladder |
| `target_level` | O | where the loop is headed; not every loop should reach 3 |
| `promotion_criteria[]` | O | loop-specific overrides of the ladder's default promotion criteria |
| `refs` | R | `{actions[] (R), prompts[] (O), process (O)}` — typed refs to what the loop runs |
| `metrics[]` | R | `{id, description, cadence, target (O)}`. The two staples: share of runs accepted without correction, steward time per week — measured weekly, they gate promotion |
| `journal` | R | pointer to the loop journal; git commit history is the journal for free (e.g. `CHANGELOG.md + git log -- dynamic/loops/<id>.yaml`) |
| `escalation` | O | where abstains and failed runs go |

A loop has no `approval` field of its own: approval semantics live in the actions it references, the ladder gates the loop. Corrections from the weekly review return to the ontology as `source: learned` facts with `evidence` pointing at the run or journal entry.

## Context artifacts (company-context tree)

The company-context tree linked via manifest `context_root` has its own artifact set, built before the ontology (see `01-concepts.md` Layer 0). Three schema contracts in `schemas/`:

- **`company-context-manifest.schema.json`** — the tree's root `manifest.yaml` (`kind: company-context-manifest`): `id`, `version`, `updated`, `company {id, name, domain}`, `artifacts[] {id, kind, path, summary ≤140, load_when}`, `product_groups[] {id, path, summary, load_when}`, optional `authoring_guide`.
- **`product-group-manifest.schema.json`** — one `manifest.yaml` per group (`kind: product-group-manifest`): `id` (= the group id that `product-group:` refs resolve to), `name`, `summary`, `inherits[]` (company artifact ids), `artifacts[]`, `products[]` (same entry shape).
- **`context-artifact.schema.json`** — shared frontmatter for every content artifact (`company-profile`, `company-strategy`, `commercial-model`, `operating-model`, `market-overview`, `competitor-landscape`, `product-group-strategy`, `segment`, `use-case`, `icp`, `personas`, `buying-context`, `gtm-motions`, `positioning`, `value-propositions`, `messaging`, `product-context`): `kind`, `id`, `meta {source, status, ...}`, optional `scope` and typed-ref fields. A `gtm-motions` artifact must declare its `motions[] {id, name, summary}` list — those ids are the canonical `gtm-motion:` ref targets.

The deep per-kind content spec (what a segment, ICP, or positioning artifact must say) lives in the tree's own `ARTIFACT-GUIDE.md`, which the planned context-builder skill will own. Guide files (`kind: company-context-readme / -agent-guide / -artifact-guide`) are documentation, not artifacts: lint and render skip them.
