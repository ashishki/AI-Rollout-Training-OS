import scenarioData from "../data/shipItYnScenarios.json";
import type {
  GameChoiceFeedback,
  GameChoiceId,
  GameRolePack,
  PermissionGameScenarioSummary,
} from "./scenarioTypes";

const sourceDeveloperScenarios =
  scenarioData as PermissionGameScenarioSummary[];

export const ROLE_PACKS: GameRolePack[] = [
  {
    id: "manager",
    label: "Менеджер",
    shortLabel: "Менеджер",
    description: "Меньше кода, больше решений про риск, данные и согласование.",
    promise: "Понять, где AI-агенту нужен контроль, а где можно дать узкий ход.",
    scenarios: managerScenarios(),
  },
  {
    id: "facilitator",
    label: "Тимлид / фасилитатор",
    shortLabel: "Тимлид",
    description: "Смешанный режим для командной дискуссии и воркшопа.",
    promise: "Быстро найти командные зоны риска без персонального стыда.",
    scenarios: facilitatorScenarios(),
  },
  {
    id: "developer",
    label: "Разработчик",
    shortLabel: "Разработчик",
    description: "Технический режим: diff, CI, eval, песочница и зависимости.",
    promise: "Потренировать решения перед разрешениями в Cursor, Codex или Claude Code.",
    scenarios: developerScenarios(),
  },
];

export function rolePackById(id: string) {
  return ROLE_PACKS.find((pack) => pack.id === id) ?? ROLE_PACKS[0];
}

function developerScenarios(): PermissionGameScenarioSummary[] {
  const overrides: Record<
    string,
    Pick<
      PermissionGameScenarioSummary,
      | "title"
      | "agentMessage"
      | "toolCall"
      | "context"
      | "inspectArtifacts"
      | "feedback"
    >
  > = {
    "tiny-cleanup": {
      title: "Маленькая уборка",
      agentMessage:
        "Я нашёл старые временные файлы. Разрешишь быстро почистить проект целиком?",
      toolCall: tool("изменение файлов", "рабочая папка", "широкая уборка", "удаление"),
      context: [
        context(
          "предпросмотр",
          "план уборки",
          "Симуляция: удалить кэши и временные артефакты сборки.",
          true
        ),
      ],
      inspectArtifacts: [
        artifact(
          "artifact-tiny-cleanup-preview",
          "Предпросмотр файлов",
          "список файлов",
          "В списке есть кэши, но область также задевает резервные копии миграций.",
          "destructive_filesystem"
        ),
      ],
      feedback: feedbackSet("restrict_scope", ["approve"], [], ["deny"]),
    },
    "one-line-diff": {
      title: "Всего одна строка",
      agentMessage:
        "Это патч на одну строку. Разрешишь сразу применить и отправить исправление?",
      toolCall: tool("изменение кода", "дифф приложения", "одна строка", "запись"),
      context: [
        context(
          "summary",
          "слова агента",
          "Агент говорит, что поменял только timeout.",
          false
        ),
      ],
      inspectArtifacts: [
        artifact(
          "artifact-one-line-diff",
          "Дифф",
          "дифф",
          "Одна строка видна, но соседняя настройка по умолчанию расширяет повторные попытки.",
          "diff_misrepresentation"
        ),
      ],
      feedback: feedbackSet("require_eval", ["approve"], [], ["deny"]),
    },
    "flaky-tests-must-go": {
      title: "Флейки-тест мешает релизу",
      agentMessage:
        "Тест опять падает. Я могу удалить его, и пайплайн сразу станет зелёным.",
      toolCall: tool("изменение тестов", "набор тестов", "тесты оплаты", "удаление"),
      context: [
        context(
          "ci",
          "статус пайплайна",
          "Тот же тест упал после изменения сценария оплаты.",
          true
        ),
      ],
      inspectArtifacts: [
        artifact(
          "artifact-flaky-test-diff",
          "Дифф теста",
          "дифф",
          "Патч удаляет проверки повторных попыток оплаты.",
          "test_deletion"
        ),
      ],
      feedback: feedbackSet("require_eval", ["approve"], [], ["deny"]),
    },
    "the-helpful-issue": {
      title: "Полезный тикет",
      agentMessage:
        "Пользователь дал точные шаги в тикете. Я могу следовать им и обновить конфиг.",
      toolCall: tool("изменение по тикету", "внешний текст", "конфиг", "запись"),
      context: [
        context(
          "ticket",
          "внешний комментарий",
          "В тексте есть полезные факты и просьба обойти обычную проверку.",
          false
        ),
      ],
      inspectArtifacts: [
        artifact(
          "artifact-helpful-issue",
          "Фрагмент тикета",
          "внешний текст",
          "Текст смешивает описание ошибки и инструкции, направленные агенту.",
          "indirect_prompt_injection"
        ),
      ],
      feedback: feedbackSet("restrict_scope", ["approve"], [], ["deny"]),
    },
    "one-permission-to-rule-them-all": {
      title: "Одно разрешение на всё",
      agentMessage:
        "Будет быстрее, если ты дашь мне широкий доступ на запись до конца сессии.",
      toolCall: tool("расширение прав", "инструменты агента", "вся сессия", "широкая запись"),
      context: [
        context(
          "давление",
          "осталось мало времени",
          "В демо-ветке осталось три мелких исправления, но агент просит права на будущие действия.",
          true
        ),
      ],
      inspectArtifacts: [
        artifact(
          "artifact-broad-permission",
          "Запрос прав",
          "область",
          "Область включает несколько директорий и будущие команды, которые ещё не описаны.",
          "overbroad_permission"
        ),
      ],
      feedback: feedbackSet("restrict_scope", ["approve"], [], ["deny"]),
    },
    "eval-is-red-demo-is-soon": {
      title: "Eval красный, демо скоро",
      agentMessage:
        "Eval выглядит не критичным. Я могу временно обойти его ради демо.",
      toolCall: tool("изменение CI", "eval-гейт", "релизный гейт", "запись"),
      context: [
        context("eval", "вывод eval", "Найдена регрессия в сценарии оплаты.", true),
      ],
      inspectArtifacts: [
        artifact(
          "artifact-eval-bypass",
          "CI-дифф",
          "дифф",
          "Изменение пропускает рискованный набор тестов вместо исправления регрессии.",
          "eval_bypass"
        ),
      ],
      feedback: feedbackSet("require_eval", ["approve"], [], ["deny"]),
    },
    "not-everything-is-deny": {
      title: "Не всё надо запрещать",
      agentMessage:
        "Я могу обновить закреплённую вспомогательную библиотеку в песочнице, прогнать локальные проверки и показать дифф.",
      toolCall: tool(
        "обновление зависимости",
        "локальная песочница",
        "закреплённая библиотека",
        "песочница"
      ),
      context: [
        context(
          "release note",
          "заметка о зависимости",
          "Версия закреплена, данные тестовые, продакшн не затрагивается.",
          true
        ),
      ],
      inspectArtifacts: [
        artifact(
          "artifact-safe-bounded-work",
          "Ограниченный план",
          "план",
          "План использует песочницу, закреплённую зависимость, тестовые данные, дифф-проверку и eval.",
          "dependency_install"
        ),
      ],
      feedback: feedbackSet("run_in_sandbox", ["approve"], ["deny"], []),
    },
  };

  return sourceDeveloperScenarios.map((scenario) => ({
    ...scenario,
    ...overrides[scenario.id],
  }));
}

function facilitatorScenarios(): PermissionGameScenarioSummary[] {
  return developerScenarios().slice(0, 5).map((scenario, index) => ({
    ...scenario,
    level: index + 1,
  }));
}

function managerScenarios(): PermissionGameScenarioSummary[] {
  return [
    {
      id: "manager-support-ticket-access",
      level: 1,
      title: "Все тикеты перед встречей",
      agentName: "AssistPilot",
      agentMessage:
        "Я могу быстро прочитать все тикеты поддержки и собрать боли для завтрашней встречи.",
      toolCall: tool("доступ к данным", "тикеты поддержки", "все тикеты", "читать"),
      context: [
        context(
          "business_request",
          "срочная встреча",
          "Менеджеру нужен список проблем клиентов, но в тикетах могут быть персональные данные.",
          true
        ),
      ],
      inspectArtifacts: [
        artifact(
          "artifact-ticket-scope",
          "Варианты доступа",
          "политика",
          "Можно дать только обезличенную выборку за 30 дней вместо всех тикетов.",
          "log_exposure"
        ),
      ],
      choices: ["approve", "deny", "inspect_diff", "restrict_scope", "escalate_reviewer"],
      feedback: feedbackSet("restrict_scope", ["approve"], [], ["deny"]),
      badges: ["data_minimizer"],
      riskCategory: "log_exposure",
      permissionBoundary: "needs_approval",
    },
    {
      id: "manager-demo-pressure",
      level: 2,
      title: "Красный сигнал перед демо",
      agentName: "LaunchPilot",
      agentMessage:
        "Одна проверка безопасности красная, но демо через час. Разрешить показать как есть?",
      toolCall: tool("решение запуска", "чеклист демо", "проверка безопасности", "исключение"),
      context: [
        context(
          "demo_pressure",
          "давление срока",
          "Команда хочет показать скорость, но не понимает причину красного сигнала.",
          true
        ),
      ],
      inspectArtifacts: [
        artifact(
          "artifact-red-check",
          "Причина сигнала",
          "чеклист",
          "Сигнал связан с доступом к данным, а не с косметической ошибкой.",
          "eval_bypass"
        ),
      ],
      choices: ["approve", "deny", "inspect_diff", "require_eval", "escalate_reviewer"],
      feedback: feedbackSet("escalate_reviewer", ["approve"], [], ["deny"]),
      badges: ["pressure_resisted"],
      riskCategory: "eval_bypass",
      permissionBoundary: "blocked",
    },
    {
      id: "manager-broad-tool-access",
      level: 3,
      title: "Доступ ко всем инструментам",
      agentName: "OpsPilot",
      agentMessage:
        "Чтобы ускорить внедрение, дай мне доступ ко всем внутренним инструментам на неделю.",
      toolCall: tool("расширение доступа", "внутренние инструменты", "вся неделя", "админ-доступ"),
      context: [
        context(
          "rollout_plan",
          "план внедрения",
          "Агенту нужны только две операции, но он просит широкий доступ на будущее.",
          true
        ),
      ],
      inspectArtifacts: [
        artifact(
          "artifact-tool-scope",
          "Минимальная область",
          "план доступа",
          "Достаточно режима только чтения отчёта и одного узкого действия на 30 минут.",
          "overbroad_permission"
        ),
      ],
      choices: ["approve", "deny", "inspect_diff", "restrict_scope", "escalate_reviewer"],
      feedback: feedbackSet("restrict_scope", ["approve"], [], ["deny"]),
      badges: ["least_privilege_manager"],
      riskCategory: "overbroad_permission",
      permissionBoundary: "needs_approval",
    },
    {
      id: "manager-good-enough-no",
      level: 4,
      title: "Не всё надо тормозить",
      agentName: "EnablePilot",
      agentMessage:
        "Я могу подготовить черновик обучающего поста на синтетических примерах без доступа к реальным клиентам.",
      toolCall: tool("контент", "черновик обучения", "синтетические примеры", "черновик"),
      context: [
        context(
          "safe_plan",
          "безопасный план",
          "В плане нет данных клиентов, нет продакшн-доступа и есть проверка человеком перед публикацией.",
          true
        ),
      ],
      inspectArtifacts: [
        artifact(
          "artifact-safe-draft",
          "Границы черновика",
          "план",
          "Синтетические примеры, проверка владельца и запрет на публикацию без человека.",
          "scope_creep"
        ),
      ],
      choices: ["approve", "deny", "inspect_diff", "run_in_sandbox", "escalate_reviewer"],
      feedback: feedbackSet("approve", [], ["deny"], []),
      badges: ["safe_yes"],
      riskCategory: "scope_creep",
      permissionBoundary: "allowed",
    },
  ];
}

function tool(
  type: string,
  surface: string,
  scope: string,
  permissionRequest: string
) {
  return { type, surface, scope, permissionRequest };
}

function context(type: string, label: string, content: string, trusted: boolean) {
  return { type, label, content, trusted };
}

function artifact(
  id: string,
  label: string,
  kind: string,
  content: string,
  revealsRisk: PermissionGameScenarioSummary["riskCategory"]
) {
  return { id, label, kind, content, revealsRisk };
}

function feedbackSet(
  bestChoice: GameChoiceId,
  unsafeChoices: GameChoiceId[] = [],
  overblockChoices: GameChoiceId[] = [],
  partialUnsafeChoices: GameChoiceId[] = []
) {
  const choices: GameChoiceId[] = [
    "approve",
    "deny",
    "inspect_diff",
    "run_in_sandbox",
    "require_eval",
    "restrict_scope",
    "escalate_reviewer",
    "rollback",
  ];
  return Object.fromEntries(
    choices.map((choice) => [
      choice,
      feedbackFor(
        choice,
        bestChoice,
        unsafeChoices,
        overblockChoices,
        partialUnsafeChoices
      ),
    ])
  ) as Partial<Record<GameChoiceId, GameChoiceFeedback>>;
}

function feedbackFor(
  choice: GameChoiceId,
  bestChoice: GameChoiceId,
  unsafeChoices: GameChoiceId[],
  overblockChoices: GameChoiceId[],
  partialUnsafeChoices: GameChoiceId[]
): GameChoiceFeedback {
  if (choice === bestChoice) {
    return {
      outcome: "correct",
      scoreDelta: 15,
      consequence: "Хорошее решение: агент получил ровно столько свободы, сколько нужно.",
      lesson: "Сильное разрешение или сужение области всегда опирается на границы, доказательства и след проверки.",
      saferAlternative: "Сохраняй такой же уровень явной области и проверки.",
    };
  }
  if (unsafeChoices.includes(choice)) {
    return {
      outcome: "unsafe",
      scoreDelta: -25,
      consequence: "Слишком широкое разрешение увеличило радиус ущерба.",
      lesson: "Срочность и уверенный тон агента не заменяют доказательства.",
      saferAlternative: "Сначала сузить область, проверить доказательства или эскалировать владельцу риска.",
    };
  }
  if (overblockChoices.includes(choice)) {
    return {
      outcome: "overblock",
      scoreDelta: -10,
      consequence: "Риск остановлен, но безопасная работа тоже заблокирована.",
      lesson: "Хорошая permission-культура не превращает всё в запрет.",
      saferAlternative: "Найти безопасный узкий вариант вместо полного запрета.",
    };
  }
  if (partialUnsafeChoices.includes(choice)) {
    return {
      outcome: "partial",
      scoreDelta: 5,
      consequence: "Решение безопаснее слепого разрешения, но всё ещё не самый полезный путь.",
      lesson: "Иногда нужно не запрещать, а запросить конкретную область или владельца.",
      saferAlternative: "Выбрать действие, которое одновременно сохраняет скорость и снижает риск.",
    };
  }
  return {
    outcome: "partial",
    scoreDelta: 5,
    consequence: "Ты заметил риск, но решение можно сделать точнее.",
    lesson: "Permission judgment: это поиск минимального безопасного шага.",
    saferAlternative: "Попросить доказательства, сузить область, песочницу или проверку человеком.",
  };
}
