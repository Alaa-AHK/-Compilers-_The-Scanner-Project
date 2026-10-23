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
