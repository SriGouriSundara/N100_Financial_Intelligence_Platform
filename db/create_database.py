import sqlite3
from pathlib import Path

DB_PATH = "db/nifty100.db"
SCHEMA_PATH = "db/schema.sql"

conn = sqlite3.connect(DB_PATH)

conn.execute(
    "PRAGMA foreign_keys = ON;"
)

with open(
    SCHEMA_PATH,
    "r",
    encoding="utf-8"
) as f:

    schema = f.read()

conn.executescript(schema)

conn.commit()

conn.close()

print("Database Created Successfully")