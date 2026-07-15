---
kind: use-case
id: commerce-analytics-core-use-case
scope: product-group:commerce-analytics
strategy_ref: product-group-strategy:commerce-analytics-strategy
segment_ref: segment:commerce-analytics-core-segment
persona_ref: personas:commerce-analytics-personas
product_refs:
  - product-context:growth-plan
  - product-context:scale-plan
meta:
  source: synthetic
  status: example
  updated: 2026-07-14
  owner: Product
  last_verified: 2026-07-14
  verify_every: 90d
---

# Governed recurring commerce performance analysis

## Functional activity

A commerce team prepares and runs a recurring review of customer, product, and
revenue performance so an accountable owner can make a trading, retention,
merchandising, or planning decision using numbers the participants understand and
trust.

This is the primary functional use case for Commerce Analytics. Revenue growth,
better decisions, and executive confidence are potential outcomes, not the activity
itself.

## Actor and context

- **Primary actor:** Head of E-commerce or an analyst supporting the commerce team.
- **Participants:** marketing, finance, data or analytics, and executive stakeholders
  when their definitions or decisions enter the review.
- **Trigger:** a weekly or monthly performance cadence, planning cycle, unexpected
  metric movement, or expansion that the current reporting method cannot support.
- **Frequency:** recurring, normally weekly or monthly; ad hoc drill-down occurs when
  the review identifies a material change.

## Inputs

- orders, line items, products, customers, refunds, timestamps, and currencies;
- supported behavioral or marketing events when required by the decision;
- agreed metric definitions and exception handling;
- the commercial question, accountable decision owner, and review cadence.

## Workflow

1. Ingest or refresh the supported commerce data for the agreed period.
2. Apply documented definitions for revenue, customer, product, cohort, and refund metrics.
3. Reconcile exceptions such as currencies, refunds, identity, and late-arriving data.
4. Compare performance across the dimensions required by the owned decision.
5. Drill into the customers, cohorts, products, or markets behind a material change.
6. Prepare a repeatable view for the commercial review.
7. Record the interpretation, owner, and follow-up decision outside the analytics
   calculation where human judgment is required.

## Current method

The team commonly combines storefront dashboards, spreadsheet exports, analyst
queries, or a custom warehouse-and-BI workflow. These methods remain valid
alternatives. The use case becomes a fit for Commerce Analytics when the current
method cannot produce the required recurring answer reliably within the team's
capacity and governance constraints.

## Friction

- repeated exports and reconciliation before every review;
- conflicting definitions across commerce, marketing, and finance;
- analysis that depends on one person's undocumented logic;
- insufficient customer, cohort, product, or cross-market drill-down;
- slow response when a new decision requires a different cut of the same data;
- no clear owner for definitions, validation, or adoption.

## Desired output

A governed and repeatable review package with documented definitions, traceable
source logic, the drill-down required for the decision, and a named owner who can
validate the result and act on it.

The product can make the workflow faster and more reproducible. The customer's
commercial action and downstream business result remain outside the product's sole
control.

## Success evidence

- The agreed review runs on its intended cadence without rebuilding core analysis.
- Participants use the same documented definitions for the scoped metrics.
- The owner can trace a reported change to the relevant source data and dimensions.
- The team can answer the agreed customer, product, cohort, or market question.
- Manual reconciliation decreases within the scoped workflow.
- Growth or Scale remains within its documented sources, limits, services, and
  customer responsibilities.

## Boundaries

This use case does not include statutory accounting, general-purpose BI, guaranteed
attribution, autonomous commercial decisions, operating the customer's warehouse,
or real-time audience delivery. Those needs require another system, a separately
validated product group, or an explicit gap rather than an implied capability.
