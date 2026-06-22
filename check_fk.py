import sqlite3

conn = sqlite3.connect(
    "db/nifty100.db"
)

cursor = conn.cursor()

cursor.execute(
    "PRAGMA foreign_key_check"
)

rows = cursor.fetchall()

print(rows)

conn.close()