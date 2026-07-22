"""
=========================================================
Dashboard Helper Utilities
Sprint 4 – Day 27
=========================================================

This module contains reusable helper functions used
across all dashboard pages.

Functions:
----------
safe_value()
safe_dataframe()
show_data_warning()
measure_load_time()
safe_plotly_chart()
"""

from __future__ import annotations

import time
import math
from typing import Any

import pandas as pd
import streamlit as st


# =========================================================
# Safe Value Formatter
# =========================================================

def safe_value(
    value: Any,
    default: str = "N/A",
    decimals: int = 2,
    suffix: str = "",
):
    """
    Convert missing values into a friendly display string.

    Examples
    --------
    None -> "N/A"
    NaN  -> "N/A"
    15.238 -> "15.24"
    """

    if value is None:
        return default

    try:
        if pd.isna(value):
            return default
    except Exception:
        pass

    if isinstance(value, (int, float)):
        return f"{value:.{decimals}f}{suffix}"

    return str(value)


# =========================================================
# Safe DataFrame
# =========================================================

def safe_dataframe(df: pd.DataFrame | None) -> pd.DataFrame:
    """
    Always return a DataFrame.

    Prevents page crashes if SQL returns None.
    """

    if df is None:
        return pd.DataFrame()

    return df.copy()


# =========================================================
# Limited Data Warning
# =========================================================

def show_data_warning(df: pd.DataFrame, min_years: int = 10):
    """
    Show warning if company has less than required years.

    Used on Trend Analysis and Company Profile.
    """

    if df.empty:
        st.warning("No data available.")
        return

    if "year" not in df.columns:
        return

    years = df["year"].nunique()

    if years < min_years:
        st.info(
            f"Limited data available ({years} years). "
            "Charts display only available records."
        )


# =========================================================
# Page Load Timer
# =========================================================

def measure_load_time(start_time: float):
    """
    Display page load time.

    Used for QA testing.
    """

    elapsed = time.perf_counter() - start_time

    if elapsed < 3:
        st.success(f"Loaded in {elapsed:.2f} seconds")
    else:
        st.warning(f"Loaded in {elapsed:.2f} seconds")


# =========================================================
# Safe Plotly Renderer
# =========================================================

def safe_plotly_chart(fig, key=None):
    """
    Render Plotly safely.

    Prevents page crash if figure is invalid.
    """

    try:
        fig.update_layout(
            autosize=True,
            margin=dict(l=20, r=20, t=40, b=20),
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            key=key,
        )

    except Exception as exc:

        st.error("Unable to render chart.")

        with st.expander("Technical Details"):
            st.exception(exc)


# =========================================================
# Safe Metric Card
# =========================================================

def safe_metric(label: str, value, suffix: str = ""):
    """
    Streamlit metric that never crashes.
    """

    st.metric(
        label,
        safe_value(value, suffix=suffix),
    )


# =========================================================
# Safe Column Lookup
# =========================================================

def get_value(df: pd.DataFrame, column: str, default=None):
    """
    Read first row safely.

    Example
    -------
    roe = get_value(df, "return_on_equity_pct")
    """

    if df.empty:
        return default

    if column not in df.columns:
        return default

    return df.iloc[0][column]


# =========================================================
# Empty Data Message
# =========================================================

def show_empty_message(message="No data available"):
    """
    Standard empty-data UI.
    """

    st.info(message)


# =========================================================
# Validate Required Columns
# =========================================================

def validate_columns(df, required_columns):
    """
    Ensure required columns exist.

    Returns True if valid.
    """

    missing = [
        c for c in required_columns
        if c not in df.columns
    ]

    if missing:
        st.error(
            "Missing columns:\n"
            + ", ".join(missing)
        )
        return False

    return True