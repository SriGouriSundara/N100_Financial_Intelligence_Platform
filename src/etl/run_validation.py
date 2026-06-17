from pathlib import Path
import pandas as pd

from src.etl.loader import load_and_normalize

from src.etl.validator import (
    dq01_pk_uniqueness,
    dq02_company_year_uniqueness,
    dq03_fk_integrity,
    dq04_balance_sheet_check,
    dq05_opm_crosscheck,
    dq06_positive_sales,
    dq07_company_id_not_null,
    dq08_year_not_null,
    dq09_sales_not_null,
    dq10_valid_year_range,
    dq11_duplicate_company_names,
    dq12_debt_positive,
    dq13_stock_price_positive,
    dq14_ratio_range,
    dq15_website_exists,
    dq16_nse_profile_exists
)

# ----------------------------
# LOAD FILES
# ----------------------------

companies = load_and_normalize(
    "data/raw/companies.xlsx"
)

profitandloss = load_and_normalize(
    "data/raw/profitandloss.xlsx"
)

balancesheet = load_and_normalize(
    "data/raw/balancesheet.xlsx"
)

financial_ratios = load_and_normalize(
    "data/raw/financial_ratios.xlsx"
)

stock_prices = load_and_normalize(
    "data/raw/stock_prices.xlsx"
)

# ----------------------------
# VALIDATION
# ----------------------------

failures = []

# DQ01
failures.extend(
    dq01_pk_uniqueness(
        companies
    )
)

# DQ02
failures.extend(
    dq02_company_year_uniqueness(
        profitandloss,
        "profitandloss"
    )
)

# DQ03
failures.extend(
    dq03_fk_integrity(
        companies,
        profitandloss,
        "profitandloss"
    )
)

# DQ04
failures.extend(
    dq04_balance_sheet_check(
        balancesheet
    )
)

# DQ05
failures.extend(
    dq05_opm_crosscheck(
        profitandloss
    )
)

# DQ06
failures.extend(
    dq06_positive_sales(
        profitandloss
    )
)

# DQ07
failures.extend(
    dq07_company_id_not_null(
        profitandloss
    )
)

# DQ08
failures.extend(
    dq08_year_not_null(
        profitandloss
    )
)

# DQ09
failures.extend(
    dq09_sales_not_null(
        profitandloss
    )
)

# DQ10
failures.extend(
    dq10_valid_year_range(
        profitandloss
    )
)

# DQ11
failures.extend(
    dq11_duplicate_company_names(
        companies
    )
)

# DQ12
failures.extend(
    dq12_debt_positive(
        financial_ratios
    )
)

# DQ13
failures.extend(
    dq13_stock_price_positive(
        stock_prices
    )
)

# DQ14
failures.extend(
    dq14_ratio_range(
        financial_ratios
    )
)

# DQ15
failures.extend(
    dq15_website_exists(
        companies
    )
)

# DQ16
failures.extend(
    dq16_nse_profile_exists(
        companies
    )
)

# ----------------------------
# SAVE OUTPUT
# ----------------------------

Path("output").mkdir(
    exist_ok=True
)

pd.DataFrame(
    failures
).to_csv(
    "output/validation_failures.csv",
    index=False
)

print("=" * 50)
print("VALIDATION COMPLETED")
print("=" * 50)
print(
    f"Total Failures Found: {len(failures)}"
)
print(
    "Output: output/validation_failures.csv"
)