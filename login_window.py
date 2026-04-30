"""
login_window.py — Voter Registration & Login Screen
2-step process:
  Step 1: Enter Name + Roll Number
  Step 2: Enter Age + Gender
Then proceeds to voting screen.
Concepts used: Tkinter, OOP, Functions, If-Else, Database handling
"""

import tkinter as tk
from tkinter import messagebox
import database as db
from styles import COLORS, FONTS, PAD, SIZES


class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.deiconify()
        self.root.title("E-Voting System — Voter Login")
        self.root.configure(bg=COLORS["bg_dark"])
        self.root.resizable(True, True)
        self._center_window(500, 700)
        self._build_ui()

    def _center_window(self, w, h):
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def _build_ui(self):
        tk.Frame(self.root, bg=COLORS["accent"], height=6).pack(fill="x")

        # Scrollable canvas setup
        canvas = tk.Canvas(self.root, bg=COLORS["bg_dark"], highlightthickness=0)
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        card = tk.Frame(canvas, bg=COLORS["bg_card"], padx=30, pady=20)
        canvas.create_window((12, 12), window=card, anchor="nw", width=460)
        card.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(-1*(e.delta//120), "units"))
        # Logo
        tk.Label(card, text="🗳️", font=("Segoe UI Emoji", 32),
                 bg=COLORS["bg_card"], fg=COLORS["accent"]).pack(pady=(0, 4))

        # Title
        tk.Label(card, text="E-VOTING SYSTEM", font=FONTS["title"],
                 bg=COLORS["bg_card"], fg=COLORS["accent"]).pack()

        tk.Label(card, text="Secure Digital Elections Platform", font=FONTS["subtitle"],
                 bg=COLORS["bg_card"], fg=COLORS["text_muted"]).pack(pady=(2, 12))

        tk.Frame(card, bg=COLORS["border"], height=1).pack(fill="x", pady=(0, 12))

        # STEP 1
        tk.Label(card, text="STEP 1 — VOTER IDENTITY", font=FONTS["small"],
                 bg=COLORS["bg_card"], fg=COLORS["text_muted"]).pack(anchor="w", pady=(0, 8))

        tk.Label(card, text="Full Name", font=FONTS["label"],
                 bg=COLORS["bg_card"], fg=COLORS["text_primary"]).pack(anchor="w")
        self.name_var = tk.StringVar()
        self._make_entry(card, self.name_var).pack(fill="x", pady=(2, 10))

        tk.Label(card, text="Roll Number", font=FONTS["label"],
                 bg=COLORS["bg_card"], fg=COLORS["text_primary"]).pack(anchor="w")
        self.roll_var = tk.StringVar()
        self._make_entry(card, self.roll_var, font=FONTS["voter_id"]).pack(fill="x", pady=(2, 12))

        tk.Frame(card, bg=COLORS["border"], height=1).pack(fill="x", pady=(0, 12))

        # STEP 2
        tk.Label(card, text="STEP 2 — PERSONAL DETAILS", font=FONTS["small"],
                 bg=COLORS["bg_card"], fg=COLORS["text_muted"]).pack(anchor="w", pady=(0, 8))

        tk.Label(card, text="Age  (must be 18 or above)", font=FONTS["label"],
                 bg=COLORS["bg_card"], fg=COLORS["text_primary"]).pack(anchor="w")
        self.age_var = tk.StringVar()
        self._make_entry(card, self.age_var).pack(fill="x", pady=(2, 10))

        tk.Label(card, text="Gender", font=FONTS["label"],
                 bg=COLORS["bg_card"], fg=COLORS["text_primary"]).pack(anchor="w")

        self.gender_var = tk.StringVar(value="Male")
        gender_frame = tk.Frame(card, bg=COLORS["bg_card"])
        gender_frame.pack(fill="x", pady=(4, 12))

        for option in ["Male", "Female", "Other"]:
            tk.Radiobutton(
                gender_frame, text=option, variable=self.gender_var, value=option,
                font=FONTS["body"], bg=COLORS["bg_card"], fg=COLORS["text_primary"],
                selectcolor=COLORS["accent"], activebackground=COLORS["bg_card"], cursor="hand2",
            ).pack(side="left", padx=(0, 16))

        # Error label
        self.error_var = tk.StringVar()
        tk.Label(card, textvariable=self.error_var, font=FONTS["small"],
                 bg=COLORS["bg_card"], fg=COLORS["accent_red"],
                 wraplength=400, justify="left").pack(anchor="w", pady=(0, 8))

        # Login button
        self.login_btn = tk.Button(
            card, text="PROCEED TO VOTE  →", font=FONTS["button"],
            bg=COLORS["accent"], fg=COLORS["text_dark"],
            activebackground=COLORS["accent_hover"], activeforeground=COLORS["text_dark"],
            relief="flat", cursor="hand2", command=self._attempt_login, pady=10,
        )
        self.login_btn.pack(fill="x", pady=(0, 8))
        self.login_btn.bind("<Enter>", lambda e: self.login_btn.config(bg=COLORS["accent_hover"]))
        self.login_btn.bind("<Leave>", lambda e: self.login_btn.config(bg=COLORS["accent"]))

        # Results button
        tk.Button(card, text="📊  View Live Results", font=FONTS["label"],
                  bg=COLORS["bg_input"], fg=COLORS["text_muted"],
                  activebackground=COLORS["border"], activeforeground=COLORS["text_primary"],
                  relief="flat", cursor="hand2", command=self._open_results, pady=6,
                  ).pack(fill="x", pady=(0, 6))

        # Admin button
        tk.Button(card, text="🔐  Admin Panel", font=FONTS["label"],
                  bg=COLORS["bg_input"], fg=COLORS["text_muted"],
                  activebackground=COLORS["border"], activeforeground=COLORS["text_primary"],
                  relief="flat", cursor="hand2", command=self._open_admin_login, pady=6,
                  ).pack(fill="x")

    def _make_entry(self, parent, textvariable, font=None):
        frame = tk.Frame(parent, bg=COLORS["border"], padx=1, pady=1)
        tk.Entry(frame, textvariable=textvariable, font=font or FONTS["body"],
                 bg=COLORS["bg_input"], fg=COLORS["text_primary"],
                 insertbackground=COLORS["accent"], relief="flat", bd=0,
                 ).pack(fill="x", ipady=8, ipadx=10)
        return frame

    def _attempt_login(self):
        name    = self.name_var.get().strip()
        roll_no = self.roll_var.get().strip().upper()
        age_str = self.age_var.get().strip()
        gender  = self.gender_var.get()

        if not name:
            self.error_var.set("⚠  Please enter your full name.")
            return
        if not roll_no:
            self.error_var.set("⚠  Please enter your roll number.")
            return
        if not age_str:
            self.error_var.set("⚠  Please enter your age.")
            return
        if not age_str.isdigit():
            self.error_var.set("⚠  Age must be a number.")
            return

        age = int(age_str)

        if age < 18:
            self.error_var.set("✗  You must be 18 or older to vote.")
            return
        if age > 120:
            self.error_var.set("✗  Please enter a valid age.")
            return

        # Check duplicate by roll number
        existing = db.get_voter(roll_no)

        if existing:
            if existing["has_voted"] == 1:
                messagebox.showwarning(
                    "Already Voted",
                    f"Roll Number {roll_no} has already cast a vote.\nEach voter can vote only once!"
                )
                self._clear_fields()
                return
            else:
                voter = existing
        else:
            db.register_voter(roll_no, name, age, gender)
            voter = {"roll_no": roll_no, "name": name, "age": age, "gender": gender, "has_voted": 0}

        self.error_var.set("")
        self._open_voting_screen(voter)

    def _clear_fields(self):
        self.name_var.set("")
        self.roll_var.set("")
        self.age_var.set("")
        self.gender_var.set("Male")
        self.error_var.set("")

    def _open_voting_screen(self, voter):
        from voting_window import VotingWindow
        self.root.withdraw()
        vote_win = tk.Toplevel(self.root)
        VotingWindow(vote_win, voter, self.root)

    def _open_results(self):
        from results_window import ResultsWindow
        ResultsWindow(tk.Toplevel(self.root))

    def _open_admin_login(self):
        from admin_window import AdminLoginWindow
        AdminLoginWindow(tk.Toplevel(self.root), self.root)
