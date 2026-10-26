"""
===================================================================================
FILE: src/scanner/scanner.py
ASSIGNED TO: Subteam 1 (Core Lexical Engine - 2 Members)
===================================================================================

[OBJECTIVE]
Implement the core scanner engine that reads source text and extracts tokens.

[RULES & SPECIFICATIONS]
1. Primary Method - getToken():
   - MUST return the next token from the input source.
   - MUST compute token attributes (lexeme value, line number, column number).
   - MUST distinguish keywords from generic identifiers.
   - MUST skip all comments '{ ... }' and whitespace without returning tokens.
   - MUST return an ENDFILE token when the source text is exhausted.
   - MUST return an ERROR token for any unrecognized character.

2. Batch Method - scan_all():
   - Repeatedly calls getToken() until ENDFILE is reached.
   - Returns the complete list of recognized tokens.
===================================================================================
"""

from typing import List, Optional
from src.scanner.tokens import (
    Token,
    TokenType,
    KEYWORDS,
    SINGLE_CHAR_SYMBOLS,
)
from src.scanner.dfa import State


class Scanner:
    """
    Lexical analyzer for the TINY language.
    Reads an input source string and provides getToken() to extract tokens sequentially.
    """

    def __init__(self, source_code: str):
        # Normalize source input
        self.source: str = source_code if source_code is not None else ""
        self.length: int = len(self.source)
        self.cursor: int = 0
        self.line: int = 1
        self.column: int = 1

    def _peek(self) -> Optional[str]:
        """Returns the next character without advancing the cursor, or None if EOF."""
        if self.cursor < self.length:
            return self.source[self.cursor]
        return None

    def _get_char(self) -> Optional[str]:
        """Consumes and returns the next character, updating line and column counters."""
        if self.cursor >= self.length:
            return None
        ch = self.source[self.cursor]
        self.cursor += 1
        if ch == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return ch

    def _unget_char(self, ch: str) -> None:
        """Pushes back a consumed character (lookahead rollback)."""
        if self.cursor > 0:
            self.cursor -= 1
            if ch == "\n":
                self.line -= 1
                # Find previous column
                prev_nl = self.source.rfind("\n", 0, self.cursor)
                if prev_nl == -1:
                    self.column = self.cursor + 1
                else:
                    self.column = self.cursor - prev_nl
            else:
                self.column -= 1

    def getToken(self) -> Token:
        """
        Extracts and returns the next Token from the source code.
        Implements DFA state transitions for TINY language.
        """
        state = State.START
        token_string: List[str] = []
        token_line = self.line
        token_col = self.column

        while state != State.DONE:
            ch = self._get_char()

            if ch is None:
                # Reached End of File (EOF)
                if state == State.START:
                    return Token(TokenType.ENDFILE, "", token_line, token_col)
                elif state == State.IN_NUM:
                    return Token(TokenType.NUMBER, "".join(token_string), token_line, token_col)
                elif state == State.IN_ID:
                    lexeme = "".join(token_string)
                    token_type = KEYWORDS.get(lexeme.lower(), TokenType.IDENTIFIER)
                    return Token(token_type, lexeme, token_line, token_col)
                elif state == State.IN_ASSIGN:
                    # Incomplete assignment operator at EOF
                    return Token(TokenType.ERROR, ":", token_line, token_col)
                elif state == State.IN_COMMENT:
                    # Unterminated comment at EOF
                    return Token(TokenType.ERROR, "Unterminated comment '{...}'", token_line, token_col)

            if state == State.START:
                # Save starting coordinates of the token
                token_line = self.line if ch == "\n" else (self.line if self.column > 1 else self.line)
                token_col = self.column - 1 if ch != "\n" else 1

                # Whitespace: ignore and stay in START
                if ch in " \t\r\n":
                    continue

                # Comment: enter IN_COMMENT state
                elif ch == "{":
                    state = State.IN_COMMENT
                    continue

                # Number: starts with a digit
                elif ch.isdigit():
                    state = State.IN_NUM
                    token_string.append(ch)

                # Identifier or Keyword: starts with a letter
                elif ch.isalpha():
                    state = State.IN_ID
                    token_string.append(ch)

                # Assignment operator ':='
                elif ch == ":":
                    state = State.IN_ASSIGN
                    token_string.append(ch)

                # Single-character special symbols
                elif ch in SINGLE_CHAR_SYMBOLS:
                    return Token(SINGLE_CHAR_SYMBOLS[ch], ch, token_line, token_col)

                # Unrecognized character
                else:
                    return Token(TokenType.ERROR, ch, token_line, token_col)

            elif state == State.IN_COMMENT:
                if ch == "}":
                    state = State.START

            elif state == State.IN_NUM:
                if ch.isdigit():
                    token_string.append(ch)
                else:
                    # Non-digit: put character back and finalize NUMBER token
                    self._unget_char(ch)
                    return Token(TokenType.NUMBER, "".join(token_string), token_line, token_col)

            elif state == State.IN_ID:
                if ch.isalpha():
                    token_string.append(ch)
                else:
                    # Non-alpha: put character back and check keywords vs identifier
                    self._unget_char(ch)
                    lexeme = "".join(token_string)
                    token_type = KEYWORDS.get(lexeme.lower(), TokenType.IDENTIFIER)
                    return Token(token_type, lexeme, token_line, token_col)

            elif state == State.IN_ASSIGN:
                if ch == "=":
                    token_string.append(ch)
                    return Token(TokenType.ASSIGN, ":=", token_line, token_col)
                else:
                    # Lone ':' is invalid in TINY
                    self._unget_char(ch)
                    return Token(TokenType.ERROR, ":", token_line, token_col)

        return Token(TokenType.ENDFILE, "", self.line, self.column)

    def scan_all(self) -> List[Token]:
        """
        Convenience method to scan all tokens until ENDFILE is reached.
        Returns a list of all tokens (excluding ENDFILE).
        """
        tokens: List[Token] = []
        while True:
            tok = self.getToken()
            if tok.type == TokenType.ENDFILE:
                break
            tokens.append(tok)
        return tokens
