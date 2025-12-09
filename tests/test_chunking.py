import unittest

from assistant.chunking import chunk_text


class ChunkingTests(unittest.TestCase):
    def test_empty_text_returns_empty_list(self) -> None:
        chunks = chunk_text("", max_chars=10)
        self.assertEqual(chunks, [])

    def test_chunks_respect_max_chars_without_overlap(self) -> None:
        text = "a" * 105

        chunks = chunk_text(text, max_chars=50, overlap=0)

        self.assertEqual(len(chunks), 3)
        self.assertEqual([len(c) for c in chunks], [50, 50, 5])
        self.assertTrue(all(len(c) <= 50 for c in chunks))

    def test_chunks_include_overlap_between_segments(self) -> None:
        text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        chunks = chunk_text(text, max_chars=10, overlap=3)

        self.assertGreater(len(chunks), 1)
        for idx in range(len(chunks) - 1):
            self.assertEqual(chunks[idx][-3:], chunks[idx + 1][:3])

    def test_long_text_chunk_output_preserves_content(self) -> None:
        long_text = "".join(str(i % 10) for i in range(5000))

        chunks = chunk_text(long_text, max_chars=1500, overlap=200)

        self.assertEqual(len(chunks), 4)
        self.assertEqual([len(ch) for ch in chunks], [1500, 1500, 1500, 1100])
        for idx in range(len(chunks) - 1):
            self.assertEqual(chunks[idx][-200:], chunks[idx + 1][:200])
        reconstructed = chunks[0] + "".join(chunk[200:] for chunk in chunks[1:])
        self.assertEqual(reconstructed, long_text)


if __name__ == "__main__":
    unittest.main()
