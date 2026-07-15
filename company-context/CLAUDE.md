---
kind: company-context-agent-guide
id: company-context-agent-guide
scope: company-context
meta:
  source: synthetic
  status: example
  updated: 2026-07-14
---

# Company context: agent guide

This directory contains the fictional static company context for Acme Analytics.
It describes durable business facts, audiences, go-to-market choices, and product
offers. It does not contain live customer, prospect, CRM, or operational data.

## Navigation

1. Read `manifest.yaml` first.
2. Load a company artifact only when its `load_when` matches the task.
3. For product-group work, follow the group manifest named in `product_groups`.
4. Within a group, load only the artifact whose `load_when` matches the task.
5. Load `ARTIFACT-GUIDE.md` only when creating, changing, or reviewing the
   structure of company-context artifacts.

For example, to answer a question about a group's ICP, read only:

```text
manifest.yaml
-> product-groups/<group>/manifest.yaml
-> product-groups/<group>/audience/icp.md
```

Do not load personas, buying context, motions, positioning, or products unless
the task needs them. If a request says "the ICP" without identifying a product
group, use the root manifest to identify the relevant group; do not merge group
ICPs into a fictional company-wide profile.

Follow typed references through manifests, never by guessing a path. A reference
selects a canonical upstream decision; repeated prose is only a local summary and
must not silently diverge from the referenced artifact.

## Ontology linkage

The GTM ontology (sibling `gtm-ontology/` tree) points here through
`context_root` in its `manifest.yaml`; this tree never links back. Ontology
processes reference `product-group:<group-id>` and `gtm-motion:<motion-id>`,
where motion ids come from the `motions:` list in each group's
`go-to-market/motions.md` frontmatter. Group and motion ids are therefore
cross-tree identifiers: renaming one is a breaking change — search both trees
(and any renders) before touching it, then re-run the GOF linter, which
follows `context_root` and validates both trees in one run.

## Interpretation rules

- Company artifacts contain only facts shared by all product groups.
- Group artifacts may specialize company facts but must not silently contradict
  them.
- Treat the dependency order as binding: strategy -> segment/use case -> audience
  -> product truth -> positioning -> value proposition -> messaging -> motion.
- A segment is a shared customer situation: organization type, champion, workflow,
  current alternative, and problem. Firmographics only narrow or prioritize it.
- An ICP file must be self-contained. It begins with its job-to-be-done or category
  market basis, then states qualification criteria and disqualifiers directly.
- Qualify in this order: confirm market participation and need, confirm ownership
  and operational readiness, check disqualifiers, then use firmographics to rank
  or narrow the already-qualified market.
- Firmographics, team names, and job titles never establish need by themselves.
  Treat them as prioritization filters unless an explicit delivery, legal, or
  product constraint makes one a hard boundary.
- Record unknown market-need or readiness criteria as unknown. Do not infer them
  from company size, industry, funding, reputation, technology, team, or role.
- Keep feature, capability, benefit, value, and business outcome distinct. Never
  turn an unverified downstream outcome into a product fact.
- Positioning defines the comparison frame and strategic argument. Messaging may
  select and adapt approved arguments for an audience or channel, but it must not
  invent a new segment, capability, differentiator, or proof point.
- A persona is a buying or adoption role in a defined situation, not a demographic
  profile. Distinguish user, champion, economic buyer, validator, blocker, and
  adoption owner where those roles differ.
- Current alternatives include internal processes, spreadsheets, services, other
  categories, vendors, and doing nothing. Use the buyer's perceived alternative,
  not only the seller's competitor list.
- This is a synthetic example. Treat its artifacts as canonical only within the
  Acme Analytics scenario and never as claims about a real business.
- No artifact in this directory authorizes an external action or a system write.
- Missing context = say so and ask. When these files do not answer a question,
  report the gap; never invent a fact to fill it.
- No personal data lives here. Personas are role archetypes, not people. Names,
  emails, and other pii stay in the source systems (properties marked `pii: true`
  in the ontology) and are read live through the ontology's bindings.
- Facts age. Artifacts carry `last_verified` and `verify_every` in `meta`; a fact
  past `last_verified + verify_every` is overdue — re-verify it with its owner
  before relying on it. Prices and market claims expire fastest.
