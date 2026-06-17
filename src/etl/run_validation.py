from src.etl.loader import load_and_normalize
from src.etl.validator import (
    dq01_pk_uniqueness,
    dq02_company_year_uniqueness,
    dq03_fk_integrity,
    save_failures
)

# Load files
companies = load_and_normalize("data/raw/companies.xlsx")
profitandloss = load_and_normalize("data/raw/profitandloss.xlsx")
balancesheet = load_and_normalize("data/raw/balancesheet.xlsx")
financial_ratios = load_and_normalize("data/raw/financial_ratios.xlsx")
stock_prices = load_and_normalize("data/raw/stock_prices.xlsx")

all_failures = []

# DQ-01
all_failures.extend(
    dq01_pk_uniqueness(companies)
)

# DQ-02
all_failures.extend(
    dq02_company_year_uniqueness(
        profitandloss,
        "profitandloss"
    )
)

all_failures.extend(
    dq02_company_year_uniqueness(
        balancesheet,
        "balancesheet"
    )
)

all_failures.extend(
    dq02_company_year_uniqueness(
        financial_ratios,
        "financial_ratios"
    )
)

# DQ-03
all_failures.extend(
    dq03_fk_integrity(
        companies,
        profitandloss,
        "profitandloss"
    )
)

all_failures.extend(
    dq03_fk_integrity(
        companies,
        balancesheet,
        "balancesheet"
    )
)

all_failures.extend(
    dq03_fk_integrity(
        companies,
        financial_ratios,
        "financial_ratios"
    )
)

all_failures.extend(
    dq03_fk_integrity(
        companies,
        stock_prices,
        "stock_prices"
    )
)

# Save CSV
save_failures(
    all_failures,
    "output/validation_failures.csv"
)

print("=" * 50)
print("VALIDATION COMPLETED")
print(f"Total Failures: {len(all_failures)}")
print("Output File: output/validation_failures.csv")
print("=" * 50)