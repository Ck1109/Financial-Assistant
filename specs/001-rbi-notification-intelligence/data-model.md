# Data Model: RBI Notification Intelligence

## SourceArtifact

Represents the immutable submitted file.

- `artifact_id`: stable identifier.
- `sha256`: required content hash; unique for exact duplicates.
- `source_uri`: origin or maintainer-provided location.
- `retrieved_at`: retrieval timestamp when applicable.
- `media_type`: PDF or supported tabular format.
- `byte_size`: original size.
- `created_at`: record creation timestamp.

Rules: bytes are never overwritten. An exact hash match is a duplicate. A changed
file creates a new artifact even when the URI is unchanged.

## DocumentVersion

Represents a logical RBI notification or approved market report derived from an
artifact.

- `document_id`: logical document identity.
- `version_id`: immutable version identifier.
- `artifact_id`: source artifact reference.
- `document_type`: RBI notification, market report, or other approved source.
- `title`: source title.
- `publication_date`: source publication date when known.
- `reporting_month`: month represented by the source when applicable.
- `authority`: issuing organization.
- `language`: primary language.
- `status`: pending, processing, indexed, degraded, rejected, or superseded.
- `provenance_note`: maintainer or extraction note.
- `approval_status`: pending, approved, revoked, or superseded.
- `approved_at`: timestamp of maintainer approval when applicable.

Rules: publication date and reporting month are distinct. A superseded version
remains available for audit and citation. Current-market eligibility uses publication
date, or the final day of reporting month when publication date is absent, and rejects
sources older than 90 calendar days, future-dated, undated, revoked, or superseded.

## TabularDataset

Represents structured data associated with an artifact or document version.

- `dataset_id`: stable dataset identifier.
- `version_id`: source version reference.
- `schema_version`: normalized schema version.
- `columns`: names, types, units, and descriptions.
- `reporting_period`: period represented by the rows.
- `row_count`: validated row count.
- `validation_status`: passed, warning, or failed.
- `duplicate_policy`: preserved, merged, or rejected with an explanation.

Rules: missing values, units, and duplicate rows are reported rather than silently
discarded.

## ExtractionRun

Represents one attempt to turn an artifact into searchable representations.

- `run_id`: unique processing identifier.
- `artifact_id`: input artifact.
- `method`: native PDF, OCR, table extraction, tabular normalization, or combination.
- `started_at`, `completed_at`: timestamps.
- `status`: queued, running, completed, degraded, or failed.
- `warnings`: non-fatal quality warnings.
- `error_code`, `error_message`: actionable failure details.
- `quality_signals`: confidence and coverage metrics.

State transitions: queued → running → completed/degraded/failed. A new run never
mutates a previous run.

## ContextSegment

Represents a searchable and citeable unit.

- `segment_id`: stable identifier.
- `version_id`: source version.
- `segment_type`: text block, page, table, row group, or table cell.
- `page_number`: PDF page when applicable.
- `location`: bounding box, table coordinates, or row/column coordinates.
- `text`: normalized retrieval text.
- `raw_reference`: link to the preserved extraction representation.
- `embedding_reference`: provider-specific index reference.
- `quality`: extraction quality status.

## Topic

Represents a normalized subject identified in a document.

- `topic_id`: stable identifier.
- `version_id`: source version.
- `label`: learner-readable topic name.
- `aliases`: observed names.
- `context_segment_ids`: supporting segments.
- `confidence`: extraction confidence.

## Question

Represents a user request.

- `question_id`: unique request identifier.
- `text`: original question.
- `interpreted_topic`: optional normalized topic.
- `time_scope`: requested period if identified.
- `question_type`: fact lookup, comparison, explanation, or market education.
- `created_at`: request timestamp.

## Answer

Represents the user-visible response.

- `answer_id`: unique response identifier.
- `question_id`: source question.
- `status`: answered, insufficient-evidence, conflicting-evidence, or failed.
- `summary`: direct response.
- `claims`: material claims with citation references.
- `uncertainty`: known limitations and conflicts.
- `effective_source_date`: date used for market-source freshness when applicable.
- `as_of_date`: question-time date shown for market commentary.
- `conflict_set`: competing claims and citations when evidence conflicts.
- `market_education_label`: required for non-RBI general commentary.
- `learning_explanation`: stages, inputs, outputs, and limitations.
- `provider_snapshot`: model and retrieval provider identifiers.
- `created_at`: response timestamp.

Rules: an answered claim must have at least one citation. Insufficient evidence must
be explicit. Personalized buy/sell/hold recommendations are invalid.

## ProcessingRun and ProviderConfiguration

`ProcessingRun` captures ingestion or analysis status, inputs, warnings, and errors.
`ProviderConfiguration` records the selected model, embedding, and vector-store
adapter versions and compatibility status. Provider identifiers are operational
metadata, not part of the user-facing answer contract.

## Relationships

```text
SourceArtifact 1 ── * DocumentVersion
DocumentVersion 1 ── * ExtractionRun
DocumentVersion 1 ── * ContextSegment
DocumentVersion 1 ── * Topic
DocumentVersion 1 ── 0..1 TabularDataset
Question 1 ── 0..1 Answer
Answer * ── * ContextSegment (through citations)
ProviderConfiguration 1 ── * ProcessingRun
```
