---
kind: icp
id: commerce-analytics-icp
scope: product-group:commerce-analytics
strategy_ref: product-group-strategy:commerce-analytics-strategy
segment_ref: segment:commerce-analytics-core-segment
use_case_ref: use-case:commerce-analytics-core-use-case
meta:
  source: synthetic
  status: example
  updated: 2026-07-14
  owner: Revenue
  last_verified: 2026-07-14
  verify_every: 90d
---

# Commerce Analytics ICP

This profile is self-contained. Use it to qualify an organization without loading
personas, buying context, go-to-market, positioning, or product documents.

## Market basis

**Primary basis:** job-to-be-done.

Commerce teams repeatedly reconcile customer, product, and revenue data to make
trading, retention, merchandising, and planning decisions. The relevant market is
made up of organizations performing this workflow, not every company that happens
to match a commerce-industry, revenue, region, or headcount filter.

**Category context:** governed commerce analytics that replaces or extends
storefront reports, spreadsheet reporting, and custom warehouse-and-BI workflows.

Observable evidence of participation in this market includes recurring commerce
reporting, repeated metric reconciliation, decisions that depend on customer or
product analysis, or active evaluation of a replacement for the current workflow.

## Canonical segment summary

Within that market, the best fit is a first-party e-commerce brand with enough
transaction and behavioral data to require analysis beyond storefront reports. It
wants governed recurring analysis without maintaining a fully custom analytics
stack and can name both the workflow owner and the decision the analysis supports.

The canonical definition is `segment:commerce-analytics-core-segment`; the primary
workflow is `use-case:commerce-analytics-core-use-case`. This summary is repeated
here so the ICP remains usable as a self-contained qualification artifact.

## Qualification criteria

An organization is a strong fit when all market-and-need and operational-readiness
criteria are true. Need-intensity and firmographic criteria prioritize qualified
organizations; they do not establish need by themselves.

### Market and need fit — required

- A commercial team performs recurring customer, product, or revenue analysis.
- The current workflow requires repeated reconciliation, depends on undocumented
  analysis, or cannot answer an owned commercial question reliably.
- The organization can name the decision the analysis should improve and the team
  responsible for acting on it.

### Operational readiness — required

- The company operates a first-party online storefront and controls its transaction data.
- At least one commercial team owns conversion, retention, or merchandising outcomes.
- The organization can provide lawful access to order, product, and customer-event data.
- An accountable business owner will validate metric definitions during onboarding.

### Need-intensity signals

- More than one team creates recurring performance reports from the same source data.
- Analysts spend at least two working days per month reconciling commerce metrics.
- The business operates across multiple markets, storefronts, or product categories.
- Leadership reviews customer acquisition, repeat purchase, and product performance monthly.

### Firmographic priority

- Annual online revenue is typically between EUR 5 million and EUR 150 million.
- The organization sells directly to consumers in Europe or the United Kingdom.
- The company typically has 50–500 employees or a commerce team of at least five people.

These ranges describe commercial priority, not proof that the workflow or need exists.

## Data readiness

The minimum viable data set includes orders, line items, products, customer
identifiers, timestamps, currencies, refunds, and a consistent storefront or
tracking source. A data warehouse is helpful but not required.

## Disqualifiers

- Marketplace-only sellers that cannot access customer-level transaction data.
- Businesses whose reporting needs remain basic and are met by storefront reports.
- Organizations seeking a general financial reporting or statutory accounting system.
- Teams unwilling or unable to define an accountable metric owner.
- Use cases that depend on unlawfully collected data or unidentified data provenance.
- Buyers expecting the product to replace their storefront, warehouse, or engagement platform.

## Quick qualification check

First confirm the recurring workflow, its current failure or cost, the decision it
supports, and its owner. Then confirm storefront ownership, available data, lawful
access, and metric-validation ownership. Check disqualifiers before using revenue,
region, or headcount to prioritize the qualified organization. If any required
criterion is unknown, record it as unknown; do not infer fit from firmographics,
brand size, industry, or reputation.

Record each required criterion as `true`, `false`, or `unknown`. A single `false`
required criterion means the organization is not currently qualified. Any `unknown`
required criterion means the result is incomplete, not provisionally qualified.
