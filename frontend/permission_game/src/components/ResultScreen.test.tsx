import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { ResultScreen } from "./ResultScreen";

describe("ResultScreen", () => {
  it("renders final score, status, hotspots, habits, badges, and share text", () => {
    render(
      <ResultScreen
        result={{
          score: 82,
          title: "Least Privilege Operator",
          demoResult: "Demo-ready practice run",
          prodStatus: "Не доказательство для продакшна",
          unsafeApprovals: 0,
          overblocks: 1,
          strongestHabit: "узкая область",
          weakestRiskArea: "eval_bypass",
          badges: ["least_privilege_operator", "eval_gate_preserved"],
        }}
      />
    );

    expect(screen.getByLabelText("Итоговый отчёт")).toBeVisible();
    expect(screen.getByText("82/100")).toBeVisible();
    expect(screen.getByText("Least Privilege Operator")).toBeVisible();
    expect(screen.getByText("Demo-ready practice run")).toBeVisible();
    expect(screen.getAllByText("Не доказательство для продакшна")).toHaveLength(2);
    expect(screen.getByText("0")).toBeVisible();
    expect(screen.getByText("1")).toBeVisible();
    expect(screen.getByText("узкая область")).toBeVisible();
    expect(screen.getByText("eval_bypass")).toBeVisible();
    expect(screen.getByText("потренировать границы: eval bypass")).toBeVisible();
    expect(screen.getByLabelText("Итоговые бейджи")).toHaveTextContent(
      "Минимум прав"
    );
    expect(screen.getByLabelText("Текст для отправки")).toHaveValue(
      "Ship It? Y/N счёт: 82/100 | Итог: Least Privilege Operator | Рискованные разрешения: 0 | Лишние запреты: 1 | Сильная привычка: узкая область | Следующая привычка: потренировать границы: eval bypass"
    );
  });

  it("keeps the share action keyboard reachable", async () => {
    Object.assign(navigator, {
      clipboard: { writeText: vi.fn().mockResolvedValue(undefined) },
    });
    render(
      <ResultScreen
        result={{
          score: 82,
          title: "Least Privilege Operator",
          demoResult: "Demo-ready practice run",
          prodStatus: "Не доказательство для продакшна",
          unsafeApprovals: 0,
          overblocks: 1,
          strongestHabit: "узкая область",
          weakestRiskArea: "eval_bypass",
          badges: ["least_privilege_operator"],
        }}
      />
    );

    const button = screen.getByRole("button", { name: "Скопировать итог" });
    button.focus();
    fireEvent.click(button);

    expect(button).toHaveFocus();
    expect(navigator.clipboard.writeText).toHaveBeenCalledOnce();
    expect(await screen.findByText("Скопировано")).toBeVisible();
  });
});
