# Pilot Success Rubric

Version: 1.0
Last updated: 2026-05-20
Status: active Phase 6 gate

Use this rubric after a pilot has current outcome metrics, discovery evidence,
and manager review notes. The decision must be based on observed customer
evidence and stored product records, not internal optimism.

---

## Outcome Decisions

### Expand

Expand when the pilot shows strong evidence that the product should move into a
larger paid or multi-team rollout with the same customer.

- Product: activation and assignment completion are strong, at least one
  manager-approved workflow change exists, and time-to-first-safe-use is short
  enough for the buyer's operating cadence.
- Quality: retrieval and feedback checks have no P0/P1 regression, citations are
  acceptable, and manager review does not find uncited policy guidance.
- Business: a named buyer owns the expansion path, budget or procurement steps
  are credible, and blockers have explicit product responses.

### Repeat

Repeat when the pilot shows product value but needs another narrow pilot before
expansion.

- Product: learners complete the workflow and managers approve at least one
  useful change, but activation, completion, or review time is uneven.
- Quality: feedback is mostly trusted, but citation precision, override rate, or
  no-answer behavior needs more measurement.
- Business: willingness-to-pay evidence exists but the buyer, procurement path,
  or second-team expansion path is not yet clear.

### Pause

Pause when the pilot does not yet justify more product or sales investment for
the same customer.

- Product: activation or completion is weak, safe-use timing is too slow, or no
  approved workflow change emerges.
- Quality: risk flags, human overrides, or eval regressions create unresolved
  trust concerns.
- Business: the customer cannot name a high-priority adoption blocker, budget is
  absent, or discovery evidence is mostly internal assumptions.

### Reposition

Reposition when repeated evidence suggests the ICP, buyer, or first use case is
wrong.

- Product: the support-team workflow is not the urgent adoption problem even
  after onboarding and reminders.
- Quality: the policy-grounded feedback model is not the trust mechanism the
  customer values.
- Business: value concentrates in a different buyer, segment, or use case than
  the target market wedge.

## Metric Groups

| Group | Metrics | Decision Use |
|-------|---------|--------------|
| Product metrics | Activation rate, assignment completion rate, guardrail pass rate, submission rate, manager review SLA, approved workflow changes per cohort, reused workflow changes after approval, risk flag rate, time-to-first-safe-use | Proves whether the pilot workflow creates safe role-specific adoption. |
| Quality metrics | Retrieval hit@3, hit@5, MRR, citation precision, no-answer accuracy, feedback faithfulness, human override rate, eval regression rate | Proves whether policy-grounded feedback is trustworthy enough for manager review. |
| Business metrics | Pilot-to-paid conversion, time to launch first cohort, time to first approved workflow change, expansion from first team to second team, security review cycle time, gross retention of active teams | Proves whether the buyer has urgency, budget, and expansion potential. |

## Minimum Evidence

- Use the latest `PilotOutcomeMetrics` output for product metrics.
- Use current retrieval and feedback evaluation evidence for quality metrics.
- Use `docs/customer_discovery.md` records for buyer, blocker, workaround, and
  willingness-to-pay evidence.
- Do not count internal assumptions as evidence for expansion.

## Decision Record Template

```markdown
### Pilot / Customer / Date

- Decision: expand | repeat | pause | reposition
- Product evidence:
- Quality evidence:
- Business evidence:
- Top blocker:
- Follow-up owner:
- Next review date:
```
