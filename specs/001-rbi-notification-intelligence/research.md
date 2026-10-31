# Research: RBI Notification Intelligence

## Decision: Use a modular two-step grounded RAG workflow first

**Rationale:** A deterministic sequence of ingest/normalize, retrieve, validate
evidence, and generate an attributed answer is easier to teach, test, and debug than
an autonomous multi-agent system. LangGraph will represent explicit workflow state
and transitions; it will not be used to hide reasoning or invent evidence.

**Alternatives considered:** A free-form agent loop was rejected for the first release
because it increases latency, makes abstention harder to guarantee, and obscures the
learning path. A fully hand-written pipeline was rejected because LangChain provides
useful standardized boundaries for loaders, embeddings, retrievers, and model adapters.

## Decision: Keep provider implementations behind ports

**Rationale:** The application will define contracts for chat generation, embeddings,
retrieval, and vector indexing. LangChain-compatible adapters can be selected by
configuration, while domain entities and answer contracts remain stable. The initial
model and vector store must be open-source and runnable locally where practical.

**Alternatives considered:** Binding the application directly to one model or vector
database was rejected because it violates the replacement requirement. Supporting
many providers in the first implementation was rejected because compatibility
contract tests provide better learning value than a large provider matrix.

## Decision: Preserve immutable, content-addressed source artifacts

**Rationale:** Every submitted PDF or table is retained with a SHA-256 hash, source
metadata, retrieval context, and processing run. Replacements create a new version
instead of overwriting history. This supports deduplication, auditability, reprocessing,
and trustworthy citations.

**Alternatives considered:** Latest-ingestion-wins was rejected because a republished
RBI document may change or correct prior content. Overwriting extracted text was
rejected because citation locations and quality comparisons would be lost.

## Decision: Cite positional PDF and table locations

**Rationale:** Material claims will cite document version, page, and text block or
table coordinates when available. Clean text is derived for retrieval, but positional
representations remain the citation substrate. Tabular claims cite dataset, row
identity, column, and reporting period.

**Alternatives considered:** Character offsets alone were rejected because extraction
changes whitespace and reading order. File-level citations alone were rejected because
they are insufficient for learner verification.

## Decision: Stage PDF extraction with explicit quality gates

**Rationale:** Use a born-digital extraction path first, an OCR path for image-only
pages, and table extraction for table-heavy pages. Each extraction run records method,
warnings, and quality signals; low-confidence output remains visible and cannot be
silently treated as authoritative.

**Alternatives considered:** OCR for every page was rejected because it adds cost and
can reduce text fidelity. A single parser for every PDF shape was rejected because
scans and tables have different failure modes.

## Decision: Use Streamlit as the initial user experience

**Rationale:** Streamlit gives learners a fast way to inspect ingestion status,
notification topics, citations, answer uncertainty, and GenAI explanations. The
domain and provider contracts remain UI-independent.

**Alternatives considered:** A separate frontend/backend split was deferred because
the repository starts empty and a modular application is easier to follow. A
production multi-service deployment was deferred until workload and operational
requirements justify it.

## Decision: Docker first; Kubernetes as a documented later target

**Rationale:** Docker provides reproducible local and CI execution immediately.
Kubernetes manifests can teach declarative deployment, jobs, secrets, and health
checks once the single-container demo is stable. Kubernetes is not required for local
validation.

**Alternatives considered:** Kubernetes from day one was rejected as disproportionate
to the initial corpus and learning objective. A hosted-only deployment was rejected
because it weakens local reproducibility and provider interchangeability.

## Decision: Treat MCP as an explicit optional tool boundary

**Rationale:** MCP tools can expose safe operations such as listing source status,
retrieving a cited context segment, or starting a processing run. Tool inputs and
outputs will use the same domain contracts as the Streamlit flow. MCP must not bypass
source attribution, safety policy, or secret handling.

**Alternatives considered:** Making MCP mandatory for all internal calls was rejected
because it adds protocol overhead to the core learning path. Unrestricted tools were
rejected because document content can contain prompt-injection-like text.

## Decision: Add layered evaluation and observability

**Rationale:** Tests will cover parsing, metadata, deduplication, adapter contracts,
abstention, citations, and end-to-end flows. Evaluation fixtures will measure topic
identification, citation correctness, unsupported-answer abstention, and latency.
Logs and metrics will include run IDs and provider status without raw secrets or
unnecessary source content.

**Alternatives considered:** Manual demonstration only was rejected because it cannot
prove the no-hallucination requirement or provider compatibility.

## Decision: Use a deterministic 90-day market-source freshness policy

**Rationale:** An approved indexed market report is eligible for current-market
education only when its effective source date is no more than 90 calendar days before
the question time. Use `publication_date` when present, otherwise the final day of
`reporting_month`; missing, invalid, future, superseded, or older sources are
ineligible. Responses display the effective date, attribution, and an “as of” date.

**Alternatives considered:** Thirty days was too restrictive for monthly reports;
180 days was too stale for current commentary; ingestion-date freshness was rejected
because re-indexing old content must not make it current.

## Decision: Represent source conflicts without choosing an unsupported winner

**Rationale:** When approved sources disagree, preserve each claim and citation,
describe the disagreement, and return a conflicting-evidence status. The assistant
may select a winner only when an explicit authority rule is present in source
metadata; otherwise it must abstain from a definitive conclusion.

**Alternatives considered:** Latest-ingestion-wins and model-selected ranking were
rejected because neither is a reliable authority rule.

## Decision: Use SQLite, checked-in migrations, and local CI

**Rationale:** SQLite plus filesystem artifacts is easy to run on localhost and keeps
provenance inspectable. SQLAlchemy repositories and Alembic migrations provide a
replaceable persistence boundary. CI runs formatting, linting, unit, contract,
integration, and evaluation checks without requiring Docker or Kubernetes.

**Alternatives considered:** A server database was deferred because it adds local
operational overhead. Docker-based CI was deferred with containerization until future
deployment work.

## Decision: Use English-first, accessible localhost interaction

**Rationale:** The first release uses English source interpretation and user-facing
labels, with text alternatives, heading hierarchy, keyboard-accessible controls,
visible focus, readable contrast, and non-color-only status indicators. Translation
keys and isolated learner content keep future localization possible.

**Alternatives considered:** Full multilingual support was deferred until the primary
learning flow is validated.
