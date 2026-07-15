---
kind: icp
id: data-activation-icp
scope: product-group:data-activation
strategy_ref: product-group-strategy:data-activation-strategy
segment_ref: segment:data-activation-core-segment
use_case_ref: use-case:data-activation-core-use-case
meta:
  source: synthetic
  status: example
  updated: 2026-07-15
  owner: Revenue
  last_verified: 2026-07-15
  verify_every: 90d
---

# Data Activation ICP

This profile is self-contained. Use it to qualify an organization without loading
personas, buying context, go-to-market, positioning, or product documents.

## Market basis

**Primary basis:** job-to-be-done.

Data and business teams repeatedly deliver approved warehouse data to operational
or engagement systems while preserving identity, consent, suppression, ownership,
and recovery behavior. The relevant market is made up of organizations performing
this workflow, not every company with a warehouse or a particular technology.

**Category context:** governed warehouse data activation that replaces or extends
custom reverse-data pipelines, manual exports, native destination connectors, and
broad customer-data platforms.

Observable evidence of participation in this market includes maintained sync
scripts, recurring exports, destination-specific mappings, business requests for
warehouse attributes or audiences, or active evaluation of data-activation tools.

## Canonical segment summary

Within that market, the best fit is a data-mature commerce organization that has a
trusted modeled layer and an owned use case for governed delivery to business or
engagement systems. It wants to reduce custom pipelines and shorten the path from
an approved model to operational use without replacing the warehouse.

The canonical definition is `segment:data-activation-core-segment`; the umbrella
workflow and its two offer variants are defined in
`use-case:data-activation-core-use-case`. This summary is repeated here so the ICP
remains usable as a self-contained qualification artifact.

## Qualification criteria

An organization is a strong fit when all market-and-need and operational-readiness
criteria are true. Need-intensity and firmographic criteria prioritize qualified
organizations; they do not establish need by themselves.

### Market and need fit — required

- A team performs or is preparing a recurring warehouse-to-destination delivery workflow.
- The current approach creates a material reliability, governance, maintenance, or speed problem.
- A business team owns at least one defined activation use case and success measure.
- A technical owner and a business owner accept responsibility for production operation and adoption.

### Operational readiness — required

- A production cloud data warehouse contains modeled customer or account data.
- A technical owner controls warehouse access, schemas, and data-quality expectations.
- Customer identities can be resolved using documented, lawful identifiers.
- At least one destination system can receive governed batch data or audiences.
- The organization can document consent, suppression, and permitted-use rules.

### Need-intensity signals

- Three or more downstream tools depend on overlapping customer attributes.
- Data engineers maintain recurring reverse-ETL scripts or manual exports.
- Business teams wait more than one week for new fields or audience definitions.
- The company operates multiple storefronts, brands, regions, or engagement channels.
- Security or data governance requires centralized control of activation access.

### Firmographic priority

- The organization operates primarily in Europe or the United Kingdom.
- The warehouse typically processes more than 10 million customer events per month.
- The company has multiple brands, regions, engagement channels, or destination systems.

These characteristics describe commercial priority and likely workflow complexity;
they are not proof that an activation need exists.

## Data readiness

The minimum viable data set includes a documented customer key, timestamped source
records, consent or suppression attributes, destination identifiers, and a modeled
table with an accountable owner. The warehouse remains the system of record.

## Disqualifiers

- No production warehouse or reliable modeled-data layer.
- No lawful identity, consent, or suppression process for the proposed use case.
- A buyer seeking only dashboards or commerce performance analysis.
- An expectation that the product will create accurate identities from anonymous,
  conflicting, or undocumented source data without customer input.
- A sub-second event-streaming requirement when batch delivery is not acceptable.
- No technical owner or no business owner for the activation use case.
- A requirement to replace the warehouse, engagement platform, or source systems.

## Quick qualification check

First confirm the recurring delivery workflow, the current failure or cost, the
owned business use case, and its technical and business owners. Then confirm the
warehouse, modeled table, identity key, destination, consent rules, update frequency,
and success measure. Check disqualifiers before using geography or scale to prioritize
the qualified organization. If any required criterion is unknown, record it as
unknown; do not infer need or readiness from technology, company size, or reputation.

Record each required criterion as `true`, `false`, or `unknown`. A single `false`
required criterion means the organization is not currently qualified. Any `unknown`
required criterion means the result is incomplete, not provisionally qualified.
