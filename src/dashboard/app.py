import streamlit as st
from pathlib import Path

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Nifty 100 Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# FIND PROJECT ROOT
# -----------------------------
ROOT = Path(__file__).resolve().parents[2]

PAGES = ROOT / "pages"

# -----------------------------
# DEFINE ALL PAGES
# -----------------------------
home = st.Page(
    str(PAGES / "01_home.py"),
    title="Home",
    icon="🏠",
    default=True,
)

profile = st.Page(
    str(PAGES / "02_profile.py"),
    title="Company Profile",
    icon="🏢",
)

screener = st.Page(
    str(PAGES / "03_screener.py"),
    title="Financial Screener",
    icon="📊",
)

peers = st.Page(
    str(PAGES / "04_peers.py"),
    title="Peer Comparison",
    icon="👥",
)

trends = st.Page(
    str(PAGES / "05_trends.py"),
    title="Trend Analysis",
    icon="📈",
)

sectors = st.Page(
    str(PAGES / "06_sectors.py"),
    title="Sector Analysis",
    icon="🏭",
)

capital = st.Page(
    str(PAGES / "07_capital.py"),
    title="Capital Allocation",
    icon="💰",
)

reports = st.Page(
    str(PAGES / "08_reports.py"),
    title="Annual Reports",
    icon="📄",
)

# -----------------------------
# NAVIGATION
# -----------------------------
pg = st.navigation(
    [
        home,
        profile,
        screener,
        peers,
        trends,
        sectors,
        capital,
        reports,
    ]
)

pg.run()