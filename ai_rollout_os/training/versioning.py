import json
from uuid import uuid4

from ai_rollout_os.audit.repository import AuditEventRepository
from ai_rollout_os.auth.tokens import ActorContext
from ai_rollout_os.db.models import AuditEvent, MissionTemplate, RolePack
from ai_rollout_os.training.schemas import MissionRead, RolePackRead
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session


class MissionVersionUpdate(BaseModel):
    id: str | None = None
    objective: str = Field(min_length=1)
    instructions: str = Field(min_length=1)
    artifact_type: str = Field(min_length=1)
    rubric_id: str = Field(min_length=1)
    guardrail_quiz_id: str = Field(min_length=1)


class RolePackVersionUpdate(BaseModel):
    role: str = Field(min_length=1)
    title: str = Field(min_length=1)
    missions: list[MissionVersionUpdate] = Field(min_length=1)


class RolePackVersionDiff(BaseModel):
    previous_version: int
    new_version: int
    changed_missions: list[str]
    changed_rubric_ids: list[str]
    changed_guardrail_quiz_ids: list[str]
    unchanged_missions: list[str]


class RolePackVersionRead(BaseModel):
    role_pack: RolePackRead
    missions: list[MissionRead]
    diff: RolePackVersionDiff


class RolePackVersioningService:
    def __init__(self, session: Session) -> None:
        self._session = session

    def create_version(
        self, role_pack_id: str, payload: RolePackVersionUpdate, actor: ActorContext
    ) -> RolePackVersionRead:
        role_pack = self._role_pack(role_pack_id, actor)
        previous_version = role_pack.version
        existing_missions = {
            mission.id: mission
            for mission in self._session.scalars(
                select(MissionTemplate).where(
                    MissionTemplate.role_pack_id == role_pack.id,
                    MissionTemplate.workspace_id == actor.workspace_id,
                    MissionTemplate.active.is_(True),
                )
            ).all()
        }

        changed_missions: list[str] = []
        changed_rubric_ids: list[str] = []
        changed_guardrail_quiz_ids: list[str] = []
        unchanged_missions: list[str] = []
        active_missions: list[MissionTemplate] = []

        for mission_payload in payload.missions:
            existing = (
                existing_missions.get(mission_payload.id)
                if mission_payload.id is not None
                else None
            )
            if existing is None:
                new_mission = self._create_mission(role_pack, mission_payload, actor)
                changed_missions.append(new_mission.id)
                active_missions.append(new_mission)
                continue

            mission_changed = _mission_changed(existing, mission_payload)
            rubric_changed = existing.rubric_id != mission_payload.rubric_id
            guardrail_changed = (
                existing.guardrail_quiz_id != mission_payload.guardrail_quiz_id
            )
            if mission_changed or rubric_changed or guardrail_changed:
                existing.active = False
                new_mission = self._create_mission(role_pack, mission_payload, actor)
                changed_missions.append(existing.id)
                if rubric_changed:
                    changed_rubric_ids.append(mission_payload.rubric_id)
                if guardrail_changed:
                    changed_guardrail_quiz_ids.append(mission_payload.guardrail_quiz_id)
                active_missions.append(new_mission)
            else:
                unchanged_missions.append(existing.id)
                active_missions.append(existing)

        role_pack.role = payload.role
        role_pack.title = payload.title
        role_pack.version = previous_version + 1
        diff = RolePackVersionDiff(
            previous_version=previous_version,
            new_version=role_pack.version,
            changed_missions=changed_missions,
            changed_rubric_ids=changed_rubric_ids,
            changed_guardrail_quiz_ids=changed_guardrail_quiz_ids,
            unchanged_missions=unchanged_missions,
        )
        AuditEventRepository(self._session).append(
            actor_id=actor.actor_id,
            action="role_pack.version_created",
            resource_type="role_pack",
            resource_id=role_pack.id,
            result="success",
            trace_id=actor.trace_id,
            details=diff.model_dump_json(),
        )
        self._session.flush()
        return RolePackVersionRead(
            role_pack=_role_pack_read(role_pack),
            missions=[_mission_read(mission) for mission in active_missions],
            diff=diff,
        )

    def compare_versions(
        self, role_pack_id: str, actor: ActorContext
    ) -> RolePackVersionDiff:
        self._role_pack(role_pack_id, actor)
        event = self._session.scalar(
            select(AuditEvent)
            .where(
                AuditEvent.resource_type == "role_pack",
                AuditEvent.resource_id == role_pack_id,
                AuditEvent.action == "role_pack.version_created",
            )
            .order_by(AuditEvent.id.desc())
            .limit(1)
        )
        if event is None or event.details is None:
            raise ValueError("Role pack version diff not found")
        return RolePackVersionDiff(**json.loads(event.details))

    def _role_pack(self, role_pack_id: str, actor: ActorContext) -> RolePack:
        role_pack = self._session.scalar(
            select(RolePack).where(
                RolePack.id == role_pack_id,
                RolePack.workspace_id == actor.workspace_id,
            )
        )
        if role_pack is None:
            raise ValueError("Role pack not found")
        return role_pack

    def _create_mission(
        self,
        role_pack: RolePack,
        payload: MissionVersionUpdate,
        actor: ActorContext,
    ) -> MissionTemplate:
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


def _mission_changed(existing: MissionTemplate, payload: MissionVersionUpdate) -> bool:
    return (
        existing.objective != payload.objective
        or existing.instructions != payload.instructions
        or existing.artifact_type != payload.artifact_type
    )


def _role_pack_read(role_pack: RolePack) -> RolePackRead:
    return RolePackRead(
        id=role_pack.id,
        workspace_id=role_pack.workspace_id,
        role=role_pack.role,
        title=role_pack.title,
        version=role_pack.version,
        launch_status=role_pack.launch_status,
    )


def _mission_read(mission: MissionTemplate) -> MissionRead:
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
