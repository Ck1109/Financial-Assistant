"""Configuration-based construction of replaceable local providers."""

from .llm import DeterministicLanguageModel, LanguageModel
from .vector_store import KeywordVectorStore, VectorStore


def create_language_model(name: str) -> LanguageModel:
    """Create a supported language model or fail explicitly."""
    if name == DeterministicLanguageModel.name:
        return DeterministicLanguageModel()
    raise ValueError(f"Unsupported language-model provider: {name}")


def create_vector_store(name: str) -> VectorStore:
    """Create a supported retrieval provider or fail explicitly."""
    if name == KeywordVectorStore.name:
        return KeywordVectorStore()
    raise ValueError(f"Unsupported retrieval provider: {name}")

