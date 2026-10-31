# Implementation Plan: RBI Notification Intelligence

**Branch**: `001-rbi-notification-intelligence` | **Date**: 2026-10-31 | **Spec**:
[spec.md](./spec.md)

**Input**: Feature specification from `/specs/001-rbi-notification-intelligence/spec.md`

## Summary

Build a learning-first Python application that runs on localhost, ingests RBI PDFs and
approved tabular data, preserves immutable source provenance, extracts searchable
content, retrieves grounded context, and returns cited summaries and answers through
Streamlit. The application will use LangChain at provider and document boundaries,
LangGraph for explicit workflow state, and MCP as an optional tool boundary.
Open-source language models, embeddings, and vector stores will be selected through
replaceable adapters rather than embedded in user-facing flows. Docker and Kubernetes
are future enhancements and are not initial runtime dependencies.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: Streamlit, LangChain, LangGraph, an open-source model
adapter, an embedding adapter, a replaceable vector-store adapter, PyMuPDF with an
OCR fallback for difficult PDFs, pandas, and a typed validation library.

**Storage**: Immutable source artifacts and extraction outputs on the local filesystem;
SQLite metadata storage accessed through repositories with versioned migrations; and a
replaceable local vector store for retrieval indexes.

**Testing**: pytest unit tests, contract tests for model/vector-store adapters,
integration tests for ingestion and grounded Q&A, and benchmark evaluation against a
curated corpus.

**Target Platform**: Local Python environment with Streamlit on localhost. Docker
packaging and Kubernetes deployment are future enhancements, not initial acceptance
dependencies.

**Project Type**: Streamlit web application with modular ingestion, retrieval,
orchestration, and provider boundaries.

**Performance Goals**: For the benchmark corpus of 100 notifications and 10,000
tabular records, 95% of supported questions return an initial response within 10
seconds under normal operating conditions; failed processing reports status within 2
minutes.

**Constraints**: No hallucinated source facts; unsupported answers must abstain.
General market commentary uses only dated, maintainer-approved, non-superseded indexed
sources no more than 90 calendar days old, and is never personalized investment
advice. Conflicting approved sources must be shown together without selecting an
unsupported winner. Secrets stay outside source control. Every material answer claim
requires source attribution. The initial interface is English-first and must meet the
documented localhost accessibility baseline.

**Scale/Scope**: Initial benchmark is 100 monthly notifications and 10,000 tabular
records, one primary source language, one Streamlit application, and one compatible
provider configuration at a time.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Learning-first delivery**: PASS. Each workflow has learner-facing explanations and
  the quickstart validates concepts as well as outcomes.
- **Fully documented code**: PASS. The plan requires contracts, data definitions,
  provider boundaries, and documentation updates with implementation changes.
- **Explicit agentic boundaries**: PASS. Ingestion, retrieval, generation, LangGraph
  state, provider adapters, and optional MCP tools have explicit contracts.
- **Correctness and safety**: PASS. Immutable provenance, abstention, dated citations,
  conflict visibility, and no personalized advice are mandatory.
- **Tested, observable simplicity**: PASS. Unit, contract, integration, and benchmark
  tests are required; Streamlit plus a modular monolith is simpler than a distributed
  first release.

No constitution violations require a complexity exception.

## Project Structure

### Documentation (this feature)

```text
specs/001-rbi-notification-intelligence/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   ├── ingestion.md
│   ├── answer.md
│   └── mcp-tools.md
└── tasks.md
```

### Source Code (repository root)

```text
src/financial_assistant/
├── app.py
├── config.py
├── domain/
│   ├── entities.py
│   └── enums.py
├── ingestion/
│   ├── pipeline.py
│   ├── pdf.py
│   ├── tables.py
│   └── provenance.py
├── retrieval/
│   ├── ports.py
│   ├── indexing.py
│   └── search.py
├── providers/
│   ├── llm.py
│   ├── embeddings.py
│   └── vector_store.py
├── workflows/
│   ├── state.py
│   └── graph.py
├── tools/
│   └── mcp.py
└── ui/
    ├── pages.py
    └── explanations.py

tests/
├── unit/
├── contract/
├── integration/
└── evaluation/

data/
├── raw/
├── extracted/
└── fixtures/

.github/workflows/
└── ci.yml
```

**Structure Decision**: Use one modular Python project so learners can trace a source
through ingestion, retrieval, orchestration, and Streamlit without distributed-service
overhead. Use SQLite and filesystem storage locally, with repositories and provider
ports keeping persistence, model, and vector-store replacement possible. CI runs local
quality checks; Docker and Kubernetes files are intentionally deferred until a future
deployment enhancement.

## Complexity Tracking

No violations. MCP remains an optional integration boundary, while the initial runtime
is a single localhost modular application. Docker and Kubernetes are deferred rather
than treated as initial complexity.
