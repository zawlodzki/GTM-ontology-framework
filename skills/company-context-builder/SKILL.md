---
name: company-context-builder
description: >
  Build an evidence-backed static company context from scratch by inventorying user
  materials, normalizing them into the GTM Ontology Framework company-context format,
  researching the company and competitors, and analyzing Closed Won CRM opportunities.
  Use when Codex needs to create, extend, or repair company-context/; document products,
  product groups, segments, ICPs, personas, buying context, positioning, messaging, or
  GTM motions; reconcile declared strategy with market or CRM evidence; or prepare the
  business context required before running gtm-ontology-builder.
---

# Company Context Builder

Build `company-context/` as durable, public-safe business context. Keep live CRM
records, customer names, contact data, opportunity IDs, raw notes, and exports out
of the directory.

Read `references/artifact-guide.md` before creating or changing artifacts. Read
`references/research-protocol.md` before web, competitor, or CRM research. Use the
starter tree under `assets/company-context/` and the bundled scripts when present.
For each approved offer, copy `assets/artifact-templates/product-context.md`,
replace its product and group tokens, add it to the group manifest `products`, and
add its typed ref to the relevant group artifacts. Create `GAPS.md` from
`assets/artifact-templates/GAPS.md` only when consequential gaps remain.
Create a root `claims.yaml` from `assets/artifact-templates/claims.yaml` only when
material, changing, disputed, or decision-critical statements need evidence below
the artifact level; then set `claims_registry: claims.yaml` in the root manifest
and add `claim_refs` only to artifacts that actually rely on those claims.

The validator requires PyYAML and jsonschema. Install them once when unavailable.
Initialize and validate with:

```text
python <path-to-this-skill>/scripts/init_company_context.py --company-id <id> --company-name <name> --company-domain <url> --updated <YYYY-MM-DD> --product-group <id:name> --motion '<group-id>:<motion-id>:<name>:<summary>'
python <path-to-this-skill>/scripts/validate_company_context.py company-context/
```

Pass `--motion` only after the user approves its globally unique canonical id,
name, and summary. Repeat it for additional motions. When no motion is approved,
the initializer omits the motions artifact and manifest entry rather than inventing
a cross-tree identifier.

For a normalized Closed Won CSV, run
`scripts/analyze_closed_won.py`; keep its record-level working report outside
`company-context/`.

## Core rules

1. Follow **discover -> propose -> confirm -> record**. Do not write canonical
   artifacts before the phase gate.
2. Preserve provenance. User statements and supplied business documents are
   `declared`; system and web observations are `discovered`; synthesis is
   `inferred`; reviewed operational learning is `learned`.
3. Confirmation changes `meta.status`, not `meta.source`. Never silently turn an
   inference into a declaration.
4. Do not invent missing facts. Record consequential unknowns in `GAPS.md`.
5. Use typed references, not file paths. Do not confirm an artifact that references
   a draft or missing prerequisite.
   Treat `product-group:<id>` and `gtm-motion:<id>` as cross-tree identifiers shared
   with a linked GTM ontology; renaming either is a breaking change.
6. Keep product-group ICPs separate. Never merge them into a fictional company-wide
   ICP.
7. Define the market from a recurring job, use case, or category before narrowing
   it with firmographics. Firmographics prioritize proven need; they do not prove it.
8. Separate feature, capability, direct benefit, value, and business outcome.
9. Perform research and CRM access read-only. Never write to a source system.
10. Work in dependency order and in batches of at most five files. Validate and
    obtain approval after every batch.

## Phase 0: Intake and scope

Ask first for:

- company name, domain, language, timezone, and context owner;
- products, product groups, offer architecture, pricing, and commercial boundaries;
- strategy, ICPs, personas, use cases, procedures, GTM motions, positioning,
  messaging, research, and sales enablement materials;
- competitor names and known company/social URLs;
- CRM, pipelines in scope, Closed Won semantics, base currency, access method, and
  available exports or connectors.

Accept files, links, pasted text, connectors, APIs, and exports. Classify requested
inputs as required, useful, supplied, or missing. Confirm the proposed product-group
boundaries and CRM scope.

**GATE:** user confirms company identity, product-group scope, source inventory,
pipeline scope, and read-only access plan. Do not scaffold or write before approval.

## Phase 1: Inventory and normalization

Create a working matrix with: source, retrieved date, facts found, target artifact
and section, provenance, freshness, ambiguity, and gaps. Keep this matrix outside
the runtime manifest; do not copy raw CRM data into the workspace.

Map supplied content to the artifact contracts without changing meaning. When the
source format differs materially, present:

- source concept and proposed target;
- semantic changes and information that would be lost;
- recommended restructuring and alternatives;
- artifacts affected downstream.

Wait for approval before applying a material transformation. For a firmographic-only
ICP, propose market basis, observable participation, required need, ownership,
operational readiness, disqualifiers, and firmographic priority as separate layers.

**GATE:** user approves the source-to-artifact mapping and every material format
transformation.

## Phase 2: Company and competitor research

Discover available tools. Prefer Exa MCP when callable. Otherwise use another
search/browser MCP or web search. If none is available, ask for URLs or documents
and record the research gap.

Research official company pages first: products, pricing, documentation, case
studies, blog, legal pages, careers, and verified social profiles. Then use credible
external sources. Distinguish company claims from independently supported facts.

Research competitors for target situation, use cases, alternatives, positioning,
offers, pricing, proof, and comparison dimensions. When several competitors require
broad external research and subagents are available, delegate one company per
subagent and require source URLs and retrieval dates.

Record every material changing claim in the claim registry with its typed scope,
supporting or contradicting evidence, retrieval date, `last_verified`, and
`verify_every`. Keep minor claims at artifact level when separate review would add
no value. Do not use search snippets as evidence when the underlying page can be
opened.

**GATE:** present findings, confidence, unsupported claims, and conflicts with
declared inputs. User chooses which disputed claims become canonical.

## Phase 3: Closed Won CRM analysis

Use a purpose-built CRM connector first, then an API or user export. Confirm the
CRM's exact won field/status and the in-scope pipelines. Analyze bona fide wins with
won dates in the trailing 12 months in the user's timezone.

Before inference, report field availability, fill rates, currencies, suspicious
test records, duplicates, cancellations, refunds, and corrections. Do not exclude
them without user approval.

Analyze the cohort across product group, use case, customer situation, industry,
geography, size, source, comparable value, cycle length, trigger, current
alternative, buying roles, reason won, and evidence coverage. Treat missing need or
readiness fields as unknown, not as evidence of fit.

Select the detailed Top 10 by base-currency value, breaking ties by most recent
won date. If comparable base-currency values do not exist, stop and ask for the
conversion source or method. Approval of an approximate ranking is not approval of
a particular FX source, date convention, fallback, or a mix of CRM and external
conversions. Propose the complete named method and wait for explicit acceptance.
Do not rank raw amounts across currencies.

For each selected opportunity inspect available notes, activities, transcripts,
emails, and linked organization data for problem, workflow, trigger, alternative,
committee, objections, criteria, selected offer, reason won, and implementation
evidence. Persist only aggregate or anonymized conclusions and evidence metadata.

**GATE:** user confirms exclusions, cohort interpretation, Top 10 selection, and
which CRM-derived ICP hypotheses may be used.

## Phase 4: Reconciliation

Present every material conflict before writing:

| Claim | Declared evidence | Research evidence | CRM evidence | Impact | Recommendation | Decision options |
|---|---|---|---|---|---|---|

Require the user to decide conflicts affecting ICP, segment, product truth,
positioning, pricing, or GTM motion. Merge complementary evidence only when it does
not change meaning. Record unresolved conflicts as gaps; never choose silently.

When both sides remain useful hypotheses, record separate claims and reciprocal
`conflicts_with` refs. When a decision replaces an older claim, keep the old claim
for audit and link the replacement with `supersedes`.

**GATE:** user resolves or explicitly defers every material conflict.

## Phase 5: Build the context

Initialize `company-context/` with the bundled initializer. Write only approved
content, in this order:

1. manifest, navigation, company profile, strategy, market, commercial and
   operating model;
2. product-group manifest, strategy, segment, and use case;
3. self-contained ICP, personas, and buying context;
4. product truth and offer boundaries;
5. positioning, value propositions, messaging, and motions.

Write at most five files per batch. Validate after each batch and wait for approval.
Keep partial artifacts `draft`. Do not create downstream artifacts whose required
upstream artifacts are absent.

If consequential data remains missing, create `GAPS.md` and set
`gaps_report: GAPS.md` in the root manifest. For each gap include the artifact or
field, sources checked, impact, owner or question, and next action. Omit both when
there are no consequential gaps.

When an approved claim registry is needed, create `claims.yaml`, set the manifest
pointer, and attach `claim_refs` before confirming dependent artifacts. Do not
create an empty registry or duplicate every artifact statement into it.

Run the bundled validator. Errors block completion; present warnings as a review
list. Report sources, freshness, resolved conflicts, deferred decisions, and files
created.

When `$gtm-context-evaluator` is installed, delegate competency case authoring,
isolated execution, and deterministic scoring to it. Cover material routing and
evidence risks introduced by this context: product-group separation, overdue claims,
unresolved conflicts, required provenance, and distractor artifacts. Do not recreate
or copy its runner into this skill. Evaluate structured response traces with:

```text
python <path-to-gtm-context-evaluator>/scripts/evaluate_context.py <cases.yaml> <responses.jsonl>
```

Golden responses must pass all hard checks. Deliberately bad responses must fail
the intended dimension. Keep any scenario-only claims outside the confirmed context
tree, and report tokens without imposing a budget unless the owner has approved one.
If the evaluator skill is unavailable, ask the user to install it and report the
competency evaluation as a handoff gap; do not block structural context validation.

## Completion handoff

Suggest, but do not start automatically:

`Use $gtm-ontology-builder to build the GTM ontology, treating company-context/manifest.yaml as the canonical static business context.`

State that `gtm-ontology-builder` should still discover live systems, CRM semantics,
pipelines, automations, agent actions, governance, and KPIs instead of copying them
from static company context.
