# Ingestion Contract

## Submit Source

The ingestion boundary accepts a source artifact and metadata:

```json
{
  "source_uri": "https://example.invalid/rbi/notification.pdf",
  "media_type": "application/pdf",
  "document_type": "rbi_notification",
  "title": "Example notification",
  "publication_date": "2026-10-01",
  "reporting_month": "2026-09",
  "authority": "Reserve Bank of India",
  "language": "en"
}
```

The submitted bytes are preserved and hashed before extraction. Metadata validation
must reject unsupported media types and invalid dates with actionable errors.

## Processing Result

```json
{
  "run_id": "run-identifier",
  "artifact_id": "artifact-identifier",
  "version_id": "version-identifier",
  "status": "completed",
  "counts": {
    "pages": 12,
    "segments": 84,
    "tables": 3,
    "rows": 120
  },
  "warnings": [],
  "error": null
}
```

Allowed statuses are `queued`, `running`, `completed`, `degraded`, and `failed`.
Failed runs must include a stable error code and corrective message. A completed or
degraded run must expose the source version and citeable segments.

## Idempotency and provenance

The SHA-256 content hash is the exact-duplicate key. Reprocessing the same artifact
may create a new extraction run but must not create a conflicting source copy.
Replaced content gets a new artifact and document version.
