"""Provider-neutral indexed-context search service."""

from financial_assistant.domain.entities import ContextSegment
from financial_assistant.providers.vector_store import RetrievedSegment, VectorStore


def search_segments(
    query: str, segments: list[ContextSegment], provider: VectorStore
) -> list[RetrievedSegment]:
    """Delegate retrieval while keeping the workflow independent of a provider."""
    return provider.search(query, segments)
