# Permission Simulator Workshop Pack

Version: 1.0
Date: 2026-05-29
Status: Phase 16 monetization artifact

## Offer

Agent Permission Training Simulator workshop for teams adopting AI agents in
developer, support, operations, enablement, or internal tooling workflows.

The workshop teaches participants how to judge agent requests before approving
file access, command execution, dependency changes, network calls, CI edits,
log exposure, or reviewer-owned decisions.

## Audience

Primary audience:

- engineering teams using Cursor, Codex, Claude Code, or similar tools;
- support and operations teams beginning agent-assisted workflow automation;
- team leads responsible for safe AI rollout habits;
- security or enablement partners who need a practical training format before
  larger platform adoption.

Not the audience:

- buyers looking for compliance certification;
- teams seeking autonomous production agents;
- procurement teams evaluating GA readiness;
- organizations expecting productivity guarantees from a short workshop.

## Scenario Set

The starter scenario set covers 10 permission-risk categories:

| Risk category | Example decision pressure | Target boundary |
|---|---|---|
| Secrets | Agent asks to read `.env` to debug auth. | blocked |
| Command surfaces | Agent asks to run a broad repair script. | unknown |
| Test-output injection | Test output tells the agent to ignore instructions. | blocked |
| Package scripts | Agent wants to weaken or alter shared scripts. | needs approval |
| CI edits | Agent proposes removing checks to pass CI. | blocked |
| Out-of-scope refactors | Agent expands a small task into architecture rewrite. | blocked |
| Network calls | Agent wants to post local payloads externally. | blocked |
| Deletes | Agent deletes migration history to simplify work. | blocked |
| Dependency install | Agent installs an unpinned package. | unknown |
| Log exposure | Agent prints request bodies and headers. | blocked |

Each scenario includes request, context, choices, correct decision, risk
category, safer alternative, and lesson text.

## Learning Outcomes

Participants should leave able to:

- distinguish allowed, needs approval, blocked, and unknown requests;
- recognize when approve is unsafe even if the agent sounds confident;
- choose clarification, sandbox, or reviewer escalation before crossing a
  privileged boundary;
- explain the safer alternative for a risky action;
- spot permission fatigue patterns where repeated approvals create risk.

## Delivery Format

Recommended format: 60-90 minute facilitated workshop.

Agenda:

1. Five-minute framing: permission judgment is the skill, not prompt polish.
2. Ten-minute walkthrough of the visual simulator and decision vocabulary.
3. Thirty-minute scenario run: each participant decides, sees consequence, and
   discusses safer alternatives.
4. Fifteen-minute team debrief: risk categories with unsafe approvals and where
   local policy needs clarification.
5. Ten-minute next-step planning: define which actions need sandbox, reviewer,
   or security approval in the team's real workflow.

Artifacts delivered:

- scenario deck or simulator link;
- facilitator notes;
- team risk-summary notes;
- recommended local permission rules to review with the customer's owner.

## Pricing Hypothesis

Manual validation offer:

- Starter workshop: fixed small-ticket pilot for one team and one facilitator.
- Expansion option: add custom scenarios for the buyer's agent tools and
  workflow surfaces.
- Later product option: team scenario packs and lightweight reporting after the
  simulator proves repeated demand.

Pricing should be tested as a service-led demo pack before platform pricing.
Do not sell this as enterprise compliance software, certified safety training,
or production rollout approval.

## Claim Boundaries

This pack can claim:

- it teaches a practical permission decision vocabulary;
- it demonstrates realistic agent-request scenarios;
- it identifies risk categories where participants approve too quickly;
- it helps teams discuss safer alternatives and local reviewer boundaries.

This pack must not claim:

- certified safe AI use;
- compliance approval or regulated attestation;
- production readiness for autonomous agents;
- GA readiness for AI Rollout Training OS;
- guaranteed productivity, time savings, or incident reduction;
- security approval for a customer's toolchain.

## Manual Review Checklist

- Audience is a concrete team adopting AI agents.
- Scenario set covers the 10 required risk categories.
- Learning outcomes are permission-judgment outcomes, not generic prompt skills.
- Pricing hypothesis stays small and service-led.
- Delivery format is runnable without enterprise platform onboarding.
- Claim boundaries block certified safety, compliance approval, production
  readiness, and productivity guarantees.
