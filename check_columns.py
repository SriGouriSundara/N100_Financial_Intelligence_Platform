from src.etl.loader import load_and_normalize

files = [
    "companies.xlsx",
    "profitandloss.xlsx",
    "balancesheet.xlsx",
    "financial_ratios.xlsx",
    "stock_prices.xlsx"
]

for file in files:
    print("\n" + "=" * 60)
    print(file)
    print("=" * 60)

    df = load_and_normalize(
        f"data/raw/{file}"
    )

    print(df.columns.tolist())