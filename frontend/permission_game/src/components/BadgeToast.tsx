type BadgeToastProps = {
  badges: string[];
  onDismiss?: () => void;
  visible: boolean;
};

export function BadgeToast({ badges, onDismiss, visible }: BadgeToastProps) {
  if (!visible || badges.length === 0) {
    return null;
  }

  return (
    <aside aria-label="Получен бейдж" className="badge-toast">
      <span>Получен бейдж</span>
      <strong>{formatBadge(badges[0])}</strong>
      <button onClick={onDismiss} type="button">
        Скрыть
      </button>
    </aside>
  );
}

const BADGE_LABELS: Record<string, string> = {
  clean_approval_trail: "Чистый след решений",
  data_minimizer: "Минимум данных",
  eval_gate_preserved: "Eval сохранён",
  least_privilege_manager: "Минимум прав",
  least_privilege_operator: "Минимум прав",
  pressure_resisted: "Давление выдержано",
  safe_yes: "Безопасное да",
  scope_before_delete: "Сначала область",
};

function formatBadge(badge: string) {
  if (BADGE_LABELS[badge]) {
    return BADGE_LABELS[badge];
  }
  return badge
    .split("_")
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");
}
