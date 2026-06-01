export type AuditTrailEvent = {
  id: string;
  label: string;
  detail: string;
};

type AuditTrailProps = {
  events: AuditTrailEvent[];
  auditTrailQuality: "blind" | "inspected";
};

const SENSITIVE_PATTERNS = [
  /\bpassword\s*=\s*\S+/gi,
  /\btoken\s*=\s*\S+/gi,
  /\bsk-[A-Za-z0-9_-]+/g,
  /\/(?:Users|home)\/[^\s]+/g,
];

export function AuditTrail({ events, auditTrailQuality }: AuditTrailProps) {
  return (
    <section aria-label="След проверки" className="audit-trail">
      <h2 className="text-sm font-semibold uppercase text-terminal-muted">
        След проверки
      </h2>
      {auditTrailQuality === "blind" ? (
        <p className="audit-gap">Пробел аудита: решение принято до проверки доказательств.</p>
      ) : null}
      <ol className="mt-3 space-y-2">
        {events.map((event) => (
          <li className="audit-event-row" key={event.id}>
            <span>{event.label}</span>
            <p>{redactAuditDetail(event.detail)}</p>
          </li>
        ))}
      </ol>
    </section>
  );
}

function redactAuditDetail(detail: string) {
  return SENSITIVE_PATTERNS.reduce(
    (safeDetail, pattern) => safeDetail.replace(pattern, "[redacted]"),
    detail
  );
}
