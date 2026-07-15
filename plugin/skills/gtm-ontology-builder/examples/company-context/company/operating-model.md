---
kind: operating-model
id: company-operating-model
scope: company
meta:
  source: synthetic
  status: example
  updated: 2026-07-14
---

# Operating model

## Functional ownership

| Function | Company-wide responsibility |
|---|---|
| Product | Portfolio direction, packaging, roadmap, and product-group definitions |
| Engineering | Platform reliability, integrations, security, and technical delivery |
| Revenue | Demand generation, qualification, sales, partnerships, and commercial terms |
| Customer Success | Onboarding, adoption, renewals, and escalation coordination |
| Data Governance | Metric definitions, data quality standards, and access controls |
| Finance | Billing, revenue policy, discount controls, and contract administration |

Individual product-group artifacts may name a primary commercial or delivery role,
but they must not redefine these company-wide ownership boundaries.

## Customer delivery model

1. Revenue confirms the relevant product group and commercial fit.
2. A technical fit review confirms data sources, access, scale, and dependencies.
3. Customer Success owns onboarding and coordinates required engineering work.
4. The customer validates metric definitions and data quality before production use.
5. Customer Success owns adoption and renewal; Engineering owns technical incidents.

## Support model

Standard support is remote and delivered during European business hours. Product
plans may define response targets or named success coverage. Security incidents
follow the incident process and are never handled as routine support requests.

## Operating boundaries

Acme Analytics employees may guide configuration and data interpretation, but the
customer remains responsible for source-system accuracy, lawful data collection,
access authorization, and business decisions based on the outputs.
