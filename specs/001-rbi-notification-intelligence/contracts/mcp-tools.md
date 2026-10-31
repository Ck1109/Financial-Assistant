# MCP Tool Contract

MCP is an optional integration boundary. Tools must call the same application services
as Streamlit and must not bypass provenance, answer validation, or safety policy.

## `list_source_status`

Input: optional `document_type`, `reporting_month`, and `status` filters.

Output: source identifiers, titles, reporting periods, current status, and warnings.
No raw source bytes or secrets are returned by default.

## `get_context_segment`

Input: `version_id` and `segment_id`.

Output: citeable segment text, source title, page or table location, extraction
quality, and provenance. Access is read-only.

## `start_processing_run`

Input: a maintainer-authorized artifact reference and processing options.

Output: `run_id`, accepted status, and validation warnings. The tool must reject
unknown artifacts, unsupported options, and unauthorized operations.

## Security and failure behavior

Tool input is treated as untrusted data. Retrieved document text must never be treated
as executable instructions. Errors use stable codes and actionable messages. Tool
responses must preserve the same source and safety guarantees as the answer contract.
