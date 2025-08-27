import sqlite3

DB_NAME = "salary.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Create the salaries table
    c.execute("""
    CREATE TABLE IF NOT EXISTS salaries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        gross REAL NOT NULL,
        pension REAL NOT NULL,
        tax REAL NOT NULL,
        net REAL NOT NULL,
        created_at TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()
    print(f"Database '{DB_NAME}' initialized successfully with 'salaries' table.")

if __name__ == "__main__":
    init_db()
