import sqlite3
from pathlib import Path

import pandas as pd

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak
)

ROOT = Path(__file__).resolve().parents[2]

DATABASE = ROOT / "db" / "nifty100.db"

PORTFOLIO_DIR = ROOT / "reports" / "portfolio"

PORTFOLIO_DIR.mkdir(
    parents=True,
    exist_ok=True
)

OUTPUT_FILE = PORTFOLIO_DIR / "portfolio_summary.pdf"

styles = getSampleStyleSheet()

TITLE = styles["Heading1"]

HEADING = styles["Heading2"]

BODY = styles["BodyText"]

BODY.wordWrap = "CJK"
def connect_database():

    print("Database Connected")

    return sqlite3.connect(DATABASE)
def load_companies(connection):

    print("Loading Companies")

    df = pd.read_sql(

        "SELECT * FROM companies",

        connection

    )

    print(f"Companies : {len(df)}")

    return df
def load_sectors(connection):

    print("Loading Sectors")

    df = pd.read_sql(

        "SELECT * FROM sectors",

        connection

    )

    print(f"Rows : {len(df)}")

    return df
def load_ratios(connection):

    print("Loading Financial Ratios")

    df = pd.read_sql(

        "SELECT * FROM financial_ratios",

        connection

    )

    print(f"Rows : {len(df)}")

    return df
def latest_year_data(df):

    latest_year = df["year"].max()

    return df[df["year"] == latest_year].copy()
def print_header(title):

    print("\n" + "=" * 60)

    print(title)

    print("=" * 60)
# ==========================================================
# TREND ARROW
# ==========================================================

def trend_arrow(history, column):

    if column not in history.columns:
        return "→"

    history = history.sort_values("year")

    if len(history) < 2:
        return "→"

    latest = history.iloc[-1][column]
    previous = history.iloc[-2][column]

    if pd.isna(latest) or pd.isna(previous):
        return "→"

    if previous == 0:
        return "→"

    pct_change = ((latest - previous) / abs(previous)) * 100

    if pct_change > 2:
        return "↑"

    elif pct_change < -2:
        return "↓"

    else:
        return "→"
# ==========================================================
# COMPANY PAGE
# ==========================================================

def company_page(

    story,
    company,
    companies_df,
    sectors_df,
    ratios_df

):

    company_row = companies_df[
        companies_df["id"] == company
    ]

    if company_row.empty:
        return

    sector_row = sectors_df[
        sectors_df["company_id"] == company
    ]

    history = (

        ratios_df[
            ratios_df["company_id"] == company
        ]
        .sort_values("year")
    )

    if history.empty:
        return

    latest = history.iloc[-1]
    company_name = company

    if "company_name" in company_row.columns:
        company_name = company_row.iloc[0]["company_name"]

    sector = "-"

    if not sector_row.empty:
        sector = sector_row.iloc[0]["broad_sector"]

    story.append(
        Paragraph(
            f"<b>{company_name}</b>",
            TITLE
        )
    )

    story.append(
        Paragraph(
            f"Sector : {sector}",
            BODY
        )
    )

    story.append(
        Spacer(1, 0.20 * inch)
    )
    data = [

        ["Metric", "Value", "Trend"],

        [
            "ROE",

            f"{latest.get('return_on_equity_pct',0):.2f}%",

            trend_arrow(
                history,
                "return_on_equity_pct"
            )
        ],

        [
            "ROCE",

            f"{latest.get('return_on_capital_employed_pct',0):.2f}%",

            trend_arrow(
                history,
                "return_on_capital_employed_pct"
            )
        ],

        [
            "Revenue CAGR",

            f"{latest.get('revenue_cagr_5yr',0):.2f}%",

            trend_arrow(
                history,
                "revenue_cagr_5yr"
            )
        ],

        [
            "PAT CAGR",

            f"{latest.get('pat_cagr_5yr',0):.2f}%",

            trend_arrow(
                history,
                "pat_cagr_5yr"
            )
        ],

        [
            "Debt / Equity",

            f"{latest.get('debt_to_equity',0):.2f}",

            trend_arrow(
                history,
                "debt_to_equity"
            )
        ],

        [
            "Quality Score",

            f"{latest.get('composite_quality_score',0):.0f}",

            trend_arrow(
                history,
                "composite_quality_score"
            )
        ]

    ]
    table = Table(

        data,

        colWidths=[220,120,70]

    )

    table.setStyle(

        TableStyle([

            ("GRID",(0,0),(-1,-1),0.5,colors.grey),

            ("BACKGROUND",(0,0),(-1,0),colors.navy),

            ("TEXTCOLOR",(0,0),(-1,0),colors.white),

            ("ALIGN",(0,0),(-1,-1),"CENTER"),

            ("WORDWRAP",(0,0),(-1,-1),"CJK"),

            ("BOTTOMPADDING",(0,0),(-1,0),8),

            ("FONTSIZE",(0,0),(-1,-1),10)

        ])

    )

    story.append(table)

    story.append(PageBreak())
# ==========================================================
# BUILD PORTFOLIO PDF
# ==========================================================

def build_portfolio_pdf(

    companies_df,
    sectors_df,
    ratios_df

):

    story = []

    companies = sorted(
        ratios_df["company_id"].unique()
    )

    for company in companies:

        company_page(

            story,

            company,

            companies_df,

            sectors_df,

            ratios_df

        )

    doc = SimpleDocTemplate(

    str(OUTPUT_FILE),

    pagesize=A4

)

    doc.build(story)

    print(f"\nGenerated : {OUTPUT_FILE.name}")                        
def main():

    print_header("Sprint 5 Day 35")

    connection = connect_database()

    companies = load_companies(connection)

    sectors = load_sectors(connection)

    ratios = load_ratios(connection)

    latest = latest_year_data(ratios)

    print_header("Foundation Ready")

    print(f"Companies      : {len(companies)}")

    print(f"Sectors        : {len(sectors)}")

    print(f"Ratio Records  : {len(ratios)}")

    print(f"Latest Records : {len(latest)}")
    print_header("Generating Portfolio Summary")

    build_portfolio_pdf(

        companies,

        sectors,

        ratios

    )

    print_header("Day 35 Summary")

    print(f"Companies Processed : {len(latest)}")

    print(f"Pages Generated     : {len(latest)}")

    print(f"Output File         : {str(OUTPUT_FILE)}")

    connection.close()
if __name__ == "__main__":
    main()