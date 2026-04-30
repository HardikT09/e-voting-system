"""
voting_window.py — Voting Screen
Displays candidates as styled radio buttons. Voter selects one and submits.
Concepts used: Tkinter, OOP, Radio Buttons, Functions, Database interaction
"""

import tkinter as tk
from tkinter import messagebox
import database as db
from styles import COLORS, FONTS, PAD, SIZES


class VotingWindow:
    """
    The main voting interface shown after successful login.
    Displays all candidates and lets the voter choose one.
    """

    def __init__(self, root, voter, login_root):
        """
        root       : This voting window's Tk/Toplevel widget
        voter      : dict with voter_id and name
        login_root : Reference to login window (to re-show it on close)
        """
        self.root = root
        self.voter = voter
        self.login_root = login_root

        self.root.title(f"E-Voting System — Welcome, {voter['name']}")

        self.root.geometry(SIZES["vote"])
        self.root.configure(bg=COLORS["bg_dark"])
        self.root.resizable(False, False)

        # Center window on screen
        self._center_window(600, 680)

        # Handle window close (X button)
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

        # Fetch candidates from DB
        self.candidates = db.get_all_candidates()

        # Tkinter variable to track selected candidate
        self.selected_candidate = tk.IntVar(value=-1)  # -1 = nothing selected

        self._build_ui()

    def _center_window(self, w, h):
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def _build_ui(self):
        """Builds the entire voting screen UI."""

        # ── Top Accent Bar ─────────────────────────────────────────────────────
        tk.Frame(self.root, bg=COLORS["accent"], height=6).pack(fill="x")

        # ── Scrollable Canvas for content ──────────────────────────────────────
        canvas = tk.Canvas(self.root, bg=COLORS["bg_dark"], highlightthickness=0)
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        self.scroll_frame = tk.Frame(canvas, bg=COLORS["bg_dark"])

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind mouse scroll
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(-1 * (e.delta // 120), "units"))

        # ── Voter Info Header ──────────────────────────────────────────────────
        header = tk.Frame(self.scroll_frame, bg=COLORS["bg_card"], padx=24, pady=16)
        header.pack(fill="x", padx=20, pady=(16, 8))

        tk.Label(
            header,
            text="🗳️  CAST YOUR VOTE",
            font=FONTS["title"],
            bg=COLORS["bg_card"],
            fg=COLORS["accent"]
        ).pack(anchor="w")

        tk.Label(
            header,
            text=f"Welcome, {self.voter['name']}  |  Roll No: {self.voter['roll_no']}",
            font=FONTS["body"],
            bg=COLORS["bg_card"],
            fg=COLORS["text_muted"]
        ).pack(anchor="w", pady=(4, 0))

        tk.Label(
            header,
            text="Select ONE candidate and click Submit Vote.",
            font=FONTS["body"],
            bg=COLORS["bg_card"],
            fg=COLORS["text_primary"]
        ).pack(anchor="w", pady=(6, 0))

        # ── Divider ───────────────────────────────────────────────────────────
        tk.Frame(self.scroll_frame, bg=COLORS["border"], height=1).pack(fill="x", padx=20, pady=4)

        # ── Candidates Section Label ──────────────────────────────────────────
        tk.Label(
            self.scroll_frame,
            text="CANDIDATES",
            font=FONTS["small"],
            bg=COLORS["bg_dark"],
            fg=COLORS["text_muted"]
        ).pack(anchor="w", padx=26, pady=(8, 4))

        # ── Candidate Cards (Radio Buttons) ───────────────────────────────────
        self.candidate_frames = []  # Track card frames for highlight effect

        for candidate in self.candidates:
            self._build_candidate_card(candidate)

        # ── Spacing ───────────────────────────────────────────────────────────
        tk.Frame(self.scroll_frame, bg=COLORS["bg_dark"], height=8).pack()

        # ── Error message ─────────────────────────────────────────────────────
        self.error_var = tk.StringVar()
        tk.Label(
            self.scroll_frame,
            textvariable=self.error_var,
            font=FONTS["small"],
            bg=COLORS["bg_dark"],
            fg=COLORS["accent_red"]
        ).pack(pady=(0, 4))

        # ── Submit Button ─────────────────────────────────────────────────────
        submit_frame = tk.Frame(self.scroll_frame, bg=COLORS["bg_dark"], padx=20)
        submit_frame.pack(fill="x", padx=20, pady=(0, 10))

        self.submit_btn = tk.Button(
            submit_frame,
            text="✔  SUBMIT MY VOTE",
            font=FONTS["button"],
            bg=COLORS["accent_green"],
            fg=COLORS["white"],
            activebackground="#219150",
            activeforeground=COLORS["white"],
            relief="flat",
            cursor="hand2",
            command=self._submit_vote,
            pady=12,
        )
        self.submit_btn.pack(fill="x")

        self.submit_btn.bind("<Enter>", lambda e: self.submit_btn.config(bg="#219150"))
        self.submit_btn.bind("<Leave>", lambda e: self.submit_btn.config(bg=COLORS["accent_green"]))

        # ── Back / Logout button ──────────────────────────────────────────────
        tk.Button(
            self.scroll_frame,
            text="← Logout",
            font=FONTS["small"],
            bg=COLORS["bg_dark"],
            fg=COLORS["text_muted"],
            activebackground=COLORS["bg_dark"],
            activeforeground=COLORS["text_primary"],
            relief="flat",
            cursor="hand2",
            command=self._on_close,
            pady=4,
        ).pack(pady=(0, 16))

    def _build_candidate_card(self, candidate):
        """
        Builds one candidate card with:
        - Symbol emoji
        - Name and party
        - Radio button to select
        """
        cid = candidate["candidate_id"]

        # Outer card frame
        card = tk.Frame(
            self.scroll_frame,
            bg=COLORS["bg_card"],
            padx=16,
            pady=14,
            relief="flat",
            bd=0,
        )
        card.pack(fill="x", padx=20, pady=6)

        self.candidate_frames.append((cid, card))

        # ── Left: Symbol ──────────────────────────────────────────────────────
        left = tk.Frame(card, bg=COLORS["bg_card"])
        left.pack(side="left", padx=(0, 16))

        symbol_frame = tk.Frame(left, bg=COLORS["bg_input"], padx=10, pady=10)
        symbol_frame.pack()

        tk.Label(
            symbol_frame,
            text=candidate["symbol"],
            font=("Segoe UI Emoji", 28),
            bg=COLORS["bg_input"]
        ).pack()

        # ── Middle: Info ──────────────────────────────────────────────────────
        mid = tk.Frame(card, bg=COLORS["bg_card"])
        mid.pack(side="left", fill="both", expand=True)

        tk.Label(
            mid,
            text=candidate["name"],
            font=FONTS["heading"],
            bg=COLORS["bg_card"],
            fg=COLORS["text_primary"],
            anchor="w"
        ).pack(fill="x")

        tk.Label(
            mid,
            text=candidate["party"],
            font=FONTS["body"],
            bg=COLORS["bg_card"],
            fg=COLORS["text_muted"],
            anchor="w"
        ).pack(fill="x")

        # ── Right: Radio Button ───────────────────────────────────────────────
        right = tk.Frame(card, bg=COLORS["bg_card"])
        right.pack(side="right", padx=(16, 0))

        rb = tk.Radiobutton(
            right,
            variable=self.selected_candidate,
            value=cid,
            bg=COLORS["bg_card"],
            activebackground=COLORS["bg_card"],
            selectcolor=COLORS["accent"],
            fg=COLORS["accent"],
            cursor="hand2",
            command=lambda c=cid: self._on_candidate_select(c),
        )
        rb.pack()

        # Make entire card clickable
        for widget in [card, left, mid, right, symbol_frame]:
            widget.bind("<Button-1>", lambda e, c=cid: self._select_by_click(c))

    def _select_by_click(self, candidate_id):
        """Selects a candidate when user clicks anywhere on the card."""
        self.selected_candidate.set(candidate_id)
        self._on_candidate_select(candidate_id)

    def _on_candidate_select(self, candidate_id):
        """
        Visually highlights the selected card.
        Changes border color of the selected card to accent color.
        """
        for cid, frame in self.candidate_frames:
            if cid == candidate_id:
                frame.config(bg=COLORS["bg_input"])
                # Recursively update child widget bg
                self._set_frame_bg(frame, COLORS["bg_input"])
            else:
                frame.config(bg=COLORS["bg_card"])
                self._set_frame_bg(frame, COLORS["bg_card"])

        self.error_var.set("")  # Clear error when user selects

    def _set_frame_bg(self, widget, color):
        """Recursively set background color for frame and its children."""
        try:
            widget.config(bg=color)
        except Exception:
            pass
        for child in widget.winfo_children():
            self._set_frame_bg(child, color)

    def _submit_vote(self):
        """
        Called when Submit Vote is clicked.
        Validates selection and records the vote in the database.
        """
        chosen_id = self.selected_candidate.get()

        if chosen_id == -1:
            # No candidate selected
            self.error_var.set("⚠  Please select a candidate before submitting.")
            return

        # Find candidate name for confirmation message
        chosen_name = ""
        for c in self.candidates:
            if c["candidate_id"] == chosen_id:
                chosen_name = c["name"]
                break

        # Confirm dialog
        confirm = messagebox.askyesno(
            "Confirm Your Vote",
            f"You are about to vote for:\n\n  {chosen_name}\n\nThis action CANNOT be undone.\nDo you confirm your vote?"
        )

        if not confirm:
            return  # User cancelled

        # ── Cast vote in database ──────────────────────────────────────────────
        db.cast_vote(self.voter["roll_no"], chosen_id)

        # Show success message
        messagebox.showinfo(
            "✅ Vote Cast Successfully!",
            f"Thank you, {self.voter['name']}!\n\nYour vote for {chosen_name} has been recorded.\nYour Voter ID has been marked as voted."
        )

        # Disable submit button to prevent re-voting within same session
        self.submit_btn.config(
            text="✔  Vote Recorded — Thank You!",
            state="disabled",
            bg=COLORS["text_muted"]
        )

        # Return to login after a moment
        self.root.after(1500, self._return_to_login)

    def _return_to_login(self):
        """Closes voting window and shows login screen again."""
        self.root.destroy()
        self.login_root.deiconify()

    def _on_close(self):
        """Called when user closes or logs out without voting."""
        self.root.destroy()
        self.login_root.deiconify()
