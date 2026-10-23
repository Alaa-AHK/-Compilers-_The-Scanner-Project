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
