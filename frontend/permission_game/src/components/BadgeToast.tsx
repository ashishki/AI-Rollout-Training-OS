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
    <aside aria-label="Badge earned" className="badge-toast">
      <span>Badge earned</span>
      <strong>{formatBadge(badges[0])}</strong>
      <button onClick={onDismiss} type="button">
        Dismiss
      </button>
    </aside>
  );
}

function formatBadge(badge: string) {
  return badge
    .split("_")
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");
}
