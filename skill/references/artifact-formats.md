# Artifact Formats

Field-by-field specification. JSON Schemas in `schemas/` are normative for structure; this doc is normative for meaning. Commented starter files in `templates/`.

Shared rules:
- Encoding UTF-8, YAML 1.2, 2-space indent.
- Every YAML artifact: `kind`, `id`, `meta` (provenance envelope — see `01-concepts.md` §3).
- References: `kind:id` strings (`object:deal`, `property:deal.lifecycle_stage`, `automation:lead-scoring`).
- `R` = required, `O` = optional.

---

## A0 — `manifest.yaml` (Tier 0 index)

| Field | R/O | Type | Notes |
|---|---|---|---|
| `kind` | R | `manifest` | |
| `ontology` | R | string | kebab-case instance id |
| `version` | R | semver string | |
| `updated` | R | date | |
| `business_summary` | R | string | ≤ 1 paragraph. The only prose an agent always has. |
| `agent_instructions` | O | string | how to navigate tiers |
| `systems[]` | R | list | `{id, role, access}` — role: crm/email-marketing/erp/…; access: mcp/api/warehouse |
| `artifacts[]` | R | list | `{path, kind, summary (≤140 chars), load_when}` |

`load_when` is an agent hint: *"working with deals, stages, forecasting"*.

## A1 — `business-context.md`

Markdown with YAML frontmatter (`kind: business-context`, `id`, `meta`). Required sections: `## Company & Offer`, `## ICP`, `## GTM Motion`, `## Team & Roles`, `## Agent Use Cases`. Keep ≤ 100 lines; it feeds interviews, not agent runtime (agents get `business_summary` from the manifest).

## A2 — `glossary.yaml`

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

## A3 — `objects/<id>.yaml` (object type)

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
| `required` | O | boolean or `from_stage: <process stage ref>` |
| `default` | O | default value on record creation |
| `validation` | O | validation rule, e.g. `regex:^[0-9]{10}$` (tax id) or expression; agents validate before write |
| `enum[]` | R if type=enum | see below |
| `ai` | R if filled_by=ai | `{prompt_ref (prompt:id), inputs[], trigger, regenerate_policy}` |
| `quality_notes` | O | known issues (stale, misused) |
| `meta` | O | per-property provenance override |

**Enum value object:** `{value, label, definition (R — business conditions for this value), set_by (R — who/what sets it), entry_conditions[] (O — checkable conditions), reversible (O bool)}`.

The `lifecycle_stage` pattern: model as an enum property AND, if it has ordered transitions/criteria, also as a `process` of type `lifecycle` referencing the property. The enum holds per-value definitions; the process holds transition logic.

## A4 — `systems/<id>.yaml`

| Field | R/O | Notes |
|---|---|---|
| `kind` | R | `system` |
| `id`, `name`, `meta` | R | |
| `role` | R | `crm / email-marketing / erp / billing / support / enrichment / automation-platform / other` |
| `vendor` | O | |
| `access[]` | R | list of methods, each: `{via: mcp/api/warehouse, ...}` — mcp: `{server, key_tools[]}`; api: `{base_url, auth, docs_url}`; warehouse: `{dataset, loaded_by}` |
| `write_access` | R | `none / limited / full` + notes |
| `rate_limits` | O | |
| `environment_notes` | O | sandboxes, admin contacts |

## A5 — `discovery/<system>/snapshot.yaml`

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

## A6 — `mappings/<system>.yaml`

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

## A7 — `identity.yaml`

Cross-system identity resolution (record linkage with MDM-style survivorship):

```yaml
kind: identity
id: identity
meta: {...}
resolutions:
  - object: object:person
    natural_keys: [email]              # ordered by preference
    sources:                           # systems contributing this object
      - {system: system:pipedrive, role: master}
      - {system: system:mailerlite, role: secondary}
    inclusion: union                   # union | intersection
    conflict_strategy: master_wins     # master_wins | most_recent | per_field
    per_field: []                      # if per_field: [{property, winner: system ref}]
```

## A8 — `processes/<id>.yaml`

| Field | R/O | Notes |
|---|---|---|
| `kind` | R | `process` |
| `id`, `name`, `description`, `meta` | R | |
| `type` | R | `pipeline / lifecycle / workflow` |
| `object` | R | `object:` ref the process moves |
| `state_property` | R | `property:` ref holding current state (stage field, lifecycle enum) |
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
| `bad_examples[]` | O | what does NOT suffice to exit — negative guard for AI classification and rep discipline |
| `customer_verifier` | O | `{description (R), check (O)}` — objective proof on the CUSTOMER side (booked slot, signed doc), not rep opinion; anti-sandbagging |
| `probability` | O | 0.0–1.0 forecast weight (pipeline processes; maps to `deal_probability` / HubSpot `metadata.probability`) |
| `required_properties[]` | O | property ids that must be non-empty in this stage |
| `owner_role` | O | |
| `sla` | O | `{target_duration_days (expected time, feeds stage-time KPI), rotting_threshold_days (no activity for N days → rotting alert; Pipedrive `rotten_days`), stuck_action}` |
| `tasks` | O | `{mandatory[], optional[]}` — rep checklists; agents verify completeness / create activities |
| `drafts` | O | `{email: draft:<id> or null, sms: draft:<id> or null}` — refs to A14 communication templates |
| `tips` | O | short guidance for the rep working this stage |
| `loss_reasons[]` | O | valid loss reasons when exiting to a negative terminal stage; keep consistent with a `lost_reason` enum property if one exists |
| `automations_triggered[]` | O | `automation:` refs firing on entry/exit |
| `kpis[]` | O | stage-level `kpi:` refs |
| `terminal` | O | bool (`won`, `lost`) + `outcome: positive/negative` |

`check` expressions: simple boolean expressions over `property` ids (`budget_confirmed == true && amount != null`). Not executed by the framework; they exist so agents/validators can evaluate them.

## A9 — `automations/<id>.yaml`

| Field | R/O | Notes |
|---|---|---|
| `kind` | R | `automation` |
| `id`, `name`, `description`, `meta` | R | |
| `platform` | R | `crm-native / n8n / zapier / make / custom-script / other` |
| `status_live` | R | `active / paused / unknown` |
| `trigger` | R | `{event, object (ref), conditions[]}` |
| `effects[]` | R | `{target (property/object ref), operation: write/create/delete/notify/external, detail}` |
| `data_fingerprint` | R | how to recognize its output: `{acting_user, field_patterns[], marker (e.g. note prefix), timing}` — at least one |
| `failure_modes[]` | O | `{symptom, impact, detection}` |
| `owner` | O | who maintains it |
| `definition_url` | O | link to n8n workflow / CRM automation |

## A10 — `actions/<id>.yaml`

| Field | R/O | Notes |
|---|---|---|
| `kind` | R | `action` |
| `id`, `name`, `description`, `meta` | R | |
| `object` | R | primary `object:` ref |
| `intent` | R | when an agent should reach for this action |
| `executor` | R | `agent / human / either` |
| `approval` | R | `none / required / conditional` (+ `approval_condition`) |
| `preconditions[]` | R | `{description, check (O)}` — must be verifiable from ontology terms |
| `inputs[]` | R | `{id, type, required, description}` |
| `workflow[]` | R | ORDERED steps: `{step, description, on_failure (abort/skip/compensate + detail)}` |
| `effects[]` | R | what changes: `{target, operation, detail}` |
| `side_effects[]` | R | `automation:` refs this will trigger + external effects (emails!). Empty list = explicit "none". |
| `postconditions[]` | O | how to verify success |
| `idempotency` | R | `safe_to_retry / not_idempotent / conditional` + notes |
| `implementations[]` | R | `{system (ref), via (mcp/api), tool_or_endpoint, notes}` |
| `error_handling` | O | prose fallback |

## A11 — `prompts/<id>.md`

YAML frontmatter: `kind: prompt`, `id`, `meta`, `used_by[]` (property/action refs), `model`, `inputs[]` (`{id, description, source}`), `output_contract` (format + where it's written), `version`. Body = the verbatim prompt. Never paraphrase a production prompt — extract it exactly; it's provenance.

## A12 — `kpis/<id>.yaml` (grouping into one file allowed)

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

## A13 — `agent-policy.yaml`

```yaml
kind: agent-policy
id: agent-policy
meta: {...}
agents:
  - id: sdr-agent
    description: ...
    allowed_actions: [action:qualify-lead, action:advance-deal-stage]
    approval_overrides: []            # {action, approval: required, condition}
    prohibitions:                     # hard NOs, in prose — override everything
      - Never delete any record.
      - Never contact a person outside declared channels.
    rate_limits: {actions_per_hour: 30}
defaults:
  unlisted_actions: forbidden         # actions not granted are forbidden
  draft_artifacts: read-as-hypothesis-only
```

## A14 — `drafts/<id>.md` (communication template)

YAML frontmatter: `kind: draft`, `id`, `meta`, `channel` (`email/sms/linkedin/other`),
`used_by[]` (process-stage refs), `language`, `variables[]` (`{id, source}` — where each
placeholder value comes from, in ontology terms), `approval` (`required` by default —
agents never send external communication autonomously unless agent-policy explicitly
grants it). Body = the template with `{{placeholders}}`.

Referenced from stages via `drafts: {email: draft:<id>, sms: draft:<id>}`.
