import pytest

from financial_assistant.providers.factory import create_language_model, create_vector_store


def test_local_provider_contracts_are_stable():
    model = create_language_model("local-deterministic")
    retrieval = create_vector_store("local-keyword")
    assert model.name == "local-deterministic"
    assert retrieval.name == "local-keyword"
    assert model.summarize(["A fact."], "Notification") == "Notification: A fact."


def test_unknown_provider_fails_explicitly():
    with pytest.raises(ValueError, match="Unsupported"):
        create_language_model("unknown")

