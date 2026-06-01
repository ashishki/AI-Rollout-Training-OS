export type RiskMeterValues = {
  velocity: number;
  blastRadius: number;
  trust: number;
  evalConfidence: number;
  auditTrail: number;
};

type RiskMetersProps = {
  values: RiskMeterValues;
};

const METER_ROWS = [
  ["Скорость", "velocity", "terminal-meter-fill-safe"],
  ["Радиус ущерба", "blastRadius", "terminal-meter-fill-risk"],
  ["Доверие", "trust", "terminal-meter-fill-warn"],
  ["Уверенность в проверке", "evalConfidence", "terminal-meter-fill-action"],
  ["След проверки", "auditTrail", "terminal-meter-fill-warn"],
] as const;

export function RiskMeters({ values }: RiskMetersProps) {
  return (
    <section aria-label="Риск-метры" className="risk-meter-stack">
      {METER_ROWS.map(([label, key, fillClass]) => {
        const value = values[key];
        return (
          <div className="risk-meter-row" key={key}>
            <div className="mb-2 flex items-center justify-between text-sm">
              <span>{label}</span>
              <span className="text-terminal-muted">{value}</span>
            </div>
            <div
              aria-label={label}
              aria-valuemax={100}
              aria-valuemin={0}
              aria-valuenow={value}
              className="terminal-meter-track"
              role="progressbar"
            >
              <span className={fillClass} style={{ width: `${value}%` }} />
            </div>
          </div>
        );
      })}
    </section>
  );
}
