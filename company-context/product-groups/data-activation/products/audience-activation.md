---
kind: product-context
id: audience-activation
scope: product-group:data-activation
product_group: data-activation
strategy_ref: product-group-strategy:data-activation-strategy
segment_ref: segment:data-activation-core-segment
use_case_ref: use-case:data-activation-core-use-case
audience_refs:
  - icp:data-activation-icp
  - personas:data-activation-personas
buying_context_ref: buying-context:data-activation-buying-context
positioning_ref: positioning:data-activation-positioning
gtm_motion_ref: gtm-motions:data-activation-motions
meta:
  source: synthetic
  status: example
  updated: 2026-07-15
  owner: Product
  last_verified: 2026-07-15
  verify_every: 90d
---

# Audience Activation

## Intended audience

Audience Activation is designed for an organization matching
`icp:data-activation-icp` whose lifecycle team needs controlled segment creation
from approved warehouse attributes. The Lifecycle Marketing Lead is the primary
champion; the Head of Data is the technical and governance sponsor.

## Primary use case

Audience Activation supports the governed audience creation and publishing variant
of `use-case:data-activation-core-use-case`. It is selected for a named lifecycle
workflow with acceptance evidence, not for generic access to warehouse data.

## Problem

Lifecycle marketers wait for engineering to create segments or rebuild definitions
inside destination tools, producing delays, inconsistent counts, and unclear
consent or suppression behavior.

## Product role

Business users can define, review, and publish audiences from an approved data
model while technical owners retain control over available fields, destinations,
refresh rules, and production access.

## Features and availability

| Feature | Availability | Conditions and limits |
|---|---|---|
| Governed audience builder | Live | Uses administrator-approved fields and operators from one approved customer model |
| Preview counts | Live | Counts depend on current warehouse data, identity, filters, and destination rules |
| Definition history and review workflow | Live | Customer names reviewers, naming rules, and approval ownership |
| Publishing approvals | Live | Production access follows customer governance and supported destinations |
| Hourly or daily refresh schedules | Live | No real-time event triggers; delivery depends on destination availability |
| Delivery monitoring and alerts | Live | Named business and technical recipients required |
| Suppression and deletion propagation | Live | Uses approved warehouse attributes; product does not decide permitted marketing use |

## Capability chains

| Current problem | Enabling feature | User capability | First-order benefit | Role in differentiation |
|---|---|---|---|---|
| Audience requests wait in engineering queues | Governed builder with approved fields and operators | Define a scoped audience without a new engineering ticket for every rule change | Shorter iteration within approved governance | Distinctive relative to ticket-driven audience creation |
| Definitions are rebuilt inside destination tools | Preview counts and definition history | Review the warehouse-based definition and expected membership before publishing | More understandable and repeatable audience logic | Distinctive relative to destination-only definitions |
| Business access risks bypassing controls | Review workflow and publishing approvals | Route an audience through named review and production approval | Controlled self-service rather than unrestricted activation | Core differentiator |
| Delivery failure is visible only after a workflow is affected | Monitoring and alerts | Observe audience delivery and involve the named owner | Faster detection and clearer responsibility | Supporting differentiator |

## Package limits

- One production warehouse connection and one approved customer model.
- Up to three supported engagement destinations.
- Up to 15 business users and five administrators.
- 15 million delivered audience memberships per month.

## Included services

- Three onboarding workshops covering model, governance, and adoption.
- Production-readiness review for the documented initial audience.
- Pilot coordination for one audience, one destination, cadence, permitted use,
  expected counts, and acceptance evidence.

## Direct benefits and outcome hypotheses

The direct benefits are controlled audience iteration, understandable definitions,
visible approvals, and observable delivery within the scoped workflow.

Faster campaign testing and lower engineering wait time are expected only when the
approved workflow is adopted. Retention, conversion, revenue, attribution, and
campaign performance depend on strategy, execution, delivery, and customer response
and are not guaranteed product results.

## Exclusions

- Campaign design, message delivery, attribution, or journey orchestration.
- Identity resolution beyond the customer-approved model.
- Acting as the legal consent record or deciding permitted marketing use.
- Real-time event triggers, unlimited audiences, or unsupported destinations.
- General attribute sync unrelated to a governed audience use case.

## Packaging and pricing assumptions

- **Subscription:** EUR 24,000 per year.
- **Onboarding:** EUR 5,000 one-time.
- **Contract:** 12 months under the company commercial model.
- **Usage allowance:** 15 million delivered audience memberships per month.

All amounts are fictional, exclude tax, and require a written quote.

## Dependencies

The customer must provide an approved customer model, consent and suppression
attributes, destination access, audience naming rules, a Lifecycle Marketing owner,
and a Head of Data or delegate responsible for production governance.

## Relevant GTM motion

Audience Activation is sales-assisted. A bounded pilot must define one audience,
one destination, expected counts, permitted use, refresh cadence, and acceptance
evidence before production scope is proposed.
