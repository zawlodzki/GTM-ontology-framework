---
kind: product-context
id: warehouse-sync
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

# Warehouse Sync

## Intended audience

Warehouse Sync is designed for an organization matching `icp:data-activation-icp`
that needs repeatable delivery of modeled attributes or records. The Head of Data
is the typical sponsor and a Data Engineer is the primary technical operator.

## Problem

Engineering maintains destination-specific scripts and manual exports that repeat
mapping logic, fail inconsistently, and consume capacity whenever a field or
destination changes.

## Outcome

Approved warehouse models are delivered to operational systems through observable,
versioned syncs with explicit ownership, failure recovery, and audit history.

## Included capabilities

- One production warehouse connection and up to three modeled source tables.
- Two supported destination connections.
- Scheduled batch syncs with a minimum 15-minute interval.
- Versioned field mappings, validation rules, and deployment history.
- Run monitoring, alerts, rejected-row detail, retry, and replay.
- Suppression and deletion propagation from approved source fields.
- Up to five operator seats and standard remote onboarding.

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
