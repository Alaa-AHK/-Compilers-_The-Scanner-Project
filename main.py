"""
===================================================================================
FILE: main.py
ASSIGNED TO: Subteam 3 (Integration, QA & Build - 1 Member)
===================================================================================

[OBJECTIVE]
Application entry point and execution mode dispatcher.

[RULES & SPECIFICATIONS]
1. Mode Dispatching Rules:
   - Default Mode: If launched with no arguments (or by double-clicking the .exe),
     launch the Graphical User Interface (Subteam 2's GUI).
   - CLI Mode: If provided with `-i <input_file>` and `-o <output_file>`,
     run headless scanning and generate the output file without opening a window.
   - Test Mode: If passed `--test`, execute the automated test suite.

2. Exit Rules:
   - Return status 0 on clean execution.
   - Return non-zero on file or scanning errors.
===================================================================================
"""
