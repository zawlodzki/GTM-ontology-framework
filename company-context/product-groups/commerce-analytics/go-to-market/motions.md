---
kind: gtm-motions
id: commerce-analytics-motions
scope: product-group:commerce-analytics
meta:
  source: synthetic
  status: example
  updated: 2026-07-14
---

# Commerce Analytics GTM motions

## Motion summary

Commerce Analytics uses a sales-led model supported by inbound education and
targeted outbound. Both paths lead to a discovery and data-fit assessment before
a product recommendation. The company does not offer an unguided self-service
purchase because metric ownership and data readiness must be confirmed.

## Inbound motion

**Primary offer:** practical guidance on commerce metrics, retention analysis,
and replacing spreadsheet reporting.

1. A prospect engages with educational content, a benchmark, or a product demonstration.
2. Revenue captures the product group, business problem, organization profile, and data sources.
3. Strong-fit accounts receive a 30-minute discovery call.
4. Qualified buyers complete a structured data-fit assessment.
5. Sales recommends Growth or Scale and documents the reason for the choice.

Inbound is the default motion for Growth. It also creates Scale opportunities when
multiple teams, sources, or governance requirements appear during discovery.

## Targeted outbound motion

Outbound focuses on accounts showing a visible trigger such as international
expansion, a new commerce leader, rapid catalog growth, or an analytics hiring gap.
Messaging starts with a specific operational hypothesis and asks the buyer to
validate it; it must not claim knowledge of private performance data.

Outbound is used selectively for Scale accounts and must identify a likely business
owner before a technical evaluation begins.

## Qualification and routing

- Use `icp:commerce-analytics-icp` for organizational fit.
- Load `personas:commerce-analytics-personas` only when tailoring the conversation.
- Route one-team, standard-source needs toward Growth.
- Route multi-team, multi-source, governance-heavy needs toward Scale.
- Stop qualification when a required ICP criterion is unknown; record the gap.
- Do not recommend a plan until the data-fit assessment confirms minimum inputs.

## Handoffs

Revenue owns discovery, qualification, and the commercial proposal. A technical
specialist validates source access and complexity. Customer Success joins before
signature when onboarding requires metric workshops or multiple stakeholder teams.

## Motion measures

Track qualified discovery rate, data-fit completion, proposal conversion, days to
decision, and the share of closed customers whose recommended plan changed during
onboarding. A high change rate indicates weak qualification or routing.
