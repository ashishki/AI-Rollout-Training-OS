import scenarioData from "./data/shipItYnScenarios.json";
import { TerminalLayout } from "./components/TerminalLayout";
import type { PermissionGameScenarioSummary } from "./game/scenarioTypes";

const scenarios: PermissionGameScenarioSummary[] =
  scenarioData as PermissionGameScenarioSummary[];

export default function App() {
  return <TerminalLayout scenarios={scenarios} />;
}
