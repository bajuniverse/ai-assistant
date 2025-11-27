"""Tests for text chunking utilities."""

import pytest

from assistant.chunking import chunk_text


def test_chunk_text_basic_split() -> None:
    text = "abcdefghij"
    assert chunk_text(text, max_chars=4, overlap=1) == ["abcd", "defg", "ghij"]


@pytest.mark.parametrize("max_chars, overlap", [(0, 0), (-5, 1)])
def test_chunk_text_rejects_non_positive_max_chars(max_chars: int, overlap: int) -> None:
    with pytest.raises(ValueError):
        chunk_text("sample", max_chars=max_chars, overlap=overlap)


def test_chunk_text_rejects_overlap_without_progress() -> None:
    with pytest.raises(ValueError):
        chunk_text("sample", max_chars=5, overlap=5)

