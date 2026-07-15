"""
Sprint 4
Day 22

Trend Analysis Page
"""

import streamlit as st
from src.dashboard.utils.db import get_companies

st.title("📈 Trend Analysis")

st.write("""
Analyze long-term financial trends for any company.

Detailed charts and multi-metric comparisons
will be implemented on Day 25.
""")

# Load company list
try:
    companies = get_companies()
    company_names = companies["company_name"].tolist()
except Exception:
    company_names = []

selected_company = st.selectbox(
    "Select Company",
    company_names
)

st.success(f"Selected Company: {selected_company}" if selected_company else "No company selected.")

st.subheader("Upcoming Features")

st.markdown("""
- 10-Year Revenue Trend
- Net Profit Trend
- ROE Trend
- ROCE Trend
- Multi Metric Overlay
- YoY Growth %
- Interactive Plotly Charts
""")

st.info("Trend Analysis page scaffold completed.")