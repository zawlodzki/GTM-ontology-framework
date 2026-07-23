# CRM Type Mapping (binding reference)

How GOF property types and stage attributes map to Pipedrive / HubSpot / Attio /
Salesforce. Used when writing bindings (A6) and when interpreting discovery snapshots.
Endpoints and names change; verify against vendor docs before relying on them.

## Platform CRMs: scope to the CRM module

Pipedrive and Attio are CRMs. Salesforce and HubSpot are platforms with a CRM inside.
For those, the ontology covers the **CRM module only**, declared explicitly in the
system profile's `scope` block (A4):

- **Salesforce**. Default in scope: Sales Cloud core objects (`Lead`, `Account`,
  `Contact`, `Opportunity`, `Task`/`Event`, optionally `Campaign` + `CampaignMember`).
  Out of scope unless requested: Service Cloud, Marketing Cloud, CPQ, Experience Cloud,
  custom app objects. A full describe returns hundreds of objects; discovery reads
  only `objects_in_scope`, and records how many objects it skipped.
- **HubSpot**. Default in scope: CRM core (`contacts`, `companies`, `deals`) + Sales
  Hub pipelines. Marketing Hub assets (forms, emails, campaigns) and Service Hub
  (tickets) enter only as separate scoped systems when a competency question needs them.
- Same rule applies to Dynamics 365 and other suite CRMs.

## Property types (`properties[].type`)

| GOF | Pipedrive (`field_type`) | HubSpot (`type`/`fieldType`) | Attio (`type`) | Salesforce (field type) |
|---|---|---|---|---|
| `string` | `varchar` | `string`/`text` | `text` | `Text` |
| `text` | `text` | `string`/`textarea` | `text` | `LongTextArea` |
| `number` | `double` | `number`/`number` | `number` | `Number` |
| `currency` | `monetary` | `number`/`number` (+currency) | `currency` | `Currency` |
| `boolean` | `enum` (Yes/No, no native bool) | `bool`/`booleancheckbox` | `checkbox` | `Checkbox` |
| `date` | `date` | `date`/`date` | `date` | `Date` |
| `datetime` | `date` + `time` (two fields!) | `datetime`/`date` | `timestamp` | `DateTime` |
| `enum` | `enum` | `enumeration`/`select` | `select` (single) | `Picklist` |
| `set` | `set` | `enumeration`/`checkbox` | `select` (multi) | `MultiselectPicklist` |
| `phone` | `phone` | `string`/`phonenumber` | `phone-number` | `Phone` |
| `email` | `varchar` | `string`/`text` | `email-address` | `Email` |
| `url` | `varchar` | `string`/`text` | `text` | `URL` |
| `user` | `user` | owner | `actor-reference` | `Lookup(User)` |
| `reference` | `org`/`people` | (no native) | `record-reference` | `Lookup` / `MasterDetail` |
| `address` | `address` | `string` | `location` | `Address` (compound) |
| `json` | (no native, text) | (no native, string) | (no native, text) | (no native, LongTextArea) |

Gotchas:

- **Pipedrive** has no single `datetime` and no native `boolean`; bind `datetime` as
  two fields, `boolean` as a Yes/No enum with `enum_map`. Enum/set options via the
  Fields API v2 bulk-options endpoint. Custom-field keys are 40-char hashes.
- **HubSpot** separates `type` (data type) from `fieldType` (UI control); record both
  in binding `notes`. Internal property names, not labels, go into `field_key`.
- **Attio** is closest to 1:1 (native `currency`, `email-address`, `phone-number`,
  `record-reference`); attributes are per-object, statuses live on a status attribute
  or lists.
- **Salesforce** custom fields carry the `__c` suffix in API names; that suffix is the
  `field_key`. Picklists can be per-record-type; native **validation rules** map to
  GOF `property.validation`; **record types** with separate sales processes = one GOF
  process per record type. **Lead conversion** (Lead → Account+Contact+Opportunity) is
  not a stage transition; model it as an action with explicit effects.

## Datetime & timezone serialization (A4 `data_standards` + A6 `datetime`)

A datetime is a point in time, not a wall-clock string. If the ontology doesn't
record what zone a system stores and expects, an agent writing a 13:00 local
meeting sends a naive "13:00", the API reads it as UTC, and it resurfaces at
15:00. Capture the contract once on the system profile, then reference it per field.

System profile (A4) — `data_standards`: `api_timezone` (zone the API stores and
returns datetimes in), `business_timezone` (zone humans/agents author times in),
`datetime_format` / `date_format` / `time_format`, `number_format`,
`boolean_encoding`, and `docs_ref` (the vendor's date-format page — verify per
release).

Binding (A6) — per date/datetime property, set the `datetime` block:

- **Timestamp**: `transform: datetime_tz`, `datetime: {precision: datetime, source_tz: <business_timezone>}`.
  Convert business zone → `api_timezone` on write, back on read.
- **Date-only**: `transform: none`, `datetime: {precision: date}`. No time, no
  zone — sent verbatim, NEVER tz-converted (converting a date can shift it a day).

| Vendor | Stores datetimes in | Format | Notes |
|---|---|---|---|
| **Pipedrive** | UTC | `YYYY-MM-DD HH:mm:ss` (ISO 8601) | No single datetime type: an activity time is `due_date` + `due_time`, both UTC; booleans 1/0. |
| **HubSpot** | UTC (epoch ms) | epoch milliseconds | Date-only properties are midnight UTC; sending a local-midnight timestamp shifts the day. |
| **Attio** | UTC | ISO 8601 (`timestamp`) | Native `timestamp`; still convert from the business zone before writing. |
| **Salesforce** | UTC | ISO 8601 (`DateTime`) | `Date` fields are zone-less; `DateTime` is stored/returned in UTC, displayed in the user's locale zone. |

## Field/metadata endpoints (discovery + bindings)

| Concern | Pipedrive | HubSpot | Attio | Salesforce |
|---|---|---|---|---|
| Field metadata | `GET /api/v2/{obj}Fields` | `GET /crm/v3/properties/{objectType}` | `GET /v2/objects/{obj}/attributes` | `GET /services/data/vXX/sobjects/{obj}/describe` (fields + picklist values) |
| Pipelines | `GET /v1/pipelines` | `GET /crm/v3/pipelines/{objectType}` | status attribute on `deals` | `OpportunityStage` (per sales process / record type) |
| Stages | `GET /v1/stages` | `stages[]` in pipeline body | `.../statuses` | `OpportunityStage` records |
| Native automations | limited API → interview | `GET /automation/v4/flows` | limited API → interview | Flows + validation rules via Tooling API |

Automation reality check: HubSpot and Salesforce expose automation metadata via API
(flows, validation rules, Apex triggers on Salesforce; list them, then interview for
intent). Pipedrive and Attio mostly don't; expect Phase 3 interviews, not
introspection, to find what runs. External loops (n8n/Make/Zapier) are interview-only
everywhere.

## Stage attributes (A8 → CRM)

| GOF stage field | Pipedrive | HubSpot | Attio | Salesforce |
|---|---|---|---|---|
| `name` | `name` | `label` | status `title` | `MasterLabel` |
| `order` | `order_nr` | `displayOrder` | `position` | `SortOrder` |
| `probability` | `deal_probability` (0–100) | `metadata.probability` (0.0–1.0) | no native → custom field | `DefaultProbability` (0–100) |
| `sla.rotting_threshold_days` | `rotten_flag` + `rotten_days` | no native → workflow | no native → automation | no native → Flow |
| terminal won/lost | deal `status` (not a stage!) | `metadata.isClosed` + probability | status flagged won/lost | `IsClosed` + `IsWon` |
| `required_properties` | required per pipeline + `important_on_stage` | stage-gating workflow | `is_required` on attribute | validation rules on `StageName` |

No native home in any CRM (context for humans + agents, stays in the ontology only):
`definition`, `entry_criteria`, `exit_criteria`, `bad_examples`, `customer_verifier`,
`tasks`, `tips`, `loss_reasons` (as stage metadata; a `lost_reason` enum FIELD binds
normally), stage-level `kpis`.
