"""Embedding provider contract kept separate from retrieval storage."""

from typing import Protocol, Sequence


class EmbeddingProvider(Protocol):
    """Minimal interchangeable embedding boundary."""

    name: str

    def embed(self, texts: Sequence[str]) -> list[list[float]]:
        """Return one vector per input text."""


class LocalHashEmbeddings:
    """Deterministic placeholder adapter for local contract demonstrations."""

    name = "local-hash"

    def embed(self, texts: Sequence[str]) -> list[list[float]]:
        """Encode text into a stable, tiny numeric representation."""
        return [[float(len(text)), float(sum(map(ord, text)) % 997)] for text in texts]

