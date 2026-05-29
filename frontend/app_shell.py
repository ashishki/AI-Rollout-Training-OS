from collections.abc import Generator
from datetime import date
from html import escape
from urllib.parse import parse_qs

from ai_rollout_os.auth.dependencies import get_settings_from_app
from ai_rollout_os.auth.permissions import require_permission
from ai_rollout_os.auth.tokens import ActorContext
from ai_rollout_os.db.models import MissionAssignment
from ai_rollout_os.permissions import score_decision
from ai_rollout_os.permissions.demo import demo_permission_scenarios
from ai_rollout_os.permissions.scenarios import PermissionScenario
from ai_rollout_os.reporting.dashboard import DashboardService
from ai_rollout_os.reporting.reports import ReportService
from ai_rollout_os.retrieval.document_models import DocumentCreate
from ai_rollout_os.retrieval.document_service import DocumentService
from ai_rollout_os.submissions.models import ManagerApprovalCreate, SubmissionCreate
from ai_rollout_os.submissions.review_service import ManagerReviewService
from ai_rollout_os.submissions.service import SubmissionService
from ai_rollout_os.training.cohort_models import CohortCreate
from ai_rollout_os.training.cohort_service import CohortService
from ai_rollout_os.training.guardrail_models import (
    AnswerChoice,
    GuardrailQuestionCreate,
    GuardrailQuizCreate,
    QuizAnswer,
    QuizSubmission,
)
from ai_rollout_os.training.guardrail_service import GuardrailService
from ai_rollout_os.training.schemas import MissionCreate, RolePackCreate
from ai_rollout_os.training.service import RolePackService
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.orm import Session

router = APIRouter()
APP_SHELL = Depends(require_permission("app.shell.view"))
OPERATOR_VIEW = Depends(require_permission("app.operator.view"))
LEARNER_VIEW = Depends(require_permission("app.learner.view"))
MANAGER_VIEW = Depends(require_permission("app.manager.view"))
CREATE_DOCUMENT = Depends(require_permission("app.operator.documents.create"))
CREATE_GUARDRAIL = Depends(require_permission("app.operator.guardrail_quizzes.create"))
CREATE_ROLE_PACK = Depends(require_permission("app.operator.role_packs.create"))
CREATE_MISSION = Depends(require_permission("app.operator.missions.create"))
LAUNCH_ROLE_PACK = Depends(require_permission("app.operator.role_packs.launch"))
CREATE_COHORT = Depends(require_permission("app.operator.cohorts.create"))
LAUNCH_COHORT = Depends(require_permission("app.operator.cohorts.launch"))
SUBMIT_GUARDRAIL = Depends(
    require_permission("app.learner.guardrail_submissions.create")
)
CREATE_SUBMISSION = Depends(require_permission("app.learner.submissions.create"))
APPROVE_SUBMISSION = Depends(require_permission("app.manager.submissions.approve"))
CREATE_REPORT = Depends(require_permission("app.manager.reports.create"))
APP_SETTINGS = Depends(get_settings_from_app)


ROLE_NAVIGATION = {
    "operator": [
        ("Policies", "/app/operator/policies"),
        ("Role Packs", "/app/operator/role-packs"),
        ("Missions", "/app/operator/missions"),
        ("Guardrails", "/app/operator/guardrails"),
        ("Cohorts", "/app/operator/cohorts"),
    ],
    "manager": [
        ("Review Queue", "/app/manager/review-queue"),
        ("Dashboard", "/app/manager/dashboard"),
        ("Reports", "/app/manager/reports"),
        ("Approvals", "/app/manager/approvals"),
    ],
    "learner": [
        ("Assignments", "/app/learner/assignments"),
        ("Guardrail Quiz", "/app/learner/guardrails"),
        ("Submissions", "/app/learner/submissions"),
        ("Feedback", "/app/learner/feedback"),
    ],
}


def get_session(request: Request) -> Generator[Session]:
    session_factory = request.app.state.session_factory
    with session_factory() as session:
        yield session


DB_SESSION = Depends(get_session)


@router.get("/app", response_class=HTMLResponse)
def app_shell(actor: ActorContext = APP_SHELL) -> HTMLResponse:
    navigation = ROLE_NAVIGATION.get(actor.role)
    if navigation is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )
    return HTMLResponse(_shell_html(role=actor.role, navigation=navigation))


@router.get("/app/permission-simulator", response_class=HTMLResponse)
def permission_simulator(actor: ActorContext = APP_SHELL) -> HTMLResponse:
    scenario = _permission_scenarios()[0]
    return HTMLResponse(
        _permission_simulator_html(
            role=actor.role,
            scenario=scenario,
            form_action="/app/permission-simulator/decisions",
        )
    )


@router.post("/app/permission-simulator/decisions", response_class=HTMLResponse)
async def submit_permission_decision(
    request: Request,
    actor: ActorContext = APP_SHELL,
) -> HTMLResponse:
    form = await _form_values(request)
    scenario_id = _form_value(form, "scenario_id")
    decision = _form_value(form, "decision")
    scenarios = {scenario.id: scenario for scenario in _permission_scenarios()}
    scenario = scenarios.get(scenario_id)
    if scenario is None:
        raise HTTPException(status_code=404, detail="Scenario not found")
    score = score_decision(scenario, decision)
    return HTMLResponse(
        _permission_result_html(role=actor.role, scenario=scenario, score=score)
    )


# Public by D-012: this route renders only static demo scenario content and does
# not read workspace, user, policy, submission, or customer data.
@router.get("/demo/permission-simulator", response_class=HTMLResponse)
def public_permission_simulator_demo() -> HTMLResponse:
    scenario = _permission_scenarios()[0]
    return HTMLResponse(
        _permission_simulator_html(
            role="demo",
            scenario=scenario,
            form_action="/demo/permission-simulator/decisions",
        )
    )


public_permission_simulator_demo.public_design_decision = (
    "D-012 static public permission simulator demo"
)


# Public by D-012: this route scores only static demo scenario choices and does
# not mutate durable state or read workspace data.
@router.post("/demo/permission-simulator/decisions", response_class=HTMLResponse)
async def submit_public_permission_demo_decision(request: Request) -> HTMLResponse:
    form = await _form_values(request)
    scenario_id = _form_value(form, "scenario_id")
    decision = _form_value(form, "decision")
    scenarios = {scenario.id: scenario for scenario in _permission_scenarios()}
    scenario = scenarios.get(scenario_id)
    if scenario is None:
        raise HTTPException(status_code=404, detail="Scenario not found")
    score = score_decision(scenario, decision)
    return HTMLResponse(
        _permission_result_html(role="demo", scenario=scenario, score=score)
    )


submit_public_permission_demo_decision.public_design_decision = (
    "D-012 static public permission simulator demo"
)


@router.get("/app/operator/{section}", response_class=HTMLResponse)
def operator_admin_section(
    section: str,
    actor: ActorContext = OPERATOR_VIEW,
) -> HTMLResponse:
    allowed_sections = {"policies", "role-packs", "missions", "guardrails", "cohorts"}
    if section not in allowed_sections:
        raise HTTPException(status_code=404, detail="Section not found")
    return HTMLResponse(_operator_admin_html(section=section, role=actor.role))


@router.get("/app/learner/{section}", response_class=HTMLResponse)
def learner_section(
    section: str,
    actor: ActorContext = LEARNER_VIEW,
    session: Session = DB_SESSION,
) -> HTMLResponse:
    allowed_sections = {"assignments", "guardrails", "submissions", "feedback"}
    if section not in allowed_sections:
        raise HTTPException(status_code=404, detail="Section not found")
    assignments = session.scalars(
        select(MissionAssignment).where(
            MissionAssignment.workspace_id == actor.workspace_id,
            MissionAssignment.learner_id == actor.actor_id,
        )
    ).all()
    return HTMLResponse(
        _learner_html(section=section, role=actor.role, assignments=assignments)
    )


@router.get("/app/manager/{section}", response_class=HTMLResponse)
def manager_section(
    section: str,
    request: Request,
    actor: ActorContext = MANAGER_VIEW,
    session: Session = DB_SESSION,
) -> HTMLResponse:
    allowed_sections = {"review-queue", "dashboard", "reports", "approvals"}
    if section not in allowed_sections:
        raise HTTPException(status_code=404, detail="Section not found")
    submissions = []
    dashboard = None
    if section in {"review-queue", "approvals"}:
        submissions = ManagerReviewService(session).list_submissions(
            actor=actor,
            learner_id=request.query_params.get("learner_id"),
            mission_id=request.query_params.get("mission_id"),
            feedback_status=request.query_params.get("feedback_status"),
            guardrail_status=request.query_params.get("guardrail_status"),
            risk_flag=request.query_params.get("risk_flag"),
        )
    if section == "dashboard" and request.query_params.get("cohort_id"):
        dashboard = DashboardService(session).cohort_dashboard(
            cohort_id=str(request.query_params["cohort_id"]),
            workspace_id=actor.workspace_id,
        )
    return HTMLResponse(
        _manager_html(
            section=section,
            role=actor.role,
            submissions=submissions,
            dashboard=dashboard,
        )
    )


@router.post("/app/operator/documents", response_class=HTMLResponse)
async def create_document_from_ui(
    request: Request,
    actor: ActorContext = CREATE_DOCUMENT,
    session: Session = DB_SESSION,
) -> HTMLResponse:
    form = await _form_values(request)
    try:
        payload = DocumentCreate(
            title=_form_value(form, "title"),
            document_type=_form_value(form, "document_type"),
            body_text=_form_value(form, "body_text"),
            effective_date=date.fromisoformat(_form_value(form, "effective_date")),
        )
        document = DocumentService(session).create_document(payload, actor)
        session.commit()
    except (HTTPException, ValidationError, ValueError) as exc:
        session.rollback()
        return _safe_error_response(exc)
    return HTMLResponse(
        _operator_result_html(
            title="Document created",
            body=(
                f'<p data-document-id="{escape(document.logical_document_id)}">'
                f"{escape(document.title)} snapshot {escape(document.snapshot_id)}</p>"
            ),
        ),
        status_code=201,
    )


@router.post("/app/operator/guardrail-quizzes", response_class=HTMLResponse)
async def create_guardrail_quiz_from_ui(
    request: Request,
    actor: ActorContext = CREATE_GUARDRAIL,
    session: Session = DB_SESSION,
) -> HTMLResponse:
    form = await _form_values(request)
    try:
        payload = GuardrailQuizCreate(
            title=_form_value(form, "title"),
            pass_threshold=int(_form_value(form, "pass_threshold")),
            questions=[
                GuardrailQuestionCreate(
                    id=_form_value(form, "question_id"),
                    question_text=_form_value(form, "question_text"),
                    answer_choices=[
                        AnswerChoice(
                            id="safe",
                            text=_form_value(form, "safe_choice_text"),
                        ),
                        AnswerChoice(
                            id="unsafe",
                            text=_form_value(form, "unsafe_choice_text"),
                        ),
                    ],
                    correct_answer_ids=[_form_value(form, "correct_answer_id")],
                    explanation=_form_value(form, "explanation"),
                )
            ],
        )
        quiz, _questions = GuardrailService(session).create_quiz(payload, actor)
        session.commit()
    except (HTTPException, ValidationError, ValueError) as exc:
        session.rollback()
        return _safe_error_response(exc)
    return HTMLResponse(
        _operator_result_html(
            title="Guardrail quiz created",
            body=f'<p data-quiz-id="{escape(quiz.id)}">{escape(quiz.title)}</p>',
        ),
        status_code=201,
    )


@router.post("/app/operator/role-packs", response_class=HTMLResponse)
async def create_role_pack_from_ui(
    request: Request,
    actor: ActorContext = CREATE_ROLE_PACK,
    session: Session = DB_SESSION,
) -> HTMLResponse:
    form = await _form_values(request)
    try:
        payload = RolePackCreate(
            role=_form_value(form, "role"),
            title=_form_value(form, "title"),
        )
        role_pack = RolePackService(session).create_draft_role_pack(payload, actor)
        session.commit()
    except (HTTPException, ValidationError, ValueError) as exc:
        session.rollback()
        return _safe_error_response(exc)
    return HTMLResponse(
        _operator_result_html(
            title="Role pack created",
            body=(
                f'<p data-role-pack-id="{escape(role_pack.id)}">'
                f"{escape(role_pack.title)}</p>"
            ),
        ),
        status_code=201,
    )


@router.post("/app/operator/missions", response_class=HTMLResponse)
async def create_mission_from_ui(
    request: Request,
    actor: ActorContext = CREATE_MISSION,
    session: Session = DB_SESSION,
) -> HTMLResponse:
    form = await _form_values(request)
    try:
        payload = MissionCreate(
            objective=_form_value(form, "objective"),
            instructions=_form_value(form, "instructions"),
            artifact_type=_form_value(form, "artifact_type"),
            rubric_id=_form_value(form, "rubric_id"),
            guardrail_quiz_id=_form_value(form, "guardrail_quiz_id"),
        )
        mission = RolePackService(session).add_mission(
            _form_value(form, "role_pack_id"), payload, actor
        )
        session.commit()
    except (HTTPException, ValidationError, ValueError) as exc:
        session.rollback()
        return _safe_error_response(exc)
    return HTMLResponse(
        _operator_result_html(
            title="Mission created",
            body=(
                f'<p data-mission-id="{escape(mission.id)}">'
                f"{escape(mission.objective)}</p>"
            ),
        ),
        status_code=201,
    )


@router.post("/app/operator/role-packs/launch", response_class=HTMLResponse)
async def launch_role_pack_from_ui(
    request: Request,
    actor: ActorContext = LAUNCH_ROLE_PACK,
    session: Session = DB_SESSION,
) -> HTMLResponse:
    form = await _form_values(request)
    try:
        role_pack = RolePackService(session).launch(
            _form_value(form, "role_pack_id"), actor
        )
        session.commit()
    except (HTTPException, ValidationError, ValueError) as exc:
        session.rollback()
        return _safe_error_response(exc)
    return HTMLResponse(
        _operator_result_html(
            title="Role pack launched",
            body=(
                f'<p data-role-pack-id="{escape(role_pack.id)}">'
                f"{escape(role_pack.launch_status)}</p>"
            ),
        )
    )


@router.post("/app/operator/cohorts", response_class=HTMLResponse)
async def create_cohort_from_ui(
    request: Request,
    actor: ActorContext = CREATE_COHORT,
    session: Session = DB_SESSION,
) -> HTMLResponse:
    form = await _form_values(request)
    try:
        payload = CohortCreate(
            role_pack_id=_form_value(form, "role_pack_id"),
            role_pack_version=int(_form_value(form, "role_pack_version")),
            manager_id=_form_value(form, "manager_id"),
            learner_ids=_learner_ids(_form_value(form, "learner_ids")),
            start_date=date.fromisoformat(_form_value(form, "start_date")),
            due_date=date.fromisoformat(_form_value(form, "due_date")),
        )
        cohort = CohortService(session).create_cohort(payload, actor)
        session.commit()
    except (HTTPException, ValidationError, ValueError) as exc:
        session.rollback()
        return _safe_error_response(exc)
    return HTMLResponse(
        _operator_result_html(
            title="Cohort created",
            body=f'<p data-cohort-id="{escape(cohort.id)}">{escape(cohort.status)}</p>',
        ),
        status_code=201,
    )


@router.post("/app/operator/cohorts/launch", response_class=HTMLResponse)
async def launch_cohort_from_ui(
    request: Request,
    actor: ActorContext = LAUNCH_COHORT,
    session: Session = DB_SESSION,
) -> HTMLResponse:
    form = await _form_values(request)
    try:
        assignments = CohortService(session).launch_cohort(
            _form_value(form, "cohort_id"), actor
        )
        session.commit()
    except (HTTPException, ValidationError, ValueError) as exc:
        session.rollback()
        return _safe_error_response(exc)
    return HTMLResponse(
        _operator_result_html(
            title="Cohort launched",
            body=f'<p data-assignment-count="{len(assignments)}">active</p>',
        )
    )


@router.post("/app/learner/guardrail-submissions", response_class=HTMLResponse)
async def submit_guardrail_from_ui(
    request: Request,
    actor: ActorContext = SUBMIT_GUARDRAIL,
    session: Session = DB_SESSION,
) -> HTMLResponse:
    form = await _form_values(request)
    try:
        payload = QuizSubmission(
            answers=[
                QuizAnswer(
                    question_id=_form_value(form, "question_id"),
                    answer_ids=_csv_values(_form_value(form, "answer_ids")),
                )
            ]
        )
        result = GuardrailService(session).score_submission(
            _form_value(form, "quiz_id"), payload, actor
        )
        session.commit()
    except (HTTPException, ValidationError, ValueError) as exc:
        session.rollback()
        return _safe_error_response(exc)
    return HTMLResponse(
        _learner_result_html(
            title="Guardrail quiz submitted",
            body=(
                f'<p data-quiz-result-id="{escape(result.id)}" '
                f'data-passed="{str(result.passed).lower()}">'
                f"Score {result.score}</p>"
            ),
        ),
        status_code=201,
    )


@router.post("/app/learner/submissions", response_class=HTMLResponse)
async def submit_artifact_from_ui(
    request: Request,
    actor: ActorContext = CREATE_SUBMISSION,
    session: Session = DB_SESSION,
) -> HTMLResponse:
    form = await _form_values(request)
    try:
        payload = SubmissionCreate(
            assignment_id=_form_value(form, "assignment_id"),
            artifact_text=_form_value(form, "artifact_text"),
            policy_snapshot_id=_form_value(form, "policy_snapshot_id"),
            rubric_id=_form_value(form, "rubric_id"),
        )
        submission = SubmissionService(session).create_submission(
            _form_value(form, "mission_id"), payload, actor
        )
        session.commit()
    except (HTTPException, ValidationError, ValueError) as exc:
        session.rollback()
        return _safe_error_response(exc)
    artifact_preview = (
        "[REDACTED]"
        if submission.redaction_status == "flagged"
        else "Artifact submitted"
    )
    return HTMLResponse(
        _learner_result_html(
            title="Submission received",
            body=(
                f'<p data-submission-id="{escape(submission.id)}" '
                f'data-review-state="{escape(submission.review_state)}" '
                f'data-redaction-status="{escape(submission.redaction_status)}">'
                f"{escape(artifact_preview)}</p>"
            ),
        ),
        status_code=201,
    )


@router.post("/app/manager/submissions/approve", response_class=HTMLResponse)
async def approve_submission_from_ui(
    request: Request,
    actor: ActorContext = APPROVE_SUBMISSION,
    session: Session = DB_SESSION,
) -> HTMLResponse:
    form = await _form_values(request)
    try:
        payload = ManagerApprovalCreate(
            approval_note=_form_value(form, "approval_note"),
            approved_workflow_change=_form_value(form, "approved_workflow_change"),
        )
        item = ManagerReviewService(session).approve_submission(
            submission_id=_form_value(form, "submission_id"),
            payload=payload,
            actor=actor,
        )
        session.commit()
    except (HTTPException, ValidationError, ValueError) as exc:
        session.rollback()
        return _safe_error_response(exc)
    return HTMLResponse(
        _manager_result_html(
            title="Submission approved",
            body=(
                f'<p data-submission-id="{escape(item.id)}" '
                f'data-approval-status="{escape(item.approval_status)}">'
                f"{escape(item.approved_workflow_change or '')}</p>"
            ),
        )
    )


@router.post("/app/manager/reports", response_class=HTMLResponse)
async def create_report_from_ui(
    request: Request,
    actor: ActorContext = CREATE_REPORT,
    session: Session = DB_SESSION,
) -> HTMLResponse:
    form = await _form_values(request)
    try:
        report = ReportService(session).create_report(
            cohort_id=_form_value(form, "cohort_id"), actor=actor
        )
        session.commit()
    except (HTTPException, ValidationError, ValueError) as exc:
        session.rollback()
        return _safe_error_response(exc)
    return HTMLResponse(
        _manager_result_html(
            title="Report created",
            body=(
                f'<p data-report-id="{escape(report.id)}">version {report.version}</p>'
            ),
        ),
        status_code=201,
    )


def _shell_html(*, role: str, navigation: list[tuple[str, str]]) -> str:
    nav_items = "\n".join(
        (
            '<a class="nav-link" '
            f'href="{escape(href)}" data-nav-item="{escape(label)}">'
            f"{escape(label)}</a>"
        )
        for label, href in navigation
    )
    role_label = escape(role.title())
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>AI Rollout Training OS</title>
    <style>
      :root {{
        color-scheme: light;
        --ink: #17202a;
        --muted: #64707d;
        --line: #d8dee5;
        --panel: #f7f9fb;
        --accent: #0f766e;
      }}
      * {{ box-sizing: border-box; }}
      body {{
        margin: 0;
        color: var(--ink);
        background: #ffffff;
        font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont,
          "Segoe UI", sans-serif;
      }}
      .app-shell {{
        min-height: 100vh;
        display: grid;
        grid-template-columns: minmax(208px, 248px) 1fr;
      }}
      .sidebar {{
        border-right: 1px solid var(--line);
        background: var(--panel);
        padding: 20px 16px;
      }}
      .brand {{
        margin: 0 0 18px;
        font-size: 18px;
        font-weight: 700;
      }}
      .role {{
        margin: 0 0 16px;
        color: var(--muted);
        font-size: 13px;
      }}
      .nav {{
        display: grid;
        gap: 6px;
      }}
      .nav-link {{
        min-height: 36px;
        display: flex;
        align-items: center;
        padding: 8px 10px;
        border-radius: 6px;
        color: var(--ink);
        text-decoration: none;
        font-weight: 600;
      }}
      .nav-link:focus,
      .nav-link:hover {{
        outline: 2px solid transparent;
        background: #e8f3f1;
        color: var(--accent);
      }}
      .workspace {{
        padding: 24px;
      }}
      .workspace h1 {{
        margin: 0 0 8px;
        font-size: 24px;
      }}
      .workspace p {{
        max-width: 720px;
        margin: 0;
        color: var(--muted);
      }}
      @media (max-width: 720px) {{
        .app-shell {{ grid-template-columns: 1fr; }}
        .sidebar {{ border-right: 0; border-bottom: 1px solid var(--line); }}
      }}
    </style>
  </head>
  <body>
    <main class="app-shell" data-authenticated="true" data-role="{escape(role)}">
      <aside class="sidebar" aria-label="{role_label} navigation">
        <p class="brand">AI Rollout Training OS</p>
        <p class="role">{role_label}</p>
        <nav class="nav" aria-label="Primary navigation">
          {nav_items}
        </nav>
      </aside>
      <section class="workspace" aria-labelledby="workspace-title">
        <h1 id="workspace-title">{role_label} Workspace</h1>
        <p>Use the navigation to manage the current pilot workflow.</p>
      </section>
    </main>
  </body>
</html>"""


def _learner_html(
    *,
    section: str,
    role: str,
    assignments: list[MissionAssignment],
) -> str:
    title = section.replace("-", " ").title()
    assignment_items = "\n".join(
        (
            f'<li data-assignment-id="{escape(assignment.id)}" '
            f'data-mission-id="{escape(assignment.mission_template_id)}">'
            f"{escape(assignment.status)}</li>"
        )
        for assignment in assignments
    )
    forms = "\n".join(
        [
            '<form method="post" action="/app/learner/guardrail-submissions" '
            'data-form="guardrail-submit"></form>',
            '<form method="post" action="/app/learner/submissions" '
            'data-form="artifact-submit"></form>',
        ]
    )
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{escape(title)} - AI Rollout Training OS</title>
  </head>
  <body>
    <main data-role="{escape(role)}" data-learner-section="{escape(section)}">
      <h1>{escape(title)}</h1>
      <ul data-assignment-list="true">
        {assignment_items}
      </ul>
      {forms}
      <section data-feedback-status="pending">Feedback status</section>
    </main>
  </body>
</html>"""


def _manager_html(
    *,
    section: str,
    role: str,
    submissions,
    dashboard,
) -> str:
    title = section.replace("-", " ").title()
    submission_items = "\n".join(
        (
            f'<li data-submission-id="{escape(item.id)}" '
            f'data-feedback-status="{escape(item.feedback_status)}" '
            f'data-guardrail-status="{escape(item.guardrail_status)}">'
            f"{escape(item.learner_id)} {escape(item.approval_status)}</li>"
        )
        for item in submissions
    )
    dashboard_html = ""
    if dashboard is not None:
        dashboard_html = (
            f'<section data-dashboard-cohort-id="{escape(dashboard.cohort_id)}" '
            f'data-completion-rate="{dashboard.completion_rate}" '
            f'data-submission-rate="{dashboard.submission_rate}" '
            f'data-approved-workflow-count="{dashboard.approved_workflow_count}">'
            "Dashboard metrics</section>"
        )
    forms = "\n".join(
        [
            '<form method="post" action="/app/manager/submissions/approve" '
            'data-form="manager-approval"></form>',
            '<form method="post" action="/app/manager/reports" '
            'data-form="manager-report"></form>',
        ]
    )
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{escape(title)} - AI Rollout Training OS</title>
  </head>
  <body>
    <main data-role="{escape(role)}" data-manager-section="{escape(section)}">
      <h1>{escape(title)}</h1>
      <ul data-manager-submission-list="true">
        {submission_items}
      </ul>
      {dashboard_html}
      {forms}
    </main>
  </body>
</html>"""


def _operator_admin_html(*, section: str, role: str) -> str:
    title = section.replace("-", " ").title()
    forms = "\n".join(
        [
            '<form method="post" action="/app/operator/documents" '
            'data-form="document"></form>',
            '<form method="post" action="/app/operator/guardrail-quizzes" '
            'data-form="guardrail"></form>',
            '<form method="post" action="/app/operator/role-packs" '
            'data-form="role-pack"></form>',
            '<form method="post" action="/app/operator/missions" '
            'data-form="mission"></form>',
            '<form method="post" action="/app/operator/role-packs/launch" '
            'data-form="role-pack-launch"></form>',
            '<form method="post" action="/app/operator/cohorts" '
            'data-form="cohort"></form>',
            '<form method="post" action="/app/operator/cohorts/launch" '
            'data-form="cohort-launch"></form>',
        ]
    )
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{escape(title)} - AI Rollout Training OS</title>
  </head>
  <body>
    <main data-role="{escape(role)}" data-operator-admin-section="{escape(section)}">
      <h1>{escape(title)}</h1>
      {forms}
    </main>
  </body>
</html>"""


def _permission_scenarios() -> list[PermissionScenario]:
    return demo_permission_scenarios()


def _permission_simulator_html(
    *, role: str, scenario: PermissionScenario, form_action: str
) -> str:
    buttons = "\n".join(
        (
            '<button type="submit" name="decision" '
            f'value="{escape(choice)}" data-decision-action="{escape(choice)}">'
            f"{escape(choice.replace('_', ' ').title())}</button>"
        )
        for choice in scenario.choices
    )
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Agent Permission Simulator</title>
    <style>
      body {{
        margin: 0;
        color: #17202a;
        background: #f7f9fb;
        font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont,
          "Segoe UI", sans-serif;
      }}
      main {{
        min-height: 100vh;
        display: grid;
        grid-template-columns: minmax(260px, 34vw) 1fr;
      }}
      .scenario-rail {{
        background: #101820;
        color: #f8fafc;
        padding: 28px;
      }}
      .scenario-rail h1 {{
        margin: 0 0 12px;
        font-size: 28px;
      }}
      .scenario-rail p {{
        margin: 0;
        color: #cbd5e1;
        line-height: 1.5;
      }}
      .workspace {{
        padding: 28px;
      }}
      .scenario-card {{
        max-width: 820px;
        border: 1px solid #d8dee5;
        border-radius: 8px;
        background: #ffffff;
        padding: 22px;
      }}
      .scenario-card h2 {{
        margin: 0 0 14px;
        font-size: 22px;
      }}
      .scenario-copy {{
        display: grid;
        gap: 12px;
        margin-bottom: 18px;
      }}
      .scenario-copy section {{
        border-left: 4px solid #0f766e;
        padding-left: 12px;
      }}
      .scenario-copy h3 {{
        margin: 0 0 4px;
        font-size: 13px;
        text-transform: uppercase;
        color: #64707d;
      }}
      .actions {{
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
      }}
      button {{
        min-height: 40px;
        border: 1px solid #0f766e;
        border-radius: 6px;
        background: #ffffff;
        color: #0f514b;
        font-weight: 700;
        padding: 8px 12px;
      }}
      button:hover,
      button:focus {{
        background: #e8f3f1;
      }}
      @media (max-width: 760px) {{
        main {{ grid-template-columns: 1fr; }}
      }}
    </style>
  </head>
  <body>
    <main data-role="{escape(role)}" data-permission-simulator="true">
      <aside class="scenario-rail">
        <h1>Agent Permission Simulator</h1>
        <p>Judge the request before an agent crosses a file, command, network,
        or approval boundary.</p>
      </aside>
      <section class="workspace">
        <article class="scenario-card" data-scenario-card="{escape(scenario.id)}">
          <h2>{escape(scenario.title)}</h2>
          <div class="scenario-copy">
            <section data-scenario-request="true">
              <h3>Request</h3>
              <p>{escape(scenario.request)}</p>
            </section>
            <section data-scenario-context="true">
              <h3>Context</h3>
              <p>{escape(scenario.context)}</p>
            </section>
          </div>
          <form method="post" action="{escape(form_action)}"
            data-form="permission-decision">
            <input type="hidden" name="scenario_id" value="{escape(scenario.id)}">
            <div class="actions" aria-label="Decision actions">
              {buttons}
            </div>
          </form>
        </article>
      </section>
    </main>
  </body>
</html>"""


def _permission_result_html(*, role: str, scenario: PermissionScenario, score) -> str:
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Permission Decision Result</title>
  </head>
  <body>
    <main data-role="{escape(role)}" data-permission-result="true">
      <section data-score-outcome="{escape(score.outcome)}">
        <h1>{escape(score.outcome.title())}</h1>
        <p data-consequence="true">{escape(score.feedback)}</p>
        <p data-safer-path="true">{escape(score.safer_alternative)}</p>
        <p data-risk-category="{escape(score.risk_category)}">
          Risk category: {escape(score.risk_category)}
        </p>
        <p data-score-summary="true">
          Selected {escape(score.selected_decision)} for
          {escape(scenario.permission_boundary)} boundary.
        </p>
      </section>
    </main>
  </body>
</html>"""


def _learner_result_html(*, title: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="en">
  <head><meta charset="utf-8"><title>{escape(title)}</title></head>
  <body>
    <main data-learner-result="success">
      <h1>{escape(title)}</h1>
      {body}
    </main>
  </body>
</html>"""


def _manager_result_html(*, title: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="en">
  <head><meta charset="utf-8"><title>{escape(title)}</title></head>
  <body>
    <main data-manager-result="success">
      <h1>{escape(title)}</h1>
      {body}
    </main>
  </body>
</html>"""


def _operator_result_html(*, title: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="en">
  <head><meta charset="utf-8"><title>{escape(title)}</title></head>
  <body>
    <main data-operator-result="success">
      <h1>{escape(title)}</h1>
      {body}
    </main>
  </body>
</html>"""


def _safe_error_response(exc: Exception) -> HTMLResponse:
    status_code = status.HTTP_400_BAD_REQUEST
    message = "Invalid form submission"
    if isinstance(exc, HTTPException):
        status_code = exc.status_code
        if isinstance(exc.detail, str):
            message = exc.detail
        elif isinstance(exc.detail, dict):
            message = str(exc.detail.get("code", "Request failed"))
        else:
            message = "Request failed"
    return HTMLResponse(
        _operator_result_html(
            title="Request failed",
            body=f'<p data-error="true">{escape(message)}</p>',
        ),
        status_code=status_code,
    )


async def _form_values(request: Request) -> dict[str, str]:
    body = (await request.body()).decode()
    parsed = parse_qs(body, keep_blank_values=True)
    return {key: values[-1] if values else "" for key, values in parsed.items()}


def _form_value(form: dict[str, str], key: str) -> str:
    value = form.get(key)
    if value is None or not str(value).strip():
        raise ValueError(f"Missing form field: {key}")
    return str(value).strip()


def _learner_ids(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def _csv_values(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]
