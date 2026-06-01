type BadgeToastProps = {
  badges: string[];
  visible: boolean;
};

export function BadgeToast({ badges, visible }: BadgeToastProps) {
  if (!visible || badges.length === 0) {
    return null;
  }

  return (
    <aside aria-label="Badge earned" className="badge-toast">
      <span>Badge earned</span>
      <strong>{formatBadge(badges[0])}</strong>
    </aside>
  );
}

function formatBadge(badge: string) {
  return badge
    .split("_")
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");
}
