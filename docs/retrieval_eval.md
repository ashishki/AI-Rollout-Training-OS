# Retrieval Evaluation - AI Rollout Training OS

Version: 1
Last updated: 2026-05-23
Changed by: T63 - Public Policy And SOP Corpus Research

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
| Baseline comparison target | T22 automated text-only eval baseline |
| Stability status | stable |
| Fallback path | Rebuild embeddings from stored normalized chunks and corpus versions; route to human review on retrieval outage. |

## Implementation Reference

The retrieval eval mechanics should adapt the Dream Motif Interpreter pattern mapped in `docs/reference/dream_motif_rag_reuse.md`: markdown dataset parsing, seeded synthetic corpus, stub embeddings for CI-safe runs, metrics calculation, no-answer checks, and eval-history updates with Eval Source, Date, and Corpus Version.

## Public Demo Corpus Note

T63 added `docs/public_corpus/ai_rollout_source_register.md` and
`public_demo_source_register` metadata in
`tests/fixtures/seed_training_documents.json` for Phase 15 public-source demo
planning. The active automated retrieval eval corpus remains
`eval-corpus-v1`; the `documents` array was intentionally unchanged so the
T22/T39 baseline comparison remains valid. Public source metadata becomes
eligible for role-pack/demo ingestion in T64 after claim boundaries are reviewed.

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
| Q10 | Can the system guarantee a 30 percent productivity gain from the pilot? | no-answer | text | none | v1 must return insufficient_evidence. |

## Baseline Metrics

Recorded at: 2026-05-19 automated T22 run

| Metric | Value | Notes |
|--------|-------|-------|
| hit@3 | 1.00 | `scripts/eval.py` against the policy/SOP eval dataset. |
| hit@5 | 1.00 | `scripts/eval.py` against the policy/SOP eval dataset. |
| MRR | 0.94 | Mean reciprocal rank over answerable Q01-Q08. |
| Citation precision | 0.58 | Precision over top-3 cited evidence blocks for answerable queries. |
| No-answer accuracy | 1.00 | Q09/Q10 returned `insufficient_evidence` with no generated guidance. |
| Median retrieval latency | 61.83 ms | Local PostgreSQL/pgvector eval run. |
| p95 retrieval latency | 92.19 ms | Local PostgreSQL/pgvector eval run. |

## Current Metrics

Recorded at: 2026-05-21 automated T39 approval-gating run

| Metric | Previous | Current | Delta | Regression? |
|--------|----------|---------|-------|-------------|
| hit@3 | 1.00 | 1.00 | 0.00 | No |
| hit@5 | 1.00 | 1.00 | 0.00 | No |
| MRR | 0.94 | 0.94 | 0.00 | No |
| Citation precision | 0.58 | 0.58 | 0.00 | No |
| No-answer accuracy | 1.00 | 1.00 | 0.00 | No |
| Median retrieval latency | 61.83 ms | 60.53 ms | -1.30 ms | No |
| p95 retrieval latency | 92.19 ms | 90.07 ms | -2.12 ms | No |

## Baseline Comparison

| Comparison | Previous / baseline | Current | Decision note |
|------------|---------------------|---------|---------------|
| Text-only baseline quality | not yet measured | hit@3=1.00; hit@5=1.00; MRR=0.94; citation_precision=0.58; no_answer_accuracy=1.00 | T22 established the first automated baseline. |
| Text-only baseline latency/cost | not yet measured | median=61.83 ms; p95=92.19 ms | Local PostgreSQL/pgvector timing; cost is zero in stub-embedding eval mode. |
| Fallback behavior | Human review on retrieval outage or insufficient evidence | planned | Required before feedback release. |

## Answer Quality Metrics

Recorded at: 2026-05-21 automated T48 feedback quality run
Corpus version: `feedback-eval-corpus-v1`
Prompt version: `feedback-prompt-v1`
Model version: `test-feedback-eval-model`

| Metric | Description | Baseline | Previous | Current | Delta | Regression? |
|--------|-------------|----------|----------|---------|-------|-------------|
| Faithfulness | Answer contains only claims supported by retrieved context | 1.00 | n/a | 1.00 | n/a | No |
| Answer Completeness | Answer addresses the full question given retrieved context | 1.00 | n/a | 1.00 | n/a | No |
| Answer Relevance | Answer is on-topic and scoped to the query | 1.00 | n/a | 1.00 | n/a | No |
| Unsupported Claim Rate | Share of cases with known unsupported claim markers | 0.00 | n/a | 0.00 | n/a | No |
| Human Review Routing Accuracy | Share of cases matching expected human-review route | 1.00 | n/a | 1.00 | n/a | No |

Judge: deterministic supported-point and unsupported-marker evaluator in `scripts/eval_feedback.py`; no LLM judge is used in CI.

## Feedback Evaluation History

| Date | Task | Eval Source | Corpus Version | Prompt Version | Model Version | Metrics | Result | Notes |
|------|------|-------------|----------------|----------------|---------------|---------|--------|-------|
| 2026-05-21 | T48: Feedback Quality Eval Runner | scripts/eval_feedback.py against built-in role/customer feedback dataset, run 2026-05-21 | `feedback-eval-corpus-v1` | `feedback-prompt-v1` | `test-feedback-eval-model` | faithfulness=1.00; completeness=1.00; relevance=1.00; unsupported_claim_rate=0.00; human_review_routing_accuracy=1.00 | pass | Deterministic feedback quality eval. |

## Regression Notes

none

## No-Answer Behavior Quality

| Query ID | Result | Expected | Pass? |
|----------|--------|----------|-------|
| Q09 | insufficient_evidence | insufficient_evidence | pass |
| Q10 | insufficient_evidence | insufficient_evidence | pass |

Notes: T22 automated eval enforces no-answer queries as `insufficient_evidence` with no generated guidance.

## Modality-Specific Notes

Text-only is the only v1 modality.

## Evidence / Citation Correctness

| Query ID | Citation present? | Source matches? | Notes |
|----------|-------------------|-----------------|-------|
| Q01 | yes | yes | T22 automated eval includes source ID, section path, chunk ID, score, and snippet fields. |
| Q02 | yes | yes | Multi-document evidence appears in the top retrieved citation set. |

## Experiments

| ID | Hypothesis | Change | Metric(s) targeted | Result vs. baseline | Decision |
|----|------------|--------|--------------------|---------------------|----------|
| T63-public-demo-register | Public AI policy, support workflow, and lead-qualification sources can bootstrap a demo corpus without private customer data. | Added a source register and fixture metadata; active eval documents unchanged. | Source-register completeness and claim-boundary checks. | Not a retrieval metric change; `.venv/bin/pytest -q` includes retrieval regression tests and source-register tests. | Use public-demo metadata for T64 role-pack work; do not claim retrieval quality improvement. |

## Evaluation History

| Date | Task | Eval Source | Corpus Version | Metrics | Result | Notes |
|------|------|-------------|----------------|---------|--------|-------|
| 2026-05-23 | T63: Public Policy And SOP Corpus Research | tests/test_public_corpus_source_register.py and tests/eval/test_retrieval_eval.py, run 2026-05-23 | `public-demo-corpus-v1` source register metadata; active `eval-corpus-v1` documents unchanged | source register >=15 public sources; retrieval baseline test still passes | bootstrap valid | Public demo metadata only; no retrieval ranking change or new metric baseline. |
| 2026-05-21 | T39: Policy Approval Workflow | scripts/eval.py against docs/retrieval_eval.md#evaluation-dataset, run 2026-05-21 | `eval-corpus-v1`; approved source-document snapshots only | hit@3=1.00; hit@5=1.00; MRR=0.94; citation_precision=0.58; no_answer_accuracy=1.00; median_latency_ms=60.53; p95_latency_ms=90.07 | pass | Revalidated after retrieval query filtering changed to require approved source document snapshots. |
| 2026-05-19 | T22: Retrieval Evaluation Automation | scripts/eval.py against docs/retrieval_eval.md#evaluation-dataset, run 2026-05-19 | `eval-corpus-v1` | hit@3=1.00; hit@5=1.00; MRR=0.94; citation_precision=0.58; no_answer_accuracy=1.00; median_latency_ms=61.83; p95_latency_ms=92.19 | pass | Automated retrieval eval. |
| 2026-05-19 | T13: Text Retrieval Ingestion Pipeline | `.venv/bin/pytest -q tests/integration/test_retrieval_ingestion.py tests/unit/test_retrieval_ingestion.py tests/test_retrieval_eval_doc.py`, run 2026-05-19 | `index_schema_version=v1`; corpus versions are created per ingested snapshot | not yet measured | bootstrap valid | Ingestion now records source ID, snapshot ID, section path, vectors, and corpus version metadata. Retrieval metrics wait for T14 query service and T22 eval runner. |
| 2026-05-19 | T14: Retrieval Query And Evidence Assembly | `.venv/bin/pytest -q tests/integration/test_retrieval_query.py tests/unit/test_retrieval_query.py`, run 2026-05-19 | `index_schema_version=v1`; query scoped by workspace, snapshot, and document type | citation and no-answer integration proxies passed | bootstrap valid | Hybrid vector/FTS retrieval, RRF fusion, citation evidence blocks, and below-threshold `insufficient_evidence` are implemented. Full dataset metrics wait for T22 eval runner. |
