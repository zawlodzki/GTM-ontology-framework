# Agent actions

## Advance deal to next stage (`advance-deal-stage`)

*Executor:* agent · *Approval:* conditional (required when target stage is won or lost, or deal.amount > 50000)

User asks to progress a deal, or a proposal from action:qualify-lead was accepted. Never for backward moves (humans only) and never to skip stages.

**Preconditions**

1. Target stage is a directly allowed transition from current stage
1. All exit criteria of the current stage evaluate true on live data
1. All required_properties of the target stage are non-empty
1. All entry criteria of the target stage evaluate true

**Workflow**

1. Re-read deal from Pipedrive (never cache); evaluate all preconditions.
2. If approval_condition triggers, request human approval; proceed only on explicit yes.
3. Terminal states: update deal status (won/lost) per bindings note. Others: update stage_id via enum_map.
4. Add note: '[agent] moved <from> -> <to>: <reason>'.

**Side effects:** automation:create-demo-activity fires when target is demo; do NOT create a demo prep activity manually

## Qualify lead from transcript (`qualify-lead`)

*Executor:* agent · *Approval:* none

User asks to qualify a lead/deal; or agent finds a deal with a newer transcript than its current qualification; or qualification is empty despite a logged call.

**Preconditions**

1. Deal exists and is in stage incoming or qualified
1. A call transcript matched to a linked person is available
1. automation:qualify-from-transcript did not already process this transcript

**Workflow**

1. Load deal, org, person context via bindings; verify preconditions live.
2. Run prompt:lead-qualification with transcript + deal context. Validate output contract ('## Qualification' header, SCORE line).
3. Write ai_qualification_summary and ai_qualification_score via update_deal.
4. Add note: '[agent] qualification generated from transcript <date>'.
5. Evaluate Qualified exit criteria; if met, PROPOSE advance-deal-stage to user (do not execute).

**Side effects:** none

*Generated from ontology `acme-analytics` v1.6.0 (2026-07-23), do not hand-edit.*
