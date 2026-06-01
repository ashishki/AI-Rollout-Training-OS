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

export type PermissionGameScenarioSummary = {
  id: string;
  level: number;
  title: string;
  riskCategory: RiskCategory;
  permissionBoundary: PermissionBoundary;
};
