---
kind: icp
id: data-activation-icp
scope: product-group:data-activation
meta:
  source: synthetic
  status: example
  updated: 2026-07-14
---

# Data Activation ICP

This profile is self-contained. Use it to qualify an organization without loading
personas, buying context, go-to-market, positioning, or product documents.

## Ideal organization

A data-mature commerce organization in Europe or the United Kingdom that already
models customer data in a cloud warehouse and needs governed delivery of that data
to business or engagement systems. It has working data infrastructure but wants to
reduce custom pipelines and shorten the path from an approved model to operational use.

## Qualification criteria

An organization is a strong fit when every required criterion and at least two
supporting criteria are true.

### Required

- A production cloud data warehouse contains modeled customer or account data.
- A technical owner controls warehouse access, schemas, and data-quality expectations.
- Customer identities can be resolved using documented, lawful identifiers.
- A business team owns at least one defined activation use case and success measure.
- At least one destination system can receive governed batch data or audiences.
- The organization can document consent, suppression, and permitted-use rules.

### Supporting

- The warehouse processes more than 10 million customer events per month.
- Three or more downstream tools depend on overlapping customer attributes.
- Data engineers maintain recurring reverse-ETL scripts or manual exports.
- Business teams wait more than one week for new fields or audience definitions.
- The company operates multiple storefronts, brands, regions, or engagement channels.
- Security or data governance requires centralized control of activation access.

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

Confirm the warehouse, modeled table, identity key, destination, business use case,
technical owner, consent rules, expected update frequency, and success measure. If
any required criterion is unknown, record it as unknown and do not infer readiness.
