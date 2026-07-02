from src.analytics.cashflow_kpis import *

def test_free_cash_flow():
    assert free_cash_flow(100, -40) == 60


def test_negative_fcf():
    assert free_cash_flow(50, -100) == -50


def test_cfo_quality():
    ratio, label = cfo_quality_score(
        [100,120,130,140,150],
        [80,100,110,120,130]
    )

    assert label == "High Quality"


def test_pat_zero():
    ratio, label = cfo_quality_score(
        [100],
        [0]
    )

    assert ratio is None


def test_capex():
    value, label = capex_intensity(-50,1000)

    assert label == "Moderate"


def test_fcf_conversion():

    fcf = free_cash_flow(100,-40)

    assert round(
        fcf_conversion_rate(
            fcf,
            120
        ),
        2
    ) == 50.00


def test_pattern():

    signs, label = capital_allocation_pattern(
        100,
        -40,
        -20,
        1.2
    )

    assert label == "Shareholder Returns"


def test_asset_light():

    value, label = capex_intensity(
        -10,
        1000
    )

    assert label == "Asset Light"