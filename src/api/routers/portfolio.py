from fastapi import APIRouter
router = APIRouter()
from fastapi import APIRouter
import pandas as pd


router=APIRouter(
prefix="/portfolio",
tags=["Portfolio"]
)


@router.get("/stats")
def stats():


    df=pd.read_csv(
    "output/portfolio_stats.csv"
    )


    return df.to_dict(
    orient="records"
    )