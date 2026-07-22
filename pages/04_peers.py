"""
Sprint 4
Day 22

Peer Comparison

Scaffold Page

Radar charts and peer analytics
will be implemented on Day 24.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from src.dashboard.utils.db import (
    get_peer_groups,
    get_peer_companies,
    get_peer_company_metrics,
    get_peer_average_metrics,
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
    page_title="Peer Comparison",
    page_icon="👥",
    layout="wide",
)

st.title("👥 Peer Comparison")

st.write(
    """
Compare a company with the average performance
of companies in the same peer group.
"""
)

# -------------------------------------------------------
# Peer Group Dropdown
# -------------------------------------------------------

peer_df = get_peer_groups()

if peer_df.empty:
    st.warning("No peer groups found.")
    st.stop()

peer_group = st.selectbox(
    "Select Peer Group",
    peer_df["peer_group_name"]
)

# -------------------------------------------------------
# Company Dropdown
# -------------------------------------------------------

companies = get_peer_companies(peer_group)

if companies.empty:
    st.info("No companies available in this peer group.")
    st.stop()

company = st.selectbox(
    "Select Company",
    companies["company_id"]
)

# -------------------------------------------------------
# Load Metrics
# -------------------------------------------------------

company_metrics = get_peer_company_metrics(company)

peer_average = get_peer_average_metrics(peer_group)

if company_metrics.empty:
    st.warning("No financial metrics available.")
    st.stop()

if peer_average.empty:
    st.warning("Peer average not available.")
    st.stop()

company_row = company_metrics.iloc[0]
peer_row = peer_average.iloc[0]

st.subheader("📈 Radar Comparison")

categories = [

    "ROE",
    "NPM",
    "Debt/Equity",
    "FCF",
    "Revenue CAGR",
    "PAT CAGR",
    "Asset Turnover",
    "Quality Score",

]

company_values = [

    company_row["return_on_equity_pct"],
    company_row["net_profit_margin_pct"],
    company_row["debt_to_equity"],
    company_row["free_cash_flow_cr"],
    company_row["revenue_cagr_5yr"],
    company_row["pat_cagr_5yr"],
    company_row["asset_turnover"],
    company_row["composite_quality_score"],

]

peer_values = [

    peer_row["roe"],
    peer_row["npm"],
    peer_row["de"],
    peer_row["fcf"],
    peer_row["revenue"],
    peer_row["pat"],
    peer_row["turnover"],
    peer_row["score"],

]

fig = go.Figure()

fig.add_trace(

    go.Scatterpolar(

        r=company_values,

        theta=categories,

        fill="toself",

        name=company,

    )

)

fig.add_trace(

    go.Scatterpolar(

        r=peer_values,

        theta=categories,

        fill="toself",

        name="Peer Average",

    )

)

fig.update_layout(

    polar=dict(
        radialaxis=dict(
            visible=True
        )
    ),

    showlegend=True,

    height=600,

)

st.plotly_chart(
    fig,
    use_container_width=True,
)

st.subheader("📊 KPI Comparison")

comparison = pd.DataFrame({

    "Metric": categories,

    "Selected Company": company_values,

    "Peer Average": peer_values,

})

st.dataframe(

    comparison,

    use_container_width=True,

    hide_index=True,

)

st.subheader("🏆 Companies in Peer Group")

table = companies.copy()

table["Benchmark"] = table["company_id"].apply(

    lambda x: "⭐" if x == company else ""

)

def highlight(row):

    if row["company_id"] == company:

        return [

            "background-color:#FFD966"

        ] * len(row)

    return [""] * len(row)

st.dataframe(

    table.style.apply(highlight, axis=1),

    use_container_width=True,

)

st.info(

    "The selected company is highlighted in gold. "
    "The radar chart compares its performance "
    "against the peer-group average."

)