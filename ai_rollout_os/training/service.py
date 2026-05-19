from uuid import uuid4

from ai_rollout_os.auth.tokens import ActorContext
from ai_rollout_os.db.models import MissionTemplate, RolePack
from ai_rollout_os.training.schemas import MissionCreate, RolePackCreate
from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session


class RolePackService:
    def __init__(self, session: Session) -> None:
        self._session = session

    def create_draft_role_pack(
        self, payload: RolePackCreate, actor: ActorContext
    ) -> RolePack:
        role_pack = RolePack(
            id=f"rp_{uuid4().hex}",
            workspace_id=actor.workspace_id,
            role=payload.role,
            title=payload.title,
            version=1,
            launch_status="inactive",
            created_by=actor.actor_id,
        )
        self._session.add(role_pack)
        self._session.flush()
        return role_pack

    def add_mission(
        self, role_pack_id: str, payload: MissionCreate, actor: ActorContext
    ) -> MissionTemplate:
        role_pack = self._role_pack_for_actor(role_pack_id, actor)
        mission = MissionTemplate(
            id=f"mission_{uuid4().hex}",
            role_pack_id=role_pack.id,
            workspace_id=actor.workspace_id,
            objective=payload.objective,
            instructions=payload.instructions,
            artifact_type=payload.artifact_type,
            rubric_id=payload.rubric_id,
            guardrail_quiz_id=payload.guardrail_quiz_id,
            active=True,
        )
        self._session.add(mission)
        self._session.flush()
        return mission

    def launch(self, role_pack_id: str, actor: ActorContext) -> RolePack:
        role_pack = self._role_pack_for_actor(role_pack_id, actor)
        active_missions = self._session.scalar(
            select(func.count())
            .select_from(MissionTemplate)
            .where(
                MissionTemplate.role_pack_id == role_pack.id,
                MissionTemplate.workspace_id == actor.workspace_id,
                MissionTemplate.active.is_(True),
            )
        )
        if active_missions == 0:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"code": "role_pack_has_no_missions"},
            )
        role_pack.launch_status = "active"
        self._session.flush()
        return role_pack

    def _role_pack_for_actor(self, role_pack_id: str, actor: ActorContext) -> RolePack:
        role_pack = self._session.scalar(
            select(RolePack).where(
                RolePack.id == role_pack_id,
                RolePack.workspace_id == actor.workspace_id,
            )
        )
        if role_pack is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Role pack not found"
            )
        return role_pack
