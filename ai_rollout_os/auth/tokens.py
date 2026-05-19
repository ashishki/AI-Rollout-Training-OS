import base64
import hashlib
import hmac
import json
import time
from dataclasses import dataclass
from typing import Any


class TokenError(ValueError):
    pass


@dataclass(frozen=True)
class ActorContext:
    actor_id: str
    role: str
    workspace_id: str
    trace_id: str


def create_token(
    *,
    actor_id: str,
    role: str,
    workspace_id: str,
    secret_key: str,
    ttl_seconds: int = 3600,
) -> str:
    payload = {
        "actor_id": actor_id,
        "role": role,
        "workspace_id": workspace_id,
        "exp": int(time.time()) + ttl_seconds,
    }
    payload_segment = _b64encode(_json_bytes(payload))
    signature_segment = _sign(payload_segment, secret_key)
    return f"{payload_segment}.{signature_segment}"


def decode_token(token: str, *, secret_key: str) -> dict[str, Any]:
    try:
        payload_segment, signature_segment = token.split(".", maxsplit=1)
    except ValueError as exc:
        raise TokenError("Invalid token") from exc

    expected_signature = _sign(payload_segment, secret_key)
    if not hmac.compare_digest(signature_segment, expected_signature):
        raise TokenError("Invalid token")

    payload = json.loads(_b64decode(payload_segment))
    required_fields = {"actor_id", "role", "workspace_id", "exp"}
    if not required_fields.issubset(payload):
        raise TokenError("Invalid token")
    if int(payload["exp"]) < int(time.time()):
        raise TokenError("Expired token")
    return payload


def _json_bytes(payload: dict[str, Any]) -> bytes:
    return json.dumps(payload, separators=(",", ":"), sort_keys=True).encode()


def _b64encode(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).decode().rstrip("=")


def _b64decode(value: str) -> bytes:
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode(value + padding)


def _sign(payload_segment: str, secret_key: str) -> str:
    digest = hmac.new(
        secret_key.encode(), payload_segment.encode(), hashlib.sha256
    ).digest()
    return _b64encode(digest)
