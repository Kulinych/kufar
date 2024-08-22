import sqlite3

name_db = 'kufar.db'

conn = sqlite3.connect(name_db)

with conn:
    conn.execute("CREATE TABLE IF NOT EXISTS ad (name TEXT, ad_id INTEGER, price FLOAT DEFAULT 0, date TEXT)")
