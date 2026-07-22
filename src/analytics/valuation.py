"""
Sprint 4 – Day 26
Valuation Module

This module:

1. Reads SQLite database
2. Reads market_cap.xlsx
3. Merges valuation data
4. Computes FCF Yield
5. Computes Sector Median P/E
6. Generates valuation flags
7. Exports Excel & CSV outputs
"""

import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd
# ----------------------------------------------------
# Project Paths
# ----------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DB_PATH = PROJECT_ROOT / "db" / "nifty100.db"

MARKET_CAP_FILE = PROJECT_ROOT / "data" / "raw" / "market_cap.xlsx"

OUTPUT_DIR = PROJECT_ROOT / "output"

OUTPUT_DIR.mkdir(exist_ok=True)
# ----------------------------------------------------
# Database Connection
# ----------------------------------------------------

def get_connection():

    return sqlite3.connect(DB_PATH)
# ----------------------------------------------------
# Load Market Cap
# ----------------------------------------------------

def load_market_cap():

    print("Loading market_cap.xlsx...")

    df = pd.read_excel(MARKET_CAP_FILE)

    print(f"Rows : {len(df)}")

    return df
market = load_market_cap()

print(market.columns.tolist())

print(market.head())
# ----------------------------------------------------
# Company Master
# ----------------------------------------------------

def load_companies():

    conn = get_connection()

    query = """

    SELECT

        c.id,

        c.company_name,

        s.broad_sector

    FROM companies c

    LEFT JOIN sectors s

    ON c.id = s.company_id

    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df
# ----------------------------------------------------
# Latest Financial Ratios
# ----------------------------------------------------

def load_ratios():

    conn = get_connection()

    query = """

    SELECT *

    FROM financial_ratios

    WHERE year =

    (

        SELECT MAX(year)

        FROM financial_ratios

    )

    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df
# ----------------------------------------------------
# Merge Everything
# ----------------------------------------------------

def merge_data():
    """
    Merge companies, latest financial ratios and latest market-cap data.
    One row per company.
    """

    companies = load_companies()

    ratios = load_ratios()

    market = load_market_cap()

    # -------------------------------------------------
    # Keep latest financial year only
    # -------------------------------------------------
    ratios = (
        ratios.sort_values("year")
              .groupby("company_id", as_index=False)
              .last()
    )

    # -------------------------------------------------
    # Keep latest market year only
    # -------------------------------------------------
    market = (
        market.sort_values("year")
              .groupby("company_id", as_index=False)
              .last()
    )

    # -------------------------------------------------
    # Merge companies + ratios
    # -------------------------------------------------
    df = companies.merge(
        ratios,
        left_on="id",
        right_on="company_id",
        how="left"
    )

    # -------------------------------------------------
    # Merge market data
    # -------------------------------------------------
    df = df.merge(
        market,
        on="company_id",
        how="left",
        suffixes=("", "_market")
    )

    print("=" * 60)
    print("Companies :", len(companies))
    print("Latest Ratios :", len(ratios))
    print("Latest Market :", len(market))
    print("Merged :", len(df))
    print("=" * 60)

    return df
# ----------------------------------------------------
# Keep Latest Record Per Company
# ----------------------------------------------------

def latest_company_records(df):
    """
    Keep only the latest year available for each company.
    This ensures valuation_summary.xlsx contains one row
    per company (92 rows).
    """

    if "year" in df.columns:

        df = df.sort_values("year")

        df = df.groupby("company_id", as_index=False).last()

    return df
# ----------------------------------------------------
# FCF Yield
# ----------------------------------------------------

def calculate_fcf_yield(df):

    df["FCF_yield_pct"] = (

        df["free_cash_flow_cr"]

        /

        df["market_cap_crore"]

    ) * 100

    return df
# ----------------------------------------------------
# Sector Median PE
# ----------------------------------------------------

def calculate_sector_pe(df):

    sector_pe = (

        df.groupby("broad_sector")["pe_ratio"]

        .median()

        .reset_index()

        .rename(

            columns={

                "pe_ratio": "sector_median_pe"

            }

        )

    )

    df = df.merge(

        sector_pe,

        on="broad_sector",

        how="left"

    )

    return df
# ----------------------------------------------------
# PE vs Sector
# ----------------------------------------------------

def compare_sector(df):

    df["PE_vs_sector_median_pct"] = (

        (

            df["pe_ratio"]

            -

            df["sector_median_pe"]

        )

        /

        df["sector_median_pe"]

    ) * 100

    return df
# ----------------------------------------------------
# Valuation Flag
# ----------------------------------------------------

def valuation_flag(row):

    pe = row["pe_ratio"]

    median = row["sector_median_pe"]

    if pd.isna(pe) or pd.isna(median):

        return "Unknown"

    if pe > median * 1.5:

        return "Caution"

    elif pe < median * 0.7:

        return "Discount"

    else:

        return "Fair"
def apply_flags(df):

    df["flag"] = df.apply(

        valuation_flag,

        axis=1

    )

    return df
# ----------------------------------------------------
# Prepare Final Output
# ----------------------------------------------------

def create_summary(df):

    summary = pd.DataFrame({

        "company_id": df["company_id"],

        "company_name": df["company_name"],

        "sector": df["broad_sector"],

        "P/E": df["pe_ratio"],

        "P/B": df["pb_ratio"],

        "EV/EBITDA": df["ev_ebitda"],

        "FCF_yield_pct": df["FCF_yield_pct"],

        "Sector_Median_PE": df["sector_median_pe"],

        "PE_vs_Sector_Median_pct":

            df["PE_vs_sector_median_pct"],

        "Flag": df["flag"]

    })

    return summary
# ----------------------------------------------------
# Export Excel
# ----------------------------------------------------

def export_summary(summary):

    output_file = OUTPUT_DIR / "valuation_summary.xlsx"

    summary.to_excel(

        output_file,

        index=False,

        engine="openpyxl"

    )

    print()

    print("=" * 60)

    print("valuation_summary.xlsx generated")

    print(output_file)

    print("=" * 60)
# ---------------------------------------------------------
# Export Valuation Flags
# ---------------------------------------------------------

def export_flags(summary):
    """
    Export only Caution and Discount companies.
    """

    flags = summary[
        summary["Flag"].isin(["Caution", "Discount"])
    ].copy()

    output_file = OUTPUT_DIR / "valuation_flags.csv"

    flags.to_csv(
        output_file,
        index=False
    )

    print()

    print("=" * 60)
    print("valuation_flags.csv generated")
    print(output_file)
    print("Flagged Companies :", len(flags))
    print("=" * 60)

    return flags    
# ----------------------------------------------------
# Pipeline
# ----------------------------------------------------

def prepare_valuation():

    print("=" * 60)
    print("Preparing Valuation Module")
    print("=" * 60)

    df = merge_data()
    df = latest_company_records(df)
    df = calculate_fcf_yield(df)

    df = calculate_sector_pe(df)

    df = compare_sector(df)

    df = apply_flags(df)
    summary = create_summary(df)

    export_summary(summary)

    flags = export_flags(summary)

    return summary, flags
    print("Valuation calculations completed.")

    return df
if __name__ == "__main__":
    summary, flags = prepare_valuation()

print()

print(summary.head())

print()

print("Summary Rows :", len(summary))

print("Flagged Rows :", len(flags))
