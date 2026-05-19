from uuid import uuid4

from ai_rollout_os.auth.tokens import ActorContext
from ai_rollout_os.db.models import (
    Cohort,
    CohortEnrollment,
    MissionAssignment,
    MissionTemplate,
    RolePack,
)
from ai_rollout_os.training.cohort_models import CohortCreate
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session


class CohortService:
    def __init__(self, session: Session) -> None:
        self._session = session

    def create_cohort(self, payload: CohortCreate, actor: ActorContext) -> Cohort:
        role_pack = self._role_pack_for_actor(
            payload.role_pack_id, payload.role_pack_version, actor
        )
        cohort = Cohort(
            id=f"cohort_{uuid4().hex}",
            workspace_id=actor.workspace_id,
            role_pack_id=role_pack.id,
            role_pack_version=payload.role_pack_version,
            manager_id=payload.manager_id,
            start_date=payload.start_date,
            due_date=payload.due_date,
            status="draft",
            created_by=actor.actor_id,
        )
        self._session.add(cohort)
        self._session.flush()
        for learner_id in payload.learner_ids:
            self._session.add(
                CohortEnrollment(
                    id=f"enroll_{uuid4().hex}",
                    cohort_id=cohort.id,
                    workspace_id=actor.workspace_id,
                    learner_id=learner_id,
                )
            )
        self._session.flush()
        return cohort

    def launch_cohort(
        self, cohort_id: str, actor: ActorContext
    ) -> list[MissionAssignment]:
        cohort = self._cohort_for_actor(cohort_id, actor)
        missions = self._session.scalars(
            select(MissionTemplate).where(
                MissionTemplate.role_pack_id == cohort.role_pack_id,
                MissionTemplate.workspace_id == actor.workspace_id,
                MissionTemplate.active.is_(True),
            )
        ).all()
        enrollments = self._session.scalars(
            select(CohortEnrollment).where(
                CohortEnrollment.cohort_id == cohort.id,
                CohortEnrollment.workspace_id == actor.workspace_id,
            )
        ).all()
        for enrollment in enrollments:
            for mission in missions:
                if self._assignment_exists(
                    cohort.id, enrollment.learner_id, mission.id
                ):
                    continue
                self._session.add(
                    MissionAssignment(
                        id=f"assign_{uuid4().hex}",
                        cohort_id=cohort.id,
                        workspace_id=actor.workspace_id,
                        learner_id=enrollment.learner_id,
                        mission_template_id=mission.id,
                        role_pack_version=cohort.role_pack_version,
                        status="assigned",
                    )
                )
        cohort.status = "active"
        self._session.flush()
        return self.assignments_for_cohort(cohort.id, actor)

    def learner_assignments(
        self, cohort_id: str, actor: ActorContext
    ) -> list[MissionAssignment]:
        cohort = self._cohort_for_actor(cohort_id, actor)
        enrollment = self._session.scalar(
            select(CohortEnrollment).where(
                CohortEnrollment.cohort_id == cohort.id,
                CohortEnrollment.workspace_id == actor.workspace_id,
                CohortEnrollment.learner_id == actor.actor_id,
            )
        )
        if enrollment is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
            )
        return self._session.scalars(
            select(MissionAssignment).where(
                MissionAssignment.cohort_id == cohort.id,
                MissionAssignment.workspace_id == actor.workspace_id,
                MissionAssignment.learner_id == actor.actor_id,
            )
        ).all()

    def assignments_for_cohort(
        self, cohort_id: str, actor: ActorContext
    ) -> list[MissionAssignment]:
        return self._session.scalars(
            select(MissionAssignment).where(
                MissionAssignment.cohort_id == cohort_id,
                MissionAssignment.workspace_id == actor.workspace_id,
            )
        ).all()

    def _role_pack_for_actor(
        self, role_pack_id: str, role_pack_version: int, actor: ActorContext
    ) -> RolePack:
        role_pack = self._session.scalar(
            select(RolePack).where(
                RolePack.id == role_pack_id,
                RolePack.version == role_pack_version,
                RolePack.workspace_id == actor.workspace_id,
            )
        )
        if role_pack is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Role pack not found"
            )
        return role_pack

    def _cohort_for_actor(self, cohort_id: str, actor: ActorContext) -> Cohort:
        cohort = self._session.scalar(
            select(Cohort).where(
                Cohort.id == cohort_id,
                Cohort.workspace_id == actor.workspace_id,
            )
        )
        if cohort is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cohort not found"
            )
        return cohort

    def _assignment_exists(
        self, cohort_id: str, learner_id: str, mission_template_id: str
    ) -> bool:
        return (
            self._session.scalar(
                select(MissionAssignment.id).where(
                    MissionAssignment.cohort_id == cohort_id,
                    MissionAssignment.learner_id == learner_id,
                    MissionAssignment.mission_template_id == mission_template_id,
                )
            )
            is not None
        )
