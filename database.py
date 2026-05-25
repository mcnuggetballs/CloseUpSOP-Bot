import sqlite3
from config import DATABASE_NAME


def get_connection():

    conn = sqlite3.connect(DATABASE_NAME)

    conn.row_factory = sqlite3.Row

    return conn


def init_db():

    conn = get_connection()

    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS aircon_status(
        aircon_name TEXT PRIMARY KEY,
        status TEXT,
        user_name TEXT,
        timestamp TEXT,
        photo_file_id TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS aircon_logs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_user_id INTEGER,
        user_name TEXT,
        aircon_name TEXT,
        action TEXT,
        timestamp TEXT,
        photo_file_id TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS closeup_logs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_user_id INTEGER,
        user_name TEXT,
        date TEXT,
        completion_timestamp TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS closeup_photos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        closeup_log_id INTEGER,
        step_number INTEGER,
        telegram_file_id TEXT
    )
    """)

    conn.commit()

    conn.close()