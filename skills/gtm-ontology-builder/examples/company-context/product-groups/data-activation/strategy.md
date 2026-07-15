---
kind: product-group-strategy
id: data-activation-strategy
scope: product-group:data-activation
company_strategy_ref: company-strategy:company-strategy
primary_segment_ref: segment:data-activation-core-segment
primary_use_case_ref: use-case:data-activation-core-use-case
primary_icp_ref: icp:data-activation-icp
meta:
  source: synthetic
  status: example
  updated: 2026-07-15
  owner: Product
  last_verified: 2026-07-15
  verify_every: 180d
---

# Data Activation strategy

## Strategic role

Data Activation is Acme Analytics' selective expansion for commerce organizations
whose warehouse models are already authoritative but whose approved customer data
is difficult to deliver safely and repeatedly into operational systems.

The group complements Commerce Analytics. It does not serve organizations that
primarily need reporting, warehouse construction, identity creation, consent-system
replacement, campaign execution, or real-time event streaming.

## GTM phase

**Current phase:** experimentation.

The group has defined offers and a plausible joint technical-business segment, but
production fit must be validated through bounded pilots. Sandbox activity tests
technical comprehension; it does not prove market need, organizational readiness,
or purchase intent.

The immediate objective is repeatability: determine whether the same segment,
ownership model, use-case family, product truth, production-readiness review, and
pilot acceptance criteria hold across qualified customers.

## Primary market

- **Segment:** `segment:data-activation-core-segment`.
- **Primary use case:** `use-case:data-activation-core-use-case`.
- **Technical sponsor:** Head of Data or equivalent warehouse and governance owner.
- **Business champion:** Lifecycle Marketing Lead or another owner of the downstream
  operational use case.
- **Primary current ways:** destination-specific scripts, manual exports, native
  connectors, and broad customer-data platforms.

Both technical and business ownership are required. A warehouse or technology
signal alone does not establish the workflow, problem, or readiness.

## Offer architecture

- **Warehouse Sync** supports repeatable delivery of approved modeled attributes or
  records through observable and recoverable batch syncs.
- **Audience Activation** supports controlled creation, review, and publishing of
  audiences from administrator-approved warehouse data.

The offers share the warehouse-to-destination workflow, identity and governance
constraints, and production-readiness path. They remain distinct variants because
their primary actor, operating step, destination behavior, and acceptance evidence
differ. Recommend both only when two separately owned use cases are confirmed.

## Primary motion

The motion combines product-led technical discovery with sales-assisted production
adoption. Documentation and a synthetic-data sandbox help technical evaluators
understand mappings and delivery behavior. Production access requires ICP
qualification, joint ownership, security review, a bounded pilot, and commercial scope.

Audience Activation is more sales-assisted because its production workflow requires
agreement between the Lifecycle Marketing owner and the Head of Data. Warehouse Sync
may begin with a technical evaluator but still needs a named downstream use-case owner.

## Constraints

- The warehouse and approved modeled layer remain authoritative.
- The customer owns identity quality, consent, suppression, deletion rules, access,
  permitted use, destination configuration, and the downstream business decision.
- No unsupervised production activation from a sandbox or product-led signup.
- No claim of perfect identity, instant delivery, error-free destinations, or
  elimination of technical ownership.
- No sub-second streaming, unlimited connectors, hidden custom modeling, or campaign
  execution inside the standard offers.
- A connector request is an implementation detail, not a qualified use case.

## Measures and gates

Review qualified readiness-review rate, pilot acceptance, time to security approval,
production activation, failure recovery evidence, and 90-day use-case adoption.

Advance from experimentation when the same workflow and ownership model repeatedly
produce accepted pilots without unpriced custom engineering. Revisit or split the
group if Warehouse Sync and Audience Activation consistently require different
segments, buying journeys, channels, or production governance rather than two
variants of one use-case family.
