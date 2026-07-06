# CRM Type Mapping (binding reference)

How GOF property types and stage attributes map to Pipedrive / HubSpot / Attio.
Used when writing bindings (A6) and when interpreting discovery snapshots.
Endpoints and names change — verify against vendor docs before relying on them.

## Property types (`properties[].type`)

| GOF | Pipedrive (`field_type`) | HubSpot (`type` / `fieldType`) | Attio (`type`) |
|---|---|---|---|
| `string` | `varchar` | `string` / `text` | `text` |
| `text` | `text` | `string` / `textarea` | `text` |
| `number` | `double` | `number` / `number` | `number` |
| `currency` | `monetary` | `number` / `number` (+ currency) | `currency` |
| `boolean` | `enum` (Yes/No — no native bool) | `bool` / `booleancheckbox` | `checkbox` |
| `date` | `date` | `date` / `date` | `date` |
| `datetime` | `date` + `time` (two fields!) | `datetime` / `date` | `timestamp` |
| `enum` | `enum` | `enumeration` / `select` | `select` (single) |
| `set` | `set` | `enumeration` / `checkbox` | `select` (multi) |
| `phone` | `phone` | `string` / `phonenumber` | `phone-number` |
| `email` | `varchar` | `string` / `text` | `email-address` |
| `url` | `varchar` | `string` / `text` | `text` |
| `user` | `user` | owner | `actor-reference` |
| `reference` | `org` / `people` | (no native) | `record-reference` |
| `address` | `address` | `string` | `location` |
| `json` | (no native — text) | (no native — string) | (no native — text) |

Gotchas:

- **Pipedrive** has no single `datetime` and no native `boolean` — bind `datetime` as two
  fields (note it in `transform: datetime_tz` + `notes`), `boolean` as Yes/No enum with
  `enum_map: {yes_id: true, no_id: false}`. Enum/set options are managed via the Fields
  API v2 bulk-options endpoint. Custom-field keys are 40-char hashes.
- **HubSpot** separates `type` (data type) from `fieldType` (UI control) — record both
  in binding `notes`. Internal property names, not labels, go into `field_key`.
- **Attio** is closest to 1:1 (native `currency`, `email-address`, `phone-number`,
  `record-reference`); attributes are per-object, statuses can live on a status
  attribute or lists.

## Field/metadata endpoints (discovery + bindings)

| Concern | Pipedrive | HubSpot | Attio |
|---|---|---|---|
| Field metadata | `GET /api/v2/{deal,person,organization}Fields` | `GET /crm/v3/properties/{objectType}` | `GET /v2/objects/{object}/attributes` |
| Pipelines | `GET /v1/pipelines` | `GET /crm/v3/pipelines/{objectType}` | status attribute on `deals` (or lists) |
| Stages | `GET /v1/stages` | `stages[]` in pipeline body | `.../statuses` |
| Native automations | limited API → discover via UI/interview | `GET /automation/v4/flows` | limited API → interview |

Automation reality check: only HubSpot exposes a mature workflow API. On Pipedrive and
Attio, agentic loops typically live in n8n/Make/scripts (`platform:` in A9), with only
simple rules in the CRM UI — expect Phase 3 interviews, not introspection, to find them.

## Stage attributes (A8 → CRM)

| GOF stage field | Pipedrive | HubSpot | Attio |
|---|---|---|---|
| `name` | `name` | `label` | status `title` |
| `order` | `order_nr` | `displayOrder` | `position` |
| `probability` | `deal_probability` (0–100) | `metadata.probability` (0.0–1.0) | no native → custom field |
| `sla.rotting_threshold_days` | `rotten_flag` + `rotten_days` | no native → workflow | no native → automation |
| terminal won/lost | deal `status` (not a stage!) | `metadata.isClosed` + probability 1.0/0.0 | status flagged won/lost |
| `required_properties` | required fields per pipeline + `important_on_stage` | stage-gating workflow validation | `is_required` on attribute |

No native home in any CRM (context for humans + agents, stays in the ontology only):
`definition`, `entry_criteria`, `exit_criteria`, `bad_examples`, `customer_verifier`,
`tasks`, `tips`, `loss_reasons` (as stage metadata; a `lost_reason` enum FIELD binds
normally), stage-level `kpis`.
