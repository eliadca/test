import sqlite3

DB_NAME = 'baseball_stats.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Create tables metadata table
    cursor.execute('''CREATE TABLE IF NOT EXISTS tables (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                     )''')

    # Create rows table
    cursor.execute('''CREATE TABLE IF NOT EXISTS rows (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        table_id INTEGER NOT NULL,
                        name TEXT,
                        ave REAL,
                        ab INTEGER,
                        h INTEGER,
                        k INTEGER,
                        bb INTEGER,
                        hbp INTEGER,
                        doubles INTEGER,
                        triples INTEGER,
                        hr INTEGER,
                        rbi INTEGER,
                        r INTEGER,
                        ops REAL,
                        FOREIGN KEY(table_id) REFERENCES tables(id) ON DELETE CASCADE
                     )''')

    conn.commit()
    conn.close()

def get_db_connection():
    return sqlite3.connect(DB_NAME)

init_db()