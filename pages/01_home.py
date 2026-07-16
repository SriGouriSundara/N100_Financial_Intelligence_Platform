"""
=========================================================
Sprint 4 - Day 23
Home Dashboard
=========================================================
"""

from pathlib import Path
import sys

# Project root
ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.dashboard.utils.db import (
    get_dashboard_summary,
    get_sector_distribution,
    get_top_companies,
)

import streamlit as st
import plotly.express as px
# ---------------------------------------------------
# Page Heading
# ---------------------------------------------------

st.title("🏠 Nifty 100 Analytics Dashboard")

st.markdown(
    """
Welcome to the Bluestock N100 Mutual Fund Analytics Dashboard.

Use the sidebar to explore financial insights.
"""
)

# ---------------------------------------------------
# Sidebar
# ---------------------------------------------------

st.sidebar.header("Dashboard Filters")

selected_year = st.sidebar.selectbox(
    "Select Financial Year",
    [2019, 2020, 2021, 2022, 2023, 2024],
    index=5
)

# ---------------------------------------------------
# Load Dashboard Data
# ---------------------------------------------------

summary = get_dashboard_summary(selected_year)

sector_df = get_sector_distribution()

top5 = get_top_companies(selected_year)

# ---------------------------------------------------
# Safety Check
# ---------------------------------------------------

if summary.empty:

    st.warning("No data available.")

    st.stop()

# ---------------------------------------------------
# KPI Tiles
# ---------------------------------------------------

st.subheader("📈 Dashboard Summary")

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Average ROE",
        f"{summary.iloc[0]['avg_roe']:.2f}%"
    )

with col2:

    pe = summary.iloc[0]["median_pe"]

    if pe is None:

        pe = "N/A"

    st.metric(
        "Median P/E",
        pe
    )

with col3:

    st.metric(
        "Median D/E",
        f"{summary.iloc[0]['median_de']:.2f}"
    )

col4, col5, col6 = st.columns(3)

with col4:

    st.metric(
        "Companies",
        int(summary.iloc[0]["total_companies"])
    )

with col5:

    st.metric(
        "Median Revenue CAGR",
        f"{summary.iloc[0]['median_revenue_cagr']:.2f}%"
    )

with col6:

    st.metric(
        "Debt-Free Companies",
        int(summary.iloc[0]["debt_free_companies"])
    )

st.divider()

# ---------------------------------------------------
# Donut Chart
# ---------------------------------------------------

st.subheader("🏭 Sector Distribution")

fig = px.pie(

    sector_df,

    names="broad_sector",

    values="company_count",

    hole=0.55,

    title="Companies by Sector"

)

fig.update_traces(textposition="inside")

st.plotly_chart(

    fig,

    use_container_width=True

)

st.divider()

# ---------------------------------------------------
# Top Companies
# ---------------------------------------------------

st.subheader("🏆 Top 5 Companies")

display_df = top5.copy()

display_df.columns = [

    "Company",

    "Composite Score",

    "ROE",

    "Revenue CAGR"

]

st.dataframe(

    display_df,

    use_container_width=True,

    hide_index=True

)

st.caption(
    "Top companies ranked by Composite Quality Score."
)