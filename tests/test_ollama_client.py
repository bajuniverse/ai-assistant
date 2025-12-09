import unittest
from unittest.mock import patch

from assistant.llm.ollama_client import chat


class OllamaClientTests(unittest.TestCase):
    @patch("assistant.llm.ollama_client.ollama.chat")
    def test_chat_sends_prompt_and_system_message(self, mock_chat) -> None:
        mock_chat.return_value = {"message": {"content": "ok"}}

        result = chat(
            prompt="Hello?",
            model="llama3",
            system_prompt="You are friendly.",
            temperature=0.5,
        )

        self.assertEqual(result, "ok")
        mock_chat.assert_called_once()
        _, kwargs = mock_chat.call_args
        self.assertEqual(kwargs["model"], "llama3")
        self.assertEqual(kwargs["options"]["temperature"], 0.5)
        self.assertEqual(
            kwargs["messages"],
            [
                {"role": "system", "content": "You are friendly."},
                {"role": "user", "content": "Hello?"},
            ],
        )

    @patch("assistant.llm.ollama_client.ollama.chat")
    def test_chat_handles_user_only_prompt(self, mock_chat) -> None:
        mock_chat.return_value = {"message": {"content": "response"}}

        result = chat(prompt="Just user")

        self.assertEqual(result, "response")
        _, kwargs = mock_chat.call_args
        self.assertEqual(
            kwargs["messages"],
            [{"role": "user", "content": "Just user"}],
        )


if __name__ == "__main__":
    unittest.main()
