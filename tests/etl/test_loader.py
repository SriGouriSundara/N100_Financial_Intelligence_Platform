import pandas as pd

from src.etl.loader import (
    load_excel,
    clean_headers,
    standardize_dataframe,
    load_and_normalize
)


# ------------------
# COMPANIES FILE
# ------------------

def test_companies_file():
    df = load_and_normalize(
        "data/raw/companies.xlsx"
    )

    assert len(df) == 92


def test_company_column():
    df = load_and_normalize(
        "data/raw/companies.xlsx"
    )

    assert "company_name" in df.columns


def test_company_not_empty():
    df = load_and_normalize(
        "data/raw/companies.xlsx"
    )

    assert len(df.columns) > 0


# ------------------
# LOAD EXCEL
# ------------------

def test_load_excel_returns_dataframe():
    df = load_excel(
        "data/raw/companies.xlsx"
    )

    assert isinstance(df, pd.DataFrame)


# ------------------
# CLEAN HEADERS
# ------------------

def test_clean_headers():
    sample = pd.DataFrame(
        [
            ["id", "name"],
            [1, "ABC"],
            [2, "XYZ"]
        ]
    )

    result = clean_headers(sample)

    assert "id" in result.columns
    assert "name" in result.columns


# ------------------
# STANDARDIZE DATAFRAME
# ------------------

def test_standardize_company_id():
    df = pd.DataFrame(
        {
            "company_id": ["abb"]
        }
    )

    result = standardize_dataframe(df)

    assert result["company_id"][0] == "ABB"


def test_standardize_year():
    df = pd.DataFrame(
        {
            "year": ["Mar-13"]
        }
    )

    result = standardize_dataframe(df)

    assert result["year"][0] == 2013


def test_standardize_year_column():
    df = pd.DataFrame(
        {
            "Year": ["Dec 2012"]
        }
    )

    result = standardize_dataframe(df)

    assert result["Year"][0] == 2012


# ------------------
# DATASET CHECKS
# ------------------

def test_profitandloss_loads():
    df = load_and_normalize(
        "data/raw/profitandloss.xlsx"
    )

    assert len(df) > 0


def test_balancesheet_loads():
    df = load_and_normalize(
        "data/raw/balancesheet.xlsx"
    )

    assert len(df) > 0


def test_cashflow_loads():
    df = load_and_normalize(
        "data/raw/cashflow.xlsx"
    )

    assert len(df) > 0


def test_analysis_loads():
    df = load_and_normalize(
        "data/raw/analysis.xlsx"
    )

    assert len(df) > 0


def test_documents_loads():
    df = load_and_normalize(
        "data/raw/documents.xlsx"
    )

    assert len(df) > 0


def test_financial_ratios_loads():
    df = load_and_normalize(
        "data/raw/financial_ratios.xlsx"
    )

    assert len(df) > 0


def test_peer_groups_loads():
    df = load_and_normalize(
        "data/raw/peer_groups.xlsx"
    )

    assert len(df) > 0


def test_sectors_loads():
    df = load_and_normalize(
        "data/raw/sectors.xlsx"
    )

    assert len(df) > 0


def test_stock_prices_loads():
    df = load_and_normalize(
        "data/raw/stock_prices.xlsx"
    )

    assert len(df) > 0