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
