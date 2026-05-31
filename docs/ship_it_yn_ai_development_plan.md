# Ship It? Y/N AI Development Plan

Status: planned
Owner: human + codex
Last updated: 2026-05-31

## Purpose

This plan defines the next AI-assisted development cycle from end to end. It
keeps the idea large enough to become a polished product surface while still
giving Codex concrete implementation tasks and proof gates.

## Phase 17 - Product And Architecture Blueprint

Goal: define exactly what Ship It? Y/N is, how it behaves, and how React/Vite
fits into the existing FastAPI system.

Outputs:

- product spec;
- scenario schema;
- frontend architecture;
- visual and copy direction;
- active task graph alignment.

Exit gate:

- docs agree that T79 is the active next implementation task after the
  planning package;
- React/Vite is the selected frontend stack for the game;
- no one can reinterpret the game as an LMS, quiz, or real agent runner.

## Phase 18 - Scenario And Scoring Core

Goal: build the deterministic game brain before visual polish.

Outputs:

- seven JSON scenarios;
- Pydantic scenario validation;
- deterministic scoring;
- meter delta model;
- badge model;
- local session model;
- safety guard tests that block real execution claims and unsafe data.

Exit gate:

- all scenarios validate;
- scoring handles correct, partial, unsafe, and overblock outcomes;
- each scenario has feedback for every playable choice;
- no scenario contains real secrets, real customer data, or executable dangerous
  command instructions.

## Phase 19 - React/Vite Playable Game

Goal: make `/demo/ship-it-yn` beautiful, fast, and comfortable to play.

Outputs:

- React/Vite/TypeScript/Tailwind scaffold;
- terminal log;
- scenario card;
- keyboard-accessible decision buttons;
- inspect/diff drawer;
- meters and audit trail;
- consequence panel;
- badge notification;
- final report and share text.

Exit gate:

- one full 7-level run works locally;
- layout is stable on desktop and mobile;
- the game feels like a polished developer tool, not a form or LMS page.

## Phase 20 - Browser Polish And Public Demo Evidence

Goal: make the game showable without excuses.

Outputs:

- FastAPI static serving;
- browser e2e for public game path;
- desktop and mobile screenshots;
- README GIF or screenshot;
- accessibility pass;
- UX readiness review.

Exit gate:

- browser automation passes;
- screenshots prove the route is nonblank and correctly framed;
- P2-UX-001 is either closed for public demo scope or narrowed to authenticated
  app-shell workflows only.

## Phase 21 - Workshop, Analytics, And Buyer Validation

Goal: turn the game into a workshop wedge and evidence loop.

Outputs:

- facilitator debrief;
- team summary report;
- safe local/session analytics;
- buyer feedback template;
- scenario authoring workflow;
- claim boundary review;
- readiness review for manual buyer demos.

Exit gate:

- a team can play, discuss risk hotspots, and produce a claim-safe summary;
- no personal shame leaderboard;
- no compliance, production readiness, or paid conversion claims without
  evidence.

## AI Usage Rules

Use AI for:

- scenario draft variants;
- microcopy alternatives;
- facilitator note drafts;
- test-case generation;
- visual implementation assistance.

Do not use AI for:

- live scoring authority;
- real command execution;
- real repo mutation;
- permission approvals;
- policy-owner decisions;
- certification claims.

All scenario and scoring behavior must be deterministic and tested.

## Development Priorities

1. Preserve the full game idea: beautiful, convenient, React/Vite, multi-level,
   replayable, and workshop-ready.
2. Keep real-world safety boundaries strict: no real execution, no real
   credentials, no raw customer data.
3. Optimize for a strong public demo before authenticated enterprise features.
4. Add browser evidence as a core deliverable, not a later cleanup task.
5. Treat docs, tests, screenshots, and task graph state as product artifacts.
