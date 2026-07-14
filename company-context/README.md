---
kind: company-context-readme
id: company-context-readme
scope: company-context
meta:
  source: synthetic
  status: example
  updated: 2026-07-14
---

# Acme Analytics company context

This directory is a fictional, public-safe example of static company context for
the GTM Ontology Framework. It separates company-wide facts from product-group
audiences, go-to-market choices, and product information so agents can load only
the context required for a task.

All companies, people, products, prices, market claims, and operating details in
this directory are synthetic. The example is authoritative only within its own
fictional scenario.

## How the context is organized

- `manifest.yaml` is the entry point and index of company-level artifacts and
  product-group manifests.
- `company/` contains facts that apply to every product group.
- `product-groups/<id>/manifest.yaml` indexes the audience, go-to-market, and
  product artifacts for one group.
- Product-group ICP files are self-contained. Reading an ICP does not require
  loading personas, motions, positioning, or product documents.

## ICP construction method

Define the market before narrowing it to an ideal customer profile:

1. Start with a job-to-be-done or a product category: the workflow a team already
   performs, or the category it buys, evaluates, or replaces.
2. State observable evidence that an organization participates in that market.
3. Apply need, ownership, and operational-readiness criteria to identify viable fit.
4. Use firmographics such as revenue, headcount, industry, and geography to narrow
   or prioritize that market only after need is established.
5. Use personas to describe the people involved in buying and adoption, not to
   substitute a job title for organizational need.

Firmographics never establish need by themselves. A company does not qualify only
because it matches a size, region, industry, business-model, team, or role filter.
Because ICP files are self-contained, each one includes a concise market basis even
when fuller jobs-to-be-done and category positioning live in separate artifacts.

Artifacts whose facts go stale (prices, market claims) carry `last_verified` and
`verify_every` in their frontmatter `meta` — the guard against silent degradation
of static context. In a real deployment the `meta` envelope follows the GOF
conventions (`docs/01-concepts.md` §3): corrections distilled from loop reviews
enter as `source: learned` with `evidence` pointing at the run. This synthetic
example keeps `source: synthetic` throughout on purpose.

For agent navigation rules, read `CLAUDE.md`. The context is not linked to the
ontology yet; that integration is intentionally outside this example's current
scope.
