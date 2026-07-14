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
the GTM Ontology Framework. It models the strategic choices and durable facts that
explain where the company competes, who it serves, what it offers, and how those
choices become positioning, messaging, and go-to-market execution.

All companies, people, products, prices, market claims, and operating details in
this directory are synthetic. The example is authoritative only within its own
fictional scenario.

## How the context is organized

- `manifest.yaml` is the entry point and index of company-level artifacts and
  product-group manifests.
- `company/` contains facts that apply to every product group.
- `product-groups/<id>/` contains one market and offer context that may specialize
  the company strategy without silently contradicting it.
- Each product-group manifest indexes its strategy, segment, use cases, audience,
  products, positioning, value propositions, messaging, and GTM motions.
- Product-group ICP files are self-contained. Reading an ICP does not require
  loading personas, motions, positioning, or product documents.
- `ARTIFACT-GUIDE.md` defines how to create and maintain every artifact. It is an
  authoring reference, not runtime context for ordinary business tasks.

The intended dependency chain is:

```text
company strategy and constraints
-> product-group strategy
-> segment + use case + current alternative
-> ICP + buying roles + buying context
-> product truth: feature -> capability -> benefit
-> differentiation + positioning
-> value propositions
-> messaging by persona, awareness stage, and channel
-> GTM motions, handoffs, and measures
```

Later artifacts specialize earlier decisions. They do not redefine them. For
example, messaging selects from an approved positioning and value proposition; it
does not create a new ICP, product capability, or competitive claim.

## Core modeling rules

The core unit of a product-group market is a customer situation, not a list of
firmographics. It combines an organization type, a champion, a recurring workflow
or use case, the current way of doing that work, and the problem with that current
way. Split situations when their alternatives, problems, buying criteria, or route
to market differ materially.

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
when the canonical segment and use-case definitions live in separate artifacts.

Keep product truth separate from marketing interpretation:

- a **feature** is a concrete product mechanism;
- a **capability** is what that mechanism lets a user do;
- a **benefit** is the direct change produced by using the capability;
- **value** is why that benefit matters to a specific role and situation;
- a **business outcome** is a more distant result with additional dependencies.

Positioning records the comparison frame and strategic reason to choose the offer.
Value propositions connect a customer situation to product truth. Messaging selects
which approved arguments to use for one audience, awareness stage, asset, or channel.

## Building and maintaining the context

Build artifacts in dependency order: company strategy, product-group strategy,
segment, use cases, ICP, buying roles and context, product truth, positioning, value
propositions, messaging, then GTM motions. Draft strategic hypotheses explicitly;
do not make downstream artifacts appear confirmed while their prerequisites remain
uncertain.

Keep one group-level artifact while the group has one coherent customer situation.
Split personas, segments, positioning, or messaging into separate files only when
selective loading would prevent agents from mixing materially different contexts.

Use typed references such as `segment:commerce-analytics-core` and
`positioning:commerce-analytics-positioning` instead of file paths inside artifacts.
The manifests remain the path index.

Artifacts whose facts go stale (prices, market claims) carry `last_verified` and
`verify_every` in their frontmatter `meta` — the guard against silent degradation
of static context. In a real deployment the `meta` envelope follows the GOF
conventions (`docs/01-concepts.md` §3): corrections distilled from loop reviews
enter as `source: learned` with `evidence` pointing at the run. This synthetic
example keeps `source: synthetic` throughout on purpose.

For agent navigation rules, read `CLAUDE.md`. The context is not linked to the
ontology yet; that integration is intentionally outside this example's current
scope.
