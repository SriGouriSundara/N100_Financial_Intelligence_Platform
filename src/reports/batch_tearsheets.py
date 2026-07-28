import pandas as pd
import sqlite3

from pathlib import Path

from tearsheet import (
    connect_database,
    load_companies,
    load_sectors,
    load_ratios,
    load_profit_loss,
    load_balance_sheet,
    load_cashflow,
    load_pros_cons,
    load_cashflow_intelligence,
    generate_tearsheet,
)

ROOT = Path(__file__).resolve().parents[2]

OUTPUT = ROOT / "output"

OUTPUT.mkdir(exist_ok=True)

SKIPPED_FILE = OUTPUT / "skipped_tearsheets.csv"
def print_header(title):

    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)
connection = connect_database()

companies = load_companies(connection)

sectors = load_sectors(connection)

ratios = load_ratios(connection)

profit_loss = load_profit_loss(connection)

balance_sheet = load_balance_sheet(connection)

cashflow = load_cashflow(connection)

pros_cons = load_pros_cons()

cashflow_kpi = load_cashflow_intelligence()    
def has_minimum_history(

    profit_loss_df,

    company,

    minimum_years=3

):

    history = (

        profit_loss_df[
            profit_loss_df["company_id"] == company
        ]
        .sort_values("year")
    )

    return len(history) >= minimum_years
skipped = []

generated = 0

for company in companies["id"]:

    if not has_minimum_history(

        profit_loss,

        company

    ):

        skipped.append(company)

        continue

    generate_tearsheet(

        company,

        companies,

        sectors,

        ratios,

        balance_sheet,

        cashflow,

        profit_loss,

        cashflow_kpi,

        pros_cons

    )

    generated += 1
    print("\nSkipped Companies")
    print("----------------------------")
    print(f"Count : {len(skipped)}")

if skipped:
    for company in skipped:
        print(company)
else:
    print("No companies skipped.")
pd.DataFrame(

    {

        "company_id": skipped

    }

).to_csv(

    SKIPPED_FILE,

    index=False

)    