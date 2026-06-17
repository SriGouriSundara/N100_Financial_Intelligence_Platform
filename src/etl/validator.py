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

    validation_failures = []

    valid_rows = df[df["total_assets"] != 0]

    equity = (
        valid_rows["equity_capital"]
        + valid_rows["reserves"]
    )

    difference_pct = abs(
        valid_rows["total_assets"]
        - (
            valid_rows["total_liabilities"]
            + equity
        )
    ) / valid_rows["total_assets"]

    failed_rows = valid_rows[
        difference_pct > 0.01
    ]

    for idx, row in failed_rows.iterrows():

        validation_failures.append({
            "rule_id": "DQ-04",
            "severity": "WARNING",
            "table_name": "balancesheet",
            "row": idx,
            "message": "Balance sheet mismatch > 1%"
        })

    return validation_failures
def dq05_opm_crosscheck(df):

    validation_failures = []

    valid_rows = df[df["sales"] != 0]

    calculated_opm = (
        valid_rows["operating_profit"]
        / valid_rows["sales"]
    ) * 100

    failed_rows = valid_rows[
        abs(
            calculated_opm
            - valid_rows["opm_percentage"]
        ) > 1
    ]

    for idx, row in failed_rows.iterrows():

        validation_failures.append({
            "rule_id": "DQ-05",
            "severity": "WARNING",
            "table_name": "profitandloss",
            "row": idx,
            "message": "OPM cross-check failed"
        })

    return validation_failures

def dq06_positive_sales(df):

    validation_failures = []

    failed_rows = df[df["sales"] <= 0]

    for idx, row in failed_rows.iterrows():
        validation_failures.append({
            "rule_id": "DQ-06",
            "severity": "WARNING",
            "table_name": "profitandloss",
            "row": idx,
            "message": "Sales must be positive"
        })

    return validation_failures

def dq07_company_id_not_null(df):

    validation_failures = []

    failed_rows = df[df["company_id"].isna()]

    for idx, row in failed_rows.iterrows():
        validation_failures.append({
            "rule_id": "DQ-07",
            "severity": "WARNING",
            "table_name": "profitandloss",
            "row": idx,
            "message": "Company ID is null"
        })

    return validation_failures

def dq08_year_not_null(df):

    validation_failures = []

    failed_rows = df[df["year"].isna()]

    for idx, row in failed_rows.iterrows():
        validation_failures.append({
            "rule_id": "DQ-08",
            "severity": "WARNING",
            "table_name": "profitandloss",
            "row": idx,
            "message": "Year is null"
        })

    return validation_failures

def dq09_sales_not_null(df):

    validation_failures = []

    failed_rows = df[df["sales"].isna()]

    for idx, row in failed_rows.iterrows():
        validation_failures.append({
            "rule_id": "DQ-09",
            "severity": "WARNING",
            "table_name": "profitandloss",
            "row": idx,
            "message": "Sales is null"
        })

    return validation_failures

def dq10_valid_year_range(df):

    validation_failures = []

    year_numeric = pd.to_numeric(
        df["year"],
        errors="coerce"
    )

    failed_rows = df[
        (year_numeric < 2000)
        | (year_numeric > 2026)
    ]

    for idx, row in failed_rows.iterrows():
        validation_failures.append({
            "rule_id": "DQ-10",
            "severity": "WARNING",
            "table_name": "profitandloss",
            "row": idx,
            "message": "Invalid year range"
        })

    return validation_failures

def dq11_duplicate_company_names(df):

    validation_failures = []

    failed_rows = df[
        df.duplicated(
            subset=["company_name"],
            keep=False
        )
    ]

    for idx, row in failed_rows.iterrows():
        validation_failures.append({
            "rule_id": "DQ-11",
            "severity": "WARNING",
            "table_name": "companies",
            "row": idx,
            "message": "Duplicate company name"
        })

    return validation_failures

def dq12_debt_positive(df):

    validation_failures = []

    failed_rows = df[
        df["total_debt_cr"] < 0
    ]

    for idx, row in failed_rows.iterrows():
        validation_failures.append({
            "rule_id": "DQ-12",
            "severity": "WARNING",
            "table_name": "financial_ratios",
            "row": idx,
            "message": "Negative debt value"
        })

    return validation_failures

def dq13_stock_price_positive(df):

    validation_failures = []

    failed_rows = df[
        df["close_price"] <= 0
    ]

    for idx, row in failed_rows.iterrows():
        validation_failures.append({
            "rule_id": "DQ-13",
            "severity": "WARNING",
            "table_name": "stock_prices",
            "row": idx,
            "message": "Invalid stock price"
        })

    return validation_failures

def dq14_ratio_range(df):

    validation_failures = []

    failed_rows = df[
        (
            df["operating_profit_margin_pct"] < -100
        )
        |
        (
            df["operating_profit_margin_pct"] > 1000
        )
    ]

    for idx, row in failed_rows.iterrows():
        validation_failures.append({
            "rule_id": "DQ-14",
            "severity": "WARNING",
            "table_name": "financial_ratios",
            "row": idx,
            "message": "Ratio out of range"
        })

    return validation_failures

def dq15_website_exists(df):

    validation_failures = []

    failed_rows = df[
        df["website"].isna()
    ]

    for idx, row in failed_rows.iterrows():
        validation_failures.append({
            "rule_id": "DQ-15",
            "severity": "WARNING",
            "table_name": "companies",
            "row": idx,
            "message": "Website missing"
        })

    return validation_failures

def dq16_nse_profile_exists(df):

    validation_failures = []

    failed_rows = df[
        df["nse_profile"].isna()
    ]

    for idx, row in failed_rows.iterrows():
        validation_failures.append({
            "rule_id": "DQ-16",
            "severity": "WARNING",
            "table_name": "companies",
            "row": idx,
            "message": "NSE profile missing"
        })

    return validation_failures

