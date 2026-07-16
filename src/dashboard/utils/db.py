"""
Shared Database Functions

Used across all Streamlit pages.

Sprint 4
"""

import sqlite3
import pandas as pd
import streamlit as st
from pathlib import Path



# --------------------------------------------------
# DATABASE LOCATION
# --------------------------------------------------

ROOT = Path(__file__).resolve().parents[3]

DB_PATH = ROOT / "db" / "nifty100.db"


# --------------------------------------------------
# CONNECTION
# --------------------------------------------------

@st.cache_resource
def get_connection():

    return sqlite3.connect(DB_PATH, check_same_thread=False)


# --------------------------------------------------
# GENERIC QUERY
# --------------------------------------------------

@st.cache_data(ttl=600)
def run_query(query, params=None):

    conn = get_connection()

    if params is None:
        params = ()

    return pd.read_sql_query(
        query,
        conn,
        params=params
    )


# --------------------------------------------------
# COMPANY LIST
# --------------------------------------------------

@st.cache_data(ttl=600)
def get_companies():

    query = """
    SELECT *
    FROM companies
    ORDER BY company_name
    """

    return run_query(query)


# --------------------------------------------------
# RATIOS
# --------------------------------------------------

@st.cache_data(ttl=600)
def get_ratios(ticker, year=None):

    query = """
    SELECT *
    FROM financial_ratios fr

    JOIN companies c

    ON fr.company_id=c.company_id

    WHERE c.nse_symbol=?
    """

    params = [ticker]

    if year is not None:

        query += " AND fr.year=?"

        params.append(year)

    query += " ORDER BY fr.year"

    return run_query(query, params)


# --------------------------------------------------
# PROFIT LOSS
# --------------------------------------------------

@st.cache_data(ttl=600)
def get_pl(ticker):

    query = """

    SELECT *

    FROM profitandloss p

    JOIN companies c

    ON p.company_id=c.company_id

    WHERE c.nse_symbol=?

    ORDER BY year

    """

    return run_query(query, [ticker])


# --------------------------------------------------
# BALANCE SHEET
# --------------------------------------------------

@st.cache_data(ttl=600)
def get_bs(ticker):

    query = """

    SELECT *

    FROM balancesheet b

    JOIN companies c

    ON b.company_id=c.company_id

    WHERE c.nse_symbol=?

    ORDER BY year

    """

    return run_query(query, [ticker])


# --------------------------------------------------
# CASH FLOW
# --------------------------------------------------

@st.cache_data(ttl=600)
def get_cf(ticker):

    query = """

    SELECT *

    FROM cashflow cf

    JOIN companies c

    ON cf.company_id=c.company_id

    WHERE c.nse_symbol=?

    ORDER BY year

    """

    return run_query(query, [ticker])


# --------------------------------------------------
# SECTORS
# --------------------------------------------------

@st.cache_data(ttl=600)
def get_sectors():

    return run_query("SELECT * FROM sectors")


# --------------------------------------------------
# PEERS
# --------------------------------------------------

@st.cache_data(ttl=600)
def get_peers(group_name):

    query = """

    SELECT *

    FROM peer_groups

    WHERE peer_group_name=?

    """

    return run_query(query, [group_name])


# --------------------------------------------------
# VALUATION
# --------------------------------------------------

@st.cache_data(ttl=600)
def get_valuation(ticker):

    query = """

    SELECT *

    FROM valuation_summary

    WHERE ticker=?

    """

    return run_query(query, [ticker])

@st.cache_data(ttl=600)
def get_dashboard_summary(year):
    """
    Home page KPI summary.

    Note:
    P/E is not available until the valuation module (Day 26),
    so it is returned as None.
    """

    query = """
    SELECT

        ROUND(AVG(return_on_equity_pct),2) AS avg_roe,

        ROUND(AVG(debt_to_equity),2) AS median_de,

        COUNT(DISTINCT company_id) AS total_companies,

        ROUND(AVG(revenue_cagr_5yr),2) AS median_revenue_cagr,

        SUM(
            CASE
                WHEN debt_to_equity = 0 THEN 1
                ELSE 0
            END
        ) AS debt_free_companies

    FROM financial_ratios

    WHERE year = ?
    """

    df = run_query(query, [year])

    # Day 26 will populate this
    df["median_pe"] = None

    return df

@st.cache_data(ttl=600)
def get_sector_distribution():
    """
    Returns company count by broad sector.
    """

    query = """
    SELECT

        broad_sector,

        COUNT(*) AS company_count

    FROM sectors

    GROUP BY broad_sector

    ORDER BY company_count DESC
    """

    return run_query(query)

@st.cache_data(ttl=600)
def get_top_companies(year):

    query = """

    SELECT

        c.company_name,

        fr.composite_quality_score,

        fr.return_on_equity_pct,

        fr.revenue_cagr_5yr

    FROM financial_ratios fr

    JOIN companies c

        ON fr.company_id = c.id

    WHERE fr.year = ?

    ORDER BY fr.composite_quality_score DESC

    LIMIT 5

    """

    return run_query(query, [year])

@st.cache_data(ttl=600)
def search_company(search_text):
    """
    Search companies using company_id or company_name.
    """

    query = """
    SELECT
        id,
        company_name
    FROM companies
    WHERE
        id LIKE ?
        OR company_name LIKE ?
    ORDER BY company_name
    """

    value = f"%{search_text}%"

    return run_query(query, [value, value])

@st.cache_data(ttl=600)
def get_company_profile(company_id):

    query = """
    SELECT

        c.id,
        c.company_name,
        c.about_company,
        s.broad_sector,
        s.sub_sector,
        c.website,
        c.chart_link

    FROM companies c

    LEFT JOIN sectors s
    ON c.id = s.company_id

    WHERE c.id = ?
    """

    return run_query(query, [company_id])

@st.cache_data(ttl=600)
def get_company_kpis(company_id, year):

    query = """
    SELECT

        return_on_equity_pct,

        net_profit_margin_pct,

        debt_to_equity,

        revenue_cagr_5yr,

        free_cash_flow_cr,

        composite_quality_score

    FROM financial_ratios

    WHERE

        company_id = ?

        AND year = ?
    """

    return run_query(query, [company_id, year])

@st.cache_data(ttl=600)
def get_company_trends(company_id):

    pl_query = """
    SELECT
        year,
        sales,
        net_profit
    FROM profitandloss
    WHERE company_id = ?
    ORDER BY year
    """

    ratio_query = """
    SELECT
        year,
        return_on_equity_pct,
        composite_quality_score
    FROM financial_ratios
    WHERE company_id = ?
    ORDER BY year
    """

    pl = run_query(pl_query, [company_id])
    ratios = run_query(ratio_query, [company_id])

    # Extract numeric year from strings like "Mar 2024"
    if not pl.empty:
        pl["year_numeric"] = (
            pl["year"]
            .astype(str)
            .str.extract(r"(\d{4})")[0]
            .astype("Int64")
        )

    if not ratios.empty:
        ratios["year_numeric"] = ratios["year"].astype("Int64")

    merged = pl.merge(
        ratios,
        on="year_numeric",
        how="left",
        suffixes=("_pl", "_ratio")
    )

    return merged

@st.cache_data(ttl=600)
def get_company_pros_cons(company_id):

    return {
        "pros": [
            "Pros data not available."
        ],
        "cons": [
            "Cons data not available."
        ]
    }