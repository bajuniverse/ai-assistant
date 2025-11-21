"""
Language model interaction subpackage.

This subpackage provides wrappers for communicating with language models via
the `ollama` Python library. Additional backends can be added by exposing
compatible functions in this package.
"""

from .ollama_client import chat  # noqa: F401