# Reference: Codex-Only Workflow

AI Rollout Training OS uses the current Codex session directly and does not launch nested Codex CLI processes.

The active execution model is:

1. The current Codex session reads `docs/prompts/ORCHESTRATOR.md`.
2. The current Codex session selects one task from `docs/tasks.md`.
3. The current Codex session edits files directly, runs tests/lint directly, performs a review pass, and updates state files.
4. The current Codex session advances to the next task or phase immediately when checks pass and no P0/P1 blockers remain.
5. Subagents are optional only when the human explicitly asks for parallel Codex work.

## Why No Nested CLI

Nested CLI execution makes logs harder to inspect, complicates approval boundaries, and is unnecessary when the active operator is already Codex with direct workspace access.

## Practical Rules

- Use direct shell commands for tests, lint, and local inspection.
- Use `apply_patch` for manual file edits.
- Do not spawn external AI processes as implementation workers.
- Keep one-task-at-a-time execution unless the human explicitly requests parallelization.
- Treat review as a separate pass in the same Codex session.
- Do not wait for a separate "continue" prompt between phases; phase boundaries are checkpoints inside the loop.

## Active Prompt

Use:

- `docs/prompts/ORCHESTRATOR.md`

Deprecated / inactive:

- Host-specific slash-command wrappers.
- Nested Codex CLI worker commands.
