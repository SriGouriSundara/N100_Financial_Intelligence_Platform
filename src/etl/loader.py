"""
loader.py
Loads Excel files into pandas DataFrames.

"""
from pathlib import Path

import pandas as pd

from src.etl.normaliser import (
    normalize_ticker,
    normalize_year
)


def load_excel(file_path):
    """
    Load Excel file into DataFrame.
    """

    return pd.read_excel(file_path)


def clean_headers(df):
    """
    Fix files where first row contains column names.
    """

    df.columns = df.iloc[0]
    df = df[1:].reset_index(drop=True)

    return df


def standardize_dataframe(df):

    if "company_id" in df.columns:
        df["company_id"] = df["company_id"].apply(
            normalize_ticker
        )

    if "year" in df.columns:
        df["year"] = df["year"].apply(
            normalize_year
        )

    if "Year" in df.columns:
        df["Year"] = df["Year"].apply(
            normalize_year
        )

    return df


def load_and_normalize(file_path):

    df = load_excel(file_path)

    first_cell = str(df.columns[0])

    if "Bluestock" in first_cell or "Mkt" in first_cell:
        df = clean_headers(df)

    df = standardize_dataframe(df)

    return df