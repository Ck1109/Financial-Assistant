"""Controlled status values used across application boundaries."""

from enum import StrEnum


class DocumentStatus(StrEnum):
    """Lifecycle state for an indexed source version."""

    PENDING = "pending"
    PROCESSING = "processing"
    INDEXED = "indexed"
    DEGRADED = "degraded"
    REJECTED = "rejected"
    SUPERSEDED = "superseded"


class ApprovalStatus(StrEnum):
    """Maintainer approval state for sources used in market education."""

    PENDING = "pending"
    APPROVED = "approved"
    REVOKED = "revoked"
    SUPERSEDED = "superseded"


class AnswerStatus(StrEnum):
    """Safe answer outcomes."""

    ANSWERED = "answered"
    INSUFFICIENT_EVIDENCE = "insufficient-evidence"
    CONFLICTING_EVIDENCE = "conflicting-evidence"
    FAILED = "failed"

