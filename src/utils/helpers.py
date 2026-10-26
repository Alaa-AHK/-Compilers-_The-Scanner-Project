"""
===================================================================================
FILE: src/utils/helpers.py
ASSIGNED TO: Subteam 3 (Integration, QA & Build - 1 Member)
===================================================================================

[OBJECTIVE]
Shared logging, CLI diagnostics, and lexical error formatting.

[RULES & SPECIFICATIONS]
1. Error Formatting:
   - Provide a standard format for reporting scanner errors:
     e.g., "[Line X, Column Y]: Lexical Error -> Unrecognized character 'Z'"

2. Diagnostics:
   - Provide a console header/banner displaying project title and execution mode.
===================================================================================
"""

from typing import Optional


def format_lexical_error(line: int, column: int, message: str, character: Optional[str] = None) -> str:
    """
    Formats a lexical error message consistently.

    Args:
        line (int): Line number of error.
        column (int): Column number of error.
        message (str): Description of the error.
        character (Optional[str]): Unrecognized character or lexeme.

    Returns:
        str: Formatted error string.
    """
    if character:
        return f"[Line {line}, Column {column}]: Lexical Error -> {message} '{character}'"
    return f"[Line {line}, Column {column}]: Lexical Error -> {message}"


def print_banner(mode: str = "GUI") -> None:
    """
    Prints a clean console diagnostic header for the application.
    """
    banner = f"""
=============================================================
  TINY Language Lexical Analyzer (Scanner Project)
  Execution Mode: {mode.upper()}
=============================================================
"""
    print(banner.strip())
