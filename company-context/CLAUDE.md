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

## Interpretation rules

- Company artifacts contain only facts shared by all product groups.
- Group artifacts may specialize company facts but must not silently contradict
  them.
- An ICP file must be self-contained and must state qualification criteria and
  disqualifiers directly.
- This is a synthetic example. Treat its artifacts as canonical only within the
  Acme Analytics scenario and never as claims about a real business.
- No artifact in this directory authorizes an external action or a system write.
