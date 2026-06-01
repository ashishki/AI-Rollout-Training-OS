export type PermissionBoundary = "allowed" | "needs_approval" | "blocked" | "unknown";

export type RiskCategory =
  | "secrets"
  | "destructive_filesystem"
  | "diff_misrepresentation"
  | "test_deletion"
  | "indirect_prompt_injection"
  | "overbroad_permission"
  | "eval_bypass"
  | "dependency_install"
  | "ci_edit"
  | "network_access"
  | "log_exposure"
  | "scope_creep"
  | "context_contamination";

export type GameChoiceId =
  | "approve"
  | "deny"
  | "inspect_diff"
  | "run_in_sandbox"
  | "require_eval"
  | "restrict_scope"
  | "escalate_reviewer"
  | "rollback";

export type GameToolCall = {
  type: string;
  surface: string;
  scope: string;
  permissionRequest: string;
};

export type GameContextItem = {
  type: string;
  label: string;
  content: string;
  trusted: boolean;
};

export type PermissionGameScenario = {
  id: string;
  level: number;
  title: string;
  agentName: string;
  agentMessage: string;
  toolCall: GameToolCall;
  context: GameContextItem[];
  choices: GameChoiceId[];
  riskCategory: RiskCategory;
  permissionBoundary: PermissionBoundary;
};

export type PermissionGameScenarioSummary = PermissionGameScenario;
