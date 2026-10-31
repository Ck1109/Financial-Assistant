---
description: "Task list for RBI Notification Intelligence"
---

# Tasks: RBI Notification Intelligence

**Input**: Design documents from
`/specs/001-rbi-notification-intelligence/`

**Prerequisites**: [plan.md](./plan.md), [spec.md](./spec.md),
[research.md](./research.md), [data-model.md](./data-model.md), [contracts/](./contracts/),
and [quickstart.md](./quickstart.md)

**Implementation scope**: The initial delivery runs locally on localhost. Docker and
Kubernetes are future enhancements and are not implementation prerequisites.

## Phase 1: Setup

**Purpose**: Initialize the local Python project and its documented development
workflow.

- [X] T001 Create the `src/financial_assistant`, `tests/{unit,contract,integration,evaluation}`, `data/{raw,extracted,fixtures}`, and `docs` directories
- [X] T002 Create `pyproject.toml` with Python 3.11+, runtime dependencies, development dependencies, pytest configuration, and package metadata
- [X] T003 [P] Create `.gitignore` and `.env.example` that exclude secrets, local databases, raw source data, extracted artifacts, and provider credentials
- [X] T004 [P] Create `README.md` with localhost setup, supported fixture data, learning goals, and an explicit note that Docker and Kubernetes are future scope
- [X] T005 [P] Create `src/financial_assistant/config.py` with typed environment configuration and actionable errors for missing required local settings
- [X] T006 [P] Create `tests/conftest.py` with isolated temporary storage, deterministic fixture configuration, and shared test factories
- [ ] T069 [P] Create `.github/workflows/ci.yml` for formatting, linting, unit, contract, integration, and evaluation checks without Docker or Kubernetes

---

## Phase 2: Foundational

**Purpose**: Implement blocking domain, persistence, provider, safety, and observability
boundaries required by every user story.

**Checkpoint**: The foundation must be complete before user-story implementation begins.

- [X] T007 Define domain enums and typed entities in `src/financial_assistant/domain/enums.py` and `src/financial_assistant/domain/entities.py` for SourceArtifact, DocumentVersion, TabularDataset, ExtractionRun, ContextSegment, Topic, Question, Answer, ProcessingRun, and ProviderConfiguration
- [X] T008 [P] Add unit tests for required fields, status values, relationships, and invalid state transitions in `tests/unit/test_domain_entities.py`
- [ ] T009 Implement metadata persistence and migrations for source artifacts, document versions, extraction runs, datasets, topics, questions, answers, and provider configurations in `src/financial_assistant/storage/metadata.py`
- [ ] T070 [P] Configure SQLite repositories and checked-in Alembic migrations for local metadata storage in `src/financial_assistant/storage/`
- [X] T010 [P] Implement content-addressed artifact storage that preserves submitted bytes and SHA-256 hashes in `src/financial_assistant/storage/artifacts.py`
- [X] T011 [P] Add repository tests for exact-duplicate detection, immutable replacements, and source-version retention in `tests/unit/test_storage.py`
- [X] T012 Define model, embedding, retrieval, and vector-store ports in `src/financial_assistant/providers/llm.py`, `src/financial_assistant/providers/embeddings.py`, and `src/financial_assistant/providers/vector_store.py`
- [X] T013 [P] Implement configuration-based provider factories with open-source local provider defaults and explicit unsupported-provider errors in `src/financial_assistant/providers/factory.py`
- [X] T014 [P] Add provider contract tests for stable inputs, outputs, errors, and replacement behavior in `tests/contract/test_provider_contracts.py`
- [X] T015 Define structured logging, run identifiers, error codes, and sensitive-data redaction in `src/financial_assistant/observability.py`
- [X] T016 [P] Add observability tests for redaction, failure events, provider status, and citation-coverage metrics in `tests/unit/test_observability.py`
- [X] T017 Define shared citation, uncertainty, abstention, and market-education safety policies in `src/financial_assistant/safety/policy.py`
- [X] T018 [P] Add safety-policy tests covering unsupported claims, conflicting sources, stale approved sources, and personalized buy/sell/hold requests in `tests/unit/test_safety_policy.py`
- [ ] T019 Create deterministic sample PDF, tabular, malformed, duplicate, and conflicting-source fixtures in `data/fixtures/`
- [X] T020 [P] Document local configuration, data classification, safe sample-data handling, and provider replacement boundaries in `docs/architecture.md`

---

## Phase 3: User Story 1 - Understand a Monthly RBI Notification (Priority: P1)

**Goal**: Ingest and interpret one monthly RBI notification with topics, context,
plain-language summary, uncertainty, and traceable citations.

**Independent Test**: With one fixture notification, a user can see its month, source
identity, summary, topics, context, limitations, and page-level citations.

### Tests for User Story 1

- [ ] T021 [P] [US1] Add PDF extraction contract tests for text pages, scanned pages, tables, reading order, and extraction warnings in `tests/contract/test_pdf_extraction.py`
- [X] T022 [P] [US1] Add notification interpretation integration tests for summary, topic separation, dates, source attribution, and unreadable-source abstention in `tests/integration/test_notification_interpretation.py`

### Implementation for User Story 1

- [X] T023 [P] [US1] Implement native PDF extraction with page and positional metadata in `src/financial_assistant/ingestion/pdf.py`
- [ ] T024 [P] [US1] Implement OCR fallback and extraction-quality signals for image-only pages in `src/financial_assistant/ingestion/ocr.py`
- [ ] T025 [US1] Implement extraction-run orchestration, quality status, warnings, and failure persistence in `src/financial_assistant/ingestion/pipeline.py`
- [X] T026 [US1] Implement traceable text-block and page ContextSegment creation in `src/financial_assistant/ingestion/provenance.py`
- [X] T027 [US1] Implement topic, entity, date, and contextual-relationship extraction over notification segments in `src/financial_assistant/analysis/topics.py`
- [X] T028 [US1] Implement indexed-context retrieval for a selected notification in `src/financial_assistant/retrieval/search.py`
- [ ] T029 [US1] Implement the explicit notification-analysis workflow state and transitions in `src/financial_assistant/workflows/state.py`
- [X] T030 [US1] Implement grounded notification summarization with claim-level citations and explicit uncertainty in `src/financial_assistant/workflows/notification.py`
- [ ] T031 [US1] Implement the Streamlit notification-selection, summary, topic, context, citation, and limitation views in `src/financial_assistant/ui/notifications.py`
- [ ] T032 [US1] Add actionable ingestion and interpretation error presentation without exposing secrets or raw sensitive content in `src/financial_assistant/ui/errors.py`
- [X] T033 [US1] Add the localhost Streamlit entry point and local storage initialization in `src/financial_assistant/app.py`

**Checkpoint**: User Story 1 is independently demonstrable and is the recommended MVP.

---

## Phase 4: User Story 2 - Ask Questions Across the Knowledge Base (Priority: P1)

**Goal**: Answer questions across PDF and tabular sources with grounded citations,
explicit insufficiency, conflict handling, and general market education only from
approved indexed sources.

**Independent Test**: A user can ask known-answer, multi-source, unsupported, and
market-condition questions and receive the correct answer status, source locations,
dates, uncertainty, and safety labeling.

### Tests for User Story 2

- [ ] T034 [P] [US2] Add tabular-ingestion contract tests for schemas, units, missing values, duplicate rows, and reporting periods in `tests/contract/test_tabular_ingestion.py`
- [ ] T035 [P] [US2] Add answer-contract tests for citations, insufficient evidence, conflicting evidence, market-education labels, and prohibited personalized recommendations in `tests/contract/test_answer_contract.py`
- [ ] T036 [P] [US2] Add question-answering integration tests for single-source, multi-source, PDF-plus-table, unsupported, stale-market, and conflicting-source questions in `tests/integration/test_question_answering.py`
- [ ] T037 [P] [US2] Add benchmark evaluation fixtures and scoring for citation correctness, abstention, topic coverage, and response latency in `tests/evaluation/test_rag_quality.py`

### Implementation for User Story 2

- [ ] T038 [P] [US2] Implement tabular normalization with column, type, unit, missing-value, duplicate-row, and reporting-period metadata in `src/financial_assistant/ingestion/tables.py`
- [ ] T039 [US2] Implement table, row-group, and cell ContextSegment provenance in `src/financial_assistant/ingestion/table_provenance.py`
- [ ] T040 [US2] Implement provider-backed indexing and retrieval ports for text and tabular segments in `src/financial_assistant/retrieval/indexing.py`
- [ ] T041 [US2] Implement question classification for fact lookup, comparison, explanation, and market education in `src/financial_assistant/analysis/questions.py`
- [ ] T042 [US2] Implement evidence sufficiency, freshness, source approval, and conflict assessment in `src/financial_assistant/retrieval/evidence.py`
- [ ] T043 [US2] Implement explicit LangGraph question-answering state, retrieval, generation, validation, and abstention transitions in `src/financial_assistant/workflows/qa_graph.py`
- [ ] T044 [US2] Implement the stable Answer contract with claim citations, uncertainty, provider snapshot, and market-education labeling in `src/financial_assistant/workflows/answers.py`
- [ ] T045 [US2] Implement the Streamlit question form, source filters, answer display, citations, conflicts, insufficiency, and market-education disclaimer in `src/financial_assistant/ui/qa.py`
- [ ] T046 [US2] Add benchmark-corpus loading and the 100-notification/10,000-record evaluation configuration in `src/financial_assistant/evaluation/benchmarks.py`

**Checkpoint**: User Stories 1 and 2 independently support notification interpretation
and grounded cross-source Q&A.

---

## Phase 5: User Story 3 - Learn How the Assistant Works (Priority: P2)

**Goal**: Explain the observable GenAI concepts, workflow stages, inputs, outputs,
limitations, and provider boundaries without exposing private chain-of-thought.

**Independent Test**: A learner can inspect explanations for ingestion, retrieval,
topic identification, answer generation, citation, uncertainty, and provider
replacement after completing the corresponding flows.

### Tests for User Story 3

- [ ] T047 [P] [US3] Add learning-content coverage tests requiring explanations for every named workflow stage and failure state in `tests/unit/test_learning_explanations.py`
- [ ] T048 [P] [US3] Add learner evaluation criteria and scoring fixtures for ingestion, retrieval, attribution, and uncertainty concepts in `tests/evaluation/test_learning_outcomes.py`

### Implementation for User Story 3

- [ ] T049 [P] [US3] Define learner-facing concept content for ingestion, chunking, embeddings, retrieval, grounding, orchestration, providers, citations, and abstention in `src/financial_assistant/ui/learning_content.py`
- [ ] T050 [US3] Implement sanitized workflow-stage explanations from observable state, inputs, outputs, and limitations in `src/financial_assistant/ui/explanations.py`
- [ ] T051 [US3] Add explanation panels to notification and Q&A views without exposing hidden chain-of-thought or secrets in `src/financial_assistant/ui/pages.py`
- [ ] T052 [US3] Add provider replacement and MCP boundary explanations to the local learning experience in `docs/learning-guide.md`

**Checkpoint**: Every completed and failed primary flow includes a beginner-readable
explanation of what happened and why.

---

## Phase 6: User Story 4 - Add and Review Source Data (Priority: P2)

**Goal**: Let a maintainer add, inspect, deduplicate, reprocess, and correct PDF and
tabular sources while preserving provenance and prior runs.

**Independent Test**: A maintainer can add valid, duplicate, malformed, empty,
unsupported, replaced, and conflicting sources and identify status and corrective
action for each.

### Tests for User Story 4

- [ ] T053 [P] [US4] Add ingestion integration tests for valid, duplicate, malformed, empty, unsupported, replaced, and conflicting sources in `tests/integration/test_source_management.py`
- [ ] T054 [P] [US4] Add processing-status contract tests for queued, running, completed, degraded, and failed states in `tests/contract/test_processing_status.py`

### Implementation for User Story 4

- [ ] T055 [US4] Implement source submission validation, metadata capture, exact-hash deduplication, and immutable replacement handling in `src/financial_assistant/ingestion/submission.py`
- [ ] T056 [US4] Implement reprocessing with retained historical ExtractionRun records and superseded DocumentVersion links in `src/financial_assistant/ingestion/reprocessing.py`
- [ ] T057 [US4] Implement source status, warnings, error codes, corrective actions, and approval metadata in `src/financial_assistant/ingestion/status.py`
- [ ] T058 [US4] Implement maintainer source-management views for upload, metadata review, status, errors, duplicate detection, and reprocessing in `src/financial_assistant/ui/source_management.py`
- [ ] T059 [US4] Implement optional MCP read-only source-status and context-segment tools using shared application services in `src/financial_assistant/tools/mcp.py`
- [ ] T060 [US4] Add MCP contract tests for input validation, authorization boundaries, provenance, prompt-injection-safe handling, and stable errors in `tests/contract/test_mcp_tools.py`

**Checkpoint**: Maintainers can manage source lifecycle without overwriting history or
making unapproved data searchable.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Complete local readiness, documentation, quality gates, and explicit
future-scope boundaries.

- [ ] T061 [P] Add unit and integration coverage for all FR-001 through FR-016 invariants in `tests/`
- [ ] T062 [P] Add local health/status diagnostics for provider availability, storage paths, and index readiness in `src/financial_assistant/diagnostics.py`
- [ ] T063 [P] Add structured metrics for processing duration, extraction quality, retrieval coverage, abstention rate, citation coverage, and answer latency in `src/financial_assistant/observability.py`
- [ ] T064 [P] Document the localhost quickstart and expected outcomes in `quickstart.md` and `README.md`
- [ ] T065 [P] Document Docker packaging and Kubernetes deployment as future enhancements only, without adding them as initial acceptance prerequisites in `docs/future-deployment.md`
- [ ] T066 Review all user-facing financial language for educational labeling, no personalized advice, source dates, and uncertainty disclosure in `src/financial_assistant/ui/`
- [ ] T067 Review all source and provider boundaries for secrets, prompt-injection handling, unnecessary raw-content logging, and actionable failures in `src/financial_assistant/`
- [ ] T068 Run the complete local validation sequence from `specs/001-rbi-notification-intelligence/quickstart.md` and record any remaining gaps in `docs/validation-notes.md`
- [ ] T071 [P] Add boundary fixtures and evaluation assertions for 89-day, 90-day, 91-day, undated, future-dated, revoked, and superseded market sources in `tests/evaluation/test_market_freshness.py`
- [ ] T072 [P] Implement conflict-set presentation and authority-rule abstention in `src/financial_assistant/retrieval/conflicts.py` and `src/financial_assistant/ui/conflicts.py`
- [ ] T073 [P] Add English-first accessibility requirements for text alternatives, heading hierarchy, keyboard access, visible focus, contrast, and non-color-only status in `docs/accessibility.md`
- [ ] T074 [P] Add localization-ready message keys and document English-only initial scope in `src/financial_assistant/ui/messages.py` and `docs/localization.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 Setup**: No dependencies; tasks T003-T006 can run in parallel after the
  project layout is agreed, and T069 follows T002.
  directory layout is agreed.
- **Phase 2 Foundational**: Depends on Phase 1; T007, T070, T010, T012, T015, T017, and
  T019 establish the shared boundaries and can be developed in parallel.
- **Phase 3 User Story 1**: Depends on Phase 2; delivers the MVP.
- **Phase 4 User Story 2**: Depends on Phase 2 and the shared entities/provider ports;
  it may reuse US1 retrieval and provenance components.
- **Phase 5 User Story 3**: Depends on the observable states and contracts from US1
  and US2, but its content authoring tasks can begin after Phase 2.
- **Phase 6 User Story 4**: Depends on Phase 2; MCP and maintainer views depend on
  source-status services but not on the learner-facing answer UI.
- **Phase 7 Polish**: Depends on the desired user stories being complete.

### User Story Dependencies

- **US1 (P1)**: Independent after Phase 2; recommended MVP.
- **US2 (P1)**: Independent after Phase 2; reuses shared provenance and provider ports
  and may integrate with US1's retrieval components.
- **US3 (P2)**: Can begin after Phase 2; final integration depends on US1 and US2
  workflow state.
- **US4 (P2)**: Independent after Phase 2; provides data lifecycle services used by
  US1 and US2.

### Parallel Opportunities

- Setup tasks T003-T006.
- Foundational tasks T008, T010-T011, T013-T014, T016-T018, and T019-T020.
- US1 extraction, OCR, and contract-test tasks T021-T024.
- US2 tabular, answer-contract, benchmark, and provider-index tasks T034-T040.
- US3 content, evaluation, and explanation tasks T047-T052.
- US4 integration and status contract tests T053-T054.
- Polish documentation, diagnostics, metrics, freshness, conflict, accessibility, and
  localization tasks T061-T072.

## Implementation Strategy

1. **MVP**: Complete Phases 1-3 and demonstrate one RBI PDF from ingestion through
   cited notification interpretation on localhost.
2. **Grounded Q&A**: Add Phase 4 for PDF/table questions, abstention, conflicts, and
   approved indexed market education.
3. **Learning experience**: Add Phase 5 so every workflow explains the GenAI concepts
   involved.
4. **Maintainer lifecycle**: Add Phase 6 for source management and optional MCP tools.
5. **Hardening**: Complete Phase 7 and validate against the measurable outcomes.

Every task follows the required checklist format with a sequential ID, optional
parallel marker, story label where applicable, and a concrete file path.
