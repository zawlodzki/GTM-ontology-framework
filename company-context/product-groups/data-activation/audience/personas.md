---
kind: personas
id: data-activation-personas
scope: product-group:data-activation
meta:
  source: synthetic
  status: example
  updated: 2026-07-14
---

# Data Activation personas

## Head of Data

**Typical role:** technical sponsor, evaluator, and governance owner.

**Goals**

- Reduce one-off exports and fragile destination pipelines.
- Keep the warehouse and modeled layer as the source of truth.
- Make activation access observable, reversible, and governed.
- Protect engineering capacity for higher-value platform work.

**Concerns**

- A vendor may introduce opaque transformations or a second customer model.
- Business users may activate fields without understanding consent or quality.
- Connector failures may be difficult to detect, reconcile, or replay.

**Decision criteria**

- Clear warehouse read boundaries and destination write behavior.
- Versioned mappings, monitoring, audit history, and failure recovery.
- Fine-grained access controls and explicit handling of deletes and suppressions.

**Influence:** validates architecture and security, defines technical acceptance,
and can block the purchase when governance or operational ownership is unclear.

## Lifecycle Marketing Lead

**Typical role:** business champion and activation use-case owner.

**Goals**

- Launch reliable lifecycle segments without recurring engineering tickets.
- Use customer value, behavior, and consent attributes in engagement workflows.
- Test new audiences faster while preserving understandable definitions.

**Concerns**

- Data may arrive too late or differ from marketing-platform counts.
- Governance may make every change as slow as the current engineering process.
- The team may receive access without the skills to validate an audience.

**Decision criteria**

- Predictable refresh cadence and visible audience counts.
- A controlled workflow for creating, reviewing, and publishing definitions.
- Clear ownership when source data or destination delivery fails.

**Influence:** defines the initial use case, validates operational usefulness, and
owns adoption after technical approval.

## Relationship between personas

The Lifecycle Marketing Lead creates urgency and defines business value. The Head
of Data protects architecture and governance. A qualified opportunity requires
both roles or named equivalents; neither technical readiness nor business demand
is sufficient alone.
