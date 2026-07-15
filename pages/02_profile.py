"""
Sprint 4
Day 22

Company Profile Page

Actual charts and KPIs will be added on Day 23.
"""

import streamlit as st

from src.dashboard.utils.db import get_companies

# -----------------------------------------------------
# TITLE
# -----------------------------------------------------

st.title("🏢 Company Profile")

st.write(
    """
    Search and view company details.

    This page will display
    company information,
    KPIs,
    charts,
    and financial statements.
    """
)

# -----------------------------------------------------
# LOAD COMPANY LIST
# -----------------------------------------------------

try:

    companies = get_companies()

    company_names = companies["company_name"].tolist()

except Exception:

    company_names = []

# -----------------------------------------------------
# SEARCH BOX
# -----------------------------------------------------

selected_company = st.selectbox(

    "Select Company",

    company_names

)

# -----------------------------------------------------
# DISPLAY
# -----------------------------------------------------

if selected_company:

    st.success(

        f"Selected Company : {selected_company}"

    )

    st.info(

        """
        Day 23 will display:

        • Company Card

        • KPIs

        • Revenue Chart

        • Profit Chart

        • ROE Trend

        • ROCE Trend

        • Pros

        • Cons
        """

    )

else:

    st.warning(

        "No company selected."

    )