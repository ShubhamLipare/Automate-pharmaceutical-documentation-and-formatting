import sqlite3
from pathlib import Path
from datetime import datetime

class SqliteMemory:
    def __init__(self,db_path="memory/agent_memory.db"):
        Path("memory").mkdir(exist_ok=True)
        self.db_path=db_path
        self.conn=sqlite3.connect(self.db_path,check_same_thread=False)
        self._create_table()
        
    def _create_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS submissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_query TEXT,
                research_notes TEXT,
                risk_assessment TEXT,
                human_feedback TEXT,
                final_report TEXT,
                created_at TEXT
            )
        """)
        self.conn.commit()
    
    def save_submission(self,state):
        self.conn.execute("""
            Insert into submissions (
                user_query,
                research_notes,
                risk_assessment,
                human_feedback,
                final_report,
                created_at) values (?, ?, ?, ?, ?, ?)
            """,(
            state.get("user_query"),
            state.get("research_notes"),
            state.get("risk_assessment"),
            state.get("human_feedback"),
            state.get("final_report"),
            datetime.now().isoformat()
            ))
        self.conn.commit()

    def fetch_similar_queries(self, user_query):
        cursor = self.conn.execute("""
            SELECT user_query, research_notes, human_feedback
            FROM submissions
            WHERE user_query LIKE ?
            ORDER BY created_at DESC
            LIMIT 3
        """, (f"%{user_query}%",))
        return cursor.fetchall()
    
    def init_auth_table(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password_hash TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        conn.close()