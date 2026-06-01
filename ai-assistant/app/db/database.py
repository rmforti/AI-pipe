from pathlib import Path
import sqlite3

DB_PATH = Path("rag.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    schema_path = Path(__file__).parent / "schema.sql"

    with open(schema_path, "r", encoding="utf-8") as file:
        schema = file.read()

    conn = get_connection()

    try:
        conn.executescript(schema)
        conn.commit()

        tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        print("Tables:", [row[0] for row in tables])

    finally:
        conn.close()