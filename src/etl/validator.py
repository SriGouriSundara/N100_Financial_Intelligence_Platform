import pandas as pd


def dq01_pk_uniqueness(companies_df):
    """
    DQ-01
    Check duplicate company IDs in companies table
    """

    failures = []

    duplicates = companies_df[
        companies_df["id"].duplicated()
    ]

    for _, row in duplicates.iterrows():

        failures.append(
            {
                "rule_id": "DQ-01",
                "severity": "CRITICAL",
                "table_name": "companies",
                "row": row.name,
                "message": f"Duplicate company id: {row['id']}"
            }
        )

    return failures


def dq02_company_year_uniqueness(df, table_name):
    """
    DQ-02
    Check duplicate (company_id, year)
    """

    failures = []

    duplicates = df[
        df.duplicated(
            subset=["company_id", "year"]
        )
    ]

    for _, row in duplicates.iterrows():

        failures.append(
            {
                "rule_id": "DQ-02",
                "severity": "CRITICAL",
                "table_name": table_name,
                "row": row.name,
                "message":
                    f"Duplicate company-year: "
                    f"{row['company_id']} {row['year']}"
            }
        )

    return failures


def dq03_fk_integrity(
        companies_df,
        child_df,
        table_name):
    """
    DQ-03
    Foreign key integrity
    """

    failures = []

    valid_ids = set(
        companies_df["id"]
    )

    invalid_rows = child_df[
        ~child_df["company_id"].isin(valid_ids)
    ]

    for _, row in invalid_rows.iterrows():

        failures.append(
            {
                "rule_id": "DQ-03",
                "severity": "CRITICAL",
                "table_name": table_name,
                "row": row.name,
                "message":
                    f"Missing company: "
                    f"{row['company_id']}"
            }
        )

    return failures


def save_failures(failures,
                  output_file):
    """
    Save failures CSV
    """

    df = pd.DataFrame(failures)

    df.to_csv(
        output_file,
        index=False
    )

    print(
        f"Saved {len(df)} failures "
        f"to {output_file}"
    )

def dq04_balance_sheet_check(df):

    equity = (
        df["equity_capital"]
        + df["reserves"]
    )

    difference_pct = abs(
        df["total_assets"]
        - (
            df["total_liabilities"]
            + equity
        )
    ) / df["total_assets"]

    failures = df[
        difference_pct > 0.01
    ]

    return failures

def dq05_opm_crosscheck(df):

    calculated_opm = (
        df["operating_profit"]
        / df["sales"]
    ) * 100

    failures = df[
        abs(
            calculated_opm
            - df["opm_percentage"]
        ) > 1
    ]

    return failures

def dq06_positive_sales(df):

    failures = df[
        df["sales"] <= 0
    ]

    return failures


def dq07_company_id_not_null(df):

    failures = df[
        df["company_id"].isna()
    ]

    return failures

def dq08_year_not_null(df):

    failures = df[
        df["year"].isna()
    ]

    return failures

def dq09_sales_not_null(df):

    failures = df[
        df["sales"].isna()
    ]

    return failures

def dq10_valid_year_range(df):

    failures = df[
        (df["year"] < 2000)
        | (df["year"] > 2026)
    ]

    return failures

def dq11_duplicate_company_names(df):

    failures = df[
        df.duplicated(
            subset=["company_name"],
            keep=False
        )
    ]

    return failures

def dq12_debt_positive(df):

    failures = df[
        df["total_debt_cr"] < 0
    ]

    return failures

def dq13_stock_price_positive(df):

    failures = df[
        df["close_price"] <= 0
    ]

    return failures

def dq14_ratio_range(df):

    failures = df[
        (
            df["operating_profit_margin_pct"]
            < -100
        )
        |
        (
            df["operating_profit_margin_pct"]
            > 1000
        )
    ]

    return failures

def dq15_website_exists(df):

    failures = df[
        df["website"].isna()
    ]

    return failures

def dq16_nse_profile_exists(df):

    failures = df[
        df["nse_profile"].isna()
    ]

    return failures

