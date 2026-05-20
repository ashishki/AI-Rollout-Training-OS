# Customer Discovery Evidence Registry

Version: 1.0
Last updated: 2026-05-20
Status: active Phase 6 registry

This registry captures customer discovery for the support-team market wedge in
`docs/product_maturity_roadmap.md#target-market-wedge`. It separates observed
customer evidence from internal assumptions so pilot decisions do not overfit
founder guesses or synthetic signals.

---

## Evidence Schema

Every discovery record must include these fields:

| Field | Required | Description |
|-------|----------|-------------|
| `record_id` | yes | Stable identifier such as `DISC-001`. |
| `date` | yes | Interview, pilot review, or evidence collection date. |
| `source_type` | yes | `interview`, `pilot_review`, `sales_call`, `support_artifact`, or `internal_assumption`. |
| `company_segment` | yes | B2B SaaS, business services, regulated-adjacent, or disqualified segment. |
| `icp_fit` | yes | `strong`, `medium`, `weak`, or `disqualified`, with reason. |
| `buyer_role` | yes | VP Support, Enablement, RevOps, AI Transformation lead, or other named role. |
| `internal_blockers` | yes | Security, Legal, Compliance, IT, Procurement, or none observed. |
| `current_workaround` | yes | What the team does today instead of this product. |
| `adoption_blocker` | yes | The concrete blocker preventing safe AI adoption or expansion. |
| `willingness_to_pay_signal` | yes | Budget owner, paid pilot, procurement motion, explicit price reaction, or no signal. |
| `pilot_outcome_notes` | yes | Activation, completion, approved workflow changes, risk notes, and manager review observations. |
| `confidence_level` | yes | `high`, `medium`, or `low`, based on directness and repeatability of evidence. |
| `evidence_quote_or_summary` | yes | Short paraphrase or quote fragment that avoids proprietary or personal data. |
| `next_decision` | yes | `expand`, `repeat`, `pause`, `reposition`, or `collect_more_evidence`. |

Do not store personal data, proprietary workflow text, customer names embedded in
submissions, credentials, secrets, or raw learner artifacts in this registry.

## Interview Log Template

```markdown
### DISC-NNN - Company Segment / Buyer Role

- Date:
- Source type:
- Company segment:
- ICP fit:
- Buyer role:
- Internal blockers:
- Current workaround:
- Adoption blocker:
- Willingness-to-pay signal:
- Pilot outcome notes:
- Confidence level:
- Evidence quote or summary:
- Observed customer evidence:
- Internal assumptions:
- Next decision:
- Follow-up owner:
```

## Observed Customer Evidence

Observed evidence comes from direct customer or pilot artifacts:

- Interview statements from ICP buyers, blockers, managers, or learners.
- Pilot metrics computed from stored product records.
- Security, legal, compliance, IT, or procurement objections stated by the
  customer.
- Customer-described workarounds, manual review burden, rollout failures, or
  willingness-to-pay signals.

Observed evidence must be attributed to a source type and date. When evidence is
weak, stale, second-hand, or only from a non-ICP segment, mark confidence as
`low`.

## Internal Assumptions

Internal assumptions are allowed only when labeled. Examples:

- Belief that VP Support owns budget before a buyer confirms it.
- Expected adoption blocker before a customer names it.
- Estimated ROI or manual review savings before pilot metrics exist.
- Assumed willingness to pay based on enthusiasm without budget or procurement
  evidence.

Internal assumptions cannot satisfy Phase 6 exit gates by themselves. Convert an
assumption into observed evidence only after a customer interview, pilot review,
or stored product metric supports it.

## Decision Rules

- Expand a pilot only when observed evidence shows manager-approved workflow
  changes, a named buyer, and a credible paid expansion path.
- Repeat a pilot when workflow-change value appears real but buyer, blocker, or
  willingness-to-pay evidence is still incomplete.
- Pause when activation or completion is weak and the customer cannot name a
  high-priority adoption blocker.
- Reposition when repeated evidence shows the current ICP, buyer, or first use
  case is wrong.
- Collect more evidence when confidence is `low`, evidence is mostly internal
  assumptions, or the source is outside the target market wedge.

## Registry

No discovery records have been accepted yet.
