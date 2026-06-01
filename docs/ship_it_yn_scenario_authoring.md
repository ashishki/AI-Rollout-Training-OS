# Ship It? Y/N Scenario Authoring Workflow

Status: draft workflow
Scope: AI-assisted drafts for future scenario packs

This workflow lets AI help draft new Ship It? Y/N scenario packs while keeping
acceptance deterministic and human-owned. AI may propose variants, but Python
schema validation, deterministic scoring tests, safety tests, and human review
decide whether a scenario enters a playable pack.

## Prompt Boundaries

Allowed AI assistance:

- draft scenario premises from a named team workflow and risk category;
- generate alternative agent messages, consequences, lessons, safer
  alternatives, badges, audit events, and facilitator notes;
- suggest which existing choice labels should be correct, partial, unsafe, or
  overblock;
- create synthetic inspect artifacts that illustrate risk without real secrets,
  customer data, source code, command recipes, personal data, or proprietary
  workflow text.

Blocked AI assistance:

- no real command execution;
- no real repo mutation;
- no real permission approval;
- no live scoring authority;
- no certification, compliance, production-readiness, PMF, incident-reduction,
  or paid-conversion claims;
- no raw customer artifacts, credentials, private logs, personal identifiers, or
  copy-paste dangerous shell commands.

Use prompts that ask for structured scenario JSON matching
`docs/permission_game_scenario_schema.md`. The prompt must include the target
audience, risk category, permission boundary, intended lesson, and explicit
instruction to use only synthetic data.

## Required Human Review

A human reviewer owns every accepted scenario. Before a scenario can ship, the
reviewer must confirm:

- the premise maps to a real team workflow without naming a customer or person;
- the permission boundary is defensible;
- the best, acceptable, unsafe, and overblock choices teach the intended
  judgment;
- every playable choice has feedback that is useful and claim-safe;
- inspect artifacts reveal the same risk as `risk_category`;
- facilitator notes support discussion rather than blame;
- language is clear to the target team and does not overfit founder assumptions.

Human review can reject an AI draft even when it validates technically.

## Schema Validation

All accepted drafts must pass the authoritative Pydantic contract:

```python
PermissionGameScenario.model_validate(candidate_record)
```

Validation must enforce the field contract in
`ai_rollout_os/permissions/game_schema.py`, including:

- stable scenario id;
- allowed choice labels;
- supported risk category;
- supported permission boundary;
- feedback for every playable choice;
- inspect artifacts that reveal the scenario risk category;
- no extra undeclared fields.

## Safety Tests

Run the deterministic scenario and safety checks before merging a pack:

```bash
.venv/bin/python -m pytest \
  tests/test_permission_game_scenarios.py \
  tests/test_permission_game_safety.py \
  tests/test_permission_game_scoring.py -q
```

These tests guard schema validity, choice feedback coverage, scoring behavior,
unsupported claims, dangerous command text, secret-like strings, and customer
data leakage.

## Blocked Live Scoring Usage

AI can help draft copy, but it cannot score live players, approve agent actions,
or decide production permission policy. The deterministic Python scoring engine
and checked-in scenario records remain the only scoring path for product
behavior.

Do not connect scenario authoring prompts to public gameplay, workshop reports,
or authenticated permission decisions. Draft generation happens offline, then
humans review and tests validate before a pack is made playable.

## Pack Examples

### Dev scenario pack

- Audience: engineering teams using coding agents.
- Example risks: `diff_misrepresentation`, `test_deletion`, `eval_bypass`.
- Example premise: an agent asks to simplify a one-line diff, remove flaky test
  coverage, or bypass a red eval before a demo.
- Human review focus: make sure the safer path preserves tests, review context,
  and rollback options.

### Support scenario pack

- Audience: support operations and enablement teams using ticket copilots.
- Example risks: `indirect_prompt_injection`, `log_exposure`,
  `context_contamination`.
- Example premise: a ticket includes helpful facts plus hostile instructions,
  or a copilot wants to paste log excerpts into a customer-facing response.
- Human review focus: separate customer-provided evidence from instructions and
  avoid storing personal or proprietary support text.

### Ops scenario pack

- Audience: operations teams automating runbooks, alerts, and deployment gates.
- Example risks: `network_access`, `ci_edit`, `overbroad_permission`.
- Example premise: an agent asks for broad network access to investigate an
  alert or edit a deployment gate under time pressure.
- Human review focus: force bounded scope, rollback paths, audit events, and
  clear escalation points.

### Data scenario pack

- Audience: analytics and data teams using agents for notebooks, dashboards, or
  warehouse tasks.
- Example risks: `secrets`, `log_exposure`, `scope_creep`.
- Example premise: an agent asks to inspect a dataset preview, use environment
  variables, or broaden query access to debug a dashboard.
- Human review focus: keep sample data synthetic and require least-privilege
  access boundaries.

### Internal Tools scenario pack

- Audience: teams building internal admin tools, scripts, and workflow bots.
- Example risks: `overbroad_permission`, `destructive_filesystem`,
  `context_contamination`.
- Example premise: an agent wants a blanket admin token, bulk cleanup access, or
  permission to trust instructions from a shared internal note.
- Human review focus: narrow permissions by action, resource, duration, and
  trusted source.

## Merge Checklist

1. Draft generated with explicit synthetic-data boundaries.
2. Human reviewer accepts the premise, lesson, choices, and claim boundaries.
3. Scenario JSON passes `PermissionGameScenario.model_validate`.
4. Scenario, safety, and scoring tests pass.
5. Facilitator notes are discussion-oriented and avoid individual blame.
6. No live scoring or permission approval uses the draft-generation step.
