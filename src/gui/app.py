"""
===================================================================================
FILE: src/gui/app.py
ASSIGNED TO: Subteam 2 (I/O & User Interface - 2 Members)
===================================================================================

[OBJECTIVE]
Desktop Graphical User Interface satisfying Deliverable #2 (Program Snapshots).
Dedicated eye-comfortable "Purple x Black" OLED dark theme with pure Python standard library.

[FEATURES]
1. Dual-pane layout:
   - Source code editor with synchronized line numbers and soft syntax highlighting.
   - Scanned tokens table with live filtering (All, Keywords, IDs, Numbers, Symbols, Errors)
     and search.
2. Low-strain "Purple x Black" palette: Deep charcoal/black surfaces with muted,
   elegant royal purple accents designed for visual comfort.
3. Interactive token selection: Clicking any token in the table jumps the editor cursor
   to that exact line and highlights the lexeme with a deep violet glow.
4. Stat Badges (Tokens count, Error badge, Lines count).
5. File actions: Open, Scan, Save Output (Deliverable #2 format), Clear, and Sample Loaders.
===================================================================================
"""

import sys
import re
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from typing import List, Optional, Dict, Any

# Ensure parent directory is in path for imports
parent_dir = Path(__file__).resolve().parent.parent.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

from src.scanner.scanner import Scanner
from src.scanner.tokens import Token, TokenType, KEYWORDS, SINGLE_CHAR_SYMBOLS
from src.io.file_handler import read_source_file, write_token_file


# Dedicated "Purple x Black" Palette - Engineered for eye comfort
THEME: Dict[str, str] = {
    "bg": "#0a090f",              # Deep Obsidian Black Base
    "panel_bg": "#121019",        # Charcoal-Black Surface
    "header_bg": "#07060a",       # Pure Deep Black Header
    "header_fg": "#ede9fe",       # Soft Lavender White (No harsh glare)
    "header_sub": "#a78bfa",      # Gentle Lilac Accent
    "fg": "#e2d9f3",              # Primary Soft Text
    "fg_sub": "#786f8c",          # Muted Dusk Violet-Gray
    "border": "#241c36",          # Subtle Dark Purple Border
    "editor_bg": "#0c0a12",       # OLED Dark Code Canvas
    "editor_fg": "#e2d9f3",       # Comfortable Code Text
    "gutter_bg": "#08070d",       # Dark Line Gutter
    "gutter_fg": "#4e4366",       # Discreet Gutter Numbers
    "cursor": "#c084fc",          # Soft Lilac Caret
    "select_bg": "#31234f",       # Deep Violet Selection
    "tree_bg": "#0c0a12",         # Table Canvas
    "tree_row_even": "#0c0a12",
    "tree_row_odd": "#14111c",    # Gentle Alternating Row
    "tree_fg": "#e2d9f3",
    "tree_header_bg": "#08060d",  # Table Column Header
    "tree_header_fg": "#a78bfa",  # Soft Lilac Column Titles
    "tree_select_bg": "#581c87",  # Deep Royal Violet Selection
    "tree_select_fg": "#ffffff",
    "error_bg": "#330d17",        # Deep Dark Wine Red
    "error_fg": "#f87171",        # Soft Pastel Red Error
    "card_bg": "#121019",
    "card_border": "#241c36",
    "primary_accent": "#6d28d9",  # Rich Royal Purple 700 (Calm, Not Blinding)
    "primary_accent_hover": "#5b21b6",
    "btn_sec_bg": "#1a1626",      # Muted Dark Purple-Black Secondary Button
    "btn_sec_border": "#28203b",
    "btn_sec_fg": "#c4b5fd",
    "btn_sec_hover": "#261f38",
    "badge_tokens_bg": "#1c152e", # Deep Violet Badge
    "badge_tokens_fg": "#c4b5fd", # Soft Lilac
    "badge_err_ok_bg": "#0d241c", # Dark Emerald Badge
    "badge_err_ok_fg": "#34d399", # Mint Green
    "badge_err_bad_bg": "#330d17",
    "badge_err_bad_fg": "#f87171",
    "badge_lines_bg": "#191426",
    "badge_lines_fg": "#a78bfa",
    "syntax_keyword": "#a78bfa",  # Soft Pastel Violet
    "syntax_comment": "#5e5473",  # Dusty Dark Lavender-Gray Italic
    "syntax_number": "#fbbf24",   # Gentle Amber Gold
    "syntax_assign": "#e879f9",   # Soft Orchid Magenta
    "syntax_symbol": "#818cf8",   # Soft Periwinkle
    "syntax_error": "#f87171",    # Soft Pastel Red
    "token_glow_bg": "#4c1d95",   # Deep Violet Glow
    "token_glow_fg": "#f3e8ff",
}


class ModernEditor(ttk.Frame):
    """
    Code Editor with:
    1. Synchronized line numbers gutter.
    2. Real-time syntax highlighting for the TINY programming language.
    3. Transient deep-violet glow highlight for selected tokens.
    """

    def __init__(self, parent, theme: dict, on_cursor_move=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.theme = theme
        self.on_cursor_move = on_cursor_move

        # Gutter line numbers
        self.gutter = tk.Text(
            self,
            width=4,
            padx=6,
            pady=6,
            takefocus=0,
            border=0,
            background=self.theme["gutter_bg"],
            foreground=self.theme["gutter_fg"],
            state="disabled",
            wrap="none",
            font=("Consolas", 11),
        )
        self.gutter.pack(side=tk.LEFT, fill=tk.Y)

        # Code text widget
        self.text = tk.Text(
            self,
            wrap="none",
            undo=True,
            font=("Consolas", 11),
            padx=8,
            pady=6,
            border=0,
            background=self.theme["editor_bg"],
            foreground=self.theme["editor_fg"],
            insertbackground=self.theme["cursor"],
            selectbackground=self.theme["select_bg"],
        )
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Vertical Scrollbar
        self.vsb = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self._on_vsb)
        self.vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.text.configure(yscrollcommand=self._on_text_scroll)

        # Configure syntax tags
        self._setup_syntax_tags()

        # Bind events
        self.text.bind("<KeyRelease>", self._on_user_action)
        self.text.bind("<MouseWheel>", self._on_user_action)
        self.text.bind("<ButtonRelease-1>", self._on_user_action)
        self.text.bind("<<Modified>>", self._on_modified)

        self.update_line_numbers()

    def _setup_syntax_tags(self):
        self.text.tag_configure(
            "syntax_keyword",
            foreground=self.theme["syntax_keyword"],
            font=("Consolas", 11, "bold"),
        )
        self.text.tag_configure(
            "syntax_comment",
            foreground=self.theme["syntax_comment"],
            font=("Consolas", 11, "italic"),
        )
        self.text.tag_configure(
            "syntax_number",
            foreground=self.theme["syntax_number"],
            font=("Consolas", 11),
        )
        self.text.tag_configure(
            "syntax_assign",
            foreground=self.theme["syntax_assign"],
            font=("Consolas", 11, "bold"),
        )
        self.text.tag_configure(
            "syntax_symbol",
            foreground=self.theme["syntax_symbol"],
            font=("Consolas", 11),
        )
        self.text.tag_configure(
            "syntax_error",
            foreground=self.theme["syntax_error"],
            font=("Consolas", 11, "bold", "underline"),
        )
        self.text.tag_configure(
            "token_glow",
            background=self.theme["token_glow_bg"],
            foreground=self.theme["token_glow_fg"],
            font=("Consolas", 11, "bold"),
        )

    def _on_vsb(self, *args):
        self.text.yview(*args)
        self.gutter.yview(*args)

    def _on_text_scroll(self, *args):
        self.vsb.set(*args)
        self.gutter.yview_moveto(args[0])

    def _on_modified(self, event=None):
        if self.text.edit_modified():
            self.update_line_numbers()
            self.highlight_syntax()
            self.text.edit_modified(False)

    def _on_user_action(self, event=None):
        self.update_line_numbers()
        self.highlight_syntax()
        if self.on_cursor_move:
            pos = self.text.index(tk.INSERT)
            row, col = pos.split(".")
            self.on_cursor_move(int(row), int(col) + 1)

    def update_line_numbers(self):
        line_count = int(self.text.index("end-1c").split(".")[0])
        lines_text = "\n".join(str(i) for i in range(1, line_count + 1))

        self.gutter.config(state="normal")
        self.gutter.delete("1.0", tk.END)
        self.gutter.insert("1.0", lines_text)
        self.gutter.config(state="disabled")
        self.gutter.yview_moveto(self.text.yview()[0])

    def highlight_syntax(self):
        """Applies real-time regex-based syntax coloring for TINY."""
        content = self.get_text()

        # Remove existing syntax tags
        for tag in ("syntax_keyword", "syntax_comment", "syntax_number", "syntax_assign", "syntax_symbol", "syntax_error"):
            self.text.tag_remove(tag, "1.0", tk.END)

        if not content:
            return

        # 1. Comments { ... } (including multiline)
        for m in re.finditer(r"\{[^}]*\}", content, flags=re.DOTALL):
            start = f"1.0+{m.start()}c"
            end = f"1.0+{m.end()}c"
            self.text.tag_add("syntax_comment", start, end)

        # 2. Unterminated comments (flag in error red)
        for m in re.finditer(r"\{[^}]*$", content, flags=re.DOTALL):
            if "}" not in m.group(0):
                start = f"1.0+{m.start()}c"
                end = f"1.0+{m.end()}c"
                self.text.tag_add("syntax_error", start, end)

        # 3. Keywords
        for m in re.finditer(r"\b(if|then|end|repeat|until|read|write)\b", content, flags=re.IGNORECASE):
            start = f"1.0+{m.start()}c"
            end = f"1.0+{m.end()}c"
            if "syntax_comment" not in self.text.tag_names(start):
                self.text.tag_add("syntax_keyword", start, end)

        # 4. Numbers
        for m in re.finditer(r"\b\d+\b", content):
            start = f"1.0+{m.start()}c"
            end = f"1.0+{m.end()}c"
            if "syntax_comment" not in self.text.tag_names(start):
                self.text.tag_add("syntax_number", start, end)

        # 5. Assignment operator ':='
        for m in re.finditer(r":=", content):
            start = f"1.0+{m.start()}c"
            end = f"1.0+{m.end()}c"
            if "syntax_comment" not in self.text.tag_names(start):
                self.text.tag_add("syntax_assign", start, end)

        # 6. Single character symbols
        for m in re.finditer(r"[;<=+\-*/()]", content):
            start = f"1.0+{m.start()}c"
            end = f"1.0+{m.end()}c"
            if "syntax_comment" not in self.text.tag_names(start):
                self.text.tag_add("syntax_symbol", start, end)

    def highlight_token_at(self, line: int, col: int, length: int):
        """Highlights a specific token location with a deep violet glow."""
        self.text.tag_remove("token_glow", "1.0", tk.END)
        start_idx = f"{line}.{col - 1}"
        end_idx = f"{line}.{col - 1 + length}"
        self.text.tag_add("token_glow", start_idx, end_idx)
        self.text.mark_set(tk.INSERT, start_idx)
        self.text.see(start_idx)

    def get_text(self) -> str:
        return self.text.get("1.0", "end-1c")

    def set_text(self, content: str):
        self.text.delete("1.0", tk.END)
        self.text.insert("1.0", content)
        self.update_line_numbers()
        self.highlight_syntax()

    def clear(self):
        self.text.delete("1.0", tk.END)
        self.update_line_numbers()
        self.highlight_syntax()


class TinyScannerApp:
    """
    Main Tkinter Desktop Application for the TINY Scanner Project.
    Styled with a dedicated eye-friendly "Purple x Black" Dark Theme.
    """

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("TINY Language Lexical Analyzer (Scanner)")
        self.root.geometry("1100x720")
        self.root.minsize(900, 540)

        # Theme reference
        self.theme = THEME
        self.current_tokens: List[Token] = []
        self.current_file_path: Optional[str] = None
        self.active_category_filter = "All"
        self.search_filter_query = ""

        # Setup ttk styles
        self._setup_ttk_styles()

        # UI Construction
        self._build_header()
        self._build_toolbar()
        self._build_main_pane()
        self._build_status_bar()

        # Keyboard shortcuts
        self._bind_shortcuts()

        # Initial table population
        self._refresh_token_table()

        # Load Factorial Sample by default for immediate gratification
        self.load_sample_by_name("Factorial Sample")

    def _setup_ttk_styles(self):
        t = self.theme
        self.root.configure(bg=t["bg"])

        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        # Treeview styling
        style.configure(
            "Treeview",
            font=("Segoe UI", 9),
            rowheight=26,
            background=t["tree_bg"],
            foreground=t["tree_fg"],
            fieldbackground=t["tree_bg"],
            borderwidth=0,
        )
        style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 9, "bold"),
            background=t["tree_header_bg"],
            foreground=t["tree_header_fg"],
            relief=tk.FLAT,
        )
        style.map("Treeview.Heading", background=[("active", t["border"])])
        style.map(
            "Treeview",
            background=[("selected", t["tree_select_bg"])],
            foreground=[("selected", t["tree_select_fg"])],
        )

    def _build_header(self):
        self.header_frame = tk.Frame(self.root, bg=self.theme["header_bg"], padx=18, pady=12)
        self.header_frame.pack(side=tk.TOP, fill=tk.X)

        # Left brand container
        left_brand = tk.Frame(self.header_frame, bg=self.theme["header_bg"])
        left_brand.pack(side=tk.LEFT)

        self.title_lbl = tk.Label(
            left_brand,
            text="TINY Language Scanner",
            font=("Segoe UI", 16, "bold"),
            bg=self.theme["header_bg"],
            fg=self.theme["header_fg"],
        )
        self.title_lbl.pack(side=tk.LEFT)

        self.badge_version = tk.Label(
            left_brand,
            text="v1.0 • Compiler Project",
            font=("Segoe UI", 8, "bold"),
            bg="#4c1d95",
            fg="#ddd6fe",
            padx=7,
            pady=2,
        )
        self.badge_version.pack(side=tk.LEFT, padx=10)

        # Right control container (Stat Badges only)
        right_controls = tk.Frame(self.header_frame, bg=self.theme["header_bg"])
        right_controls.pack(side=tk.RIGHT)

        # Stat Chips Container
        self.stats_container = tk.Frame(right_controls, bg=self.theme["header_bg"])
        self.stats_container.pack(side=tk.RIGHT)

        # Token Badge Chip
        self.chip_tokens = tk.Label(
            self.stats_container,
            text="0 Tokens",
            font=("Segoe UI", 9, "bold"),
            bg=self.theme["badge_tokens_bg"],
            fg=self.theme["badge_tokens_fg"],
            padx=10,
            pady=3,
        )
        self.chip_tokens.pack(side=tk.LEFT, padx=4)

        # Error Badge Chip
        self.chip_errors = tk.Label(
            self.stats_container,
            text="0 Errors",
            font=("Segoe UI", 9, "bold"),
            bg=self.theme["badge_err_ok_bg"],
            fg=self.theme["badge_err_ok_fg"],
            padx=10,
            pady=3,
        )
        self.chip_errors.pack(side=tk.LEFT, padx=4)

        # Lines Badge Chip
        self.chip_lines = tk.Label(
            self.stats_container,
            text="1 Lines",
            font=("Segoe UI", 9, "bold"),
            bg=self.theme["badge_lines_bg"],
            fg=self.theme["badge_lines_fg"],
            padx=10,
            pady=3,
        )
        self.chip_lines.pack(side=tk.LEFT, padx=4)

    def _build_toolbar(self):
        self.toolbar = tk.Frame(self.root, bg=self.theme["panel_bg"], padx=14, pady=8)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        # Primary Scan Button (Royal Purple)
        self.btn_scan = tk.Button(
            self.toolbar,
            text="⚡ Scan Code",
            font=("Segoe UI", 10, "bold"),
            bg=self.theme["primary_accent"],
            fg="#ffffff",
            activebackground=self.theme["primary_accent_hover"],
            activeforeground="#ffffff",
            relief=tk.FLAT,
            padx=14,
            pady=5,
            cursor="hand2",
            command=self.scan_code,
        )
        self.btn_scan.pack(side=tk.LEFT, padx=(0, 8))

        # Secondary Button Helper
        def make_sec_btn(text: str, command):
            return tk.Button(
                self.toolbar,
                text=text,
                font=("Segoe UI", 9),
                bg=self.theme["btn_sec_bg"],
                fg=self.theme["btn_sec_fg"],
                activebackground=self.theme["btn_sec_hover"],
                activeforeground="#ffffff",
                relief=tk.FLAT,
                padx=10,
                pady=5,
                cursor="hand2",
                command=command,
            )

        self.btn_open = make_sec_btn("📂 Open File", self.open_file)
        self.btn_open.pack(side=tk.LEFT, padx=4)

        self.btn_save = make_sec_btn("💾 Save Output", self.save_output)
        self.btn_save.pack(side=tk.LEFT, padx=4)

        self.btn_clear = make_sec_btn("🧹 Clear", self.clear_all)
        self.btn_clear.pack(side=tk.LEFT, padx=4)

        # Vertical Divider
        self.div1 = tk.Frame(self.toolbar, width=1, height=22, bg=self.theme["border"])
        self.div1.pack(side=tk.LEFT, padx=12)

        # Quick Sample Loader
        self.lbl_sample = tk.Label(
            self.toolbar,
            text="Sample:",
            font=("Segoe UI", 9),
            bg=self.theme["panel_bg"],
            fg=self.theme["fg_sub"],
        )
        self.lbl_sample.pack(side=tk.LEFT, padx=(0, 6))

        self.sample_combo = ttk.Combobox(
            self.toolbar,
            state="readonly",
            values=["Factorial Sample", "Full Specification Test"],
            width=22,
            font=("Segoe UI", 9),
        )
        self.sample_combo.current(0)
        self.sample_combo.pack(side=tk.LEFT, padx=4)

        self.btn_load_sample = make_sec_btn("Load", self.load_selected_sample)
        self.btn_load_sample.pack(side=tk.LEFT, padx=4)

    def _build_main_pane(self):
        # Container frame
        self.pane_container = tk.Frame(self.root, bg=self.theme["bg"], padx=14, pady=10)
        self.pane_container.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.paned = ttk.PanedWindow(self.pane_container, orient=tk.HORIZONTAL)
        self.paned.pack(fill=tk.BOTH, expand=True)

        # ----------------- LEFT PANE: SOURCE CODE EDITOR -----------------
        self.left_card = tk.Frame(self.paned, bg=self.theme["panel_bg"], padx=2, pady=2)
        self.paned.add(self.left_card, weight=5)

        # Editor Header
        self.editor_header = tk.Frame(self.left_card, bg=self.theme["panel_bg"], padx=10, pady=6)
        self.editor_header.pack(side=tk.TOP, fill=tk.X)

        self.editor_title = tk.Label(
            self.editor_header,
            text="📄 SOURCE CODE (TINY)",
            font=("Segoe UI", 10, "bold"),
            bg=self.theme["panel_bg"],
            fg=self.theme["fg"],
        )
        self.editor_title.pack(side=tk.LEFT)

        self.editor_file_badge = tk.Label(
            self.editor_header,
            text="sample_factorial.tiny",
            font=("Segoe UI", 8),
            bg=self.theme["border"],
            fg=self.theme["header_sub"],
            padx=8,
            pady=2,
        )
        self.editor_file_badge.pack(side=tk.RIGHT)

        # Main Code Editor
        self.editor = ModernEditor(
            self.left_card,
            theme=self.theme,
            on_cursor_move=self._on_editor_cursor_move,
        )
        self.editor.pack(fill=tk.BOTH, expand=True)

        # ----------------- RIGHT PANE: TOKENS EXPLORER -----------------
        self.right_card = tk.Frame(self.paned, bg=self.theme["panel_bg"], padx=2, pady=2)
        self.paned.add(self.right_card, weight=6)

        # Right Header (Title + Search Filter)
        self.table_header = tk.Frame(self.right_card, bg=self.theme["panel_bg"], padx=10, pady=6)
        self.table_header.pack(side=tk.TOP, fill=tk.X)

        self.table_title = tk.Label(
            self.table_header,
            text="🔍 SCANNED TOKENS",
            font=("Segoe UI", 10, "bold"),
            bg=self.theme["panel_bg"],
            fg=self.theme["fg"],
        )
        self.table_title.pack(side=tk.LEFT)

        # Search Box
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self._on_filter_changed())

        self.search_box = tk.Entry(
            self.table_header,
            textvariable=self.search_var,
            font=("Segoe UI", 9),
            bg=self.theme["editor_bg"],
            fg=self.theme["editor_fg"],
            insertbackground=self.theme["cursor"],
            relief=tk.FLAT,
            width=20,
        )
        self.search_box.pack(side=tk.RIGHT, padx=4)

        self.lbl_search_icon = tk.Label(
            self.table_header,
            text="Filter:",
            font=("Segoe UI", 9),
            bg=self.theme["panel_bg"],
            fg=self.theme["fg_sub"],
        )
        self.lbl_search_icon.pack(side=tk.RIGHT)

        # Filter Category Chips Bar
        self.category_bar = tk.Frame(self.right_card, bg=self.theme["panel_bg"], padx=10, pady=4)
        self.category_bar.pack(side=tk.TOP, fill=tk.X)

        self.filter_buttons = {}
        for cat in ["All", "Keywords", "Identifiers", "Numbers", "Symbols", "Errors"]:
            btn = tk.Button(
                self.category_bar,
                text=cat,
                font=("Segoe UI", 8, "bold" if cat == "All" else "normal"),
                bg=self.theme["primary_accent"] if cat == "All" else self.theme["btn_sec_bg"],
                fg="#ffffff" if cat == "All" else self.theme["fg_sub"],
                activebackground=self.theme["primary_accent_hover"],
                activeforeground="#ffffff",
                relief=tk.FLAT,
                padx=8,
                pady=2,
                cursor="hand2",
                command=lambda c=cat: self._set_category_filter(c),
            )
            btn.pack(side=tk.LEFT, padx=2)
            self.filter_buttons[cat] = btn

        # Treeview Table
        columns = ("index", "value", "type", "category", "line", "col")
        self.tree = ttk.Treeview(
            self.right_card,
            columns=columns,
            show="headings",
            selectmode="browse",
        )

        self.tree.heading("index", text="#")
        self.tree.heading("value", text="Token Value (Lexeme)")
        self.tree.heading("type", text="Token Type")
        self.tree.heading("category", text="Category")
        self.tree.heading("line", text="Line")
        self.tree.heading("col", text="Col")

        self.tree.column("index", width=40, minwidth=35, anchor=tk.CENTER)
        self.tree.column("value", width=140, minwidth=90, anchor=tk.W)
        self.tree.column("type", width=120, minwidth=90, anchor=tk.W)
        self.tree.column("category", width=95, minwidth=80, anchor=tk.CENTER)
        self.tree.column("line", width=50, minwidth=40, anchor=tk.CENTER)
        self.tree.column("col", width=50, minwidth=40, anchor=tk.CENTER)

        tree_vsb = ttk.Scrollbar(self.right_card, orient=tk.VERTICAL, command=self.tree.yview)
        tree_hsb = ttk.Scrollbar(self.right_card, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=tree_vsb.set, xscrollcommand=tree_hsb.set)

        self.tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=4, pady=4)
        tree_vsb.pack(side=tk.RIGHT, fill=tk.Y)
        tree_hsb.pack(side=tk.BOTTOM, fill=tk.X)

        # Bind token click to editor navigation
        self.tree.bind("<<TreeviewSelect>>", self._on_token_selected)

    def _build_status_bar(self):
        self.status_bar = tk.Frame(self.root, bg=self.theme["header_bg"], padx=14, pady=6)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.status_msg = tk.Label(
            self.status_bar,
            text="⚡ Ready. Load code or hit 'Scan Code' to analyze.",
            font=("Segoe UI", 9),
            bg=self.theme["header_bg"],
            fg=self.theme["fg_sub"],
            anchor=tk.W,
        )
        self.status_msg.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.cursor_pos_lbl = tk.Label(
            self.status_bar,
            text="Ln 1, Col 1",
            font=("Segoe UI", 9),
            bg=self.theme["header_bg"],
            fg=self.theme["fg_sub"],
            anchor=tk.E,
        )
        self.cursor_pos_lbl.pack(side=tk.RIGHT)

    def _bind_shortcuts(self):
        self.root.bind("<Control-o>", lambda e: self.open_file())
        self.root.bind("<Control-s>", lambda e: self.save_output())
        self.root.bind("<F5>", lambda e: self.scan_code())
        self.root.bind("<Control-Return>", lambda e: self.scan_code())
        self.root.bind("<Control-n>", lambda e: self.clear_all())

    def _classify_token_category(self, token: Token) -> str:
        """Categorizes token for badge tags and quick filtering."""
        if token.type == TokenType.ERROR:
            return "Errors"
        if token.type in (TokenType.IF, TokenType.THEN, TokenType.END, TokenType.REPEAT, TokenType.UNTIL, TokenType.READ, TokenType.WRITE):
            return "Keywords"
        if token.type == TokenType.IDENTIFIER:
            return "Identifiers"
        if token.type == TokenType.NUMBER:
            return "Numbers"
        return "Symbols"

    def _set_category_filter(self, category: str):
        self.active_category_filter = category
        for cat, btn in self.filter_buttons.items():
            if cat == category:
                btn.config(bg=self.theme["primary_accent"], fg="#ffffff", font=("Segoe UI", 8, "bold"))
            else:
                btn.config(bg=self.theme["btn_sec_bg"], fg=self.theme["fg_sub"], font=("Segoe UI", 8, "normal"))
        self._refresh_token_table()

    def _on_filter_changed(self):
        self.search_filter_query = self.search_var.get().strip().lower()
        self._refresh_token_table()

    def _refresh_token_table(self):
        """Rebuilds treeview rows matching active filters."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Configure tags
        self.tree.tag_configure("evenrow", background=self.theme["tree_row_even"], foreground=self.theme["tree_fg"])
        self.tree.tag_configure("oddrow", background=self.theme["tree_row_odd"], foreground=self.theme["tree_fg"])
        self.tree.tag_configure(
            "errortoken",
            background=self.theme["error_bg"],
            foreground=self.theme["error_fg"],
            font=("Segoe UI", 9, "bold"),
        )

        visible_count = 0
        for i, token in enumerate(self.current_tokens, start=1):
            category = self._classify_token_category(token)

            # Apply category filter
            if self.active_category_filter != "All" and category != self.active_category_filter:
                continue

            # Apply search filter
            if self.search_filter_query:
                query = self.search_filter_query
                match = (
                    query in token.value.lower()
                    or query in token.display_type.lower()
                    or query in token.type.name.lower()
                    or query in category.lower()
                    or query in str(token.line)
                )
                if not match:
                    continue

            visible_count += 1
            is_err = token.type == TokenType.ERROR
            tag = "errortoken" if is_err else ("evenrow" if visible_count % 2 == 0 else "oddrow")

            display_category = "⚠️ ERROR" if is_err else category[:-1] if category.endswith("s") else category
            self.tree.insert(
                "",
                tk.END,
                values=(i, token.value, token.display_type, display_category, token.line, token.column),
                tags=(tag,),
            )

    def _on_editor_cursor_move(self, row: int, col: int):
        self.cursor_pos_lbl.config(text=f"Ln {row}, Col {col}")

    def scan_code(self):
        """Runs the scanner on editor text and updates statistics and table."""
        source_code = self.editor.get_text()

        if not source_code.strip():
            self.current_tokens = []
            self._update_stat_chips(0, 0, 1)
            self._refresh_token_table()
            self.set_status("⚠️ Editor is empty. Enter or load TINY code to scan.")
            return

        try:
            scanner = Scanner(source_code)
            self.current_tokens = scanner.scan_all()
        except Exception as ex:
            messagebox.showerror("Scanner Error", f"Unexpected error during scanning:\n{ex}")
            self.set_status(f"Scanning failed: {ex}", is_error=True)
            return

        error_count = sum(1 for t in self.current_tokens if t.type == TokenType.ERROR)
        line_count = int(self.editor.text.index("end-1c").split(".")[0])
        token_count = len(self.current_tokens)

        self._update_stat_chips(token_count, error_count, line_count)
        self._refresh_token_table()

        if error_count > 0:
            self.set_status(
                f"⚠️ Completed with {error_count} lexical ERROR(s) flagged in red.",
                is_error=True,
            )
        else:
            self.set_status(
                f"✓ Scan successful! Recognized {token_count} valid tokens."
            )

    def _update_stat_chips(self, token_count: int, error_count: int, line_count: int):
        t = self.theme
        self.chip_tokens.config(
            text=f"{token_count} Tokens",
            bg=t["badge_tokens_bg"],
            fg=t["badge_tokens_fg"],
        )
        self.chip_lines.config(
            text=f"{line_count} Lines",
            bg=t["badge_lines_bg"],
            fg=t["badge_lines_fg"],
        )

        if error_count == 0:
            self.chip_errors.config(
                text="0 Errors",
                bg=t["badge_err_ok_bg"],
                fg=t["badge_err_ok_fg"],
            )
        else:
            self.chip_errors.config(
                text=f"{error_count} Errors",
                bg=t["badge_err_bad_bg"],
                fg=t["badge_err_bad_fg"],
            )

    def set_status(self, message: str, is_error: bool = False):
        color = "#f87171" if is_error else self.theme["fg_sub"]
        self.status_msg.config(text=message, fg=color)

    def open_file(self):
        """Loads a TINY file into the editor."""
        file_path = filedialog.askopenfilename(
            title="Open TINY Source File",
            filetypes=[
                ("TINY Source Files", "*.tiny;*.txt"),
                ("TINY Files (*.tiny)", "*.tiny"),
                ("Text Files (*.txt)", "*.txt"),
                ("All Files (*.*)", "*.*"),
            ],
        )
        if not file_path:
            return

        try:
            content = read_source_file(file_path)
            self.editor.set_text(content)
            self.current_file_path = file_path
            name = Path(file_path).name
            self.editor_file_badge.config(text=name)
            self.set_status(f"✓ Loaded: '{name}'")
            self.scan_code()
        except Exception as ex:
            messagebox.showerror("Error Opening File", f"Could not open file:\n{ex}")
            self.set_status(f"Error reading file: {ex}", is_error=True)

    def save_output(self):
        """Saves scanned tokens to file in project spec format."""
        if not self.current_tokens:
            messagebox.showwarning(
                "No Tokens",
                "Please scan some TINY code first before exporting token output.",
            )
            return

        initial_name = "tokens_output.txt"
        if self.current_file_path:
            initial_name = Path(self.current_file_path).stem + "_tokens.txt"

        output_path = filedialog.asksaveasfilename(
            title="Save Scanned Tokens",
            initialfile=initial_name,
            defaultextension=".txt",
            filetypes=[
                ("Text Files (*.txt)", "*.txt"),
                ("All Files (*.*)", "*.*"),
            ],
        )
        if not output_path:
            return

        try:
            write_token_file(self.current_tokens, output_path, use_spec_casing=True)
            saved_name = Path(output_path).name
            self.set_status(f"✓ Saved {len(self.current_tokens)} tokens to '{saved_name}'.")
            messagebox.showinfo(
                "Export Complete",
                f"Successfully saved {len(self.current_tokens)} tokens to:\n{output_path}",
            )
        except Exception as ex:
            messagebox.showerror("Error Saving", f"Could not write file:\n{ex}")
            self.set_status(f"Error saving file: {ex}", is_error=True)

    def clear_all(self):
        """Resets editor and token table."""
        self.editor.clear()
        self.current_tokens = []
        self.current_file_path = None
        self.editor_file_badge.config(text="Untitled")
        self._update_stat_chips(0, 0, 1)
        self._refresh_token_table()
        self.set_status("Cleared editor and token explorer.")

    def load_selected_sample(self):
        selection = self.sample_combo.get()
        self.load_sample_by_name(selection)

    def load_sample_by_name(self, name: str):
        samples_dir = Path(__file__).resolve().parent.parent.parent / "samples"
        if "Factorial" in name:
            target = samples_dir / "sample_factorial.tiny"
        else:
            target = samples_dir / "sample_test.tiny"

        if not target.exists():
            return

        try:
            content = read_source_file(target)
            self.editor.set_text(content)
            self.current_file_path = str(target)
            self.editor_file_badge.config(text=target.name)
            self.scan_code()
        except Exception:
            pass

    def _on_token_selected(self, event):
        """Highlights the selected token in the editor with a visual glow."""
        selection = self.tree.selection()
        if not selection:
            return
        values = self.tree.item(selection[0], "values")
        if len(values) >= 6:
            try:
                lexeme = str(values[1])
                line = int(values[4])
                col = int(values[5])
                self.editor.highlight_token_at(line, col, len(lexeme))
            except (ValueError, IndexError):
                pass


def launch_gui():
    root = tk.Tk()
    app = TinyScannerApp(root)
    root.mainloop()


if __name__ == "__main__":
    launch_gui()
