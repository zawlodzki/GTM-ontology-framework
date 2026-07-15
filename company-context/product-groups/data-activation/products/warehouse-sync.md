---
kind: product-context
id: warehouse-sync
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

# Warehouse Sync

## Intended audience

Warehouse Sync is designed for an organization matching `icp:data-activation-icp`
that needs repeatable delivery of modeled attributes or records. The Head of Data
is the typical sponsor and a Data Engineer is the primary technical operator.

## Primary use case

Warehouse Sync supports the modeled attribute or record delivery variant of
`use-case:data-activation-core-use-case`. It is selected for an owned recurring
sync workflow, not because a buyer asks for a connector.

## Problem

Engineering maintains destination-specific scripts and manual exports that repeat
mapping logic, fail inconsistently, and consume capacity whenever a field or
destination changes.

## Product role

Approved warehouse models are delivered to operational systems through observable,
versioned syncs with explicit ownership, failure recovery, and audit history.

## Features and availability

| Feature | Availability | Conditions and limits |
|---|---|---|
| Scheduled batch syncs | Live | Minimum 15-minute interval and supported source and destination required |
| Versioned field mappings and validation rules | Live | Customer supplies approved models, identifiers, mappings, and destination behavior |
| Deployment history | Live | Covers configurations managed inside the product scope |
| Run monitoring, alerts, and rejected-row detail | Live | Named alert recipients and production runbook owner required |
| Retry and replay | Live | Subject to destination behavior, retained run evidence, and approved recovery procedure |
| Suppression and deletion propagation | Live | Uses approved source fields; product is not the legal consent record |

## Capability chains

| Current problem | Enabling feature | User capability | First-order benefit | Role in differentiation |
|---|---|---|---|---|
| Each destination uses separate mapping code | Versioned mappings and validation rules | Deploy approved source-to-destination behavior from one documented configuration | Less duplicated mapping logic for the scoped flow | Distinctive relative to unmanaged scripts and exports |
| Failures are discovered late and cannot be explained | Monitoring, alerts, and rejected-row detail | Observe run state and identify affected records | Faster detection and clearer operational ownership | Distinctive relative to opaque manual delivery |
| Recovery requires ad hoc engineering work | Retry, replay, and deployment history | Recover an approved run according to the runbook | More repeatable recovery within destination constraints | Supporting differentiator |
| Suppressions and deletions vary by destination | Approved source fields and propagation behavior | Carry documented suppression and deletion signals into the scoped delivery | More consistent enforcement evidence | Required governance capability, not legal consent determination |

## Package limits

- One production warehouse connection and up to three modeled source tables.
- Two supported destination connections.
- Up to five operator seats.
- 25 million delivered rows per month across two destinations.

## Included services

- Standard remote onboarding.
- Production-readiness review for the documented initial flow.
- Pilot coordination within the agreed model, use case, and destination scope.

## Direct benefits and outcome hypotheses

The direct benefits are documented mapping behavior, observable delivery, explicit
failure ownership, and more repeatable recovery for the scoped sync.

Reduced engineering maintenance and faster business access are expected only if the
customer adopts the flow and retires equivalent custom work. Campaign performance,
revenue, and other downstream business outcomes remain outside the product's control.

## Exclusions

- Building warehouse models, ingestion pipelines, or source-system extraction.
- Creating customer identities from unresolved or anonymous records.
- Business-user audience building or campaign execution.
- Sub-second streaming, unlimited custom connectors, or destination administration.
- Acting as the legal record of consent or data-processing purpose.

## Packaging and pricing assumptions

- **Subscription:** EUR 18,000 per year.
- **Onboarding:** EUR 4,000 one-time.
- **Contract:** 12 months under the company commercial model.
- **Usage allowance:** 25 million delivered rows per month across two destinations.

All amounts are fictional, exclude tax, and require a written quote.

## Dependencies

The customer must provide supported warehouse and destination access, production-ready
models, stable identifiers, approved mappings, alert recipients, and a runbook owner.
Customer-managed credentials remain under customer access control.

## Relevant GTM motion

Warehouse Sync commonly begins with product-led technical discovery and moves to
sales-assisted production review. Sandbox completion does not replace ICP,
security, or production-readiness qualification.
