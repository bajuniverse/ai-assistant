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

    try:
        doc = fitz.open(path)
    except Exception as exc:
        raise RuntimeError(f"Failed to read PDF {path}: {exc}") from exc

    texts: list[str] = []
    try:
        for page in doc:
            texts.append(page.get_text())
    except Exception as exc:
        raise RuntimeError(f"Failed to extract text from PDF {path}: {exc}") from exc
    finally:
        doc.close()

    return "\n".join(texts)
