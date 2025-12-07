import sqlite3

def init_db():
    conn = sqlite3.connect("warnings.db")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS warnings (
            guild_id INTEGER,
            user_id INTEGER,
            reason TEXT,
            timestamp TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS owners (
            guild_id INTEGER PRIMARY KEY,
            owner_id INTEGER
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            guild_id INTEGER PRIMARY KEY,
            admin_id INTEGER
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS report_channels (
            guild_id INTEGER PRIMARY KEY,
            channel_id INTEGER
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS url_whitelist (
            domain TEXT PRIMARY KEY
        )
    """)

    conn.commit()
    conn.close()

def set_owner(guild_id: int, owner_id: int):
    conn = sqlite3.connect("warnings.db")
    c = conn.cursor()
    c.execute("REPLACE INTO owners (guild_id, owner_id) VALUES (?, ?)", (guild_id, owner_id))
    conn.commit()
    conn.close()

def get_owner(guild_id: int):
    conn = sqlite3.connect("warnings.db")
    c = conn.cursor()
    c.execute("SELECT owner_id FROM owners WHERE guild_id = ?", (guild_id,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

def set_admin(guild_id: int, admin_id: int):
    conn = sqlite3.connect("warnings.db")
    c = conn.cursor()
    c.execute("REPLACE INTO admins (guild_id, admin_id) VALUES (?, ?)", (guild_id, admin_id))
    conn.commit()
    conn.close()

def get_admin(guild_id: int):
    conn = sqlite3.connect("warnings.db")
    c = conn.cursor()
    c.execute("SELECT admin_id FROM admins WHERE guild_id = ?", (guild_id,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

def set_report_channel(guild_id: int, channel_id: int):
    conn = sqlite3.connect("warnings.db")
    c = conn.cursor()
    c.execute("REPLACE INTO report_channels (guild_id, channel_id) VALUES (?, ?)", (guild_id, channel_id))
    conn.commit()
    conn.close()

def get_report_channel(guild_id: int):
    conn = sqlite3.connect("warnings.db")
    c = conn.cursor()
    c.execute("SELECT channel_id FROM report_channels WHERE guild_id = ?", (guild_id,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None
