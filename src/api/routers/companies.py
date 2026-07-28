from fastapi import APIRouter
router = APIRouter()
"""
Company API endpoints
Sprint 6 - Day 39
"""

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse

import sqlite3
import pandas as pd
from pathlib import Path


router = APIRouter(
    prefix="/companies",
    tags=["Companies"]
)


DB_PATH = "db/nifty100.db"



# -------------------------------------------------
# Database Connection
# -------------------------------------------------

def get_connection():

    """
    Create SQLite connection
    """

    return sqlite3.connect(DB_PATH)



# -------------------------------------------------
# GET ALL COMPANIES
# -------------------------------------------------

@router.get("/")
def get_companies(
        sector: str | None = None,
        market_cap_category: str | None = None,
        search: str | None = None
):

    """
    Return all companies with optional filters
    """

    conn = get_connection()


    query = """

    SELECT
        id,
        company_name,
        broad_sector,
        sub_sector,
        roe_percentage AS roe_pct,
        roce_percentage AS roce_pct,
        nse_ticker

    FROM companies

    WHERE 1=1

    """

    params=[]


    if sector:

        query += """
        AND broad_sector = ?
        """

        params.append(sector)



    if search:

        query += """

        AND (
        company_name LIKE ?
        OR nse_ticker LIKE ?
        )

        """

        params.extend(
            [
                f"%{search}%",
                f"%{search}%"
            ]
        )



    df=pd.read_sql(
        query,
        conn,
        params=params
    )


    conn.close()


    return df.to_dict(
        orient="records"
    )



# -------------------------------------------------
# COMPANY PROFILE
# -------------------------------------------------

@router.get("/{ticker}")
def company_profile(
    ticker:str
):

    """
    Complete company profile
    """

    conn=get_connection()


    company=pd.read_sql(
        """
        SELECT *
        FROM companies
        WHERE nse_ticker=?
        """,
        conn,
        params=[ticker]
    )


    if company.empty:

        raise HTTPException(
            status_code=404,
            detail="Ticker not found"
        )



    ratios=pd.read_sql(
        """

        SELECT *
        FROM financial_ratios

        WHERE company_id=?

        ORDER BY year DESC

        LIMIT 1

        """,
        conn,
        params=[
            company.iloc[0]["id"]
        ]
    )


    conn.close()


    return {

        "company":
        company.iloc[0].to_dict(),

        "latest_kpis":
        ratios.iloc[0].to_dict()
        if not ratios.empty
        else {}

    }




# -------------------------------------------------
# COMMON HISTORY FUNCTION
# -------------------------------------------------


def get_history(
        ticker,
        table,
        from_year=None,
        to_year=None
):


    conn=get_connection()


    query=f"""

    SELECT *

    FROM {table}

    WHERE company_id=
    (
        SELECT id
        FROM companies
        WHERE nse_ticker=?
    )

    """

    params=[ticker]



    if from_year:

        query+=" AND year >= ?"

        params.append(from_year)



    if to_year:

        query+=" AND year <= ?"

        params.append(to_year)



    df=pd.read_sql(
        query,
        conn,
        params=params
    )


    conn.close()


    if df.empty:

        raise HTTPException(
            status_code=404,
            detail="Data not found"
        )


    return df.to_dict(
        orient="records"
    )



# -------------------------------------------------
# P&L HISTORY
# -------------------------------------------------

@router.get("/{ticker}/pl")
def get_pl(
        ticker:str,
        from_year:str|None=None,
        to_year:str|None=None
):

    return get_history(
        ticker,
        "profitandloss",
        from_year,
        to_year
    )



# -------------------------------------------------
# BALANCE SHEET
# -------------------------------------------------

@router.get("/{ticker}/bs")
def get_bs(
        ticker:str,
        from_year:str|None=None,
        to_year:str|None=None
):

    return get_history(
        ticker,
        "balancesheet",
        from_year,
        to_year
    )



# -------------------------------------------------
# CASH FLOW
# -------------------------------------------------

@router.get("/{ticker}/cashflow")
def get_cashflow(
        ticker:str,
        from_year:str|None=None,
        to_year:str|None=None
):

    return get_history(
        ticker,
        "cashflow",
        from_year,
        to_year
    )



# -------------------------------------------------
# RATIOS
# -------------------------------------------------

@router.get("/{ticker}/ratios")
def get_ratios(
        ticker:str,
        year:int|None=None
):


    conn=get_connection()


    query="""

    SELECT *

    FROM financial_ratios

    WHERE company_id=
    (
        SELECT id
        FROM companies
        WHERE nse_ticker=?
    )

    """

    params=[ticker]


    if year:

        query+=" AND year=?"

        params.append(year)



    df=pd.read_sql(
        query,
        conn,
        params=params
    )


    conn.close()


    return df.to_dict(
        orient="records"
    )



# -------------------------------------------------
# TEARSHEET PDF
# -------------------------------------------------

@router.get("/{ticker}/tearsheet")
def get_tearsheet(
        ticker:str
):


    file_path = Path(
        f"reports/tearsheets/{ticker}_tearsheet.pdf"
    )


    if not file_path.exists():

        raise HTTPException(
            status_code=404,
            detail="Tearsheet unavailable"
        )


    return FileResponse(
        file_path,
        media_type="application/pdf"
    )