---
kind: gtm-motions
id: commerce-analytics-motions
scope: product-group:commerce-analytics
strategy_ref: product-group-strategy:commerce-analytics-strategy
segment_ref: segment:commerce-analytics-core-segment
use_case_ref: use-case:commerce-analytics-core-use-case
icp_ref: icp:commerce-analytics-icp
persona_ref: personas:commerce-analytics-personas
buying_context_ref: buying-context:commerce-analytics-buying-context
positioning_ref: positioning:commerce-analytics-positioning
value_proposition_ref: value-propositions:commerce-analytics-value-propositions
messaging_ref: messaging:commerce-analytics-messaging
product_refs:
  - product-context:growth-plan
  - product-context:scale-plan
motions:
  - id: commerce-analytics-inbound
    name: Inbound education and capture
    summary: Educational content leads to discovery and a data-fit assessment; default motion for Growth.
  - id: commerce-analytics-outbound
    name: Targeted outbound
    summary: Trigger-based SDR outreach validating one workflow hypothesis; used selectively for Scale accounts.
meta:
  source: synthetic
  status: example
  updated: 2026-07-15
  owner: Revenue
  last_verified: 2026-07-15
  verify_every: 90d
---

# Commerce Analytics GTM motions

## Motion summary

**GTM phase:** expansion inside the established Commerce Analytics segment.

**Model:** sales-led, supported by inbound education and selective one-to-one
outbound. Both paths lead to discovery and a data-fit assessment before a product
recommendation. The company does not offer unguided self-service purchase because
metric ownership, source access, and operational readiness require validation.

**Primary channel:** practical educational content distributed through organic
search and the company's email audience. It fits a use-case- or category-aware
champion who actively investigates recurring reporting and analysis problems.

**Secondary channel:** SDR email with optional LinkedIn follow-up for accounts with
a visible trigger. It validates a workflow hypothesis; it does not claim private
knowledge or purchase intent.

## Market targeting

Target organizations showing evidence of the commerce-analysis workflow: recurring
metric reconciliation, spreadsheet reporting, cross-team definition conflicts, or
an owned decision that current storefront reports cannot support. Buying triggers
and category-evaluation signals strengthen priority but do not replace evidence of
the underlying workflow.

Revenue, headcount, geography, industry, and job titles may narrow or prioritize
accounts only after a workflow hypothesis exists. Never qualify an account or write
outreach solely because it matches firmographic filters.

## Inbound education and capture

**Primary offer:** practical guidance on commerce metrics, retention analysis,
and replacing spreadsheet reporting.

1. Problem- and use-case-stage content helps the champion diagnose the recurring
   workflow, current alternative, and struggling moment.
2. A checklist, benchmark, webinar, or use-case guide invites the buyer to document
   the owned decision and reporting cadence.
3. Revenue captures the workflow, business problem, owner, urgency, current method,
   and source context before offering discovery.
4. A strong-fit account receives a 30-minute discovery call focused on qualification
   and buying context, not a generic product tour.
5. Qualified buyers complete a structured data-fit assessment with the technical validator.
6. Sales recommends Growth or Scale and documents the evidence, assumptions, gaps,
   responsibilities, and reason for the route.

Inbound is the default motion for Growth. It also creates Scale opportunities when
multiple teams, sources, or governance requirements appear during discovery.

## Targeted outbound motion

Outbound focuses on accounts showing a visible trigger such as international
expansion, a new commerce leader, rapid catalog growth, or an analytics hiring gap.
The SDR uses public context to state one narrow operational hypothesis and asks the
likely champion to validate it. Follow-up may provide one relevant workflow example
or diagnostic, but must not claim private performance data or infer fit from the
trigger alone.

Outbound is used selectively for Scale accounts and must identify a likely business
owner before a technical evaluation begins. It is reviewed as a separate source so
weak outbound qualification cannot be hidden by inbound performance.

## Journey execution

| Stage | Primary asset or interaction | Owner | Exit signal |
|---|---|---|---|
| Problem or outcome aware | Educational article, checklist, benchmark, or webinar | Revenue marketing | Buyer identifies a recurring workflow and meaningful failure |
| Use-case aware | Use-case guide or workflow diagnostic | Revenue marketing and champion | Decision, cadence, owner, inputs, and desired output are named |
| Category aware | Alternative comparison and discovery | Revenue | Buyer accepts a comparison frame and chooses paths to validate |
| Product aware | Representative demo and structured discovery | Revenue and Product specialist | Required ICP criteria are known and product validation is warranted |
| Validation and decision | Data-fit assessment, security review, proposal, and onboarding plan | Revenue, technical specialist, Finance, Customer Success | Scope, responsibilities, gaps, price, and adoption ownership are accepted |
| Adoption | Metric validation, workflow launch, and adoption review | Customer Success and champion | The agreed review runs on cadence with named ownership |

## Qualification and routing

- Use `icp:commerce-analytics-icp` for organizational fit.
- Use `segment:commerce-analytics-core-segment` for the customer situation and
  `personas:commerce-analytics-personas` when tailoring the interaction.
- Confirm the recurring workflow, its current failure or cost, and its owner first.
- Confirm operational and data readiness before applying firmographic priority.
- Route one-team, standard-source needs toward Growth.
- Route multi-team, multi-source, governance-heavy needs toward Scale.
- Stop qualification when a required ICP criterion is unknown; record the gap.
- Do not recommend a plan until the data-fit assessment confirms minimum inputs.

No decision is a valid outcome when the current alternative still works, urgency is
insufficient, implementation capacity is unavailable, or a required owner, source,
security condition, or definition cannot be confirmed.

## Handoffs

Revenue owns discovery, qualification, and the commercial proposal. A technical
specialist validates source access and complexity. Customer Success joins before
signature when onboarding requires metric workshops or multiple stakeholder teams.

The accepted data-fit result, responsibilities, definitions requiring validation,
and unresolved gaps pass to Customer Success. A closed deal without a named adoption
owner or recurring review cadence is not ready for routine onboarding.

## Capacity and execution constraints

- Maintain one primary segment and inbound education path while testing supporting tactics.
- Do not add a channel until the current motion has an owner, adequate review period,
  and stage-level conversion evidence.
- Discovery and data-fit capacity limits how many qualified opportunities can run
  concurrently; do not compensate by weakening qualification.
- Custom source, model, or service needs remain gaps or separate scope and must not
  be hidden inside the standard offer.

## Motion measures

Review monthly by source and offer:

- content-to-workflow-diagnostic conversion;
- diagnostic-to-qualified-discovery rate;
- outbound hypothesis response and qualified-discovery rate;
- data-fit completion and disqualification reasons;
- proposal conversion and days to decision;
- Growth versus Scale routing and evidence;
- share of closed customers whose recommended plan changes during onboarding;
- time to the first recurring review and adoption of its agreed cadence.

A high onboarding plan-change rate indicates weak qualification or routing. Expand
channels or adjacent segments only when the same customer situation, positioning,
qualification logic, bounded offer, and adoption path remain repeatable.
