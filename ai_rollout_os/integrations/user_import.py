import csv
import logging
from dataclasses import dataclass
from io import StringIO

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ai_rollout_os.audit.repository import AuditEventRepository
from ai_rollout_os.auth.tokens import ActorContext
from ai_rollout_os.db.models import User

logger = logging.getLogger(__name__)

ALLOWED_IMPORTED_ROLES = {"operator", "manager", "learner"}
REQUIRED_COLUMNS = {"user_id", "email", "role", "manager_id", "team"}


class UserImportError(ValueError):
    pass


@dataclass(frozen=True)
class ImportedUserRow:
    user_id: str
    email: str
    role: str
    manager_id: str | None
    team: str


@dataclass(frozen=True)
class UserImportResult:
    imported_count: int
    role_counts: dict[str, int]
    teams: list[str]
    manager_links: dict[str, str]


class UserImportService:
    def __init__(self, session: Session) -> None:
        self._session = session

    def import_csv(self, csv_text: str, actor: ActorContext) -> UserImportResult:
        rows = _parse_csv(csv_text)
        errors = self._validate_rows(rows, actor.workspace_id)
        if errors:
            logger.warning(
                "user_import.validation_failed",
                extra={"error_count": len(errors), "row_count": len(rows)},
            )
            raise UserImportError("CSV import validation failed")

        for row in rows:
            existing = self._session.get(User, row.user_id)
            if existing is None:
                self._session.add(
                    User(
                        id=row.user_id,
                        workspace_id=actor.workspace_id,
                        email=row.email,
                        role=row.role,
                    )
                )
                continue
            existing.email = row.email
            existing.role = row.role

        result = _result(rows)
        AuditEventRepository(self._session).append(
            actor_id=actor.actor_id,
            action="users.imported",
            resource_type="users",
            resource_id=actor.workspace_id,
            result="success",
            trace_id=actor.trace_id,
            details=f"imported={result.imported_count}",
        )
        self._session.flush()
        return result

    def _validate_rows(
        self, rows: list[ImportedUserRow], workspace_id: str
    ) -> list[str]:
        errors: list[str] = []
        seen_user_ids: set[str] = set()
        seen_emails: set[str] = set()
        imported_roles = {row.user_id: row.role for row in rows}
        existing_manager_ids = set(
            self._session.scalars(
                select(User.id).where(
                    User.workspace_id == workspace_id,
                    User.role == "manager",
                )
            ).all()
        )

        for index, row in enumerate(rows, start=1):
            if row.user_id in seen_user_ids:
                errors.append(f"row {index}: duplicate user_id")
            seen_user_ids.add(row.user_id)
            normalized_email = row.email.lower()
            if normalized_email in seen_emails:
                errors.append(f"row {index}: duplicate email")
            seen_emails.add(normalized_email)
            if row.role not in ALLOWED_IMPORTED_ROLES:
                errors.append(f"row {index}: unsupported role")
            if "@" not in row.email:
                errors.append(f"row {index}: invalid email")
            if not row.team:
                errors.append(f"row {index}: missing team")
            if row.role == "learner":
                manager_role = imported_roles.get(row.manager_id or "")
                if (
                    row.manager_id not in existing_manager_ids
                    and manager_role != "manager"
                ):
                    errors.append(f"row {index}: unknown manager")

        existing_emails = self._session.scalars(
            select(User.email).where(
                User.workspace_id == workspace_id,
                func.lower(User.email).in_(seen_emails),
                User.id.not_in(seen_user_ids),
            )
        ).all()
        if existing_emails:
            errors.append("email already assigned")
        return errors


def _parse_csv(csv_text: str) -> list[ImportedUserRow]:
    reader = csv.DictReader(StringIO(csv_text))
    columns = set(reader.fieldnames or [])
    missing = REQUIRED_COLUMNS - columns
    if missing:
        raise UserImportError("CSV import missing required columns")

    rows = [
        ImportedUserRow(
            user_id=(row.get("user_id") or "").strip(),
            email=(row.get("email") or "").strip().lower(),
            role=(row.get("role") or "").strip().lower(),
            manager_id=(row.get("manager_id") or "").strip() or None,
            team=(row.get("team") or "").strip(),
        )
        for row in reader
    ]
    if not rows:
        raise UserImportError("CSV import contains no rows")
    return rows


def _result(rows: list[ImportedUserRow]) -> UserImportResult:
    role_counts = {role: 0 for role in sorted(ALLOWED_IMPORTED_ROLES)}
    teams = sorted({row.team for row in rows})
    manager_links: dict[str, str] = {}
    for row in rows:
        role_counts[row.role] += 1
        if row.manager_id:
            manager_links[row.user_id] = row.manager_id
    return UserImportResult(
        imported_count=len(rows),
        role_counts=role_counts,
        teams=teams,
        manager_links=manager_links,
    )
