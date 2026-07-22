"""
=========================================================
Sprint 4 - Day 23
Profile Page
=========================================================
"""
from pathlib import Path
import sys
# Project root
ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.dashboard.utils.db import (
     search_company,
    get_company_profile,
    get_company_kpis,
    get_company_trends,
    get_company_pros_cons,
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

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.title("🏢 Company Profile")

# Sidebar

year = st.sidebar.selectbox(
    "Financial Year",
    [2019,2020,2021,2022,2023,2024],
    index=5
)
# -----------------------------------
# Company Search with Autocomplete
# -----------------------------------

search = st.text_input(
    "Search Company ID or Name",
    placeholder="Type TCS, RELIANCE, INFY..."
)

if search.strip() == "":
    st.info("👈 Type a company name or ticker.")
    st.stop()

# Search matching companies
matches = search_company(search)

# No matching company
if matches.empty:
    st.warning("⚠️ Ticker not found — please try another.")
    st.stop()

# Create dropdown options
options = (
    matches["id"] + " - " + matches["company_name"]
).tolist()

selected = st.selectbox(
    "Matching Companies",
    options,
    key="company_dropdown"
)

# Extract company ID
company_id = selected.split(" - ")[0]

company_id = matches.iloc[0]["id"]

profile = get_company_profile(company_id)

kpi = get_company_kpis(company_id, year)

trend = get_company_trends(company_id)

pros_cons = get_company_pros_cons(company_id)

st.subheader(profile.iloc[0]["company_name"])

col1,col2 = st.columns(2)

with col1:

    st.write("**Company ID**")

    st.write(profile.iloc[0]["id"])

    st.write("**Sector**")

    st.write(profile.iloc[0]["broad_sector"])

    st.write("**Sub Sector**")

    st.write(profile.iloc[0]["sub_sector"])

with col2:

    st.write("**Website**")

    st.write(profile.iloc[0]["website"])

st.write(profile.iloc[0]["about_company"])

st.subheader("Key Metrics")

c1,c2,c3 = st.columns(3)

c4,c5,c6 = st.columns(3)

c1.metric("ROE",f"{kpi.iloc[0]['return_on_equity_pct']:.2f}%")

c2.metric("NPM",f"{kpi.iloc[0]['net_profit_margin_pct']:.2f}%")

c3.metric("D/E",f"{kpi.iloc[0]['debt_to_equity']:.2f}")

c4.metric("Revenue CAGR",f"{kpi.iloc[0]['revenue_cagr_5yr']:.2f}%")

c5.metric("Free Cash Flow",f"{kpi.iloc[0]['free_cash_flow_cr']:.2f}")

c6.metric("Composite Score",f"{kpi.iloc[0]['composite_quality_score']:.2f}")

st.subheader("Revenue vs Net Profit")

fig = px.bar(

    trend,

    x="year_pl",

    y=["sales","net_profit"],

    barmode="group"

)

st.plotly_chart(fig,use_container_width=True)
st.subheader("ROE Trend")

trend = get_company_trends(company_id)

if trend.empty:
    st.info("No historical trend data available.")
else:
    # Remove rows without ROE
    trend = trend.dropna(subset=["return_on_equity_pct"])

    fig = go.Figure()

    # ROE Line
    fig.add_trace(
        go.Scatter(
            x=trend["year_pl"],
            y=trend["return_on_equity_pct"],
            mode="lines+markers",
            name="ROE",
        )
    )

    # Composite Score Line
    fig.add_trace(
        go.Scatter(
            x=trend["year_pl"],
            y=trend["composite_quality_score"],
            mode="lines+markers",
            name="Composite Score",
            yaxis="y2",
        )
    )

    fig.update_layout(
        title="ROE vs Composite Score",
        xaxis_title="Year",
        yaxis=dict(title="ROE (%)"),
        yaxis2=dict(
            title="Composite Score",
            overlaying="y",
            side="right",
        ),
        hovermode="x unified",
        height=450,
    )

    st.plotly_chart(fig, use_container_width=True)
st.subheader("Pros")

for item in pros_cons["pros"]:

    st.success(item)

st.subheader("Cons")

for item in pros_cons["cons"]:

    st.error(item)

