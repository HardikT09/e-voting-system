"""
database.py — Database Module for E-Voting System
Handles all SQLite database operations: setup, queries, updates.
Concepts used: Functions, SQLite, Database Handling
"""

import sqlite3  # Built-in Python library for SQLite databases

# ─── Database file path (same folder as project) ──────────────────────────────
DB_PATH = "database.db"


def get_connection():
    """
    Returns a connection object to the SQLite database.
    Using a function keeps database access modular and reusable.
    """
    conn = sqlite3.connect(DB_PATH)
    return conn


def initialize_database():
    """
    Creates all required tables and pre-fills demo voters and candidates.
    This function runs once when the app starts.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # ── Create 'voters' table ──────────────────────────────────────────────────
    # roll_no    : unique roll number — used as primary key
    # name       : voter's full name
    # age        : voter's age (must be 18+)
    # gender     : voter's gender
    # has_voted  : 0 = not voted yet, 1 = already voted
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS voters (
            roll_no   TEXT PRIMARY KEY,
            name      TEXT NOT NULL,
            age       INTEGER NOT NULL,
            gender    TEXT NOT NULL,
            has_voted INTEGER DEFAULT 0
        )
    """)

    # ── Create 'candidates' table ──────────────────────────────────────────────
    # candidate_id : unique ID for each candidate
    # name         : display name of the candidate
    # party        : political party name
    # symbol       : emoji symbol for the party
    # votes        : running vote count
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS candidates (
            candidate_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name         TEXT NOT NULL,
            party        TEXT NOT NULL,
            symbol       TEXT NOT NULL,
            votes        INTEGER DEFAULT 0
        )
    """)

    # ── Create 'votes' table (audit log) ──────────────────────────────────────
    # Stores each cast vote — useful for result analysis
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS votes (
            vote_id      INTEGER PRIMARY KEY AUTOINCREMENT,
            voter_id     TEXT NOT NULL,
            candidate_id INTEGER NOT NULL,
            timestamp    DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # ── Create 'admin' table ──────────────────────────────────────────────────
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admin (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    """)

    # ── No pre-filled voters — voters register themselves at login ────────────

    # ── Pre-fill Demo Candidates (if table is empty) ──────────────────────────
    cursor.execute("SELECT COUNT(*) FROM candidates")
    if cursor.fetchone()[0] == 0:
        demo_candidates = [
            ("Vikram Rathore",  "Progressive Party",    "🌟"),
            ("Meena Desai",     "Unity Alliance",        "🌸"),
            ("Suresh Kumar",    "National Front",        "🦁"),
        ]
        cursor.executemany(
            "INSERT INTO candidates (name, party, symbol, votes) VALUES (?, ?, ?, 0)",
            demo_candidates
        )

    # ── Pre-fill Admin Credentials ─────────────────────────────────────────────
    cursor.execute("SELECT COUNT(*) FROM admin")
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "INSERT INTO admin (username, password) VALUES (?, ?)",
            ("admin", "admin123")
        )

    conn.commit()
    conn.close()
    print("[DB] Database initialized successfully.")


# ─── VOTER FUNCTIONS ──────────────────────────────────────────────────────────

def get_voter(roll_no):
    """
    Returns the voter's row as a dict if found, else None.
    Used to check if roll number already exists (duplicate prevention).
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT roll_no, name, age, gender, has_voted FROM voters WHERE roll_no = ?",
        (roll_no,)
    )
    row = cursor.fetchone()
    conn.close()

    if row:
        return {"roll_no": row[0], "name": row[1], "age": row[2], "gender": row[3], "has_voted": row[4]}
    return None


def register_voter(roll_no, name, age, gender):
    """
    Registers a new voter into the database.
    Called when a new roll number logs in for the first time.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO voters (roll_no, name, age, gender, has_voted) VALUES (?, ?, ?, ?, 0)",
        (roll_no, name, age, gender)
    )
    conn.commit()
    conn.close()


def mark_voter_as_voted(roll_no):
    """
    Updates has_voted = 1 for the given voter after they cast their vote.
    This prevents duplicate voting.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE voters SET has_voted = 1 WHERE roll_no = ?",
        (roll_no,)
    )
    conn.commit()
    conn.close()


# ─── CANDIDATE FUNCTIONS ──────────────────────────────────────────────────────

def get_all_candidates():
    """
    Returns list of all candidates as list of dicts.
    Used to populate the voting screen.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT candidate_id, name, party, symbol, votes FROM candidates"
    )
    rows = cursor.fetchall()
    conn.close()

    candidates = []
    for row in rows:
        candidates.append({
            "candidate_id": row[0],
            "name":         row[1],
            "party":        row[2],
            "symbol":       row[3],
            "votes":        row[4],
        })
    return candidates


def cast_vote(roll_no, candidate_id):
    """
    Records the vote:
    1. Inserts a row into the votes audit table
    2. Increments the candidate's vote count
    3. Marks the voter as has_voted = 1
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO votes (voter_id, candidate_id) VALUES (?, ?)",
        (roll_no, candidate_id)
    )
    cursor.execute(
        "UPDATE candidates SET votes = votes + 1 WHERE candidate_id = ?",
        (candidate_id,)
    )
    cursor.execute(
        "UPDATE voters SET has_voted = 1 WHERE roll_no = ?",
        (roll_no,)
    )

    conn.commit()
    conn.close()


def get_results():
    """
    Returns all candidates sorted by votes descending.
    Used in the Results screen.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name, party, symbol, votes FROM candidates ORDER BY votes DESC"
    )
    rows = cursor.fetchall()
    conn.close()

    results = []
    for row in rows:
        results.append({
            "name":   row[0],
            "party":  row[1],
            "symbol": row[2],
            "votes":  row[3],
        })
    return results


def get_total_votes():
    """Returns total number of votes cast so far."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(votes) FROM candidates")
    total = cursor.fetchone()[0]
    conn.close()
    return total if total else 0


# ─── ADMIN FUNCTIONS ──────────────────────────────────────────────────────────

def verify_admin(username, password):
    """Returns True if admin credentials match."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM admin WHERE username = ? AND password = ?",
        (username, password)
    )
    result = cursor.fetchone()
    conn.close()
    return result is not None


def reset_all_votes():
    """
    Resets all votes for a fresh election (Admin only).
    Clears the votes table, resets candidate counts, marks all voters as not voted.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM votes")
    cursor.execute("UPDATE candidates SET votes = 0")
    cursor.execute("UPDATE voters SET has_voted = 0")
    conn.commit()
    conn.close()
