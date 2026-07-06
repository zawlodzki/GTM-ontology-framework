# Changelog — acme-analytics ontology

## 1.1.0 — 2026-07-06
- Stage model extended (blueprint alignment): bad_examples, customer_verifier,
  probability (forecast weights 0.10→1.0), SLA split into target_duration_days +
  rotting_threshold_days, tasks, tips, loss_reasons.
- New artifact type: drafts (A14) — added qualification-followup-email.

## 1.0.0 — 2026-07-06
- Initial confirmed ontology: Pipedrive (CRM) + n8n automations.
- 3 object types, 1 process (7 stages), 3 automations, 2 agent actions, 3 KPIs.
- Known gaps: person.lifecycle_stage=opportunity has no automation — relies on AE discipline;
  Mailerlite (email marketing) out of scope for v1, planned as second system.
