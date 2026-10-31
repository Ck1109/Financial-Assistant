"""Typed local configuration for the Financial Assistant."""

from dataclasses import dataclass
import os
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    """Runtime paths and provider names loaded from environment variables."""

    data_dir: Path
    llm_provider: str
    retrieval_provider: str

    @classmethod
    def from_env(cls) -> "Settings":
        """Load configuration and create the local data directories."""
        data_dir = Path(os.getenv("FINANCIAL_ASSISTANT_DATA_DIR", "data"))
        settings = cls(
            data_dir=data_dir,
            llm_provider=os.getenv("FINANCIAL_ASSISTANT_LLM_PROVIDER", "local-deterministic"),
            retrieval_provider=os.getenv(
                "FINANCIAL_ASSISTANT_RETRIEVAL_PROVIDER", "local-keyword"
            ),
        )
        (settings.data_dir / "raw").mkdir(parents=True, exist_ok=True)
        (settings.data_dir / "extracted").mkdir(parents=True, exist_ok=True)
        return settings

