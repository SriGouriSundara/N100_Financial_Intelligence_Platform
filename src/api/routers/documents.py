from fastapi import APIRouter
router = APIRouter()
from fastapi import APIRouter
import sqlite3
import pandas as pd


router=APIRouter(
prefix="/companies",
tags=["Documents"]
)


@router.get("/{ticker}/documents")
def documents(ticker:str):


    conn=sqlite3.connect(
    "db/nifty100.db"
    )


    df=pd.read_sql(

    """

    SELECT *

    FROM documents

    WHERE company_id=

    (

    SELECT id
    FROM companies
    WHERE nse_ticker=?

    )

    """,

    conn,

    params=[ticker]

    )


    conn.close()


    return df.to_dict(
    orient="records"
    )