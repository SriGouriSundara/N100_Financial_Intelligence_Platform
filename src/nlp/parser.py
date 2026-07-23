"""
===========================================================
Bluestock N100 Financial Intelligence Platform
Sprint 5 - Day 29
NLP Analysis Text Parser
===========================================================

Purpose
-------
1. Read analysis.xlsx
2. Parse CAGR related text using Regex
3. Generate analysis_parsed.csv
4. Generate parse_failures.csv
5. Compare parsed values with Ratio Engine
6. Flag large differences (>5%)

Author : Your Team
"""

import re
import sqlite3
from pathlib import Path

import pandas as pd

# ==========================================================
# PROJECT PATHS
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "output"
DB_DIR = PROJECT_ROOT / "db"

ANALYSIS_FILE = DATA_DIR / "raw" / "analysis.xlsx"
DATABASE_FILE = DB_DIR / "nifty100.db"

OUTPUT_DIR.mkdir(exist_ok=True)

PARSED_OUTPUT = OUTPUT_DIR / "analysis_parsed.csv"
FAILURE_OUTPUT = OUTPUT_DIR / "parse_failures.csv"
VALIDATION_OUTPUT = OUTPUT_DIR / "cagr_validation.csv"

# ==========================================================
# REGEX
# ==========================================================

REGEX_PATTERN = re.compile(
    r"(\d+)\s*Years?:?\s*(-?[\d.]+)%",
    re.IGNORECASE,
)

# ==========================================================
# TARGET COLUMNS
# ==========================================================

TARGET_FIELDS = [
    "compounded_sales_growth",
    "compounded_profit_growth",
    "stock_price_cagr",
    "roe",
]

# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def print_header(title: str):
    """Pretty console header"""

    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def safe_string(value):
    """
    Convert None / NaN into empty string.
    """

    if pd.isna(value):
        return ""

    return str(value).strip()


def parse_text(text):
    """
    Parse text like

    10 Years: 21%

    Returns

    period = 10
    value = 21.0

    Returns None if parsing fails.
    """

    text = safe_string(text)

    if text == "":
        return None

    match = REGEX_PATTERN.search(text)

    if match is None:
        return None

    period = int(match.group(1))
    value = float(match.group(2))

    return {
        "period_years": period,
        "value_pct": value,
    }


def load_analysis_file():
    """
    Read analysis.xlsx
    """

    print_header("Loading Analysis Excel")

    if not ANALYSIS_FILE.exists():
        raise FileNotFoundError(
            f"\nAnalysis file not found:\n{ANALYSIS_FILE}"
        )

    # Read Excel (skip the title row)
    df = pd.read_excel(
        ANALYSIS_FILE,
        header=1
    )

    print(f"Rows Loaded : {len(df)}")
    print(f"Columns     : {len(df.columns)}")

    print("\nDetected Columns:\n")
    for column in df.columns:
        print(column)

    return df

def initialise_output_lists():
    """
    Create empty containers
    """

    parsed_rows = []

    failed_rows = []

    validation_rows = []

    return (
        parsed_rows,
        failed_rows,
        validation_rows,
    )


def save_dataframe(df, path):
    """
    Save CSV.
    """

    df.to_csv(path, index=False)

    print(f"Saved -> {path.name}")
# ==========================================================
# PARSING ENGINE
# ==========================================================

def parse_analysis_data(df):
    """
    Parse all target fields from analysis.xlsx.

    Returns
    -------
    parsed_df
        Successfully parsed records

    failed_df
        Records that failed regex parsing
    """

    print_header("Parsing Analysis Text")

    parsed_rows, failed_rows, validation_rows = initialise_output_lists()

    total_cells = 0
    parsed_cells = 0
    failed_cells = 0

    for _, row in df.iterrows():

        company_id = safe_string(row["company_id"])

        for metric in TARGET_FIELDS:

            total_cells += 1

            raw_text = safe_string(row.get(metric, ""))

            result = parse_text(raw_text)

            if result is None:

                failed_cells += 1

                failed_rows.append(
                    {
                        "company_id": company_id,
                        "metric_type": metric,
                        "original_text": raw_text,
                        "reason": "Regex Pattern Not Matched",
                    }
                )

                continue

            parsed_cells += 1

            parsed_rows.append(
                {
                    "company_id": company_id,
                    "metric_type": metric,
                    "period_years": result["period_years"],
                    "value_pct": result["value_pct"],
                }
            )

    print("\nParsing Summary")
    print("-------------------------")
    print(f"Total Cells   : {total_cells}")
    print(f"Parsed        : {parsed_cells}")
    print(f"Failed        : {failed_cells}")

    parsed_df = pd.DataFrame(parsed_rows)

    failed_df = pd.DataFrame(failed_rows)

    return parsed_df, failed_df
# ==========================================================
# SAVE OUTPUT FILES
# ==========================================================

def generate_output_files(parsed_df, failed_df):
    """
    Save parser outputs.
    """

    print_header("Saving CSV Files")

    save_dataframe(parsed_df, PARSED_OUTPUT)

    save_dataframe(failed_df, FAILURE_OUTPUT)

    print("\nOutput Summary")
    print("-----------------------")
    print(f"Parsed Records : {len(parsed_df)}")
    print(f"Failed Records : {len(failed_df)}")
# ==========================================================
# DATABASE
# ==========================================================

def connect_database():
    """
    Connect to SQLite database.
    """

    print_header("Connecting SQLite")

    if not DATABASE_FILE.exists():
        raise FileNotFoundError(
            f"Database not found:\n{DATABASE_FILE}"
        )

    conn = sqlite3.connect(DATABASE_FILE)

    print("Connected Successfully")

    return conn
def load_financial_ratios(conn):
    """
    Read Ratio Engine output.
    """

    print_header("Loading financial_ratios")

    query = """
    SELECT
        company_id,
        year,
        revenue_cagr_5yr,
        pat_cagr_5yr,
        return_on_equity_pct
    FROM financial_ratios
    """

    ratios = pd.read_sql_query(query, conn)

    print(f"Rows Loaded : {len(ratios)}")

    return ratios

# ==========================================================
# METRIC MAPPING
# ==========================================================

def metric_to_database_column(metric):
    """
    Match parser metric names
    with Ratio Engine columns.
    """

    mapping = {

        "compounded_sales_growth":
            "revenue_cagr_5yr",

        "compounded_profit_growth":
            "pat_cagr_5yr",

        "roe":
            "return_on_equity_pct",

        # stock price CAGR
        # no equivalent in financial_ratios

        "stock_price_cagr":
            None,
    }

    return mapping.get(metric)
# ==========================================================
# CROSS VALIDATION
# ==========================================================

def validate_parsed_values(parsed_df, ratios_df):

    print_header("Cross Validation")

    validation_rows = []

    latest = (
        ratios_df
        .sort_values("year")
        .groupby("company_id")
        .tail(1)
    )

    for _, row in parsed_df.iterrows():

        company = row["company_id"]

        metric = row["metric_type"]

        parsed_value = row["value_pct"]

        db_column = metric_to_database_column(metric)

        if db_column is None:
            continue

        match = latest[
            latest["company_id"] == company
        ]

        if match.empty:
            continue

        db_value = match.iloc[0][db_column]

        if pd.isna(db_value):
            continue

        difference = abs(parsed_value - db_value)

        status = (
            "MANUAL REVIEW"
            if difference > 5
            else "OK"
        )

        validation_rows.append(
            {
                "company_id": company,
                "metric_type": metric,
                "parsed_value": parsed_value,
                "database_value": db_value,
                "difference_pct": round(difference,2),
                "status": status,
            }
        )

    validation_df = pd.DataFrame(validation_rows)

    save_dataframe(
        validation_df,
        VALIDATION_OUTPUT,
    )

    print(f"\nValidation Records : {len(validation_df)}")

    return validation_df
    
# ==========================================================
# MAIN
# ==========================================================
def main():

    print_header("Sprint 5 - Day 29")

    print("Parser started successfully!")

    df = load_analysis_file()

    print("\nDetected Columns:\n")

    for col in df.columns:
        print(col)

    print("\nFirst 5 rows:")

    print(df.head())

    parsed_df, failed_df = parse_analysis_data(df)

    generate_output_files(
        parsed_df,
        failed_df,
    )

    conn = connect_database()

    ratios = load_financial_ratios(conn)

    validation = validate_parsed_values(
        parsed_df,
        ratios,
    )

    conn.close()

    print_header("Day 29 Completed")

    print(f"Parsed Records      : {len(parsed_df)}")

    print(f"Failed Records      : {len(failed_df)}")

    print(f"Validation Records  : {len(validation)}")

    print("\nGenerated Files")

    print("----------------------")

    print(PARSED_OUTPUT.name)

    print(FAILURE_OUTPUT.name)

    print(VALIDATION_OUTPUT.name)
if __name__ == "__main__":
    main()        

