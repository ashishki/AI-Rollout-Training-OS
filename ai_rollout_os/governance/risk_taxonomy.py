from dataclasses import dataclass

RISK_TAXONOMY_VERSION = "risk-taxonomy-v1"


class UnknownRiskFlagError(ValueError):
    pass


@dataclass(frozen=True)
class RiskCategory:
    id: str
    label: str
    aliases: frozenset[str]


RISK_TAXONOMY = {
    "privacy": RiskCategory(
        id="privacy",
        label="PII or personal data exposure",
        aliases=frozenset({"pii", "personal_data", "sensitive_data_detected"}),
    ),
    "legal": RiskCategory(
        id="legal",
        label="Legal approval or legal advice required",
        aliases=frozenset({"legal_approval", "legal_review"}),
    ),
    "medical": RiskCategory(
        id="medical",
        label="Medical or health-related regulated use",
        aliases=frozenset({"health", "regulated_health_data"}),
    ),
    "financial": RiskCategory(
        id="financial",
        label="Financial advice, payment data, or regulated financial use",
        aliases=frozenset({"payment_data", "financial_advice"}),
    ),
    "customer_data": RiskCategory(
        id="customer_data",
        label="Customer data or proprietary customer context",
        aliases=frozenset({"customer_data_marker"}),
    ),
    "unsupported_claim": RiskCategory(
        id="unsupported_claim",
        label="Unsupported claim or insufficient evidence",
        aliases=frozenset({"unsupported_claims", "missing_evidence"}),
    ),
    "policy_ownership": RiskCategory(
        id="policy_ownership",
        label="Policy ownership, approval, or certification boundary",
        aliases=frozenset({"policy_change", "policy_approval", "certification"}),
    ),
}

_ALIAS_TO_ID = {
    alias: category.id
    for category in RISK_TAXONOMY.values()
    for alias in category.aliases | {category.id}
}


def normalize_risk_flags(flags: list[str]) -> list[str]:
    normalized: set[str] = set()
    unknown: list[str] = []
    for flag in flags:
        key = flag.strip().lower()
        if not key:
            continue
        risk_id = _ALIAS_TO_ID.get(key)
        if risk_id is None:
            unknown.append(flag)
            continue
        normalized.add(risk_id)
    if unknown:
        joined = ", ".join(sorted(unknown))
        raise UnknownRiskFlagError(f"Unknown risk flags: {joined}")
    return sorted(normalized)
