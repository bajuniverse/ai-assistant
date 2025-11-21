"""
Command-line interface for the AI assistant.

Defines a `main` function that parses arguments and dispatches to the
appropriate functionality: summarising files, ingesting a folder into the
vector store, or asking a question over ingested content.

The CLI uses the `argparse` module to provide a structured interface.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from .config import get_config
from .summarizer import summarize_folder, summarize_single_file
from .rag import ingest_folder, answer_question


def build_parser() -> argparse.ArgumentParser:
    """Construct and return the argument parser for this CLI."""
    parser = argparse.ArgumentParser(
        description="Local AI assistant for documents and images (summary + RAG).",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subparser for summary
    summary = subparsers.add_parser(
        "summary", help="Summarise files in a folder or a single file"
    )
    summary.add_argument(
        "--folder",
        type=str,
        help="Folder path containing files to summarise",
    )
    summary.add_argument(
        "--file",
        type=str,
        help="Path to a single file to summarise",
    )

    # Subparser for ingest
    ingest = subparsers.add_parser(
        "ingest", help="Ingest a folder into the vector store for RAG"
    )
    ingest.add_argument(
        "--folder",
        type=str,
        required=True,
        help="Folder to ingest into the vector store",
    )

    # Subparser for ask
    ask = subparsers.add_parser(
        "ask", help="Ask questions over previously ingested content"
    )
    ask.add_argument(
        "--question",
        type=str,
        required=True,
        help="The question to ask over the ingested documents",
    )

    return parser


def main() -> None:
    """Entry point for the CLI.

    Parses arguments and invokes the corresponding functionality based on the
    provided subcommand.
    """
    parser = build_parser()
    args = parser.parse_args()
    cfg = get_config()

    if args.command == "summary":
        # Summarise a single file or all files in a folder
        if args.file:
            summarize_single_file(Path(args.file), cfg)
        elif args.folder:
            summarize_folder(Path(args.folder), cfg)
        else:
            parser.error("summary requires --file or --folder")

    elif args.command == "ingest":
        # Ingest a folder into the vector store
        ingest_folder(Path(args.folder), cfg)

    elif args.command == "ask":
        # Ask a question over ingested content
        answer = answer_question(args.question, cfg)
        print("\n=== Answer ===\n")
        print(answer)