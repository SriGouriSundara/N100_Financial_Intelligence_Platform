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