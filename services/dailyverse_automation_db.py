import sqlite3

conn = sqlite3.connect('data/dailyverse_automation.db')
cursor = conn.cursor()

cursor.execute('''
                CREATE TABLE IF NOT EXISTS dailyverse_automation (
                    user_id INTEGER,
                    guild_id INTEGER,
                    channel_id INTEGER,
                    hour INTEGER,
                    timezone TEXT,
                    PRIMARY KEY (user_id, guild_id)
                )
              ''')
conn.commit()

def get_dailyverse_automation_user_count():
    cursor.execute("SELECT COUNT(*) FROM dailyverse_automation")
    return cursor.fetchone()[0]

def set_dailyverse_automation(user_id, guild_id, channel_id, hour, timezone):
    cursor.execute('''
        INSERT INTO dailyverse_automation (user_id, guild_id, channel_id, hour, timezone)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(user_id, guild_id) DO UPDATE SET
            channel_id=excluded.channel_id,
            hour=excluded.hour,
            timezone=excluded.timezone
    ''', (user_id, guild_id, channel_id, hour, timezone))
    conn.commit()

def get_dailyverse_automation_settings(user_id, guild_id):
    cursor.execute('''
        SELECT channel_id, hour, timezone
        FROM dailyverse_automation
        WHERE user_id = ? AND guild_id = ?
    ''', (user_id, guild_id))
    return cursor.fetchone()

def get_all_dailyverse_automation_settings():
    cursor.execute('''
        SELECT user_id, guild_id, channel_id, hour, timezone
        FROM dailyverse_automation
    ''')
    return cursor.fetchall()

def delete_dailyverse_automation(user_id, guild_id):
    cursor.execute("DELETE FROM dailyverse_automation WHERE user_id = ? AND guild_id = ?", (user_id, guild_id))
    conn.commit()