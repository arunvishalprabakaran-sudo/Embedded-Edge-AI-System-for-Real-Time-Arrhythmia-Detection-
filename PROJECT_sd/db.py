"""
db.py
Single place that knows how to open a connection to the database.
Every other file imports get_connection() instead of calling sqlite3 directly —
so if you ever switch to PostgreSQL/MySQL later, this is the only file you touch.
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "patient_tracker.db")
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")   # SQLite disables FK enforcement by default
    conn.row_factory = sqlite3.Row             # lets us access columns by name, e.g. row["name"]
    return conn


def init_db():
    """Creates the tables if they don't exist yet. Safe to run multiple times."""
    conn = get_connection()
    with open(SCHEMA_PATH, "r") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print(f"Database initialized at {DB_PATH}")
