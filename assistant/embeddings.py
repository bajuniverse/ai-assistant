"""
Embedding utilities for the RAG pipeline.

Provides a local sentence-transformer embedding function that can be used with
ChromaDB. Defaults to the small `all-MiniLM-L6-v2` model for lightweight,
offline-friendly embeddings. Raises a clear error if the dependency is missing.
Includes helpers to validate embedding outputs for numeric type and uniform
dimensions.
"""

from numbers import Real
from typing import Optional, Sequence

from chromadb.utils import embedding_functions


DEFAULT_EMBED_MODEL = "all-MiniLM-L6-v2"


def _resolve_model_name(cfg_name: Optional[str]) -> str:
    """Map config names to actual model identifiers."""
    if not cfg_name:
        return DEFAULT_EMBED_MODEL
    if cfg_name.lower() in {"all-minilm", "all-minilm-l6", "all-minilm-l6-v2"}:
        return DEFAULT_EMBED_MODEL
    return cfg_name


def get_embedding_function(model_name: Optional[str] = None):
    """Return a sentence-transformer embedding function for ChromaDB."""
    resolved = _resolve_model_name(model_name)
    try:
        return embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=resolved
        )
    except ImportError as exc:
        raise RuntimeError(
            "sentence-transformers is not installed. "
            "Install it with `pip install sentence-transformers`."
        ) from exc


def validate_embeddings(embeddings: Sequence[Sequence[Real]]) -> int:
    """Validate embeddings are numeric and share a uniform dimension.

    Returns:
        The embedding dimension.

    Raises:
        ValueError: If embeddings are empty or dimensions mismatch.
        TypeError: If any element is non-numeric.
    """
    if not embeddings:
        raise ValueError("No embeddings were generated.")
    dim = len(embeddings[0])
    if dim == 0:
        raise ValueError("Embedding dimension must be greater than zero.")

    for emb in embeddings:
        if len(emb) != dim:
            raise ValueError("Embeddings have inconsistent dimensions.")
        for val in emb:
            if not isinstance(val, Real):
                raise TypeError("Embedding values must be numeric.")
    return dim
