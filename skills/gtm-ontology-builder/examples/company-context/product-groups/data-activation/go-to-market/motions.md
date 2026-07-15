---
kind: gtm-motions
id: data-activation-motions
scope: product-group:data-activation
strategy_ref: product-group-strategy:data-activation-strategy
segment_ref: segment:data-activation-core-segment
use_case_ref: use-case:data-activation-core-use-case
icp_ref: icp:data-activation-icp
persona_ref: personas:data-activation-personas
buying_context_ref: buying-context:data-activation-buying-context
positioning_ref: positioning:data-activation-positioning
value_proposition_ref: value-propositions:data-activation-value-propositions
messaging_ref: messaging:data-activation-messaging
product_refs:
  - product-context:warehouse-sync
  - product-context:audience-activation
motions:
  - id: data-activation-product-led
    name: Product-led technical discovery
    summary: Docs and a synthetic-data sandbox lead evaluators to a production-readiness review; common for Warehouse Sync.
  - id: data-activation-sales-assisted
    name: Sales-assisted adoption
    summary: Qualification, readiness review, and a bounded pilot for production adoption; primary route for Audience Activation.
meta:
  source: synthetic
  status: example
  updated: 2026-07-15
  owner: Revenue
  last_verified: 2026-07-15
  verify_every: 90d
---

# Data Activation GTM motions

## Motion summary

**GTM phase:** experimentation.

**Model:** product-led technical discovery plus sales-assisted production adoption.
Documentation, implementation guides, and a synthetic-data sandbox let technical
evaluators understand the product model. Production access always requires ICP
qualification, joint ownership, readiness review, security approval, a bounded
pilot, and commercial scope.

**Primary channel:** technical documentation and a restricted synthetic-data sandbox
for reverse-ETL-aware technical evaluators.

**Secondary channel:** practical business use-case education and selective one-to-one
outreach for lifecycle owners experiencing audience delay or inconsistency. It
validates a workflow hypothesis rather than claiming a private problem.

## Market targeting

Target organizations showing evidence of a warehouse-to-destination workflow:
maintained sync scripts, recurring exports, destination-specific mappings, business
requests for modeled attributes or audiences, or active evaluation of activation
tools. A warehouse, named technology, senior data role, or large event volume is a
priority signal only; none establishes an activation need by itself.

Messaging must begin with a workflow or category hypothesis that the buyer can
validate. Do not infer private architecture, data quality, consent maturity, or
purchase intent from public firmographic or technology data.

## Technical discovery and capture

1. An evaluator reviews a warehouse-to-destination use case or implementation guide.
2. The evaluator creates a sandbox project with sample models and a non-production destination.
3. Product telemetry records completed mappings, test deliveries, and errors without capturing customer data.
4. A fit prompt asks about the recurring workflow, its current limitation, the
   production warehouse, use case, destination, and owners.
5. Qualified evaluators can request a production-readiness review.

This path is most common for Warehouse Sync and usually begins with a Head of Data
or Data Engineer. Sandbox activity signals technical interest, not ICP fit or
purchase intent by itself.

## Business use-case discovery

Practical content and targeted outreach help a Lifecycle Marketing Lead document
one recurring audience workflow, its current method, delay or inconsistency, expected
counts, permitted use, cadence, and technical owner. A workflow guide or diagnostic
leads to joint discovery with the Head of Data; it does not lead directly to a demo
or production trial.

Use public triggers such as a new engagement platform, regional expansion, or a
visible data-governance initiative only to form a narrow hypothesis. Ask the buyer
to confirm the private workflow and impact. This path is most relevant to Audience
Activation and remains a controlled experiment until repeated qualified demand exists.

## Sales-assisted adoption

Sales assistance begins when an organization needs production credentials, a
security review, multiple destinations, or a governed business-user workflow.

1. Revenue confirms `icp:data-activation-icp`, the recurring delivery workflow,
   its current failure or cost, and the named business use case.
2. A technical specialist reviews architecture, identity, consent, and failure handling.
3. The buyer and specialist define a bounded pilot with acceptance evidence.
4. Sales recommends Warehouse Sync, Audience Activation, or both.
5. Customer Success joins before signature to confirm operating ownership.

Audience Activation is primarily sales-assisted because the Lifecycle Marketing
Lead and Head of Data must agree on definitions, access, and operating controls.

## Journey execution

| Stage | Primary asset or interaction | Owner | Exit signal |
|---|---|---|---|
| Problem or outcome aware | Workflow article, checklist, incident guide, or lifecycle workshop | Revenue marketing | Buyer identifies a recurring delivery flow and meaningful failure or delay |
| Use-case aware | Use-case guide or workflow diagnostic | Revenue marketing and business or technical owner | Model, destination, cadence, current method, and both owners are named |
| Category aware | Alternative comparison, documentation, and discovery | Revenue and Product | Buyer accepts a comparison frame and chooses paths to validate |
| Product and technical aware | Synthetic-data sandbox, representative demo, and structured discovery | Product and technical evaluator | Required ICP criteria are known and production-readiness review is warranted |
| Production readiness | Architecture, identity, permitted-use, security, destination, and runbook review | Technical specialist and customer validators | A bounded pilot can be defined or a blocking gap is documented |
| Pilot and decision | One-flow pilot, security approval, proposal, and responsibility matrix | Revenue, technical specialist, Customer Success, and committee | Acceptance evidence, scope, owners, price, and unresolved gaps are accepted or rejected |
| Adoption | Production launch and 30-, 60-, and 90-day operating reviews | Customer Success and customer owners | The agreed flow runs, failures are owned, and the downstream workflow uses the data |

## Product routing

- Confirm workflow need and ownership before technical and firmographic priority.
- Confirm operational readiness before recommending a production path.
- Route repeatable attribute or record delivery toward Warehouse Sync.
- Route marketer-managed segments and audience publishing toward Audience Activation.
- Recommend both only when the buyer has two distinct owned use cases.
- Do not treat a connector request as a business use case.
- Stop qualification when a required ICP criterion is unknown and record the gap.
- Do not recommend a production pilot until identity, consent, source ownership,
  destination ownership, recovery, and adoption evidence can be reviewed.

No decision is valid when the current method still works, recurring volume or
urgency is insufficient, security capacity is unavailable, an owner is missing,
or the need requires streaming, identity creation, consent determination, or a
broader customer-data platform.

## Handoffs

Product owns sandbox education. Revenue owns qualification and commercial scope.
The technical specialist owns production-readiness evidence. Customer Success owns
pilot coordination and post-sale adoption; Engineering owns connector defects.

The accepted source-to-destination map or audience definition, identity and
permitted-use assumptions, destination behavior, alert and recovery owners, pilot
evidence, product limits, and unresolved gaps pass to Customer Success. A signature
without joint ownership or a production runbook is not ready for routine onboarding.

## Experiment and capacity constraints

- Test the technical and business acquisition paths separately; do not hide weak
  qualification behind aggregate pipeline volume.
- Limit concurrent pilots to the technical-specialist and Customer Success capacity
  required for readiness review, evidence collection, and operating handoff.
- Do not expand channels or destination promises until the current segment,
  ownership model, offer route, pilot criteria, and adoption path repeat.
- Record unsupported connector, streaming, identity, security, or custom-model needs
  as gaps or separate scope rather than absorbing them into the standard offer.
- Treat the two offers as separate experiments when their buying journey, owners,
  or production gates diverge materially.

## Motion measures

Review monthly by acquisition path and offer:

- documentation-to-sandbox and sandbox-to-readiness-review conversion;
- business diagnostic or outreach-to-joint-discovery conversion;
- required-criterion unknowns, disqualification reasons, and qualified pilot rate;
- time to readiness completion and security approval;
- pilot acceptance, rejection reason, and unpriced custom work;
- Warehouse Sync versus Audience Activation routing and evidence;
- production activation, failure-recovery evidence, and time to first accepted run;
- 30-, 60-, and 90-day downstream use-case adoption;
- share of closed customers whose offer or scope changes during onboarding.

A high onboarding scope-change rate indicates weak qualification, product routing,
or pilot evidence. Advance beyond experimentation only when the same segment,
ownership model, bounded offer, proof, and adoption path repeat without hidden
custom engineering.
