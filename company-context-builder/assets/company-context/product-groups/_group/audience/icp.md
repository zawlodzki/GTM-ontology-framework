---
kind: icp
id: {{PRODUCT_GROUP_ID}}-icp
scope: product-group:{{PRODUCT_GROUP_ID}}
strategy_ref: product-group-strategy:{{PRODUCT_GROUP_ID}}-strategy
segment_ref: segment:{{PRODUCT_GROUP_ID}}-core-segment
use_case_ref: use-case:{{PRODUCT_GROUP_ID}}-core-use-case
meta:
  source: inferred
  status: draft
  updated: {{UPDATED}}
  owner: Unknown
  last_verified: {{UPDATED}}
  verify_every: 90d
---

# {{PRODUCT_GROUP_NAME}} ICP

This profile must remain self-contained. Use it to qualify an organization without
loading personas, buying context, positioning, motions, or product files.

## Market basis

State the primary job-to-be-done, use case, or established category. Describe
observable evidence that an organization participates in the market. Firmographic
similarity alone is not market participation.

## Canonical segment summary

Summarize `segment:{{PRODUCT_GROUP_ID}}-core-segment` and
`use-case:{{PRODUCT_GROUP_ID}}-core-use-case` so the ICP works independently.

## Qualification criteria

A strong fit requires all market-and-need and operational-readiness criteria to be
true. Need-intensity and firmographic criteria only prioritize qualified companies.

### Market and need fit — required

- Unknown recurring workflow or category participation.
- Unknown limitation, failure, or cost in the current alternative.
- Unknown owned decision, desired progress, or use-case outcome.

### Operational readiness — required

- Unknown accountable workflow and adoption owner.
- Unknown delivery, implementation, legal, or product prerequisites.
- Unknown access to the inputs required by the use case.

### Need-intensity signals

- Unknown.

### Firmographic priority

- Unknown. Confirm need first and state why each range improves priority.

## Data or delivery readiness

Record the minimum inputs, access, capacity, ownership, and compliance required.

## Disqualifiers

List evidence that makes the organization unqualified now. Keep unknown criteria
as unknown rather than treating them as either fit or disqualification.

## Quick qualification check

Confirm market participation and need, then ownership and operational readiness,
then disqualifiers, and only then firmographic priority. Record each required
criterion as `true`, `false`, or `unknown`. Any `false` means not currently
qualified; any `unknown` means incomplete.
