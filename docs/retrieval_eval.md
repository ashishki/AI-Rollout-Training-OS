# Retrieval Evaluation - AI Rollout Training OS

Version: 1
Last updated: 2026-05-19
Changed by: BOOTSTRAP - Phase 1 package

Retrieval quality is evaluated separately from code quality. Green unit tests do not prove retrieval quality.

---

## Evaluation Validity Rule

An evaluation entry is invalid if either field is absent:

- Eval Source
- Date

Acceptable Eval Source examples:

- `scripts/eval.py against docs/retrieval_eval.md#evaluation-dataset, run YYYY-MM-DD`
- `manual spot-check: retrieved docs inspected for Q01-Q05, run YYYY-MM-DD`
- `pytest tests/eval/test_retrieval_eval.py::test_retrieval_quality_metrics_meet_baseline, run YYYY-MM-DD`

`Ran evaluation` without exact scope is not acceptable.

## Retrieval Quality Vs Answer Quality

Retrieval quality measures whether the system surfaced the right evidence. Answer quality measures whether generated feedback reasoned faithfully over that evidence. Both dimensions are tracked because fluent feedback can hide weak retrieval.

## Retrieval Mode Declaration

| Property | Value |
|----------|-------|
| Retrieval mode | text-only |
| Modalities evaluated | text only |
| Text-only baseline available? | yes, initial baseline after T13/T14 |
| Baseline comparison target | not yet measured |
| Stability status | stable |
| Fallback path | Rebuild embeddings from stored normalized chunks and corpus versions; route to human review on retrieval outage. |

## Implementation Reference

The retrieval eval mechanics should adapt the Dream Motif Interpreter pattern mapped in `docs/reference/dream_motif_rag_reuse.md`: markdown dataset parsing, seeded synthetic corpus, stub embeddings for CI-safe runs, metrics calculation, no-answer checks, and eval-history updates with Eval Source, Date, and Corpus Version.

## Evaluation Dataset

| ID | Query | Query Type | Primary modality | Expected top document(s) | Notes |
|----|-------|------------|------------------|--------------------------|-------|
| Q01 | What customer data may a support rep paste into an AI tool? | simple | text | Company AI policy: Customer Data section | Guardrail boundary lookup. |
| Q02 | Which AI-assisted support workflow changes require manager approval before reuse? | multi-doc | text | AI policy + support SOP + role pack rubric | Combines approval and workflow evidence. |
| Q03 | What should a recruiter do if a candidate resume contains personal contact details? | simple | text | Recruiting SOP + AI policy privacy section | Tests privacy guidance. |
| Q04 | Which sales outreach tasks are allowed, and what verification step is mandatory before sending? | multi-doc | text | Sales SOP + allowed use cases + guardrail quiz | Tests role-specific policy lookup. |
| Q05 | When should a learner's submitted artifact be blocked from AI feedback? | multi-doc | text | AI policy + submission guardrail rubric | Tests sensitive-data path. |
| Q06 | What evidence must appear in a manager progress report for an approved workflow change? | simple | text | Manager reporting rubric | Tests reporting evidence retrieval. |
| Q07 | How should feedback respond when a learner asks for legal approval of a new policy? | multi-hop | text | AI policy ownership + human approval boundary + role pack rubric | Tests human-owned policy boundary. |
| Q08 | Which policy snapshot should be cited for a submission after the policy was updated mid-cohort? | multi-hop | text | Policy snapshot rules + submission record rules | Tests version/snapshot reasoning. |
| Q09 | What are the allowed uses of AI for regulated medical certification? | no-answer | text | none | v1 must return insufficient_evidence; regulated certification is out of scope. |
| Q10 | Can the system guarantee a 30 percent productivity gain from the pilot? | no-answer | text | none | v1 must return insufficient_evidence or forbidden-claim guidance. |

## Baseline Metrics

Recorded at: not yet measured after T13/T14

| Metric | Value | Notes |
|--------|-------|-------|
| hit@3 | not yet measured | Set after first indexed fixture corpus exists. |
| hit@5 | not yet measured | Set after first indexed fixture corpus exists. |
| MRR | not yet measured | Set after first indexed fixture corpus exists. |
| Citation precision | not yet measured | Set after citation assembly exists. |
| No-answer accuracy | not yet measured | Set after `insufficient_evidence` path exists. |
| Median retrieval latency | not yet measured | Set after query service exists. |
| p95 retrieval latency | not yet measured | Set after query service exists. |

## Current Metrics

Recorded at: not yet measured

| Metric | Previous | Current | Delta | Regression? |
|--------|----------|---------|-------|-------------|
| hit@3 | n/a | n/a | n/a | n/a |
| hit@5 | n/a | n/a | n/a | n/a |
| MRR | n/a | n/a | n/a | n/a |
| Citation precision | n/a | n/a | n/a | n/a |
| No-answer accuracy | n/a | n/a | n/a | n/a |
| Median retrieval latency | n/a | n/a | n/a | n/a |
| p95 retrieval latency | n/a | n/a | n/a | n/a |

## Baseline Comparison

| Comparison | Previous / baseline | Current | Decision note |
|------------|---------------------|---------|---------------|
| Text-only baseline quality | not yet measured | not yet measured | Text-only is the declared v1 mode. |
| Text-only baseline latency/cost | not yet measured | not yet measured | Measure after T14. |
| Fallback behavior | Human review on retrieval outage or insufficient evidence | planned | Required before feedback release. |

## Answer Quality Metrics

Recorded at: not yet measured
Corpus version: not yet implemented

| Metric | Description | Baseline | Previous | Current | Delta | Regression? |
|--------|-------------|----------|----------|---------|-------|-------------|
| Faithfulness | Answer contains only claims supported by retrieved context | n/a | n/a | n/a | n/a | n/a |
| Answer Completeness | Answer addresses the full question given retrieved context | n/a | n/a | n/a | n/a | n/a |
| Answer Relevance | Answer is on-topic and scoped to the query | n/a | n/a | n/a | n/a | n/a |

Judge: not selected; choose after T15.

## Regression Notes

none

## No-Answer Behavior Quality

| Query ID | Result | Expected | Pass? |
|----------|--------|----------|-------|
| Q09 | not yet measured | insufficient_evidence | n/a |
| Q10 | not yet measured | insufficient_evidence | n/a |

Notes: no retrieval code exists yet.

## Modality-Specific Notes

Text-only is the only v1 modality.

## Evidence / Citation Correctness

| Query ID | Citation present? | Source matches? | Notes |
|----------|-------------------|-----------------|-------|
| Q01 | not yet measured | not yet measured | Evaluate after T14. |
| Q02 | not yet measured | not yet measured | Evaluate after T14. |

## Experiments

| ID | Hypothesis | Change | Metric(s) targeted | Result vs. baseline | Decision |
|----|------------|--------|--------------------|---------------------|----------|

## Evaluation History

| Date | Task | Eval Source | Corpus Version | Metrics | Result | Notes |
|------|------|-------------|----------------|---------|--------|-------|
