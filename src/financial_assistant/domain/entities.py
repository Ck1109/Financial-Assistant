"""Serializable domain entities for provenance, retrieval, and answers."""

from dataclasses import asdict, dataclass, field
from datetime import date, datetime, timezone
from typing import Any
from uuid import uuid4

from .enums import AnswerStatus, ApprovalStatus, DocumentStatus


def new_id(prefix: str) -> str:
    """Create a readable stable identifier for a local record."""
    return f"{prefix}-{uuid4().hex}"


@dataclass(frozen=True)
class SourceArtifact:
    """Immutable submitted bytes and their content hash."""

    artifact_id: str
    sha256: str
    source_uri: str
    media_type: str
    byte_size: int
    created_at: str


@dataclass(frozen=True)
class DocumentVersion:
    """Logical notification or report derived from an artifact."""

    document_id: str
    version_id: str
    artifact_id: str
    document_type: str
    title: str
    publication_date: str | None = None
    reporting_month: str | None = None
    authority: str | None = None
    language: str = "en"
    status: DocumentStatus = DocumentStatus.PENDING
    approval_status: ApprovalStatus = ApprovalStatus.PENDING


@dataclass(frozen=True)
class ContextSegment:
    """Citeable text or table unit used during retrieval."""

    segment_id: str
    version_id: str
    segment_type: str
    text: str
    location: str
    page_number: int | None = None
    quality: str = "normal"


@dataclass(frozen=True)
class Topic:
    """Learner-readable topic with source support."""

    topic_id: str
    version_id: str
    label: str
    aliases: tuple[str, ...] = ()
    context_segment_ids: tuple[str, ...] = ()
    confidence: float = 1.0


@dataclass(frozen=True)
class TabularDataset:
    """Normalized tabular source metadata."""

    dataset_id: str
    version_id: str
    columns: tuple[str, ...] = ()
    reporting_period: str | None = None
    row_count: int = 0
    validation_status: str = "pending"


@dataclass(frozen=True)
class ExtractionRun:
    """One immutable extraction attempt and its outcome."""

    run_id: str
    artifact_id: str
    method: str
    status: str
    warnings: tuple[str, ...] = ()
    error_code: str | None = None


@dataclass(frozen=True)
class Question:
    """Original user question and its interpreted scope."""

    question_id: str
    text: str
    question_type: str | None = None
    time_scope: str | None = None


@dataclass(frozen=True)
class ProcessingRun:
    """Observable ingestion or analysis run."""

    run_id: str
    status: str
    error_code: str | None = None
    error_message: str | None = None


@dataclass(frozen=True)
class ProviderConfiguration:
    """Configured provider names and compatibility status."""

    language_model: str
    embeddings: str
    vector_store: str
    compatibility_status: str = "unknown"


@dataclass(frozen=True)
class Citation:
    """Location of evidence supporting a material claim."""

    version_id: str
    segment_id: str
    location: str


@dataclass(frozen=True)
class Claim:
    """A material answer statement and its evidence."""

    text: str
    citations: tuple[Citation, ...]


@dataclass(frozen=True)
class Answer:
    """Safe user-visible answer contract."""

    answer_id: str
    status: AnswerStatus
    summary: str
    claims: tuple[Claim, ...] = ()
    uncertainty: tuple[str, ...] = ()
    market_education_label: str | None = None
    learning_explanation: dict[str, Any] = field(default_factory=dict)
    provider_snapshot: dict[str, str] = field(default_factory=dict)
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-compatible representation for the UI and tests."""
        return asdict(self)


def today_iso() -> str:
    """Return the local workflow's current date in ISO format."""
    return date.today().isoformat()
