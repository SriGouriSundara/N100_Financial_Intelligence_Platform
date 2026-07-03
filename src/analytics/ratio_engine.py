"""
Sprint 2 - Day 12
Ratio Engine

This module reads financial data from SQLite,
calculates all KPIs using the analytics modules,
and populates the financial_ratios table.
"""
import sqlite3
import pandas as pd
from pathlib import Path

from src.analytics.ratios import *
from src.analytics.cagr import *
from src.analytics.cashflow_kpis import *
from src.etl.normaliser import normalize_year

DB_PATH = Path("db") / "nifty100.db"

def connect_db():
    """
    Create a connection to the SQLite database.
    """
    return sqlite3.connect(DB_PATH)

def load_source_tables(conn):
    """
    Load all required source tables from SQLite,
    normalize data, remove duplicates,
    and return clean DataFrames.
    """

    # -------------------------------
    # Load tables from SQLite
    # -------------------------------

    profit_df = pd.read_sql_query(
        "SELECT * FROM profitandloss",
        conn
    )

    balance_df = pd.read_sql_query(
        "SELECT * FROM balancesheet",
        conn
    )

    cashflow_df = pd.read_sql_query(
        "SELECT * FROM cashflow",
        conn
    )

    companies_df = pd.read_sql_query(
        "SELECT * FROM companies",
        conn
    )

    sectors_df = pd.read_sql_query(
        "SELECT * FROM sectors",
        conn
    )

    # -------------------------------
    # Display loaded rows
    # -------------------------------

    print("\nRows Loaded")
    print("-" * 25)
    print(f"Profit & Loss : {len(profit_df)}")
    print(f"Balance Sheet : {len(balance_df)}")
    print(f"Cash Flow     : {len(cashflow_df)}")
    print(f"Companies     : {len(companies_df)}")
    print(f"Sectors       : {len(sectors_df)}")

    # -------------------------------
    # Normalize year columns
    # -------------------------------

    profit_df["year"] = (
        profit_df["year"]
        .apply(normalize_year)
    )

    balance_df["year"] = (
        balance_df["year"]
        .apply(normalize_year)
    )

    cashflow_df["year"] = (
        cashflow_df["year"]
        .apply(normalize_year)
    )

    # Remove TTM rows (CAGR requires actual years)
    profit_df = profit_df[
        profit_df["year"] != "TTM"
    ]

    balance_df = balance_df[
        balance_df["year"] != "TTM"
    ]

    cashflow_df = cashflow_df[
        cashflow_df["year"] != "TTM"
    ]

    # Convert year to integer
    profit_df["year"] = profit_df["year"].astype(int)
    balance_df["year"] = balance_df["year"].astype(int)
    cashflow_df["year"] = cashflow_df["year"].astype(int)

    # -------------------------------
    # Remove duplicate company-year
    # -------------------------------

    profit_before = len(profit_df)
    balance_before = len(balance_df)
    cashflow_before = len(cashflow_df)

    profit_df = (
        profit_df
        .sort_values(["company_id", "year"])
        .drop_duplicates(
            subset=["company_id", "year"],
            keep="last"
        )
    )

    balance_df = (
        balance_df
        .sort_values(["company_id", "year"])
        .drop_duplicates(
            subset=["company_id", "year"],
            keep="last"
        )
    )

    cashflow_df = (
        cashflow_df
        .sort_values(["company_id", "year"])
        .drop_duplicates(
            subset=["company_id", "year"],
            keep="last"
        )
    )

    print("\nDuplicate Removal Summary")
    print("-" * 35)
    print(
        f"Profit & Loss : "
        f"{profit_before} -> {len(profit_df)}"
    )
    print(
        f"Balance Sheet : "
        f"{balance_before} -> {len(balance_df)}"
    )
    print(
        f"Cash Flow     : "
        f"{cashflow_before} -> {len(cashflow_df)}"
    )

    # -------------------------------
    # Sort all tables
    # -------------------------------

    profit_df = (
        profit_df
        .sort_values(
            ["company_id", "year"]
        )
        .reset_index(drop=True)
    )

    balance_df = (
        balance_df
        .sort_values(
            ["company_id", "year"]
        )
        .reset_index(drop=True)
    )

    cashflow_df = (
        cashflow_df
        .sort_values(
            ["company_id", "year"]
        )
        .reset_index(drop=True)
    )

    companies_df = (
        companies_df
        .sort_values("id")
        .reset_index(drop=True)
    )

    sectors_df = (
        sectors_df
        .sort_values("company_id")
        .reset_index(drop=True)
    )

    # -------------------------------
    # Validation
    # -------------------------------

    unique_keys = (
        pd.concat(
            [
                profit_df[["company_id", "year"]],
                balance_df[["company_id", "year"]],
                cashflow_df[["company_id", "year"]],
            ]
        )
        .drop_duplicates()
    )

    duplicate_keys = (
        profit_df
        .duplicated(
            subset=["company_id", "year"]
        )
        .sum()
    )
     # Return DataFrames

    return (
        profit_df,
        balance_df,
        cashflow_df,
        companies_df,
        sectors_df,
    )
def prepare_master_dataframe():
    """
    Build one master dataframe by combining all source tables.

    Steps:
    1. Load all source tables.
    2. Remove duplicate (company_id, year) records from each table.
    3. Build a master company-year key.
    4. Merge Profit & Loss, Balance Sheet, Cash Flow,
       Companies and Sectors.
    5. Return one clean dataframe for KPI calculations.
    """

    conn = connect_db()

    (
        profit_df,
        balance_df,
        cashflow_df,
        companies_df,
        sectors_df
    ) = load_source_tables(conn)

    # REMOVE DUPLICATE COMPANY-YEAR RECORDS
    profit_before = len(profit_df)
    balance_before = len(balance_df)
    cashflow_before = len(cashflow_df)

    profit_df = (
        profit_df
        .sort_values("id")
        .drop_duplicates(
            subset=["company_id", "year"],
            keep="last"
        )
    )

    balance_df = (
        balance_df
        .sort_values("id")
        .drop_duplicates(
            subset=["company_id", "year"],
            keep="last"
        )
    )

    cashflow_df = (
        cashflow_df
        .sort_values("id")
        .drop_duplicates(
            subset=["company_id", "year"],
            keep="last"
        )
    )
    # BUILD MASTER COMPANY-YEAR KEY
    keys = (
        pd.concat(
            [
                profit_df[["company_id", "year"]],
                balance_df[["company_id", "year"]],
                cashflow_df[["company_id", "year"]],
            ],
            ignore_index=True
        )
        .drop_duplicates()
        .sort_values(
            ["company_id", "year"]
        )
        .reset_index(drop=True)
    )

    print(f"\nUnique Company-Year Keys : {len(keys)}")

    # MERGE PROFIT & LOSS
    master_df = keys.merge(
        profit_df,
        on=["company_id", "year"],
        how="left",
        suffixes=("", "_pl")
    )

    # MERGE BALANCE SHEET
    master_df = master_df.merge(
        balance_df,
        on=["company_id", "year"],
        how="left",
        suffixes=("_pl", "_bs")
    )

    # MERGE CASH FLOW
    master_df = master_df.merge(
        cashflow_df,
        on=["company_id", "year"],
        how="left",
        suffixes=("", "_cf")
    )

    # MERGE COMPANIES
    master_df = master_df.merge(
        companies_df,
        left_on="company_id",
        right_on="id",
        how="left",
        suffixes=("", "_company")
    )

    # MERGE SECTORS
    master_df = master_df.merge(
        sectors_df,
        on="company_id",
        how="left",
        suffixes=("", "_sector")
    )
    
    # FINAL CLEANUP
    master_df = (
        master_df
        .sort_values(
            ["company_id", "year"]
        )
        .reset_index(drop=True)
    )

    duplicate_count = master_df.duplicated(
        subset=["company_id", "year"]
    ).sum()

    print(f"\nMaster Dataset Rows : {len(master_df)}")
    print(f"Duplicate Keys      : {duplicate_count}")

    conn.close()

    return master_df

def show_dataset_information(df):
    """
    Print dataset information.
    """

    print()
    print("=" * 60)
    print("MASTER DATASET")
    print("=" * 60)
    print("Rows :", len(df))
    print("Columns :", len(df.columns))
    print()
    print(df.head())
    print()
    print("=" * 60)

from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    return_on_equity,
    debt_to_equity,
    interest_coverage_ratio,
    asset_turnover,
)
###
from src.analytics.cashflow_kpis import (
    free_cash_flow,
    capex_intensity,
    fcf_conversion_rate,
)

from src.analytics.cagr import (
    revenue_cagr,
    pat_cagr,
    eps_cagr,
)

def calculate_kpis(df):
    """
    Calculate all financial KPIs for the financial_ratios table.
    """

    import numpy as np
    import pandas as pd

    # =====================================================
    # PROFITABILITY RATIOS
    # =====================================================

    df["net_profit_margin_pct"] = df.apply(
        lambda x: net_profit_margin(
            x["net_profit"],
            x["sales"]
        ),
        axis=1
    )

    df["operating_profit_margin_pct"] = df.apply(
        lambda x: operating_profit_margin(
            x["operating_profit"],
            x["sales"]
        ),
        axis=1
    )

    df["return_on_equity_pct"] = df.apply(
        lambda x: return_on_equity(
            x["net_profit"],
            x["equity_capital"],
            x["reserves"]
        ),
        axis=1
    )

    # =====================================================
    # LEVERAGE RATIOS
    # =====================================================

    df["debt_to_equity"] = df.apply(
        lambda x: debt_to_equity(
            x["borrowings"],
            x["equity_capital"],
            x["reserves"]
        ),
        axis=1
    )

    def safe_interest_coverage(
        operating_profit,
        other_income,
        interest
    ):

        if pd.isna(interest) or interest == 0:
            return np.nan

        operating_profit = (
            0 if pd.isna(operating_profit)
            else operating_profit
        )

        other_income = (
            0 if pd.isna(other_income)
            else other_income
        )

        return (
            operating_profit +
            other_income
        ) / interest

    df["interest_coverage"] = df.apply(
        lambda x: safe_interest_coverage(
            x["operating_profit"],
            x["other_income"],
            x["interest"]
        ),
        axis=1
    )

    df["asset_turnover"] = df.apply(
        lambda x: asset_turnover(
            x["sales"],
            x["total_assets"]
        ),
        axis=1
    )

    # =====================================================
    # CASH FLOW KPIs
    # =====================================================

    df["free_cash_flow_cr"] = df.apply(
        lambda x: free_cash_flow(
            x["operating_activity"],
            x["investing_activity"]
        ),
        axis=1
    )

    capex = df.apply(
        lambda x: capex_intensity(
            x["investing_activity"],
            x["sales"]
        ),
        axis=1
    )

    df["capex_cr"] = capex.apply(
        lambda x: x[0]
    )

    df["capex_label"] = capex.apply(
        lambda x: x[1]
    )

    df["cash_from_operations_cr"] = (
        df["operating_activity"]
    )

    df["total_debt_cr"] = (
        df["borrowings"]
    )

    # =====================================================
    # PER SHARE METRICS
    # =====================================================

    df["earnings_per_share"] = df["eps"]

    df["book_value_per_share"] = df["book_value"]

    df["dividend_payout_ratio_pct"] = (
        df["dividend_payout"]
    )

    # =====================================================
    # CAGR ENGINE
    # =====================================================

    def compute_cagr(
        dataframe,
        column,
        years=5
    ):

        dataframe = dataframe.copy()

        dataframe = dataframe.sort_values(
            ["company_id", "year"]
        )

        cagr_column = (
            f"{column}_cagr_{years}yr"
        )

        dataframe[cagr_column] = np.nan

        for company, group in dataframe.groupby(
            "company_id"
        ):

            group = group.sort_values("year")

            values = group.set_index("year")[column]

            for _, row in group.iterrows():

                current_year = row["year"]

                current_value = row[column]

                previous_year = (
                    current_year - years
                )

                if previous_year not in values.index:
                    continue

                previous_value = values.loc[
                    previous_year
                ]

                if (
                    pd.isna(previous_value)
                    or pd.isna(current_value)
                    or previous_value <= 0
                    or current_value <= 0
                ):
                    continue

                cagr = (
                    (
                        current_value /
                        previous_value
                    ) ** (1 / years) - 1
                ) * 100

                dataframe.loc[
                    (
                        dataframe["company_id"]
                        == company
                    )
                    &
                    (
                        dataframe["year"]
                        == current_year
                    ),
                    cagr_column
                ] = cagr

        return dataframe

    df = compute_cagr(
        df,
        "sales",
        5
    )

    df = compute_cagr(
        df,
        "net_profit",
        5
    )

    df = compute_cagr(
        df,
        "eps",
        5
    )

    # =====================================================
    # COMPOSITE QUALITY SCORE
    # =====================================================

    df["composite_quality_score"] = 0

    # ROE > 15%

    df.loc[
        df["return_on_equity_pct"] > 15,
        "composite_quality_score"
    ] += 1

    # Net Profit Margin > 10%

    df.loc[
        df["net_profit_margin_pct"] > 10,
        "composite_quality_score"
    ] += 1

    # Debt to Equity < 1

    df.loc[
        df["debt_to_equity"] < 1,
        "composite_quality_score"
    ] += 1

    # Interest Coverage > 3

    df.loc[
        df["interest_coverage"] > 3,
        "composite_quality_score"
    ] += 1

    # Asset Turnover > 1

    df.loc[
        df["asset_turnover"] > 1,
        "composite_quality_score"
    ] += 1

    return df

import sqlite3
import pandas as pd


def populate_financial_ratios(master_df):
    """
    Populate financial_ratios table with calculated KPIs.
    """

    print("\n[STEP] Populating financial_ratios table...\n")

    conn = connect_db()
    cursor = conn.cursor()

    # Remove existing rows so we don't create duplicates
    cursor.execute("DELETE FROM financial_ratios")

    rows_inserted = 0

    for _, row in master_df.iterrows():

        cursor.execute(
            """
            INSERT INTO financial_ratios (

                company_id,
                year,

                net_profit_margin_pct,
                operating_profit_margin_pct,
                return_on_equity_pct,

                debt_to_equity,
                interest_coverage,
                asset_turnover,

                free_cash_flow_cr,
                capex_cr,

                earnings_per_share,
                book_value_per_share,
                dividend_payout_ratio_pct,

                total_debt_cr,
                cash_from_operations_cr,

                revenue_cagr_5yr,
                pat_cagr_5yr,
                eps_cagr_5yr,

                composite_quality_score

            )

            VALUES
            (
                ?,?,?,?,?,?,
                ?,?,?,?,
                ?,?,?,?,
                ?,?,?,?,
                ?
            )
            """,

            (

                row["company_id"],
                int(row["year"]),

                row["net_profit_margin_pct"],
                row["operating_profit_margin_pct"],
                row["return_on_equity_pct"],

                row["debt_to_equity"],
                row["interest_coverage"],
                row["asset_turnover"],

                row["free_cash_flow_cr"],
                row["capex_cr"],

                row["earnings_per_share"],
                row["book_value_per_share"],
                row["dividend_payout_ratio_pct"],

                row["total_debt_cr"],
                row["cash_from_operations_cr"],

                row.get("sales_cagr_5yr"),
                row.get("net_profit_cagr_5yr"),
                row.get("eps_cagr_5yr"),

                row["composite_quality_score"]
            )

        )

        rows_inserted += 1

    conn.commit()

    print(f"Inserted Rows : {rows_inserted}")

    conn.close()

def main():
    """
    Main function to run the Ratio Engine (FIXED + DEBUG ENABLED)
    """

    print("\n[START] Running Ratio Engine...\n")

    # STEP 1: Build master dataset
    master_df = prepare_master_dataframe()

    # STEP 2: Show base dataset info
    show_dataset_information(master_df)

    # STEP 3: RUN KPI ENGINE
    print("\n[STEP] Calculating KPIs...\n")

    master_df = calculate_kpis(master_df)

    # 🔥 DEBUG CHECK (VERY IMPORTANT)
    print("\n" + "=" * 60)
    print("DEBUG: KPI ENGINE VALIDATION")
    print("=" * 60)

    print("\nInterest Coverage Sample:")
    print(
        master_df[[
            "company_id",
            "year",
            "interest_coverage"
        ]].head(10)
    )

    print("\nCAGR Columns Generated:")
    print([col for col in master_df.columns if "cagr" in col])

    print("\nSample CAGR Data (if exists):")
    cagr_cols = [col for col in master_df.columns if "cagr" in col]
    if cagr_cols:
        print(master_df[["company_id", "year"] + cagr_cols].head(10))
    else:
        print("❌ No CAGR columns found!")

    # STEP 4: KPI PREVIEW
    print("\n" + "=" * 60)
    print("FINAL KPI PREVIEW")
    print("=" * 60)

    preview_cols = [
        "company_id",
        "year",
        "net_profit_margin_pct",
        "operating_profit_margin_pct",
        "return_on_equity_pct",
        "debt_to_equity",
        "interest_coverage",
        "asset_turnover",
        "free_cash_flow_cr",
        "capex_cr",
        "earnings_per_share",
        "book_value_per_share",
        "dividend_payout_ratio_pct",
        "cash_from_operations_cr",
        "total_debt_cr",
    ]

    # SAFE COLUMN FILTER (avoids crash if missing)
    preview_cols = [c for c in preview_cols if c in master_df.columns]

    print(master_df[preview_cols].head(10))

    print("\n[END] Ratio Engine Completed Successfully\n")


if __name__ == "__main__":
    main()