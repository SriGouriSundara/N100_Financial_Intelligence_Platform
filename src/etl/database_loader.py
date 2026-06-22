"""
Day 05 - Full Data Load

Purpose:
--------
1. Read all Excel files
2. Normalize data
3. Load into SQLite
4. Generate load_audit.csv
5. Show FULL errors for debugging

"""
import sqlite3
import pandas as pd
from pathlib import Path

# ==================================================
# PATHS
# ==================================================

BASE_DIR = Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / "db" / "nifty100.db"

RAW_DIR = BASE_DIR / "data" / "raw"

OUTPUT_DIR = BASE_DIR / "output"

OUTPUT_DIR.mkdir(exist_ok=True)

# ==================================================
# FILES
# ==================================================

DATA_FILES = {
    "companies": "companies.xlsx",
    "analysis": "analysis.xlsx",
    "documents": "documents.xlsx",
    "profitandloss": "profitandloss.xlsx",
    "balancesheet": "balancesheet.xlsx",
    "cashflow": "cashflow.xlsx",
    "financial_ratios": "financial_ratios.xlsx",
    "peer_groups": "peer_groups.xlsx",
    "sectors": "sectors.xlsx",
    "stock_prices": "stock_prices.xlsx"
}

# Files with title row
HEADER_ONE_FILES = {
    "companies",
    "analysis",
    "documents",
    "profitandloss",
    "balancesheet",
    "cashflow"
}

# ==================================================
# READ EXCEL
# ==================================================

def load_excel(table_name, file_name):

    file_path = RAW_DIR / file_name

    if table_name in HEADER_ONE_FILES:

        df = pd.read_excel(
            file_path,
            header=1
        )

    else:

        df = pd.read_excel(
            file_path
        )

    return df

# ==================================================
# LOAD TABLE
# ==================================================

def load_table(conn, table_name, file_name):

    print(f"Loading {table_name}")

    df = load_excel(
        table_name,
        file_name
    )

    rows = len(df)

    df.to_sql(
        table_name,
        conn,
        if_exists="append",
        index=False
    )

    return rows

# ==================================================
# MAIN
# ==================================================

def main():

    conn = sqlite3.connect(DB_PATH)

    audit_rows = []

    load_order = [
        "companies",
        "analysis",
        "documents",
        "profitandloss",
        "balancesheet",
        "cashflow",
        "financial_ratios",
        "peer_groups",
        "sectors",
        "stock_prices"
    ]

    for table in load_order:

        rows = load_table(
            conn,
            table,
            DATA_FILES[table]
        )

        audit_rows.append(
            {
                "table_name": table,
                "rows_loaded": rows
            }
        )

    audit_df = pd.DataFrame(audit_rows)

    audit_df.to_csv(
        OUTPUT_DIR / "load_audit.csv",
        index=False
    )

    conn.commit()

    conn.close()

    print("\nLOAD COMPLETE")

if __name__ == "__main__":
    main()