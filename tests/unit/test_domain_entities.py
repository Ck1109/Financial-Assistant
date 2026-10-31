from financial_assistant.domain.entities import Answer, Claim, Citation
from financial_assistant.domain.enums import AnswerStatus


def test_answer_serializes_and_requires_explicit_status():
    answer = Answer("answer-1", AnswerStatus.INSUFFICIENT_EVIDENCE, "Not enough data.")
    assert answer.to_dict()["status"] == AnswerStatus.INSUFFICIENT_EVIDENCE


def test_citation_is_structured():
    claim = Claim("A fact.", (Citation("version-1", "segment-1", "page 1"),))
    assert claim.citations[0].location == "page 1"

