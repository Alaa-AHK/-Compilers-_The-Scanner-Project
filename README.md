# TINY Language Scanner

A lexical analyzer for the TINY programming language, written in Python.
It reads a TINY source file and writes out the list of tokens it finds,
one per line, in the form `value, type`.

## Project layout

```text
.
├── main.py                 # Entry point and command line handling
├── build_exe.bat           # Builds the Windows executable
├── requirements.txt        # PyInstaller, for packaging only
│
├── src/
│   ├── scanner/
│   │   ├── tokens.py       # Token types, keyword table, output formatting
│   │   ├── dfa.py          # Scanner states
│   │   └── scanner.py      # getToken() and the scanning loop
│   ├── io/
│   │   └── file_handler.py # Reading source files, writing token files
│   └── utils/
│       └── helpers.py      # Console output and error message formatting
│
├── tests/
│   └── test_scanner.py     # Unit tests
│
└── samples/                # Example TINY programs
    ├── sample_factorial.tiny
    └── sample_test.tiny
```

## Requirements

- Python 3.8 or newer (standard library only, no dependencies)
- PyInstaller, only if you want to build the standalone `.exe`

## Running from source

```bash
python main.py -i samples/sample_factorial.tiny -o output_tokens.txt
```

| Option | Meaning |
| :--- | :--- |
| `-i`, `--input` | Path to the TINY source file to scan |
| `-o`, `--output` | Path to write the token list to |

Both options are required. Running `python main.py` with no arguments prints
the usage help.

Exit codes: `0` on a clean scan, `1` if lexical errors were found, `2` if the
input file could not be read.

## Running the executable

A standalone build needs no Python installed. It takes the same arguments:

```cmd
dist\TinyScanner\TinyScanner.exe -i samples\sample_factorial.tiny -o output_tokens.txt
```

## Building the executable

```cmd
build_exe.bat
```

The result is `dist\TinyScanner\TinyScanner.exe`. Note that the build wipes
`dist\TinyScanner\` first, so close anything open in that folder before
running it, and keep your test files elsewhere.

## Running the tests

```bash
python -m unittest discover tests
```

Run this from the project root, otherwise the `src` package will not be found.

## Output format

Each recognized token is written on its own line as `value, type`:

```text
read, READ
x, Identifier
;, SEMICOLON
if, IF
0, number
<, LESSTHAN
x, Identifier
then, THEN
```

Comments enclosed in `{ ... }` are skipped. Anything that does not form a
legal token is reported as `ERROR`.

## Tokens

Reserved words: `if`, `then`, `end`, `repeat`, `until`, `read`, `write`.
These are case-sensitive, so `IF` scans as an identifier, not a keyword.

Symbols: `;` `<` `=` `+` `-` `*` `/` `(` `)` `:=`

An identifier is a sequence of letters; a number is a sequence of digits.

