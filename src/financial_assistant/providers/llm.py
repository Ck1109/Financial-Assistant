"""Language-model port and deterministic local implementation."""

from typing import Protocol, Sequence


class LanguageModel(Protocol):
    """Minimal provider contract used by grounded workflows."""

    name: str

    def summarize(self, passages: Sequence[str], title: str) -> str:
        """Create a summary from supplied evidence only."""


class DeterministicLanguageModel:
    """Safe local adapter that never invents facts outside supplied passages."""

    name = "local-deterministic"

    def summarize(self, passages: Sequence[str], title: str) -> str:
        """Return a concise evidence-bounded summary for local demonstrations."""
        if not passages:
            return f"No indexed evidence is available for {title}."
        return f"{title}: " + " ".join(p.strip() for p in passages[:3])

