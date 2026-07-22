"""
Sprint 4
Day 22

Financial Screener Page

This is the scaffold page.
Interactive filters and exports will be implemented on Day 24.
"""

import streamlit as st
import pandas as pd
from src.dashboard.utils.db import (
    get_screener_data,
    apply_filters,
    apply_preset,
    export_csv,
)
from src.dashboard.utils.helpers import (
    safe_value,
    safe_dataframe,
    show_data_warning,
    measure_load_time,
    safe_plotly_chart,
    safe_metric,
    show_empty_message,
)

# -------------------------------------------------------
# Page Configuration
# -------------------------------------------------------

st.set_page_config(
    page_title="Financial Screener",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Financial Screener")

st.write(
    """
Use the sidebar filters to discover companies
matching your investment criteria.
"""
)

# -------------------------------------------------------
# Sidebar
# -------------------------------------------------------

st.sidebar.header("Screener Filters")

year = st.sidebar.selectbox(
    "Financial Year",
    [2019, 2020, 2021, 2022, 2023, 2024],
    index=5,
)

# -------------------------------------------------------
# Load Data
# -------------------------------------------------------

df = get_screener_data(year)

if df.empty:
    st.warning("No financial data available.")
    st.stop()

# -------------------------------------------------------
# Sidebar Sliders
# -------------------------------------------------------

roe = st.sidebar.slider(
    "Minimum ROE (%)",
    -100.0,
    500.0,
    15.0,
)

de = st.sidebar.slider(
    "Maximum Debt/Equity",
    0.0,
    10.0,
    2.0,
)

fcf = st.sidebar.slider(
    "Minimum Free Cash Flow",
    -50000.0,
    50000.0,
    0.0,
)

revenue = st.sidebar.slider(
    "Revenue CAGR 5Y (%)",
    -50.0,
    100.0,
    10.0,
)

pat = st.sidebar.slider(
    "PAT CAGR 5Y (%)",
    -50.0,
    100.0,
    10.0,
)

opm = st.sidebar.slider(
    "Operating Margin (%)",
    -50.0,
    100.0,
    10.0,
)

# -------------------------------------------------------
# Placeholder sliders
# (Implemented in Day 26)
# -------------------------------------------------------

st.sidebar.markdown("---")

st.sidebar.caption("Available after Day 26")

st.sidebar.slider(
    "Maximum P/E",
    0.0,
    100.0,
    20.0,
    disabled=True,
)

st.sidebar.slider(
    "Maximum P/B",
    0.0,
    20.0,
    3.0,
    disabled=True,
)

st.sidebar.slider(
    "Dividend Yield (%)",
    0.0,
    10.0,
    2.0,
    disabled=True,
)

icr = st.sidebar.slider(
    "Interest Coverage",
    0.0,
    20.0,
    2.0,
)

# -------------------------------------------------------
# Preset Screeners
# -------------------------------------------------------

st.subheader("Preset Screeners")

col1, col2, col3 = st.columns(3)

quality = col1.button("🏆 Quality")

growth = col2.button("🚀 Growth")

dividend = col3.button("💰 Dividend")

col4, col5, col6 = st.columns(3)

debtfree = col4.button("✅ Debt Free")

turnaround = col5.button("📈 Turnaround")

value = col6.button("💎 Value")

filtered = df.copy()

# -------------------------------------------------------
# Preset Logic
# -------------------------------------------------------

if quality:

    filtered = apply_preset(df, "Quality")

elif growth:

    filtered = apply_preset(df, "Growth")

elif dividend:

    filtered = apply_preset(df, "Dividend")

elif debtfree:

    filtered = apply_preset(df, "Debt Free")

elif turnaround:

    filtered = apply_preset(df, "Turnaround")

else:

    filtered = apply_filters(
        df,
        roe,
        de,
        fcf,
        revenue,
        pat,
        opm,
        icr,
    )

# -------------------------------------------------------
# Result Count
# -------------------------------------------------------

st.success(
    f"{len(filtered)} companies match your filters."
)

# -------------------------------------------------------
# Sort
# -------------------------------------------------------

filtered = filtered.sort_values(
    by="composite_quality_score",
    ascending=False,
)

# -------------------------------------------------------
# Display Columns
# -------------------------------------------------------

columns = [

    "company_id",

    "company_name",

    "broad_sector",

    "return_on_equity_pct",

    "debt_to_equity",

    "free_cash_flow_cr",

    "revenue_cagr_5yr",

    "pat_cagr_5yr",

    "operating_profit_margin_pct",

    "interest_coverage",

    "composite_quality_score",

]

st.dataframe(

    filtered[columns],

    use_container_width=True,

    hide_index=True,

)

# -------------------------------------------------------
# Download CSV
# -------------------------------------------------------

csv = export_csv(filtered)

st.download_button(

    label="⬇ Download CSV",

    data=csv,

    file_name="screener_results.csv",

    mime="text/csv",

)