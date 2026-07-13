# GTM Ontology Framework: project guide

This repo contains the GOF framework (docs, schemas, templates, tools), the
`gtm-ontology-builder` skill (`skill/`), and a complete example ontology instance
(`gtm-ontology/`). Framework spec: `README.md` and `docs/`.

<!-- gtm-ontology:start -->
## GTM Ontology

The business ontology of the GTM stack lives in `gtm-ontology/`. Before working
with CRM data, sales processes, pipelines, or agent actions, read
`gtm-ontology/CLAUDE.md` (navigation rules), then `gtm-ontology/manifest.yaml`
(artifact index). Never act on artifacts with `meta.status: draft`; check
`gtm-ontology/governance/agent-policy.yaml` before executing any action.
<!-- gtm-ontology:end -->

## Commit Message Format

Use scope-prefixed commits: **`scope: description`**. Scope is what changed 
(the subsystem/area affected), not the type of change. This makes history 
readable for debugging, investigating incidents, and understanding project 
trajectory. The description should be clear enough that type is obvious.

**Natural scopes for this project:**
- `gtm-ontology:` — changes to the business ontology instance
- `skill:` — changes to the gtm-ontology-builder skill
- `docs:` — framework documentation
- `templates:` — skill/project templates
- `tools:` — render/utility scripts

**Examples:**
- `gtm-ontology: add new-business process with lead scoring`
- `skill: improve variable interpolation in draft generation`
- `docs: clarify semantic object relationship rules`
- `tools: fix render_ontology.py datetime handling`
