import pandas as pd

summary = pd.read_excel("output/valuation_summary.xlsx")
flags = pd.read_csv("output/valuation_flags.csv")

print("=" * 60)
print("VALUATION SUMMARY")
print("=" * 60)

print("Rows :", len(summary))
print("Unique Companies :", summary["company_id"].nunique())

print()

print("=" * 60)
print("FLAGS")
print("=" * 60)

print(flags["Flag"].value_counts())

print()

print("Duplicate Company IDs :", summary["company_id"].duplicated().sum())

print("Missing Company IDs :", summary["company_id"].isna().sum())

print("Missing Flags :", summary["Flag"].isna().sum())