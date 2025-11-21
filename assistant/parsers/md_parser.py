"""
Markdown text extraction.

Reads a Markdown file as plain text. In future enhancements, Markdown
syntax could be stripped or converted to HTML/text for better summarisation.
"""

from pathlib import Path


def extract_md_text(path: Path) -> str:
    """Read and return the content of a Markdown file as plain text.

    Args:
        path: Path to the Markdown file.

    Returns:
        The raw content of the file.
    """
    return path.read_text(encoding="utf-8", errors="ignore")