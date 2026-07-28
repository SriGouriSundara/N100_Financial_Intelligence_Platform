from fastapi import APIRouter
router = APIRouter()
"""
Screener API
Day 40 Sprint 6
"""


from fastapi import APIRouter, HTTPException
import sqlite3
import pandas as pd


router = APIRouter(
    prefix="/screener",
    tags=["Screener"]
)


DB_PATH="db/nifty100.db"



def connection():

    return sqlite3.connect(DB_PATH)



@router.get("/")
def screener(

    min_roe:float|None=None,
    max_de:float|None=None,
    min_fcf:float|None=None,
    sector:str|None=None,
    min_rev_cagr_5yr:float|None=None,
    min_pat_cagr_5yr:float|None=None,
    max_pe:float|None=None

):


    conn=connection()


    query="""

    SELECT

    c.company_name,
    c.nse_ticker,
    c.broad_sector,

    r.return_on_equity_pct,
    r.debt_to_equity,
    r.free_cash_flow_cr,
    r.revenue_cagr_5yr,
    r.pat_cagr_5yr,
    r.composite_quality_score


    FROM companies c

    JOIN financial_ratios r

    ON c.id=r.company_id


    WHERE r.year=
    (
        SELECT MAX(year)
        FROM financial_ratios
    )

    """



    df=pd.read_sql(query,conn)



    if min_roe is not None:

        df=df[
            df.return_on_equity_pct>=min_roe
        ]


    if max_de is not None:

        df=df[
            df.debt_to_equity<=max_de
        ]


    if min_fcf is not None:

        df=df[
            df.free_cash_flow_cr>=min_fcf
        ]



    if sector:

        df=df[
            df.broad_sector==sector
        ]



    if min_rev_cagr_5yr:

        df=df[
            df.revenue_cagr_5yr>=min_rev_cagr_5yr
        ]



    if min_pat_cagr_5yr:

        df=df[
            df.pat_cagr_5yr>=min_pat_cagr_5yr
        ]



    conn.close()



    return df.sort_values(
        "composite_quality_score",
        ascending=False
    ).to_dict(
        orient="records"
    )