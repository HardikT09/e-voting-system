"""
results_window.py — Results & Analytics Screen
Displays vote counts, winner, and a bar-chart visualization using Tkinter Canvas.
Concepts used: Tkinter, Canvas Drawing, Loops, Database, OOP
"""

import tkinter as tk
from tkinter import ttk
import database as db
from styles import COLORS, FONTS, PAD, SIZES


class ResultsWindow:
    def __init__(self, root, is_admin=False):
        self.win = root
        self.is_admin = is_admin

        self.win.title("E-Voting System — Live Results")
        self.win.geometry(SIZES["results"])
        self.win.configure(bg=COLORS["bg_dark"])
        self.win.resizable(True, True)

        self._center_window(640, 700)
        self._build_ui()

    def _center_window(self, w, h):
        sw = self.win.winfo_screenwidth()
        sh = self.win.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.win.geometry(f"{w}x{h}+{x}+{y}")

    def _build_ui(self):
        # Top accent bar
        tk.Frame(self.win, bg=COLORS["accent_green"], height=6).pack(fill="x")

        # Scrollable canvas setup
        canvas = tk.Canvas(self.win, bg=COLORS["bg_dark"], highlightthickness=0)
        scrollbar = tk.Scrollbar(self.win, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # This is the scrollable frame — all content goes inside 'root'
        self.root = tk.Frame(canvas, bg=COLORS["bg_dark"])
        canvas.create_window((0, 0), window=self.root, anchor="nw", width=620)
        self.root.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(-1*(e.delta//120), "units"))

        # Header
        header = tk.Frame(self.root, bg=COLORS["bg_card"], padx=24, pady=16)
        header.pack(fill="x", padx=20, pady=(16, 4))

        tk.Label(header, text="📊  ELECTION RESULTS", font=FONTS["title"],
                 bg=COLORS["bg_card"], fg=COLORS["accent_green"]).pack(anchor="w")

        tk.Label(header, text="Live Vote Counts — Updated in Real Time", font=FONTS["subtitle"],
                 bg=COLORS["bg_card"], fg=COLORS["text_muted"]).pack(anchor="w", pady=(2, 0))

        # Fetch data
        results = db.get_results()
        total   = db.get_total_votes()

        # Winner banner
        if total > 0:
            winner = results[0]
            winner_frame = tk.Frame(self.root, bg="#1A3A2A", padx=20, pady=12)
            winner_frame.pack(fill="x", padx=20, pady=8)

            tk.Label(winner_frame, text=f"🏆  LEADING:  {winner['symbol']}  {winner['name']}",
                     font=FONTS["winner"], bg="#1A3A2A", fg=COLORS["accent_green"]).pack(anchor="w")

            pct = (winner["votes"] / total * 100) if total > 0 else 0
            tk.Label(winner_frame, text=f"{winner['party']}  ·  {winner['votes']} votes  ·  {pct:.1f}%",
                     font=FONTS["body"], bg="#1A3A2A", fg=COLORS["text_muted"]).pack(anchor="w", pady=(2, 0))
        else:
            no_vote_frame = tk.Frame(self.root, bg=COLORS["bg_card"], padx=20, pady=12)
            no_vote_frame.pack(fill="x", padx=20, pady=8)
            tk.Label(no_vote_frame, text="No votes have been cast yet.",
                     font=FONTS["body_bold"], bg=COLORS["bg_card"], fg=COLORS["text_muted"]).pack()

        # Bar chart
        tk.Label(self.root, text="VOTE DISTRIBUTION", font=FONTS["small"],
                 bg=COLORS["bg_dark"], fg=COLORS["text_muted"]).pack(anchor="w", padx=26, pady=(8, 2))

        chart_frame = tk.Frame(self.root, bg=COLORS["bg_card"], padx=10, pady=10)
        chart_frame.pack(fill="x", padx=20, pady=(0, 4))
        self._draw_bar_chart(chart_frame, results, total)

        # Detailed table
        tk.Label(self.root, text="DETAILED BREAKDOWN", font=FONTS["small"],
                 bg=COLORS["bg_dark"], fg=COLORS["text_muted"]).pack(anchor="w", padx=26, pady=(12, 4))

        table_frame = tk.Frame(self.root, bg=COLORS["bg_card"], padx=16, pady=10)
        table_frame.pack(fill="x", padx=20, pady=(0, 8))
        self._build_table(table_frame, results, total)

        # Total votes
        tk.Label(self.root, text=f"Total Votes Cast: {total}", font=FONTS["body_bold"],
                 bg=COLORS["bg_dark"], fg=COLORS["text_primary"]).pack(pady=4)

        # Admin Reset Button
        if self.is_admin:
            tk.Frame(self.root, bg=COLORS["border"], height=1).pack(fill="x", padx=20, pady=8)
            tk.Button(
                self.root, text="🔄  Reset All Votes (Admin Only)", font=FONTS["label"],
                bg=COLORS["accent_red"], fg=COLORS["white"],
                activebackground="#C0392B", activeforeground=COLORS["white"],
                relief="flat", cursor="hand2", command=self._reset_votes, pady=8,
            ).pack(padx=20, fill="x")

        # Refresh Button
        tk.Button(
            self.root, text="🔃  Refresh Results", font=FONTS["label"],
            bg=COLORS["bg_input"], fg=COLORS["text_muted"],
            activebackground=COLORS["border"], activeforeground=COLORS["text_primary"],
            relief="flat", cursor="hand2", command=self._refresh, pady=6,
        ).pack(padx=20, fill="x", pady=(8, 20))

    def _draw_bar_chart(self, parent, results, total):
        canvas_w = 580
        canvas_h = 160
        canvas = tk.Canvas(parent, width=canvas_w, height=canvas_h,
                           bg=COLORS["bg_card"], highlightthickness=0)
        canvas.pack()

        if total == 0:
            canvas.create_text(canvas_w // 2, canvas_h // 2, text="No votes yet",
                               fill=COLORS["text_muted"], font=FONTS["body"])
            return

        bar_colors = [COLORS["accent"], COLORS["accent_green"], "#5B9BD5", "#9B59B6"]
        bar_height = 28
        max_bar_w  = 300
        y_start    = 20
        label_x    = 10
        bar_x      = 180
        gap        = 48
        max_votes  = max(r["votes"] for r in results) if results else 1

        for i, r in enumerate(results):
            y     = y_start + i * gap
            color = bar_colors[i % len(bar_colors)]

            canvas.create_text(label_x, y + bar_height // 2,
                               text=f"{r['symbol']} {r['name']}",
                               fill=COLORS["text_primary"], font=FONTS["label"], anchor="w")

            canvas.create_rectangle(bar_x, y, bar_x + max_bar_w, y + bar_height,
                                    fill=COLORS["bg_input"], outline="")

            fill_w = int(max_bar_w * r["votes"] / max_votes) if max_votes > 0 else 0
            if fill_w > 0:
                canvas.create_rectangle(bar_x, y, bar_x + fill_w, y + bar_height,
                                        fill=color, outline="")

            pct = r["votes"] / total * 100 if total > 0 else 0
            canvas.create_text(bar_x + max_bar_w + 10, y + bar_height // 2,
                               text=f"{r['votes']} ({pct:.0f}%)",
                               fill=COLORS["text_primary"], font=FONTS["label"], anchor="w")

    def _build_table(self, parent, results, total):
        headers = ["Rank", "Symbol", "Candidate", "Party", "Votes", "%"]
        widths   = [4,       6,       18,          18,      6,       6]

        header_frame = tk.Frame(parent, bg=COLORS["bg_input"])
        header_frame.pack(fill="x", pady=(0, 4))

        for header, w in zip(headers, widths):
            tk.Label(header_frame, text=header, font=FONTS["body_bold"],
                     bg=COLORS["bg_input"], fg=COLORS["accent"],
                     width=w, anchor="w").pack(side="left", padx=4, pady=4)

        for rank, r in enumerate(results, start=1):
            pct    = f"{r['votes']/total*100:.1f}%" if total > 0 else "0%"
            row_bg = COLORS["bg_card"] if rank % 2 == 0 else "#1F3248"
            row    = tk.Frame(parent, bg=row_bg)
            row.pack(fill="x")

            for val, w in zip([str(rank), r["symbol"], r["name"], r["party"], str(r["votes"]), pct], widths):
                tk.Label(row, text=val, font=FONTS["body"], bg=row_bg,
                         fg=COLORS["text_primary"], width=w, anchor="w").pack(side="left", padx=4, pady=3)

    def _reset_votes(self):
        from tkinter import messagebox
        confirm = messagebox.askyesno(
            "Reset Votes",
            "Are you sure you want to RESET ALL VOTES?\nThis will clear all vote records and allow voters to vote again.",
        )
        if confirm:
            db.reset_all_votes()
            messagebox.showinfo("Done", "All votes have been reset successfully.")
            self._refresh()

    def _refresh(self):
        self.win.destroy()
        ResultsWindow(tk.Toplevel(), is_admin=self.is_admin)