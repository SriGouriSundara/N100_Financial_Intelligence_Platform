from fastapi import APIRouter
router = APIRouter()
from fastapi import APIRouter
import sqlite3
import pandas as pd


router=APIRouter(
prefix="/market-cap",
tags=["Valuation"]
)


DB="db/nifty100.db"



@router.get("/{ticker}")
def valuation(ticker:str):


    conn=sqlite3.connect(DB)


    df=pd.read_sql(

    """

    SELECT *

    FROM stock_prices

    WHERE ticker=?

    ORDER BY year


    """,

    conn,

    params=[ticker]

    )


    conn.close()


    return df.to_dict(
    orient="records"
    )