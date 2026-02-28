import sqlite3
from memory.sqlite_memory import SqliteMemory
import bcrypt

class AuthService:
    def __init__(self):
        self.memory=SqliteMemory()
        self.memory.init_auth_table()
        self.db_path=self.memory.db_path

    def hash_password(self,password):
        return bcrypt.hashpw(password.encode(),bcrypt.gensalt())
    
    def verify_password(self,password,hashed):
        return bcrypt.checkpw(password.encode(),hashed)
    
    def signup(self,username,password):
        conn=sqlite3.connect(self.db_path)
        cursor=conn.cursor()
        try:
            hashed_pw=self.hash_password(password)
            cursor.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, hashed_pw)
            )
            conn.commit()
            return True, "User created successfully"
        except sqlite3.IntegrityError:
            return False,"User Already exists"
        finally:
            conn.close()

    def login(self,username,password):
        conn=sqlite3.connect(self.db_path)
        cursor=conn.cursor()
        cursor.execute(
            "SELECT password_hash FROM users WHERE username = ?",
            (username,)
        )
        row=cursor.fetchone()
        conn.close()
        if not row:
            return False, "User not found"

        stored_hash = row[0]

        if self.verify_password(password, stored_hash):
            return True, "Login successful"
        else:
            return False, "Incorrect password"