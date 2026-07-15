"""
Sprint 4
Day 22

Peer Comparison

Scaffold Page

Radar charts and peer analytics
will be implemented on Day 24.
"""

import streamlit as st
from src.dashboard.utils.db import get_companies

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("👥 Peer Comparison")

st.write("""
Compare a company with its peer group.

Radar charts and percentile rankings
will be available in Day 24.
""")

# --------------------------------------------------
# COMPANY LIST
# --------------------------------------------------

try:

    companies = get_companies()

    company_names = companies["company_name"].tolist()

except Exception:

    company_names = []

# --------------------------------------------------
# COMPANY SELECTION
# --------------------------------------------------

selected = st.selectbox(

    "Choose Company",

    company_names

)

# --------------------------------------------------
# PLACEHOLDER
# --------------------------------------------------

if selected:

    st.success(

        f"Selected : {selected}"

    )

st.subheader("Upcoming Features")

features = [

    "Radar Chart",

    "Peer Ranking",

    "Percentile Score",

    "Benchmark Comparison",

    "Peer KPI Table"

]

for item in features:

    st.checkbox(

        item,

        value=False,

        disabled=True

    )

st.info(
    """
    Day 24 Implementation

    • Radar Chart

    • Plotly Charts

    • Peer Ranking

    • Percentiles

    • Benchmark Highlight
    """
)