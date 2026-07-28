"""
Nifty100 Financial Intelligence API

Sprint 6 Day 38
FastAPI Application
"""


from fastapi import FastAPI, Request

from fastapi.middleware.cors import CORSMiddleware

import time



from src.api.routers import health
from src.api.routers import companies
from src.api.routers import screener
from src.api.routers import sectors
from src.api.routers import peers
from src.api.routers import valuation
from src.api.routers import portfolio
from src.api.routers import documents




app = FastAPI(

    title="Nifty100 Financial Intelligence API",

    version="1.0.0"

)



# -----------------------------
# CORS Configuration
# -----------------------------

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]

)



# -----------------------------
# Request Logging Middleware
# -----------------------------

@app.middleware("http")
async def request_logger(
    request:Request,
    call_next
):

    start=time.time()


    response = await call_next(
        request
    )


    duration = time.time()-start


    print(

        request.method,

        request.url.path,

        round(duration,4),

        "seconds"

    )


    return response



# -----------------------------
# Routers
# -----------------------------


PREFIX="/api/v1"



app.include_router(
    health.router,
    prefix=PREFIX
)


app.include_router(
    companies.router,
    prefix=PREFIX
)


app.include_router(
    screener.router,
    prefix=PREFIX
)


app.include_router(
    sectors.router,
    prefix=PREFIX
)


app.include_router(
    peers.router,
    prefix=PREFIX
)


app.include_router(
    valuation.router,
    prefix=PREFIX
)


app.include_router(
    portfolio.router,
    prefix=PREFIX
)


app.include_router(
    documents.router,
    prefix=PREFIX
)

from src.api.routers import companies
app.include_router(
    companies.router,
    prefix="/api/v1"
)
from src.api.routers import (
companies,
screener,
sectors,
peers,
valuation,
portfolio,
documents
)



app.include_router(
screener.router,
prefix="/api/v1"
)


app.include_router(
sectors.router,
prefix="/api/v1"
)


app.include_router(
peers.router,
prefix="/api/v1"
)


app.include_router(
valuation.router,
prefix="/api/v1"
)


app.include_router(
portfolio.router,
prefix="/api/v1"
)


app.include_router(
documents.router,
prefix="/api/v1"
)



@app.get("/")
def root():

    return {

        "message":
        "Nifty100 Financial Intelligence API running"

    }