# src/etl/normaliser.py

import re


def normalize_ticker(ticker):
    """
    Convert company ticker into standard format.

    Examples:
        abb -> ABB
        hdfcbank -> HDFCBANK
    """

    if ticker is None:
        return None

    return str(ticker).strip().upper()


def normalize_year(year_value):
    """
    Convert year formats into standard format.

    Examples:
        Dec 2012 -> 2012
        Mar-13 -> 2013
        2024 -> 2024
        TTM -> TTM
    """

    if year_value is None:
        return None

    year_str = str(year_value).strip()

    # Handle TTM
    if year_str.upper() == "TTM":
        return "TTM"

    four_digit_match = re.search(
        r"(20\d{2}|19\d{2})",
        year_str
    )

    if four_digit_match:
        return int(
            four_digit_match.group()
        )

    two_digit_match = re.search(
        r"-(\d{2})$",
        year_str
    )

    if two_digit_match:
        return int(
            "20" +
            two_digit_match.group(1)
        )

    raise ValueError(
        f"Invalid year format: {year_value}"
    )