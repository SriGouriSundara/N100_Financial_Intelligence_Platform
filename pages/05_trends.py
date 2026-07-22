"""
Sprint 4
Day 22

Trend Analysis Page
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from src.dashboard.utils.db import (
    get_trend_companies,
    get_trend_metrics,
    get_company_timeseries,
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

# --------------------------------------------------------
# Page Configuration
# --------------------------------------------------------

st.set_page_config(
    page_title="Trend Analysis",
    page_icon="📈",
    layout="wide",
)

st.title("📈 Trend Analysis")

st.write(
    """
Compare financial metrics over time for a selected company.
Select up to three metrics to overlay on a single interactive chart.
"""
)

# --------------------------------------------------------
# Company Search
# --------------------------------------------------------

companies = get_trend_companies()

if companies.empty:
    st.error("No companies found.")
    st.stop()

company_name = st.selectbox(
    "Select Company",
    companies["company_name"]
)

company_id = companies.loc[
    companies["company_name"] == company_name,
    "id"
].iloc[0]

# --------------------------------------------------------
# Metric Selector
# --------------------------------------------------------

metric_dict = get_trend_metrics()

selected_metrics = st.multiselect(
    "Select up to 3 Metrics",
    list(metric_dict.keys()),
    default=["Revenue"],
    max_selections=3,
)

if len(selected_metrics) == 0:
    st.warning("Please select at least one metric.")
    st.stop()

# --------------------------------------------------------
# Load Data
# --------------------------------------------------------

df = get_company_timeseries(company_id)

if df.empty:
    st.warning("No historical data available.")
    st.stop()

df = df.sort_values("year")

fig = go.Figure()

for metric in selected_metrics:

    column = metric_dict[metric]

    if column not in df.columns:
        continue

    plot_df = df[["year", column]].copy()

    plot_df = plot_df.dropna()

    if plot_df.empty:
        continue

    fig.add_trace(

        go.Scatter(

            x=plot_df["year"],

            y=plot_df[column],

            mode="lines+markers",

            name=metric,

        )

    )

fig.update_layout(

    title=f"{company_name} Financial Trends",

    xaxis_title="Year",

    yaxis_title="Metric Value",

    hovermode="x unified",

    legend_title="Metrics",

    template="plotly_white",

    height=650,

)

st.plotly_chart(
    fig,
    use_container_width=True,
)
st.subheader("📊 Year-over-Year (YoY) Change")

for metric in selected_metrics:

    column = metric_dict[metric]

    if column not in df.columns:
        continue

    yoy = df[["year", column]].copy()

    yoy = yoy.dropna()

    if len(yoy) < 2:
        continue

    yoy["YoY %"] = yoy[column].pct_change() * 100

    st.markdown(f"### {metric}")

    display = yoy.copy()

    display["YoY %"] = display["YoY %"].round(2)

    st.dataframe(
        display,
        use_container_width=True,
        hide_index=True,
    )
fig = go.Figure()

for metric in selected_metrics:

    column = metric_dict[metric]

    if column not in df.columns:
        continue

    temp = df[["year", column]].dropna().copy()

    if temp.empty:
        continue

    temp["YoY"] = temp[column].pct_change() * 100

    fig.add_trace(

        go.Scatter(

            x=temp["year"],

            y=temp[column],

            mode="lines+markers+text",

            text=[
                "" if pd.isna(x) else f"{x:.1f}%"
                for x in temp["YoY"]
            ],

            textposition="top center",

            name=metric,

        )

    )

fig.update_layout(

    template="plotly_white",

    hovermode="x unified",

    height=650,

)

st.plotly_chart(
    fig,
    use_container_width=True,
)

st.subheader("📄 Raw Data")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True,
)

st.info(
    """
• Select up to three metrics to compare trends.
• Hover over the chart for exact values.
• YoY percentages are calculated automatically.
• Missing values are ignored to prevent chart errors.
"""
)
