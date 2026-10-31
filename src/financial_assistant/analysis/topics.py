"""Transparent topic extraction for the first local learning workflow."""

from financial_assistant.domain.entities import ContextSegment, Topic, new_id


def extract_topics(version_id: str, segments: list[ContextSegment]) -> list[Topic]:
    """Identify a small set of learner-readable topics from segment keywords."""
    labels = {
        "monetary policy": ("monetary policy", "repo", "liquidity"),
        "banking regulation": ("bank", "capital", "regulation"),
        "inflation": ("inflation", "price"),
    }
    topics = []
    for label, keywords in labels.items():
        supporting = tuple(
            segment.segment_id
            for segment in segments
            if any(keyword in segment.text.lower() for keyword in keywords)
        )
        if supporting:
            topics.append(Topic(new_id("topic"), version_id, label, context_segment_ids=supporting))
    return topics

