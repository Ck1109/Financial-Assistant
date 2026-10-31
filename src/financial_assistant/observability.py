"""Small structured observability helpers with sensitive-value redaction."""

import re
from dataclasses import dataclass
from uuid import uuid4


@dataclass(frozen=True)
class RunEvent:
    """Inspectable event emitted by a processing or answer workflow."""

    run_id: str
    event: str
    status: str
    detail: str


def new_run_id() -> str:
    """Create a correlation identifier for one workflow execution."""
    return f"run-{uuid4().hex}"


def redact(value: str) -> str:
    """Remove common credential-shaped values before logging."""
    return re.sub(r"(?i)(api[_-]?key|token|password)=\S+", r"\1=[REDACTED]", value)

