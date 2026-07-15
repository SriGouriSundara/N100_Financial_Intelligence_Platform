"""
Sprint 4
Day 22

Annual Reports Page
"""

import streamlit as st
from src.dashboard.utils.db import get_companies

st.title("📄 Annual Reports")

st.write("""
Browse annual reports
for every company.
""")

try:

    companies = get_companies()

    company_names = companies["company_name"].tolist()

except Exception:

    company_names = []

selected_company = st.selectbox(

    "Select Company",

    company_names

)

if selected_company:

    st.success(

        f"Selected Company: {selected_company}"

    )

st.subheader("Upcoming Features")

st.markdown("""

- Annual Report Links

- PDF Viewer

- Download Button

- Report Availability

- Financial Documents

""")

st.info("Annual Reports page scaffold completed.")