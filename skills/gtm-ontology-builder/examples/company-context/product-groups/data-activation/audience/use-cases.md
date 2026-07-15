---
kind: use-case
id: data-activation-core-use-case
scope: product-group:data-activation
strategy_ref: product-group-strategy:data-activation-strategy
segment_ref: segment:data-activation-core-segment
persona_ref: personas:data-activation-personas
product_refs:
  - product-context:warehouse-sync
  - product-context:audience-activation
meta:
  source: synthetic
  status: example
  updated: 2026-07-15
  owner: Product
  last_verified: 2026-07-15
  verify_every: 90d
---

# Governed warehouse-to-destination delivery

## Functional activity

A data team and an accountable business owner deliver approved modeled customer
data from the warehouse into an operational system on a recurring schedule while
preserving documented identity, access, consent, suppression, deletion, monitoring,
and recovery behavior.

This is the umbrella use case for Data Activation. Reduced engineering effort,
faster campaign execution, and business growth are potential outcomes, not the
functional activity itself.

## Actors and context

- **Technical sponsor:** Head of Data or equivalent architecture and governance owner.
- **Technical operator:** Data Engineer or platform owner responsible for mappings,
  credentials, monitoring, and recovery.
- **Business owner:** Lifecycle Marketing Lead or another owner of the destination
  workflow and its success measure.
- **Validators:** Privacy or Security, destination owner, and procurement where required.
- **Trigger:** a recurring delivery request, new destination, engineering bottleneck,
  reliability incident, governance review, or approved warehouse-model launch.
- **Frequency:** scheduled batch delivery, normally from 15-minute intervals through
  daily cadence depending on the offer and approved workflow.

## Inputs

- a production warehouse and approved modeled table;
- stable lawful identifiers and documented destination keys;
- approved fields, transformations, consent, suppression, and deletion attributes;
- supported destination access and customer-managed credentials;
- refresh cadence, failure behavior, acceptance evidence, and named owners.

## Shared workflow

1. Select an approved warehouse model and owned operational use case.
2. Confirm permitted fields, identity behavior, destination, cadence, and owners.
3. Map source attributes or audience definitions to the supported destination behavior.
4. Validate counts, fields, suppressions, deletes, and rejected records before production.
5. Review and approve the production configuration under the customer's access rules.
6. Deliver on the agreed schedule and expose run status, errors, and audit evidence.
7. Alert the named owner, retry or replay according to the runbook, and reconcile exceptions.
8. Review adoption and expand only after the initial workflow meets its acceptance evidence.

## Variant A: modeled attribute or record delivery

**Product:** `product-context:warehouse-sync`.

The technical operator maps approved warehouse fields to operational-system records
and runs observable, versioned batch syncs. Success depends on delivery accuracy,
recovery behavior, and reduced destination-specific maintenance for the scoped flow.

This variant does not include business-user audience building, campaign execution,
or identity creation.

## Variant B: governed audience creation and publishing

**Product:** `product-context:audience-activation`.

The Lifecycle Marketing owner defines an audience using administrator-approved
fields and operators, previews and reviews the definition, and publishes it to an
approved engagement destination under technical governance.

Success depends on understandable definitions, expected counts, permitted use,
delivery evidence, and adoption by the owned lifecycle workflow. This variant does
not include campaign design, orchestration, attribution, or consent determination.

## Current methods

Teams commonly use custom scripts, manual exports, native destination connectors,
or a broad customer-data platform. These remain valid alternatives. The use case
becomes a fit when the current method cannot meet the owned workflow's reliability,
governance, maintenance, or speed requirements within the organization's capacity.

## Friction

- destination-specific code duplicates mapping and business logic;
- business changes wait for engineering tickets;
- audience or attribute definitions diverge inside destination tools;
- access, consent, suppression, or deletion handling is difficult to audit;
- failures lack a named owner, rejected-row detail, retry, replay, or reconciliation;
- technical interest exists without a production owner or measurable business use case.

## Desired output

A production delivery flow with approved source logic, explicit destination behavior,
named technical and business owners, observable runs, recoverable failures, and
acceptance evidence tied to the operational use case.

The product can make delivery more repeatable and observable. The customer remains
responsible for source quality, permitted use, downstream configuration, adoption,
and the business result.

## Success evidence

- The initial modeled table, use case, and destination pass documented pilot criteria.
- Delivered fields or audience counts match the approved rules within agreed tolerances.
- Consent, suppression, deletion, and identity behavior are verified for the scope.
- Failed or partial runs alert the owner and can be explained and recovered as documented.
- The business owner uses the delivered data in the intended operational workflow.
- Expansion reuses the ownership and governance model without hidden custom engineering.

## Boundaries

This use case does not include warehouse modeling, ingestion, anonymous identity
resolution, legal consent decisions, sub-second streaming, campaign execution,
general commerce reporting, or autonomous production activation. Treat those needs
as another system, separately validated scope, or an explicit gap.
