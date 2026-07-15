---
kind: personas
id: data-activation-personas
scope: product-group:data-activation
strategy_ref: product-group-strategy:data-activation-strategy
segment_ref: segment:data-activation-core-segment
use_case_ref: use-case:data-activation-core-use-case
icp_ref: icp:data-activation-icp
meta:
  source: synthetic
  status: example
  updated: 2026-07-15
  owner: Revenue
  last_verified: 2026-07-15
  verify_every: 90d
---

# Data Activation personas

These are buying, governance, and adoption roles inside
`segment:data-activation-core-segment`, not demographic profiles. A qualified
production opportunity requires both a technical owner and a business owner.

## Head of Data

**Common aliases:** Director of Data, VP Data, Head of Data Platform, Analytics Engineering Lead.

**Buying roles:** technical sponsor, architecture owner, governance owner, and
possible economic buyer. This role can veto production activation.

**Proximity to the problem:** direct to the engineering and governance burden,
medium to the downstream business delay.

**Responsibilities in the purchase**

- Confirm warehouse and modeled-layer readiness.
- Own source access, identity rules, mappings, data-quality expectations, and runbooks.
- Define technical acceptance and the allowed production operating model.
- Bring Privacy or Security into the evaluation before production scope is proposed.
- Name the technical operator and confirm who responds to failures.

**Direct product outcome**

Approved warehouse models are delivered through observable, versioned, and
recoverable flows while the warehouse remains authoritative.

**Translated business outcome**

Engineering can support repeatable operational use without maintaining a separate
custom pipeline for every scoped destination. Capacity savings remain conditional
on connector fit, adoption, and retirement of the previous workflow.

**Triggers**

- A warehouse modernization produces an approved customer model.
- Engineering reviews fragile reverse-data pipelines or manual exports.
- A failed delivery or governance review exposes weak monitoring and ownership.
- A new destination or region multiplies mapping and permitted-use complexity.

**Concerns**

- A vendor may introduce opaque transformations or a second customer model.
- Business users may activate fields without understanding consent or quality.
- Connector failures may be difficult to detect, reconcile, or replay.

**Decision criteria**

- Clear warehouse read boundaries and destination write behavior.
- Versioned mappings, monitoring, audit history, and failure recovery.
- Fine-grained access controls and explicit handling of deletes and suppressions.

**Evidence expected**

- Source-to-destination mapping and explicit identity behavior.
- Monitoring, rejected-row detail, retry, replay, and reconciliation evidence.
- Warehouse read and destination write boundaries.
- Security, permitted-use, suppression, deletion, and credential responsibilities.
- Bounded pilot criteria and a named production runbook owner.

**Likely objections**

- "This creates a second customer model outside the warehouse."
- "The transformation and failure behavior are opaque."
- "Business access will bypass consent or data-quality controls."
- "We still have to own every operational problem, so the product adds little."

**Influence:** validates architecture and security, defines technical acceptance,
and can block the purchase when governance or operational ownership is unclear.

**Journey participation:** enters during technical discovery, remains through
readiness review, pilot, security approval, production launch, and expansion.

## Lifecycle Marketing Lead

**Common aliases:** CRM Lead, Retention Lead, Lifecycle Marketing Manager, Customer Marketing Lead.

**Buying roles:** business champion, use-case owner, adoption owner, and operator
for the Audience Activation variant.

**Proximity to the problem:** direct to the business delay and audience workflow,
indirect to pipeline implementation and warehouse governance.

**Responsibilities in the purchase**

- Name the audience or downstream workflow and its measurable acceptance evidence.
- Confirm expected fields, counts, destination, cadence, and operational owner.
- Validate whether controlled self-service improves the workflow in practice.
- Accept naming, review, publishing, and permitted-use rules.
- Own adoption after technical approval.

**Direct product outcome**

The lifecycle team can define, review, and publish a governed audience from approved
warehouse fields with visible counts and delivery status.

**Translated business outcome**

The team can reduce waiting and test lifecycle workflows more frequently while
retaining technical controls. Faster campaign learning or improved retention remains
conditional on campaign design, delivery, audience quality, and customer response.

**Triggers**

- A new lifecycle program requires warehouse attributes unavailable in the destination.
- Repeated audience requests wait in an engineering queue.
- Destination-built definitions produce inconsistent counts or unclear ownership.
- Regional expansion changes suppression or permitted-use requirements.

**Concerns**

- Data may arrive too late or differ from marketing-platform counts.
- Governance may make every change as slow as the current engineering process.
- The team may receive access without the skills to validate an audience.

**Decision criteria**

- Predictable refresh cadence and visible audience counts.
- A controlled workflow for creating, reviewing, and publishing definitions.
- Clear ownership when source data or destination delivery fails.

**Evidence expected**

- Audience builder using only administrator-approved fields and operators.
- Preview counts, definition history, review, and publishing approvals.
- A pilot with one audience, destination, cadence, permitted use, and expected counts.
- Clear response when source data or delivery fails.

**Likely objections**

- "Governance will make every change as slow as an engineering ticket."
- "The counts will not match the engagement platform."
- "We will receive access without enough context to validate the audience."
- "This does not help us design or run the campaign."

**Influence:** defines the initial use case, validates operational usefulness, and
owns adoption after technical approval.

**Journey participation:** creates or validates business urgency, joins product
evaluation, owns pilot acceptance, and remains through production adoption.

## Supporting buying roles

| Role | Buying role | Primary gate | Evidence required |
|---|---|---|---|
| Data Engineer | Technical evaluator and operational maintainer | Mapping behavior, deployment, monitoring, failure recovery, and maintenance | Sandbox project, mapping example, run detail, retry, replay, and runbook |
| Privacy or Security Lead | Permitted-use and risk reviewer | Access, credentials, consent, suppression, deletion, audit, and regional rules | Security evidence, responsibility matrix, source-field behavior, and approval path |
| Engagement Platform Owner | Destination validator | Field availability, destination configuration, counts, delivery, and downstream ownership | Test delivery, rejected records, destination acceptance, and rollback behavior |
| Finance or Procurement | Commercial and contractual reviewer | Price, usage, term, support, liability, and written scope | Order assumptions, limits, support boundaries, and commercial approval |

## Relationship between personas

The Lifecycle Marketing Lead creates urgency and defines business value. The Head
of Data protects architecture and governance. A qualified opportunity requires
both roles or named equivalents; neither technical readiness nor business demand
is sufficient alone. Data Engineering, Privacy or Security, and the destination
owner validate production gates; sandbox activity does not make them a buyer or
prove organizational fit by itself.
