from financial_assistant.domain.entities import ContextSegment, DocumentVersion
from financial_assistant.providers.llm import DeterministicLanguageModel
from financial_assistant.providers.vector_store import KeywordVectorStore
from financial_assistant.workflows.notification import interpret_notification


def test_notification_interpretation_is_cited_and_topics_are_exposed():
    document = DocumentVersion(
        "document-1", "version-1", "artifact-1", "rbi_notification", "Monetary policy update"
    )
    segments = [
        ContextSegment("segment-1", "version-1", "page", "The repo rate and liquidity conditions were reviewed.", "page 1", 1),
        ContextSegment("segment-2", "version-1", "page", "Inflation risks remain monitored.", "page 2", 2),
    ]
    answer, topics = interpret_notification(
        document, segments, DeterministicLanguageModel(), KeywordVectorStore()
    )
    assert answer.claims[0].citations[0].location == "page 1"
    assert {topic.label for topic in topics} == {"monetary policy", "inflation"}
