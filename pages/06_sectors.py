"""
Sprint 4
Day 22

Sector Analysis Page
"""

import streamlit as st
from src.dashboard.utils.db import get_sectors

st.title("🏭 Sector Analysis")

st.write("""
Analyze companies sector-wise.

Bubble charts and sector KPIs
will be implemented on Day 25.
""")

try:
    sectors = get_sectors()

    if "broad_sector" in sectors.columns:
        sector_list = sorted(sectors["broad_sector"].dropna().unique())
    else:
        sector_list = []

except Exception:
    sector_list = []

selected_sector = st.selectbox(
    "Select Sector",
    sector_list
)

if selected_sector:
    st.success(f"Selected Sector: {selected_sector}")

st.subheader("Upcoming Features")

st.markdown("""
- Sector Bubble Chart
- Sector Median KPIs
- Revenue Distribution
- ROE Comparison
- Market Cap Analysis
- Sub-sector Comparison
""")

st.info("Sector Analysis page scaffold completed.")