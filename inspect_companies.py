import pandas as pd

file_path = "data/raw/companies.xlsx"

df = pd.read_excel(
    file_path,
    header=None
)

print("\nShape:")
print(df.shape)

print("\nFirst 15 Rows:")
print(df.head(15))