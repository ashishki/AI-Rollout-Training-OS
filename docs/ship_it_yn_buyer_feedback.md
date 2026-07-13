# Ship It? Y/N Buyer Feedback Loop

Status: manual demo template
Scope: buyer conversations for `/demo/ship-it-yn`

Use this artifact after a bounded manual demo or workshop conversation. It is a
learning loop for whether the game creates a credible buyer discussion, not a
proof of PMF, paid conversion, compliance certification, or production safety.

Related artifacts:

- Moderated-session protocol and rubric: `docs/MODERATED_SESSION_PROTOCOL.md`
- Machine-readable session log: `docs/evidence/moderated_session_log.json`
- Facilitator pack: `docs/ship_it_yn_facilitator_pack.md`
- Safe team summary: `ai_rollout_os/permissions/game_summary.py`
- Local analytics snapshot: browser `localStorage` key
  `ship-it-yn-analytics-v1`
- Discovery registry: `docs/customer_discovery.md`

## Manual Demo Feedback Template

Manual demo feedback template fields:

```markdown
### DEMO-NNN - Segment / Buyer Role

- Date:
- Source type: manual_demo
- Company segment:
- Buyer role:
- Team agent usage:
- Current permission review workaround:
- Strongest scenario:
- Why strongest:
- Weakest scenario:
- Why weakest:
- Willingness to run workshop:
- Objections:
- Security or procurement blockers:
- Success metric the buyer would trust:
- Next action:
- Follow-up owner:
- No PMF or paid-conversion claim:
```

## Field Guidance

- Buyer role: name the role, not the person. Examples: VP Support, Enablement
  lead, RevOps lead, AI Transformation lead, Security partner, or Engineering
  Enablement.
- Team agent usage: capture whether the team already uses coding agents,
  support copilots, internal workflow agents, spreadsheet automation, or only
  informal chat tools.
- Strongest scenario: record the level that made the buyer describe a real
  workflow risk, such as eval bypass, broad cleanup, indirect prompt injection,
  or overbroad permission.
- Weakest scenario: record the level that felt irrelevant, confusing, too
  obvious, or mismatched to the buyer's operating environment.
- Willingness to run workshop: use one of `yes`, `maybe`, or `no`, with the
  buyer-stated reason.
- Objections: capture direct objections around urgency, audience, security,
  enablement burden, procurement, budget owner, or credibility.
- Next action: choose `schedule_workshop`, `send_pack`, `customize_scenarios`,
  `security_review`, `collect_more_evidence`, `pause`, or `reposition`.

Do not store customer name, personal email, raw learner prompt, proprietary workflow text,
credential, secret, source code, or screenshots containing
sensitive data in this document.

## Evidence Log

Use one entry per buyer conversation. Keep observed evidence and
founder/operator assumptions separate so later demo-readiness reviews do not
overstate validation.

```markdown
### DEMO-NNN - Segment / Buyer Role

- Date:
- Buyer role:
- Company segment:
- Team agent usage:
- Strongest scenario:
- Weakest scenario:
- Willingness to run workshop:
- Objections:
- Next action:

Observed evidence:
- Direct buyer statement:
- Behavior during demo:
- Workshop or procurement signal:
- Analytics or aggregate summary signal:

Founder/operator assumptions:
- Assumption:
- Why it is still an assumption:
- Evidence needed to validate it:

Claim boundary:
- Assumptions do not count as buyer validation.
- No PMF or paid-conversion claim from this record alone.
- No compliance, certification, or production-readiness claim from game
  completion, workshop discussion, or local analytics.
```

## Review Cadence

After every three manual demos, review the evidence log against
`docs/customer_discovery.md` decision rules:

- Continue if multiple buyers name the same workflow risk and agree to a
  workshop or scenario-customization follow-up.
- Customize scenarios when the buyer sees the category but not the exact team
  workflow.
- Pause or reposition when objections cluster around low urgency, wrong buyer,
  or lack of agent usage.
- Keep assumptions labeled until a buyer, blocker, or pilot artifact directly
  supports them.
