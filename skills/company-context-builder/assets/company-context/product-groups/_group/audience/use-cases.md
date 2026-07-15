---
kind: use-case
id: {{PRODUCT_GROUP_ID}}-core-use-case
scope: product-group:{{PRODUCT_GROUP_ID}}
strategy_ref: product-group-strategy:{{PRODUCT_GROUP_ID}}-strategy
segment_ref: segment:{{PRODUCT_GROUP_ID}}-core-segment
persona_ref: personas:{{PRODUCT_GROUP_ID}}-personas
product_refs: []
meta:
  source: inferred
  status: draft
  updated: {{UPDATED}}
  owner: Unknown
  last_verified: {{UPDATED}}
  verify_every: 90d
---

# {{PRODUCT_GROUP_NAME}} primary use case

## Functional activity

Describe the recurring activity an actor performs and the progress sought. Do not
use a feature, connector, or distant business result as the use case.

## Actor and context

- **Primary actor:** Unknown.
- **Participants:** Unknown.
- **Trigger:** Unknown.
- **Frequency:** Unknown.

## Inputs

List the information, materials, systems, ownership, and preconditions required.

## Workflow

Describe the ordered activity independently of any one product implementation.

## Current method

Describe how the work is performed today and why that method remains valid.

## Friction

Record evidenced failure, cost, delay, risk, or capacity constraints in the current
method.

## Desired output

Define the direct output of successful work and separate it from downstream value.

## Success evidence

List observable evidence that the workflow improved within the agreed scope.

## Boundaries

State adjacent jobs, unsupported outcomes, and conditions that require another
product group or an explicit gap.
