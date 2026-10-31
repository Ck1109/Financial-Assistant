"""Streamlit entry point for the localhost learning demonstration."""

from pathlib import Path

import streamlit as st

from financial_assistant.config import Settings
from financial_assistant.domain.entities import DocumentVersion, new_id
from financial_assistant.ingestion.pdf import extract_pdf
from financial_assistant.ingestion.provenance import pages_to_segments
from financial_assistant.providers.llm import DeterministicLanguageModel
from financial_assistant.providers.vector_store import KeywordVectorStore
from financial_assistant.safety.policy import insufficient_answer
from financial_assistant.storage.artifacts import ArtifactStore
from financial_assistant.workflows.notification import interpret_notification


def main() -> None:
    """Render the safe local demo and explain its observable stages."""
    settings = Settings.from_env()
    st.set_page_config(page_title="Financial Assistant", layout="wide")
    st.title("Financial Assistant")
    st.caption("Learning-first, grounded RBI notification interpretation")
    st.info("This local demo uses replaceable provider ports and does not provide personalized investment advice.")
    st.subheader("Provider configuration")
    st.write({"language_model": settings.llm_provider, "retrieval": settings.retrieval_provider})
    st.subheader("Learning workflow")
    st.markdown("1. Preserve source bytes and provenance.\n2. Extract citeable context.\n3. Retrieve relevant evidence.\n4. Summarize only supported evidence.")
    st.caption(f"Local data directory: {Path(settings.data_dir).resolve()}")
    uploaded = st.file_uploader("Upload an RBI notification PDF", type=["pdf"])
    if uploaded is None:
        st.info("Upload a PDF to run the local, citeable interpretation workflow.")
        return
    title = st.text_input("Notification title", value=uploaded.name)
    if not st.button("Interpret notification"):
        return
    try:
        stored = ArtifactStore(settings.data_dir / "raw").save(
            uploaded.getvalue(), uploaded.name, "application/pdf"
        )
        version_id = new_id("version")
        document = DocumentVersion(
            document_id=new_id("document"),
            version_id=version_id,
            artifact_id=stored.artifact.artifact_id,
            document_type="rbi_notification",
            title=title,
        )
        pages = extract_pdf(stored.path)
        segments = pages_to_segments(version_id, pages)
        answer, topics = interpret_notification(
            document, segments, DeterministicLanguageModel(), KeywordVectorStore()
        )
        st.subheader("Grounded summary")
        st.write(answer.summary)
        st.subheader("Topics")
        st.write([topic.label for topic in topics] or ["No supported topics identified."])
        st.subheader("Citations")
        for claim in answer.claims:
            for citation in claim.citations:
                st.write(f"{citation.location} ({citation.segment_id})")
        st.subheader("Learning explanation")
        st.write(answer.learning_explanation)
        if stored.duplicate:
            st.info("This exact source was already preserved; no duplicate bytes were created.")
    except (RuntimeError, ValueError, OSError) as exc:
        st.error(f"Interpretation failed: {exc}")
        st.write(insufficient_answer(str(exc), {
            "language_model": DeterministicLanguageModel.name,
            "retrieval": KeywordVectorStore.name,
        }).to_dict())


if __name__ == "__main__":
    main()
