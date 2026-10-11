import sqlite3

class Gestore_DB:
    def __init__(self):
        connection = sqlite3.connect("NoteWork.db")
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS note (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                content TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_modified_at DATETIME
            )
        """)
        
        connection.commit()
        connection.close()
    
    def new_note(self, title, content, created_at, last_modified_at):
        connection = sqlite3.connect("NoteWork.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO note (title, content, created_at, last_modified_at) VALUES (?, ?, ?, ?)", (title, content, created_at, last_modified_at))
        connection.commit()
        connection.close()
        
    def get_all_notes(self):
        connection = sqlite3.connect("NoteWork.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM note")
        notes = cursor.fetchall()
        connection.close()
        return notes