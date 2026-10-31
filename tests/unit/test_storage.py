from financial_assistant.storage.artifacts import ArtifactStore


def test_artifact_store_preserves_exact_duplicates(tmp_path):
    store = ArtifactStore(tmp_path)
    first = store.save(b"source", "fixture.pdf", "application/pdf")
    second = store.save(b"source", "fixture.pdf", "application/pdf")
    assert first.path == second.path
    assert second.duplicate is True
    assert first.path.read_bytes() == b"source"

