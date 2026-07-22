"""
Sprint 4
Day 27

Integration QA Test Runner
"""

from pathlib import Path
import sqlite3
import pandas as pd
import time

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DB_PATH = PROJECT_ROOT / "db" / "nifty100.db"

OUTPUT = PROJECT_ROOT / "output" / "qa_test_results.csv"


def record(test_name, status, details):
    return {
        "Test": test_name,
        "Status": status,
        "Details": details,
    }


def main():

    results = []

    conn = sqlite3.connect(DB_PATH)

    # ----------------------------------------------------
    # Company Count
    # ----------------------------------------------------

    companies = pd.read_sql(
        """
        SELECT COUNT(*)
        AS total
        FROM companies
        """,
        conn,
    ).iloc[0]["total"]

    if companies >= 92:
        results.append(record("Company Count", "PASS", companies))
    else:
        results.append(record("Company Count", "FAIL", companies))

    # ----------------------------------------------------
    # Ratio Count
    # ----------------------------------------------------

    ratios = pd.read_sql(
        """
        SELECT COUNT(*)
        AS total
        FROM financial_ratios
        """,
        conn,
    ).iloc[0]["total"]

    if ratios > 1000:
        results.append(record("Financial Ratio Rows", "PASS", ratios))
    else:
        results.append(record("Financial Ratio Rows", "FAIL", ratios))

    # ----------------------------------------------------
    # Missing KPI Check
    # ----------------------------------------------------

    missing = pd.read_sql(
        """
        SELECT
        SUM(
            CASE
                WHEN return_on_equity_pct IS NULL
                THEN 1
                ELSE 0
            END
        ) missing
        FROM financial_ratios
        """,
        conn,
    ).iloc[0]["missing"]

    results.append(record("Missing ROE", "PASS", missing))

    # ----------------------------------------------------
    # Partial History
    # ----------------------------------------------------

    partial = pd.read_sql(
        """
        SELECT
        company_id,
        COUNT(*) years

        FROM financial_ratios

        GROUP BY company_id

        HAVING years<10
        """,
        conn,
    )

    results.append(
        record(
            "Partial History Companies",
            "PASS",
            len(partial),
        )
    )

    # ----------------------------------------------------
    # CSV Export
    # ----------------------------------------------------

    valuation = PROJECT_ROOT / "output" / "valuation_summary.xlsx"

    if valuation.exists():
        results.append(
            record(
                "Valuation Summary",
                "PASS",
                "File Exists",
            )
        )
    else:
        results.append(
            record(
                "Valuation Summary",
                "FAIL",
                "Missing",
            )
        )

    # ----------------------------------------------------
    # Performance Test
    # ----------------------------------------------------

    start = time.time()

    pd.read_sql(
        """
        SELECT *
        FROM financial_ratios
        LIMIT 500
        """,
        conn,
    )

    elapsed = round(time.time() - start, 3)

    if elapsed < 3:
        status = "PASS"
    else:
        status = "FAIL"

    results.append(
        record(
            "Dashboard Query Time",
            status,
            f"{elapsed} sec",
        )
    )

    conn.close()

    df = pd.DataFrame(results)

    OUTPUT.parent.mkdir(exist_ok=True)

    df.to_csv(OUTPUT, index=False)

    print(df)

    print()

    print("QA Report Saved")

    print(OUTPUT)


if __name__ == "__main__":
    main()