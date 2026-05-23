# 🗳️ E-Voting System

A secure, desktop-based digital voting application built with Python. Designed to allow individuals and organizations to conduct fair, validated elections with built-in integrity checks.

---

## 🚀 Features

- ✅ **Age Verification** — Only voters aged 18+ are allowed to register and vote
- ✅ **Unique Voter ID** — Each voter ID can only be used once, preventing duplicate votes
- ✅ **Voter Registration** — Captures name, age, gender, and Voter ID at login
- ✅ **Candidate Management** — Lists all candidates standing in the election
- ✅ **Live Voting Window** — Clean GUI for casting votes securely
- ✅ **Results Window** — Displays real-time election results after voting closes
- ✅ **Persistent Storage** — All data stored in a local SQLite database

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.x |
| GUI Framework | Tkinter |
| Database | SQLite3 |
| Styling | Custom styles module |

---

## 📁 Project Structure

```
e-voting-system/
│
├── main.py              # Entry point — launches the application
├── login_window.py      # Voter registration & age/ID validation
├── voting_window.py     # Voting interface & candidate selection
├── results_window.py    # Election results display
├── database.py          # Database setup & all CRUD operations
├── database.db          # SQLite database file (auto-generated)
└── styles.py            # Centralized UI styling constants
```

---

## ⚙️ How to Run

**1. Clone the repository**
```bash
git clone https://github.com/HardikT09/e-voting-system.git
cd e-voting-system
```

**2. Make sure Python 3 is installed**
```bash
python --version
```

**3. Run the application**
```bash
python main.py
```

> No external libraries required — uses only Python standard library (Tkinter + SQLite3)

---

## 🖥️ How It Works

1. Voter opens the app and enters their **Name, Age, Gender, and Voter ID**
2. System validates: age must be **18+** and Voter ID must be **unique**
3. If valid, voter proceeds to the **Voting Window** and selects a candidate
4. Vote is recorded in the **SQLite database**
5. After voting closes, the **Results Window** displays final counts

---

## 📌 Use Cases

- Student body elections
- Society or club polls
- Small organizational voting
- Any scenario requiring a fair, validated voting process

---

## 🙋‍♂️ Author

**Hardik Takkar**
- LinkedIn: [linkedin.com/in/hardik-takkar](https://linkedin.com/in/hardik-takkar)
- GitHub: [github.com/HardikT09](https://github.com/HardikT09)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
