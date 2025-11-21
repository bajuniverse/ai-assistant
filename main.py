"""
Entry point for the AI assistant CLI.

Run this script to summarise files, ingest folders into the vector store, or ask questions over ingested data.

Example usage:

    python main.py summary --folder ./data
    python main.py ingest --folder ./data
    python main.py ask --question "What is this about?"
"""

from assistant.cli import main


if __name__ == "__main__":
    main()