# Research, evidence, and CRM protocol

Use this reference for source inventory, external research, conflict handling, and
Closed Won analysis. Keep raw evidence in its source system or temporary workspace;
only public-safe conclusions belong in `company-context/`.

## Contents

1. Source inventory
2. Research fallback order
3. Evidence and freshness
4. Normalization and conflicts
5. Closed Won cohort
6. Detailed Top 10 review
7. Privacy and persistence

## Source inventory

Inventory each source with:

| Field | Meaning |
|---|---|
| Source ID | Stable working identifier, never a CRM record ID in output |
| Type | User statement, file, URL, social profile, CRM, API, or export |
| Owner | Person or system responsible for the source |
| Retrieved | Timestamp and timezone |
| Coverage | Target artifacts and topics supported |
| Provenance | `declared`, `discovered`, `inferred`, or `learned` |
| Freshness | `last_verified` and proposed `verify_every` |
| Limitations | Missing fields, marketing bias, sample bias, or access limits |

Treat user-provided public collateral as `declared` because the user selected it as
business input; note when the collateral itself contains an unverified market claim.

## Research fallback order

1. Detect and use Exa MCP when available.
2. Use another research/search MCP with direct page retrieval.
3. Use web search plus browser/page opening.
4. Ask the user for URLs, exports, or copied content.
5. Record a gap when no evidence can be obtained.

Prefer primary sources for product, pricing, legal, and company claims. Use credible
independent sources for market and competitor interpretation. Open the source page;
do not treat a search snippet as final evidence.

For social media, prefer verified company accounts and named executive accounts
when the role is relevant. Separate current company policy from an individual's
opinion or an old campaign.

## Evidence and freshness

Attach evidence to claims that depend on research, CRM analysis, customer evidence,
or a review. Store public URLs directly. For private systems, use a safe evidence
description such as `CRM Closed Won aggregate, trailing 12 months, reviewed
YYYY-MM-DD`; do not store record identifiers or private links.

Suggested verification cadences:

- pricing and package availability: 30d;
- positioning, messaging, and competitor claims: 90d;
- company strategy and operating model: 180d;
- mission and durable company identity: 365d.

Use a shorter cadence when the source signals an active change. A fact past
`last_verified + verify_every` is overdue and must be rechecked or left as a warning.

Use the optional root claim registry only when evidence must be reviewed at a finer
grain than the containing artifact. Give each material claim one exact statement,
a typed scope, provenance, owner, supporting or contradicting evidence, and its own
freshness. Inferred claims state confidence. Keep ordinary durable facts in their
artifacts rather than expanding the registry without a review need.

## Normalization and conflicts

Classify normalization as:

- **lossless:** only headings, naming, ordering, or typed refs change;
- **interpretive:** source concepts are split, combined, or assigned new semantics;
- **lossy:** source information cannot be represented without omission.

Apply lossless normalization after showing the mapping. Require explicit approval
for interpretive or lossy normalization. Preserve the original nuance in evidence
or a gap when the target model cannot represent it.

Create a conflict whenever two sources cannot both be treated as true in the same
scope and time. Do not call different product-group ICPs a conflict. Present the
exact scope, dates, source strengths, business impact, and decision options. The
user decides; the agent may recommend.

If the conflict remains unresolved, preserve both claims and add reciprocal
`conflicts_with` refs. If a reviewed claim replaces an older statement, use
`supersedes` and retain the older claim for audit. Never treat a one-way conflict,
an expired claim, or a superseded statement as current truth.

## Closed Won cohort

Use the user's timezone and calculate a trailing 12-month interval ending at the
analysis timestamp. Filter on the CRM's actual won timestamp, not creation date or
current stage label alone. Include all agreed pipelines.

Before analysis, report:

- total records and counts by pipeline and currency;
- missingness for every proposed dimension;
- duplicate, test, cancelled, refunded, or corrected candidates;
- availability of comparable base-currency value;
- availability of notes, activities, transcripts, emails, and organization links.

Do not silently discard zero-value wins: they may represent pilots, renewals, or
data errors. Ask the user how to classify material anomalies.

Analyze distributions and recurring combinations for:

- product group and offer;
- customer situation, use case, and trigger;
- current alternative and problem;
- operational readiness and ownership evidence;
- industry, geography, employee or revenue band;
- acquisition source and sales owner;
- value and sales-cycle duration;
- buying roles, objections, selection criteria, and reason won.

Distinguish absence from lack of data. A blank CRM field is `unknown`, not evidence
that the criterion was absent. Report denominators and field coverage with every
pattern.

## Detailed Top 10 review

Rank by trusted base-currency value descending, then won timestamp descending. If
the CRM has no trusted converted value, stop and obtain an approved conversion
method. Never compare raw currency amounts.

Approval that an approximate ranking is acceptable does not authorize a conversion
method. Present and obtain explicit acceptance for the named rate source, rate date
(for example won date), non-business-day fallback, base currency, rounding, whether
existing CRM conversions will be preserved or recalculated, and any sensitivity
check near ranks 8–12. Do not silently mix CRM-provided base values with externally
converted values. Record the approved method and a `base_value_source` for every
multi-currency record before running the helper.

For each selected win, inspect evidence for:

1. organization and customer situation;
2. recurring workflow or category participation;
3. trigger and struggling moment;
4. previous or considered alternatives;
5. need intensity, ownership, and readiness;
6. buying committee and adoption owner;
7. objections, validation criteria, and proof requested;
8. product or package selected and stated reason won;
9. implementation or adoption evidence available at analysis time;
10. missing evidence and confidence.

Use the Top 10 as qualitative evidence, not as a statistically representative
sample. Compare its conclusions with the full cohort and label value-selection bias.

## Privacy and persistence

Never place the following in `company-context/`: customer or prospect names,
personal data, CRM IDs, private URLs, raw notes, transcripts, emails, activities,
exports, or record-level tables.

Persist only aggregate counts, anonymized patterns, safe evidence descriptions, and
user-approved durable conclusions. Delete temporary raw working files when the
execution environment permits safe cleanup; otherwise report their location and ask
the user to handle retention.
