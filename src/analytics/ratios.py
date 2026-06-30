"""
Sprint 2 - Day 08
Profitability Ratio Engine

This module contains functions to calculate profitability ratios
for the N100 Financial Intelligence Platform.

"""
import logging
from pathlib import Path

output_folder = Path("output")
output_folder.mkdir(exist_ok=True)

log_file = output_folder / "ratio_edge_cases.log"

logger = logging.getLogger("ratio_engine")
logger.setLevel(logging.INFO)

# Prevent duplicate handlers
if not logger.handlers:
    file_handler = logging.FileHandler(log_file, mode="a")
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

# FUNCTION 1:

def net_profit_margin(net_profit, sales):

    """
    Calculate Net Profit Margin.
    Formula:
    (Net Profit / Sales) * 100
    Returns:
        float : Net Profit Margin (%)
        None  : If sales is zero
    """
    if sales == 0:
        return None
    return (net_profit / sales) * 100


# FUNCTION 2:

def operating_profit_margin(operating_profit, sales):
    """
    Calculate Operating Profit Margin.
    Formula:
    (Operating Profit / Sales) * 100
    Returns:
        float : Operating Profit Margin (%)
        None  : If sales is zero
    """
    if sales == 0:
        return None
    return (operating_profit / sales) * 100


# FUNCTION 3:

def check_opm_difference(
    company_name,
    year,
    calculated_opm,
    source_opm
):
    """
    Compare calculated OPM with source OPM.
    If difference is greater than 1%,
    write a message into ratio_edge_cases.log.
    Returns:
        True  -> Difference greater than 1%
        False -> Difference within limit
    """
    difference = abs(calculated_opm - source_opm)
    if difference > 1:
        logger.info(
                f"{company_name} | "
                f"Year={year} | "
                f"Calculated OPM={calculated_opm:.2f}% | "
                f"Source OPM={source_opm:.2f}% | "
                f"Difference={difference:.2f}%"

        )
        return True
    return False


# FUNCTION 4:

def return_on_equity(net_profit, equity_capital, reserves):
    """
    Calculate Return on Equity (ROE).
    Formula:
    Net Profit / (Equity + Reserves) * 100
    Returns:
        float : ROE
        None  : If Equity + Reserves <= 0
    """
    total_equity = equity_capital + reserves
    if total_equity <= 0:
        return None
    return (net_profit / total_equity) * 100


# FUNCTION 5:

def return_on_capital_employed(
    ebit,
    equity_capital,
    reserves,
    borrowings,
    broad_sector=None
):
    """
    Calculate Return on Capital Employed (ROCE).
    Formula:
    EBIT / (Equity + Reserves + Borrowings) * 100
    Note:
    For Financials sector, benchmark comparison
    will be handled later (Day 13).
    """
    capital_employed = (
        equity_capital +
        reserves +
        borrowings
    )
    if capital_employed <= 0:
        return None
    roce = (ebit / capital_employed) * 100
    return roce

# FUNCTION 6:

def return_on_assets(net_profit, total_assets):
    """
    Calculate Return on Assets (ROA).
    Formula:
    Net Profit / Total Assets * 100
    Returns:
        float : ROA
        None  : If total assets is zero
    """
    if total_assets == 0:
        return None
    return (net_profit / total_assets) * 100