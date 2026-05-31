# Entropy Core And Gensyn Integration

Status: planned reference integration
Last updated: 2026-05-29

## Purpose

Training OS can use Entropy-style receipts to make permission simulations
auditable: what decision was made, what evidence was shown, what permission
boundary applied, and what correction feedback was produced.

Gensyn is only a design reference for diverse scenario/candidate generation and
evaluator/referee roles.

Before building custom Gensyn-shaped logic, run the Gensyn OSS reuse gate from
`repo://AI_workflow_playbook/docs/entropy_core_and_gensyn_reference_policy.md`.
Check official Gensyn repos first and record whether the result is dependency,
vendored component, adapted code, pattern-only reuse, or rejection.

## Entropy Core Use

Default level: receipt-compatible now; schema-compatible next.

Planned local artifacts:

- `permission_judgment_record`
- `scenario_decision_receipt`
- `learner_error_pattern`
- `referee_feedback_record`

Example:

```yaml
type: permission_judgment_record
source_project: ai-rollout-training-os
scenario_id: perm-001
decision: needs_approval
evidence_shown:
  - "Tool writes to external CRM."
  - "User data contains PII."
expected_boundary: human_approval_required
verifier:
  method: deterministic_answer_key
  status: passed
entropy_core:
  use_level: receipt_compatible
  runtime_dependency: false
```

## Required Context-Refs

```yaml
Context-Refs:
  - repo://AI_workflow_playbook/docs/entropy_core_and_gensyn_reference_policy.md
  - repo://Entropy_Protocol/docs/ENTROPY_CORE_AND_GENSYN_REFERENCES.md
```

## Gensyn-Inspired Pattern

Allowed adaptation:

```text
diverse scenario variants -> learner answer -> evaluator/referee verdict -> feedback
```

This can help produce varied training cases without turning the product into an
autonomous training swarm.

## Proof Layer Implementation

Training OS should use Entropy Core to prove scenario decisions and scoring
outcomes, not to run the game.

Implementation path:

1. Define `scenario_decision_receipt` with schema id, scenario id, learner
   action, expected permission boundary, score delta, evidence shown, and
   verifier status.
2. Use schema compatibility before changing scenario/scoring receipt formats.
3. Keep UI, gameplay, facilitation, and learner feedback product-local.
4. Block workshop/product claims when receipts lack verifier status or evidence
   for the expected boundary.

Core value here: make permission training outcomes explainable and auditable
without turning the game into a compliance platform.

Not adopted: decentralized runtime, token incentives, on-chain coordination,
model training, or P2P agent swarms.
