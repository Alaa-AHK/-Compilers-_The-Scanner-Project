"""
===================================================================================
FILE: src/gui/app.py
ASSIGNED TO: Subteam 2 (I/O & User Interface - 2 Members)
===================================================================================

[OBJECTIVE]
Desktop Graphical User Interface satisfying Deliverable #2 (Program Snapshots).

[RULES & SPECIFICATIONS]
1. UI Layout Requirements:
   - Built exclusively with Python standard library (Tkinter) so it compiles to .exe.
   - Dual-pane layout:
       * Left Pane: Text editor for typing, pasting, or loading TINY source code.
       * Right Pane: Table/list displaying scanned tokens (Value, Type, Line).
   - Control Buttons:
       * [Open File]: Load a TINY source file into the editor.
       * [Scan Code]: Run the scanner on current editor text and populate the token table.
       * [Save Output]: Export the token list into the required format file.
       * [Clear]: Reset editor and token table.

2. Presentation Rules:
   - Display a status bar showing the total count of scanned tokens and errors.
   - Highlight or flag any lexical ERROR tokens visually.
===================================================================================
"""
