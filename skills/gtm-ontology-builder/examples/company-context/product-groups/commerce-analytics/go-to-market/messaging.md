---
kind: messaging
id: commerce-analytics-messaging
scope: product-group:commerce-analytics
strategy_ref: product-group-strategy:commerce-analytics-strategy
segment_ref: segment:commerce-analytics-core-segment
use_case_ref: use-case:commerce-analytics-core-use-case
persona_ref: personas:commerce-analytics-personas
buying_context_ref: buying-context:commerce-analytics-buying-context
positioning_ref: positioning:commerce-analytics-positioning
value_proposition_ref: value-propositions:commerce-analytics-value-propositions
product_refs:
  - product-context:growth-plan
  - product-context:scale-plan
meta:
  source: synthetic
  status: example
  updated: 2026-07-15
  owner: Revenue
  last_verified: 2026-07-15
  verify_every: 90d
---

# Commerce Analytics messaging

This artifact selects approved arguments from positioning and value propositions.
It is not copy, and it does not authorize a new segment, capability, differentiator,
or proof point.

## Core message hierarchy

1. **What it is:** governed commerce analytics.
2. **Who it is for:** first-party commerce teams with an owned recurring analysis workflow.
3. **Surface problem:** the review is delayed, disputed, or unable to explain an important change.
4. **Current way:** storefront reports, spreadsheet reconciliation, custom BI, or no change.
5. **How it works:** opinionated commerce models, documented definitions, and traceable drill-down.
6. **Direct benefit:** a repeatable and explainable review within bounded scope.
7. **Offer distinction:** Growth for one team; Scale for multi-team or multi-market governance.
8. **Proof:** representative model, metric dictionary, data-fit result, responsibilities,
   and product-specific feature evidence.

## Audience selection

| Role | Lead with | Translate toward | Proof emphasis | Avoid |
|---|---|---|---|---|
| Head of E-commerce | Recurring workflow, reconciliation, explainability, and adoption | Stable review cadence and ability to own the decision | Model, drill-down, definitions, onboarding, and direct workflow evidence | Generic executive outcomes or feature dumping |
| CMO or executive sponsor | Cross-team inconsistency, ownership, and adoption | Shared evidence for planning and budget discussion | Governance, access, adoption cadence, scope, and commercial assumptions | Perfect attribution or guaranteed growth |
| Data or Analytics Lead | Supported sources, model logic, identity, freshness, and ownership | Bounded technical effort and governed reuse | Data-fit, mappings, definitions, exception handling, and warehouse-export conditions | Claims that Acme replaces the data platform |
| Finance Lead | Calculation boundaries, refunds, currencies, and traceability | Confidence in the scoped commercial metric discussion | Definitions, reconciliation rules, and explicit non-accounting boundary | Calling analytics statutory or financial reporting |
| Security or IT | Access, credentials, supported integrations, and responsibility | Bounded implementation and operational risk | Security evidence, connection model, and incident boundary | "Effortless" setup or unspecified access |

## Awareness-stage matrix

| Stage | Primary question | Message objective | Message and proof | Suitable asset or channel | Call to action |
|---|---|---|---|---|---|
| Problem or outcome aware | Why is our commerce review slow or disputed? | Make the recurring workflow and struggling moment visible | Show reconciliation, definition conflict, and person dependency using practical examples | Educational article, checklist, benchmark, or webinar | Compare the current workflow against the checklist |
| Use-case aware | What should a better recurring analysis workflow do? | Define the activity, inputs, output, cadence, and ownership | Explain governed recurring review without introducing distant outcomes | Use-case guide, workshop, or diagnostic | Document the owned decision and workflow |
| Category aware | Should we extend reports, keep spreadsheets, build BI, or buy commerce analytics? | Establish the recognizable category and honest alternatives | Compare control, effort, depth, governance, and adoption boundaries | Comparison guide or discovery conversation | Select the approaches worth validating |
| Product aware | Can Commerce Analytics support our data and decision? | Connect the use case to product truth | Show models, definitions, drill-down, package boundaries, and offer distinction | Product page, representative demo, or first-call deck | Book structured discovery or data-fit review |
| Validation and decision | Which offer fits and what risk remains? | Make scope, ownership, proof, and assumptions explicit | Use data-fit result, security evidence, price, responsibility matrix, and onboarding plan | Technical review, proposal, and decision pack | Approve, reject, or close a documented gap |
| Adoption | Is the agreed workflow running and owned? | Reinforce operating behavior rather than repeat acquisition copy | Show validated definitions, cadence, ownership, usage, and unresolved gaps | Onboarding plan and adoption review | Complete the next workflow milestone |

## Offer-specific emphasis

### Growth

- Lead with repeated preparation and explainability for one commerce team.
- Show standard models, metric definitions, drill-down, supported source limits, and
  two validation workshops.
- Do not imply multi-team governance, governed warehouse export, or downstream activation.

### Scale

- Lead with definition ownership and consistent analysis across evidenced teams,
  markets, storefronts, sources, or currencies.
- Show change history, access controls, governance workshops, and adoption review.
- Do not imply unlimited sources, real-time activation, warehouse operation, or
  guaranteed cross-channel attribution.

## Channel briefs

### Inbound education

- **Primary audience:** Head of E-commerce experiencing a visible workflow problem.
- **Primary question:** why does the recurring review remain unreliable despite
  existing reports and spreadsheets?
- **Argument:** the issue is repeatability, definitions, drill-down, and ownership,
  not simply a lack of dashboards.
- **Proof:** practical examples and a workflow diagnostic; avoid premature product claims.

### Targeted outbound

- **Primary audience:** likely commerce champion at an account with a visible trigger.
- **Primary question:** is this operational hypothesis true for their current workflow?
- **Argument:** name the public trigger, state a narrow hypothesis, and ask the buyer
  to validate it.
- **Proof:** no private performance claim; use only observable context and a relevant
  workflow example.

### Discovery and data-fit

- **Primary audience:** champion plus technical validator.
- **Primary question:** is the use case owned, urgent, supportable, and within a
  documented offer?
- **Argument:** connect the current method and struggling moment to product truth,
  responsibilities, limits, and success evidence.
- **Proof:** live customer inputs, representative model, and explicit gaps.

## Must say

- The recurring workflow, owned decision, current alternative, and struggling moment.
- Which feature and capability support each direct benefit.
- The relevant product limits, customer responsibilities, and proof strength.
- Whether a business outcome is a product fact, expected benefit, or possibility.

## Must not say

- "Increase revenue", "improve retention", or "make better decisions" as an
  unsupported primary promise.
- "Single source of truth", "AI-powered", "all-in-one", or "easy to use" as the
  differentiator without a specific mechanism and comparison.
- That the product replaces the customer's warehouse, storefront, engagement tool,
  accounting system, or human commercial judgment.
- That a visible trigger proves a private problem, purchase intent, or ICP fit.
