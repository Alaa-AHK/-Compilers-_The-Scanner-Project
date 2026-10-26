"""
===================================================================================
FILE: src/scanner/dfa.py
ASSIGNED TO: Subteam 1 (Core Lexical Engine - 2 Members)
===================================================================================

[OBJECTIVE]
Define the Deterministic Finite Automaton (DFA) states and transition rules for TINY.

[RULES & SPECIFICATIONS]
1. States Required:
   - START: Ready to consume the next token.
   - IN_NUM: Processing numeric digits.
   - IN_ID: Processing alphabetic characters.
   - IN_ASSIGN: Processing ':' leading into ':='.
   - IN_COMMENT: Inside comment delimiters '{' and '}'.
   - DONE: Token successfully recognized.

2. State Rules:
   - Whitespace: Ignored in START state.
   - Comments: Everything between '{' and '}' must be skipped; do not emit tokens.
   - Assignment: A lone ':' is invalid; only ':=' is recognized.
   - Delimiters: Single-character symbols (';', '+', '-', '*', '/', '(', ')', '<', '=')
     transition immediately to DONE.
===================================================================================
"""

from enum import Enum, auto


class State(Enum):
    """
    DFA states for the TINY language lexical analyzer.
    """
    START = auto()       # Initial state before reading a token
    IN_NUM = auto()      # Accumulating digit characters
    IN_ID = auto()       # Accumulating alphabetic identifier/keyword characters
    IN_ASSIGN = auto()   # Saw ':', expecting '=' next
    IN_COMMENT = auto()  # Inside '{ ... }', skipping contents until '}'
    DONE = auto()        # Token recognition complete
