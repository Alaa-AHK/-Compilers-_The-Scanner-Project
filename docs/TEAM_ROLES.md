# Subteams Breakdown & Project Rules (2, 2, 1 Division)

---

## 👥 Subteams Overview

```
                         ┌─────────────────────────────┐
                         │    TINY SCANNER PROJECT     │
                         └──────────────┬──────────────┘
                                        │
         ┌──────────────────────────────┼──────────────────────────────┐
         ▼                              ▼                              ▼
     Subteam 1                      Subteam 2                      Subteam 3
  (2 Students)                   (2 Students)                   (1 Student)
  Core Lexical Engine            I/O & User Interface           Integration & Build
```

---

### 🔹 Subteam 1: Core Lexical Engine (2 Students)
- **Module Path:** `src/scanner/`
- **Assigned Files:**
  - `src/scanner/tokens.py`
  - `src/scanner/dfa.py`
  - `src/scanner/scanner.py`
  - `src/scanner/__init__.py`
- **Objective:** Build the lexical analyzer engine that reads TINY code and generates tokens.
- **Rules & Deliverables:**
  1. Define all language tokens (Keywords: `if`, `then`, `end`, `repeat`, `until`, `read`, `write`; Symbols: `;`, `<`, `=`, `+`, `-`, `*`, `/`, `(`, `)`, `:=`; Dynamic: `IDENTIFIER`, `NUMBER`; Control: `ENDFILE`, `ERROR`).
  2. Implement `getToken()` returning the next token with computed attributes (lexeme, line, column).
  3. Format tokens as `<token_value>, <token_type>` (e.g. `x , Identifier`, `:=, assign`, `4, number`).
  4. Skip all comments `{ ... }` and whitespace without producing tokens.
  5. Identify illegal characters and emit `ERROR` tokens.

---

### 🔹 Subteam 2: I/O & User Interface (2 Students)
- **Module Paths:** `src/io/`, `src/gui/`
- **Assigned Files:**
  - `src/io/file_handler.py`
  - `src/gui/app.py`
- **Objective:** Handle input/output files and provide the desktop GUI for program snapshots.
- **Rules & Deliverables:**
  1. **File I/O:** Read input code from `.tiny` / `.txt` files and write formatted token lists to the destination file.
  2. **Desktop GUI (Tkinter):** Built strictly with standard Python libraries so it runs on Windows without installations (Deliverable #2: Snapshots).
  3. **Interface Layout:** Dual-pane layout (Code Editor on the left, Token Table on the right) with buttons: `Open File`, `Scan Code`, `Save Output`, and `Clear`.
  4. **Status Reporting:** Show scanned token count and highlight any lexical errors.

---

### 🔹 Subteam 3: Integration, QA & Packaging (1 Student)
- **Root & Test Paths:** Root, `tests/`, `src/utils/`
- **Assigned Files:**
  - `main.py`
  - `tests/test_scanner.py`
  - `src/utils/helpers.py`
  - `build_exe.bat`
- **Objective:** Application entry point, automated test verification, and Windows `.exe` creation.
- **Rules & Deliverables:**
  1. **Main Entry (`main.py`):** Launch GUI mode by default; run headless CLI mode when given input/output arguments.
  2. **Automated QA (`tests/test_scanner.py`):** Assert correctness of all tokens, comment stripping, and format compliance.
  3. **Windows Executable (`build_exe.bat`):** Package the project into a standalone Windows `.exe` requiring no third-party installations (Deliverable #1).
