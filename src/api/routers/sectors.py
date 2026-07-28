from fastapi import APIRouter
router = APIRouter()
from fastapi import APIRouter,HTTPException
import sqlite3
import pandas as pd


router=APIRouter(
prefix="/sectors",
tags=["Sectors"]
)


DB="db/nifty100.db"



@router.get("/")
def sectors():

    conn=sqlite3.connect(DB)


    df=pd.read_sql(
    """

    SELECT

    c.broad_sector,

    COUNT(*) company_count,

    AVG(r.return_on_equity_pct) median_roe,

    AVG(r.debt_to_equity) median_de


    FROM companies c

    JOIN financial_ratios r

    ON c.id=r.company_id


    GROUP BY broad_sector


    """,
    conn
    )


    conn.close()


    return df.to_dict(
    orient="records"
    )





@router.get("/{sector}/companies")
def sector_companies(
sector:str
):

    conn=sqlite3.connect(DB)


    df=pd.read_sql(
    """

    SELECT

    c.company_name,
    c.nse_ticker,
    c.broad_sector,

    r.*

    FROM companies c

    JOIN financial_ratios r

    ON c.id=r.company_id

    WHERE c.broad_sector=?

    """,
    conn,
    params=[sector]
    )


    conn.close()


    if df.empty:

        raise HTTPException(
        404,
        "Sector not found"
        )


    return df.to_dict(
    orient="records"
    )