import sqlite3
import json

class DatabaseManager:
    def __init__(self, db_name="agent_history.db"):
        # Database file se connect karein (Agar file nahi hai to khud ban jayegi)
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        # Table banana: History store karne ke liye
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                original_prompt TEXT,
                intent TEXT,
                tone TEXT,
                improved_prompt TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def add_record(self, prompt, intent, tone, improved):
        # Data insert karne ka function
        self.cursor.execute('''
            INSERT INTO history (original_prompt, intent, tone, improved_prompt)
            VALUES (?, ?, ?, ?)
        ''', (prompt, str(intent), str(tone), improved))
        self.conn.commit()

    def fetch_all(self):
        # Saara data nikalne ke liye
        self.cursor.execute('SELECT * FROM history ORDER BY timestamp DESC')
        return self.cursor.fetchall()