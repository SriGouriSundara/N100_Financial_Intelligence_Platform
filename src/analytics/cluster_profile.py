"""
Sprint 6 Day 37
Cluster Profiling and Portfolio Statistics

Tasks:
1. Cluster profiling
2. Cluster naming
3. Correlation heatmap
4. Outlier detection
5. Portfolio statistics
"""


import sqlite3
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns


DB_PATH = "db/nifty100.db"

CLUSTER_FILE = "output/cluster_labels.csv"

OUTLIER_FILE = "output/outlier_report.csv"

STATS_FILE = "output/portfolio_stats.csv"

HEATMAP_FILE = "reports/correlation_heatmap.png"



# ------------------------------------------------
# Load latest year financial data
# ------------------------------------------------

def load_latest_data():

    conn = sqlite3.connect(DB_PATH)


    query = """

    SELECT
        company_id,
        year,
        return_on_equity_pct,
        debt_to_equity,
        revenue_cagr_5yr,
        pat_cagr_5yr,
        eps_cagr_5yr,
        operating_profit_margin_pct,
        net_profit_margin_pct,
        free_cash_flow_cr,
        cash_from_operations_cr

    FROM financial_ratios fr

INNER JOIN companies c

ON fr.company_id = c.id

WHERE fr.year =
(
    SELECT MAX(year)
    FROM financial_ratios
)

GROUP BY fr.company_id

"""



    df = pd.read_sql(
        query,
        conn
    )


    conn.close()


    return df



# ------------------------------------------------
# Cluster profiling
# ------------------------------------------------

def profile_clusters(df):


    clusters = pd.read_csv(
        CLUSTER_FILE
    )


    merged = df.merge(
        clusters,
        on="company_id"
    )


    features = [

        "return_on_equity_pct",
        "debt_to_equity",
        "revenue_cagr_5yr",
        "free_cash_flow_cr",
        "operating_profit_margin_pct"

    ]


    profile = merged.groupby(
        "cluster_id"
    )[features].agg(
        [
            "mean",
            "median"
        ]
    )


    print("\nCluster Profile\n")

    print(profile)



    return merged



# ------------------------------------------------
# Correlation Heatmap
# ------------------------------------------------

def create_heatmap(df):


    metrics = [

        "return_on_equity_pct",
        "debt_to_equity",
        "revenue_cagr_5yr",
        "pat_cagr_5yr",
        "eps_cagr_5yr",
        "operating_profit_margin_pct",
        "net_profit_margin_pct",
        "free_cash_flow_cr",
        "cash_from_operations_cr"

    ]


    corr = df[metrics].corr()


    plt.figure(
        figsize=(12,8)
    )


    sns.heatmap(

        corr,

        annot=True,

        fmt=".2f"

    )


    plt.title(
        "Nifty100 KPI Correlation Matrix"
    )


    plt.tight_layout()


    plt.savefig(
        HEATMAP_FILE
    )


    plt.close()



# ------------------------------------------------
# Outlier Detection
# ------------------------------------------------

def detect_outliers(df):


    metrics = [

        "return_on_equity_pct",
        "debt_to_equity",
        "revenue_cagr_5yr",
        "pat_cagr_5yr",
        "operating_profit_margin_pct"

    ]


    df["outlier_flag"] = False


    records = []


    for metric in metrics:


        mean = df[metric].mean()

        std = df[metric].std()


        df["z_score"] = (

            (df[metric]-mean)
            /
            std

        )


        abnormal = df[
            abs(df["z_score"]) > 3
        ]


        for _, row in abnormal.iterrows():


            records.append(

                {

                "company_id":
                row["company_id"],

                "metric":
                metric,

                "value":
                row[metric],

                "z_score":
                row["z_score"]

                }

            )



    outliers = pd.DataFrame(records)


    outliers.to_csv(
        OUTLIER_FILE,
        index=False
    )



# ------------------------------------------------
# Portfolio Statistics
# ------------------------------------------------

def generate_statistics(df):


    metrics = [

        "return_on_equity_pct",
        "debt_to_equity",
        "revenue_cagr_5yr",
        "pat_cagr_5yr",
        "eps_cagr_5yr",
        "operating_profit_margin_pct",
        "net_profit_margin_pct",
        "free_cash_flow_cr"

    ]



    result=[]



    for metric in metrics:


        result.append(

            {

            "metric":metric,

            "P10":
            df[metric].quantile(.10),

            "P25":
            df[metric].quantile(.25),

            "P50":
            df[metric].median(),

            "P75":
            df[metric].quantile(.75),

            "P90":
            df[metric].quantile(.90),

            "Mean":
            df[metric].mean(),

            "Std":
            df[metric].std()

            }

        )


    pd.DataFrame(result).to_csv(

        STATS_FILE,

        index=False

    )



# ------------------------------------------------
# Main
# ------------------------------------------------


if __name__ == "__main__":


    print(
        "Loading data..."
    )


    data = load_latest_data()



    print(
        "Companies:",
        len(data)
    )


    merged = profile_clusters(
        data
    )


    create_heatmap(
        data
    )


    detect_outliers(
        data
    )


    generate_statistics(
        data
    )


    print(
        "Day 37 completed successfully"
    )