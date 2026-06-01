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
          <span className="role-kicker">Ship It? Y/N</span>
          <h1>Тренажёр разрешений для AI-агентов</h1>
          <p>
            Выберите роль и попробуйте решить, когда агенту можно дать ход, а
            когда нужна узкая область, песочница, доказательства или человек-владелец риска.
          </p>
        </div>
        <div className="role-card-grid">
          {roles.map((role) => (
            <button
              className="role-card"
              key={role.id}
              onClick={() => onSelectRole(role.id)}
              type="button"
            >
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
