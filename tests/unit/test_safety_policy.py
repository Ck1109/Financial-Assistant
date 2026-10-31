import pytest

from financial_assistant.domain.entities import Answer
from financial_assistant.domain.enums import AnswerStatus
from financial_assistant.safety.policy import validate_answer


def test_answered_claim_without_citation_is_rejected():
    with pytest.raises(ValueError, match="citations"):
        validate_answer(Answer("a", AnswerStatus.ANSWERED, "A fact.", claims=(type("C", (), {"citations": ()})(),)))


def test_personalized_advice_is_rejected():
    with pytest.raises(ValueError, match="recommendations"):
        validate_answer(Answer("a", AnswerStatus.ANSWERED, "You should buy this.", claims=()))
