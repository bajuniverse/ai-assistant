import unittest

from assistant.cli import build_parser


class CliParserTests(unittest.TestCase):
    def test_summary_parses_file_argument(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["summary", "--file", "foo.txt"])
        self.assertEqual(args.command, "summary")
        self.assertEqual(args.file, "foo.txt")
        self.assertIsNone(args.folder)

    def test_summary_parses_folder_argument(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["summary", "--folder", "docs"])
        self.assertEqual(args.command, "summary")
        self.assertEqual(args.folder, "docs")
        self.assertIsNone(args.file)

    def test_ingest_requires_folder(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["ingest", "--folder", "docs"])
        self.assertEqual(args.command, "ingest")
        self.assertEqual(args.folder, "docs")

    def test_ask_requires_question(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["ask", "--question", "What?"])
        self.assertEqual(args.command, "ask")
        self.assertEqual(args.question, "What?")


if __name__ == "__main__":
    unittest.main()
