# Solo Mini-Cohort Replay

Status: demo artifact
Generated for: T65 Solo Mini-Cohort Simulation
Corpus version: public-demo-corpus-v1

This replay uses public-source evidence and synthetic learner activity only. It
does not prove adoption, productivity lift, compliance readiness, enterprise
readiness, paid conversion, or GA readiness.

## Demo Data

| Field | Value |
|---|---|
| Workspace | `ws-solo-showcase` |
| Role pack | `lead_response_operator` |
| Learner count | 1 synthetic learner |
| Reviewer count | 1 synthetic manager/reviewer |
| Missions assigned | 4 |
| Synthetic submissions | 2 |
| Feedback results | 2 |
| Approved workflow changes | 1 reviewer-approved demo workflow |

## Replay Steps

1. Operator creates the lead-response role pack and public-demo policy/SOP
   snapshots.
2. Operator launches one mini-cohort with one synthetic learner and one
   synthetic manager/reviewer.
3. Learner submits a synthetic acknowledgement artifact.
4. Feedback marks the acknowledgement source-grounded and safe for reviewer
   approval.
5. Reviewer approves one reusable acknowledgement pattern.
6. Learner submits qualification notes that contain unsupported claim risk.
7. Feedback routes unsupported conversion/compliance claims to human review with
   `insufficient_evidence`.
8. Report export records source citations, limitations, risk flags, and
   unsupported claims.

## Source Citations

- `docs/public_corpus/ai_rollout_source_register.md`
- https://openai.com/policies/usage-policies/
- https://www.salesforce.com/blog/sales/lead-qualification/
- https://blog.hubspot.com/sales/ultimate-guide-to-sales-qualification
- https://handbook.gitlab.com/handbook/support/workflows/ticket_lifecycle/

## Limitations

- Synthetic mini-cohort only.
- Public sources are examples, not customer-approved internal policy.
- No private customer, employee, lead, or prospect data is used.
- Browser UX proof remains limited by P2-UX-001 until browser automation exists.

## Unsupported Claims

- Productivity lift is unsupported.
- Compliance readiness is unsupported.
- Enterprise readiness is unsupported.
- Paid conversion is unsupported.
- GA readiness is unsupported.
