"""
Sprint 4
Day 22

Financial Screener Page

This is the scaffold page.
Interactive filters and exports will be implemented on Day 24.
"""

import streamlit as st
from src.dashboard.utils.db import get_companies

# --------------------------------------------------
# PAGE TITLE
# --------------------------------------------------

st.title("📊 Financial Screener")

st.write("""
Welcome to the Financial Screener.

This page will allow users to filter companies
using various financial metrics.
""")

# --------------------------------------------------
# LOAD COMPANIES
# --------------------------------------------------

try:
    companies = get_companies()

    company_count = len(companies)

except Exception:
    companies = None
    company_count = 0

# --------------------------------------------------
# DASHBOARD SUMMARY
# --------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Companies Loaded",
        value=company_count
    )

with col2:
    st.metric(
        label="Preset Screeners",
        value="6"
    )

with col3:
    st.metric(
        label="Filter Metrics",
        value="10+"
    )

# --------------------------------------------------
# PLACEHOLDER FILTERS
# --------------------------------------------------

st.subheader("Available Filters")

filters = [
    "ROE",
    "Debt to Equity",
    "Revenue CAGR",
    "PAT CAGR",
    "Operating Profit Margin",
    "P/E",
    "P/B",
    "Dividend Yield",
    "Interest Coverage",
    "Free Cash Flow"
]

for item in filters:
    st.checkbox(item, value=False, disabled=True)

# --------------------------------------------------
# PLACEHOLDER TABLE
# --------------------------------------------------

st.subheader("Preview")

if companies is not None:
    st.dataframe(companies.head())

st.info("""
Day 24 will include:

• Interactive sliders

• Preset screeners

• Live filtering

• CSV Download

• Composite Score Sorting
""")