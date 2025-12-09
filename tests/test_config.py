import tempfile
from pathlib import Path
import unittest

from assistant.config import get_config


class ConfigTests(unittest.TestCase):
    def test_defaults_apply_when_missing_keys(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cfg_path = Path(tmp) / "config.yaml"
            cfg_path.write_text("")

            cfg = get_config(str(cfg_path))

            self.assertEqual(cfg.model["name"], "llama3")
            self.assertEqual(cfg.model["temperature"], 0.2)
            self.assertEqual(cfg.rag["chunk_size"], 1500)
            self.assertEqual(cfg.rag["chunk_overlap"], 200)
            self.assertEqual(cfg.paths["output_folder"], "./outputs")
            self.assertEqual(cfg.logging["level"], "INFO")

    def test_yaml_values_override_defaults(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cfg_path = Path(tmp) / "config.yaml"
            cfg_path.write_text(
                "model:\n"
                "  name: custom-model\n"
                "  temperature: 0.5\n"
                "rag:\n"
                "  top_k: 2\n"
                "paths:\n"
                "  output_folder: ./out\n"
                "logging:\n"
                "  level: DEBUG\n"
            )

            cfg = get_config(str(cfg_path))

            self.assertEqual(cfg.model["name"], "custom-model")
            self.assertEqual(cfg.model["temperature"], 0.5)
            self.assertEqual(cfg.rag["top_k"], 2)
            self.assertEqual(cfg.paths["output_folder"], "./out")
            self.assertEqual(cfg.logging["level"], "DEBUG")


if __name__ == "__main__":
    unittest.main()
