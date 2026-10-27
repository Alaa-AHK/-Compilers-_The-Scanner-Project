"""
===================================================================================
FILE: main.py
ASSIGNED TO: Subteam 3 (Integration, QA & Build - 1 Member)
===================================================================================

[OBJECTIVE]
Application entry point and execution mode dispatcher (CLI only).

[RULES & SPECIFICATIONS]
1. Mode Dispatching Rules:
   - CLI Mode: If provided with `-i <input_file>` and `-o <output_file>`,
     run headless scanning and generate the output file.
   - Test Mode: If passed `--test`, execute the automated test suite.
   - Default Mode: If launched with no arguments, print usage help and exit
     with a non-zero status.

2. Exit Rules:
   - Return status 0 on clean execution.
   - Return non-zero on file or scanning errors.
===================================================================================
"""

import sys
import argparse
import unittest
from pathlib import Path
from src.utils.helpers import print_banner, format_lexical_error
from src.io.file_handler import process_file
from src.scanner.tokens import TokenType


def run_tests() -> int:
    """Executes the automated test suite."""
    print_banner(mode="TEST SUITE")
    loader = unittest.TestLoader()
    suite = loader.discover("tests")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return 0 if result.wasSuccessful() else 1


def run_cli(input_path: str, output_path: str) -> int:
    """Runs headless scanning and outputs tokens to the specified file."""
    print_banner(mode="CLI")
    print(f"Reading input file:  '{input_path}'")
    print(f"Destination output: '{output_path}'")

    try:
        tokens = process_file(input_path, output_path)
        errors = [t for t in tokens if t.type == TokenType.ERROR]

        print(f"\n[+] Scan completed: {len(tokens)} tokens scanned.")
        if errors:
            print(f"[!] Warning: {len(errors)} lexical error(s) detected:")
            for err in errors:
                print("    " + format_lexical_error(err.line, err.column, "Unrecognized symbol", err.value))
            print(f"[+] Output written with flagged errors to: '{output_path}'")
            return 1
        else:
            print(f"[+] Success: No lexical errors detected.")
            print(f"[+] Output written to: '{output_path}'")
            return 0
    except Exception as ex:
        print(f"\n[-] Error: {ex}", file=sys.stderr)
        return 2


def main() -> int:
    parser = argparse.ArgumentParser(
        description="TINY Language Lexical Analyzer (Scanner)"
    )
    parser.add_argument(
        "-i", "--input",
        help="Path to input TINY source file (.tiny or .txt)"
    )
    parser.add_argument(
        "-o", "--output",
        help="Path to output file for tokens list"
    )
    # parser.add_argument(
    #     "--test",
    #     action="store_true",
    #     help="Run automated test suite"
    # )

    args = parser.parse_args()

    # if args.test:
    #     return run_tests()

    if args.input and args.output:
        return run_cli(args.input, args.output)

    # Default mode: no action specified, show usage help
    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
