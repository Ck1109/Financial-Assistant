"""Conversion of extracted pages into citeable context segments."""

from financial_assistant.domain.entities import ContextSegment, new_id
from .pdf import ExtractedPage


def pages_to_segments(version_id: str, pages: list[ExtractedPage]) -> list[ContextSegment]:
    """Create one traceable segment per extracted page."""
    return [
        ContextSegment(
            segment_id=new_id("segment"),
            version_id=version_id,
            segment_type="page",
            text=page.text,
            location=f"page {page.page_number}",
            page_number=page.page_number,
            quality=page.quality,
        )
        for page in pages
        if page.text
    ]

