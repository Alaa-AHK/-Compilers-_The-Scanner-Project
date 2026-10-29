"""
FILE: src/io/file_handler.py
Handle reading source code files and generating the required output token files.
"""

from pathlib import Path
import sys
from typing import Union, Optional
from src.scanner.scanner import Scanner

# ===========================================================
# Input Handling & Normalization
# ===========================================================

def normalize_source_input(source: str) -> str:
    if source is None:
        return ""
    return source.replace("\r\n", "\n").replace("\r", "\n")


def validate_source_code(source: str) -> bool:
    if not isinstance(source, str):
        return False
    return bool(source.strip())


def read_source_file(file_path: Union[str, Path], encoding: str = "utf-8") -> str:
    """
    Reads a TINY source code file (.tiny or .txt) from disk and returns its content as a normalized string.
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
    """
    raw_content = sys.stdin.read()
    return normalize_source_input(raw_content)


# ===================================================================================
# Output Generation & Processing
# ===================================================================================
def write_token_file(tokens: list, output_path: Union[str, Path], use_spec_casing: bool = True) -> None:
    """
    Writes tokens to output file in format: '<token_value>, <token_type>'
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
    """
    source_code = read_source_file(input_path)
    scanner = Scanner(source_code)
    tokens = scanner.scan_all()
    write_token_file(tokens, output_path)
    return tokens