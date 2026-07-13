import sqlite3
import pandas as pd

DATABASE = "db/nifty100.db"


def test_peer_percentiles_table_exists():

    conn = sqlite3.connect(DATABASE)

    tables = pd.read_sql(

        "SELECT name FROM sqlite_master WHERE type='table'",

        conn

    )

    conn.close()

    assert "peer_percentiles" in tables["name"].values


def test_peer_percentiles_not_empty():

    conn = sqlite3.connect(DATABASE)

    count = pd.read_sql(

        "SELECT COUNT(*) AS total FROM peer_percentiles",

        conn

    )

    conn.close()

    assert count.loc[0, "total"] > 0


def test_peer_groups_exist():

    conn = sqlite3.connect(DATABASE)

    count = pd.read_sql(

        """
        SELECT COUNT(DISTINCT peer_group_name) total
        FROM peer_groups
        """,

        conn

    )

    conn.close()

    assert count.loc[0, "total"] == 11


def test_percentile_range():

    conn = sqlite3.connect(DATABASE)

    df = pd.read_sql(

        """
        SELECT percentile_rank
        FROM peer_percentiles
        """,

        conn

    )

    conn.close()

    assert df["percentile_rank"].between(0, 1).all()