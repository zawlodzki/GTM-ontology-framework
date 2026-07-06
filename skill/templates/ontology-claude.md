<!-- Template for gtm-ontology/CLAUDE.md — the agent navigation file.
     The skill fills <placeholders> and writes it in Phase 5.
     Mirror to gtm-ontology/AGENTS.md when the repo uses that convention. -->
# GTM Ontology — agent guide

This folder is the machine-readable ontology of <company>'s go-to-market stack
(GOF format): business semantics, processes, automations, agent actions, KPIs.
It is the source of truth. CRM live data is NOT here — read it via the access
methods declared in `binding/systems/`.

## Navigation (strict order)

1. Read `manifest.yaml` first — business summary + index of every artifact with
   a one-line summary and a `load_when` hint. Version: check it matches what you
   expect; if renders or caches disagree with YAML, YAML wins.
2. Load full artifacts ONLY when their `load_when` matches your task. Do not
   bulk-load the folder — artifacts are sized for selective reading.
3. Before executing ANY action: read `governance/agent-policy.yaml`, then the
   `dynamic/actions/<id>.yaml` contract, and follow its `workflow` order exactly.

## Hard rules

- Never act on artifacts with `meta.status: draft` — read them as hypotheses only.
- Actions not listed in agent-policy for your role are forbidden.
- Never write fields marked `writable: false` in `binding/mappings/` — they are
  bot- or human-managed. Attribute field values using `filled_by` (semantic layer)
  and automation `data_fingerprint`s before trusting or changing them.
- Moving records between process stages: only via the relevant action, only
  forward, only when the current stage's exit criteria hold on LIVE data.
- Files in `render/` are generated views for humans — never edit, never cite as source.

## Layout

| Path | Contents |
|---|---|
| `manifest.yaml` | index — always read first |
| `context/` | business context, glossary |
| `semantic/objects/` | object types, property semantics, enum definitions |
| `binding/` | systems, bindings (physical field keys), identity, discovery snapshots |
| `dynamic/` | processes (stage criteria), automations (+fingerprints), actions, prompts, drafts |
| `measurement/kpis/` | KPI definitions |
| `governance/agent-policy.yaml` | what you may do — check before acting |
