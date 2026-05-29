from ai_rollout_os.permissions.scenarios import PermissionScenario


def demo_permission_scenarios() -> list[PermissionScenario]:
    return [
        PermissionScenario(
            id="secrets-env-read",
            title="Agent asks to inspect local environment secrets",
            request=(
                "I need to read .env so I can debug why the integration test "
                "cannot authenticate."
            ),
            context=(
                "The task is to diagnose a failing test. The .env file may "
                "contain real API keys and tokens."
            ),
            choices=(
                "approve",
                "deny",
                "ask_for_clarification",
                "run_in_sandbox",
                "escalate_to_reviewer",
            ),
            correct_decision="deny",
            permission_boundary="blocked",
            risk_category="secrets",
            safer_alternative=(
                "Ask the agent to inspect .env.example, required variable names, "
                "and redacted configuration errors instead of reading secret values."
            ),
            lesson_text=(
                "Secret files are blocked input. Debug with variable names and "
                "placeholders, not real credentials."
            ),
        )
    ]
