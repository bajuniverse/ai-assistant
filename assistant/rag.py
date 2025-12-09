"""
Retrieval-augmented generation (RAG) utilities.

This module provides functions for ingesting folders into a vector store
(Chroma), retrieving relevant document chunks in response to a query, and
answering questions using a language model. Ingestion splits documents
into chunks and stores embeddings along with metadata. Retrieval fetches
top-k relevant chunks, which are then used as context in a prompt to
generate an answer.
"""

from __future__ import annotations

from pathlib import Path
from typing import List, Tuple

import chromadb

from .config import Config
from .embeddings import get_embedding_function, validate_embeddings
from .file_discovery import iter_files, is_text_file, is_image_file
from .parsers.pdf_parser import extract_pdf_text
from .parsers.docx_parser import extract_docx_text
from .parsers.md_parser import extract_md_text
from .parsers.txt_parser import extract_txt_text
from .parsers.image_parser import ocr_image
from .chunking import chunk_text
from .llm.ollama_client import chat


def _extract_text(path: Path) -> str:
    """Helper to select the correct parser for a file."""
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


def _get_chroma_collection(cfg: Config):
    """Get or create the ChromaDB collection used for document embeddings."""
    client = chromadb.PersistentClient(path=cfg.paths.get("vector_store", "./vector_store"))
    embed_fn = get_embedding_function(cfg.rag.get("embedding_model"))
    collection = client.get_or_create_collection(
        name="documents", embedding_function=embed_fn
    )
    return collection, embed_fn


def _clear_existing_for_source(collection, source: Path) -> None:
    """Remove any existing entries for a given source path to avoid duplication on re-ingest."""
    try:
        collection.delete(where={"source": str(source)})
    except Exception as exc:
        print(f"[WARN] Could not clear existing entries for {source}: {exc}")


def ingest_folder(folder: Path, cfg: Config) -> None:
    """Ingest all supported files in a folder into the vector store."""
    collection, embed_fn = _get_chroma_collection(cfg)
    rag_cfg = cfg.rag
    chunk_size: int = rag_cfg.get("chunk_size", 1500)
    overlap: int = rag_cfg.get("chunk_overlap", 200)

    ids: List[str] = []
    docs: List[str] = []
    metadatas: List[dict] = []

    for f in iter_files(folder):
        if not (is_text_file(f) or is_image_file(f)):
            continue
        try:
            text = _extract_text(f)
        except Exception as e:
            print(f"[ERROR] Failed to parse {f}: {e}")
            continue
        # Delete existing entries for this source so repeated ingestion does not duplicate.
        _clear_existing_for_source(collection, f)
        chunks = chunk_text(text, max_chars=chunk_size, overlap=overlap)
        for idx, ch in enumerate(chunks):
            if not ch.strip():
                continue
            ids.append(f"{f.resolve()}#{idx}")
            docs.append(ch)
            metadatas.append({"source": str(f), "chunk_index": idx})

    if not docs:
        print("[INGEST] No documents to ingest.")
        return

    try:
        embeddings = embed_fn(docs)
        validate_embeddings(embeddings)
    except Exception as exc:
        print(f"[ERROR] Failed to embed documents: {exc}")
        return

    collection.add(ids=ids, documents=docs, metadatas=metadatas, embeddings=embeddings)
    print(f"[INGEST] Ingested {len(docs)} chunks from folder {folder}")


def _retrieve(query: str, cfg: Config, top_k: int) -> List[Tuple[str, dict]]:
    """Retrieve the top-k most relevant documents from the vector store."""
    if not query.strip():
        return []

    collection, embed_fn = _get_chroma_collection(cfg)
    try:
        query_embeddings = embed_fn([query])
        validate_embeddings(query_embeddings)
    except Exception as exc:
        print(f"[ERROR] Failed to embed query: {exc}")
        return []

    results = collection.query(query_embeddings=query_embeddings, n_results=top_k)
    docs_list: List[List[str]] = results.get("documents", [[]])  # type: ignore[assignment]
    metas_list: List[List[dict]] = results.get("metadatas", [[]])  # type: ignore[assignment]
    docs = docs_list[0] if docs_list else []
    metas = metas_list[0] if metas_list else []
    return list(zip(docs, metas))


def answer_question(question: str, cfg: Config, debug: bool = False) -> str:
    """Answer a user question using retrieved context and a language model."""
    top_k = cfg.rag.get("top_k", 5)
    model = cfg.model.get("name", "llama3")
    temp = cfg.model.get("temperature", 0.2)

    retrieved = _retrieve(question, cfg, top_k=top_k)
    if not retrieved:
        return "I couldn't find any relevant content in the vector store."

    if debug:
        print(f"[DEBUG] Retrieved {len(retrieved)} chunks:")

    context_parts: List[str] = []
    source_info: List[str] = []
    for doc, meta in retrieved:
        context_parts.append(doc)
        src = meta.get("source") if meta else None  # type: ignore[arg-type]
        if src:
            source_info.append(src)
            if debug:
                idx = meta.get("chunk_index") if meta else None  # type: ignore[arg-type]
                suffix = f" (chunk {idx})" if idx is not None else ""
                print(f"[DEBUG] {src}{suffix}")
    context_str = "\n\n---\n\n".join(context_parts)
    sources = sorted(set(source_info))
    sources_str = "\n".join(sources)

    prompt = (
        "You are a retrieval-augmented assistant. "
        "Answer the user's question using ONLY the context below. "
        "If the answer is not present in the context, say so. "
        "Do not add a Sources section; the system will append it.\n\n"
        f"Context:\n{context_str}\n\n"
        f"Question: {question}\n\n"
        "Answer clearly and concisely."
    )

    answer = chat(prompt, model=model, temperature=temp)
    if sources_str:
        answer += f"\n\nSources:\n{sources_str}"
    return answer
