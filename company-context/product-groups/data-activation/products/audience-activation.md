---
kind: product-context
id: audience-activation
scope: product-group:data-activation
product_group: data-activation
audience_refs:
  - icp:data-activation-icp
  - personas:data-activation-personas
gtm_motion_ref: gtm-motions:data-activation-motions
meta:
  source: synthetic
  status: example
  updated: 2026-07-14
  last_verified: 2026-07-14
  verify_every: 90d
---

# Audience Activation

## Intended audience

Audience Activation is designed for an organization matching
`icp:data-activation-icp` whose lifecycle team needs controlled segment creation
from approved warehouse attributes. The Lifecycle Marketing Lead is the primary
champion; the Head of Data is the technical and governance sponsor.

## Problem

Lifecycle marketers wait for engineering to create segments or rebuild definitions
inside destination tools, producing delays, inconsistent counts, and unclear
consent or suppression behavior.

## Outcome

Business users can define, review, and publish audiences from an approved data
model while technical owners retain control over available fields, destinations,
refresh rules, and production access.

## Included capabilities

- One production warehouse connection and one approved customer model.
- Up to three supported engagement destinations.
- Governed audience builder using administrator-approved fields and operators.
- Preview counts, definition history, review workflow, and publishing approvals.
- Hourly or daily refresh schedules with delivery monitoring and alerts.
- Suppression and deletion propagation from approved warehouse attributes.
- Up to 15 business users, five administrators, and three onboarding workshops.

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
