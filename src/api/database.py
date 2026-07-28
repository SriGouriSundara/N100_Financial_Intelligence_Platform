"""
SQLite database connection helper
Sprint 6 Day 38
"""


import sqlite3


DB_PATH = "db/nifty100.db"



def get_connection():
    """
    Create SQLite database connection.
    """

    connection = sqlite3.connect(
        DB_PATH
    )

    connection.row_factory = sqlite3.Row

    return connection