import unittest
from unittest.mock import MagicMock, patch

import assistant.rag as rag
from assistant.config import Config


class RagRetrievalTests(unittest.TestCase):
    @patch("assistant.rag.get_embedding_function")
    @patch("assistant.rag.chromadb.PersistentClient")
    def test_query_embedding_passed_to_chroma(self, mock_client, mock_get_embed_fn) -> None:
        fake_collection = MagicMock()
        fake_collection.query.return_value = {
            "documents": [["doc1"]],
            "metadatas": [[{"source": "s1"}]],
        }
        mock_client.return_value.get_or_create_collection.return_value = fake_collection

        embeddings = [[0.1, 0.2, 0.3]]
        mock_get_embed_fn.return_value = lambda texts: embeddings

        cfg = Config()

        results = rag._retrieve("hello", cfg, top_k=1)

        fake_collection.query.assert_called_once_with(
            query_embeddings=embeddings, n_results=1
        )
        self.assertEqual(results, [("doc1", {"source": "s1"})])

    def test_empty_query_returns_empty_results(self) -> None:
        cfg = Config()
        results = rag._retrieve("   ", cfg, top_k=1)
        self.assertEqual(results, [])

    @patch("assistant.rag.chat", return_value="answer body")
    @patch("assistant.rag._retrieve")
    def test_sources_exclude_missing_and_deduplicate(self, mock_retrieve, mock_chat) -> None:
        mock_retrieve.return_value = [
            ("doc text 1", {"source": "file1.txt"}),
            ("doc text 2", {"source": "file1.txt"}),
            ("doc text 3", {"source": None}),
        ]
        cfg = Config()

        answer = rag.answer_question("q", cfg)

        self.assertIn("Sources:\nfile1.txt", answer)
        # Ensure only one instance of file1.txt
        self.assertEqual(answer.count("file1.txt"), 1)
        mock_chat.assert_called_once()

    @patch("assistant.rag.chat", return_value="answer body")
    @patch("assistant.rag._retrieve")
    def test_answer_includes_expected_sources_and_context(self, mock_retrieve, mock_chat) -> None:
        mock_retrieve.return_value = [
            ("context from B", {"source": "b.txt"}),
            ("context from A", {"source": "a.txt"}),
        ]
        cfg = Config()

        answer = rag.answer_question("What?", cfg)

        prompt = mock_chat.call_args.args[0]
        self.assertIn("context from A", prompt)
        self.assertIn("context from B", prompt)
        self.assertIn("Question: What?", prompt)
        self.assertIn("Sources:\na.txt\nb.txt", answer)

    @patch("assistant.rag.chat", return_value="answer body")
    @patch("assistant.rag._retrieve")
    @patch("assistant.rag.print")
    def test_debug_logs_sources(self, mock_print, mock_retrieve, mock_chat) -> None:
        mock_retrieve.return_value = [
            ("doc text 1", {"source": "file1.txt", "chunk_index": 0}),
            ("doc text 2", {"source": "file2.txt", "chunk_index": 1}),
        ]
        cfg = Config()

        rag.answer_question("q", cfg, debug=True)

        mock_print.assert_any_call("[DEBUG] Retrieved 2 chunks:")
        mock_print.assert_any_call("[DEBUG] file1.txt (chunk 0)")
        mock_print.assert_any_call("[DEBUG] file2.txt (chunk 1)")


if __name__ == "__main__":
    unittest.main()
