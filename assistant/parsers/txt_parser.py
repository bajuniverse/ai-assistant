"""
Plain text file reader.

Reads plain text files using UTF-8 encoding with error handling for
unexpected byte sequences.
"""

from pathlib import Path


def extract_txt_text(path: Path) -> str:
    """Read and return the content of a plain text file.

    Args:
        path: Path to the text file.

    Returns:
        The contents of the file as a string.
    """
    return path.read_text(encoding="utf-8", errors="ignore")