import pandas as pd

from src.etl.validator import (
    dq01_pk_uniqueness,
    dq02_company_year_uniqueness,
    dq03_fk_integrity
)


def test_dq01_duplicate_company():

    df = pd.DataFrame(
        {
            "id": ["ABB", "ABB"]
        }
    )

    failures = dq01_pk_uniqueness(df)

    assert len(failures) == 1


def test_dq02_duplicate_company_year():

    df = pd.DataFrame(
        {
            "company_id": ["ABB", "ABB"],
            "year": [2024, 2024]
        }
    )

    failures = dq02_company_year_uniqueness(
        df,
        "profitandloss"
    )

    assert len(failures) == 1


def test_dq03_missing_fk():

    companies = pd.DataFrame(
        {
            "id": ["ABB"]
        }
    )

    child = pd.DataFrame(
        {
            "company_id": ["XYZ"]
        }
    )

    failures = dq03_fk_integrity(
        companies,
        child,
        "profitandloss"
    )

    assert len(failures) == 1

import pandas as pd

from src.etl.validator import (
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


# =====================================
# DQ-04 Balance Sheet Check
# =====================================

def test_dq04_balance_sheet_check():

    df = pd.DataFrame({
        "total_assets": [1000],
        "total_liabilities": [700],
        "equity_capital": [100],
        "reserves": [100]
    })

    result = dq04_balance_sheet_check(df)

    assert len(result) == 1


# =====================================
# DQ-05 OPM Cross Check
# =====================================

def test_dq05_opm_crosscheck():

    df = pd.DataFrame({
        "sales": [1000],
        "operating_profit": [300],
        "opm_percentage": [10]
    })

    result = dq05_opm_crosscheck(df)

    assert len(result) == 1


# =====================================
# DQ-06 Positive Sales
# =====================================

def test_dq06_positive_sales():

    df = pd.DataFrame({
        "sales": [-100]
    })

    result = dq06_positive_sales(df)

    assert len(result) == 1


# =====================================
# DQ-07 Company ID Not Null
# =====================================

def test_dq07_company_id_not_null():

    df = pd.DataFrame({
        "company_id": [None]
    })

    result = dq07_company_id_not_null(df)

    assert len(result) == 1


# =====================================
# DQ-08 Year Not Null
# =====================================

def test_dq08_year_not_null():

    df = pd.DataFrame({
        "year": [None]
    })

    result = dq08_year_not_null(df)

    assert len(result) == 1


# =====================================
# DQ-09 Sales Not Null
# =====================================

def test_dq09_sales_not_null():

    df = pd.DataFrame({
        "sales": [None]
    })

    result = dq09_sales_not_null(df)

    assert len(result) == 1


# =====================================
# DQ-10 Valid Year Range
# =====================================

def test_dq10_valid_year_range():

    df = pd.DataFrame({
        "year": [1995]
    })

    result = dq10_valid_year_range(df)

    assert len(result) == 1


# =====================================
# DQ-11 Duplicate Company Names
# =====================================

def test_dq11_duplicate_company_names():

    df = pd.DataFrame({
        "company_name": [
            "ABC",
            "ABC"
        ]
    })

    result = dq11_duplicate_company_names(df)

    assert len(result) == 2


# =====================================
# DQ-12 Debt Positive
# =====================================

def test_dq12_debt_positive():

    df = pd.DataFrame({
        "total_debt_cr": [-500]
    })

    result = dq12_debt_positive(df)

    assert len(result) == 1


# =====================================
# DQ-13 Stock Price Positive
# =====================================

def test_dq13_stock_price_positive():

    df = pd.DataFrame({
        "close_price": [0]
    })

    result = dq13_stock_price_positive(df)

    assert len(result) == 1


# =====================================
# DQ-14 Ratio Range
# =====================================

def test_dq14_ratio_range():

    df = pd.DataFrame({
        "operating_profit_margin_pct": [2000]
    })

    result = dq14_ratio_range(df)

    assert len(result) == 1


# =====================================
# DQ-15 Website Exists
# =====================================

def test_dq15_website_exists():

    df = pd.DataFrame({
        "website": [None]
    })

    result = dq15_website_exists(df)

    assert len(result) == 1


# =====================================
# DQ-16 NSE Profile Exists
# =====================================

def test_dq16_nse_profile_exists():

    df = pd.DataFrame({
        "nse_profile": [None]
    })

    result = dq16_nse_profile_exists(df)

    assert len(result) == 1