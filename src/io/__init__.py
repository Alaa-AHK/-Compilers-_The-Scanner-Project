"""
Package: src/io
Maintained by: Subteam 2 (I/O & User Interface - 2 Members)

Exports input file handling and normalization functions.
"""

from .file_handler import (
    read_source_file,
    read_source_from_stdin,
    normalize_source_input,
    validate_source_code,
)

__all__ = [
    "read_source_file",
    "read_source_from_stdin",
    "normalize_source_input",
    "validate_source_code",
]
