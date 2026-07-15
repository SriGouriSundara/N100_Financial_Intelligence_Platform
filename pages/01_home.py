"""
Sprint 4
Day 22

Home Page

This is the landing page of the dashboard.
Detailed KPIs and charts will be added on Day 23.
"""

import streamlit as st

# -----------------------------------------------------
# PAGE TITLE
# -----------------------------------------------------

st.title("🏠 Home")

st.markdown(
"""
Welcome to the **N100 Financial Intelligence Platform**.

This dashboard provides financial analytics for the Nifty 100 companies.

Use the navigation menu on the left to explore the dashboard.
"""
)

# -----------------------------------------------------
# PROJECT INFORMATION
# -----------------------------------------------------

st.subheader("Project Overview")

col1, col2 = st.columns(2)

with col1:
    st.info(
        """
        **Project**

        Bluestock N100 Mutual Fund Analytics
        """
    )

with col2:
    st.info(
        """
        **Database**

        SQLite

        92 Companies

        10+ Tables
        """
    )

# -----------------------------------------------------
# UPCOMING FEATURES
# -----------------------------------------------------

st.subheader("Upcoming Dashboard Features")

features = [
    "Company Profile",
    "Financial Screener",
    "Peer Comparison",
    "Trend Analysis",
    "Sector Analysis",
    "Capital Allocation",
    "Annual Reports",
]

for feature in features:
    st.checkbox(feature, value=False, disabled=True)

st.success("Home page loaded successfully.")