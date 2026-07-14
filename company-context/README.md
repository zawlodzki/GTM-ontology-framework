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

Artifacts whose facts go stale (prices, market claims) carry `last_verified` and
`verify_every` in their frontmatter `meta` — the guard against silent degradation
of static context. In a real deployment the `meta` envelope follows the GOF
conventions (`docs/01-concepts.md` §3): corrections distilled from loop reviews
enter as `source: learned` with `evidence` pointing at the run. This synthetic
example keeps `source: synthetic` throughout on purpose.

For agent navigation rules, read `CLAUDE.md`. The context is not linked to the
ontology yet; that integration is intentionally outside this example's current
scope.
