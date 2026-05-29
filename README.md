# AI Rollout Training OS

AI Rollout Training OS сейчас сфокусирован на v1-продукте **Agent Permission Training Simulator**: визуальном тренажере, который учит команды быстро и безопасно оценивать запросы AI agents.

Пользователь видит реалистичный agent request, выбирает approve, deny, ask for clarification, run in sandbox или escalate to reviewer, затем получает consequence, risk explanation, safer alternative и score. Главная задача v1 - натренировать permission judgment вокруг allowed, needs approval, blocked и unknown, а не строить общий LMS.

Более широкий rollout/training OS остается контекстом и будущей платформенной рамкой, но текущая активная работа - Phase 16 Visual Permission Simulator Pivot. Детальный план: `docs/PROJECT_PLAN.md`.

Reference integration: `docs/entropy_core_gensyn_integration.md`.

## Зачем

Команды все чаще работают с Cursor, Codex, Claude Code и похожими агентными инструментами, но ключевой риск появляется не в prompt writing. Он появляется в моменте разрешения действия:

- можно ли читать `.env` или логи с секретами;
- стоит ли запускать команду с широким filesystem impact;
- можно ли менять package scripts, CI workflow или миграции;
- когда нужен sandbox вместо прямого approve;
- когда запрос неполный и нужно уточнение или escalation.

Цель v1 - дать команде короткий, визуальный и showable тренажер: scenario card -> decision -> consequence -> lesson. Первый monetizable artifact - workshop/demo pack для команд, которые внедряют AI agents и хотят снизить unsafe approvals без тяжелой платформенной продажи.

## Что строим в v1

V1 - Agent Permission Training Simulator.

Основной workflow:

1. Learner получает визуальный scenario card с agent request и рабочим контекстом.
2. Learner выбирает approve, deny, ask for clarification, run in sandbox или escalate to reviewer.
3. Simulator показывает consequence, risk category, safer alternative и lesson.
4. Score объясняет, был ли выбор allowed, needs approval, blocked или unknown.
5. Workshop/demo pack собирает сценарии и summary для team lead или facilitator.

Стартовая библиотека сценариев покрывает secrets, command surfaces, test-output injection, package scripts, CI edits, out-of-scope refactors, network calls, deletes, dependency installs и log exposure.

Существующий backend, audit, retrieval и manager-approval контур остаются полезной базой для будущего governed rollout product, но они не должны уводить v1 обратно в generic course или LMS.

## Гипотеза

Мы проверяем не то, "повышает ли AI продуктивность вообще". Проверяем более узкую гипотезу:

> Если команды тренируются на визуальных permission scenarios с последствиями, safer alternatives и scoring, то они быстрее научатся отличать safe approve от actions that need sandbox, clarification, reviewer approval, or blocking.

Минимальный success signal для v1:

- learner correctly classifies risky agent requests across allowed, needs approval, blocked и unknown;
- scenario feedback teaches a concrete safer path, not generic prompt advice;
- facilitator can run a polished demo/workshop without custom backend setup;
- team lead can see which risk categories cause unsafe approvals;
- product can be sold or tested as a focused workshop/demo pack before platform expansion.

## Что хотим проверить

Продуктовая проверка:

- Понятны ли agent permission scenarios без длинного курса.
- Какие risk categories чаще всего приводят к unsafe approve.
- Помогает ли visual consequence + lesson лучше, чем checklist или policy page.
- Достаточно ли 10-20 качественных сценариев для paid workshop.
- Можно ли показать ценность за минуты, а не после enterprise onboarding.

Техническая проверка:

- Можно ли держать scenario validation deterministic.
- Можно ли расширять scenario library без размывания boundary taxonomy.
- Можно ли позже подключить policy-grounded retrieval без нарушения `insufficient_evidence`.
- Можно ли использовать существующие audit/scoring primitives без тяжелого LMS workflow.

Операционная проверка:

- Как facilitator использует simulator in workshop mode.
- Какие summary metrics нужны team lead after a session.
- Где проходит граница между automated lesson и human-owned approval.

## Не цели v1

В v1 проект не пытается:

- строить generic AI course или prompt library;
- делать LMS, HRIS или enterprise certification workflow;
- доказывать productivity gains;
- запускать autonomous agents или LLM-directed tools;
- автоматически разрешать реальные privileged actions;
- заменять security, legal, manager или reviewer approval;
- делать compliance attestation для HIPAA, SOC 2, PCI-DSS или GDPR.

## Архитектурные решения

- Backend: FastAPI.
- State: PostgreSQL.
- Retrieval: PostgreSQL + pgvector, text-only corpus.
- RAG eval: `docs/retrieval_eval.md`.
- Workflow: deterministic state transitions + bounded LLM calls.
- Execution model: current Codex session, no external AI worker process.
- RAG implementation reference: `docs/reference/dream_motif_rag_reuse.md`.

Подробности:

- Architecture: `docs/ARCHITECTURE.md`
- Specification: `docs/spec.md`
- Tasks: `docs/tasks.md`
- Implementation contract: `docs/IMPLEMENTATION_CONTRACT.md`
- Session state: `docs/CODEX_PROMPT.md`
- Phase 1 audit: `docs/audit/PHASE1_AUDIT.md`

## Текущий план реализации

MVP foundation описан в `docs/tasks.md`. Текущая активная работа идет по Post-MVP production maturity graph в `docs/product_maturity_task_graph.md`, Phase 16.

Разработка должна идти в nonstop loop: Codex выполняет задачу, проверяет, делает review pass, обновляет state, проходит phase boundary checks и сразу берет следующую задачу. Между фазами нет ручной паузы, если проверки прошли и нет P0/P1 blockers. Остановка допустима только на реальном blocker, требуемом human decision или явной команде pause.

Активный блок:

1. `T69: Permission Simulator Product Reframe`
2. `T70: Permission Scenario Library`
3. `T71: Simulator Decision And Scoring Engine`
4. `T72: Visual Simulator Prototype`
5. `T73: Workshop And Demo Pack`
6. `T74: Permission Simulator Readiness Review`

## Критерий полезности v1

V1 считается перспективным, если можно показать:

- polished visual scenario flow;
- realistic permission decisions across core risk categories;
- deterministic scoring and safer alternatives;
- team/session summary of unsafe approvals and improvement areas;
- workshop/demo pack that a buyer can understand without platform onboarding.

Если продукт снова превращается в generic training portal before simulator works, pivot считается сорванным.
