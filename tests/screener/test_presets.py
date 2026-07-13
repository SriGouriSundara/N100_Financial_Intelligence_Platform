import pandas as pd

from src.screener.engine import run_preset


def test_returns_dataframe():

    df = pd.DataFrame(
        {
            "return_on_equity_pct": [20],
            "debt_to_equity": [0.5],
            "free_cash_flow_cr": [100],
            "revenue_cagr_5yr": [15],
            "pat_cagr_5yr": [25],
            "dividend_payout_ratio_pct": [50],
            "broad_sector": ["Technology"],
            "composite_quality_score": [90],
        }
    )

    rules = {
        "roe_min": 15
    }

    result = run_preset(
        df,
        "unit_test",
        rules
    )

    assert len(result) == 1


def test_empty_result():

    df = pd.DataFrame(
        {
            "return_on_equity_pct": [5],
            "broad_sector": ["Technology"],
            "composite_quality_score": [50],
        }
    )

    rules = {
        "roe_min": 20
    }

    result = run_preset(
        df,
        "unit_test",
        rules
    )

    assert len(result) == 0


def test_missing_column():

    df = pd.DataFrame(
        {
            "company": ["ABC"]
        }
    )

    rules = {
        "roe_min": 15
    }

    result = run_preset(
        df,
        "unit_test",
        rules
    )

    assert isinstance(result, pd.DataFrame)