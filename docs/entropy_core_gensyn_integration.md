# Entropy Core And Gensyn Integration

Status: implemented local permission decision receipt; Core runtime not adopted
Last updated: 2026-05-31

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

Default level: receipt-compatible for permission decision receipts.

Local artifacts:

- `permission_judgment_record`
- `permission_decision_receipt` implemented in
  `ai_rollout_os/permissions/proof.py`
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

Implemented now:

- `build_permission_decision_receipt(...)` records scenario id, selected
  decision, expected decision, outcome, risk category, permission boundary, and
  evidence refs for scenario context, boundary, and lesson.
- The existing permission simulator result loop builds a receipt after scoring
  in `/app/permission-simulator/decisions` and
  `/demo/permission-simulator/decisions`, then exposes verifier status, receipt
  hash, and evidence refs in the result markup.
- Unsafe decisions become failed receipts; partial decisions become
  `needs_review`.
- `tests/test_permission_proof_receipts.py` covers passed, failed, and
  mismatched-score paths. `tests/test_permission_ui.py` covers route-level
  receipt wiring for passed and failed simulator decisions.

Next implementation tasks:

1. Reuse `build_permission_decision_receipt(...)` in the Ship It? Y/N game
   result path when the React/Vite game scoring loop is implemented.
2. Use schema compatibility before changing scenario/scoring receipt formats.
3. Keep UI, gameplay, facilitation, and learner feedback product-local.
4. Block workshop/product claims when receipts lack verifier status or evidence
   for the expected boundary.

Core value here: make permission training outcomes explainable and auditable
without turning the game into a compliance platform.

Not adopted: decentralized runtime, token incentives, on-chain coordination,
model training, or P2P agent swarms.
