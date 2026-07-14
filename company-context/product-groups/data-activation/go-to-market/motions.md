---
kind: gtm-motions
id: data-activation-motions
scope: product-group:data-activation
meta:
  source: synthetic
  status: example
  updated: 2026-07-14
---

# Data Activation GTM motions

## Motion summary

Data Activation combines product-led technical discovery with sales-assisted
production adoption. Documentation, sample projects, and a restricted sandbox let
technical evaluators understand the model before speaking with sales. Production
access always requires qualification, security review, and a commercial agreement.

## Market targeting

Target organizations showing evidence of a warehouse-to-destination workflow:
maintained sync scripts, recurring exports, destination-specific mappings, business
requests for modeled attributes or audiences, or active evaluation of activation
tools. A warehouse, named technology, senior data role, or large event volume is a
priority signal only; none establishes an activation need by itself.

Messaging must begin with a workflow or category hypothesis that the buyer can
validate. Do not infer private architecture, data quality, consent maturity, or
purchase intent from public firmographic or technology data.

## Product-led technical discovery

**Primary entry point:** technical documentation and a sandbox using synthetic data.

1. An evaluator reviews a warehouse-to-destination use case or implementation guide.
2. The evaluator creates a sandbox project with sample models and a non-production destination.
3. Product telemetry records completed mappings, test deliveries, and errors without capturing customer data.
4. A fit prompt asks about the recurring workflow, its current limitation, the
   production warehouse, use case, destination, and owners.
5. Qualified evaluators can request a production-readiness review.

This path is most common for Warehouse Sync and usually begins with a Head of Data
or Data Engineer. Sandbox activity signals technical interest, not ICP fit or
purchase intent by itself.

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

## Product routing

- Confirm workflow need and ownership before technical and firmographic priority.
- Confirm operational readiness before recommending a production path.
- Route repeatable attribute or record delivery toward Warehouse Sync.
- Route marketer-managed segments and audience publishing toward Audience Activation.
- Recommend both only when the buyer has two distinct owned use cases.
- Do not treat a connector request as a business use case.
- Stop when identity, consent, source ownership, or destination ownership is unknown.

## Handoffs

Product owns sandbox education. Revenue owns qualification and commercial scope.
The technical specialist owns production-readiness evidence. Customer Success owns
pilot coordination and post-sale adoption; Engineering owns connector defects.

## Motion measures

Track sandbox-to-readiness-review conversion, qualified pilot rate, time to security
approval, pilot acceptance, production activation, and 90-day use-case adoption.
Do not optimize sandbox sign-ups without measuring production fit and adoption.
