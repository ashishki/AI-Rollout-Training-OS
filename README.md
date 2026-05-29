# AI Rollout Training OS

AI Rollout Training OS - это система для измеримого внедрения AI в рабочих командах. Проект помогает компании перейти от разовых AI-воркшопов и общих prompt-библиотек к ролевым заданиям, проверяемым guardrail-сценариям, policy-grounded feedback и менеджерскому подтверждению реальных изменений в рабочих процессах.

Статус: active pivot. Проект переориентируется в visual Agent Permission Training Simulator: интерактивные сценарии approve/deny/defer/sandbox для команд, внедряющих AI agents. Детальный план: `docs/PROJECT_PLAN.md`.

## Зачем

Во многих компаниях AI уже "внедряют", но доказательств adoption мало:

- сотрудники проходят обучение, но не применяют AI на реальных задачах;
- менеджеры не видят, какие workflow действительно изменились;
- политика безопасности и SOP живут отдельно от практических заданий;
- feedback по работам не масштабируется без ручной проверки;
- красивые демо не превращаются в повторяемую операционную практику.

Цель проекта - дать пилотной команде короткий, управляемый контур: назначить ролевые миссии, собрать реальные рабочие артефакты, проверить guardrails, дать AI-assisted feedback с цитатами из политики/SOP и получить manager-approved evidence того, что workflow стал лучше и безопаснее.

## Что строим в v1

MVP рассчитан на один company workspace в одном пилоте.

Основные роли:

- Operator / training owner - настраивает role packs, миссии, policy/SOP документы, guardrail quizzes, rubrics и экспорт отчетов.
- Learner - выполняет миссии, отправляет текстовые workflow artifacts, получает feedback и дорабатывает submissions.
- Manager - смотрит прогресс команды, риски, feedback и утверждает повторяемые workflow changes.
- System worker - запускает bounded background jobs для ingestion, feedback, reminders и reports.

Основной workflow:

1. Operator загружает AI policy, SOP, allowed/forbidden use cases, rubrics и role-specific mission content.
2. Система индексирует эти материалы через text-only RAG.
3. Learner выполняет assigned missions и отправляет реальные текстовые артефакты.
4. Система проверяет guardrails и sensitive-data indicators.
5. Feedback service оценивает submission по rubric и policy/SOP evidence.
6. Manager утверждает или отклоняет workflow change.
7. Dashboard и export показывают adoption evidence по cohort.

## Гипотеза

Мы проверяем не то, "повышает ли AI продуктивность вообще". Проверяем более узкую и измеримую гипотезу:

> Если обучение AI строить вокруг ролевых миссий, реальных workflow artifacts, company policy/SOP evidence и manager approval, то пилотная команда сможет за короткий цикл показать измеримые, безопасные и повторяемые AI-assisted workflow changes.

Минимальный success signal для v1 pilot:

- не менее 70% enrolled users завершают хотя бы одну role-specific mission;
- не менее 50% enrolled users отправляют реальный workflow artifact;
- managers утверждают минимум 3 repeatable AI-assisted workflow changes;
- feedback содержит проверяемые citations или возвращает `insufficient_evidence`;
- dashboard metrics считаются из сохраненных records, а не из LLM summary.

## Что хотим проверить

Продуктовая проверка:

- Понятны ли пользователям role-specific missions без постоянного фасилитатора.
- Достаточно ли текстовых submissions для оценки реального применения AI.
- Готовы ли managers использовать dashboard и approvals как adoption evidence.
- Помогают ли guardrail quizzes снизить риск небезопасного AI usage.
- Дает ли система больше практической пользы, чем обычный workshop + prompt library.

Техническая проверка:

- Можно ли надежно ground feedback в company policy/SOP через text-only RAG.
- Работает ли обязательный `insufficient_evidence` путь без hallucinated policy guidance.
- Достаточно ли pgvector + PostgreSQL FTS + reciprocal rank fusion для v1 retrieval.
- Можно ли адаптировать RAG/eval подход из Dream Motif Interpreter без переноса dream-domain логики.
- Укладывается ли feedback generation в приемлемую latency для pilot workflow.

Операционная проверка:

- Можно ли сохранять audit trail для submissions, feedback, approvals, reports и policy snapshots.
- Достаточно ли deterministic state machine для cohort progress, scoring и reports.
- Где проходит граница между AI-assisted feedback и human-owned approval.
- Какие metrics действительно нужны менеджеру для решения "масштабировать / не масштабировать".

## Не цели v1

В v1 проект не пытается:

- заменить тренеров, менеджеров или владельцев политики;
- автоматически сертифицировать сотрудников;
- доказывать общие productivity gains без pilot evidence;
- строить multi-company SaaS;
- индексировать PDF, screenshots, video или spreadsheets;
- запускать autonomous agents или LLM-directed tools;
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

Реализация идет по task graph в `docs/tasks.md`.

Разработка должна идти в nonstop loop: Codex выполняет задачу, проверяет, делает review pass, обновляет state, проходит phase boundary checks и сразу берет следующую задачу. Между фазами нет ручной паузы, если проверки прошли и нет P0/P1 blockers. Остановка допустима только на реальном blocker, требуемом human decision или явной команде pause.

Первый блок:

1. `T01: Project Skeleton`
2. `T02: CI Setup`
3. `T03: First Smoke Tests`

Ключевые RAG/eval задачи:

- `T13: Retrieval Ingestion`
- `T14: Retrieval Query`
- `T22: Retrieval Evaluation`

## Критерий полезности пилота

Пилот считается перспективным, если после первой cohort можно показать:

- реальные submitted artifacts, а не только quiz completion;
- manager-approved workflow changes;
- понятные risk and guardrail outcomes;
- feedback с citations и audit trail;
- повторяемую процедуру запуска следующей cohort.

Если команда завершает обучение, но не создает утвержденных workflow changes, гипотеза не подтверждена.
