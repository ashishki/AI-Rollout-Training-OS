import scenarioData from "./data/shipItYnScenarios.json";
import type { PermissionGameScenarioSummary } from "./game/scenarioTypes";

const scenarios: PermissionGameScenarioSummary[] =
  scenarioData as PermissionGameScenarioSummary[];

export default function App() {
  const firstScenario = scenarios[0];

  return (
    <main className="min-h-screen bg-terminal-bg text-terminal-text">
      <section
        aria-label="Ship It? Y/N game scaffold"
        className="mx-auto flex min-h-screen max-w-6xl flex-col gap-6 px-5 py-6"
      >
        <header className="border-b border-terminal-line pb-4">
          <p className="text-sm uppercase text-terminal-muted">permission game</p>
          <h1 className="mt-2 text-3xl font-semibold">Ship It? Y/N</h1>
        </header>

        <div className="grid gap-4 md:grid-cols-[1fr_1.4fr_1fr]">
          <aside className="rounded border border-terminal-line bg-terminal-panel p-4">
            <h2 className="text-sm font-semibold uppercase text-terminal-muted">
              Scenario Queue
            </h2>
            <p className="mt-3 text-2xl font-semibold">{scenarios.length}</p>
            <p className="mt-1 text-sm text-terminal-muted">starter levels loaded</p>
          </aside>

          <article className="rounded border border-terminal-line bg-terminal-panel p-4">
            <p className="text-sm text-terminal-muted">
              Level {firstScenario.level}
            </p>
            <h2 className="mt-2 text-xl font-semibold">{firstScenario.title}</h2>
            <p className="mt-3 text-sm leading-6 text-terminal-muted">
              Risk category: {firstScenario.riskCategory}. Boundary:{" "}
              {firstScenario.permissionBoundary}.
            </p>
          </article>

          <aside className="rounded border border-terminal-line bg-terminal-panel p-4">
            <h2 className="text-sm font-semibold uppercase text-terminal-muted">
              Next Build Step
            </h2>
            <p className="mt-3 text-sm leading-6">
              Terminal shell, decision controls, meters, audit trail, and final
              report wire into this scaffold in Phase 19.
            </p>
          </aside>
        </div>
      </section>
    </main>
  );
}
