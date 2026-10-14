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
                last_modified_at DATETIME,
                ia_output TEXT
            )
        """)
        
        connection.commit()
        connection.close()
    
    def new_note(self, title="Nuova nota", content="", created_at="", last_modified_at="", ia_output=""):
        connection = sqlite3.connect("NoteWork.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO note (title, content, created_at, last_modified_at, ia_output) VALUES (?, ?, ?, ?, ?)", (title, content, created_at, last_modified_at, ia_output))
        connection.commit()
        
        note_id = cursor.lastrowid
        connection.close()
        return note_id
        
    def get_all_notes(self):
        connection = sqlite3.connect("NoteWork.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM note")
        notes = cursor.fetchall()
        connection.close()
        return notes
    
    def get_note_by_id(self, search_id):
        connection = sqlite3.connect("NoteWork.db")
        cursor = connection.cursor()
        cursor.execute("SELECT id, title, content, created_at, last_modified_at, ia_output FROM note WHERE id = ?", (search_id,))
        note = cursor.fetchone()
        connection.close()
        return note
    
    def update_note(self, note_id, title, content, last_modified_at, ia_output):
        connection = sqlite3.connect("NoteWork.db")
        cursor = connection.cursor()
        cursor.execute("UPDATE note SET title = ?, content = ?, last_modified_at = ?, ia_output = ? WHERE id = ?", (title, content, last_modified_at, ia_output, note_id))
        connection.commit()
        connection.close()
        
    def delete_note(self, note_id):
        connection = sqlite3.connect("NoteWork.db")
        cursor = connection.cursor()
        cursor.execute("DELETE FROM note WHERE id = ?", (note_id,))
        connection.commit()
        connection.close()