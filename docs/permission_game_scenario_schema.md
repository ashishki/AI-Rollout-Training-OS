# Permission Game Scenario Schema

Status: planned
Owner: codex
Last updated: 2026-05-31

## Purpose

This schema defines the data contract for Ship It? Y/N scenarios. The same
scenario records should power:

- public React/Vite game play;
- deterministic Python scoring tests;
- workshop facilitator notes;
- future authenticated team summaries.

The schema must remain data-driven so new scenario packs can be added without
rewriting game UI logic.

## Required Scenario Fields

```json
{
  "id": "eval-bypass-before-demo",
  "level": 6,
  "title": "Eval Is Red, Demo Is Soon",
  "agent_name": "PatchPilot",
  "agent_message": "Eval looks non-critical. I can bypass it for the demo.",
  "tool_call": {
    "type": "config_change",
    "surface": "ci_eval",
    "scope": "deployment_gate",
    "permission_request": "write"
  },
  "context": [
    {
      "type": "terminal_log",
      "label": "eval output",
      "content": "Regression detected in checkout flow.",
      "trusted": true
    }
  ],
  "inspect_artifacts": [
    {
      "id": "diff-eval-bypass",
      "label": "CI diff",
      "kind": "diff",
      "content": "- run: npm test\n+ run: npm test -- --skip-risky-suite",
      "reveals_risk": "eval_bypass"
    }
  ],
  "choices": [
    "approve",
    "deny",
    "inspect_diff",
    "require_eval",
    "run_in_sandbox",
    "restrict_scope",
    "escalate_reviewer"
  ],
  "best_choices": ["require_eval"],
  "acceptable_choices": ["escalate_reviewer"],
  "unsafe_choices": ["approve"],
  "overblock_choices": ["deny"],
  "permission_boundary": "blocked",
  "risk_category": "eval_bypass",
  "meters": {
    "velocity": -8,
    "blast_radius": 45,
    "trust": -20,
    "eval_confidence": -35,
    "audit_trail": -15
  },
  "feedback": {
    "approve": {
      "outcome": "unsafe",
      "consequence": "The demo shipped with a hidden regression.",
      "lesson": "Eval gates protect rollout quality under pressure.",
      "safer_alternative": "Fix the regression or ship a scoped canary with rollback."
    },
    "require_eval": {
      "outcome": "correct",
      "consequence": "The rollout paused until the regression was understood.",
      "lesson": "Demo pressure is not a release policy.",
      "safer_alternative": "Run the eval, fix the issue, then retry the gate."
    }
  },
  "badges": ["eval_gate_preserved"],
  "audit_events": [
    "required_eval_before_deploy"
  ],
  "facilitator_notes": [
    "Ask players whether they have ever approved a skipped test or eval under time pressure."
  ]
}
```

## Enumerations

Allowed choices:

- `approve`
- `deny`
- `inspect_diff`
- `run_in_sandbox`
- `require_eval`
- `restrict_scope`
- `escalate_reviewer`
- `rollback`

Permission boundaries:

- `allowed`
- `needs_approval`
- `blocked`
- `unknown`

Risk categories:

- `secrets`
- `destructive_filesystem`
- `diff_misrepresentation`
- `test_deletion`
- `indirect_prompt_injection`
- `overbroad_permission`
- `eval_bypass`
- `dependency_install`
- `ci_edit`
- `network_access`
- `log_exposure`
- `scope_creep`
- `context_contamination`

Feedback outcomes:

- `correct`
- `partial`
- `unsafe`
- `overblock`

## Validation Rules

Every scenario must:

- have a stable `id`;
- have exactly one `level` between 1 and 7 for the first game pack;
- include `agent_message`, `tool_call`, `choices`, `risk_category`, and
  `permission_boundary`;
- include at least one `best_choices` value;
- include feedback for every playable choice;
- mark unsafe and overblock choices when applicable;
- include one or more audit events;
- include at least one facilitator note;
- avoid real secrets, real customer data, real employee data, real commands that
  can be copied into a shell, or claims of compliance certification.

## Client/Server Contract

Python owns authoritative validation and final scoring.

The React client may preview meter movement for responsive UX, but client-side
score previews are not authoritative for authenticated or workshop reporting.

Public demo persistence is local only:

- `session_id`
- `scenario_order`
- `decisions`
- `time_to_decision`
- `inspected_artifacts`
- `final_score`

Authenticated workshop reporting may later store:

- actor or anonymous team identifier;
- scenario id;
- selected decision;
- outcome;
- risk category;
- timestamp;
- session id.

No raw prompt, real code, real credentials, real logs, or customer artifacts
belong in public demo scenario records.
