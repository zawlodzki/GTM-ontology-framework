# gtm-ontology-builder (Claude Code plugin)

The `gtm-ontology-builder` skill packaged as a Claude Code plugin. It builds an
agent-ready business ontology of a GTM stack (Pipedrive, HubSpot, Attio, Salesforce,
email marketing, ERP): objects and custom fields with business semantics, pipelines
with entry/exit criteria, AI-filled fields and their prompts, automations with data
fingerprints, agent actions, and KPIs — a 4-layer, machine-readable model.

The skill is self-contained: it bundles the renderer (`tools/render_ontology.py`),
the JSON schemas, and a complete validated example ontology.

## Install

**From a local checkout (development / testing):**

```bash
claude --plugin-dir ./plugin
```

**Reload after edits, without restarting:**

```
/reload-plugins
```

**From a marketplace** (once this repo is registered as one):

```
/plugin marketplace add zawlodzki/GTM-ontology-framework
/plugin install gtm-ontology-builder
```

## Use

The skill is model-invoked — describe the task and Claude picks it up:

> Build an ontology of my CRM.

or invoke it directly by its namespaced name:

```
/gtm-ontology-builder:gtm-ontology-builder
```

It runs a phased interview (scope → discovery → semantic modeling → business logic →
agent actions & policy → validation), asking for confirmation at each gate, and writes
the result to a `gtm-ontology/` folder at your workspace root.

## Rendering

After the ontology exists, generate human-facing views:

```bash
pip install pyyaml
python skills/gtm-ontology-builder/tools/render_ontology.py gtm-ontology/
```

Output lands in `gtm-ontology/render/` — a process table, a Mermaid funnel, a field
dictionary, an action catalog, and an interactive `explorer.html`. See
`skills/gtm-ontology-builder/examples/gtm-ontology/render/` for a sample.

## Contents

```
plugin/
├── .claude-plugin/plugin.json          manifest
└── skills/gtm-ontology-builder/
    ├── SKILL.md                        phase-by-phase instructions
    ├── references/                     artifact format spec, CRM type mapping
    ├── templates/                      starter artifact templates
    ├── schemas/                        JSON Schemas (validation)
    ├── tools/render_ontology.py        the renderer
    └── examples/gtm-ontology/          complete worked example (Pipedrive B2B SaaS)
```
