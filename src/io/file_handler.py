"""
===================================================================================
FILE: src/io/file_handler.py
ASSIGNED TO: Subteam 2 (I/O & User Interface - 2 Members)
===================================================================================

[OBJECTIVE]
Handle reading source code files and generating the required output token files.

[RULES & SPECIFICATIONS]
1. Input File Reading:
   - Accept a file path pointing to a TINY source file (.txt or .tiny).
   - Return the complete source text as a string.
   - Handle missing files or read errors gracefully.

2. Deliverable Output File Generation:
   - Accept a list of tokens and a destination file path.
   - Write each token on a new line matching the required project format:
       <token_value>, <token_type>
     Examples:
       x , Identifier
       :=, assign
       4, number
   - Exclude control tokens like ENDFILE from the written output.

3. End-to-End File Processing:
   - Provide a function that connects: Input File -> Scanner -> Output File.
===================================================================================
"""
