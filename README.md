# TINY Language Lexical Analyzer (Scanner Project)

A lexical analyzer for the TINY programming language implemented in Python. Organized by subteams according to the 2, 2, 1 team division.

---

## 👥 Subteams Overview (2, 2, 1 Division)

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

| Subteam | Size | Scope | Assigned Files | Objective & Rules |
| :--- | :--- | :--- | :--- | :--- |
| **Subteam 1** | 2 Students | Core Lexical Engine | `src/scanner/tokens.py`<br>`src/scanner/dfa.py`<br>`src/scanner/scanner.py` | Implement `getToken()`, define tokens & DFA states, ignore `{...}` comments, format tokens. |
| **Subteam 2** | 2 Students | I/O & User Interface | `src/io/file_handler.py`<br>`src/gui/app.py` | Read/write token files (`value, type`) and provide Tkinter GUI for program snapshots. |
| **Subteam 3** | 1 Student | Integration & Packaging | `main.py`<br>`tests/test_scanner.py`<br>`build_exe.bat` | CLI/GUI dispatcher, automated test suite, and Windows `.exe` packaging. |

---

## 📂 Formal Project Folder Structure

```text
Compilers/
├── .gitignore                      # Git ignore patterns
├── README.md                       # Project documentation
├── requirements.txt                # Packaging dependencies (pyinstaller)
├── build_exe.bat                   # [Subteam 3] Windows .exe compilation script
├── main.py                         # [Subteam 3] Application entry point (CLI/GUI)
│
├── src/
│   ├── scanner/                    # === SUBTEAM 1: CORE LEXICAL ENGINE (2 Students) ===
│   │   ├── tokens.py               # Token definitions & formatting rules
│   │   ├── dfa.py                  # DFA states & transition rules
│   │   └── scanner.py              # getToken() scanner engine
│   │
│   ├── io/                         # === SUBTEAM 2: I/O & GUI (2 Students) ===
│   │   └── file_handler.py         # File input reading & output serialization
│   │
│   ├── gui/
│   │   └── app.py                  # Tkinter desktop GUI (for Snapshots)
│   │
│   └── utils/                      # === SUBTEAM 3: INTEGRATION & QA (1 Student) ===
│       └── helpers.py              # Diagnostics and error formatting
│
├── tests/
│   └── test_scanner.py             # [Subteam 3] Automated test suite
│
└── samples/                        # Sample TINY code snippets
    ├── sample_factorial.tiny
    └── sample_test.tiny
```

---

## 🚀 How to Run the Project

### 1. Launch GUI Mode (for Screenshots):
```bash
python main.py
```

### 2. Run CLI Mode:
```bash
python main.py -i samples/sample_factorial.tiny -o output_tokens.txt
```

### 3. Run Automated Tests:
```bash
python -m unittest discover tests
```

### 4. Build Standalone Windows Executable (`.exe`):
```cmd
build_exe.bat
```
The standalone `.exe` will be generated inside the `dist/` directory.
