---
kind: company-context-artifact-guide
id: company-context-artifact-guide
scope: company-context
meta:
  source: synthetic
  status: example
  updated: 2026-07-14
---

# Company-context artifact guide

Use this guide when creating, changing, or reviewing company-context artifacts.
For ordinary business questions, start with `manifest.yaml` and load only the
runtime artifacts selected by `load_when`.

## Composition model

Company context is a dependency graph of strategic choices and durable facts:

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

An artifact may summarize an upstream decision for readability, but the typed
reference identifies the canonical source. Downstream artifacts specialize earlier
choices; they do not redefine them.

## Common envelope

Markdown artifacts use YAML frontmatter with:

- `kind`: artifact type;
- `id`: unique stable identifier;
- `scope`: `company` or `product-group:<id>`;
- typed references required by the artifact contract;
- `meta.source`: `declared`, `discovered`, `inferred`, `learned`, or `synthetic`;
- `meta.status`: use the status conventions of the containing repository;
- `meta.updated`;
- `meta.owner` when a business owner exists;
- `meta.last_verified` and `meta.verify_every` for facts that age;
- `meta.evidence` when a claim depends on research, customer evidence, or a review.

Use typed references such as `segment:commerce-analytics-core`, never file paths.
Manifests map artifact IDs to paths and supply `summary` and `load_when`.

## Company strategy

Record the choices shared by all product groups:

- mission and company boundaries;
- target-market choices and exclusions;
- portfolio and offer architecture;
- current GTM phase;
- planning horizon and material resource constraints;
- strategic choices and company-level narrative boundaries;
- shared capabilities or principles, with evidence where they are claims;
- triggers for expansion, contraction, or review.

Company narrative is not a substitute for product-group positioning. It constrains
what group positioning may claim without forcing different groups into one message.

## Product-group strategy

Define why the group exists as a separate strategic unit:

- inherited company choices;
- primary segment and adjacent segments;
- primary use case and champion;
- current GTM phase: experimentation, beachhead, or expansion;
- offers and the logic that separates them;
- primary motion, capacity constraints, and decision horizon;
- success, expansion, and stop criteria.

Create a separate group only when the customer situation, buying process, product
truth, or route to market differs materially. Packaging differences alone do not
create a new market.

## Segment

A segment is a shared customer situation. Capture:

- market basis: use case, established category, or both;
- organization context and firmographic priority;
- champion or team closest to the problem;
- recurring workflow and desired progress;
- current alternative, including manual work or doing nothing;
- limitation, problem, and observable struggling moment;
- market maturity and starting awareness state;
- common buying criteria and behavior;
- observable signals, qualification boundaries, and disqualifiers;
- reachable channels or communities;
- priority and relationship to adjacent segments;
- owner, evidence, assumptions, and freshness.

Start with the workflow or category. Apply industry, geography, revenue, headcount,
technology, and role filters only after the customer situation is coherent. Split
segments when alternatives, problems, criteria, or buying behavior diverge enough
to require different positioning or motions.

## Use case

Keep job, use case, capability, and outcome distinct:

- a job describes context and desired progress;
- a use case is a functional activity or workflow;
- a capability is what the product lets a user do;
- an outcome is the result of successful work.

For each use case record the actor or team, trigger, activity, inputs, outputs,
frequency, current method, friction, desired outcome, success evidence, and links
to segments, personas, products, and capabilities. "Increase revenue" is not a use
case; neither is a feature or connector name.

## ICP

An ICP qualifies organizations inside a defined market; it does not create the
market from firmographics. Keep it self-contained and include:

- `segment_ref` and concise market basis;
- observable evidence of market participation;
- required workflow, need, ownership, and operational-readiness criteria;
- need-intensity signals;
- firmographic priority after need is established;
- data or delivery readiness where relevant;
- disqualifiers;
- qualification order and `true` / `false` / `unknown` handling.

Unknown does not mean fit. Job titles, technologies, funding, reputation, industry,
or company size do not prove need by themselves.

## Personas and buying roles

Model roles in a defined buying and adoption situation, not demographics. Capture:

- segment and use-case references;
- role aliases and responsibilities;
- buying-role tags: user, champion, economic buyer, sponsor, validator, blocker,
  procurement, or adoption owner;
- proximity to the problem and influence or veto rights;
- goals, direct product outcome, and translated business outcome;
- triggers, concerns, objections, and evaluation criteria;
- evidence expected and implementation concerns;
- journey stages where the role participates;
- relationships with other roles;
- language and trusted channels when known.

Market primarily to the role closest to the problem and able to champion change.
Adapt the value horizon for other stakeholders instead of forcing one generic value
proposition across the committee.

## Buying context

Record why and how a purchase starts and progresses:

- persistent problems and buying triggers;
- current alternatives and switching inertia;
- committee, decision ownership, and adoption ownership;
- evaluation criteria and proof expected;
- blockers, risks, security, legal, procurement, or pilot requirements;
- awareness journey from outcome or problem awareness through use-case, category,
  product, validation, decision, and adoption stages.

For each material stage capture the customer's question, involved roles, required
evidence, suitable message or asset, call to action, and exit signal. A homepage,
demo request, signup, or product event is not the entire buying journey or proof of
organizational fit.

## Product and offer

Store product truth separately from positioning. Record:

- audience, segment, use-case, strategy, positioning, and motion references;
- primary and secondary use cases;
- features with availability: live, beta, or planned;
- capabilities phrased as user actions;
- the feature that enables each capability;
- conditions, limitations, dependencies, and exclusions;
- direct functional benefits;
- higher-order outcomes as hypotheses with explicit assumptions;
- package limits, pricing, and included services as separate concepts;
- table-stakes versus distinctive capabilities;
- proof or acceptance evidence and claim guardrails.

Do not place roadmap capabilities under a live offer without marking availability.
Do not combine feature, capability, service, and package limit in one undifferentiated
list.

## Positioning

Positioning records how one offer should be understood by a defined segment. Include:

- strategy, segment, ICP, persona, use-case, product, and buying-context references;
- scope level: broad market, segment, or offer;
- market maturity and audience awareness;
- primary anchor: category, use case, or current alternative;
- secondary anchors: organization type or persona that add context;
- category choice and rationale;
- buyer-perceived current alternatives;
- problem and struggling moment linked to the primary anchor;
- differentiation chains from alternative weakness through capability and feature
  to direct benefit;
- table stakes versus distinctive claims;
- desired perception, proof references, and message guardrails.

Build positioning only after the market, audience, and product truth are explicit.
Do not start with a tagline. Claims such as "easy to use", "AI-powered", "platform",
or distant revenue outcomes are not differentiation without a specific comparison,
mechanism, and evidence.

## Value proposition

A value proposition is a traceable argument for one role and use case:

```text
segment + persona + use case
-> current alternative
-> limitation or problem
-> product feature
-> capability
-> direct benefit
-> value for the role
-> proof and assumptions
```

Record first-order benefits separately from second-order or business outcomes.
State claim strength as guaranteed, expected, or possible. Do not invent personal
motives or imply that software alone controls a result with external dependencies.

## Messaging

Messaging selects approved positioning and value propositions for one context.
For each brief or matrix row capture:

- positioning, product, segment, persona, and use-case references;
- asset type and channel;
- awareness stage and primary customer question;
- message objective and core argument;
- selected problem, capability, feature, benefit, proof, and competitive frame;
- narrative outline and call to action;
- `must_say` and `must_not_say` guardrails;
- owner, approver, review date, and learning evidence.

Homepage, product page, sales conversation, campaign, and onboarding need different
selections from the same strategy. A copy edit does not authorize a positioning
change, and messaging feedback must not silently change product truth.

## GTM motion

Connect strategy to repeatable execution:

- GTM phase and segment, ICP, use-case, persona, offer, positioning, and messaging refs;
- sales-led, product-led, sales-assisted, or partner model;
- entry awareness, triggers, offer, and call to action;
- primary channel and the reason it fits the segment;
- education, demand creation, and demand capture path;
- qualification, routing, handoffs, activation, and adoption;
- team capacity and service constraints;
- metrics, review cadence, and repeatability or expansion gates.

Choose one primary segment, motion, and channel while establishing repeatability.
Expansion is a separate GTM program, not an automatic consequence of adding more
channels or broadening the ICP.

## Build and review sequence

1. Confirm company strategy, portfolio boundaries, and constraints.
2. Define the product-group strategy and primary customer situation.
3. Record the segment, use cases, current alternatives, and market maturity.
4. Build the self-contained ICP and buying roles.
5. Map buying context, journey, evidence, and blockers.
6. Record product truth and offer boundaries.
7. Choose category and write differentiation chains.
8. Write positioning and value propositions.
9. Build messaging briefs by persona, awareness stage, asset, and channel.
10. Define the GTM motion, handoffs, measures, and expansion gates.
11. Validate references, manifest completeness, evidence, freshness, and conflicts.

Review downstream artifacts whenever an upstream decision changes. Do not mark a
downstream artifact more certain than the market, product, or evidence it depends on.
