---
kind: product-context
id: {{PRODUCT_ID}}
scope: product-group:{{PRODUCT_GROUP_ID}}
product_group: {{PRODUCT_GROUP_ID}}
strategy_ref: product-group-strategy:{{PRODUCT_GROUP_ID}}-strategy
segment_ref: segment:{{PRODUCT_GROUP_ID}}-core-segment
use_case_ref: use-case:{{PRODUCT_GROUP_ID}}-core-use-case
audience_refs:
  - icp:{{PRODUCT_GROUP_ID}}-icp
  - personas:{{PRODUCT_GROUP_ID}}-personas
buying_context_ref: buying-context:{{PRODUCT_GROUP_ID}}-buying-context
positioning_ref: positioning:{{PRODUCT_GROUP_ID}}-positioning
gtm_motion_refs: []
meta:
  source: declared
  status: draft
  updated: {{UPDATED}}
  owner: Unknown
  last_verified: {{UPDATED}}
  verify_every: 90d
---

# {{PRODUCT_NAME}}

## Intended audience

State the linked ICP, primary persona, customer situation, and adoption owner.

## Primary use case

Describe the scope in which this offer supports the canonical use case. Packaging
does not create a separate market by itself.

## Problem

State the evidenced limitation in the current alternative that the offer addresses.

## Product role

Describe the offer's bounded role without positioning language or distant outcomes.

## Features and availability

| Feature | Availability | Conditions and limits |
|---|---|---|
| Unknown | Live, beta, or planned | Unknown |

## Capability chains

| Current problem | Enabling feature | User capability | First-order benefit | Role in differentiation |
|---|---|---|---|---|
| Unknown | Unknown | Unknown | Unknown | Table stakes or distinctive with evidence |

## Package limits

- Unknown.

## Included services

- Unknown. Keep services separate from software features.

## Direct benefits and outcome hypotheses

Separate direct functional benefits from customer-controlled or externally
dependent outcomes. State assumptions and claim strength.

## Exclusions

- Unknown unsupported features, services, sources, usage, or outcomes.

## Packaging and pricing assumptions

Record price, currency, tax treatment, contract, usage, and validity date. Do not
copy historical deal terms as current policy.

## Dependencies

List customer inputs, access, ownership, implementation, legal, and adoption needs.

## Relevant GTM motion

Add one or more confirmed `gtm-motion:<id>` references, then explain when each
motion should recommend this offer and what evidence is required before routing.
