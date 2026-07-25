"""
Sprint 5 - Day 32
Capital Allocation Report
"""
from pathlib import Path
import sqlite3
import pandas as pd
import numpy as np
# ==========================================================
# PROJECT PATHS
# ==========================================================

ROOT = Path(__file__).resolve().parents[2]
DB_FILE = ROOT / "db" / "nifty100.db"
CAPITAL_FILE = ROOT / "output" / "capital_allocation.csv"
CASHFLOW_FILE = ROOT / "output" / "cashflow_intelligence.xlsx"
PATTERN_OUTPUT = ROOT / "output" / "pattern_changes.csv"
# ==========================================================
# PRINT HEADER
# ==========================================================

def print_header(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)
# ==========================================================
# DATABASE
# ==========================================================

def connect_database():
    print_header("Connecting Database")
    conn = sqlite3.connect(DB_FILE)
    print("Database Connected")
    return conn
# ==========================================================
# LOAD CAPITAL ALLOCATION
# ==========================================================

def load_capital_allocation():
    print_header("Loading Capital Allocation")
    df = pd.read_csv(CAPITAL_FILE)
    print(f"Rows : {len(df)}")
    print(f"Columns : {len(df.columns)}")
    print("\nColumns")
    for c in df.columns:
        print(c)
    return df
# ==========================================================
# LOAD CASHFLOW INTELLIGENCE
# ==========================================================

def load_cashflow_intelligence():
    print_header("Loading Cashflow Intelligence")
    df = pd.read_excel(CASHFLOW_FILE)
    print(f"Rows : {len(df)}")
    return df
# ==========================================================
# VERIFY CAPITAL DATA
# ==========================================================

def verify_capital_allocation(df):
    print_header("Verifying Capital Allocation")
    companies = df["company_id"].nunique()
    years = df["year"].nunique()
    print(f"Companies : {companies}")
    print(f"Years      : {years}")
    expected = companies * years
    print(f"Expected Records : {expected}")
    print(f"Actual Records   : {len(df)}")
    if expected == len(df):
        print("\n Dataset Complete")
    else:
        print("\n Missing Records Detected")
# ==========================================================
# MAIN
# ==========================================================

def main():
    print_header("Sprint 5 Day 32")
    conn = connect_database()
    capital = load_capital_allocation()
    cashflow = load_cashflow_intelligence()
    verify_capital_allocation(capital)
    conn.close()
    print_header("Foundation Ready")

if __name__ == "__main__":
    main()