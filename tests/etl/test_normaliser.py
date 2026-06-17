import pytest

from src.etl.normaliser import (
    normalize_ticker,
    normalize_year
)


# ------------------
# TICKER TESTS
# ------------------

def test_ticker_uppercase():
    assert normalize_ticker("abb") == "ABB"


def test_ticker_spaces():
    assert normalize_ticker(" hdfcbank ") == "HDFCBANK"


def test_ticker_already_upper():
    assert normalize_ticker("TCS") == "TCS"


def test_ticker_mixed_case():
    assert normalize_ticker("ReLiAnCe") == "RELIANCE"


def test_ticker_empty_string():
    assert normalize_ticker("") == ""


def test_ticker_none():
    assert normalize_ticker(None) is None


def test_ticker_numeric():
    assert normalize_ticker(123) == "123"


def test_ticker_special_chars():
    assert normalize_ticker("abc-ltd") == "ABC-LTD"


# ------------------
# YEAR TESTS
# ------------------

def test_year_dec():
    assert normalize_year("Dec 2012") == 2012


def test_year_mar():
    assert normalize_year("Mar 2014") == 2014


def test_year_short():
    assert normalize_year("Mar-13") == 2013


def test_year_integer():
    assert normalize_year(2024) == 2024


def test_year_string():
    assert normalize_year("2020") == 2020


def test_year_2015():
    assert normalize_year("2015") == 2015


def test_year_1999():
    assert normalize_year("1999") == 1999


def test_year_none():
    assert normalize_year(None) is None


def test_year_invalid():
    with pytest.raises(ValueError):
        normalize_year("INVALID")


def test_year_invalid_text():
    with pytest.raises(ValueError):
        normalize_year("hello world")


def test_year_invalid_symbol():
    with pytest.raises(ValueError):
        normalize_year("@@@")

def test_year_ttm():
    assert normalize_year("TTM") == "TTM"