import { useState } from "react";
import { TerminalLayout } from "./components/TerminalLayout";
import { RoleSelector } from "./components/RoleSelector";
import { ROLE_PACKS, rolePackById } from "./game/rolePacks";
import type { GameRoleId } from "./game/scenarioTypes";

export default function App() {
  const [selectedRoleId, setSelectedRoleId] = useState<GameRoleId | null>(null);

  if (!selectedRoleId) {
    return <RoleSelector roles={ROLE_PACKS} onSelectRole={setSelectedRoleId} />;
  }

  const selectedRole = rolePackById(selectedRoleId);

  return (
    <TerminalLayout
      onChangeRole={() => setSelectedRoleId(null)}
      role={selectedRole}
      scenarios={selectedRole.scenarios}
    />
  );
}
