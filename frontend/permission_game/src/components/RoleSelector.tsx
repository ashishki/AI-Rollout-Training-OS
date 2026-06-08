import type { GameRoleId, GameRolePack } from "../game/scenarioTypes";

type RoleSelectorProps = {
  roles: GameRolePack[];
  onSelectRole: (roleId: GameRoleId) => void;
};

export function RoleSelector({ roles, onSelectRole }: RoleSelectorProps) {
  return (
    <main className="role-selector-shell">
      <section aria-label="Выбор роли" className="role-selector">
        <div className="role-selector-copy">
          <span className="role-kicker">Тренажёр разрешений / Ship It? Y/N</span>
          <h1>AI-агент просит ход. Ты решаешь границу.</h1>
          <p>
            Три режима для русскоязычной команды: проще для менеджера, плотнее
            для тимлида, глубже для разработчика.
          </p>
        </div>
        <RoleStage />
        <div className="role-card-grid">
          {roles.map((role, index) => (
            <button
              className="role-card"
              key={role.id}
              onClick={() => onSelectRole(role.id)}
              type="button"
            >
              <span className="role-card-index">0{index + 1}</span>
              <span className="role-card-visual" aria-hidden="true">
                <i />
                <i />
                <i />
              </span>
              <span>{role.shortLabel}</span>
              <strong>{role.label}</strong>
              <p>{role.description}</p>
              <small>{role.promise}</small>
            </button>
          ))}
        </div>
      </section>
    </main>
  );
}

function RoleStage() {
  return (
    <div className="role-stage" aria-hidden="true">
      <div className="role-stage-tile tile-a" />
      <div className="role-stage-tile tile-b" />
      <div className="role-stage-tile tile-c" />
      <div className="role-stage-tile tile-d" />
      <div className="role-stage-tile tile-e" />
      <div className="role-stage-line" />
    </div>
  );
}
