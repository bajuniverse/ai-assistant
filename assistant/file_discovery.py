"""
Utilities for discovering files within a folder.

This module provides helper functions to iterate over files in a directory
recursively and to determine whether a file is supported for text or
image processing based on its extension.
"""

from pathlib import Path
from typing import Iterable


# Supported extensions for text documents and images.
SUPPORTED_TEXT_EXTS = {".pdf", ".docx", ".md", ".txt"}
SUPPORTED_IMAGE_EXTS = {".png", ".jpg", ".jpeg"}


def iter_files(folder: Path) -> Iterable[Path]:
    """Yield all files in the given folder recursively.

    Args:
        folder: The root directory to search.

    Yields:
        Path objects for every file found in the directory tree.
    """
    for path in folder.rglob("*"):
        if path.is_file():
            yield path


def is_text_file(path: Path) -> bool:
    """Return True if the file has a supported text extension."""
    return path.suffix.lower() in SUPPORTED_TEXT_EXTS


def is_image_file(path: Path) -> bool:
    """Return True if the file has a supported image extension."""
    return path.suffix.lower() in SUPPORTED_IMAGE_EXTS