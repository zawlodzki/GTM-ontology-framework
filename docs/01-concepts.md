# Concepts

## 1. Layer model

### Layer 1: Semantic (*what exists*)

The conceptual model of the business, independent of any tool. Canonical **object types** (Deal, Person, Organization, Subscription…), their **properties** with business meaning, and **links** between them. The semantic layer owns:

- Property **semantics**: what a value means, who fills it, when it changes.
- **Enum definitions**: for every dropdown value, the business conditions under which it applies (e.g. what must be true for `lifecycle_stage = SQL`).
- **AI-field provenance**: for fields written by AI (e.g. qualification summary from a call transcript), a reference to the prompt that produces them.
- **Fill authorship** (`filled_by`): `human | automation | ai | integration | system`. This is the single most important fact for an agent interpreting a value.

An object type is canonical, not system-shaped: `Person` collapses Pipedrive "person", Mailerlite "subscriber", HubSpot "contact". Never model one object type per source table (see anti-patterns in `04-extending.md`).

### Layer 2: Binding (*where data lives, how to reach it*)

Binds the semantic model to physical systems:

- **System profile**: what the app is, its role in the stack, access methods (MCP server + tool names, REST API, warehouse tables), rate limits, write permissions.
- **Discovery snapshot**: raw, timestamped introspection output (entities, fields incl. custom-field keys, enum options, pipelines/stages, users, automation list). Ground truth for bindings; diffed on re-discovery to detect drift.
- **Binding**: semantic property → physical field key, per system. Includes transformations (e.g. Pipedrive custom-field hash keys, enum option IDs → canonical values) and writability.
- **Identity resolution**: natural keys (email, org domain, external IDs) that identify the same real-world entity across systems, plus merge strategy (master source, union vs. intersection, per-field precedence).

The binding layer is the only layer that changes when you swap access methods (API → MCP) or rename a custom field.

### Layer 3: Dynamic (*what happens, what can be done*)

Two halves:

**Logic already running in the systems**, so agents can correctly interpret data as *effects of executed logic*:

- **Processes**: pipelines and lifecycles modeled as state machines. Per stage: entry criteria, exit criteria, required properties, allowed transitions, SLAs, automations triggered, owning role, stage KPIs.
- **Automations**: every workflow (CRM-native, n8n, Zapier, Make…) with trigger, conditions, effects, and a **data fingerprint**: how to recognize its output in the data (authoring user, field patterns, note prefixes, timestamps).

**Logic agents may execute**:

- **Actions**: contracts for agent-executable operations: preconditions, inputs, ordered workflow steps, effects, side effects (incl. automations they will trigger!), approval requirements, idempotency, error handling, and per-system implementation (which MCP tool / API endpoint).
- **Prompts**: versioned prompt files behind AI-filled fields and AI-executed actions.
- **Drafts**: communication templates (email/SMS) referenced from process stages; agents use them as approved content, never free-compose external messages.
- **Playbooks** (optional): multi-action sequences for larger jobs.

### Layer 4: Measurement & Governance (*how success is measured, what agents may do*)

- **KPIs** at three levels (company, process, stage), each with formula bound to ontology terms, grain, target, owner, and source of truth.
- **Data quality rules** (largely derivable from stage `required_properties` and entry criteria).
- **Agent policy**: allowed actions per agent role, approval gates, hard prohibitions, rate limits.

## 2. Artifact catalog

| # | Artifact | Layer | Format | One per | Schema |
|---|---|---|---|---|---|
| A0 | `manifest.yaml` | index | YAML | ontology | `manifest.schema.json` |
| A1 | `business-context.md` | 1 | Markdown + YAML frontmatter | ontology | none |
| A2 | `glossary.yaml` | 1 | YAML | ontology | none (see formats doc) |
| A3 | `objects/<id>.yaml` | 1 | YAML | object type | `object-type.schema.json` |
| A4 | `systems/<id>.yaml` | 2 | YAML | connected app | `system.schema.json` |
| A5 | `discovery/<system>/snapshot.yaml` | 2 | YAML | system × run | none (normalized envelope, system-specific body) |
| A6 | `mappings/<system>.yaml` | 2 | YAML | system | `binding.schema.json` |
| A7 | `identity.yaml` | 2 | YAML | ontology | none (see formats doc) |
| A8 | `processes/<id>.yaml` | 3 | YAML | process | `process.schema.json` |
| A9 | `automations/<id>.yaml` | 3 | YAML | automation | `automation.schema.json` |
| A10 | `actions/<id>.yaml` | 3 | YAML | action | `action.schema.json` |
| A11 | `prompts/<id>.md` | 3 | Markdown + YAML frontmatter | prompt | none |
| A12 | `kpis/<id>.yaml` | 4 | YAML | KPI (grouping allowed) | `kpi.schema.json` |
| A13 | `agent-policy.yaml` | 4 | YAML | ontology | none (see formats doc) |
| A14 | `drafts/<id>.md` | 3 | Markdown + YAML frontmatter | communication template | none (see formats doc) |

Grouping rule: artifacts marked "one per X" may be grouped into a single file (a YAML list) while the ontology is small (< ~10 entries of that kind); split into per-entity files when they grow, so agents can load them individually.

## 3. Conventions

- **IDs**: kebab-case, unique within artifact kind (`new-business`, `advance-deal-stage`).
- **Cross-references**: `kind:id`, e.g. `object:deal`, `property:deal.lifecycle_stage`, `automation:lead-scoring`, `kpi:win-rate`, `action:advance-deal-stage`, `prompt:lead-qualification`, `process:new-business`, `system:pipedrive`. Validators must resolve every reference.
- **Files** are referenced by ontology-root-relative path.
- **Names**: object types PascalCase in `name`, kebab-case in `id`. Link labels UPPER_SNAKE_CASE (`BELONGS_TO`, `ATTENDED`).
- **Every YAML artifact** starts with `kind:` and `id:`.

### Provenance envelope (required on every artifact; optional per-property)

```yaml
meta:
  source: discovered | inferred | declared
    # discovered = introspected from the system
    # inferred   = proposed by AI, needs human confirmation
    # declared   = stated by a human (business logic not present in any system)
  status: draft | confirmed
  confirmed_by: <person>        # required when status: confirmed and source != discovered
  updated: YYYY-MM-DD
```

Rule: **agents must not act on `status: draft` artifacts** (they may read them as hypotheses). Actions and agent-policy must reference only confirmed artifacts.

## 4. Progressive disclosure

Three tiers keep agent context small:

- **Tier 0, entry point.** `CLAUDE.md` in the ontology root (navigation rules, hard rules, directory map; static, ~1 page; mirrored as `AGENTS.md` where that convention is used) plus `manifest.yaml` (target < 2k tokens): business summary (1 paragraph), systems list, and an index of every artifact with `kind`, `path`, one-line `summary`, and `load_when` hint. An agent always loads these and usually nothing else up front. Agents discover the ontology via a marker-delimited block in the workspace root `CLAUDE.md`/`AGENTS.md` (written in Phase 5).
- **Tier 1, artifact heads.** Every artifact's first ~15 lines (kind, id, name, description, meta) are self-sufficient as a summary. Agents may head-read files cheaply.
- **Tier 2, full artifacts**, loaded on demand per the manifest's `load_when` hints.

Size discipline: keep any single artifact under ~200 lines; move long prose to a linked `.md`; split grouped files when they exceed the limit.

## 5. Versioning

- Ontology-level semver in `manifest.yaml` (`version:`). Bump minor on artifact additions/changes, major on breaking renames of ids/refs.
- `CHANGELOG.md` per ontology instance.
- Discovery snapshots are immutable and timestamped; keep the latest plus history as needed for drift diffs.
