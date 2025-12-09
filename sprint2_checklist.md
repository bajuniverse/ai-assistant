# Sprint 2 To-Do Checklist (Actionable)

## Goal
Implement a fully functional Retrieval-Augmented Generation (RAG) pipeline, enabling semantic search and Q&A over ingested documents.

---

## 1. Vector Store Setup (ChromaDB)
- [x] Install and verify ChromaDB compatibility with project
- [x] Create persistent vector store directory (`./vector_store`)
- [x] Implement helper to initialise or load Chroma collection
- [x] Add metadata schema (source file, chunk index)

---

## 2. Ingestion Pipeline
- [x] Implement ingestion entry function `ingest_folder()`
- [x] Parse all supported files (PDF, DOCX, MD, TXT, OCR images)
- [x] Convert extracted text into chunks using existing chunker
- [x] Embed each chunk into vector format
- [x] Store (id, document text, metadata, embedding) in Chroma
- [x] Ensure ingestion can run repeatedly without duplication issues
- [x] Add helpful ingestion logging (file count, chunk count, etc.)

---

## 3. Embedding System
- [x] Select embedding model (local or external)
- [x] Implement embedding wrapper
- [x] Validate embeddings are numeric vectors of uniform dimension
- [x] Handle errors gracefully when chunks are empty

---

## 4. Retrieval
- [x] Implement query embedding
- [x] Implement vector similarity search (top_k from config)
- [x] Validate retrieved documents include metadata
- [x] Add debug option to print retrieved chunk sources

---

## 5. Prompt Assembly for RAG
- [x] Build full LLM prompt containing:
  - [x] Instruction header
  - [x] Injected retrieved context chunks
  - [x] The user question
- [x] Add guardrails: "If answer not found in context, say so."
- [x] Ensure formatting is consistent for LLM processing

---

## 6. Ask Command (CLI Integration)
- [x] Build CLI command: `ask --question "..."`
- [x] Connect CLI to retrieval + prompt pipeline
- [x] Display answer with "Sources:" below
- [x] Handle case where vector store is empty (show useful error)
- [ ] Add optional verbosity flag for debugging

---

## 7. Error Handling & Edge Cases
- [x] Handle ingestion of unreadable/corrupt files
- [x] Gracefully skip empty text extractions
- [x] Warn if no relevant chunks found
- [x] Ensure question embedding does not crash on empty query

---

## 8. Testing
- [ ] Test ingestion on sample dataset
- [ ] Test query with simple question
- [x] Validate answers match expected source documents
- [ ] Test retrieval accuracy with multiple similar documents
- [ ] Confirm metadata (file names) are correctly returned

---

## 9. Documentation Updates
- [ ] Update README with RAG workflow explanation
- [ ] Add examples:
  - [ ] Running ingestion
  - [ ] Asking questions
  - [ ] Troubleshooting vector store issues
- [ ] Add diagram showing RAG flow (optional)

---

## 10. Sprint Review Checklist
- [ ] Demonstrate ingestion on a folder of mixed documents
- [ ] Demonstrate semantic Q&A returning correct information
- [ ] Show retrieved chunk sources
- [ ] Document limitations & planned improvements
