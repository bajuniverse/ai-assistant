"""
Wrapper functions for interacting with Ollama models.

This module abstracts the details of constructing requests and parsing
responses from the `ollama` library. It exposes a `chat` function that
sends a prompt to a specified model and returns the generated reply.
"""

from typing import Optional

import ollama


def chat(
    prompt: str,
    model: str = "llama3",
    system_prompt: Optional[str] = None,
    temperature: float = 0.2,
) -> str:
    """Send a chat prompt to the specified Ollama model and return the reply.

    Args:
        prompt: The user prompt to send to the model.
        model: The name of the model to use.
        system_prompt: An optional system message to set the behaviour of the model.
        temperature: Sampling temperature controlling randomness of the output.

    Returns:
        The content of the model's response.
    """
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    resp = ollama.chat(
        model=model,
        messages=messages,
        options={"temperature": temperature},
    )
    # The response dictionary includes a 'message' key with 'content'.
    return resp["message"]["content"]