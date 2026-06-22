import pandas as pd

files = [
    "companies.xlsx",
    "profitandloss.xlsx",
    "balancesheet.xlsx",
    "cashflow.xlsx",
    "stock_prices.xlsx",
    "financial_ratios.xlsx"
]

for file in files:

    print("\n")
    print("=" * 60)
    print(file)
    print("=" * 60)

    path = f"data/raw/{file}"

    df = pd.read_excel(path)

    print(df.columns.tolist())