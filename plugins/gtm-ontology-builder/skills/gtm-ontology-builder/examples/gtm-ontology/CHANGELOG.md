# Changelog: acme-analytics ontology

## 1.2.0 (2026-07-13)
- Deduplication rules on identity.yaml (A7 `match`): match keys, distinguishing
  fields, never_match_on, and merge/survivorship policy per object.
- Fixed latent branch-merge bug: Organizations no longer auto-dedup on `domain`
  alone (branch offices share domain+name); domain matches now route to review.
- Known gap: org `address` / `vat_id` not modeled — needed to auto-distinguish
  branches. Until added, org merges stay human-reviewed.

## 1.1.0 (2026-07-06)
- Stage model extended (blueprint alignment): bad_examples, customer_verifier,
  probability (forecast weights 0.10→1.0), SLA split into target_duration_days +
  rotting_threshold_days, tasks, tips, loss_reasons.
- New artifact type: drafts (A14); added qualification-followup-email.

## 1.0.0 (2026-07-06)
- Initial confirmed ontology: Pipedrive (CRM) + n8n automations.
- 3 object types, 1 process (7 stages), 3 automations, 2 agent actions, 3 KPIs.
- Known gaps: person.lifecycle_stage=opportunity has no automation, relies on AE discipline;
  Mailerlite (email marketing) out of scope for v1, planned as second system.
