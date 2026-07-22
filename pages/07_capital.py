"""
Sprint 4
Day 22

Capital Allocation Page
"""
import os
import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------

st.set_page_config(
    page_title="Capital Allocation",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Capital Allocation Map")

st.markdown(
    """
Visualize all companies based on their capital allocation pattern.

The treemap groups companies into capital allocation categories.

Click a category below to view all companies belonging to that pattern.
"""
)

# -----------------------------------------------------
# LOAD CSV
# -----------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

csv_path = os.path.join(
    BASE_DIR,
    "output",
    "capital_allocation.csv"
)

if not os.path.exists(csv_path):

    st.error("capital_allocation.csv not found.")

    st.stop()

df = pd.read_csv(csv_path)

if df.empty:

    st.warning("Capital Allocation data is empty.")

    st.stop()
required_columns = [

    "company_id",

    "year",

    "pattern_label"

]

missing = [

    c for c in required_columns

    if c not in df.columns

]

if missing:

    st.error(

        f"Missing columns: {missing}"

    )

    st.stop()    
latest_year = df["year"].max()

latest_df = df[

    df["year"] == latest_year

].copy()

summary = (

    latest_df

    .groupby("pattern_label")

    .size()

    .reset_index(name="Company Count")

)

summary = summary.sort_values(

    "Company Count",

    ascending=False

)

st.subheader("📊 Capital Allocation Treemap")

fig = px.treemap(

    summary,

    path=["pattern_label"],

    values="Company Count",

    color="Company Count",

    hover_data=["Company Count"]

)

fig.update_layout(

    height=650

)

st.plotly_chart(

    fig,

    use_container_width=True

)

st.subheader("📂 Explore Pattern")

selected_pattern = st.selectbox(

    "Select Capital Allocation Pattern",

    sorted(summary["pattern_label"].unique())

)

companies = latest_df[

    latest_df["pattern_label"]

    == selected_pattern

].copy()

companies = companies.sort_values(

    "company_id"

)

c1, c2 = st.columns(2)

c1.metric(

    "Pattern",

    selected_pattern

)

c2.metric(

    "Companies",

    len(companies)

)

st.subheader("🏢 Companies")

st.dataframe(

    companies,

    use_container_width=True,

    hide_index=True

)

csv = companies.to_csv(

    index=False

).encode("utf-8")

st.download_button(

    "⬇ Download Companies",

    csv,

    file_name=f"{selected_pattern}.csv",

    mime="text/csv"

)

st.subheader("📈 Pattern Distribution")

bar = px.bar(

    summary,

    x="pattern_label",

    y="Company Count",

    text="Company Count"

)

bar.update_layout(

    xaxis_title="Pattern",

    yaxis_title="Companies",

    height=450

)

st.plotly_chart(

    bar,

    use_container_width=True

)

st.subheader("📋 Pattern Summary")

st.dataframe(

    summary,

    use_container_width=True,

    hide_index=True

)
st.info(

"""
Capital Allocation Patterns are generated during Sprint 2.

Examples include:

• Reinvestor

• Shareholder Returns

• Growth Funded by Debt

• Cash Accumulator

• Liquidating Assets

• Distress Signal

• Mixed

• Pre-Revenue

Use this page to quickly identify companies with similar capital deployment behaviour.

"""

)
