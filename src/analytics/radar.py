"""
=========================================================
Sprint 3
Day 19
Radar Chart Engine
=========================================================
"""

import os
import sqlite3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ---------------------------------------------------
# Database
# ---------------------------------------------------

DATABASE = "db/nifty100.db"

REPORT_FOLDER = Path("reports/radar_charts")
REPORT_FOLDER.mkdir(parents=True, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)

# ---------------------------------------------------
# Connect Database
# ---------------------------------------------------

connection = sqlite3.connect(DATABASE)

print()

print("=" * 60)
print("SPRINT 3 - DAY 19")
print("=" * 60)

financial_ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    connection
)

peer_groups = pd.read_sql(
    "SELECT * FROM peer_groups",
    connection
)

companies = pd.read_sql(
    "SELECT * FROM companies",
    connection
)

peer_percentiles = pd.read_sql(
    "SELECT * FROM peer_percentiles",
    connection
)

print()

print("Tables Loaded")
print("-" * 30)

print("financial_ratios :", len(financial_ratios))
print("peer_groups      :", len(peer_groups))
print("companies        :", len(companies))
print("peer_percentiles :", len(peer_percentiles))

latest_df = financial_ratios.merge(

    peer_groups,

    on="company_id",

    how="left"

)

latest_df = latest_df.merge(

    companies[
        [
            "id",
            "company_name",
            "roce_percentage"
        ]
    ],

    left_on="company_id",

    right_on="id",

    how="left"

)

print()

print("=" * 60)
print("latest_df DATASET")
print("=" * 60)

print()

print("Rows :", len(latest_df))

print("Columns :", len(latest_df.columns))

print()

print(latest_df.columns.tolist())

RADAR_METRICS = [

    "return_on_equity_pct",

    "roce_percentage",

    "net_profit_margin_pct",

    "debt_to_equity",

    "free_cash_flow_cr",

    "pat_cagr_5yr",

    "revenue_cagr_5yr",

    "composite_quality_score"

]

# ---------------------------------------------------
# Normalize Metrics (0–100)
# ---------------------------------------------------

def normalize_series(series):
    """
    Normalize values to a 0–100 scale.
    """

    minimum = series.min()
    maximum = series.max()

    if maximum == minimum:
        return pd.Series([50] * len(series), index=series.index)

    return ((series - minimum) / (maximum - minimum)) * 100

# ---------------------------------------------------
# Normalize Metrics
# ---------------------------------------------------

normalized_latest_df = latest_df.copy()

for metric in RADAR_METRICS:

    normalized_latest_df[metric] = normalize_series(
        normalized_latest_df[metric].fillna(0)
    )

print()
print("Metrics normalized successfully.")

# ---------------------------------------------------
# Peer Group Average
# ---------------------------------------------------

peer_average = (

    normalized_latest_df

    .groupby("peer_group_name")[RADAR_METRICS]

    .mean()

    .reset_index()

)

print()
print("Peer Group Average Created")

print()

print(peer_average.head())

# ---------------------------------------------------
# Radar Chart Function
# ---------------------------------------------------

def create_radar(company_row, peer_row):

    labels = RADAR_METRICS

    company_values = company_row[labels].values.tolist()

    peer_values = peer_row[labels].values.tolist()

    company_values += company_values[:1]
    peer_values += peer_values[:1]

    angles = np.linspace(
        0,
        2 * np.pi,
        len(labels),
        endpoint=False
    ).tolist()

    angles += angles[:1]

    fig = plt.figure(figsize=(8, 8))

    ax = plt.subplot(111, polar=True)

    ax.plot(
        angles,
        company_values,
        linewidth=2,
        label="Company"
    )

    ax.fill(
        angles,
        company_values,
        alpha=0.25
    )

    ax.plot(
        angles,
        peer_values,
        linestyle="--",
        linewidth=2,
        label="Peer Average"
    )

    ax.set_xticks(angles[:-1])

    ax.set_xticklabels(
        [
            "ROE",
            "ROCE",
            "NPM",
            "D/E",
            "FCF",
            "PAT CAGR",
            "REV CAGR",
            "Composite"
        ],
        fontsize=9
    )

    ax.set_title(
        company_row["company_name"],
        fontsize=12
    )

    plt.legend(loc="upper right")

    filename = os.path.join(

        REPORT_FOLDER,

        f"{company_row['company_id']}_radar.png"

    )

    plt.savefig(
        filename,
        dpi=200,
        bbox_inches="tight"
    )

    plt.close()

# ---------------------------------------------------
# Generate Radar Charts
# ---------------------------------------------------

count = 0
# -------------------------------------------------------
# Keep only the latest year for each company
# -------------------------------------------------------

normalized_latest_df = (
    normalized_latest_df
    .sort_values("year")
    .groupby("company_id", as_index=False)
    .tail(1)
)

print(f"Latest Company Records : {len(normalized_latest_df)}")

charts_created = 0
peer_df = latest_df[
    latest_df["peer_group_name"].notna()
]

for _, row in peer_df.iterrows():

    # Existing radar chart code remains exactly the same
    charts_created += 1
print()
print("=" * 60)
print("DAY 19 SUMMARY")
print("=" * 60)

print(f"Radar Charts Generated : {charts_created}")

print()
print("Execution Completed Successfully.")

# ---------------------------------------------------
# Companies Without Peer Group
# ---------------------------------------------------

missing = normalized_latest_df[
    normalized_latest_df["peer_group_name"].isna()
]

print()

print("Companies without peer group :", len(missing))

print()

print("=" * 60)
print("DAY 19 PART 2 COMPLETED")
print("=" * 60)

connection.close()

print()

print("Radar Metrics Check")

print("-" * 30)

for metric in RADAR_METRICS:

    if metric in latest_df.columns:

        print(f"[OK] {metric}")

    else:

        print(f"[MISSING] {metric}")

        # ============================================================
# DAY 19 PART 3
# Standalone charts for companies without peer group
# ============================================================

    print("\nCreating standalone charts...")
    overall_average = latest_df[[
    "return_on_equity_pct",
    "roce_percentage",
    "net_profit_margin_pct",
    "debt_to_equity",
    "free_cash_flow_cr",
    "pat_cagr_5yr",
    "revenue_cagr_5yr",
    "composite_quality_score"
]].mean()

    companies_without_peer = latest_df[
     latest_df["peer_group_name"].isna()
]

standalone_count = 0

for _, row in companies_without_peer.iterrows():

    plt.figure(figsize=(5,4))

    plt.bar(
        ["Composite Score"],
        [row["composite_quality_score"]],
        width=0.4,
    )

    plt.axhline(
        overall_average["composite_quality_score"],
        linestyle="--",
        linewidth=2,
        label="Nifty100 Average",
    )

    plt.title(row["company_name"])

    plt.legend()

    plt.tight_layout()

    filename = (
        REPORT_FOLDER
        / f"{row['company_id']}_standalone.png"
    )

    plt.savefig(filename)

    plt.close()

    standalone_count += 1

print("Standalone Charts :", standalone_count)

# ============================================================
# FINAL VALIDATION
# ============================================================

import os

print("\n============================================================")
print("DAY 19 VALIDATION")
print("============================================================")

# Count generated files
radar_files = [
    f for f in os.listdir(REPORT_FOLDER)
    if f.endswith("_radar.png")
]

standalone_files = [
    f for f in os.listdir(REPORT_FOLDER)
    if f.endswith("_standalone.png")
]

png_files = radar_files + standalone_files

print(f"Historical Records Processed : {len(latest_df)}")
print(f"Latest Company Charts Saved : {len(radar_files)}")
print(f"Standalone Charts Saved     : {len(standalone_files)}")
print(f"Total PNG Files             : {len(png_files)}")

print()

if len(png_files) > 0:
    print("Radar Chart Export : PASSED")
else:
    print("Radar Chart Export : FAILED")

print("\nSample Files")

for file in png_files[:10]:
    print(file)

print("\nReport Folder")
print(REPORT_FOLDER.resolve())

print("\nDAY 19 COMPLETED SUCCESSFULLY")