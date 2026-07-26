"""
Sprint 2 - Day 11
Cash Flow KPI Engine
"""

import csv
from pathlib import Path
import pandas as pd
import re

def normalize_year(value):

    if pd.isna(value):
        return None

    value = str(value).strip()

    m = re.search(r"(19\d{2}|20\d{2})", value)
    if m:
        return int(m.group(1))

    m = re.search(r"-(\d{2})$", value)
    if m:
        yy = int(m.group(1))
        return 2000 + yy if yy < 50 else 1900 + yy

    return None

# ==========================================================
# FREE CASH FLOW
# ==========================================================

def free_cash_flow(operating_activity, investing_activity):
    """
    Formula:
    CFO + Investing Cash Flow

    Negative FCF is allowed.
    """
    return operating_activity + investing_activity

# ==========================================================
# CFO QUALITY SCORE
# ==========================================================

def cfo_quality_score(cfo_list, pat_list):
    """
    Calculates average CFO/PAT ratio over 5 years.

    Returns:
        average_ratio
        quality_label
    """

    ratios = []

    for cfo, pat in zip(cfo_list, pat_list):

        if pat == 0:
            return None, None

        ratios.append(cfo / pat)

    average = sum(ratios) / len(ratios)

    if average > 1:
        label = "High Quality"

    elif average >= 0.5:
        label = "Moderate"

    else:
        label = "Accrual Risk"

    return round(average, 2), label

# ==========================================================
# CAPEX INTENSITY
# ==========================================================

def capex_intensity(investing_activity, sales):

    if sales == 0:
        return None, None

    value = abs(investing_activity) / sales * 100

    if value < 3:
        label = "Asset Light"

    elif value <= 8:
        label = "Moderate"

    else:
        label = "Capital Intensive"

    return round(value, 2), label


# ==========================================================
# FCF CONVERSION
# ==========================================================

def fcf_conversion_rate(
    free_cash_flow_value,
    operating_profit
):

    if operating_profit == 0:
        return None

    return (
        free_cash_flow_value /
        operating_profit
    ) * 100


# ==========================================================
# CAPITAL ALLOCATION
# ==========================================================

def capital_allocation_pattern(
    cfo,
    cfi,
    cff,
    cfo_pat_ratio=0
):

    signs = (
        "+" if cfo >= 0 else "-",
        "+" if cfi >= 0 else "-",
        "+" if cff >= 0 else "-"
    )

    mapping = {

        ("+", "-", "-"):
            "Shareholder Returns"
            if cfo_pat_ratio > 1
            else "Reinvestor",

        ("+", "+", "-"):
            "Liquidating Assets",

        ("-", "+", "+"):
            "Distress Signal",

        ("-", "-", "+"):
            "Growth Funded by Debt",

        ("+", "+", "+"):
            "Cash Accumulator",

        ("-", "-", "-"):
            "Pre-Revenue",

        ("+", "-", "+"):
            "Mixed"

    }

    return signs, mapping.get(signs, "Unclassified")
def generate_historical_capital_allocation(
    cashflow,
    pnl
):

    print_header("Generating Historical Capital Allocation")

    rows = []

    # Company list (already filtered to master list in main())
    companies = sorted(
        cashflow["company_id"].astype(str).unique()
    )

    # Historical years
    years = sorted(
        cashflow["year"]
        .dropna()
        .astype(int)
        .unique()
    )

    for company in companies:

        company_cf = cashflow[
            cashflow["company_id"].astype(str) == company
        ]

        company_pl = pnl[
            pnl["company_id"].astype(str) == company
        ]

        for year in years:

            cf_year = company_cf[
                company_cf["year"] == year
            ]

            if cf_year.empty:
                continue

            pl_year = company_pl[
                company_pl["year"] == year
            ]

            cf_row = cf_year.iloc[0]

            cfo = cf_row["operating_activity"]
            cfi = cf_row["investing_activity"]
            cff = cf_row["financing_activity"]

            # Skip incomplete records
            if (
                pd.isna(cfo)
                or pd.isna(cfi)
                or pd.isna(cff)
            ):
                continue

            pat = 0

            if (
                not pl_year.empty
                and pd.notna(pl_year.iloc[0]["net_profit"])
            ):
                pat = pl_year.iloc[0]["net_profit"]

            ratio = 0

            if (
                pd.notna(pat)
                and pat != 0
            ):
                ratio = cfo / pat

            signs, label = capital_allocation_pattern(
                cfo,
                cfi,
                cff,
                ratio
            )

            rows.append([
                company,
                year,
                signs[0],
                signs[1],
                signs[2],
                label
            ])

    print(f"Companies : {len(companies)}")
    print(f"Years     : {len(years)}")
    print(f"Rows      : {len(rows)}")

    export_capital_allocation(rows)

    print("Saved -> capital_allocation.csv")

# ==========================================================
# EXPORT CSV
# ==========================================================

def export_capital_allocation(
    rows,
    output_file="output/capital_allocation.csv"
):

    Path("output").mkdir(exist_ok=True)

    with open(
        output_file,
        "w",
        newline="",
        encoding="utf-8"
    ) as csvfile:

        writer = csv.writer(csvfile)

        writer.writerow([
            "company_id",
            "year",
            "cfo_sign",
            "cfi_sign",
            "cff_sign",
            "pattern_label"
        ])

        writer.writerows(rows)
"""
Bluestock N100 Financial Intelligence Platform
Sprint 5
Day 31
Cash Flow Intelligence Module
"""

import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

# PROJECT PATHS
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DB_PATH = PROJECT_ROOT / "db" / "nifty100.db"

OUTPUT_DIR = PROJECT_ROOT / "output"

OUTPUT_DIR.mkdir(exist_ok=True)

EXCEL_OUTPUT = OUTPUT_DIR / "cashflow_intelligence.xlsx"

DISTRESS_OUTPUT = OUTPUT_DIR / "distress_alerts.csv"
# PRINT HELPERS
def print_header(title):

    print("\n" + "=" * 60)

    print(title)

    print("=" * 60)
# DATABASE
def connect_database():

    print_header("Connecting Database")

    if not DB_PATH.exists():

        raise FileNotFoundError(DB_PATH)

    conn = sqlite3.connect(DB_PATH)

    print("Database Connected")

    return conn
def load_companies(conn):

    print_header("Loading Companies")

    df = pd.read_sql_query(
        "SELECT * FROM companies",
        conn
    )

    print(f"Companies : {len(df)}")

    return df
def load_cashflow(conn):
    print_header("Loading Cash Flow")
    df = pd.read_sql_query(
        "SELECT * FROM cashflow",
        conn
    )
    print(f"Cash Flow Rows : {len(df)}")
    return df

def load_profit_loss(conn):
    print_header("Loading Profit & Loss")
    df = pd.read_sql_query(
        "SELECT * FROM profitandloss",
        conn
    )
    print(f"P&L Rows : {len(df)}")
    return df

def load_ratios(conn):

    print_header("Loading Financial Ratios")

    df = pd.read_sql_query(
        "SELECT * FROM financial_ratios",
        conn
    )

    print(f"Ratio Rows : {len(df)}")

    return df
# LOAD SECTORS
# ==========================================================
def load_sectors(connection):

    print_header("Loading Sectors")

    query = "SELECT * FROM sectors"

    sectors = pd.read_sql(query, connection)

    print(f"Sector Rows : {len(sectors)}")

    return sectors
# LATEST YEAR
def latest_year(df):

    latest = (

        df

        .sort_values(
            ["company_id", "year"]
        )

        .drop_duplicates(
            subset=["company_id"],
            keep="last"
        )

        .reset_index(drop=True)
    )
    return latest
# COMPANY CONSISTENCY CHECK
def compare_company_ids(companies, df, table_name):

    print_header(f"Company Validation - {table_name}")

    master_ids = set(companies["id"].astype(str))

    table_ids = set(df["company_id"].astype(str))

    extra = sorted(table_ids - master_ids)

    missing = sorted(master_ids - table_ids)

    print(f"Companies table : {len(master_ids)}")
    print(f"{table_name} : {len(table_ids)}")

    print()

    print(f"Extra IDs : {len(extra)}")

    if extra:

        print(extra)

    print()

    print(f"Missing IDs : {len(missing)}")

    if missing:

        print(missing)
# CFO QUALITY ENGINE
def calculate_cfo_quality(cashflow, pnl):

    print_header("Calculating CFO Quality")

    merged = pd.merge(
        cashflow,
        pnl[
            [
                "company_id",
                "year",
                "net_profit"
            ]
        ],
        on=[
            "company_id",
            "year"
        ],
        how="left"
    )

    results = []

    for company, history in merged.groupby("company_id"):

        history = (
            history
            .sort_values("year")
            .tail(5)
        )

        ratios = []

        for _, row in history.iterrows():

            cfo = row["operating_activity"]

            pat = row["net_profit"]

            ratio = safe_divide(cfo, pat)

            if pd.notna(ratio):
                ratios.append(ratio)

        score = np.mean(ratios) if len(ratios) else np.nan

        label = cfo_quality_label(score)

        results.append(
            {
                "company_id": company,
                "cfo_quality_score": round(score, 2)
                if pd.notna(score)
                else np.nan,
                "cfo_quality_label": label,
            }
        )

    quality = pd.DataFrame(results)

    print(f"CFO Quality Records : {len(quality)}")

    return quality
# OUTPUT CONTAINERS
def initialise_results():

    intelligence_rows = []

    distress_rows = []

    return intelligence_rows, distress_rows
# SAVE OUTPUTS
# ==========================================================
def save_excel(df):

    with pd.ExcelWriter(

        EXCEL_OUTPUT,

        engine="openpyxl"

    ) as writer:

        df.to_excel(

            writer,

            sheet_name="CashFlow",

            index=False

        )

    print(f"Saved -> {EXCEL_OUTPUT.name}")
def save_distress(df):
    """
    Save Distress Alerts CSV.
    """

    df.to_csv(
        DISTRESS_OUTPUT,
        index=False,
    )

    print(f"Saved -> {DISTRESS_OUTPUT.name}")
    # ==========================================================
# DAY 31 VALIDATION
# ==========================================================

def validate_outputs(capital_df, distress_df):

    print_header("DAY 31 VALIDATION")

    required_columns = [

        "company_id",

        "sector",

        "cfo_quality_score",

        "cfo_quality_label",

        "capex_intensity_pct",

        "capex_label",

        "fcf_cagr_5yr",

        "fcf_conversion_pct",

        "distress_flag",

        "deleveraging_flag",

        "capital_allocation_label"

    ]

    print("Checking cashflow_intelligence.xlsx")

    print("------------------------------------")

    print(f"Rows Found : {len(capital_df)}")

    if len(capital_df) == 92:

        print("✓ Row Count Correct")

    else:

        print("✗ Expected 92 rows")

    print("\nChecking Required Columns")

    missing = [

        col

        for col in required_columns

        if col not in capital_df.columns

    ]

    if len(missing) == 0:

        print("✓ All Required Columns Present")

    else:

        print("✗ Missing Columns:")

        for col in missing:

            print(col)

    print("\nChecking Labels")

    print("--------------------")

    print(

        "High Quality :", 

        (capital_df["cfo_quality_label"] == "High Quality").sum()

    )

    print(

        "Moderate :", 

        (capital_df["cfo_quality_label"] == "Moderate").sum()

    )

    print(

        "Accrual Risk :", 

        (capital_df["cfo_quality_label"] == "Accrual Risk").sum()

    )

    print(

        "Asset Light :", 

        (capital_df["capex_label"] == "Asset Light").sum()

    )

    print(

        "Moderate :", 

        (capital_df["capex_label"] == "Moderate").sum()

    )

    print(

        "Capital Intensive :", 

        (capital_df["capex_label"] == "Capital Intensive").sum()

    )

    print("\nChecking Deleveraging")

    print("-------------------------")

    print(

        capital_df["deleveraging_flag"].value_counts(dropna=False)

    )

    print("\nChecking Distress Alerts")

    print("-------------------------")

    print(f"Alerts Generated : {len(distress_df)}")

    if DISTRESS_OUTPUT.exists():

        print("✓ distress_alerts.csv exists")

    else:

        print("✗ distress_alerts.csv missing")

    if EXCEL_OUTPUT.exists():

        print("✓ cashflow_intelligence.xlsx exists")

    else:

        print("✗ cashflow_intelligence.xlsx missing")

    print_header("VALIDATION COMPLETE")

# UTILITIES
def safe_divide(a, b):
    if pd.isna(a) or pd.isna(b):
        return np.nan
    if b == 0:
        return np.nan
    return a / b
# CFO QUALITY LABEL
def cfo_quality_label(score):

    if pd.isna(score):
        return "Unknown"

    if score > 1.0:
        return "High Quality"

    if score >= 0.5:
        return "Moderate"

    return "Accrual Risk"
# CAPEX LABEL
def capex_label(value):

    if pd.isna(value):
        return "Unknown"

    if value < 3:
        return "Asset Light"

    if value <= 8:
        return "Moderate"

    return "Capital Intensive"
# CAPITAL ALLOCATION LABEL
# ==========================================================
def capital_allocation_label(fcf_conversion, fcf_cagr):

    if pd.isna(fcf_conversion):

        return "Unknown"

    # If CAGR cannot be calculated because of
    # negative/zero FCF values, still classify
    if pd.isna(fcf_cagr):

        if fcf_conversion >= 80:
            return "Good"

        elif fcf_conversion >= 50:
            return "Average"

        else:
            return "Weak"

    if fcf_conversion >= 80 and fcf_cagr >= 15:
        return "Excellent"

    elif fcf_conversion >= 50 and fcf_cagr >= 8:
        return "Good"

    elif fcf_conversion >= 25:
        return "Average"

    return "Weak"
# CAGR
# ==========================================================
def calculate_cagr(start_value, end_value, years):

    if years <= 0:
        return np.nan

    if pd.isna(start_value) or pd.isna(end_value):
        return np.nan

    # CAGR is not meaningful if start or end is <= 0
    if start_value <= 0 or end_value <= 0:
        return np.nan

    return (
        (end_value / start_value) ** (1 / years) - 1
    ) * 100

# CAPEX INTELLIGENCE

def calculate_capex_intensity(cashflow, pnl):

    print_header("Calculating CapEx Intensity")

    cash = cashflow.copy()

    pl = pnl.copy()
    # Detect Investing Activity column
    investing_column = None

    possible_investing = [
    "investing_activity",
    "cash_from_investing_activity",
    "cash_from_investing_activities",
    "investing_cash_flow"
]
    for col in possible_investing:
        if col in cash.columns:
            investing_column = col
            break

    if investing_column is None:
        raise ValueError(
            "Investing Activity column not found."
        )
    # Detect Revenue column
    # ---------------------------------------------

    revenue_column = None

    possible_revenue = [

        "sales",
        "sales_cr",
        "revenue",
        "revenue_cr",
        "total_revenue"

    ]

    for col in possible_revenue:

        if col in pl.columns:
            revenue_column = col
            break

    if revenue_column is None:
        raise ValueError(
            "Revenue column not found."
        )
    # Merge Cash Flow & P&L
    # ---------------------------------------------

    merged = cash.merge(

        pl[
            [
                "company_id",
                "year",
                revenue_column
            ]
        ],

        on=[
            "company_id",
            "year"
        ],

        how="left"

    )
    # CapEx Intensity
    # ---------------------------------------------
    merged["capex_intensity_pct"] = (
        merged[investing_column].abs()
        /
        merged[revenue_column]

    ) * 100
    # Latest Year Only
    # ---------------------------------------------
    latest = latest_year(merged)
    latest = latest[
        [
            "company_id",
            "capex_intensity_pct"
        ]
    ].copy()
    latest["capex_label"] = (
        latest["capex_intensity_pct"]
        .apply(capex_label)
    )
    print(
        f"CapEx Records : {len(latest)}"
    )
    return latest
# CFO / PAT Ratio
# ---------------------------------------------

    merged["cfo_pat_ratio"] = merged.apply(

        lambda row: safe_divide(

            row["operating_activity"],

            row["net_profit"]

        ),

        axis=1

    )
# Five-Year Average
# ---------------------------------------------

    summary = (

        merged

        .groupby("company_id")

        .agg(

            cfo_quality_score=(

                "cfo_pat_ratio",

                "mean"

            )

        )

        .reset_index()

    )

# Labels
# ---------------------------------------------

    summary["cfo_quality_label"] = summary[
        "cfo_quality_score"
    ].apply(cfo_quality_label)

    print(
        f"CFO Quality Records : {len(summary)}"
    )

    return summary
# Detect PAT column
# -----------------------------------------------

    pat_column = None

    possible_pat = [

        "net_profit",
        "net_profit_cr",
        "profit_after_tax",
        "pat"

    ]

    for col in possible_pat:

        if col in pl.columns:

            pat_column = col

            break

    if pat_column is None:

        raise ValueError(
            "PAT column not found."
        )
# Merge
# -----------------------------------------------

    merged = cash.merge(

        pl[

            [

                "company_id",

                "year",

                pat_column

            ]

        ],

        on=[

            "company_id",

            "year"

        ],

        how="left"

    )
# CFO / PAT
# -----------------------------------------------

    merged["cfo_pat_ratio"] = merged.apply(

        lambda row:

        safe_divide(

            row[cfo_column],

            row[pat_column]

        ),

        axis=1

    )
# Average 5-year score
# -----------------------------------------------

    summary = (

        merged

        .groupby("company_id")

        .agg(

            cfo_quality_score=(

                "cfo_pat_ratio",

                "mean"

            )

        )

        .reset_index()

    )

    summary["cfo_quality_label"] = summary[
        "cfo_quality_score"
    ].apply(cfo_quality_label)

    print(

        f"CFO Quality Records : {len(summary)}"

    )

    return summary
# DISTRESS & DELEVERAGING ENGINE
# ==========================================================

def calculate_distress_signals(cashflow, pnl):

    print_header("Calculating Distress & Deleveraging")

    cash = cashflow.copy()
    profit = pnl.copy()
    # Detect required columns
    # ------------------------------------------------------

    cfo_column = None
    cff_column = None
    borrowings_column = None

    cfo_candidates = [

    "operating_activity",
    "cash_from_operating_activity",
    "cash_from_operations",
    "operating_cash_flow",
    "cash_from_operating_activities",
    "cfo"
]
    cff_candidates = [
    "financing_activity",
    "cash_from_financing_activity",
    "cash_from_financing_activities",
    "financing_cash_flow",
    "cff"
]

    borrowing_candidates = [
        "borrowings",
        "total_borrowings",
        "borrowings_cr",
        "debt"
    ]

    for col in cfo_candidates:
        if col in cash.columns:
            cfo_column = col
            break

    for col in cff_candidates:
        if col in cash.columns:
            cff_column = col
            break

    for col in borrowing_candidates:
        if col in cash.columns:
            borrowings_column = col
            break

    if cfo_column is None:
        raise ValueError("Operating Cash Flow column not found.")

    if cff_column is None:
        raise ValueError("Financing Cash Flow column not found.")
    # Detect Net Profit column
    # ------------------------------------------------------

    profit_column = None

    for col in [
        "net_profit",
        "net_profit_cr",
        "profit_after_tax",
        "pat"
    ]:
        if col in profit.columns:
            profit_column = col
            break

    if profit_column is None:
        raise ValueError("Net Profit column not found.")
    # Merge
    # ------------------------------------------------------

    merged = cash.merge(

        profit[
            [
                "company_id",
                "year",
                profit_column
            ]
        ],

        on=[
            "company_id",
            "year"
        ],

        how="left"

    )

    latest = latest_year(merged)

    intelligence = []
    distress = []
    # Loop company-wise
    # ------------------------------------------------------

    for _, row in latest.iterrows():

        company = row["company_id"]
        history = (
            merged[
                merged["company_id"] == company
            ]
            .sort_values("year")
        )

        distress_flag = False
        deleveraging_flag = False
        # Distress
        # ----------------------------------------------

        if (
            row[cfo_column] < 0
            and
            row[cff_column] > 0
        ):

            distress_flag = True
        # Deleveraging
        # ----------------------------------------------

        if borrowings_column is not None:

            if len(history) >= 2:

                last2 = history.tail(2)

                borrow = last2[
                    borrowings_column
                ].tolist()

                if (
                    row[cff_column] < 0
                    and
                    borrow[0] > borrow[1]
                ):

                    deleveraging_flag = True

        intelligence.append(

            {

                "company_id": company,

                "distress_flag": distress_flag,

                "deleveraging_flag": deleveraging_flag

            }

        )

        if distress_flag:

            distress.append(

                {

                    "company_id": company,

                    "cfo_value": row[cfo_column],

                    "cff_value": row[cff_column],

                    "latest_net_profit": row[profit_column],

                    "distress_flag": True

                }

            )

    intelligence_df = pd.DataFrame(intelligence)

    distress_df = pd.DataFrame(distress)

    print(f"Companies Analysed : {len(intelligence_df)}")
    print(f"Distress Alerts    : {len(distress_df)}")
    return intelligence_df, distress_df
# CAPITAL ALLOCATION INTELLIGENCE
# ==========================================================

def calculate_capital_allocation(
    cashflow,
    pnl,
    ratios,
    sectors,
    cfo_quality,
    capex,
    distress
):

    print_header("Capital Allocation Intelligence")

    latest_ratio = latest_year(ratios)

    latest_cash = latest_year(cashflow)

    latest_pnl = latest_year(pnl)
    sector_lookup = {}

    if "company_id" in sectors.columns:

     sector_column = None

    for col in sectors.columns:

        if "sector" in col.lower():

            sector_column = col

            break

    if sector_column:

        sector_lookup = dict(

            zip(

                sectors["company_id"],

                sectors[sector_column]

            )
        )
        records = []

    for _, ratio in latest_ratio.iterrows():

        company = ratio["company_id"]

        # -----------------------------------------
        # Cash Flow History
        # -----------------------------------------
        cash_history = (
            cashflow[
                cashflow["company_id"] == company
            ]
            .sort_values("year")
            .copy()
        )


        # -----------------------------------------
        # Calculate Free Cash Flow
        # -----------------------------------------
        cash_history["free_cash_flow"] = (
            cash_history["operating_activity"]
            +
            cash_history["investing_activity"]
        )


        cash_history = cash_history[
            cash_history["free_cash_flow"].notna()
        ]


        # -----------------------------------------
        # FCF CAGR
        # -----------------------------------------
        fcf_cagr = np.nan


        if len(cash_history) >= 2:

            first = cash_history.iloc[0]["free_cash_flow"]

            last = cash_history.iloc[-1]["free_cash_flow"]

            years = len(cash_history) - 1


            if years > 0:

                fcf_cagr = calculate_cagr(
                    first,
                    last,
                    years
                )


        # -----------------------------------------
        # FCF Conversion
        # -----------------------------------------
        conversion = np.nan


        latest_cf = latest_cash[
            latest_cash["company_id"] == company
        ]


        latest_profit = latest_pnl[
            latest_pnl["company_id"] == company
        ]


        if (
            not latest_cf.empty
            and
            not latest_profit.empty
        ):

            cfo = latest_cf.iloc[0].get(
                "operating_activity",
                np.nan
            )


            pat = latest_profit.iloc[0].get(
                "net_profit",
                np.nan
            )


            if (
                pd.notna(cfo)
                and
                pd.notna(pat)
                and
                pat != 0
            ):

                conversion = (
                    cfo / pat
                ) * 100



        # -----------------------------------------
        # Capital Allocation Label
        # -----------------------------------------
        label = capital_allocation_label(
            conversion,
            fcf_cagr
        )


        # -----------------------------------------
        # Lookup Existing Results
        # -----------------------------------------
        cfo_row = cfo_quality[
            cfo_quality["company_id"] == company
        ]


        capex_row = capex[
            capex["company_id"] == company
        ]


        distress_row = distress[
            distress["company_id"] == company
        ]


        # -----------------------------------------
        # Append Company Record
        # -----------------------------------------
        records.append(

            {

                "company_id": company,


                "sector": sector_lookup.get(
                    company,
                    "Unknown"
                ),


                "cfo_quality_score":

                    cfo_row.iloc[0]["cfo_quality_score"]

                    if not cfo_row.empty

                    else np.nan,


                "cfo_quality_label":

                    cfo_row.iloc[0]["cfo_quality_label"]

                    if not cfo_row.empty

                    else "Unknown",


                "capex_intensity_pct":

                    capex_row.iloc[0]["capex_intensity_pct"]

                    if not capex_row.empty

                    else np.nan,


                "capex_label":

                    capex_row.iloc[0]["capex_label"]

                    if not capex_row.empty

                    else "Unknown",


                "fcf_cagr_5yr":
                    fcf_cagr,


                "fcf_conversion_pct":
                    conversion,


                "distress_flag":

                    distress_row.iloc[0]["distress_flag"]

                    if not distress_row.empty

                    else False,


                "deleveraging_flag":

                    distress_row.iloc[0]["deleveraging_flag"]

                    if not distress_row.empty

                    else False,


                "capital_allocation_label":
                    label

            }

        )
    result = pd.DataFrame(records)
    print(
    f"Capital Allocation Records : {len(result)}"
)
    return result
# MAIN
def main():

    print_header("Sprint 5 CASH FLOW-KPI'S")

    # ======================================================
    # CONNECT DATABASE
    # ======================================================

    connection = connect_database()

    # ======================================================
    # LOAD TABLES
    # ======================================================

    companies = load_companies(connection)
    sectors = load_sectors(connection)
    cashflow = load_cashflow(connection)
    pnl = load_profit_loss(connection)
    ratios = load_ratios(connection)

    # ======================================================
    # NORMALIZE YEARS
    # ======================================================

    cashflow["year"] = cashflow["year"].apply(normalize_year)
    pnl["year"] = pnl["year"].apply(normalize_year)

    cashflow = cashflow.dropna(subset=["year"])
    pnl = pnl.dropna(subset=["year"])

    cashflow["year"] = cashflow["year"].astype(int)
    pnl["year"] = pnl["year"].astype(int)

    # ======================================================
    # FILTER TO MASTER 92 COMPANIES
    # ======================================================

    master_ids = set(
        companies["id"].astype(str)
    )

    cashflow = cashflow[
        cashflow["company_id"].astype(str).isin(master_ids)
    ].copy()

    pnl = pnl[
        pnl["company_id"].astype(str).isin(master_ids)
    ].copy()

    ratios = ratios[
        ratios["company_id"].astype(str).isin(master_ids)
    ].copy()

    sectors = sectors[
        sectors["company_id"].astype(str).isin(master_ids)
    ].copy()

    # ======================================================
    # HISTORICAL CAPITAL ALLOCATION (SPRINT 2)
    # ======================================================

    generate_historical_capital_allocation(
        cashflow,
        pnl
    )

    # ======================================================
    # LATEST YEAR DATA
    # ======================================================

    latest_cf = latest_year(cashflow)
    latest_ratios = latest_year(ratios)

    # ======================================================
    # DAY 31
    # CFO QUALITY
    # ======================================================

    cfo_quality = calculate_cfo_quality(
        cashflow,
        pnl
    )

    # ======================================================
    # CAPEX INTENSITY
    # ======================================================

    capex = calculate_capex_intensity(
        cashflow,
        pnl
    )

    # ======================================================
    # DISTRESS & DELEVERAGING
    # ======================================================

    distress_flags, distress_alerts = calculate_distress_signals(
        cashflow,
        pnl
    )

    # ======================================================
    # CAPITAL ALLOCATION INTELLIGENCE
    # ======================================================

    capital = calculate_capital_allocation(
        cashflow,
        pnl,
        ratios,
        sectors,
        cfo_quality,
        capex,
        distress_flags
    )

    # ======================================================
    # SAVE OUTPUTS
    # ======================================================

    save_excel(capital)

    save_distress(
        distress_alerts
    )

    validate_outputs(
        capital,
        distress_alerts
    )

    # ======================================================
    # SUMMARY
    # ======================================================

    print_header("DAY 31 COMPLETED")

    print(f"Companies               : {len(companies)}")
    print(f"CFO Quality Records     : {len(cfo_quality)}")
    print(f"CapEx Records           : {len(capex)}")
    print(f"Distress Analysis       : {len(distress_flags)}")
    print(f"Distress Alerts         : {len(distress_alerts)}")
    print(f"Capital Allocation      : {len(capital)}")

    print("\nGenerated Files")
    print(f"✓ {EXCEL_OUTPUT.name}")
    print(f"✓ {DISTRESS_OUTPUT.name}")

    connection.close()


if __name__ == "__main__":
    main()