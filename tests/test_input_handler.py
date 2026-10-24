"""
Unit tests for Input Handling (src/io/file_handler.py)
"""

import unittest
from pathlib import Path
from src.io.file_handler import (
    read_source_file,
    normalize_source_input,
    validate_source_code,
)


class TestInputHandler(unittest.TestCase):
    def setUp(self):
        self.samples_dir = Path(__file__).resolve().parent.parent / "samples"
        self.sample_file = self.samples_dir / "sample_factorial.tiny"

    def test_read_existing_source_file(self):
        content = read_source_file(self.sample_file)
        self.assertIsInstance(content, str)
        self.assertIn("read x;", content)
        self.assertIn("fact := 1;", content)
        self.assertNotIn("\r\n", content, "All line endings should be normalized to LF")

    def test_read_nonexistent_file_raises_error(self):
        with self.assertRaises(FileNotFoundError):
            read_source_file("non_existent_file.tiny")

    def test_read_empty_path_raises_value_error(self):
        with self.assertRaises(ValueError):
            read_source_file("")

    def test_normalize_source_input(self):
        crlf_text = "read x;\r\nfact := 1;\r\n"
        normalized = normalize_source_input(crlf_text)
        self.assertEqual(normalized, "read x;\nfact := 1;\n")

        cr_text = "line1\rline2"
        self.assertEqual(normalize_source_input(cr_text), "line1\nline2")
        self.assertEqual(normalize_source_input(""), "")
        self.assertEqual(normalize_source_input(None), "")

    def test_validate_source_code(self):
        self.assertTrue(validate_source_code("read x;"))
        self.assertFalse(validate_source_code(""))
        self.assertFalse(validate_source_code("   \n\t  "))
        self.assertFalse(validate_source_code(None))


if __name__ == "__main__":
    unittest.main()
