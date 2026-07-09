"""
Sprint 3
Day 15

Financial Screener Engine

This module:

1. Reads screener_config.yaml
2. Connects to SQLite
3. Loads financial data
4. Applies configurable filters
5. Returns screened companies
6. Exports results
"""

import sqlite3
import yaml
import pandas as pd

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATABASE_PATH = PROJECT_ROOT / "db" / "nifty100.db"

CONFIG_PATH = PROJECT_ROOT / "config" / "screener_config.yaml"

OUTPUT_PATH = PROJECT_ROOT / "output"

OUTPUT_PATH.mkdir(exist_ok=True)

def connect_db():
    """
    Create SQLite connection.
    """

    return sqlite3.connect(DATABASE_PATH)

def load_config():
    """
    Load screener configuration.
    """

    with open(CONFIG_PATH, "r") as file:

        config = yaml.safe_load(file)

    return config

def load_tables(conn):
    """
    Load all required tables.
    """

    financial_ratios = pd.read_sql_query(
        "SELECT * FROM financial_ratios",
        conn
    )

    companies = pd.read_sql_query(
        "SELECT * FROM companies",
        conn
    )

    sectors = pd.read_sql_query(
        "SELECT * FROM sectors",
        conn
    )

    stock_prices = pd.read_sql_query(
        "SELECT * FROM stock_prices",
        conn
    )

    print("\nTables Loaded")
    print("-" * 30)

    print(
        "financial_ratios :",
        len(financial_ratios)
    )

    print(
        "companies :",
        len(companies)
    )

    print(
        "sectors :",
        len(sectors)
    )

    print(
        "stock_prices :",
        len(stock_prices)
    )

    return (
        financial_ratios,
        companies,
        sectors,
        stock_prices
    )

def prepare_master_dataframe():
    """
    Prepare the master DataFrame used by the Screener Engine.

    Steps:
    1. Connect to SQLite
    2. Load required tables
    3. Get latest stock price for each company
    4. Merge financial ratios, companies, sectors and prices
    5. Keep only the latest financial year per company
    6. Perform validation checks
    7. Return the final master DataFrame
    """

    conn = connect_db()

    (
        financial_ratios,
        companies,
        sectors,
        stock_prices
    ) = load_tables(conn)

    # -------------------------------------------------------
    # Latest available stock price for each company
    # -------------------------------------------------------

    latest_prices = (
        stock_prices
        .sort_values("date")
        .groupby("company_id", as_index=False)
        .tail(1)
    )

    # -------------------------------------------------------
    # Merge financial ratios with company master
    # -------------------------------------------------------

    master = financial_ratios.merge(
        companies,
        left_on="company_id",
        right_on="id",
        how="left",
        suffixes=("", "_company")
    )
    # -------------------------------------------------------
# Remove records that do not match a valid company
# -------------------------------------------------------

    master = master[
    master["company_name"].notna()
].copy()

    # -------------------------------------------------------
    # Merge sector information
    # -------------------------------------------------------

    master = master.merge(
        sectors,
        on="company_id",
        how="left"
    )
    # -------------------------------------------------------
# Keep latest financial year only
# -------------------------------------------------------

    master = (
    master
    .sort_values("year")
    .groupby("company_id", as_index=False)
    .tail(1)
    .reset_index(drop=True)
)

    # -------------------------------------------------------
    # Merge latest stock prices
    # -------------------------------------------------------

    master = master.merge(
        latest_prices,
        on="company_id",
        how="left",
        suffixes=("", "_price")
    )

    # -------------------------------------------------------
    # Sort records
    # -------------------------------------------------------

    master = (
        master
        .sort_values(
            ["company_id", "year"]
        )
        .reset_index(drop=True)
    )

    # -------------------------------------------------------
    # Keep latest financial year only
    # -------------------------------------------------------

    master = (
        master
        .sort_values("year")
        .groupby("company_id", as_index=False)
        .tail(1)
        .reset_index(drop=True)
    )

    # -------------------------------------------------------
    # Validation Summary
    # -------------------------------------------------------

    print()
    print("=" * 60)
    print("MASTER DATASET")
    print("=" * 60)

    print(f"Latest Company Records : {len(master)}")
    print(f"Columns               : {len(master.columns)}")

    print()

    print("Unique Company IDs")
    print("-" * 40)

    print(
        "financial_ratios :",
        financial_ratios["company_id"].nunique()
    )

    if "company_id" in companies.columns:
        print(
            "companies        :",
            companies["company_id"].nunique()
        )
    else:
        print(
            "companies        :",
            companies["id"].nunique()
        )

    print(
        "master           :",
        master["company_id"].nunique()
    )

    print()

    print("Duplicate Company IDs")
    print("-" * 40)

    duplicates = (
        master["company_id"]
        .value_counts()
    )

    duplicates = duplicates[
        duplicates > 1
    ]

    if duplicates.empty:
        print("No duplicate company IDs found.")
    else:
        print(duplicates)

    print()

    print("Available Columns")
    print("-" * 60)

    for column in sorted(master.columns):
        print(column)

    conn.close()

    return master
   

def apply_min_filter(df, column, minimum):
    """
    Keep rows where column >= minimum.
    Ignore filter if minimum is None.
    """

    if minimum is None:
        return df

    if column not in df.columns:
        print(f"[WARNING] Column '{column}' not found. Skipping filter.")
        return df

    before = len(df)

    df = df[df[column] >= minimum]

    after = len(df)

    print(f"{column} >= {minimum} : {before} -> {after}")

    return df

def apply_max_filter(df, column, maximum):
    """
    Keep rows where column <= maximum.
    """

    if maximum is None:
        return df

    if column not in df.columns:
        print(f"[WARNING] Column '{column}' not found. Skipping filter.")
        return df

    before = len(df)

    df = df[df[column] <= maximum]

    after = len(df)

    print(f"{column} <= {maximum} : {before} -> {after}")

    return df

def apply_debt_to_equity_filter(df, maximum):
    """
    Apply D/E filter.

    Financial companies always pass.
    """

    if maximum is None:
        return df

    before = len(df)

    financial_mask = (
        df["broad_sector"]
        == "Financials"
    )

    non_financial_mask = (
        ~financial_mask
    )

    filtered_non_financial = df[
        non_financial_mask
    ]

    filtered_non_financial = filtered_non_financial[
        filtered_non_financial["debt_to_equity"] <= maximum
    ]

    financial_df = df[
        financial_mask
    ]

    result = pd.concat(
        [
            financial_df,
            filtered_non_financial
        ]
    )

    after = len(result)

    print(f"D/E Filter : {before} -> {after}")

    return result

def apply_interest_coverage_filter(df, minimum):
    """
    Apply Interest Coverage filter.

    If icr_label exists:
        Debt Free companies always pass.

    Otherwise:
        Companies with NULL interest_coverage
        are treated as Debt Free.
    """

    if minimum is None:
        return df

    before = len(df)

    # Case 1: Sprint document implementation
    if "icr_label" in df.columns:

        debt_free = (
            df["icr_label"] == "Debt Free"
        )

    # Case 2: Your current database
    else:

        debt_free = (
            df["interest_coverage"].isna()
        )

    normal = ~debt_free

    filtered = df[normal]

    filtered = filtered[
        filtered["interest_coverage"] >= minimum
    ]

    result = pd.concat(
        [
            filtered,
            df[debt_free]
        ]
    )

    after = len(result)

    print(
        f"Interest Coverage Filter : {before} -> {after}"
    )

    return result

def apply_filters(df, config):
    """
    Apply all configured filters.
    """

    filters = config["filters"]

    # -------------------------------------------------
    # ROE
    # -------------------------------------------------

    df = apply_min_filter(
        df,
        "return_on_equity_pct",
        filters.get("roe_min")
    )

    # -------------------------------------------------
    # Debt to Equity
    # -------------------------------------------------

    df = apply_debt_to_equity_filter(
        df,
        filters.get("debt_to_equity_max")
    )

    # -------------------------------------------------
    # Free Cash Flow
    # -------------------------------------------------

    df = apply_min_filter(
        df,
        "free_cash_flow_cr",
        filters.get("free_cash_flow_min")
    )

    # -------------------------------------------------
    # Revenue CAGR
    # -------------------------------------------------

    df = apply_min_filter(
        df,
        "revenue_cagr_5yr",
        filters.get("revenue_cagr_5yr_min")
    )

    # -------------------------------------------------
    # PAT CAGR
    # -------------------------------------------------

    df = apply_min_filter(
        df,
        "pat_cagr_5yr",
        filters.get("pat_cagr_5yr_min")
    )

    # -------------------------------------------------
    # Operating Margin
    # -------------------------------------------------

    df = apply_min_filter(
        df,
        "operating_profit_margin_pct",
        filters.get("operating_profit_margin_min")
    )

    # -------------------------------------------------
    # Interest Coverage
    # -------------------------------------------------

    df = apply_interest_coverage_filter(
        df,
        filters.get("interest_coverage_min")
    )

   # -------------------------------------------------
# Metrics not available in current database
#
# These filters are intentionally skipped.
#
# They will be enabled when the database contains:
#
# - pe_ratio
# - pb_ratio
# - dividend_yield
# - market_cap
# - net_profit
# - sales
# -------------------------------------------------
    # -------------------------------------------------
    # EPS CAGR
    # -------------------------------------------------

    df = apply_min_filter(
        df,
        "eps_cagr_5yr",
        filters.get("eps_cagr_5yr_min")
    )

    # -------------------------------------------------
    # Asset Turnover
    # -------------------------------------------------

    df = apply_min_filter(
        df,
        "asset_turnover",
        filters.get("asset_turnover_min")
    )

    # -------------------------------------------------
    # Sales
    # -------------------------------------------------

    df = apply_min_filter(
        df,
        "sales",
        filters.get("sales_min")
    )

    return df

def sort_results(df, config):

    sorting = config["sorting"]

    return df.sort_values(

        sorting["column"],

        ascending=sorting["ascending"]

    )
if __name__ == "__main__":

    print("\n" + "=" * 60)
    print("SPRINT 3 - DAY 15 : FINANCIAL SCREENER ENGINE")
    print("=" * 60)

    # --------------------------------------------------
    # Load Configuration
    # --------------------------------------------------

    config = load_config()

    print("\nConfiguration loaded successfully.")

    # --------------------------------------------------
    # Prepare Master Data
    # --------------------------------------------------

    master = prepare_master_dataframe()

    print("\nMaster DataFrame prepared successfully.")

    # --------------------------------------------------
    # Apply Filters
    # --------------------------------------------------

    screened = apply_filters(
        master,
        config
    )

    print("\nFiltering completed successfully.")

    # --------------------------------------------------
    # Sort Results
    # --------------------------------------------------

    screened = sort_results(
        screened,
        config
    )

    print("\nSorting completed successfully.")

    # --------------------------------------------------
    # Display Summary
    # --------------------------------------------------

    print("\n" + "=" * 60)
    print("SCREENING SUMMARY")
    print("=" * 60)

    print(f"Total Companies Analysed : {len(master)}")
    print(f"Companies Passed         : {len(screened)}")

    if len(master) > 0:
        percentage = (len(screened) / len(master)) * 100
        print(f"Selection Rate           : {percentage:.2f}%")

    print("\nTop Screened Companies")
    print("-" * 60)

    display_columns = [
        "company_id",
        "company_name",
        "year",
        "return_on_equity_pct",
        "debt_to_equity",
        "free_cash_flow_cr",
        "revenue_cagr_5yr",
        "pat_cagr_5yr",
        "operating_profit_margin_pct",
        "interest_coverage",
        "asset_turnover",
        "composite_quality_score"
    ]

    available_columns = [
        col for col in display_columns
        if col in screened.columns
    ]

    print(
        screened[available_columns]
        .head(10)
        .to_string(index=False)
    )

    # --------------------------------------------------
    # Export Excel
    # --------------------------------------------------

    output_file = OUTPUT_PATH / "screener_output.xlsx"

    screened.to_excel(
        output_file,
        index=False
    )

    print("\n" + "=" * 60)
    print("EXPORT COMPLETED")
    print("=" * 60)

    print(f"Excel File : {output_file}")
    print(f"Rows Saved : {len(screened)}")

    print("\nDay 15 completed successfully.")