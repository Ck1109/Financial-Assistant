"""Grounded notification interpretation workflow."""

from financial_assistant.analysis.topics import extract_topics
from financial_assistant.domain.entities import Answer, ContextSegment, DocumentVersion, Claim
from financial_assistant.domain.enums import AnswerStatus
from financial_assistant.providers.llm import LanguageModel
from financial_assistant.providers.vector_store import VectorStore
from financial_assistant.safety.policy import cited_claim, insufficient_answer, validate_answer


def interpret_notification(
    document: DocumentVersion,
    segments: list[ContextSegment],
    model: LanguageModel,
    retrieval: VectorStore,
) -> tuple[Answer, list]:
    """Retrieve evidence, summarize only that evidence, and return topics."""
    retrieved = retrieval.search(document.title, segments)
    evidence = [item.segment for item in retrieved] or segments
    if not evidence:
        return insufficient_answer("The notification has no extracted text.", {"language_model": model.name, "retrieval": retrieval.name}), []
    summary = model.summarize([segment.text for segment in evidence], document.title)
    claim = cited_claim(summary, document.version_id, evidence[0].segment_id, evidence[0].location)
    answer = Answer(
        answer_id=f"answer-{document.version_id}",
        status=AnswerStatus.ANSWERED,
        summary=summary,
        claims=(claim,),
        learning_explanation={
            "stages": [
                {"name": "retrieval", "purpose": "Find relevant indexed context."},
                {"name": "grounding", "purpose": "Keep the summary bounded by cited evidence."},
            ],
            "limitations": ["The local demonstration summarizes extracted text and does not expose hidden reasoning."],
        },
        provider_snapshot={"language_model": model.name, "retrieval": retrieval.name},
    )
    validate_answer(answer)
    return answer, extract_topics(document.version_id, evidence)

