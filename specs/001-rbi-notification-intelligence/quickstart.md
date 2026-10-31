# Quickstart Validation Guide

This guide validates the first demonstrable slice without requiring Kubernetes or a
live external market-data service.

## Prerequisites

- Python 3.11 or newer
- Git
- Docker Desktop or an equivalent Docker runtime
- A local open-source model and embedding configuration supported by the selected
  provider adapters
- Fixture files from `data/fixtures/`: one representative RBI PDF, one table, and
  one malformed or unsupported file

## Local setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

Copy the example configuration to a local, untracked environment file and set the
model, embedding, and vector-store provider names. Do not commit credentials or
private source data.

## Run focused validation

```powershell
pytest tests/unit tests/contract
pytest tests/integration
pytest tests/evaluation
streamlit run src/financial_assistant/app.py
```

Expected outcomes:

1. Unit tests validate metadata, hashes, extraction states, citation construction,
   abstention rules, and answer safety invariants.
2. Contract tests show that at least one configured model and vector-store adapter
   satisfy the provider interfaces.
3. Integration tests ingest the PDF and table, show source status, identify topics,
   answer a known question with page/table citations, and abstain for an unsupported
   question.
4. Evaluation tests report topic/date accuracy, citation correctness, unsupported
   answer abstention, and the benchmark response-time target.
5. Streamlit shows ingestion status, notification interpretation, question answering,
   citations, uncertainty, and a learner-facing explanation of ingestion, retrieval,
   and answer generation.

## Deferred deployment scope

Docker packaging and Kubernetes deployment are future enhancements. They are not
required for this feature's local acceptance and must not be prerequisites for running
the localhost flow.

See [data-model.md](./data-model.md), [contracts/ingestion.md](./contracts/ingestion.md),
and [contracts/answer.md](./contracts/answer.md) for the entities and interface
invariants validated by this guide.
