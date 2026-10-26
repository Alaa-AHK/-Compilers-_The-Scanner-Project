"""
===================================================================================
FILE: tests/test_scanner.py
ASSIGNED TO: Subteam 3 (Integration, QA & Build - 1 Member)
===================================================================================

[OBJECTIVE]
Automated Quality Assurance suite verifying scanner correctness.

[RULES & SPECIFICATIONS]
1. Test Coverage Rules:
   - Keywords: Verify 'if', 'then', 'end', 'repeat', 'until', 'read', 'write'.
   - Symbols: Verify ';', '<', '=', '+', '-', '*', '/', '(', ')', ':='.
   - Identifiers vs Keywords: Verify that words like 'read' are keywords, while
     'reading' or 'x' are treated as generic identifiers.
   - Numbers: Verify integers such as '12', '289', '0'.
   - Comments: Verify that any text inside '{ ... }' produces no tokens.
   - Error Tokens: Verify that illegal characters (e.g. '@', '$') yield ERROR tokens.
   - Output Format: Verify token string matches "<tokenvalue>, <tokentype>".
===================================================================================
"""

import unittest
from pathlib import Path
from src.scanner.tokens import TokenType, Token
from src.scanner.scanner import Scanner
from src.io.file_handler import read_source_file


class TestScanner(unittest.TestCase):
    def test_keywords(self):
        source = "if then end repeat until read write"
        scanner = Scanner(source)
        tokens = scanner.scan_all()
        expected = [
            TokenType.IF,
            TokenType.THEN,
            TokenType.END,
            TokenType.REPEAT,
            TokenType.UNTIL,
            TokenType.READ,
            TokenType.WRITE,
        ]
        self.assertEqual([t.type for t in tokens], expected)

    def test_symbols(self):
        source = "; < = + - * / ( ) :="
        scanner = Scanner(source)
        tokens = scanner.scan_all()
        expected = [
            TokenType.SEMICOLON,
            TokenType.LESSTHAN,
            TokenType.EQUAL,
            TokenType.PLUS,
            TokenType.MINUS,
            TokenType.MULT,
            TokenType.DIV,
            TokenType.OPENBRACKET,
            TokenType.CLOSEDBRACKET,
            TokenType.ASSIGN,
        ]
        self.assertEqual([t.type for t in tokens], expected)

    def test_identifiers_vs_keywords(self):
        source = "read reading x if iffy"
        scanner = Scanner(source)
        tokens = scanner.scan_all()
        self.assertEqual(tokens[0].type, TokenType.READ)
        self.assertEqual(tokens[1].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[1].value, "reading")
        self.assertEqual(tokens[2].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[2].value, "x")
        self.assertEqual(tokens[3].type, TokenType.IF)
        self.assertEqual(tokens[4].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[4].value, "iffy")

    def test_numbers(self):
        source = "12 289 0 405"
        scanner = Scanner(source)
        tokens = scanner.scan_all()
        for tok in tokens:
            self.assertEqual(tok.type, TokenType.NUMBER)
        self.assertEqual([t.value for t in tokens], ["12", "289", "0", "405"])

    def test_comments_skipped(self):
        source = "{ comment 1 } x := 5; { multiline\ncomment } y := 10;"
        scanner = Scanner(source)
        tokens = scanner.scan_all()
        lexemes = [t.value for t in tokens]
        self.assertEqual(lexemes, ["x", ":=", "5", ";", "y", ":=", "10", ";"])

    def test_error_tokens(self):
        source = "@ $ : 123"
        scanner = Scanner(source)
        tokens = scanner.scan_all()
        self.assertEqual(tokens[0].type, TokenType.ERROR)
        self.assertEqual(tokens[0].value, "@")
        self.assertEqual(tokens[1].type, TokenType.ERROR)
        self.assertEqual(tokens[1].value, "$")
        self.assertEqual(tokens[2].type, TokenType.ERROR)
        self.assertEqual(tokens[2].value, ":")
        self.assertEqual(tokens[3].type, TokenType.NUMBER)
        self.assertEqual(tokens[3].value, "123")

    def test_output_format(self):
        tok1 = Token(TokenType.IDENTIFIER, "x", line=1, column=1)
        tok2 = Token(TokenType.ASSIGN, ":=", line=1, column=3)
        tok3 = Token(TokenType.NUMBER, "4", line=1, column=6)

        self.assertEqual(tok1.to_output_format(), "x, Identifier")
        self.assertEqual(tok2.to_output_format(), ":=, assign")
        self.assertEqual(tok3.to_output_format(), "4, number")

    def test_sample_factorial(self):
        sample_path = Path(__file__).resolve().parent.parent / "samples" / "sample_factorial.tiny"
        source = read_source_file(sample_path)
        scanner = Scanner(source)
        tokens = scanner.scan_all()
        self.assertTrue(len(tokens) > 0)
        # Check that no ERROR tokens were emitted for valid factorial code
        error_tokens = [t for t in tokens if t.type == TokenType.ERROR]
        self.assertEqual(error_tokens, [])


if __name__ == "__main__":
    unittest.main()
