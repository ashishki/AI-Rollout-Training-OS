# Open-Source AI Rollout Research Protocol

Status: active
Date: 2026-05-22

This protocol is mandatory for solo/small-team showcase work when no corporate
design partner, internal policy packet, or real cohort data is available. The
agent must gather public policy, SOP, and role-workflow evidence to build
demo-safe training artifacts without claiming enterprise validation.

## When To Research

Use public research when a task needs:

- public AI policy examples;
- public SOP or support workflow examples;
- role-specific mission ideas;
- allowed/forbidden AI-use examples;
- public governance, risk, or adoption references;
- demo corpus material for a solo/small-team rollout.

## Allowed Sources

- public AI policy and responsible-use pages;
- public support, sales, operations, or customer-service SOP examples;
- public help-center and internal-process style documentation;
- public AI governance frameworks or guidance pages;
- public product docs that describe repeatable workflows;
- operator-authored notes and synthetic submissions clearly labeled as demo.

## Forbidden Sources

- private company policies, internal SOPs, customer data, employee submissions,
  HR records, or proprietary documents without explicit approval;
- claims that a public demo proves adoption, productivity lift, enterprise
  readiness, or paid conversion;
- regulated compliance attestation claims.

## Required Source Register

Every public demo corpus must include:

| Field | Required |
|---|---|
| source_url_or_locator | yes |
| captured_at | yes |
| source_type | yes |
| role_or_policy_use | yes |
| extracted_fact | yes |
| demo_use | yes |
| limitation | yes |

Store links and short extracted notes. Do not commit large raw pages unless they
are sanitized fixtures with explicit public-demo labels.

## Claim Rule

Public research may support role-pack demos, policy-grounded feedback examples,
and solo/small-team training flows. It does not support enterprise adoption,
productivity, compliance, or GA claims. Real adoption proof still requires a
real cohort or named reviewer evidence.
