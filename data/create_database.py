import sqlite3

def create_database():
    conn = sqlite3.connect('templates.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS templates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        trigger TEXT,
        type TEXT,
        body TEXT,
        footer TEXT,
        options TEXT,
        seed TEXT,
        additional_actions TEXT
    )
    ''')
    
    conn.commit()
    conn.close()

create_database()