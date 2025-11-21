"""
Top-level package for the local AI assistant.

This package exposes modules for configuration handling, command-line interface,
file discovery, text chunking, summarisation, retrieval-augmented generation,
and language model interaction.
"""

from . import cli, config, file_discovery, chunking, summarizer, rag  # noqa: F401