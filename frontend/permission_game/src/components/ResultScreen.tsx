import { buildShareText, recommendedNextHabit } from "../game/shareText";

export type FinalResult = {
  score: number;
  title: string;
  demoResult: string;
  prodStatus: string;
  unsafeApprovals: number;
  overblocks: number;
  strongestHabit: string;
  weakestRiskArea: string;
  badges: string[];
};

type ResultScreenProps = {
  result: FinalResult;
};

export function ResultScreen({ result }: ResultScreenProps) {
  const shareText = buildShareText(result);

  return (
    <section aria-label="Final report" className="result-screen">
      <div className="terminal-region-header">
        <span>final report</span>
        <span>{result.prodStatus}</span>
      </div>
      <h1>{result.title}</h1>
      <p className="result-score">{result.score}/100</p>
      <dl className="result-grid">
        <ResultMetric label="Demo result" value={result.demoResult} />
        <ResultMetric label="Prod status" value={result.prodStatus} />
        <ResultMetric label="Unsafe approvals" value={result.unsafeApprovals} />
        <ResultMetric label="Overblocks" value={result.overblocks} />
        <ResultMetric label="Strongest habit" value={result.strongestHabit} />
        <ResultMetric label="Weakest risk area" value={result.weakestRiskArea} />
        <ResultMetric
          label="Recommended next habit"
          value={recommendedNextHabit(result.weakestRiskArea)}
        />
      </dl>
      <div className="result-badges" aria-label="Final badges">
        {result.badges.map((badge) => (
          <span key={badge}>{badge.replaceAll("_", " ")}</span>
        ))}
      </div>
      <textarea aria-label="Share text" readOnly value={shareText} />
    </section>
  );
}

function ResultMetric({ label, value }: { label: string; value: number | string }) {
  return (
    <div>
      <dt>{label}</dt>
      <dd>{value}</dd>
    </div>
  );
}
