# Local AI Assistant

This project provides a **local assistant** for summarising and querying
documents and images on your machine. It uses the open‑source
[`ollama`](https://github.com/ollama/ollama) language model runner to power
the language model, and [`Chroma`](https://www.trychroma.com/) for the
vector store. The code base is written in Python and is ready to run on
your own hardware with no external dependencies beyond the specified
Python packages.

## Features

### 📄 Summarise Documents

- Supports **PDF**, **DOCX**, **Markdown**, and **plain text** files.
- Extracts text, splits it into manageable chunks, and generates clear
  bullet‑point summaries using a local language model.
- Writes summaries to a dedicated `outputs/` folder alongside the
  original file name (e.g. `report.pdf.summary.md`).

### 🖼️ Image OCR

- Basic **OCR** using Tesseract via `pytesseract` for **PNG** and **JPG**
  images.
- Treats extracted text from images like a document so it can be
  summarised and indexed.
- Placeholder for vision‑enabled models if you wish to add richer image
  descriptions.

### 🔎 Retrieval‑Augmented QA

- Ingest your folder into a **vector store**. Each document is split
  into chunks, embedded, and stored with metadata about the source
  file.
- Ask natural language questions over your ingested data. The assistant
  retrieves relevant chunks and answers using them as context.
- Provides citations by listing the file paths used to answer the
  question.

## Installation

1. **Clone** this repository or copy the `ai-assistant` folder into your
   workspace.
2. Install Python 3.10 or newer.
3. Install the required packages:

   ```bash
   cd ai-assistant
   pip install -e .
   # or, if you prefer a requirements.txt style:
   # pip install -r requirements.txt
   ```

4. [Install Ollama](https://github.com/ollama/ollama#installation) and
   ensure it is running (`ollama serve`). Pull a language model such as
   `llama3`:

   ```bash
   ollama pull llama3
   ```

5. Optional: install
   [Tesseract](https://github.com/tesseract-ocr/tesseract#installing-tesseract)
   on your system and ensure it is in your `PATH` if you plan to use
   OCR.

## Usage

From the root directory, run the CLI via `main.py`:

```bash
# Summarise all supported files in a folder
python main.py summary --folder ./data

# Summarise a single file
python main.py summary --file ./data/report.pdf

# Ingest a folder into the vector store for RAG
python main.py ingest --folder ./data

# Ask a question over the ingested documents
python main.py ask --question "What does the report say about sales?"
```

### Configuration

The assistant reads settings from `config.yaml`. You can adjust:

- **model**: Name of the Ollama model and sampling temperature.
- **rag**: Embedding model (placeholder), number of top results, chunk size and overlap.
- **paths**: Data, output, and vector store directories.
- **logging**: Log level.

## Project Layout

| Path                           | Purpose                                     |
|--------------------------------|---------------------------------------------|
| `config.yaml`                  | User‑configurable settings                  |
| `main.py`                      | CLI entry point                             |
| `assistant/config.py`          | Configuration loader                        |
| `assistant/cli.py`             | Argument parser and subcommand dispatcher   |
| `assistant/file_discovery.py`  | Discover and filter files                   |
| `assistant/chunking.py`        | Simple text chunking                        |
| `assistant/llm/ollama_client.py`| Wrapper for Ollama API                      |
| `assistant/parsers/`           | Modules to extract text from various formats|
| `assistant/summarizer.py`      | Summary routines                            |
| `assistant/rag.py`             | Retrieval‑augmented QA routines             |

## Extending the Assistant

- **Vision models**: Integrate a vision‑enabled Ollama model to replace or
  supplement the OCR path in `assistant/parsers/image_parser.py`.
- **Token‑based chunking**: Replace the simple character chunker in
  `assistant/chunking.py` with a tokenizer (e.g. from HuggingFace) for
  more precise splitting.
- **Embeddings**: Swap the placeholder embedding model name in
  `config.yaml` and `rag.py` for an actual local embedding model via
  Ollama or another library.
- **Web or GUI**: Build a web front‑end with Flask or FastAPI, or a
  Streamlit/Gradio interface for interactive use.

## License

This project is provided for educational purposes without any warranty.
