---
kind: product-context
id: scale-plan
scope: product-group:commerce-analytics
product_group: commerce-analytics
strategy_ref: product-group-strategy:commerce-analytics-strategy
segment_ref: segment:commerce-analytics-core-segment
use_case_ref: use-case:commerce-analytics-core-use-case
includes_ref: product-context:growth-plan
audience_refs:
  - icp:commerce-analytics-icp
  - personas:commerce-analytics-personas
buying_context_ref: buying-context:commerce-analytics-buying-context
positioning_ref: positioning:commerce-analytics-positioning
gtm_motion_ref: gtm-motions:commerce-analytics-motions
meta:
  source: synthetic
  status: example
  updated: 2026-07-14
  owner: Product
  last_verified: 2026-07-14
  verify_every: 90d
---

# Scale plan

## Intended audience

Scale is designed for an organization matching `icp:commerce-analytics-icp` that
needs shared analysis across multiple teams, markets, storefronts, or data sources.
The Head of E-commerce typically champions the project; the CMO is commonly the
economic buyer or executive sponsor.

## Primary use case

Scale expands `use-case:commerce-analytics-core-use-case` across multiple teams,
markets, storefronts, or supported sources. It does not add an unrelated use case;
broader scope must still support an owned recurring commerce decision.

## Problem

The organization has useful analysis in several tools, but definitions, access,
and reporting cadences differ across teams. Leaders need broader adoption and
governance without committing to a general-purpose data-platform program.

## Product role

A shared commerce analytics environment with cross-team definitions, controlled
access, broader source coverage, and an operating cadence for maintaining trust.

## Features and availability

Scale includes the Growth feature set plus:

| Feature | Availability | Conditions and limits |
|---|---|---|
| Multi-storefront and multi-source commerce model | Live | Up to five storefronts and three supported behavioral or marketing sources |
| Multi-market and multi-currency analysis | Live | Agreed identity, currency, and comparison rules required |
| Role-based access and team workspaces | Live | Customer names users, roles, and workspace owners |
| Definition ownership and change history | Live | Governance participants and approval ownership required |
| Governed warehouse export | Live | Supported destination and customer-managed credentials required |

## Capability chains

| Current problem | Enabling feature | User capability | First-order benefit | Role in differentiation |
|---|---|---|---|---|
| Teams use conflicting definitions and reporting cadences | Definition ownership, change history, and shared models | Govern definitions and review changes across teams | Fewer silent definition conflicts and clearer accountability | Distinctive relative to unmanaged reporting workflows |
| Markets or storefronts cannot be compared consistently | Multi-storefront, multi-source, and multi-currency model | Analyze the agreed metrics across scoped markets and sources | One governed comparison without rebuilding each market separately | Distinctive for the expanded commerce use case |
| Broader access creates control concerns | Role-based access and team workspaces | Give participants scoped access to the same underlying model | Broader adoption without making every view universally accessible | Table stakes for multi-team deployment |
| Modeled results need a governed downstream path | Governed warehouse export | Deliver scoped analytics data to a supported customer destination | Reuse modeled output without implying real-time activation | Supporting differentiator |

## Package limits

- Up to five production storefronts and three supported behavioral or marketing sources.
- Up to 40 named users and 12 scheduled report deliveries.
- Up to 10 million tracked customer events per month.

## Included services

- Named Customer Success owner.
- Quarterly adoption review.
- Four onboarding workshops covering sources, metrics, governance, and adoption.

## Direct benefits and outcome hypotheses

The direct benefits are consistent analysis across the scoped teams and markets,
controlled access, visible definition ownership, and a repeatable governance cadence.

Better executive planning, budget allocation, retention, margin, or revenue are
possible higher-order outcomes. They depend on adoption, source quality, governance,
interpretation, and commercial execution and are not guaranteed product results.

## Exclusions

- Building or operating the customer's warehouse and ingestion infrastructure.
- Real-time audience delivery to engagement destinations.
- Bespoke machine-learning models or guaranteed attribution accuracy.
- Unlimited custom sources, historical reconstruction, or data cleansing.
- Contract terms or service levels not written in the order form.

## Packaging and pricing assumptions

- **Subscription:** starts at EUR 30,000 per year.
- **Onboarding:** starts at EUR 6,000 one-time.
- **Contract:** 12 months under the company commercial model.
- **Usage allowance:** up to 10 million tracked customer events per month.

Final pricing depends on source count, event volume, storefronts, historical data,
and governance complexity. All amounts are fictional and exclude tax.

## Dependencies

The customer must name business and technical owners, provide source access, agree
on identity and currency rules, and participate in governance workshops. Warehouse
export requires a supported destination and customer-managed credentials.

## Relevant GTM motion

Scale is sold through inbound or targeted outbound, always with discovery and a
technical data-fit assessment. Recommend it when broader scope is evidenced, not
solely because a buyer has a larger budget.
