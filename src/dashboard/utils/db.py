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

@st.cache_data(ttl=600)
def get_screener_data(year):
    """
    Load all screener metrics for the selected year.
    """

    query = """
    SELECT

        c.id AS company_id,

        c.company_name,

        s.broad_sector,

        fr.return_on_equity_pct,

        fr.net_profit_margin_pct,

        fr.operating_profit_margin_pct,

        fr.debt_to_equity,

        fr.interest_coverage,

        fr.free_cash_flow_cr,

        fr.asset_turnover,

        fr.revenue_cagr_5yr,

        fr.pat_cagr_5yr,

        fr.composite_quality_score

    FROM financial_ratios fr

    JOIN companies c

        ON fr.company_id = c.id

    LEFT JOIN sectors s

        ON c.id = s.company_id

    WHERE fr.year = ?

    """

    return run_query(query, [year])

def apply_filters(
    df,
    roe,
    de,
    fcf,
    revenue,
    pat,
    opm,
    icr,
):
    """
    Apply all screener filters.
    """

    filtered = df.copy()

    filtered = filtered[
        filtered["return_on_equity_pct"] >= roe
    ]

    filtered = filtered[
        filtered["debt_to_equity"] <= de
    ]

    filtered = filtered[
        filtered["free_cash_flow_cr"] >= fcf
    ]

    filtered = filtered[
        filtered["revenue_cagr_5yr"] >= revenue
    ]

    filtered = filtered[
        filtered["pat_cagr_5yr"] >= pat
    ]

    filtered = filtered[
        filtered["operating_profit_margin_pct"] >= opm
    ]

    filtered = filtered[
        filtered["interest_coverage"] >= icr
    ]

    return filtered

def apply_preset(df, preset):
    """
    Apply predefined screener presets.
    """

    presets = {

        "Quality":

        (
            15,
            1,
            0,
            10,
            10,
            15,
            2
        ),

        "Growth":

        (
            15,
            2,
            0,
            15,
            20,
            10,
            2
        ),

        "Dividend":

        (
            12,
            2,
            0,
            8,
            8,
            10,
            2
        ),

        "Debt Free":

        (
            12,
            0,
            0,
            5,
            5,
            10,
            2
        ),

        "Turnaround":

        (
            5,
            3,
            -999999,
            10,
            10,
            5,
            1
        )

    }

    values = presets[preset]

    return apply_filters(

        df,

        values[0],

        values[1],

        values[2],

        values[3],

        values[4],

        values[5],

        values[6]

    )

def export_csv(df):
    """
    Convert DataFrame to CSV.
    """

    return df.to_csv(
        index=False
    ).encode(
        "utf-8"
    )

@st.cache_data(ttl=600)
def get_peer_groups():
    """
    Returns all peer groups.
    """

    query = """

    SELECT DISTINCT

        peer_group_name

    FROM peer_groups

    ORDER BY peer_group_name

    """

    return run_query(query)

@st.cache_data(ttl=600)
def get_peer_companies(group_name):

    query = """

    SELECT

        company_id

    FROM peer_groups

    WHERE peer_group_name=?

    ORDER BY company_id

    """

    return run_query(query, [group_name])

@st.cache_data(ttl=600)
def get_peer_company_metrics(company_id):

    query = """

    SELECT

        return_on_equity_pct,

        net_profit_margin_pct,

        debt_to_equity,

        free_cash_flow_cr,

        revenue_cagr_5yr,

        pat_cagr_5yr,

        asset_turnover,

        composite_quality_score

    FROM financial_ratios

    WHERE company_id=?

    ORDER BY year DESC

    LIMIT 1

    """

    return run_query(query, [company_id])

@st.cache_data(ttl=600)
def get_peer_average_metrics(group_name):

    query = """

    SELECT

        AVG(fr.return_on_equity_pct) AS roe,

        AVG(fr.net_profit_margin_pct) AS npm,

        AVG(fr.debt_to_equity) AS de,

        AVG(fr.free_cash_flow_cr) AS fcf,

        AVG(fr.revenue_cagr_5yr) AS revenue,

        AVG(fr.pat_cagr_5yr) AS pat,

        AVG(fr.asset_turnover) AS turnover,

        AVG(fr.composite_quality_score) AS score

    FROM financial_ratios fr

    JOIN peer_groups pg

    ON fr.company_id=pg.company_id

    WHERE

        pg.peer_group_name=?

    """

    return run_query(query, [group_name])

from src.dashboard.utils.db import *

print(get_screener_data(2024).head())

print(get_peer_groups())

print(get_peer_companies("IT Services"))

print(get_peer_company_metrics("TCS"))

print(get_peer_average_metrics("IT Services"))

# ============================================================
# DAY 25 DASHBOARD FUNCTIONS
# Trend Analysis
# Sector Analysis
# Capital Allocation
# Annual Reports
# ============================================================

import sqlite3
import pandas as pd
from pathlib import Path
import streamlit as st

# ------------------------------------------------------------
# Database Path
# ------------------------------------------------------------

DB_PATH = Path(__file__).resolve().parents[3] / "db" / "nifty100.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


# ============================================================
# TREND ANALYSIS
# ============================================================

@st.cache_data(ttl=600)
def get_trend_companies():
    """
    Returns all companies for search dropdown.
    """

    conn = get_connection()

    query = """
    SELECT
        id,
        company_name
    FROM companies
    ORDER BY company_name
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_trend_metrics():
    """
    Metrics available for Trend Analysis.
    """

    return {

        "Revenue": "sales",

        "Net Profit": "net_profit",

        "ROE": "return_on_equity_pct",

        "Net Profit Margin": "net_profit_margin_pct",

        "Debt / Equity": "debt_to_equity",

        "Revenue CAGR": "revenue_cagr_5yr",

        "PAT CAGR": "pat_cagr_5yr",

        "Asset Turnover": "asset_turnover",

        "Free Cash Flow": "free_cash_flow_cr",

    }


@st.cache_data(ttl=600)
def get_company_timeseries(company_id):
    """
    Returns 10-year financial history.
    """

    conn = get_connection()

    query = """
    SELECT

        fr.year,

        pl.sales,

        pl.net_profit,

        fr.return_on_equity_pct,

        fr.net_profit_margin_pct,

        fr.debt_to_equity,

        fr.revenue_cagr_5yr,

        fr.pat_cagr_5yr,

        fr.asset_turnover,

        fr.free_cash_flow_cr

    FROM financial_ratios fr

    LEFT JOIN profitandloss pl

        ON fr.company_id = pl.company_id
       AND fr.year = pl.year

    WHERE fr.company_id = ?

    ORDER BY fr.year
    """

    df = pd.read_sql(query, conn, params=[company_id])

    conn.close()

    return df


# ============================================================
# SECTOR ANALYSIS
# ============================================================

@st.cache_data(ttl=600)
def get_sector_list():
    """
    Returns all broad sectors.
    """

    conn = get_connection()

    query = """
    SELECT DISTINCT broad_sector

    FROM sectors

    ORDER BY broad_sector
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_sector_data(sector_name, year=2024):

    conn = get_connection()

    query = """
    SELECT

        c.id,
        c.company_name,
        s.sub_sector,

        pl.sales,

        fr.return_on_equity_pct,

        s.market_cap_category,

        fr.composite_quality_score

    FROM sectors s

    JOIN companies c
        ON s.company_id=c.id

    LEFT JOIN financial_ratios fr
        ON c.id=fr.company_id
        AND fr.year=?

    LEFT JOIN profitandloss pl
        ON c.id=pl.company_id
        AND pl.year=?

    WHERE s.broad_sector=?
    """

    df = pd.read_sql(
        query,
        conn,
        params=[year, year, sector_name]
    )
    print(df.columns.tolist())

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_sector_medians(sector_name, year=2024):
    """
    Median KPIs for sector bar chart.
    """

    conn = get_connection()

    query = """
    SELECT

        median(return_on_equity_pct) AS median_roe,

        median(net_profit_margin_pct) AS median_npm,

        median(debt_to_equity) AS median_de,

        median(revenue_cagr_5yr) AS median_revenue,

        median(pat_cagr_5yr) AS median_pat

    FROM financial_ratios fr

    JOIN sectors s

        ON fr.company_id = s.company_id

    WHERE

        s.broad_sector = ?

        AND fr.year = ?
    """

    try:

        df = pd.read_sql(

            query,

            conn,

            params=[sector_name, year]

        )

    except Exception:

        # SQLite builds without MEDIAN() support
        raw = pd.read_sql(
            """
            SELECT
                fr.return_on_equity_pct,
                fr.net_profit_margin_pct,
                fr.debt_to_equity,
                fr.revenue_cagr_5yr,
                fr.pat_cagr_5yr
            FROM financial_ratios fr
            JOIN sectors s
              ON fr.company_id=s.company_id
            WHERE s.broad_sector=?
              AND fr.year=?
            """,
            conn,
            params=[sector_name, year]
        )

        df = pd.DataFrame([{

            "median_roe":
                raw["return_on_equity_pct"].median(),

            "median_npm":
                raw["net_profit_margin_pct"].median(),

            "median_de":
                raw["debt_to_equity"].median(),

            "median_revenue":
                raw["revenue_cagr_5yr"].median(),

            "median_pat":
                raw["pat_cagr_5yr"].median(),

        }])

    conn.close()

    return df


# ============================================================
# CAPITAL ALLOCATION
# ============================================================

@st.cache_data(ttl=600)
def get_capital_patterns():
    """
    Returns all capital allocation patterns.

    Uses generated CSV if available.
    """

    csv_path = (
        Path(__file__).resolve().parents[3]
        / "output"
        / "capital_allocation.csv"
    )

    if csv_path.exists():

        return pd.read_csv(csv_path)

    return pd.DataFrame()


@st.cache_data(ttl=600)
def get_capital_companies(pattern):
    """
    Companies belonging to selected pattern.
    """

    df = get_capital_patterns()

    if df.empty:

        return df

    return df[df["pattern_label"] == pattern]


# ============================================================
# ANNUAL REPORTS
# ============================================================

@st.cache_data(ttl=600)
def get_report_companies():
    """
    Company search list.
    """

    return get_trend_companies()


@st.cache_data(ttl=600)
def get_annual_reports(company_id):
    """
    Returns report links.

    Gracefully handles projects
    without reports table.
    """

    conn = get_connection()

    try:

        query = """
        SELECT

            year,

            annual_report

        FROM documents

        WHERE company_id=?

        ORDER BY year DESC
        """

        df = pd.read_sql(

            query,

            conn,

            params=[company_id]

        )

    except Exception:

        df = pd.DataFrame(

            columns=[
                "year",
                "annual_report"
            ]

        )

    conn.close()

    return df