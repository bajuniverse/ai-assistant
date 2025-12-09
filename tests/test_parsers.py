import tempfile
import unittest
from pathlib import Path

from assistant.parsers.docx_parser import extract_docx_text
from assistant.parsers.md_parser import extract_md_text
from assistant.parsers.pdf_parser import extract_pdf_text
from assistant.parsers.txt_parser import extract_txt_text


class ParserErrorHandlingTests(unittest.TestCase):
    def test_txt_parser_raises_on_unreadable_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            unreadable_path = Path(tmp) / "subdir"
            unreadable_path.mkdir()
            with self.assertRaises(RuntimeError):
                extract_txt_text(unreadable_path)

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


if __name__ == "__main__":
    unittest.main()
