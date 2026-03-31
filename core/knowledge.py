"""Knowledge base loader — reads full KB into context for LLM calls."""

from pathlib import Path
from config import KB_PATH


def load_knowledge_base(path: Path = KB_PATH) -> str:
    """Load the full knowledge base content as a string.

    The KB is ~58K tokens and fits within a single LLM context window.
    No chunking or retrieval needed — the model's native attention
    handles relevance selection.
    """
    if not path.exists():
        raise FileNotFoundError(f"Knowledge base not found at {path}")
    return path.read_text(encoding="utf-8")


def get_kb_token_estimate(text: str) -> int:
    """Rough token estimate (~4 chars per token for Claude)."""
    return len(text) // 4
