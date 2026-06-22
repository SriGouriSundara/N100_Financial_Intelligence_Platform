import pandas as pd

files = [
    "companies.xlsx",
    "profitandloss.xlsx",
    "balancesheet.xlsx",
    "cashflow.xlsx",
    "analysis.xlsx",
    "documents.xlsx",
    "financial_ratios.xlsx",
    "peer_groups.xlsx",
    "sectors.xlsx",
    "stock_prices.xlsx"
]

for file in files:

    print("\n")
    print("=" * 70)
    print(file)
    print("=" * 70)

    try:

        df = pd.read_excel(
            f"data/raw/{file}",
            header=None
        )

        print(df.head(5))

    except Exception as e:

        print("ERROR:", e)