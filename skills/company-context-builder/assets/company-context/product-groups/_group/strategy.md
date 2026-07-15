---
kind: product-group-strategy
id: {{PRODUCT_GROUP_ID}}-strategy
scope: product-group:{{PRODUCT_GROUP_ID}}
company_strategy_ref: company-strategy:company-strategy
primary_segment_ref: segment:{{PRODUCT_GROUP_ID}}-core-segment
primary_use_case_ref: use-case:{{PRODUCT_GROUP_ID}}-core-use-case
primary_icp_ref: icp:{{PRODUCT_GROUP_ID}}-icp
meta:
  source: inferred
  status: draft
  updated: {{UPDATED}}
  owner: Unknown
  last_verified: {{UPDATED}}
  verify_every: 180d
---

# {{PRODUCT_GROUP_NAME}} strategy

## Strategic role

Explain why this group exists as a separate strategic unit and how it specializes
company strategy around one coherent customer situation.

## GTM phase

State whether the group is in experimentation, beachhead, or expansion. Define what
that phase authorizes and what would require a new strategy decision.

## Primary market

- **Segment:** `segment:{{PRODUCT_GROUP_ID}}-core-segment`.
- **Primary use case:** `use-case:{{PRODUCT_GROUP_ID}}-core-use-case`.
- **Typical champion:** Unknown.
- **Economic buyer:** Unknown.
- **Primary current alternatives:** Unknown.

Qualify through workflow need, ownership, and readiness before firmographics.

## Offer architecture

Describe approved offers and the complexity, adoption scope, service, or product
truth that separates them. Packaging differences alone do not create a new market.

## Primary motion

Choose one primary route to market and explain why it matches the segment's buying
behavior, awareness, and the company's capacity.

## Constraints

Record delivery, product, channel, evidence, and claim boundaries.

## Measures and gates

Define success, repeatability, expansion, review, and stop criteria for the current
decision horizon.
