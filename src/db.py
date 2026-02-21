import sqlite3
from exceptions.custom_exception import CustomException
from logger import GLOBAL_LOGGER as log
def get_connection():
    try:
        log.info("connecting to database")
        conn=sqlite3.connect("business_ai.db")
        conn.row_factory=sqlite3.Row
        return conn
    except Exception as e:
        log.error(f"Error while connecting databse:{e}")
        raise CustomException(f"Error while connecting databse:{e}")

def init_db():
    conn=get_connection()
    log.info("connected to database sucessfully.")
    cursor = conn.cursor()
    # Documents table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # Reports table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT,
            report TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # Memory table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            key TEXT,
            value TEXT
        )
    """)
    conn.commit()
    conn.close()

