"""
Sprint 4
Day 22

Sector Analysis Page
"""
import streamlit as st
import pandas as pd
import plotly.express as px

from src.dashboard.utils.db import (
    get_sector_list,
    get_sector_data,
    get_sector_medians,
)

# -----------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------

st.set_page_config(
    page_title="Sector Analysis",
    page_icon="🏭",
    layout="wide",
)

st.title("🏭 Sector Analysis")

st.markdown(
    """
Compare companies within a sector using interactive visualizations.

**Bubble Chart**
- X Axis → Revenue
- Y Axis → ROE
- Bubble Size → Market Cap
- Bubble Color → Sub-sector
"""
)

# -----------------------------------------------------
# LOAD SECTOR LIST
# -----------------------------------------------------

sector_df = get_sector_list()

if sector_df.empty:
    st.error("No sectors found in database.")
    st.stop()

sector = st.selectbox(
    "Select Sector",
    sorted(sector_df["broad_sector"].unique())
)

# -----------------------------------------------------
# LOAD DATA
# -----------------------------------------------------

df = get_sector_data(sector)

if df.empty:
    st.warning("No data available for this sector.")
    st.stop()

# -----------------------------------------------------
# CLEAN DATA
# -----------------------------------------------------

numeric_columns = [
    "sales",
    "return_on_equity_pct",
    "market_cap",
]

for col in numeric_columns:

    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.fillna(0)

# -----------------------------------------------------
# BUBBLE CHART
# -----------------------------------------------------

st.subheader("📊 Revenue vs ROE")

size_column = "market_cap" if "market_cap" in df.columns else None
if "market_cap" in df.columns:

    fig = px.scatter(
        df,
        x="sales",
        y="return_on_equity_pct",
        size="market_cap",
        color="sub_sector",
        hover_name="company_name",
        text="company_name",
    )

else:

    fig = px.scatter(
        df,
        x="sales",
        y="return_on_equity_pct",
        color="sub_sector",
        hover_name="company_name",
        text="company_name",
    )

fig = px.scatter(

    df,

    x="sales",

    y="return_on_equity_pct",

    size=size_column,

    color="sub_sector",

    hover_name="company_name",

    text="company_name",

)

fig.update_traces(

    textposition="top center",

)

fig.update_layout(

    template="plotly_white",

    height=650,

    xaxis_title="Revenue",

    yaxis_title="Return on Equity (%)",

)

st.plotly_chart(

    fig,

    use_container_width=True,

)

# -----------------------------------------------------
# SUMMARY
# -----------------------------------------------------

col1, col2, col3 = st.columns(3)

col1.metric(

    "Companies",

    len(df),

)

col2.metric(

    "Average ROE",

    f"{df['return_on_equity_pct'].mean():.2f}%",

)

col3.metric(

    "Total Revenue",

    f"{df['sales'].sum():,.0f}",

)

# -----------------------------------------------------
# MEDIAN KPI
# -----------------------------------------------------

st.subheader("📈 Sector Median KPIs")

median_df = get_sector_medians(sector)

if not median_df.empty:

    melted = median_df.melt(

        var_name="Metric",

        value_name="Value"

    )

    fig_bar = px.bar(

        melted,

        x="Metric",

        y="Value",

        text="Value",

    )

    fig_bar.update_traces(

        texttemplate="%{text:.2f}",

        textposition="outside",

    )

    fig_bar.update_layout(

        template="plotly_white",

        height=500,

    )

    st.plotly_chart(

        fig_bar,

        use_container_width=True,

    )

else:

    st.info("Median KPI data not available.")

# -----------------------------------------------------
# COMPANY TABLE
# -----------------------------------------------------

st.subheader("📋 Companies in Sector")

display_columns = [

    "company_name",

    "sub_sector",

    "sales",

    "return_on_equity_pct",

]

if "market_cap" in df.columns:
    display_columns.append("market_cap")

available_columns = [c for c in display_columns if c in df.columns]

st.dataframe(

    df[available_columns],

    use_container_width=True,

    hide_index=True,

)

# -----------------------------------------------------
# DOWNLOAD
# -----------------------------------------------------

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(

    label="⬇ Download Sector Data",

    data=csv,

    file_name=f"{sector}_sector_analysis.csv",

    mime="text/csv",

)

# -----------------------------------------------------
# HELP
# -----------------------------------------------------

st.info(
    """
Bubble Size = Market Capitalization

Bubble Color = Sub-sector

Hover over a bubble to see detailed company information.
"""
)
