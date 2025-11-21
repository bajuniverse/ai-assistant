"""
Image handling utilities.

Provides functions for performing OCR on images and, optionally, using a
vision-enabled language model to generate captions or descriptions of
images. The OCR functionality relies on Tesseract via the `pytesseract`
library. Users must have Tesseract installed on their system for OCR to
function.
"""

from pathlib import Path
from typing import Optional


def ocr_image(path: Path) -> str:
    """Perform OCR on an image file and return extracted text.

    Requires the `pytesseract` and `Pillow` libraries to be installed, and
    Tesseract must be available on the system path.

    Args:
        path: Path to the image file.

    Returns:
        The text extracted from the image.

    Raises:
        RuntimeError: If required libraries are not installed.
    """
    try:
        import pytesseract  # type: ignore[import-not-found]
        from PIL import Image  # type: ignore[import-not-found]
    except ImportError as exc:
        raise RuntimeError(
            "pytesseract and Pillow must be installed for OCR."
        ) from exc

    img = Image.open(path)
    return pytesseract.image_to_string(img)


def describe_image_with_llm(
    path: Path,
    model: str = "llava",  # Placeholder for a vision model; adjust if using another model
) -> Optional[str]:
    """Describe an image using a vision-capable language model (stub).

    This function is provided as a placeholder for integrating a vision model
    through Ollama. The implementation will depend on how such models are
    exposed via the Ollama API. Currently, it returns None, leaving the
    OCR fallback as the primary image processing method.

    Args:
        path: Path to the image file.
        model: Name of the vision-enabled model to call.

    Returns:
        A description of the image, or None if no model is integrated.
    """
    # TODO: Integrate with a vision-enabled language model if available.
    _ = path  # unused for now
    _ = model
    return None