import unittest

from assistant.embeddings import validate_embeddings


class EmbeddingValidationTests(unittest.TestCase):
    def test_valid_embeddings_return_dimension(self) -> None:
        embeddings = [
            [0.1, 0.2, 0.3],
            [1.0, -1.0, 2.5],
        ]

        dim = validate_embeddings(embeddings)

        self.assertEqual(dim, 3)

    def test_raises_on_mismatched_dimensions(self) -> None:
        embeddings = [
            [0.1, 0.2],
            [0.3, 0.4, 0.5],
        ]

        with self.assertRaises(ValueError):
            validate_embeddings(embeddings)

    def test_raises_on_non_numeric(self) -> None:
        embeddings = [
            [0.1, "oops", 0.3],  # type: ignore[list-item]
        ]

        with self.assertRaises(TypeError):
            validate_embeddings(embeddings)

    def test_raises_on_empty_embeddings(self) -> None:
        with self.assertRaises(ValueError):
            validate_embeddings([])


if __name__ == "__main__":
    unittest.main()
