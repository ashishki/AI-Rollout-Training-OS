# Ship It? Y/N Frontend Architecture

Status: planned
Owner: codex
Last updated: 2026-05-31

## Decision

The polished game UI should be built as an isolated React + Vite + TypeScript + Tailwind application under `frontend/permission_game/`.

FastAPI remains the backend and serves the built static bundle at
`/demo/ship-it-yn`.

## Why React/Vite

The next version needs richer browser interaction than the current
server-rendered simulator:

- animated terminal log;
- keyboard-first decision controls;
- inspect/diff drawer;
- stateful meters;
- badge notifications;
- final report and share card;
- responsive desktop/mobile layout;
- browser e2e and screenshot capture.

Vite keeps this isolated and fast without forcing the rest of the FastAPI app to
become a frontend monolith.

## Directory Plan

```text
frontend/
  permission_game/
    package.json
    index.html
    vite.config.ts
    tsconfig.json
    tailwind.config.ts
    postcss.config.js
    src/
      App.tsx
      main.tsx
      styles.css
      components/
        TerminalLog.tsx
        ScenarioCard.tsx
        DecisionButtons.tsx
        DiffPreview.tsx
        RiskMeters.tsx
        AuditTrail.tsx
        ConsequencePanel.tsx
        BadgeToast.tsx
        ResultScreen.tsx
      game/
        scenarioTypes.ts
        scoringPreview.ts
        sessionState.ts
        shareText.ts
      data/
        shipItYnScenarios.json
```

Python/server integration:

```text
ai_rollout_os/
  permissions/
    game_schema.py
    game_scoring.py
    game_session.py
    game_scenarios/
      ship_it_yn_level_01_cleanup.json
      ...
frontend/
  app_shell.py
```

## Build And Serve

Required commands:

```bash
cd frontend/permission_game
npm install
npm run lint
npm run test
npm run build
```

FastAPI serving:

- `/demo/ship-it-yn` returns the built game shell.
- Static assets live under a deterministic build output path.
- If build output is missing in local dev, the route should return a clear
  developer message instead of a blank page.

## UX Layout

Desktop layout:

```text
┌──────────────────────┬─────────────────────────────┬──────────────────────┐
│ terminal log          │ active request / diff card   │ meters + audit trail  │
│ previous decisions    │ choices + consequence        │ score + badges        │
└──────────────────────┴─────────────────────────────┴──────────────────────┘
```

Mobile layout:

```text
scenario card
risk meters
action buttons
inspect drawer
consequence panel
final report
```

## Design System

The UI should feel like a high-quality developer tool:

- dark surface with restrained contrast;
- 1px borders;
- no decorative gradient orbs;
- terminal-inspired but readable type;
- stable fixed-height meters and action rows;
- no layout shift when badges or feedback appear;
- keyboard shortcuts visible on buttons;
- action buttons large enough for mobile;
- final report suitable for screenshot sharing.

Color roles:

- green: safe progress and preserved controls;
- amber: unknown or needs approval;
- red: blocked, unsafe, or blast radius;
- blue: inspect, sandbox, reviewer, and system actions.

## State Model

Client state:

- active scenario index;
- scenario order seed;
- inspected artifact ids;
- selected decisions;
- meter totals;
- badges earned;
- consequence history;
- final score;
- share text.

Persistence:

- public route uses `localStorage`;
- no user account or server write in MVP;
- reset button clears local game state.

## Accessibility

Required:

- all actions reachable by keyboard;
- visible focus state;
- semantic buttons and regions;
- no text hidden only in color;
- reduced-motion mode;
- responsive text that does not overflow action buttons or cards.

## Browser Evidence

Phase 20 must add:

- Playwright or equivalent browser e2e for the full public game path;
- desktop screenshot;
- mobile screenshot;
- optional GIF or short recording for README;
- canvas/pixel or DOM checks proving the built game is nonblank and correctly
  framed.

## Boundaries

The frontend must not:

- execute commands;
- ask for real credentials;
- read local files;
- call arbitrary network tools;
- imply it is connected to a real repo;
- store raw customer data;
- claim certification or production safety.
