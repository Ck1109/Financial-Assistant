"""Retrieval port and a small deterministic keyword implementation."""

from dataclasses import dataclass
import re
from typing import Protocol, Sequence

from financial_assistant.domain.entities import ContextSegment


@dataclass(frozen=True)
class RetrievedSegment:
    """Segment plus deterministic relevance score."""

    segment: ContextSegment
    score: float


class VectorStore(Protocol):
    """Provider-neutral retrieval contract."""

    name: str

    def search(self, query: str, segments: Sequence[ContextSegment]) -> list[RetrievedSegment]:
        """Return relevant segments ordered by score."""


class KeywordVectorStore:
    """Transparent local retrieval adapter used for learning and tests."""

    name = "local-keyword"

    def search(self, query: str, segments: Sequence[ContextSegment]) -> list[RetrievedSegment]:
        """Score segments by normalized query-token overlap."""
        tokens = set(re.findall(r"[a-z0-9]+", query.lower()))
        ranked = []
        for segment in segments:
            words = set(re.findall(r"[a-z0-9]+", segment.text.lower()))
            score = len(tokens & words) / max(len(tokens), 1)
            if score:
                ranked.append(RetrievedSegment(segment, score))
        return sorted(ranked, key=lambda item: (-item.score, item.segment.segment_id))

