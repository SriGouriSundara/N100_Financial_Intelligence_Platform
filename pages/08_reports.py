"""
Sprint 4
Day 22

Annual Reports Page
"""
import streamlit as st
import pandas as pd

from src.dashboard.utils.db import (
    get_report_companies,
    get_annual_reports,
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

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Annual Reports",
    page_icon="📄",
    layout="wide",
)

st.title("📄 Annual Reports")

st.markdown(
"""
Search and open company Annual Reports from BSE.

- ✅ Available reports contain clickable links.
- ❌ Missing reports are clearly marked.
"""
)

# --------------------------------------------------
# LOAD COMPANY LIST
# --------------------------------------------------

companies = get_report_companies()

if companies.empty:
    st.error("No companies found.")
    st.stop()

# --------------------------------------------------
# SEARCH BOX
# --------------------------------------------------

search = st.text_input(
    "🔍 Search Company",
    placeholder="Enter company name or ticker"
)

filtered = companies.copy()

if search:

    search = search.lower()

    filtered = filtered[
        filtered["company_name"].str.lower().str.contains(search)
        |
        filtered["id"].str.lower().str.contains(search)
    ]

if filtered.empty:

    st.warning("Ticker not found.")

    st.stop()

# --------------------------------------------------
# COMPANY SELECTOR
# --------------------------------------------------

company_name = st.selectbox(
    "Select Company",
    filtered["company_name"]
)

company_id = filtered.loc[
    filtered["company_name"] == company_name,
    "id"
].iloc[0]

# --------------------------------------------------
# LOAD REPORTS
# --------------------------------------------------

reports = get_annual_reports(company_id)

if reports.empty:

    st.info("No Annual Reports available.")

    st.stop()

reports = reports.sort_values(
    "Year",
    ascending=False
)

# --------------------------------------------------
# DISPLAY REPORTS
# --------------------------------------------------

st.subheader(f"📑 {company_name}")

st.divider()

for _, row in reports.iterrows():

    year = row["Year"]

    url = str(row["Annual_Report"]).strip()

    c1, c2, c3 = st.columns([1,5,2])

    c1.write(year)

    if (
        pd.notna(url)
        and
        url != ""
        and
        url.lower() != "null"
    ):

        c2.markdown(
            f"🔗 [Open Annual Report]({url})"
        )

        c3.success("Available")

    else:

        c2.write("-")

        c3.error("Unavailable")

# --------------------------------------------------
# DOWNLOAD REPORT LIST
# --------------------------------------------------

download_df = reports.copy()

csv = download_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="⬇ Download Report List",
    data=csv,
    file_name=f"{company_id}_annual_reports.csv",
    mime="text/csv",
)

# --------------------------------------------------
# SUMMARY
# --------------------------------------------------

available = reports["Annual_Report"].fillna("").astype(str)

available = available[
    (available != "")
    &
    (available.str.lower() != "null")
]

missing = len(reports) - len(available)

st.divider()

c1, c2, c3 = st.columns(3)

c1.metric(
    "Total Reports",
    len(reports)
)

c2.metric(
    "Available",
    len(available)
)

c3.metric(
    "Unavailable",
    missing
)

st.info(
"""
Annual Reports are sourced from the **documents** table in the SQLite database.

Reports marked **Available** contain valid BSE report links stored in the database.

Reports marked **Unavailable** have no URL stored.
"""
)