import sqlite3

conn = sqlite3.connect('data/user_translation.db')
cursor = conn.cursor()

cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_translation (
                    user_id INTEGER PRIMARY KEY, 
                    default_translation TEXT
                )
              ''')
conn.commit()

def get_user_translation(user_id):
    cursor.execute("SELECT default_translation FROM user_translation WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    return result[0] if result else None

def get_user_settings(user_id):
    cursor.execute("SELECT * FROM user_translation WHERE user_id = ?", (user_id,))
    return cursor.fetchone()

def set_user_translation(user_id, translation):
    cursor.execute("REPLACE INTO user_translation (user_id, default_translation) VALUES (?, ?)", (user_id, translation))
    conn.commit()

def get_user_count():
    cursor.execute("SELECT COUNT(*) FROM user_translation")
    return cursor.fetchone()[0]

def remove_user_translation(user_id):
    cursor.execute("DELETE FROM user_translation WHERE user_id = ?", (user_id,))
    conn.commit()