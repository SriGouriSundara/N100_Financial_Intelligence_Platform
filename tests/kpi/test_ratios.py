"""
Unit Tests
Sprint 2 - Day 08

Tests for:
1. Net Profit Margin
2. Operating Profit Margin
3. ROE
4. ROCE
5. ROA
"""

from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    check_opm_difference,
    return_on_equity,
    return_on_capital_employed,
    return_on_assets,
)

# -------------------------------------------------------
# Test 1
# Net Profit Margin - Normal Case
# -------------------------------------------------------

def test_net_profit_margin_normal():
    assert net_profit_margin(100, 500) == 20.0


# -------------------------------------------------------
# Test 2
# Net Profit Margin - Sales = 0
# -------------------------------------------------------

def test_net_profit_margin_zero_sales():
    assert net_profit_margin(100, 0) is None


# -------------------------------------------------------
# Test 3
# ROE Normal
# -------------------------------------------------------

def test_return_on_equity_normal():
    assert return_on_equity(100, 200, 300) == 20.0


# -------------------------------------------------------
# Test 4
# ROE Negative Equity
# -------------------------------------------------------

def test_return_on_equity_negative():
    assert return_on_equity(100, -200, 100) is None


# -------------------------------------------------------
# Test 5
# ROA Normal
# -------------------------------------------------------

def test_return_on_assets_normal():
    assert return_on_assets(100, 500) == 20.0


# -------------------------------------------------------
# Test 6
# ROA Assets = 0
# -------------------------------------------------------

def test_return_on_assets_zero():
    assert return_on_assets(100, 0) is None


# -------------------------------------------------------
# Test 7
# OPM Match
# -------------------------------------------------------

def test_opm_match():
    calculated = operating_profit_margin(250, 1000)

    assert calculated == 25.0

    assert (
        check_opm_difference(
            "ABC Ltd",
            2024,
            calculated,
            25.0
        )
        is False
    )


# -------------------------------------------------------
# Test 8
# OPM Mismatch
# -------------------------------------------------------

def test_opm_mismatch():

    calculated = operating_profit_margin(250, 1000)

    result = check_opm_difference(
        "ABC Ltd",
        2024,
        calculated,
        20.0
    )

    print("Result =", result)

    assert result is True