from financial_assistant.observability import new_run_id, redact


def test_redaction_does_not_log_credentials():
    assert "secret" not in redact("api_key=secret")
    assert "[REDACTED]" in redact("api_key=secret")
    assert new_run_id().startswith("run-")

