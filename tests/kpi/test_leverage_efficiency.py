import pytest

from src.analytics.ratios import (
    debt_to_equity,
    high_leverage_flag,
    interest_coverage_ratio,
    icr_label,
    icr_warning_flag,
    net_debt,
    asset_turnover,
)


def test_debt_to_equity_normal():
    assert debt_to_equity(500, 100, 100) == 2.5


def test_debt_free_returns_zero():
    assert debt_to_equity(0, 100, 100) == 0


def test_negative_equity_returns_none():
    assert debt_to_equity(100, -100, 50) is None


def test_high_leverage_flag():
    assert high_leverage_flag(6, "Technology") is True


def test_financial_sector_no_flag():
    assert high_leverage_flag(6, "Financials") is False


def test_interest_zero_returns_none():
    assert interest_coverage_ratio(200, 20, 0) is None


def test_icr_label():
    assert icr_label(None) == "Debt Free"


def test_asset_turnover_zero_assets():
    assert asset_turnover(1000, 0) is None