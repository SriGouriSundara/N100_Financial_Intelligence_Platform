"""
KMeans clustering module
Sprint 6 Day 36

Purpose:
Group Nifty100 companies into financial archetypes
"""

import sqlite3
import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

import matplotlib.pyplot as plt


# -----------------------------
# Project paths
# -----------------------------

DB_PATH = "db/nifty100.db"

OUTPUT_FILE = "output/cluster_labels.csv"

ELBOW_FILE = "reports/elbow_plot.png"


# -----------------------------
# Load financial data
# -----------------------------

def load_company_features():
    """
    Load latest year financial metrics
    """

    connection = sqlite3.connect(DB_PATH)
    query = """

SELECT
    fr.company_id,
    fr.return_on_equity_pct,
    fr.debt_to_equity,
    fr.revenue_cagr_5yr,
    fr.free_cash_flow_cr,
    fr.operating_profit_margin_pct

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



    df = pd.read_sql(query, connection)

    connection.close()

    return df



# -----------------------------
# Missing value handling
# -----------------------------

def fill_missing_values(df):
    """
    Replace missing KPI values
    with median values
    """

    features = [
    "return_on_equity_pct",
    "debt_to_equity",
    "revenue_cagr_5yr",
    "free_cash_flow_cr",
    "operating_profit_margin_pct"
]


    for column in features:

        df[column] = df[column].fillna(
            df[column].median()
        )


    return df



# -----------------------------
# Create elbow graph
# -----------------------------

def create_elbow_plot(X):

    inertia = []

    k_values = range(2,11)


    for k in k_values:

        model = KMeans(
            n_clusters=k,
            random_state=42
        )

        model.fit(X)

        inertia.append(
            model.inertia_
        )


    plt.figure(figsize=(8,5))

    plt.plot(
        list(k_values),
        inertia,
        marker="o"
    )


    plt.xlabel("Number of Clusters")

    plt.ylabel("Inertia")

    plt.title(
        "KMeans Elbow Plot"
    )


    plt.savefig(
        ELBOW_FILE,
        bbox_inches="tight"
    )

    plt.close()



# -----------------------------
# Assign cluster names
# -----------------------------

def cluster_names(cluster_id):

    names = {

        0:
        "High Quality Compounders",

        1:
        "Defensive Dividend Payers",

        2:
        "Value Cyclicals",

        3:
        "Distressed or Turnaround",

        4:
        "Emerging Growth"

    }


    return names.get(
        cluster_id,
        "Unknown"
    )



# -----------------------------
# Main clustering function
# -----------------------------

def run_clustering():


    print(
        "Loading company data..."
    )


    df = load_company_features()


    print(
        "Companies loaded:",
        len(df)
    )


    df = fill_missing_values(df)



    features = [
    "return_on_equity_pct",
    "debt_to_equity",
    "revenue_cagr_5yr",
    "free_cash_flow_cr",
    "operating_profit_margin_pct"
]

    X = df[features]



    # Scaling

    scaler = StandardScaler()


    X_scaled = scaler.fit_transform(X)



    # Elbow plot

    create_elbow_plot(
        X_scaled
    )



    # KMeans

    model = KMeans(

        n_clusters=5,

        random_state=42

    )


    df["cluster_id"] = model.fit_predict(
        X_scaled
    )



    # Distance from centroid

    distances = model.transform(
        X_scaled
    )


    df["distance_from_centroid"] = (

        distances.min(axis=1)

    )



    df["cluster_name"] = (

        df["cluster_id"]
        .apply(cluster_names)

    )



    output = df[

        [

        "company_id",

        "cluster_id",

        "cluster_name",

        "distance_from_centroid"

        ]

    ]



    output.to_csv(

        OUTPUT_FILE,

        index=False

    )


    print(
        "Cluster file generated"
    )

if __name__ == "__main__":

    run_clustering()