"""
main.py — Entry Point for E-Voting System
Run this file to start the application.

Project  : Python-Based E-Voting System
Author   : BTech 2nd Year Mini Project
Database : SQLite (built-in, no installation needed)
GUI      : Tkinter (built-in, no installation needed)

How to Run:
    python main.py

Modules:
    main.py          → App entry point (this file)
    database.py      → All database operations
    login_window.py  → Voter login screen
    voting_window.py → Candidate selection & vote casting
    results_window.py→ Results & bar chart display
    admin_window.py  → Admin authentication & controls
    styles.py        → Color theme & font constants
"""

import tkinter as tk
import database as db
from login_window import LoginWindow


def main():
    """
    Main function — initializes the database and launches the GUI.
    This is the program's starting point.
    """
    print("=" * 50)
    print("   E-VOTING SYSTEM — Starting Up")
    print("=" * 50)

    # Step 1: Set up the database (create tables + demo data if needed)
    db.initialize_database()
    print("[APP] Database ready.")

    # Step 2: Create the root Tkinter window
    root = tk.Tk()
    # root.withdraw()   # comment this out temporarily   # Hide root; LoginWindow creates its own styled window

    # Step 3: Launch the Login Window
    login = LoginWindow(root)
    print("[APP] Login window launched.")

    # Step 4: Start the Tkinter event loop (keeps window alive)
    root.mainloop()

    print("[APP] Application closed.")


# Standard Python entry point check
if __name__ == "__main__":
    main()
