# Company Context & GTM Ontology Builder (Claude Code plugin)

This plugin packages two complementary skills. `company-context-builder` inventories
business materials, researches the company and competitors, analyzes Closed Won CRM
evidence, reconciles conflicts, and builds a validated static `company-context/`.
`gtm-ontology-builder` then maps live GTM systems into an agent-ready ontology of
objects, fields, pipelines, automations, actions, governance, and KPIs.

Both skills are self-contained. They bundle their format references, schemas,
templates, validation tools, and worked or starter context required to run outside
this repository.

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

The skills are model-invoked — describe the task and Claude picks the relevant one:

> Build company context from my materials and won CRM deals.

> Build an ontology of my CRM using the existing company context.

or invoke it directly by its namespaced name:

```
/gtm-ontology-builder:gtm-ontology-builder
```

or:

```
/gtm-ontology-builder:company-context-builder
```

Each skill uses phased discovery and confirmation gates. The first writes
`company-context/`; the second links it as canonical static context while building
`gtm-ontology/`.

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
└── skills/
    ├── company-context-builder/         context workflow, templates, schemas, and tools
    └── gtm-ontology-builder/            ontology workflow, examples, schemas, and tools
```
