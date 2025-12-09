import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from assistant.parsers.docx_parser import extract_docx_text
from assistant.parsers.md_parser import extract_md_text
from assistant.parsers.pdf_parser import extract_pdf_text
from assistant.parsers.txt_parser import extract_txt_text


class ParserErrorHandlingTests(unittest.TestCase):
    def test_txt_parser_returns_empty_string_for_empty_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            empty_file = Path(tmp) / "empty.txt"
            empty_file.write_text("", encoding="utf-8")
            self.assertEqual(extract_txt_text(empty_file), "")

    def test_txt_parser_raises_on_unreadable_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            unreadable_path = Path(tmp) / "subdir"
            unreadable_path.mkdir()
            with self.assertRaises(RuntimeError):
                extract_txt_text(unreadable_path)

    def test_md_parser_returns_empty_string_for_empty_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            empty_file = Path(tmp) / "empty.md"
            empty_file.write_text("", encoding="utf-8")
            self.assertEqual(extract_md_text(empty_file), "")

    def test_md_parser_raises_on_unreadable_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            unreadable_path = Path(tmp) / "subdir"
            unreadable_path.mkdir()
            with self.assertRaises(RuntimeError):
                extract_md_text(unreadable_path)

    def test_pdf_parser_raises_on_missing_file_or_dependency(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            missing_file = Path(tmp) / "missing.pdf"
            with self.assertRaises(RuntimeError):
                extract_pdf_text(missing_file)

    def test_docx_parser_raises_on_missing_file_or_dependency(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            missing_file = Path(tmp) / "missing.docx"
            with self.assertRaises(RuntimeError):
                extract_docx_text(missing_file)

    def test_pdf_parser_raises_on_corrupted_file(self) -> None:
        class FakeFitzModule:
            @staticmethod
            def open(path):
                raise ValueError(f"Corrupted PDF {path}")

        with tempfile.TemporaryDirectory() as tmp:
            bad_pdf = Path(tmp) / "bad.pdf"
            bad_pdf.write_text("not a real pdf", encoding="utf-8")
            with patch.dict("sys.modules", {"fitz": FakeFitzModule}):
                with self.assertRaises(RuntimeError):
                    extract_pdf_text(bad_pdf)

    def test_docx_parser_raises_on_corrupted_file(self) -> None:
        class FakeDocxModule:
            @staticmethod
            def Document(path):
                raise ValueError(f"Corrupted DOCX {path}")

        with tempfile.TemporaryDirectory() as tmp:
            bad_docx = Path(tmp) / "bad.docx"
            bad_docx.write_text("not a real docx", encoding="utf-8")
            with patch.dict("sys.modules", {"docx": FakeDocxModule}):
                with self.assertRaises(RuntimeError):
                    extract_docx_text(bad_docx)


if __name__ == "__main__":
    unittest.main()
