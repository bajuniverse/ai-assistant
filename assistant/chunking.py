"""
Text chunking utilities.

Provide functions to split large pieces of text into smaller chunks for
processing by language models. Chunking is based on character length, with
optional overlap to maintain context across chunks. These functions can be
replaced or extended with token-based chunking if needed.
"""

from typing import List


def chunk_text(text: str, max_chars: int, overlap: int = 0) -> List[str]:
    """Split text into a list of chunks of at most `max_chars` characters.

    Chunks are created by slicing the text into segments. If `overlap` is
    specified, each chunk will overlap the previous one by the given number
    of characters. This simple approach helps preserve context across
    boundaries but may produce redundant content.

    Args:
        text: The full text to split.
        max_chars: Maximum number of characters per chunk.
        overlap: Optional number of characters to include from the end of
            the previous chunk at the start of the next chunk.

    Returns:
        A list of text chunks.
    """
    if not text:
        return []

    chunks: List[str] = []
    start = 0
    length = len(text)

    while start < length:
        end = min(start + max_chars, length)
        chunks.append(text[start:end])
        if end == length:
            break
        # Move start forward, subtracting overlap to create overlap with the previous chunk.
        start = end - overlap if overlap > 0 else end

    return chunks