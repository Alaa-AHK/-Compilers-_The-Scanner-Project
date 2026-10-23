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
