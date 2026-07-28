"""
Health API endpoint
"""


from fastapi import APIRouter

import sqlite3
import time


router = APIRouter()


START_TIME = time.time()


DB_PATH = "db/nifty100.db"



TABLES = [

"companies",
"profitandloss",
"balancesheet",
"cashflow",
"analysis",
"documents",
"prosandcons",
"sectors",
"stock_prices",
"financial_ratios"

]



@router.get("/health")
def health_check():

    connection = sqlite3.connect(
        DB_PATH
    )


    counts = {}


    for table in TABLES:

        result = connection.execute(
            f"SELECT COUNT(*) FROM {table}"
        )

        counts[table] = result.fetchone()[0]


    connection.close()


    return {

        "status":"ok",

        "db_row_counts":counts,

        "uptime_seconds":
        round(
            time.time()-START_TIME,
            2
        ),

        "version":"1.0.0"

    }