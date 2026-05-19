import sqlite3
import uuid

class DatabaseManager:
    def __init__(self, db_name="agent_builder.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS agents (
                id TEXT PRIMARY KEY,
                name TEXT,
                system_prompt TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id TEXT PRIMARY KEY,
                agent_name TEXT,
                user_message TEXT,
                ai_response TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def save_agent(self, name, prompt):
        try:
            new_id = str(uuid.uuid4())
            self.cursor.execute('INSERT INTO agents (id, name, system_prompt) VALUES (?, ?, ?)', (new_id, name, prompt))
            self.conn.commit()
            return new_id
        except Exception as e:
            print(f"Error saving agent: {e}")
            return None
        
    def update_agent(self, agent_id, name, prompt):
        try:
            self.cursor.execute('''
                UPDATE agents 
                SET name = ?, system_prompt = ? 
                WHERE id = ?
            ''', (name, prompt, agent_id))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Update Error: {e}")
            return False

    def get_agent_prompt(self, name):
        self.cursor.execute('SELECT system_prompt FROM agents WHERE name = ?', (name,))
        row = self.cursor.fetchone()
        return row[0] if row else None
    
    def get_agent_details(self, agent_id):
        self.cursor.execute('SELECT id, name, system_prompt FROM agents WHERE id = ?', (agent_id,))
        row = self.cursor.fetchone()
        if row:
            return {"id": row[0], "name": row[1], "prompt": row[2]}
        return None

    def add_history(self, agent_name, message, response):
        try:
            self.cursor.execute('''
                INSERT INTO history (id, agent_name, user_message, ai_response)
                VALUES (?, ?, ?, ?)
            ''', (str(uuid.uuid4()), agent_name, message, response))
            self.conn.commit()
        except Exception as e:
            print(f"History Error: {e}")

    def get_history(self, agent_name):
        self.cursor.execute('SELECT user_message, ai_response FROM history WHERE agent_name = ? ORDER BY timestamp DESC', (agent_name,))
        return self.cursor.fetchall()

    def fetch_all_agents(self):
        self.cursor.execute('SELECT id, name FROM agents')
        return [{"id": row[0], "name": row[1]} for row in self.cursor.fetchall()]
    
    def delete_agent(self, agent_id):
        try:
            self.cursor.execute("SELECT name FROM agents WHERE id = ?", (agent_id,))
            row = self.cursor.fetchone()
            if row:
                self.cursor.execute("DELETE FROM agents WHERE id = ?", (agent_id,))
                self.cursor.execute("DELETE FROM history WHERE agent_name = ?", (row[0],))
                self.conn.commit()
            return True
        except Exception as e:
            print(f"Delete Error: {e}")
            return False