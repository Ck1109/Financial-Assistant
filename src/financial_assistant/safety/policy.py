"""Centralized safety checks for grounded and educational responses."""

import re

from financial_assistant.domain.entities import Answer, Claim, Citation
from financial_assistant.domain.enums import AnswerStatus


PERSONAL_ADVICE = re.compile(r"\b(buy|sell|hold|invest|my portfolio|my money)\b", re.I)


def insufficient_answer(reason: str, provider_snapshot: dict[str, str]) -> Answer:
    """Build an explicit abstention rather than a success-shaped fallback."""
    return Answer(
        answer_id="answer-insufficient",
        status=AnswerStatus.INSUFFICIENT_EVIDENCE,
        summary="The indexed data is insufficient to answer this question.",
        uncertainty=(reason,),
        provider_snapshot=provider_snapshot,
    )


def validate_answer(answer: Answer) -> None:
    """Reject unsafe answer contracts with missing citations or advice."""
    if answer.status == AnswerStatus.ANSWERED:
        if any(not claim.citations for claim in answer.claims):
            raise ValueError("Answered claims must include at least one citations entry.")
    if PERSONAL_ADVICE.search(answer.summary):
        raise ValueError("Personalized investment recommendations are not permitted.")


def cited_claim(text: str, version_id: str, segment_id: str, location: str) -> Claim:
    """Create a claim with one explicit provenance citation."""
    return Claim(text=text, citations=(Citation(version_id, segment_id, location),))
