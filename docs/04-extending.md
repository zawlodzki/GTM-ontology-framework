# Extending & Maintaining

## Adding a new system (email marketing, ERP, billing, support…)

Adding e.g. Mailerlite or an ERP does **not** restructure the ontology. Run the process scoped to the new system:

1. **Phase 0 (scoped):** add `binding/systems/<new>.yaml`; extend use cases.
2. **Phase 1:** discovery snapshot for the new system.
3. **Phase 2:** map discovered entities onto *existing* object types first (Mailerlite "subscriber" → existing `object:person`, add to its `aliases`). Create new object types only for genuinely new concepts (`Campaign`, `Invoice`, `PurchaseOrder`). Add links to existing objects (`Invoice BELONGS_TO Organization`).
4. **Identity resolution:** extend `binding/identity.yaml` — natural keys joining the new system to existing objects (person: `email`; organization: `domain`, VAT/tax ID for ERP), master source, conflict strategy per MDM survivorship practice (master_wins / most_recent / per_field; union vs. intersection).
5. **Phases 3–5:** elicit the new system's processes/automations/KPIs; define new agent actions; extend `agent-policy.yaml`; re-validate; bump minor version.

Typical additions per system class:

| System class | New objects | Typical processes | Typical agent actions |
|---|---|---|---|
| Email marketing | Campaign, Segment, EmailEvent | nurture lifecycle, list hygiene | add-to-segment, enroll-in-sequence (usually `approval: required`) |
| ERP / billing | Invoice, Order, Product, Contract | order-to-cash | read-mostly; create-draft-invoice with approval |
| Support | Ticket | support workflow | summarize, link ticket to Organization |
| Enrichment | (none — writes properties) | — | trigger-enrichment |

Cross-system business logic (e.g. "customer lifecycle spans CRM won-deal + first paid invoice in ERP") becomes a `process` whose stage criteria reference properties of *multiple* objects — this is exactly why criteria live in the ontology, not in any single app.

## Drift detection

Systems change under you. Scheduled (weekly/monthly) or before any major agent deployment:

1. Re-run Phase 1 → new snapshot.
2. Diff against previous snapshot: fields added/removed/renamed, enum options changed, stages changed, automations appeared/disappeared, fill-rate collapses (a field silently abandoned).
3. Classify: **breaking** (bound field removed, stage deleted → validation fails, agents on this area paused), **semantic** (new enum option with no definition → Phase 3 mini-interview), **cosmetic** (label rename → update binding).
4. Record in `CHANGELOG.md`, bump version.

## Access-method changes

API → MCP or vice versa touches only `systems/<id>.yaml` (access block) and `actions/*.implementations`. Semantic/dynamic layers untouched — this separation is the point of the binding layer.

## Anti-patterns

Standard ontology-engineering and data-modeling anti-patterns, applied to GTM:

1. **Table-mirroring.** One object type per source table. Collapse synonyms; hide join/junk tables in bindings.
2. **God object.** `Deal` with 120 properties including copies of org and person data. Use links.
3. **Prose-only logic.** Stage criteria written as an essay nobody can check. Always pair `description` with a `check` expression where possible.
4. **Inventing data.** Adding `lead_score` to the semantic layer because it would be nice, though nothing produces it. Record as a semantic gap instead — no attribute without a producer.
5. **Unfingerprinted automations.** An automation without a data fingerprint means agents can't attribute values → they overwrite bot-managed fields or trust stale AI output.
6. **Actions without side-effect lists.** An agent moves a deal to "Won" unaware it fires the invoice automation. `side_effects` is required — empty list is an explicit claim of none.
7. **Skipping confirmation.** Shipping `inferred` artifacts as truth. Draft ≠ confirmed; agents must not act on drafts.
8. **Manifest bloat.** Copying artifact bodies into the manifest. Manifest = index with one-liners; details stay in Tier 2.
9. **Modeling everything.** Ontology scope = agent use cases (Phase 0). Unused corners of the CRM can stay unmodeled; record them as out-of-scope.
