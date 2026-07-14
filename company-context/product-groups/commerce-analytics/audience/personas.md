---
kind: personas
id: commerce-analytics-personas
scope: product-group:commerce-analytics
strategy_ref: product-group-strategy:commerce-analytics-strategy
segment_ref: segment:commerce-analytics-core-segment
use_case_ref: use-case:commerce-analytics-core-use-case
icp_ref: icp:commerce-analytics-icp
meta:
  source: synthetic
  status: example
  updated: 2026-07-14
  owner: Revenue
  last_verified: 2026-07-14
  verify_every: 90d
---

# Commerce Analytics personas

These are buying and adoption roles inside
`segment:commerce-analytics-core-segment`, not demographic profiles. Titles vary;
the role a person plays in the use case and purchase is canonical.

## Head of E-commerce

**Common aliases:** Director of E-commerce, E-commerce Lead, Head of Digital Commerce.

**Buying roles:** primary champion, use-case owner, operational owner, and adoption
owner. For a bounded Growth purchase this role may also control the budget.

**Proximity to the problem:** direct. This role owns or participates in the weekly
commercial review and experiences the cost of inconsistent or person-dependent analysis.

**Responsibilities in the purchase**

- Name the recurring decision and the analysis workflow that supports it.
- Validate the problem with the current reporting method.
- Align commerce participants on scope and metric ownership.
- Confirm adoption cadence and recommend Growth or Scale after data-fit review.
- Own use after launch and surface changes in the decision or workflow.

**Direct product outcome**

A repeatable commerce review with documented definitions, drill-down, and less
spreadsheet reconciliation for the scoped team.

**Translated business outcome**

The team can act sooner and with greater confidence on trading, retention, and
merchandising questions. Conversion, repeat purchase, margin, or revenue improvement
remain hypotheses because the product does not control the commercial action.

**Triggers**

- Reporting breaks during expansion to a new market, storefront, or category.
- Weekly reviews are delayed by reconciliation or challenged definitions.
- A new leader introduces a formal performance and ownership cadence.
- An analyst departure exposes undocumented reporting logic.

**Concerns**

- Implementation may consume scarce commerce and analytics capacity.
- Reported metrics may not match finance or storefront definitions.
- A new tool may create another dashboard that the team stops using.

**Decision criteria**

- Fast connection to existing commerce data.
- Clear metric definitions and drill-down to underlying transactions.
- Useful workflows for weekly trading decisions, not only executive reporting.

**Evidence expected**

- A representative commerce data model and metric dictionary.
- Drill-down from a reported metric to its scoped source logic.
- A bounded onboarding plan with customer responsibilities.
- Clear product limits, price assumptions, and an adoption cadence.

**Likely objections**

- "We can keep doing this in spreadsheets."
- "Our storefront already provides these reports."
- "The team cannot spare time for another implementation."
- "The numbers will not match Finance."

**Influence:** initiates evaluation, defines use cases, validates adoption, and
usually recommends the selected plan.

**Journey participation:** present from problem recognition through evaluation,
data-fit validation, decision, onboarding, and adoption.

## Chief Marketing Officer

**Common aliases:** VP Marketing, Chief Growth Officer, executive commercial sponsor.

**Buying roles:** economic buyer or executive sponsor when the purchase spans
marketing, commerce, several markets, or a larger annual commitment.

**Proximity to the problem:** indirect to medium. This role experiences inconsistent
planning or budget decisions but usually does not prepare the recurring analysis.

**Responsibilities in the purchase**

- Confirm that the use case supports an owned executive or cross-team decision.
- Approve broader scope, budget, and cross-functional ownership.
- Resolve conflicts over adoption, metric governance, or team participation.
- Assess whether the proposal is a bounded analytics program rather than another dashboard.

**Direct product outcome**

Cross-team access to governed commerce and customer analysis with explicit ownership
and a review cadence.

**Translated business outcome**

Marketing, commerce, and leadership can use a shared evidence base for planning and
budget discussion. Better allocation or growth remains conditional on the quality
of the commercial decision and execution.

**Triggers**

- Leadership or a board challenges inconsistent acquisition, retention, or revenue metrics.
- Multi-market growth makes existing reporting difficult to govern.
- A broader planning cycle requires commerce and marketing to use consistent definitions.

**Concerns**

- Insight may arrive too late to influence campaign and budget decisions.
- Attribution claims may create false precision.
- Costs may expand without measurable adoption across teams.

**Decision criteria**

- Reliable cross-channel and cohort reporting.
- Governance strong enough for executive planning.
- A credible adoption plan with accountable owners and review cadence.

**Evidence expected**

- A clear distinction between Growth and Scale scope.
- Proof of definition ownership, controlled access, and cross-team adoption support.
- Commercial assumptions, total implementation effort, and success measures.

**Likely objections**

- "This is another analytics tool without an adoption plan."
- "The result does not justify the cross-team cost."
- "The attribution claims are not credible."

**Influence:** approves budget, resolves cross-functional ownership, and evaluates
whether the product supports strategic planning beyond the commerce team.

**Journey participation:** joins when the use case, economic scope, and adoption
owner are clear; remains involved at decision and quarterly adoption review for Scale.

## Supporting buying roles

| Role | Buying role | Primary gate | Evidence required |
|---|---|---|---|
| Data or Analytics Lead | Technical validator and metric-governance reviewer | Source access, model fit, identity, freshness, and definition ownership | Data-fit assessment, source mapping, metric logic, and exception handling |
| Finance Lead | Definition reviewer and possible blocker | Revenue, refund, currency, margin, and reporting boundaries | Calculation definitions, reconciliation approach, and explicit non-accounting boundary |
| Security or IT | Risk validator and possible blocker | Access method, credentials, integration, security, and support ownership | Security documentation, supported connection pattern, and incident boundary |
| Customer Success counterpart | Adoption participant | Named owners, onboarding capacity, training, and review cadence | Responsibility matrix, onboarding plan, and adoption measures |

## Relationship between personas

The Head of E-commerce normally owns the day-to-day problem and product adoption.
The CMO becomes central when the purchase affects marketing measurement, multiple
teams, or a larger annual commitment. Product files identify which persona is
primary for each offer. Data, Finance, and Security roles validate specific gates;
they do not become the primary marketing audience merely because they can block a
purchase.
