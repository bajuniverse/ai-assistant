import tempfile
import unittest
from pathlib import Path

from assistant.file_discovery import iter_files, is_text_file, is_image_file


class FileDiscoveryTests(unittest.TestCase):
    def test_iter_files_recurses(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a").mkdir()
            (root / "a" / "doc1.txt").write_text("hi")
            (root / "b").mkdir()
            (root / "b" / "doc2.md").write_text("hello")
            (root / "image.jpg").write_text("fake")

            found = {p.relative_to(root) for p in iter_files(root)}
            expected = {
                Path("a/doc1.txt"),
                Path("b/doc2.md"),
                Path("image.jpg"),
            }
            self.assertSetEqual(found, expected)

    def test_extension_checks(self) -> None:
        self.assertTrue(is_text_file(Path("file.pdf")))
        self.assertTrue(is_text_file(Path("file.docx")))
        self.assertTrue(is_text_file(Path("file.md")))
        self.assertTrue(is_text_file(Path("file.txt")))
        self.assertFalse(is_text_file(Path("file.png")))

        self.assertTrue(is_image_file(Path("pic.jpg")))
        self.assertTrue(is_image_file(Path("pic.jpeg")))
        self.assertTrue(is_image_file(Path("pic.png")))
        self.assertFalse(is_image_file(Path("pic.txt")))


if __name__ == "__main__":
    unittest.main()
