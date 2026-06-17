"""
loader.py
Loads Excel files into pandas DataFrames
and performs basic normalization.
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
    Fix files where first row contains
    actual column names.
    """

    df.columns = df.iloc[0]
    df = df[1:].reset_index(drop=True)

    return df


def standardize_dataframe(df):
    """
    Standardize company_id and year columns.
    Remove duplicate company-year records.
    """

    # Normalize company IDs
    if "company_id" in df.columns:
        df["company_id"] = df["company_id"].apply(
            normalize_ticker
        )

    # Normalize year
    if "year" in df.columns:
        df["year"] = df["year"].apply(
            normalize_year
        )

    if "Year" in df.columns:
        df["Year"] = df["Year"].apply(
            normalize_year
        )

    # Remove duplicate company-year rows
    if (
        "company_id" in df.columns
        and
        "year" in df.columns
    ):
        df = df.drop_duplicates(
            subset=["company_id", "year"],
            keep="first"
        )

    return df


def load_and_normalize(file_path):
    """
    Load Excel file and normalize it.
    Automatically fixes Bluestock files
    that contain title rows above headers.
    """

    df = load_excel(file_path)

    first_column_name = str(
        df.columns[0]
    )

    if (
        "Bluestock" in first_column_name
        or
        "Mkt" in first_column_name
    ):
        df = clean_headers(df)

    df = standardize_dataframe(df)

    return df