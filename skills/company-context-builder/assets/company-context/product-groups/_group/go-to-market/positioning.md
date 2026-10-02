---
kind: positioning
id: {{PRODUCT_GROUP_ID}}-positioning
scope: product-group:{{PRODUCT_GROUP_ID}}
strategy_ref: product-group-strategy:{{PRODUCT_GROUP_ID}}-strategy
segment_ref: segment:{{PRODUCT_GROUP_ID}}-core-segment
use_case_ref: use-case:{{PRODUCT_GROUP_ID}}-core-use-case
icp_ref: icp:{{PRODUCT_GROUP_ID}}-icp
persona_ref: personas:{{PRODUCT_GROUP_ID}}-personas
buying_context_ref: buying-context:{{PRODUCT_GROUP_ID}}-buying-context
product_refs: []
meta:
  source: inferred
  status: draft
  updated: {{UPDATED}}
  owner: Unknown
  last_verified: {{UPDATED}}
  verify_every: 90d
---

# {{PRODUCT_GROUP_NAME}} positioning

## Scope and desired perception

Define the segment, use case, offers, and perception this positioning governs.

## Market maturity and awareness

Summarize the category's maturity and the role-specific audience profile from
`segment:{{PRODUCT_GROUP_ID}}-core-segment`. Preserve the distinction between
knowing the category and using, evaluating, or planning to buy it. Keep unsupported
observations `unknown`; do not infer a comparison frame from either dimension.

## Anchors and category choice

- **Primary anchor:** Unknown use case, category, or current alternative.
- **Secondary organization anchor:** Unknown.
- **Secondary persona anchor:** Unknown.
- **Base category and modifier:** Unknown.
- **Category strategy and rationale:** Unknown.

## Problem linked to the primary anchor

State the problem and observable struggling moment in the chosen frame.

## Positioning statement

Write only after segment, audience, product truth, alternatives, and proof are
explicit. Do not start with a tagline.

## Buyer-perceived alternatives

| Alternative | Why the buyer values it | Limitation at the struggling moment | Positioning implication |
|---|---|---|---|
| Unknown | Unknown | Unknown | Unknown |

## Comparison frames

Select the primary comparison for each material role and situation from the
buyer-perceived alternatives above. Distinguish how the buyer works today from
what they would compare with this offer. A category-aware non-user may compare
vendors, the current workflow, or both; establish the frame from evidence.

| Role and situation | Primary comparison | When another frame applies | Evidence and source refs |
|---|---|---|---|
| Unknown | Unknown vendor, current workflow, other category, or no change | Unknown | Unknown; use approved typed refs |

## Differentiation chains

| Alternative weakness | Product truth | Capability | Direct benefit | Proof in context |
|---|---|---|---|---|
| Unknown | Unknown | Unknown | Unknown | Unknown |

Separate table stakes from specific, evidenced differentiation.

## Differentiation summary

Summarize the comparison mechanism without unsupported superlatives.

## Offer distinction

Route offers by evidenced use-case complexity and adoption scope, not budget alone.

## Claim and proof rules

| Claim | Required proof | Strength |
|---|---|---|
| Unknown | Unknown | Guaranteed, expected, or possible |

## Decision summary

Complete this compact review card after the argument is explicit. Select approved
facts from the sections above and their canonical upstream artifacts; keep typed
refs with the summary. Do not introduce a new audience, capability, or claim here.

| Decision | Approved selection and source refs |
|---|---|
| Audience and situation | Unknown; select from `segment:{{PRODUCT_GROUP_ID}}-core-segment` and `personas:{{PRODUCT_GROUP_ID}}-personas` |
| Category and rationale | Unknown; summarize the category choice above |
| Awareness and participation | Unknown; summarize the scoped segment profile |
| Primary comparison | Unknown; select the applicable comparison frame above |
| Alternative limitation | Unknown; select the limitation relevant to that comparison |
| Product mechanism and direct benefit | Unknown; select the differentiation chain and approved product refs |
| Proof and claim strength | Unknown; select the proof, assumptions, and applicable claim refs |

## Semantic review

Before confirmation, check the complete argument:

- The comparison frame fits the intended role and situation and has evidence.
- The stated limitation belongs to that alternative in the scoped use case.
- The differentiator addresses that limitation through an available product mechanism.
- The proof supports the direct benefit and the strength of the promise; assumptions
  behind higher-order outcomes remain explicit.
- Messaging selects the applicable comparison frame without changing these decisions.

Record consequential unknowns and leave affected arguments draft until resolved.
Schema checks and competency trace scoring do not establish semantic correctness.

## Message guardrails

- List claims, categories, comparisons, and outcomes that messaging must not invent.

## Review triggers

Define changes in buyer behavior, product truth, alternatives, or proof that require
positioning review.
