---
kind: product-context
id: growth-plan
scope: product-group:commerce-analytics
product_group: commerce-analytics
strategy_ref: product-group-strategy:commerce-analytics-strategy
segment_ref: segment:commerce-analytics-core-segment
use_case_ref: use-case:commerce-analytics-core-use-case
audience_refs:
  - icp:commerce-analytics-icp
  - personas:commerce-analytics-personas
buying_context_ref: buying-context:commerce-analytics-buying-context
positioning_ref: positioning:commerce-analytics-positioning
gtm_motion_refs:
  - gtm-motion:commerce-analytics-inbound
meta:
  source: synthetic
  status: example
  updated: 2026-07-14
  owner: Product
  last_verified: 2026-07-14
  verify_every: 90d
---

# Growth plan

## Intended audience

Growth is designed for an organization matching `icp:commerce-analytics-icp` with
one primary commerce team and standard data sources. The Head of E-commerce is the
typical champion and operational owner.

## Primary use case

Growth supports `use-case:commerce-analytics-core-use-case` for one primary commerce
team with standard sources and one reporting currency. It packages an existing
workflow at bounded scope; it is not a separate market from Scale.

## Problem

The team has outgrown native storefront reports and manually reconciles recurring
customer, product, and revenue analysis. It needs trustworthy weekly insight but
does not require a multi-team governance program.

## Product role

A governed commerce workspace with agreed metric definitions, repeatable analysis,
and enough drill-down for the team to replace its core spreadsheet reporting cycle.

## Features and availability

| Feature | Availability | Conditions and limits |
|---|---|---|
| Standard order, customer, product, cohort, refund, and repeat-purchase models | Live | Supported source model and agreed definitions required |
| Documented metric dictionary | Live | Customer validates definitions and exception handling |
| Transaction and dimension drill-down | Live | Limited to scoped, lawfully accessible source data |
| Single-currency normalization | Live | One reporting currency under the standard rules |
| Scheduled report delivery | Live | Up to three deliveries within the package |
| CSV export | Live | Export does not replace a governed warehouse integration |

## Capability chains

| Current problem | Enabling feature | User capability | First-order benefit | Role in differentiation |
|---|---|---|---|---|
| Recurring reports are rebuilt from exports | Standard commerce models and metric dictionary | Run the agreed analysis with the same definitions each cycle | Less repeated preparation and reconciliation | Distinctive for the bounded commerce workflow |
| A reported change cannot be explained | Transaction and dimension drill-down | Trace a metric movement to relevant customers, products, cohorts, or refunds | The owner can explain and validate the scoped result | Distinctive relative to basic storefront reporting |
| Weekly review preparation depends on manual distribution | Scheduled report delivery | Deliver the agreed view on its operating cadence | Fewer manual preparation steps | Table stakes supporting adoption |
| Operators need data outside the workspace | CSV export | Export the scoped result for permitted follow-up work | Portability without inventing a downstream activation capability | Table stakes |

## Package limits

- One production storefront and one supported behavioral-event source.
- Up to 10 named users and three scheduled report deliveries.
- One reporting currency.
- Up to 2 million tracked customer events per month.

## Included services

- Standard remote onboarding.
- Two metric-validation workshops.
- Configuration limited to the documented feature and source scope.

## Direct benefits and outcome hypotheses

The direct benefits are a repeatable review, documented definitions, traceable
drill-down, and fewer manual preparation steps inside the scoped workflow.

Faster commercial decisions, improved conversion, retention, margin, or revenue are
possible higher-order outcomes. They depend on the customer's source quality,
adoption, interpretation, and commercial action and are not guaranteed product results.

## Exclusions

- Custom identity resolution across unrelated brands or business units.
- Governed warehouse exports or downstream audience activation.
- Custom financial accounting, attribution, or forecasting models.
- More than one production storefront or reporting currency.
- Dedicated success management or contractual response-time commitments.

## Packaging and pricing assumptions

- **Subscription:** EUR 12,000 per year.
- **Onboarding:** EUR 2,500 one-time.
- **Contract:** 12 months under the company commercial model.
- **Usage allowance:** up to 2 million tracked customer events per month.

All amounts are fictional examples, exclude tax, and require a written quote.

## Dependencies

The customer must provide documented source access, a business owner for metrics,
and representative historical data. Onboarding cannot complete until the customer
validates required definitions and exception handling.

## Relevant GTM motion

Growth is primarily sold through the inbound sales-led motion. Recommend it only
after organizational fit and data readiness are confirmed.
