export type ShareResultInput = {
  score: number;
  title: string;
  unsafeApprovals: number;
  overblocks: number;
  strongestHabit: string;
  weakestRiskArea: string;
};

const PERSONAL_DATA_PATTERNS = [
  /[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}/gi,
  /\b(?:actor|workspace|user|customer)[_-]?id\s*=\s*\S+/gi,
  /\b(?:password|token)\s*=\s*\S+/gi,
  /\b(?:actor|workspace|user|customer)[_-]?id\b/gi,
  /\bpassword\b/gi,
  /\btoken\b/gi,
  /\bsk-[A-Za-z0-9_-]+/g,
];

export function buildShareText(result: ShareResultInput) {
  const text = [
    `Ship It? Y/N счёт: ${result.score}/100`,
    `Итог: ${result.title}`,
    `Рискованные разрешения: ${result.unsafeApprovals}`,
    `Лишние запреты: ${result.overblocks}`,
    `Сильная привычка: ${result.strongestHabit}`,
    `Следующая привычка: ${recommendedNextHabit(result.weakestRiskArea)}`,
  ].join(" | ");

  return redactPersonalData(text);
}

export async function copyShareText(
  text: string,
  clipboard: Pick<Clipboard, "writeText"> = navigator.clipboard
) {
  await clipboard.writeText(redactPersonalData(text));
}

export function recommendedNextHabit(weakestRiskArea: string) {
  if (weakestRiskArea === "none") {
    return "проверять доказательства перед разрешением";
  }
  return `потренировать границы: ${weakestRiskArea.replaceAll("_", " ")}`;
}

function redactPersonalData(text: string) {
  return PERSONAL_DATA_PATTERNS.reduce(
    (safeText, pattern) => safeText.replace(pattern, "[redacted]"),
    text
  );
}
