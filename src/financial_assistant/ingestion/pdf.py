"""Native PDF text extraction with an explicit degraded fallback."""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ExtractedPage:
    """Text and citation metadata for one page."""

    page_number: int
    text: str
    quality: str


def extract_pdf(path: Path) -> list[ExtractedPage]:
    """Extract pages using pypdf when installed, otherwise report a clear error."""
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise RuntimeError(
            "PDF extraction requires the optional 'pypdf' dependency. "
            "Install the project dependencies and retry."
        ) from exc
    pages = []
    for index, page in enumerate(PdfReader(str(path)).pages, start=1):
        text = (page.extract_text() or "").strip()
        pages.append(ExtractedPage(index, text, "normal" if text else "degraded"))
    return pages

