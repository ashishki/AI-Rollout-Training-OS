from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from typing import Literal

from ai_rollout_os.permissions.scenarios import PermissionScenario
from ai_rollout_os.permissions.scoring import DecisionScore

PROOF_RECEIPT_SCHEMA_VERSION = "entropy_core.product_receipt.v1"
PRODUCT_ID = "ai-rollout-training-os"


@dataclass(frozen=True)
class PermissionEvidenceRef:
    ref_id: str
    ref_type: Literal["scenario", "permission_boundary", "lesson"]
    supports: str
    checksum_sha256: str


@dataclass(frozen=True)
class PermissionDecisionProofReceipt:
    type: Literal["permission_decision_receipt"]
    schema_version: Literal["entropy_core.product_receipt.v1"]
    product_id: Literal["ai-rollout-training-os"]
    receipt_id: str
    scenario_id: str
    selected_decision: str
    correct_decision: str
    outcome: str
    risk_category: str
    permission_boundary: str
    verifier_status: Literal["passed", "needs_review", "failed"]
    evidence_refs: tuple[PermissionEvidenceRef, ...]
    generated_at: datetime
    entropy_core_level: Literal["receipt_compatible"]

    def canonical_json(self) -> str:
        payload = asdict(self)
        payload["generated_at"] = self.generated_at.isoformat()
        return json.dumps(
            payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True
        )

    def receipt_sha256(self) -> str:
        return hashlib.sha256(self.canonical_json().encode("utf-8")).hexdigest()


def build_permission_decision_receipt(
    *,
    scenario: PermissionScenario,
    score: DecisionScore,
    generated_at: datetime | None = None,
) -> PermissionDecisionProofReceipt:
    if score.scenario_id != scenario.id:
        raise ValueError("score scenario_id must match permission scenario id")
    verifier_status: Literal["passed", "needs_review", "failed"]
    if score.outcome == "correct":
        verifier_status = "passed"
    elif score.outcome == "partial":
        verifier_status = "needs_review"
    else:
        verifier_status = "failed"

    evidence_refs = (
        _evidence_ref(
            ref_id=f"scenario:{scenario.id}",
            ref_type="scenario",
            supports="decision_context",
            value=f"{scenario.request}\n{scenario.context}",
        ),
        _evidence_ref(
            ref_id=f"permission_boundary:{scenario.id}",
            ref_type="permission_boundary",
            supports=scenario.permission_boundary,
            value=f"{scenario.permission_boundary}:{scenario.risk_category}",
        ),
        _evidence_ref(
            ref_id=f"lesson:{scenario.id}",
            ref_type="lesson",
            supports=score.correct_decision,
            value=scenario.lesson_text,
        ),
    )
    receipt_seed = (
        f"{scenario.id}:{score.selected_decision}:"
        f"{score.correct_decision}:{score.outcome}"
    )
    return PermissionDecisionProofReceipt(
        type="permission_decision_receipt",
        schema_version=PROOF_RECEIPT_SCHEMA_VERSION,
        product_id=PRODUCT_ID,
        receipt_id="pdr_"
        + hashlib.sha256(receipt_seed.encode("utf-8")).hexdigest()[:16],
        scenario_id=scenario.id,
        selected_decision=score.selected_decision,
        correct_decision=score.correct_decision,
        outcome=score.outcome,
        risk_category=score.risk_category,
        permission_boundary=score.permission_boundary,
        verifier_status=verifier_status,
        evidence_refs=evidence_refs,
        generated_at=generated_at or datetime.now(UTC),
        entropy_core_level="receipt_compatible",
    )


def _evidence_ref(
    *,
    ref_id: str,
    ref_type: Literal["scenario", "permission_boundary", "lesson"],
    supports: str,
    value: str,
) -> PermissionEvidenceRef:
    return PermissionEvidenceRef(
        ref_id=ref_id,
        ref_type=ref_type,
        supports=supports,
        checksum_sha256=hashlib.sha256(value.encode("utf-8")).hexdigest(),
    )
