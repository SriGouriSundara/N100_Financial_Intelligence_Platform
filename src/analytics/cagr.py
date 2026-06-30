"""
Sprint 2 - Day 10
CAGR Engine

This module calculates CAGR values for Revenue,
PAT and EPS while handling all required edge cases.
"""

from math import pow

# ==========================================================
# CAGR FLAGS
# ==========================================================

NORMAL = "NORMAL"
DECLINE_TO_LOSS = "DECLINE_TO_LOSS"
TURNAROUND = "TURNAROUND"
BOTH_NEGATIVE = "BOTH_NEGATIVE"
ZERO_BASE = "ZERO_BASE"
INSUFFICIENT = "INSUFFICIENT"


def calculate_cagr(start_value, end_value, years):
    """
    Calculate CAGR with edge-case handling.

    Returns:
        (cagr_value, flag)
    """

    # Not enough history
    if years <= 0:
        return None, INSUFFICIENT

    # Zero starting value
    if start_value == 0:
        return None, ZERO_BASE

    # Positive → Negative
    if start_value > 0 and end_value < 0:
        return None, DECLINE_TO_LOSS

    # Negative → Positive
    if start_value < 0 and end_value > 0:
        return None, TURNAROUND

    # Negative → Negative
    if start_value < 0 and end_value < 0:
        return None, BOTH_NEGATIVE

    # Normal CAGR
    cagr = (pow(end_value / start_value, 1 / years) - 1) * 100

    return round(cagr, 2), NORMAL


# ==========================================================
# Revenue CAGR
# ==========================================================

def revenue_cagr(start_sales, end_sales, years):
    return calculate_cagr(start_sales, end_sales, years)


# ==========================================================
# PAT CAGR
# ==========================================================

def pat_cagr(start_pat, end_pat, years):
    return calculate_cagr(start_pat, end_pat, years)


# ==========================================================
# EPS CAGR
# ==========================================================

def eps_cagr(start_eps, end_eps, years):
    return calculate_cagr(start_eps, end_eps, years)