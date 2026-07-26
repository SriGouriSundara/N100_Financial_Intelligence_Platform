"""
Sprint 5 - Day 32
Capital Allocation Report
"""
import sqlite3
from pathlib import Path
import numpy as np
import pandas as pd
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DB_PATH = PROJECT_ROOT / "db" / "nifty100.db"

CAPITAL_FILE = PROJECT_ROOT / "output" / "capital_allocation.csv"

CASHFLOW_FILE = PROJECT_ROOT / "output" / "cashflow_intelligence.xlsx"

PATTERN_OUTPUT = PROJECT_ROOT / "output" / "pattern_changes.csv"

DISTRIBUTION_OUTPUT = (
    PROJECT_ROOT
    / "output"
    / "capital_pattern_distribution.csv"
)
def print_header(title):

    print("\n" + "=" * 60)

    print(title)

    print("=" * 60)
def connect_database():

    print_header("Connecting Database")

    conn = sqlite3.connect(DB_PATH)

    print("Database Connected")

    return conn
def load_capital_allocation():

    print_header("Loading Capital Allocation")

    df = pd.read_csv(CAPITAL_FILE)

    print(f"Rows : {len(df)}")

    print(f"Columns : {len(df.columns)}")
    print("\nCapital Allocation Columns")
    print("-" * 40)
    print(df.columns.tolist())

    return df
def load_cashflow():

    print_header("Loading Cashflow Intelligence")

    df = pd.read_excel(CASHFLOW_FILE)

    print(f"Rows : {len(df)}")

    return df
# ==========================================================
# CAPITAL ALLOCATION VALIDATION
# ==========================================================

def validate_capital_allocation(capital_df, cashflow_df):

    print_header("Validating Capital Allocation")

    # ---------------------------------------------
    # Unique Companies
    # ---------------------------------------------

    capital_companies = set(capital_df["company_id"].unique())

    cashflow_companies = set(cashflow_df["company_id"].unique())

    missing_companies = sorted(
        cashflow_companies - capital_companies
    )

    extra_companies = sorted(
        capital_companies - cashflow_companies
    )

    print(f"Companies in Capital File : {len(capital_companies)}")
    print(f"Companies in Cashflow     : {len(cashflow_companies)}")

    if not missing_companies:
        print("✓ All companies present")
    else:
        print("✗ Missing companies:")
        for company in missing_companies:
            print(f"  - {company}")

    if extra_companies:
        print("\nAdditional companies found:")
        for company in extra_companies:
            print(f"  - {company}")

# ---------------------------------------------
# Year Coverage
# ---------------------------------------------

    print("\nYear Coverage")
    print("--------------------------")
    year_counts = (

    capital_df
    .groupby("company_id")["year"]
    .nunique()
    .sort_values()

)

    print(
    f"Minimum Years : {year_counts.min()}"
)

    print(
    f"Maximum Years : {year_counts.max()}"
)

    print(
    f"Average Years : {year_counts.mean():.1f}"
)

    print("\nCompanies with fewer than 5 years")

    few_years = year_counts[year_counts < 5]

    if few_years.empty:

     print("✓ None")

    else:

     for company, years in few_years.items():

        print(f"{company} -> {years} years")

    # ---------------------------------------------
    # Latest Year Distribution
    # ---------------------------------------------

    latest_year = capital_df["year"].max()

    latest = capital_df[
        capital_df["year"] == latest_year
    ]

    print("\nLatest Year Summary")
    print("--------------------------")

    print(f"Latest Year : {latest_year}")
    print(f"Records     : {len(latest)}")

    return latest
# ==========================================================
# PATTERN DISTRIBUTION
# ==========================================================

def generate_pattern_distribution(latest_df):

    print_header("Pattern Distribution")

    # ---------------------------------------------
    # Detect Pattern Column
    # ---------------------------------------------

    pattern_column = None

    possible_columns = [

        "pattern_label",
        "capital_allocation_pattern",
        "capital_allocation",
        "pattern",
        "allocation_pattern"

    ]

    for col in possible_columns:

        if col in latest_df.columns:

            pattern_column = col

            break

    if pattern_column is None:

        raise ValueError(
            f"Pattern column not found.\nAvailable Columns: {list(latest_df.columns)}"
        )

    print(f"Using Column : {pattern_column}")
    distribution = (

    latest_df[pattern_column]

    .value_counts()

    .reset_index()

)

    distribution.columns = [

    "capital_allocation_pattern",

    "company_count"

]

    distribution.to_csv(

    DISTRIBUTION_OUTPUT,

    index=False

)

    print("\nDistribution Summary")
    print("----------------------------")
    print(distribution)
    print(f"\nSaved -> {DISTRIBUTION_OUTPUT.name}")
    return distribution
# ==========================================================
# PATTERN CHANGE DETECTION
# ==========================================================

def generate_pattern_changes(capital_df):

    print_header("Pattern Change Detection")

    records = []

    latest_year = capital_df["year"].max()

    previous_year = sorted(
        capital_df["year"].unique()
    )[-2]

    companies = sorted(
        capital_df["company_id"].unique()
    )

    for company in companies:

        company_df = capital_df[
            capital_df["company_id"] == company
        ]

        latest = company_df[
            company_df["year"] == latest_year
        ]

        previous = company_df[
            company_df["year"] == previous_year
        ]

        if latest.empty or previous.empty:
            continue

        latest_pattern = latest.iloc[0]["pattern_label"]

        previous_pattern = previous.iloc[0]["pattern_label"]

        changed = latest_pattern != previous_pattern

        records.append(

            {

                "company_id": company,

                "previous_year": previous_year,

                "previous_pattern": previous_pattern,

                "current_year": latest_year,

                "current_pattern": latest_pattern,

                "changed": changed

            }

        )

    result = pd.DataFrame(records)

    result.to_csv(

        PATTERN_OUTPUT,

        index=False

    )

    print(f"Companies Compared : {len(result)}")

    print(

        f"Pattern Changes    : {result['changed'].sum()}"

    )

    print(f"Saved -> {PATTERN_OUTPUT.name}")

    return result
# ==========================================================
# UPDATE CASHFLOW INTELLIGENCE
# ==========================================================

def update_cashflow_intelligence(

    cashflow_df,

    latest_capital

):

    print_header("Updating Cashflow Intelligence")

    latest_patterns = latest_capital[
        [
            "company_id",
            "pattern_label"
        ]
    ].copy()

    latest_patterns.rename(

        columns={
            "pattern_label":
            "capital_allocation_pattern"
        },

        inplace=True

    )

    updated = cashflow_df.merge(

        latest_patterns,

        on="company_id",

        how="left"

    )

    updated.to_excel(

        CASHFLOW_FILE,

        index=False

    )

    print(

        f"Updated Rows : {len(updated)}"

    )

    print(

        "Added Column : capital_allocation_pattern"

    )

    print(

        f"Saved -> {CASHFLOW_FILE.name}"

    )

    return updated
# ==========================================================
# FINAL VALIDATION
# ==========================================================

def final_validation(updated_df):

    print_header("DAY 32 VALIDATION")

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

        "capital_allocation_label",

        "capital_allocation_pattern"

    ]

    print(f"Rows : {len(updated_df)}")

    if len(updated_df) == 92:

        print("✓ 92 rows verified")

    else:

        print("✗ Row count mismatch")

    missing = [

        col

        for col in required_columns

        if col not in updated_df.columns

    ]

    if len(missing) == 0:

        print("✓ All required columns present")

    else:

        print("Missing Columns:")

        for col in missing:

            print(f" - {col}")

    print("\nPattern Distribution")

    print("----------------------")

    print(

        updated_df[

            "capital_allocation_pattern"

        ].value_counts()

    )
    
def main():

    print_header("Sprint 5 Day 32")

    conn = connect_database()

    capital = load_capital_allocation()

    cashflow = load_cashflow()

    latest = validate_capital_allocation(

    capital,

    cashflow
)
    distribution = generate_pattern_distribution(latest)
    pattern_changes = generate_pattern_changes(capital)
    updated = update_cashflow_intelligence(

    cashflow,

    latest

)

    final_validation(

    updated

)
    print_header("SUMMARY")
    print(f"Capital Allocation Rows : {len(capital)}")
    print(f"Cashflow Rows           : {len(updated)}")
    print(f"Latest Year Records     : {len(latest)}")
    print(f"Pattern Categories      : {len(distribution)}")
    print(f"Pattern Changes         : {len(pattern_changes)}")
    print(
    f"Companies Changed       : "
    f"{pattern_changes['changed'].sum()}"
)
    print("\nGenerated Files")
    print("----------------------------")
    print("✓ cashflow_intelligence.xlsx")
    print("✓ capital_pattern_distribution.csv")
    print("✓ pattern_changes.csv")
    conn.close()

if __name__ == "__main__":

    main()