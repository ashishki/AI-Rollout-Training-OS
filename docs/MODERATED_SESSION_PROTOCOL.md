# Ship It? Y/N Moderated Session Protocol

Updated: 2026-07-13
Status: protocol only; no moderated session recorded

This protocol is the next product-evidence gate for the local synthetic demo.
It does not authorize outreach, collection of private workflow data, or a claim
that training changes team behavior. A real session requires a consenting adult
participant and a human facilitator.

## Research question

Can a participant explain a safer permission decision after completing a
bounded set of synthetic scenarios, and which scenario wording or consequence
remains confusing? This is a usability/learning question, not a certification,
security-control, incident-reduction, or productivity study.

## Session boundary

- Duration: target 20-30 minutes.
- Input: only the committed synthetic Ship It? Y/N scenarios.
- Participant identifier: random session code; do not store a name, email,
  employer, repository, source code, credentials, raw prompt, or screen capture.
- Facilitator records categorical decisions and paraphrased observations only.
- Local analytics may be inspected with the participant's knowledge, then
  cleared; no tracking endpoint is enabled.
- The participant can stop or decline any question without consequence.

## Rubric

For three facilitator-selected scenarios, record the participant's decision and
one-sentence rationale before feedback, then repeat with a matched or adjacent
scenario after feedback.

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| Boundary recognition | Misses the privileged/sensitive boundary | Notices risk but cannot locate the boundary | Identifies the concrete boundary and affected resource |
| Action choice | Unsafe approve or unrelated action | Safer direction but scope/approval is incomplete | Chooses deny, clarify, sandbox, scope, eval, inspect, or escalate with a reason |
| Consequence reasoning | Unsupported or absent | Names a generic risk | Connects the action to a plausible, scenario-grounded consequence |
| Safer alternative | None | Generic “be careful” | Gives a bounded next step that preserves the task's intent |

The rubric score is descriptive for this session. Do not average it into a
population metric or claim improvement from one participant. Record wording
confusion separately from permission judgment.

## Required record

Only after a real session, add one privacy-reviewed record to
`docs/evidence/moderated_session_log.json` with:

- random `session_id` and date;
- participant role category and prior agent-use band, without employer/name;
- consent and privacy-review booleans;
- scenario IDs, pre/post categorical decisions, rubric totals, and paraphrased
  confusion points;
- facilitator limitations and whether a follow-up was consented;
- explicit false fields for certification, production, incident reduction,
  adoption, paid conversion, and causal learning claims.

The log's tests must continue to reject a count that does not equal the records
array. A self-authored dry run belongs in tests/fixtures and must not be entered
as a moderated session.

## Decision rule

- Continue only to another bounded session when the record is complete and at
  least one concrete wording/feedback change is supported by observed behavior.
- Revise scenarios when confusion is attributable to wording rather than the
  permission concept.
- Pause when participants cannot relate the scenarios to their work or when the
  required privacy boundary prevents a useful session.
- No release/adoption claim follows automatically from any number of sessions;
  a later evidence review must decide what the records support.

## Current blocker

The repository cannot supply a real participant. As of 2026-07-13 the canonical
session count is zero. This is an external evidence gate, not a reason to invent
a participant, copy a buyer target list, or relabel a developer test as research.
