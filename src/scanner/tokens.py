"""
===================================================================================
FILE: src/scanner/tokens.py
ASSIGNED TO: Subteam 1 (Core Lexical Engine - 2 Members)
===================================================================================

[OBJECTIVE]
Define the language vocabulary, token representations, and formatting rules.

[RULES & SPECIFICATIONS]
1. Supported Token Types:
   - Reserved Keywords: 'if', 'then', 'end', 'repeat', 'until', 'read', 'write'
   - Special Symbols: ';', '<', '=', '+', '-', '*', '/', '(', ')', ':='
   - Dynamic Tokens:
       * IDENTIFIER: Any sequence of letters (e.g. 'x', 'abc', 'xyz')
       * NUMBER: Any sequence of digits (e.g. '12', '289')
   - Control Tokens: ENDFILE, ERROR

2. Token Data Structure:
   - Must encapsulate: token type, string value (lexeme), line number, column number.

3. Output Formatting Rule:
   - Every token must format as: "<token_value>, <token_type>"
   - Examples from spec:
       x , Identifier
       :=, assign
       4, number
===================================================================================
"""

from enum import Enum, auto
from typing import Dict, Any


class TokenType(Enum):
    # Reserved Keywords
    IF = auto()
    THEN = auto()
    END = auto()
    REPEAT = auto()
    UNTIL = auto()
    READ = auto()
    WRITE = auto()

    # Special Symbols
    SEMICOLON = auto()
    LESSTHAN = auto()
    EQUAL = auto()
    PLUS = auto()
    MINUS = auto()
    MULT = auto()
    DIV = auto()
    OPENBRACKET = auto()
    CLOSEDBRACKET = auto()
    ASSIGN = auto()

    # Dynamic Tokens
    IDENTIFIER = auto()
    NUMBER = auto()

    # Control / Error Tokens
    ENDFILE = auto()
    ERROR = auto()


# Mapping of reserved keywords (lowercase) to their TokenType
KEYWORDS: Dict[str, TokenType] = {
    "if": TokenType.IF,
    "then": TokenType.THEN,
    "end": TokenType.END,
    "repeat": TokenType.REPEAT,
    "until": TokenType.UNTIL,
    "read": TokenType.READ,
    "write": TokenType.WRITE,
}

# Mapping of single-character special symbols to their TokenType
SINGLE_CHAR_SYMBOLS: Dict[str, TokenType] = {
    ";": TokenType.SEMICOLON,
    "<": TokenType.LESSTHAN,
    "=": TokenType.EQUAL,
    "+": TokenType.PLUS,
    "-": TokenType.MINUS,
    "*": TokenType.MULT,
    "/": TokenType.DIV,
    "(": TokenType.OPENBRACKET,
    ")": TokenType.CLOSEDBRACKET,
}

# Canonical output display names as shown in the project specification table & examples
SPEC_DISPLAY_NAMES: Dict[TokenType, str] = {
    TokenType.SEMICOLON: "SEMICOLON",
    TokenType.IF: "IF",
    TokenType.THEN: "THEN",
    TokenType.END: "END",
    TokenType.REPEAT: "REPEAT",
    TokenType.UNTIL: "UNTIL",
    TokenType.IDENTIFIER: "Identifier",  # Matches spec example: "x , Identifier"
    TokenType.ASSIGN: "assign",          # Matches spec example: ":=, assign"
    TokenType.READ: "READ",
    TokenType.WRITE: "WRITE",
    TokenType.LESSTHAN: "LESSTHAN",
    TokenType.EQUAL: "EQUAL",
    TokenType.PLUS: "PLUS",
    TokenType.MINUS: "MINUS",
    TokenType.MULT: "MULT",
    TokenType.DIV: "DIV",
    TokenType.OPENBRACKET: "OPENBRACKET",
    TokenType.CLOSEDBRACKET: "CLOSEDBRACKET",
    TokenType.NUMBER: "number",          # Matches spec example: "4, number"
    TokenType.ERROR: "ERROR",
    TokenType.ENDFILE: "ENDFILE",
}


class Token:
    """
    Represents a recognized lexical token in TINY.

    Attributes:
        type (TokenType): The enumerated category of the token.
        value (str): The literal lexeme string from the source code.
        line (int): 1-indexed source line where the token starts.
        column (int): 1-indexed source column where the token starts.
    """

    def __init__(self, token_type: TokenType, value: str, line: int = 1, column: int = 1):
        self.type = token_type
        self.value = value
        self.line = line
        self.column = column

    @property
    def type_name(self) -> str:
        """Returns the canonical token type name (e.g. 'IDENTIFIER', 'ASSIGN')."""
        return self.type.name

    @property
    def display_type(self) -> str:
        """Returns the spec-matched display type name (e.g. 'Identifier', 'assign')."""
        return SPEC_DISPLAY_NAMES.get(self.type, self.type.name)

    def to_output_format(self, use_spec_casing: bool = True) -> str:
        """
        Formats token matching the project output file rule:
            <token_value>, <token_type>
        Examples:
            x , Identifier
            :=, assign
            4, number
        """
        type_str = self.display_type if use_spec_casing else self.type_name
        return f"{self.value}, {type_str}"

    def __repr__(self) -> str:
        return f"Token({self.type.name}, {self.value!r}, line={self.line}, col={self.column})"

    def __str__(self) -> str:
        return self.to_output_format()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Token):
            return False
        return (
            self.type == other.type
            and self.value == other.value
            and self.line == other.line
            and self.column == other.column
        )
