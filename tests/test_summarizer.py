import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch

from assistant.config import Config
from assistant.summarizer import summarize_single_file


class SummarizerPipelineTests(unittest.TestCase):
    @patch("assistant.summarizer.chat")
    def test_summarize_single_file_runs_pipeline_and_writes_output(self, mock_chat) -> None:
        mock_chat.side_effect = ["s1", "s2", "s3", "final summary"]

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            input_file = tmp_path / "sample.txt"
            input_file.write_text("abcdefghijABCDEFGHIJklmnop", encoding="utf-8")

            cfg_path = tmp_path / "config.yaml"
            cfg_path.write_text(
                "model:\n"
                "  name: test-model\n"
                "  temperature: 0.5\n"
                "rag:\n"
                "  chunk_size: 10\n"
                "  chunk_overlap: 2\n"
                f"paths:\n"
                f"  output_folder: {tmp_path / 'out'}\n"
            )

            cfg = Config(cfg_path)

            summarize_single_file(input_file, cfg)

            output_file = tmp_path / "out" / "sample.txt.summary.md"
            self.assertTrue(output_file.exists())
            self.assertEqual(output_file.read_text(encoding="utf-8"), "final summary")
            self.assertEqual(mock_chat.call_count, 4)  # three chunks + final summary
            for call in mock_chat.call_args_list:
                self.assertEqual(call.kwargs["model"], "test-model")
                self.assertEqual(call.kwargs["temperature"], 0.5)


if __name__ == "__main__":
    unittest.main()
