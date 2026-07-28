from fastapi import APIRouter
router = APIRouter()
from fastapi import APIRouter,HTTPException
import sqlite3
import pandas as pd


router=APIRouter(
prefix="/peers",
tags=["Peers"]
)


DB="db/nifty100.db"



@router.get("/{group_name}")
def peers(group_name:str):


    conn=sqlite3.connect(DB)



    df=pd.read_sql(

    """

    SELECT *

    FROM peer_percentiles

    WHERE peer_group_name=?

    """,

    conn,

    params=[group_name]

    )



    conn.close()



    if df.empty:

        raise HTTPException(
        404,
        "Peer group not found"
        )



    return df.to_dict(
    orient="records"
    )