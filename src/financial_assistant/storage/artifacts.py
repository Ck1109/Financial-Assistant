"""Content-addressed local artifact storage."""

from dataclasses import dataclass
import hashlib
from datetime import datetime, timezone
from pathlib import Path

from financial_assistant.domain.entities import SourceArtifact, new_id


@dataclass(frozen=True)
class StoredArtifact:
    """Artifact metadata plus the path of preserved submitted bytes."""

    artifact: SourceArtifact
    path: Path
    duplicate: bool


class ArtifactStore:
    """Preserve source bytes and avoid duplicate searchable copies."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def save(self, content: bytes, source_uri: str, media_type: str) -> StoredArtifact:
        """Hash and persist bytes, returning duplicate information explicitly."""
        digest = hashlib.sha256(content).hexdigest()
        path = self.root / digest
        duplicate = path.exists()
        if not duplicate:
            path.write_bytes(content)
        artifact = SourceArtifact(
            artifact_id=new_id("artifact"),
            sha256=digest,
            source_uri=source_uri,
            media_type=media_type,
            byte_size=len(content),
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        return StoredArtifact(artifact=artifact, path=path, duplicate=duplicate)
