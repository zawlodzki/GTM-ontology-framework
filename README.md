# CRM Ontology agent skill for Pipedrive, HubSpot, Attio, Salesforce

Make your CRM understandable for AI agents.

A schema export tells an agent that a dropdown called `lifecycle_stage` exists with
values Lead / MQL / SQL. It doesn't tell it when a lead actually becomes an SQL, which
n8n workflow writes the AI summary field and from what prompt, or that moving a deal to
"Demo" fires an automation that creates a task. That knowledge sits in people's heads
and breaks the moment an agent starts writing to your CRM.

This repo is a method for writing it down once, in a form that works for three
audiences at the same time: your sales team and leadership (rendered tables and
funnel diagrams, no YAML), AI agents (small, indexed YAML artifacts), and the CRM
API (field keys, enum maps, stage ids). If you run a CRM as an admin or own the
sales process, this is for you.

## What's inside

| Folder | What it is |
|---|---|
| `skill/` | The **gtm-ontology-builder** skill. Install it in Claude, say "map my CRM" and it interviews you, introspects the CRM through MCP or API, and builds the ontology folder with you. |
| `plugin/` | The same skill packaged as a Claude Code plugin, installable from this repo's marketplace (see [Install](#install)). |
| `plugins/gtm-ontology-builder/` | The skill packaged as a Codex plugin. |
| `.agents/plugins/marketplace.json` | The Codex marketplace manifest for installing and sharing the plugin directly from this repo. |
| `gtm-ontology/` | A complete, validated example: fictional B2B SaaS on Pipedrive. Pipeline with entry/exit criteria, AI-filled fields with their prompt, 3 automations with data fingerprints, agent actions, KPIs. This is exactly what the skill produces. |
| `docs/` | The method: 4 layers, a 7-phase process with interview question banks, a format spec for every artifact, CRM type mappings, extension and anti-pattern notes. |
| `schemas/` | JSON Schema for each artifact type: validate everything, trust nothing. |
| `templates/` | Commented starter files. |
| `tools/render_ontology.py` | One command: ontology → readable process table, Mermaid funnel, field dictionary, action catalog, interactive `explorer.html`. |
| `tools/lint_ontology.py` | One command: health report. Schema validation, reference resolution, orphans, stale facts (`last_verified`), pii rules, loop/ladder consistency. The care-mode workhorse. |

## How it works

Four layers. **Semantic** is what exists in the business: objects, fields with meaning,
conditions behind every dropdown value. **Binding** is where the data physically lives:
systems, field-key mappings, cross-system identity. **Dynamic** is what happens: pipelines
as state machines, existing automations with fingerprints so agents can tell who wrote
a value, and action contracts defining what an agent may do, in what order, with what
approvals — grouped into loops, each with a human steward. **Measurement & governance**
is KPIs defined in ontology terms, a permission ladder for agents (read-only →
approve-each-write → autonomous-with-log, promotion earned per loop), and hard limits.

Everything the system can't tell you gets collected in a structured interview. Every
statement carries its provenance (`discovered` / `inferred` / `declared` / `learned`)
and a status: agents never act on drafts.

## Install

As a **Codex plugin**:

```sh
codex plugin marketplace add zawlodzki/GTM-ontology-framework
codex plugin add gtm-ontology-builder@personal
```

Start a new Codex task after installation so it picks up the plugin and its skill.

As a **Claude Code plugin**:

```
/plugin marketplace add zawlodzki/GTM-ontology-framework
/plugin install gtm-ontology-builder@gtm-ontology-framework
```

As a **standalone skill**: grab `gtm-ontology-builder.skill` from this repo and add it
to Claude (Cowork or Claude Code), or copy `skill/` into your skills folder.

Either way the skill is self-contained — it bundles the renderer, JSON schemas, and the
complete worked example.

## Quickstart

1. Install the skill or plugin (see [Install](#install)).
2. Connect your CRM. An MCP server is best, an API token works too. Salesforce works
   as well; for platform CRMs (Salesforce, HubSpot) the skill scopes itself to the CRM
   module: Sales Cloud objects, not the whole platform.
3. Say: *"Build an ontology of my CRM."* The skill runs the phases, asks before it
   writes, and ends with a `gtm-ontology/` folder in your repo plus an entry in your
   root `CLAUDE.md` so every future agent knows where to look.

Before running anything, open `gtm-ontology/render/explorer.html` from the example:
funnel, business logic per stage, actions, automations and the reference graph, all
in one file. That's the end state you're building toward.

## Why this exists

I implement CRMs for a living. On every project the same process knowledge had to be
written three times: a table for the sales team, context for AI agents, configuration
for the API. Three copies, three places to drift apart. This framework keeps one source
of truth in YAML and renders the rest. The example in `gtm-ontology/` is small on
purpose: read it in ten minutes, then decide if the method fits your stack.

## License

MIT. Use it, change it, ship it; just keep the copyright notice.

## Work with me

Want to talk about AI in B2B sales, or about implementing and optimizing a CRM?
grzesiek@zawlodzki.pl · [zawlodzki.pl](https://zawlodzki.pl)
