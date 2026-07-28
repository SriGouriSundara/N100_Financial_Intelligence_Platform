import sqlite3
from pathlib import Path

import pandas as pd

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)
ROOT = Path(__file__).resolve().parents[2]

DATABASE = ROOT / "db" / "nifty100.db"

OUTPUT_DIR = ROOT / "reports" / "sector"

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)
styles = getSampleStyleSheet()

TITLE = styles["Heading1"]

HEADING = styles["Heading2"]

BODY = styles["BodyText"]

BODY.wordWrap = "CJK"
def connect_database():

    print("Database Connected")

    return sqlite3.connect(DATABASE)
def load_companies(connection):

    print("\nLoading Companies")

    companies = pd.read_sql(
        """
        SELECT *
        FROM companies
        """,
        connection
    )

    print(f"Companies : {len(companies)}")
    return companies
def load_sectors(connection):

    print("\nLoading Sectors")

    sectors = pd.read_sql(

        "SELECT * FROM sectors",

        connection

    )

    print(f"Rows : {len(sectors)}")

    return sectors
def load_ratios(connection):

    print("\nLoading Ratios")

    ratios = pd.read_sql(

        "SELECT * FROM financial_ratios",

        connection

    )

    print(f"Rows : {len(ratios)}")

    return ratios
def latest_year_data(df):

    latest = df["year"].max()

    return df[df["year"] == latest].copy()
def get_col(df, *names):

    for name in names:

        if name in df.columns:

            return name

    return None
# ==========================================================
# SECTOR SUMMARY
# ==========================================================

def sector_summary(sector_data):

    def median_value(df, columns):

        for col in columns:

            if col in df.columns:

                values = pd.to_numeric(
                    df[col],
                    errors="coerce"
                ).dropna()

                if len(values):
                    return round(values.median(), 2)

        return 0

    return {

        "Companies": len(sector_data),

        "Median ROE": median_value(
            sector_data,
            [
                "return_on_equity_pct",
                "roe_percentage",
                "roe"
            ]
        ),

        "Median ROCE": median_value(
            sector_data,
            [
                "return_on_capital_employed_pct",
                "roce_percentage",
                "return_on_capital_employed"
            ]
        ),

        "Median Revenue CAGR": median_value(
            sector_data,
            [
                "revenue_cagr_5yr"
            ]
        ),

        "Median PAT CAGR": median_value(
            sector_data,
            [
                "pat_cagr_5yr"
            ]
        ),

        "Median D/E": median_value(
            sector_data,
            [
                "debt_to_equity"
            ]
        ),

        "Median Quality": median_value(
            sector_data,
            [
                "composite_quality_score"
            ]
        )

    }
    # ------------------------------------------------------
    # Safe helper
    # ------------------------------------------------------

    def median_value(df, columns):

        for col in columns:

            if col in df.columns:

                values = pd.to_numeric(
                    df[col],
                    errors="coerce"
                )

                if values.notna().any():
                    return round(values.median(), 2)

        return "N/A"

    # ------------------------------------------------------
    # Median KPIs
    # ------------------------------------------------------

    summary = [

        ["Metric", "Median"],

        [
            "ROE %",
            median_value(
                sector_data,
                [
                    "return_on_equity_pct",
                    "roe_percentage",
                    "roe"
                ]
            )
        ],

        [
            "ROCE %",
            median_value(
                sector_data,
                [
                    "return_on_capital_employed_pct",
                    "roce_percentage",
                    "return_on_capital_employed"
                ]
            )
        ],

        [
            "Revenue CAGR %",
            median_value(
                sector_data,
                ["revenue_cagr_5yr"]
            )
        ],

        [
            "PAT CAGR %",
            median_value(
                sector_data,
                ["pat_cagr_5yr"]
            )
        ],

        [
            "Debt / Equity",
            median_value(
                sector_data,
                ["debt_to_equity"]
            )
        ],

        [
            "Quality Score",
            median_value(
                sector_data,
                ["composite_quality_score"]
            )
        ]

    ]

    table = Table(summary, colWidths=[230, 120])

    table.setStyle(

        TableStyle([

            ("BACKGROUND", (0,0), (-1,0), colors.navy),

            ("TEXTCOLOR", (0,0), (-1,0), colors.white),

            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),

            ("GRID", (0,0), (-1,-1), 0.5, colors.grey),

            ("BACKGROUND", (0,1), (-1,-1), colors.whitesmoke),

            ("ALIGN", (1,1), (-1,-1), "CENTER"),

            ("BOTTOMPADDING", (0,0), (-1,0), 8)

        ])

    )
    story.append(table)

def cover_page(

    story,

    sector_name,

    summary

):

    story.append(

        Paragraph(

            f"{sector_name} Sector Report",

            TITLE

        )

    )

    story.append(Spacer(1, 0.3 * inch))

    data = [

        ["Metric", "Value"],

        ["Companies", summary["Companies"]],

        ["Median ROE", f'{summary["Median ROE"]:.2f}%'],

        ["Median ROCE", f'{summary["Median ROCE"]:.2f}%'],

        ["Median D/E", f'{summary["Median D/E"]:.2f}'],

        ["Median Revenue CAGR",

         f'{summary["Median Revenue CAGR"]:.2f}%'],

        ["Median PAT CAGR",

         f'{summary["Median PAT CAGR"]:.2f}%']

    ]

    table = Table(

        data,

        colWidths=[220, 180]

    )

    table.setStyle(

        TableStyle([

            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),

            ("BACKGROUND", (0, 0), (-1, 0), colors.navy),

            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

            ("ALIGN", (0, 0), (-1, -1), "CENTER"),

            ("BOTTOMPADDING", (0, 0), (-1, 0), 8)

        ])

    )

    story.append(table)

    story.append(Spacer(1, 0.4 * inch))
def company_table(

    story,

    companies,

    ratios

):

    latest = latest_year_data(ratios)

    latest = latest[

        latest.company_id.isin(companies)

    ]

    latest = latest.sort_values(

        "company_id"

    )

    table_data = [[

        "Company",

        "ROE",

        "ROCE",

        "Revenue CAGR",

        "PAT CAGR",

        "EPS CAGR",

        "D/E",

        "Quality"

    ]]

    for _, row in latest.iterrows():

        table_data.append([

            Paragraph(

                str(row["company_id"]),

                BODY

            ),

            f'{row.get("return_on_equity_pct", row.get("roe_percentage", 0)):.1f}',

f'{row.get("return_on_capital_employed_pct",
           row.get("roce_percentage", 0)):.1f}',
            f'{row["revenue_cagr_5yr"]:.1f}',

            f'{row["pat_cagr_5yr"]:.1f}',

            f'{row["eps_cagr_5yr"]:.1f}',

            f'{row["debt_to_equity"]:.2f}',

            f'{row["composite_quality_score"]:.0f}'

        ])

    table = Table(

        table_data,

        repeatRows=1,

        colWidths=[95, 50, 50, 70, 70, 70, 50, 60]

    )

    table.setStyle(

        TableStyle([

            ("GRID", (0, 0), (-1, -1), 0.3, colors.grey),

            ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),

            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

            ("WORDWRAP", (0, 0), (-1, -1), "CJK"),

            ("FONTSIZE", (0, 0), (-1, -1), 8)

        ])

    )

    story.append(table)
# ==========================================================
# GENERATE SECTOR REPORT
# ==========================================================
def generate_sector_report(
    sector_name,
    sector_companies,
    ratios
):

    pdf_path = OUTPUT_DIR / f"{sector_name}_report.pdf"

    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=A4
    )

    story = []

    sector_data = ratios[
        ratios["company_id"].isin(sector_companies)
    ].copy()

    latest_year = sector_data["year"].max()

    latest_data = sector_data[
        sector_data["year"] == latest_year
    ].copy()

    summary = sector_summary(latest_data)

    cover_page(
        story,
        sector_name,
        summary
    )

    company_table(
    story,
    sector_companies,
    ratios
)
    doc.build(story)

    print(f"Generated : {pdf_path.name}")

# ==========================================================
# MAIN
# ==========================================================
def main():

    print("=" * 60)
    print("Sprint 5 Day 34 - Sector Report Generation")
    print("=" * 60)

    connection = connect_database()

    sectors = load_sectors(connection)
    companies = load_companies(connection)
    ratios = load_ratios(connection)

    # Rename company id if required
    companies = companies.rename(
        columns={
            "id": "company_id"
        }
    )

    # Merge sector names into ratios
    ratios = ratios.merge(
        sectors[
            [
                "company_id",
                "broad_sector"
            ]
        ],
        on="company_id",
        how="left"
    )

    print("\nGenerating Sector Reports")
    print("-" * 40)

    generated = 0

    for sector in sorted(
        ratios["broad_sector"].dropna().unique()
    ):

        sector_df = ratios[
            ratios["broad_sector"] == sector
        ]

        company_ids = sector_df[
            "company_id"
        ].unique()

        try:

            generate_sector_report(
                sector,
                company_ids,
                ratios
            )

            generated += 1

        except Exception as e:

            print(f"✗ Failed : {sector}")
            print(e)

    connection.close()

    print("\n" + "=" * 60)
    print("Day 34 Summary")
    print("=" * 60)

    print(f"Total Sectors      : {len(ratios['broad_sector'].dropna().unique())}")
    print(f"Reports Generated  : {generated}")
    print(f"Output Folder      : {OUTPUT_DIR}")

    print("\nCompleted Successfully")


if __name__ == "__main__":
    main()