from collections.abc import Generator

from ai_rollout_os.auth.permissions import require_role
from ai_rollout_os.auth.tokens import ActorContext
from ai_rollout_os.training.schemas import (
    MissionCreate,
    MissionRead,
    RolePackCreate,
    RolePackRead,
)
from ai_rollout_os.training.service import RolePackService
from ai_rollout_os.training.versioning import (
    RolePackVersionDiff,
    RolePackVersioningService,
    RolePackVersionRead,
    RolePackVersionUpdate,
)
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

router = APIRouter()
OPERATOR_ACTOR = Depends(require_role("operator"))


def get_session(request: Request) -> Generator[Session]:
    session_factory = request.app.state.session_factory
    with session_factory() as session:
        yield session


DB_SESSION = Depends(get_session)


@router.post("/role-packs", response_model=RolePackRead, status_code=201)
def create_role_pack(
    payload: RolePackCreate,
    actor: ActorContext = OPERATOR_ACTOR,
    session: Session = DB_SESSION,
) -> RolePackRead:
    role_pack = RolePackService(session).create_draft_role_pack(payload, actor)
    session.commit()
    return RolePackRead(
        id=role_pack.id,
        workspace_id=role_pack.workspace_id,
        role=role_pack.role,
        title=role_pack.title,
        version=role_pack.version,
        launch_status=role_pack.launch_status,
    )


@router.post("/role-packs/{role_pack_id}/missions", response_model=MissionRead)
def add_mission(
    role_pack_id: str,
    payload: MissionCreate,
    actor: ActorContext = OPERATOR_ACTOR,
    session: Session = DB_SESSION,
) -> MissionRead:
    mission = RolePackService(session).add_mission(role_pack_id, payload, actor)
    session.commit()
    return MissionRead(
        id=mission.id,
        role_pack_id=mission.role_pack_id,
        workspace_id=mission.workspace_id,
        objective=mission.objective,
        instructions=mission.instructions,
        artifact_type=mission.artifact_type,
        rubric_id=mission.rubric_id,
        guardrail_quiz_id=mission.guardrail_quiz_id,
        active=mission.active,
    )


@router.post("/role-packs/{role_pack_id}/launch", response_model=RolePackRead)
def launch_role_pack(
    role_pack_id: str,
    actor: ActorContext = OPERATOR_ACTOR,
    session: Session = DB_SESSION,
) -> RolePackRead:
    role_pack = RolePackService(session).launch(role_pack_id, actor)
    session.commit()
    return RolePackRead(
        id=role_pack.id,
        workspace_id=role_pack.workspace_id,
        role=role_pack.role,
        title=role_pack.title,
        version=role_pack.version,
        launch_status=role_pack.launch_status,
    )


@router.post(
    "/role-packs/{role_pack_id}/versions",
    response_model=RolePackVersionRead,
)
def create_role_pack_version(
    role_pack_id: str,
    payload: RolePackVersionUpdate,
    actor: ActorContext = OPERATOR_ACTOR,
    session: Session = DB_SESSION,
) -> RolePackVersionRead:
    result = RolePackVersioningService(session).create_version(
        role_pack_id, payload, actor
    )
    session.commit()
    return result


@router.get(
    "/role-packs/{role_pack_id}/versions/compare",
    response_model=RolePackVersionDiff,
)
def compare_role_pack_versions(
    role_pack_id: str,
    actor: ActorContext = OPERATOR_ACTOR,
    session: Session = DB_SESSION,
) -> RolePackVersionDiff:
    return RolePackVersioningService(session).compare_versions(role_pack_id, actor)
