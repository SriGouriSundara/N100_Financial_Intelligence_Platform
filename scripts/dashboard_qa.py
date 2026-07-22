"""
=========================================================
Sprint 4 - Day 27
Dashboard Integration QA
=========================================================
"""

from pathlib import Path
import sqlite3
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "db" / "nifty100.db"
OUTPUT = ROOT / "output" / "qa_test_results.csv"


TEST_TICKERS = [
    ("IT", "TCS"),
    ("IT", "INFY"),
    ("Financials", "HDFCBANK"),
    ("Financials", "ICICIBANK"),
    ("FMCG", "HINDUNILVR"),
    ("FMCG", "ITC"),
    ("Energy", "RELIANCE"),
    ("Energy", "ONGC"),
    ("Healthcare", "SUNPHARMA"),
    ("Healthcare", "DRREDDY"),
]


def run_query(query, params=()):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df


def test_company_exists(ticker):
    df = run_query(
        """
        SELECT company_name
        FROM companies
        WHERE id=?
        """,
        (ticker,),
    )

    return not df.empty


def test_financial_ratios(ticker):
    df = run_query(
        """
        SELECT *
        FROM financial_ratios
        WHERE company_id=?
        """,
        (ticker,),
    )

    return not df.empty


def test_profit_loss(ticker):
    df = run_query(
        """
        SELECT *
        FROM profitandloss
        WHERE company_id=?
        """,
        (ticker,),
    )

    return not df.empty


def test_sector(ticker):
    df = run_query(
        """
        SELECT *
        FROM sectors
        WHERE company_id=?
        """,
        (ticker,),
    )

    return not df.empty


def main():

    results = []

    print("=" * 60)
    print("Dashboard Integration QA")
    print("=" * 60)

    for sector, ticker in TEST_TICKERS:

        company = test_company_exists(ticker)
        ratios = test_financial_ratios(ticker)
        pl = test_profit_loss(ticker)
        sec = test_sector(ticker)

        passed = all([company, ratios, pl, sec])

        results.append(
            {
                "Sector": sector,
                "Ticker": ticker,
                "Company": company,
                "Ratios": ratios,
                "ProfitLoss": pl,
                "SectorData": sec,
                "PASS": passed,
            }
        )

        print(
            f"{ticker:12} "
            f"{'PASS' if passed else 'FAIL'}"
        )

    df = pd.DataFrame(results)

    OUTPUT.parent.mkdir(exist_ok=True)

    df.to_csv(OUTPUT, index=False)

    print()
    print("=" * 60)
    print("QA completed")
    print(f"Results saved to {OUTPUT}")
    print("=" * 60)

    print()
    print(df)


if __name__ == "__main__":
    main()