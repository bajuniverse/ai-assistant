"""
PDF text extraction.

Uses PyMuPDF (imported as `fitz`) to load PDF documents and extract the
text content of each page. If PyMuPDF is not installed, an informative
RuntimeError is raised instructing the user to install the dependency.
"""

from pathlib import Path


def extract_pdf_text(path: Path) -> str:
    """Extract text from a PDF file.

    Args:
        path: Path to the PDF file.

    Returns:
        A string containing the concatenated text of all pages.

    Raises:
        RuntimeError: If PyMuPDF is not installed.
    """
    try:
        import fitz  # type: ignore[import-not-found]
    except ImportError as exc:
        raise RuntimeError(
            "pymupdf (fitz) not installed. Install with `pip install pymupdf`."
        ) from exc

    doc = fitz.open(path)
    texts: list[str] = []
    for page in doc:
        texts.append(page.get_text())
    doc.close()
    return "\n".join(texts)