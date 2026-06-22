import pandas as pd

df = pd.read_excel(
    "data/raw/companies.xlsx",
    header=1
)

print("Rows:")
print(len(df))

print("\nDuplicate IDs:")

print(
    df["id"].duplicated().sum()
)