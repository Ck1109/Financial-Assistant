# Financial Assistant

Financial Assistant is a learning-first localhost application for exploring
grounded question answering over RBI notifications and tabular data. The project
is intentionally being built as a demonstrable Agentic AI learning application:
each boundary should be understandable, testable, documented, and replaceable.

## Current status

The current implementation is an MVP foundation and one complete notification
interpretation slice:

1. Upload an RBI notification PDF in Streamlit.
2. Preserve the submitted bytes using a SHA-256 content address.
3. Extract page text and page-level provenance.
4. Retrieve relevant local evidence.
5. Produce a summary bounded by the retrieved evidence.
6. Display topics, citations, provider names, and a learning explanation.

The current test suite contains 9 passing tests. The task breakdown is maintained
in [tasks.md](specs/001-rbi-notification-intelligence/tasks.md); 25 of 74 tasks
are currently marked complete. Do not mark a task complete until its behavior is
implemented and validated.

## Prerequisites

- Windows PowerShell
- Python 3.11 or newer
- Git is recommended for collaboration, although the current workspace may not
  have Git installed or initialized

Docker and Kubernetes are future enhancements and are not required to run the
current localhost implementation.

## Setup on Windows

From the project directory:

```powershell
cd D:\Code\Python\Learning\Financial-Assistant
python -m venv .venv
```

If PowerShell permits script activation:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

If PowerShell reports that script execution is disabled, use the virtual
environment directly. Activation is optional:

```powershell
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
```

The project installs Streamlit, pandas, Pydantic, pypdf, pytest, and Ruff.
Provider credentials are not required for the deterministic local adapters.

## Run the tests

With the environment activated:

```powershell
python -m pytest tests -q
python -m compileall -q src tests
```

Without activation:

```powershell
.\.venv\Scripts\python.exe -m pytest tests -q
.\.venv\Scripts\python.exe -m compileall -q src tests
```

Expected test output for the current baseline:

```text
9 passed
```

## Run the application

With the environment activated:

```powershell
streamlit run src\financial_assistant\app.py
```

Without activation:

```powershell
.\.venv\Scripts\streamlit.exe run src\financial_assistant\app.py
```

Open the localhost URL printed by Streamlit, normally
`http://localhost:8501`.

## Run the project locally from a fresh checkout

Use the following complete sequence in PowerShell:

```powershell
cd D:\Code\Python\Learning\Financial-Assistant
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\python.exe -m pytest tests -q
.\.venv\Scripts\streamlit.exe run src\financial_assistant\app.py
```

The final command starts the local Streamlit server. Open the URL shown in the
terminal, usually:

```text
http://localhost:8501
```

If PowerShell activation is enabled on your machine, the equivalent activated
workflow is:

```powershell
cd D:\Code\Python\Learning\Financial-Assistant
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
python -m pytest tests -q
streamlit run src\financial_assistant\app.py
```

Activation is optional. The first sequence calls the executables inside `.venv`
directly and therefore also works when PowerShell blocks `Activate.ps1`.

### Verify the MVP flow

1. Upload a readable RBI notification PDF.
2. Enter or accept the notification title.
3. Select **Interpret notification**.
4. Verify the grounded summary, topics, citations, and learning explanation.
5. Upload the same file again and verify that the application reports an exact
   duplicate rather than creating duplicate stored bytes.

Unreadable PDFs produce an explicit error/insufficiency result. The application
must not turn missing evidence into an invented source fact.

## Configuration

Copy [.env.example](.env.example) to a local `.env` file only if you need to
override defaults. Never commit `.env` or credentials.

Supported settings:

| Variable | Default | Purpose |
|---|---|---|
| `FINANCIAL_ASSISTANT_DATA_DIR` | `data` | Local raw and extracted artifact storage |
| `FINANCIAL_ASSISTANT_LLM_PROVIDER` | `local-deterministic` | Language-model adapter name |
| `FINANCIAL_ASSISTANT_RETRIEVAL_PROVIDER` | `local-keyword` | Retrieval adapter name |

The current adapters are deterministic and local. They are deliberately small
teaching implementations, not production-grade model or vector database
integrations.

## Repository map

```text
src/financial_assistant/
├── app.py                         # Streamlit localhost entry point
├── config.py                      # Environment-backed settings
├── domain/
│   ├── entities.py                # Typed provenance and answer entities
│   └── enums.py                   # Controlled status values
├── ingestion/
│   ├── pdf.py                     # Native PDF extraction
│   └── provenance.py              # Page-to-citation segments
├── analysis/
│   └── topics.py                  # Transparent topic extraction
├── providers/
│   ├── llm.py                     # Language-model port and local adapter
│   ├── embeddings.py              # Embedding port and local adapter
│   ├── vector_store.py             # Retrieval port and local adapter
│   └── factory.py                 # Provider construction
├── retrieval/
│   └── search.py                  # Provider-neutral search service
├── safety/
│   └── policy.py                  # Citation and advice safety checks
├── storage/
│   └── artifacts.py               # SHA-256 content-addressed storage
├── workflows/
│   └── notification.py            # Grounded notification workflow
└── observability.py               # Run IDs and redaction

tests/
├── unit/
├── contract/
├── integration/
└── evaluation/
```

See [architecture.md](docs/architecture.md) for the current design rationale.
The complete product design is in [plan.md](specs/001-rbi-notification-intelligence/plan.md),
[spec.md](specs/001-rbi-notification-intelligence/spec.md), and the
[contracts](specs/001-rbi-notification-intelligence/contracts/) directory.

## Recommended next work

Continue in task order, starting with the remaining foundation and MVP tasks:

1. Add SQLite metadata persistence and Alembic migrations (`T009`, `T070`).
2. Add deterministic sample PDF, tabular, malformed, duplicate, and conflicting
   fixtures (`T019`).
3. Add PDF extraction contract tests and OCR fallback (`T021`, `T024`).
4. Add extraction-run orchestration and explicit workflow state (`T025`, `T029`).
5. Separate the Streamlit notification UI into the planned UI modules
   (`T031`, `T032`).
6. Implement tabular ingestion and cross-source grounded Q&A (Phase 4).
7. Add learning content, source management, MCP boundaries, accessibility
   validation, and CI.

Before implementing the later market and conflict tasks, reconcile the latest
specification decisions with the older planning text: the specification uses
maintainer judgment for market-source freshness and retrieval-score selection
when sources conflict.

## Safety and contribution rules

- Never fabricate an answer when indexed evidence is missing.
- Every answered material claim must have a citation.
- Do not provide personalized buy, sell, or hold recommendations.
- Keep secrets and private source data out of source control.
- Preserve source bytes and provenance; do not overwrite historical versions.
- Add focused tests and documentation with each behavior change.
- Prefer explicit provider and workflow contracts over hidden framework behavior.
- Do not expose private chain-of-thought; expose observable stages, inputs,
  outputs, citations, and limitations instead.

## Deferred scope

Docker packaging, Kubernetes deployment, live market-data retrieval, multilingual
support, and production-scale model/vector-store integrations are intentionally
deferred. The initial target is a clear, safe, locally runnable learning demo.
