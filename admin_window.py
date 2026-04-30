"""
admin_window.py — Admin Login Window
Allows the admin to login and access the Results panel with reset capability.
Concepts used: Tkinter, OOP, Functions, Database verification
"""

import tkinter as tk
from tkinter import messagebox
import database as db
from styles import COLORS, FONTS, PAD, SIZES


class AdminLoginWindow:
    """
    A dialog window for admin authentication.
    Default credentials: username='admin', password='admin123'
    """

    def __init__(self, root, parent_root):
        self.root = root
        self.parent_root = parent_root  # Reference to login window

        self.root.title("Admin Login")
        self.root.geometry(SIZES["admin"])
        self.root.configure(bg=COLORS["bg_dark"])
        self.root.resizable(False, False)

        self._center_window(420, 300)
        self._build_ui()

    def _center_window(self, w, h):
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def _build_ui(self):
        tk.Frame(self.root, bg=COLORS["accent_red"], height=4).pack(fill="x")

        card = tk.Frame(self.root, bg=COLORS["bg_card"], padx=30, pady=24)
        card.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(
            card,
            text="🔐  ADMIN LOGIN",
            font=FONTS["heading"],
            bg=COLORS["bg_card"],
            fg=COLORS["accent_red"]
        ).pack(pady=(0, 16))

        # ── Username ───────────────────────────────────────────────────────────
        tk.Label(card, text="Username", font=FONTS["label"],
                 bg=COLORS["bg_card"], fg=COLORS["text_muted"]).pack(anchor="w")

        self.username_var = tk.StringVar()
        tk.Entry(
            card,
            textvariable=self.username_var,
            font=FONTS["body"],
            bg=COLORS["bg_input"],
            fg=COLORS["text_primary"],
            insertbackground=COLORS["accent"],
            relief="flat",
        ).pack(fill="x", ipady=6, ipadx=8, pady=(2, 12))

        # ── Password ───────────────────────────────────────────────────────────
        tk.Label(card, text="Password", font=FONTS["label"],
                 bg=COLORS["bg_card"], fg=COLORS["text_muted"]).pack(anchor="w")

        self.password_var = tk.StringVar()
        self.pwd_entry = tk.Entry(
            card,
            textvariable=self.password_var,
            show="•",    # Masks password
            font=FONTS["body"],
            bg=COLORS["bg_input"],
            fg=COLORS["text_primary"],
            insertbackground=COLORS["accent"],
            relief="flat",
        )
        self.pwd_entry.pack(fill="x", ipady=6, ipadx=8, pady=(2, 6))
        self.pwd_entry.bind("<Return>", lambda e: self._attempt_admin_login())

        # ── Hint ──────────────────────────────────────────────────────────────
        tk.Label(
            card,
            text="Demo: admin / admin123",
            font=FONTS["small"],
            bg=COLORS["bg_card"],
            fg=COLORS["text_muted"]
        ).pack(anchor="w", pady=(0, 12))

        # ── Login Button ──────────────────────────────────────────────────────
        tk.Button(
            card,
            text="LOGIN AS ADMIN",
            font=FONTS["button"],
            bg=COLORS["accent_red"],
            fg=COLORS["white"],
            activebackground="#C0392B",
            activeforeground=COLORS["white"],
            relief="flat",
            cursor="hand2",
            command=self._attempt_admin_login,
            pady=8,
        ).pack(fill="x")

    def _attempt_admin_login(self):
        """Validates admin credentials and opens the admin results panel."""
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()

        if db.verify_admin(username, password):
            # Credentials valid — open results with admin privileges
            self.root.destroy()

            from results_window import ResultsWindow
            results_win = tk.Toplevel(self.parent_root)
            ResultsWindow(results_win, is_admin=True)
        else:
            messagebox.showerror(
                "Login Failed",
                "Invalid username or password.\nPlease try again."
            )
            self.password_var.set("")
