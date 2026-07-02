"""
Sprint 2 - Day 11
Cash Flow KPI Engine
"""

import csv
from pathlib import Path


# ==========================================================
# FREE CASH FLOW
# ==========================================================

def free_cash_flow(operating_activity, investing_activity):
    """
    Formula:
    CFO + Investing Cash Flow

    Negative FCF is allowed.
    """
    return operating_activity + investing_activity


# ==========================================================
# CFO QUALITY SCORE
# ==========================================================

def cfo_quality_score(cfo_list, pat_list):
    """
    Calculates average CFO/PAT ratio over 5 years.

    Returns:
        average_ratio
        quality_label
    """

    ratios = []

    for cfo, pat in zip(cfo_list, pat_list):

        if pat == 0:
            return None, None

        ratios.append(cfo / pat)

    average = sum(ratios) / len(ratios)

    if average > 1:
        label = "High Quality"

    elif average >= 0.5:
        label = "Moderate"

    else:
        label = "Accrual Risk"

    return round(average, 2), label


# ==========================================================
# CAPEX INTENSITY
# ==========================================================

def capex_intensity(investing_activity, sales):

    if sales == 0:
        return None, None

    value = abs(investing_activity) / sales * 100

    if value < 3:
        label = "Asset Light"

    elif value <= 8:
        label = "Moderate"

    else:
        label = "Capital Intensive"

    return round(value, 2), label


# ==========================================================
# FCF CONVERSION
# ==========================================================

def fcf_conversion_rate(
    free_cash_flow_value,
    operating_profit
):

    if operating_profit == 0:
        return None

    return (
        free_cash_flow_value /
        operating_profit
    ) * 100


# ==========================================================
# CAPITAL ALLOCATION
# ==========================================================

def capital_allocation_pattern(
    cfo,
    cfi,
    cff,
    cfo_pat_ratio=0
):

    signs = (
        "+" if cfo >= 0 else "-",
        "+" if cfi >= 0 else "-",
        "+" if cff >= 0 else "-"
    )

    mapping = {

        ("+", "-", "-"):
            "Shareholder Returns"
            if cfo_pat_ratio > 1
            else "Reinvestor",

        ("+", "+", "-"):
            "Liquidating Assets",

        ("-", "+", "+"):
            "Distress Signal",

        ("-", "-", "+"):
            "Growth Funded by Debt",

        ("+", "+", "+"):
            "Cash Accumulator",

        ("-", "-", "-"):
            "Pre-Revenue",

        ("+", "-", "+"):
            "Mixed"

    }

    return signs, mapping.get(signs, "Unclassified")


# ==========================================================
# EXPORT CSV
# ==========================================================

def export_capital_allocation(
    rows,
    output_file="output/capital_allocation.csv"
):

    Path("output").mkdir(exist_ok=True)

    with open(
        output_file,
        "w",
        newline="",
        encoding="utf-8"
    ) as csvfile:

        writer = csv.writer(csvfile)

        writer.writerow([
            "company_id",
            "year",
            "cfo_sign",
            "cfi_sign",
            "cff_sign",
            "pattern_label"
        ])

        writer.writerows(rows)