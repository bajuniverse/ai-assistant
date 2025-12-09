"""
DOCX text extraction.

Leverages the `python-docx` library to read Microsoft Word documents and
return the concatenated text of all paragraphs. If `python-docx` is not
installed, a RuntimeError is raised with installation instructions.
"""

from pathlib import Path


def extract_docx_text(path: Path) -> str:
    """Extract text from a DOCX file.

    Args:
        path: Path to the DOCX file.

    Returns:
        A string containing the text of all paragraphs in the document.

    Raises:
        RuntimeError: If `python-docx` is not installed.
    """
    try:
        import docx  # type: ignore[import-not-found]
    except ImportError as exc:
        raise RuntimeError(
            "python-docx not installed. Install with `pip install python-docx`."
        ) from exc

    try:
        doc = docx.Document(path)
    except Exception as exc:
        raise RuntimeError(f"Failed to read DOCX {path}: {exc}") from exc

    try:
        return "\n".join(paragraph.text for paragraph in doc.paragraphs)
    except Exception as exc:
        raise RuntimeError(f"Failed to extract text from DOCX {path}: {exc}") from exc
