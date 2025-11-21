"""
Document parsing utilities.

This package includes modules for extracting text from various file formats,
including PDF, DOCX, Markdown, plain text, and images via OCR. Each parser
exposes an `extract_*_text` function that returns the raw textual content
from a file.
"""

from .pdf_parser import extract_pdf_text  # noqa: F401
from .docx_parser import extract_docx_text  # noqa: F401
from .md_parser import extract_md_text  # noqa: F401
from .txt_parser import extract_txt_text  # noqa: F401
from .image_parser import ocr_image, describe_image_with_llm  # noqa: F401