"""
File summarisation utilities.

This module provides functions for summarising individual files and entire
folders of files. It relies on the parsers to extract text from various
file formats, uses chunking to split long texts into manageable pieces,
and uses a language model via the LLM wrapper to generate concise
summaries. The resulting summaries are written to disk in the configured
output directory.
"""

from pathlib import Path
from typing import List

from .file_discovery import is_text_file, is_image_file, iter_files
from .parsers.pdf_parser import extract_pdf_text
from .parsers.docx_parser import extract_docx_text
from .parsers.md_parser import extract_md_text
from .parsers.txt_parser import extract_txt_text
from .parsers.image_parser import ocr_image
from .chunking import chunk_text
from .llm.ollama_client import chat
from .config import Config


def _extract_text_for_file(path: Path) -> str:
    """Determine the correct parser for a file based on its extension."""
    suffix = path.suffix.lower()

    if suffix == ".pdf":
        return extract_pdf_text(path)
    if suffix == ".docx":
        return extract_docx_text(path)
    if suffix == ".md":
        return extract_md_text(path)
    if suffix == ".txt":
        return extract_txt_text(path)
    if suffix in {".png", ".jpg", ".jpeg"}:
        return ocr_image(path)

    raise ValueError(f"Unsupported file type: {suffix}")


def summarize_text(text: str, cfg: Config) -> str:
    """Summarise a piece of text using the configured language model."""
    model = cfg.model.get("name", "llama3")
    temp = cfg.model.get("temperature", 0.2)

    prompt = (
        "You are a concise summarisation assistant. "
        "Summarise the following content in clear bullet points. "
        "Focus on key ideas and facts.\n\n"
        f"Content:\n{text}"
    )
    return chat(prompt, model=model, temperature=temp)


def summarize_single_file(path: Path, cfg: Config) -> None:
    """Summarise a single file and write the summary to disk."""
    # Extract text using the appropriate parser
    text = _extract_text_for_file(path)
    rag_cfg = cfg.rag
    chunk_size: int = rag_cfg.get("chunk_size", 1500)
    chunk_overlap: int = rag_cfg.get("chunk_overlap", 200)

    # Split text into chunks for summarisation
    chunks: List[str] = chunk_text(text, max_chars=chunk_size, overlap=chunk_overlap)

    # Summarise each chunk
    partial_summaries: List[str] = []
    for ch in chunks:
        partial_summaries.append(summarize_text(ch, cfg))

    # Combine partial summaries and summarise again for a final result
    combined = "\n".join(partial_summaries)
    final_summary = summarize_text(combined, cfg)

    # Determine output path and ensure the directory exists
    output_folder = Path(cfg.paths.get("output_folder", "./outputs"))
    output_folder.mkdir(parents=True, exist_ok=True)
    out_path = output_folder / f"{path.name}.summary.md"

    # Write summary
    out_path.write_text(final_summary, encoding="utf-8")

    print(f"[SUMMARY] {path} -> {out_path}")


def summarize_folder(folder: Path, cfg: Config) -> None:
    """Summarise all supported files in a folder recursively."""
    for f in iter_files(folder):
        if is_text_file(f) or is_image_file(f):
            try:
                summarize_single_file(f, cfg)
            except Exception as e:
                print(f"[ERROR] Failed to summarise {f}: {e}")