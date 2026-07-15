---
kind: company-context-agent-guide
id: company-context-agent-guide
scope: company-context
meta:
  source: declared
  status: confirmed
  updated: {{UPDATED}}
---

# Company context: agent guide

This directory contains the static company context for {{COMPANY_NAME}}. It
describes durable business facts, audiences, go-to-market choices, and product
offers. It does not contain live customer, prospect, CRM, or operational data.

## Navigation

1. Read `manifest.yaml` first.
2. Load a company artifact only when its `load_when` matches the task.
3. For product-group work, follow the group manifest named in `product_groups`.
4. Within a group, load only the artifact whose `load_when` matches the task.
5. Load `ARTIFACT-GUIDE.md` only when authoring or structurally reviewing context.
6. Load `GAPS.md` only when reviewing completeness or planning further discovery.

Never merge product-group ICPs. Follow typed references through manifests instead
of guessing paths. A typed reference selects the canonical upstream decision;
repeated prose must not silently diverge from it.

## Ontology linkage

The GTM ontology in a sibling `gtm-ontology/` tree may point here through
`context_root` in its manifest; this tree never links back. Ontology processes
reference `product-group:<group-id>` and `gtm-motion:<motion-id>`, where motion
ids come from the `motions:` list in each group's `go-to-market/motions.md`
frontmatter. Group and motion ids are therefore cross-tree identifiers. Renaming
one is a breaking change: search both trees and generated renders first, then run
the GOF linter, which follows `context_root` and validates both trees together.

## Interpretation rules

- Company artifacts contain only facts shared by all product groups.
- Group artifacts may specialize company facts but must not silently contradict them.
- Follow the dependency order: strategy -> segment/use case -> audience -> product
  truth -> positioning -> value proposition -> messaging -> motion.
- Define a segment from organization context, champion, recurring workflow,
  current alternative, and problem. Use firmographics only to narrow or prioritize.
- Keep each ICP self-contained. Confirm market participation, need, ownership, and
  readiness before applying disqualifiers and firmographic priority.
- Record unknown criteria as unknown. Never infer need from industry, size,
  funding, reputation, technology, team, or title.
- Keep feature, capability, benefit, value, and business outcome distinct.
- Treat personas as buying and adoption roles, not demographic profiles.
- Treat internal work, spreadsheets, services, other categories, vendors, and no
  change as possible current alternatives.
- No artifact authorizes an external action or system write.
- Missing context means report the gap and ask; never invent a fact.
- No personal data belongs here. Read live CRM data through governed ontology
  bindings when a task requires it.
- Re-verify facts that are past `last_verified + verify_every` before relying on them.
