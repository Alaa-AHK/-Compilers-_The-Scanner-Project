"""
===================================================================================
FILE: src/io/file_handler.py
ASSIGNED TO: Subteam 2 (I/O & User Interface - 2 Members)
===================================================================================

[OBJECTIVE]
Handle reading source code files and generating the required output token files.

[RULES & SPECIFICATIONS]
1. Input File Reading (IMPLEMENTED IN THIS MODULE):
   - Accept a file path pointing to a TINY source file (.txt or .tiny).
   - Return the complete source text as a clean, normalized string.
   - Gracefully handle missing files, encoding issues, and empty input.

2. Deliverable Output File Generation (STUB / FUTURE STEP):
   - Accept a list of tokens and a destination file path.
   - Write each token on a new line matching the required project format:
       <token_value>, <token_type>
     Examples:
       x , Identifier
       :=, assign
       4, number
   - Exclude control tokens like ENDFILE from the written output.

3. End-to-End File Processing (FUTURE STEP):
   - Provide a function that connects: Input File -> Scanner -> Output File.
===================================================================================
"""

from pathlib import Path
import sys
from typing import Union, Optional


def normalize_source_input(source: str) -> str:
    """
    Normalizes raw source text for the scanner.

    Rules:
      - Converts CRLF (\r\n) and legacy CR (\r) to standard LF (\n).
      - Preserves tabs and indentation for accurate column tracking.

    Args:
        source (str): Raw input text.

    Returns:
        str: Normalized source text.
    """
    if source is None:
        return ""
    return source.replace("\r\n", "\n").replace("\r", "\n")


def validate_source_code(source: str) -> bool:
    """
    Validates whether the provided source code contains content to scan.

    Args:
        source (str): Source code string to check.

    Returns:
        bool: True if source contains non-whitespace characters, False otherwise.
    """
    if not isinstance(source, str):
        return False
    return bool(source.strip())


def read_source_file(file_path: Union[str, Path], encoding: str = "utf-8") -> str:
    """
    Reads a TINY source code file (.tiny or .txt) from disk.

    Rules:
      - Path must point to an existing file.
      - Uses UTF-8 by default; falls back to latin-1 if decoding fails.
      - Normalizes line endings to \n.

    Args:
        file_path (Union[str, Path]): Absolute or relative path to the source file.
        encoding (str): Primary character encoding to use (default: 'utf-8').

    Returns:
        str: Normalized source code text.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        IsADirectoryError: If the specified path is a directory.
        ValueError: If file path is invalid or empty.
        IOError: If reading the file fails due to permission or OS errors.
    """
    if not file_path:
        raise ValueError("File path cannot be empty.")

    target = Path(file_path)

    if not target.exists():
        raise FileNotFoundError(f"Source file not found: '{file_path}'")

    if not target.is_file():
        raise IsADirectoryError(f"Target path is a directory, not a file: '{file_path}'")

    try:
        content = target.read_text(encoding=encoding)
    except UnicodeDecodeError:
        # Fallback to latin-1 encoding if UTF-8 fails
        content = target.read_text(encoding="latin-1")
    except OSError as err:
        raise IOError(f"Failed to read file '{file_path}': {err}") from err

    return normalize_source_input(content)


def read_source_from_stdin() -> str:
    """
    Reads source code directly from standard input (stdin).
    Useful for piping or CLI redirection.

    Returns:
        str: Normalized source code text read from stdin.
    """
    raw_content = sys.stdin.read()
    return normalize_source_input(raw_content)


# ===================================================================================
# Subteam 2: Output Generation & Processing
# ===================================================================================
def write_token_file(tokens: list, output_path: Union[str, Path], use_spec_casing: bool = True) -> None:
    """
    Writes tokens to output file in format: '<token_value>, <token_type>'

    Rules:
      - Each token is written on a new line.
      - Control tokens such as ENDFILE are excluded.
      - Uses UTF-8 encoding.

    Args:
        tokens (list): List of Token objects.
        output_path (Union[str, Path]): Target output file path.
        use_spec_casing (bool): If True, uses spec-compatible casing (e.g. Identifier, assign, number).
    """
    if not output_path:
        raise ValueError("Output file path cannot be empty.")

    target = Path(output_path)
    target.parent.mkdir(parents=True, exist_ok=True)

    lines = []
    for tok in tokens:
        # Skip control tokens like ENDFILE
        if hasattr(tok, "type") and getattr(tok.type, "name", "") == "ENDFILE":
            continue

        if hasattr(tok, "to_output_format"):
            lines.append(tok.to_output_format(use_spec_casing=use_spec_casing))
        else:
            lines.append(str(tok))

    content = "\n".join(lines)
    if content:
        content += "\n"

    target.write_text(content, encoding="utf-8")


def process_file(input_path: Union[str, Path], output_path: Union[str, Path]) -> list:
    """
    Connects: Input File -> Scanner -> Output File.

    Args:
        input_path (Union[str, Path]): Source TINY file path.
        output_path (Union[str, Path]): Destination token file path.

    Returns:
        list: The list of scanned Token objects.
    """
    from src.scanner.scanner import Scanner

    source_code = read_source_file(input_path)
    scanner = Scanner(source_code)
    tokens = scanner.scan_all()
    write_token_file(tokens, output_path)
    return tokens
