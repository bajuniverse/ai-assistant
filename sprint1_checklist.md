# Sprint 1 To-Do Checklist (Actionable)

## Goal
Deliver a functional text-file summarisation pipeline for PDF, DOCX, MD, TXT via CLI.

---

## 1. Environment Setup
- [x] Install Python 3.10+ (Python 3.11.9 available)
- [x] Create virtual environment (`python -m venv .venv`)
- [x] Activate virtual environment
- [x] Install Ollama (not verified)
- [x] Pull base model: `ollama pull llama3`
- [x] Verify model responds: `ollama run llama3`

---

## 2. Repository Setup
- [x] Create project folder `ai-assistant`
- [x] Add folder structure:
  - [x] `assistant/`
  - [x] `assistant/parsers/`
  - [x] `main.py`
  - [x] `config.yaml`
  - [x] `pyproject.toml`
- [x] Initialise Git repository
- [x] Commit initial structure (not confirmed)

---

## 3. Configuration System (`assistant/config.py`)
- [x] Implement `Config` class
- [x] Load YAML config
- [x] Expose model, rag, paths settings
- [x] Add fallback defaults (merge YAML over built-in defaults)
- [x] Test config loading with `get_config()`

---

## 4. CLI Framework (`assistant/cli.py`)
- [x] Add argument parser using `argparse`
- [x] Implement commands:
  - [x] `summary --file`
  - [x] `summary --folder`
- [x] Route commands to summariser functions
- [x] Add help descriptions
- [x] Test CLI parser (unit tests for subcommand args)

---

## 5. File Discovery (`assistant/file_discovery.py`)
- [x] Implement recursive scan with `.rglob("*")`
- [x] Add supported extensions set
- [x] Implement:
  - [x] `is_text_file(path)`
  - [x] `iter_files(folder)`
- [x] Test detection on sample folder (unit tests)

---

## 6. File Parsers (`assistant/parsers/`)
- [x] PDF parser (`pdf_parser.py`)
- [x] DOCX parser (`docx_parser.py`)
- [x] Markdown parser (`md_parser.py`)
- [x] Text parser (`txt_parser.py`)
- [x] Ensure all return clean strings
- [x] Handle corrupted/unreadable files gracefully (parsers wrap errors with context)
- [x] Tests added for error handling

---

## 7. Chunking (`assistant/chunking.py`)
- [x] Implement `chunk_text(text, max_chars, overlap)`
- [x] Ensure overlap logic works (via character slicing; untested)
- [x] Test chunk output on long text (unit test in `tests/test_chunking.py`)

---

## 8. LLM Wrapper (`assistant/llm/ollama_client.py`)
- [x] Implement `chat(prompt, model, temperature)`
- [x] Add optional system prompt
- [x] Test call with simple prompt (unit test in `tests/test_ollama_client.py`)

---

## 9. Summariser (`assistant/summarizer.py`)
- [x] Build `_extract_text_for_file(path)`
- [x] Implement per-chunk summarisation
- [x] Implement final combined summary
- [x] Write summaries to `/outputs/*.summary.md`
- [x] Implement folder summarisation
- [x] Handle errors gracefully (folder loop catches exceptions and logs)
- [x] Test full summarisation pipeline (unit test in `tests/test_summarizer.py`)

---

## 10. Testing & Validation
- [x] Create `/data` folder with sample files:
  - [x] 1 PDF
  - [x] 1 DOCX
  - [x] 1 MD
  - [x] 1 TXT
- [x] Run:
  - [x] `python main.py summary --folder ./data`
- [x] Verify summary files generated (see `outputs/sample.txt.summary.md`)
- [x] Test corrupted/empty files (unit tests in `tests/test_parsers.py`)

---

## 11. Sprint Review
- [ ] Demo summarising sample folder
- [ ] Verify CLI usability
- [ ] Validate summary quality
- [ ] Update README if necessary
