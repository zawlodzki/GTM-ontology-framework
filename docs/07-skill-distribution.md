# Skill distribution

The source of truth for shareable skills is:

- `skills/gtm-ontology-builder/`
- `skills/company-context-builder/`

Do not edit their plugin payloads or `.skill` archives directly. Those are
generated distributions.

## Root framework copies

`skills/gtm-ontology-builder/` is standalone and therefore bundles selected
files that also exist at the repository root:

- `tools/render_ontology.py`, `tools/lint_ontology.py`, and
  `tools/evaluate_context.py` → skill `tools/`
- `schemas/*.json` → skill `schemas/`
- `gtm-ontology/` → skill `examples/gtm-ontology/`
- `company-context/` → skill `examples/company-context/`

When any of those root files change, update the corresponding source-skill copy
in the same commit. This root-to-skill step is intentionally not performed by
the distribution workflow. Skill-specific instructions, references, and
templates stay under the source skill only.

## Generated distributions

Each source skill is mirrored, without `.DS_Store`, `__pycache__`, or `*.pyc`,
to both plugin payloads:

- `plugin/skills/<skill-name>/` for the Claude Code plugin
- `plugins/gtm-ontology-builder/skills/<skill-name>/` for the Codex plugin

The generator also creates `<skill-name>.skill` at the repository root. Each
archive contains one top-level directory named after the skill and uses stable
ordering, timestamps, and permissions so identical sources produce identical
bytes.

Run the generator locally with:

```bash
python tools/sync_skill_distributions.py sync
python tools/sync_skill_distributions.py check
```

`check` is read-only and exits non-zero when any payload or archive has drifted.

## GitHub Actions and versions

`.github/workflows/sync-skill-distributions.yml` runs after every push to
`main`, and can also be started with `workflow_dispatch`. It tests the generator,
finds the latest commit that changed `skills/`, synchronizes all distributions,
checks the result, and commits only generated paths as
`skill: regenerate distributions`.

For a new source revision the workflow increments the patch component in both
plugin manifests. The Claude manifest receives `X.Y.Z`; the Codex manifest
receives the same core plus `+codex.<12-character-source-sha>`. A repeated run
for the same source SHA does not increment the version again. The workflow uses
`contents: write`, never force-pushes, and retries once from the latest `main`
when a concurrent push wins the race.

Use `workflow_dispatch` to repair drift or retry a failed synchronization. The
repository must permit GitHub Actions to write to `main`; branch protection must
either allow that push or explicitly grant the Actions bot a bypass.

## Tagged release checks

Before a tagged release:

1. Run `claude plugin validate ./plugin`.
2. Validate `plugins/gtm-ontology-builder/` with the `plugin-creator` validator.
3. Install from the repository marketplace with
   `codex plugin add gtm-ontology-builder@personal`.
4. Confirm the installed cache contains both source skill entrypoints:
   `skills/gtm-ontology-builder/SKILL.md` and
   `skills/company-context-builder/SKILL.md`.

Use the `plugin-creator` cachebuster flow for local Codex updates. Never edit an
installed plugin cache directly.
