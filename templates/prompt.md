---
kind: prompt
id: lead-qualification
meta: {source: declared, status: draft, updated: 2026-01-01}
used_by:
  - property:deal.ai_qualification_summary
  - action:qualify-lead
model: gpt-4.1 (as configured in n8n node)
inputs:
  - {id: transcript, description: full call transcript, source: Fireflies via n8n}
  - {id: deal_context, description: amount, org industry, source channel, source: Pipedrive}
output_contract: >
  Markdown starting with '## Qualification'; sections Budget/Authority/Need/Timeline;
  final line 'SCORE: <0-100>'. Written to deal.ai_qualification_summary; score parsed
  into deal.ai_qualification_score.
version: 3
---

<!-- VERBATIM production prompt below. Never paraphrase — this is provenance. -->

You are a B2B sales analyst. Based on the call transcript and deal context below...
