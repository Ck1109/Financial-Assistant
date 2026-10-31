# Answer Contract

## Response shape

```json
{
  "answer_id": "answer-identifier",
  "status": "answered",
  "summary": "Plain-language answer.",
  "claims": [
    {
      "text": "Material claim.",
      "citations": [
        {
          "version_id": "version-identifier",
          "segment_id": "segment-identifier",
          "location": "page 4, table 2, row 7"
        }
      ]
    }
  ],
  "uncertainty": [],
  "market_education_label": null,
  "learning_explanation": {
    "stages": [
      {"name": "retrieval", "purpose": "Find relevant indexed context."},
      {"name": "answering", "purpose": "Compose an attributed response."}
    ],
    "limitations": []
  },
  "provider_snapshot": {
    "language_model": "configured-provider",
    "retrieval": "configured-provider"
  }
}
```

## Invariants

- `status=answered` requires citations for every material claim.
- `status=insufficient-evidence` or `status=conflicting-evidence` must explain the
  limitation and must not invent a source fact.
- General market commentary requires `market_education_label`, approved-source
  citations no more than 90 calendar days old by effective source date, an
  `as_of_date`, and no personalized recommendation.
- Conflicting approved sources require `status=conflicting-evidence`, a `conflict_set`
  containing each competing claim and citation, and no definitive winner unless an
  explicit authority rule is present.
- The contract does not expose private chain-of-thought; learning explanations
  describe observable stages, inputs, outputs, and limitations.
