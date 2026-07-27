"""
============================================================
Sprint 5 Day 33
Company Tearsheet Generator
============================================================
"""

from pathlib import Path
import sqlite3
import pandas as pd

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch

from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.graphics import renderPDF
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import (
    Paragraph,
    Table,
    TableStyle
)

# ==========================================================
# PARAGRAPH STYLE
# ==========================================================

styles = getSampleStyleSheet()

bullet_style = styles["BodyText"]

bullet_style.fontName = "Helvetica"

bullet_style.fontSize = 9

bullet_style.leading = 12

bullet_style.alignment = TA_LEFT
# ==========================================================
# PROJECT PATHS
# ==========================================================

ROOT = Path(__file__).resolve().parents[2]

DATABASE = ROOT / "db" / "nifty100.db"

OUTPUT_FOLDER = ROOT / "reports" / "tearsheets"

OUTPUT_FOLDER.mkdir(

    parents=True,

    exist_ok=True

)

PROS_CONS = ROOT / "output" / "pros_cons_generated.csv"

cashflow_intelligence_df = ROOT / "output" / "cashflow_intelligence.xlsx"

# ==========================================================
# PDF CONSTANTS
# ==========================================================

PAGE_WIDTH, PAGE_HEIGHT = A4

MARGIN = 35

HEADER_HEIGHT = 45

KPI_HEIGHT = 55

CONTENT_WIDTH = PAGE_WIDTH - (2 * MARGIN)

styles = getSampleStyleSheet()

# ==========================================================
# TEST COMPANIES
# ==========================================================

TEST_COMPANIES = [

    "TCS",

    "HDFCBANK",

    "RELIANCE",

    "SUNPHARMA",

    "TATASTEEL"

]
# ==========================================================
# COLORS
# ==========================================================

NAVY = colors.HexColor("#17375E")

GREEN = colors.HexColor("#228B22")

RED = colors.HexColor("#C00000")

LIGHT_GREY = colors.HexColor("#F3F3F3")

DARK_GREY = colors.HexColor("#404040")

WHITE = colors.white
# ==========================================================
# DATABASE
# ==========================================================
def connect_database():
    connection = sqlite3.connect(DATABASE)
    print("Database Connected")
    return connection
# ==========================================================
# PRINT HEADER
# ==========================================================

def print_header(title):

    print()

    print("=" * 60)

    print(title)

    print("=" * 60)
# ==========================================================
# LOAD COMPANY MASTER
# ==========================================================

def load_companies(connection):

    print_header("Loading Companies")

    df = pd.read_sql(

        "SELECT * FROM companies",

        connection

    )

    print(f"Companies : {len(df)}")

    return df
# ==========================================================
# LOAD RATIOS
# ==========================================================

def load_ratios(connection):

    print_header("Loading Financial Ratios")

    df = pd.read_sql(

        "SELECT * FROM financial_ratios",

        connection

    )

    print(f"Rows : {len(df)}")

    return df
# ==========================================================
# LOAD PROFIT & LOSS
# ==========================================================

def load_profit_loss(connection):

    print_header("Loading Profit & Loss")

    df = pd.read_sql(

        "SELECT * FROM profitandloss",

        connection

    )

    print(f"Rows : {len(df)}")
    return df
# ==========================================================
# LOAD BALANCE SHEET
# ==========================================================

def load_balance_sheet(connection):

    print_header("Loading Balance Sheet")

    df = pd.read_sql(

        "SELECT * FROM balancesheet",

        connection

    )

    print(f"Rows : {len(df)}")

    return df
# ==========================================================
# LOAD CASH FLOW
# ==========================================================

def load_cashflow(connection):

    print_header("Loading Cash Flow")

    df = pd.read_sql(

        "SELECT * FROM cashflow",

        connection

    )

    print(f"Rows : {len(df)}")

    return df
# ==========================================================
# LOAD PROS / CONS
# ==========================================================

def load_pros_cons():

    print_header("Loading Pros & Cons")

    df = pd.read_csv(PROS_CONS)

    print(f"Rows : {len(df)}")

    return df
# ==========================================================
# LOAD CASHFLOW INTELLIGENCE
# ==========================================================

def load_cashflow_intelligence():

    print_header("Loading Cashflow Intelligence")

    df = pd.read_excel(cashflow_intelligence_df)

    print(f"Rows : {len(df)}")

    return df
def load_sectors(connection):

    print_header("Loading Sectors")

    query = "SELECT * FROM sectors"

    sectors = pd.read_sql(query, connection)

    print(f"Rows : {len(sectors)}")
    return sectors
# ==========================================================
# GET COMPANY INFORMATION
# ==========================================================
def get_company_info(
    companies_df,
    sectors_df,
    company_id
):

    company = companies_df[
        companies_df["id"] == company_id
    ]

    if company.empty:
        return {}

    row = company.iloc[0]

    sector = "Unknown"

    sector_row = sectors_df[
        sectors_df["company_id"] == company_id
    ]

    if not sector_row.empty:

        sector = sector_row.iloc[0]["broad_sector"]

    return {

    "company_id": row["id"],

    "company_name": row["company_name"],

    "sector": sector,

    "website": row.get("website", ""),

    "roe_percentage": row.get("roe_percentage", 0),

    "roce_percentage": row.get("roce_percentage", 0)

}
# ==========================================================
# LATEST FINANCIAL YEAR
# ==========================================================

def latest_year(

    ratios_df,

    company_id

):

    company = ratios_df[

        ratios_df["company_id"] == company_id

    ]

    if company.empty:

        return ""

    return int(

        company["year"].max()
    )
# ==========================================================
# GET LATEST RATIO RECORD
# ==========================================================

def get_latest_ratios(ratios_df, company_id):

    company = ratios_df[
        ratios_df["company_id"] == company_id
    ]

    if company.empty:
        return {}

    latest = (
        company
        .sort_values("year")
        .iloc[-1]
    )

    return latest
def get_financial_history(pl_df, company_id):

    print("\n==============================")
    print("DEBUG : get_financial_history")
    print("==============================")
    print("Company :", company_id)
    print("Columns :", pl_df.columns.tolist())

    company = pl_df[
        pl_df["company_id"] == company_id
    ].copy()

    print("Filtered Columns :", company.columns.tolist())
    print("Rows :", len(company))

    company = company.sort_values("year")

    return company.tail(10)
# ==========================================================
# COMPANY FINANCIAL HISTORY
# ==========================================================

def get_financial_history(pl, company):

    history = (

        pl[
            pl["company_id"] == company
        ]
        .sort_values("year")
        .tail(10)

    )

    return history
# ==========================================================
# GET BALANCE SHEET HISTORY
# ==========================================================

def get_balance_sheet_history(

    balance_df,

    company_id

):

    history = (

        balance_df[
            balance_df["company_id"] == company_id
        ]
        .sort_values("year")
        .tail(10)
        .copy()

    )

    return history
def get_latest_cashflow(cashflow_df, company_id):

    company = cashflow_df[
        cashflow_df["company_id"] == company_id
    ].copy()

    if company.empty:
        return None

    year_column = None

    for col in [
        "year",
        "financial_year",
        "fy",
        "report_year",
    ]:
        if col in company.columns:
            year_column = col
            break

    if year_column is None:
        raise KeyError(
            f"No year column found.\nAvailable columns:\n{company.columns.tolist()}"
        )

    company = company.sort_values(year_column)

    return company.iloc[-1]
# ==========================================================
# SAFE CASHFLOW VALUE
# ==========================================================

def get_cashflow_value(

    row,

    possible_columns,

    default=0

):

    for col in possible_columns:

        if col in row.index:

            value = row[col]

            if pd.notna(value):

                return value

    return default
# ==========================================================
# SAFE COLUMN FETCH
# ==========================================================

def get_column(

    dataframe,

    possible_columns,

    default=0

):

    for column in possible_columns:

        if column in dataframe.columns:

            return dataframe[column].fillna(default)

    return pd.Series(

        [default] * len(dataframe)

    )
# ==========================================================
# BALANCE SHEET COMPOSITION
# ==========================================================

def draw_balance_sheet_chart(

    pdf,

    balance_history,

    x,

    y

):

    drawing = Drawing(500, 230)

    chart = VerticalBarChart()

    chart.x = 45
    chart.y = 35

    chart.width = 380
    chart.height = 140

    equity = get_column(

        balance_history,

        [

            "total_equity",

            "equity",

            "shareholders_equity",

            "equity_cr"

        ]

    ).tolist()

    borrowings = get_column(

        balance_history,

        [

            "borrowings",

            "total_borrowings",

            "debt",

            "borrowings_cr"

        ]

    ).tolist()

    liabilities = get_column(

        balance_history,

        [

            "other_liabilities",

            "total_liabilities",

            "liabilities",

            "other_liabilities_cr"

        ]

    ).tolist()

    chart.data = [

        equity,

        borrowings,

        liabilities

    ]

    chart.categoryAxis.categoryNames = [

        str(year)

        for year in balance_history["year"]

    ]

    max_value = max(

        max(equity, default=0),

        max(borrowings, default=0),

        max(liabilities, default=0)

    )

    chart.valueAxis.valueMin = 0
    chart.valueAxis.valueMax = max_value * 1.20 if max_value > 0 else 100

    chart.bars[0].fillColor = HexColor("#1E88E5")
    chart.bars[1].fillColor = HexColor("#EF6C00")
    chart.bars[2].fillColor = HexColor("#8E24AA")

    drawing.add(chart)

    renderPDF.draw(

        drawing,

        pdf,

        x,

        y

    )

    pdf.setFont(

        "Helvetica-Bold",

        13

    )

    pdf.drawString(

        x,

        y + 195,

        "Balance Sheet Composition (10 Years)"

    )

    pdf.setFont(

        "Helvetica",

        9

    )

    pdf.drawString(

        x,

        y + 180,

        "Blue = Equity   Orange = Borrowings   Purple = Other Liabilities"

    )
# ==========================================================
# PAGE HEADER
# ==========================================================

from reportlab.lib.colors import HexColor, white

NAVY = HexColor("#0B2E59")


def draw_header(pdf, info, year):
    """
    Professional Page-1 Header
    """

    # Navy Banner
    pdf.setFillColor(NAVY)
    pdf.rect(0, 760, 595, 82, stroke=0, fill=1)

    # Company Name
    pdf.setFillColor(white)
    pdf.setFont("Helvetica-Bold", 22)
    pdf.drawString(
        30,
        808,
        str(info.get("company_name", ""))
    )

    # Company ID
    pdf.setFont("Helvetica", 12)
    pdf.drawString(
        30,
        788,
        f"Ticker : {info.get('company_id','')}"
    )

    # Sector
    pdf.drawString(
        180,
        788,
        f"Sector : {info.get('sector','Unknown')}"
    )

    # FY
    pdf.drawString(
        420,
        788,
        f"FY {year}"
    )
# ==========================================================
# REPORT TITLE
# ==========================================================

# ==========================================================
# REPORT TITLE
# ==========================================================

from reportlab.lib.colors import HexColor

TITLE = HexColor("#143C72")


def draw_report_title(pdf):

    pdf.setFillColor(TITLE)

    pdf.setFont(
        "Helvetica-Bold",
        18
    )

    pdf.drawString(
        30,
        735,
        "Company Financial Tearsheet"
    )

    pdf.setFont(
        "Helvetica",
        11
    )

    pdf.drawString(
        30,
        718,
        "Financial Performance • Quality • Cash Flow • Capital Allocation"
    )
# ==========================================================
# DRAW SINGLE KPI TILE
# ==========================================================

def draw_kpi_tile(

    pdf,

    x,

    y,

    title,

    value,

    width=165,

    height=60

):

    pdf.setFillColorRGB(
        0.95,
        0.95,
        0.95
    )

    pdf.roundRect(

        x,

        y,

        width,

        height,

        8,

        fill=1,

        stroke=0

    )

    pdf.setFillColorRGB(0,0,0)

    pdf.setFont(

        "Helvetica-Bold",

        10

    )

    pdf.drawString(

        x+10,

        y+42,

        title

    )

    pdf.setFont(

        "Helvetica-Bold",

        18

    )

    pdf.drawString(

        x+10,

        y+15,

        value

    )    
# ==========================================================
# DRAW KPI DASHBOARD
# ==========================================================

def draw_kpis(

    pdf,

    ratio,

    info

):

    x = 40
    gap = 12
    w = 165
    h = 60

    row1 = PAGE_HEIGHT - 190
    row2 = PAGE_HEIGHT - 265

    # -------------------------------
    # Row 1
    # -------------------------------

    draw_kpi_tile(
        pdf,
        x,
        row1,
        "ROE",
        f"{ratio['return_on_equity_pct']:.1f}%"
    )

    draw_kpi_tile(
        pdf,
        x + w + gap,
        row1,
        "ROCE",
        f"{info['roce_percentage']:.1f}%"
    )

    draw_kpi_tile(
        pdf,
        x + 2 * (w + gap),
        row1,
        "Revenue CAGR",
        f"{ratio['revenue_cagr_5yr']:.1f}%"
    )

    # -------------------------------
    # Row 2
    # -------------------------------

    draw_kpi_tile(
        pdf,
        x,
        row2,
        "PAT CAGR",
        f"{ratio['pat_cagr_5yr']:.1f}%"
    )

    draw_kpi_tile(
        pdf,
        x + w + gap,
        row2,
        "Debt / Equity",
        f"{ratio['debt_to_equity']:.2f}"
    )

    draw_kpi_tile(
        pdf,
        x + 2 * (w + gap),
        row2,
        "Quality Score",
        f"{ratio['composite_quality_score']:.0f}"
    )
# ==========================================================
# DRAW REVENUE CHART
# ==========================================================

def draw_revenue_chart(pdf, history):

    drawing = Drawing(250,160)

    chart = VerticalBarChart()

    chart.x = 30
    chart.y = 20

    chart.width = 180
    chart.height = 100

    revenue = history["sales"].fillna(0).tolist()

    chart.data = [revenue]

    chart.categoryAxis.categoryNames = [

        str(y)

        for y in history["year"]

    ]

    chart.valueAxis.valueMin = 0

    chart.bars[0].fillColor = HexColor("#1565C0")

    drawing.add(chart)

    renderPDF.draw(

        drawing,

        pdf,

        35,

        120

    )

    pdf.setFont(

        "Helvetica-Bold",

        11

    )

    pdf.drawString(

        35,

        280,

        "Revenue (10 Years)"

    )   
# ==========================================================
# DRAW NET PROFIT CHART
# ==========================================================

def draw_profit_chart(pdf, history):

    drawing = Drawing(250,160)

    chart = VerticalBarChart()

    chart.x = 30
    chart.y = 20

    chart.width = 180
    chart.height = 100

    profits = history["net_profit"].fillna(0).tolist()

    chart.data = [profits]

    chart.categoryAxis.categoryNames = [

        str(y)

        for y in history["year"]

    ]

    chart.valueAxis.valueMin = min(

        0,

        min(profits)

    )

    chart.bars[0].fillColor = HexColor("#2E7D32")

    drawing.add(chart)

    renderPDF.draw(

        drawing,

        pdf,

        305,

        120

    )

    pdf.setFont(

        "Helvetica-Bold",

        11

    )

    pdf.drawString(

        305,

        280,

        "Net Profit (10 Years)"

    )          
# ==========================================================
# DRAW ROE & OPM TREND
# ==========================================================

def draw_ratio_trend(pdf, ratios_df, company):

    history = (

        ratios_df[
            ratios_df["company_id"] == company
        ]
        .sort_values("year")
        .tail(10)

    )

    drawing = Drawing(520,180)

    chart = HorizontalLineChart()

    chart.x = 40
    chart.y = 30

    chart.width = 420
    chart.height = 100

    roe = history["return_on_equity_pct"].fillna(0).tolist()

    opm = history["operating_profit_margin_pct"].fillna(0).tolist()

    chart.data = [

        roe,

        opm

    ]

    chart.categoryAxis.categoryNames = [

        str(y)

        for y in history["year"]

    ]

    chart.lines[0].strokeColor = HexColor("#1565C0")

    chart.lines[1].strokeColor = HexColor("#D32F2F")

    drawing.add(chart)

    renderPDF.draw(

        drawing,

        pdf,

        40,

        -40

    )

    pdf.setFont(

        "Helvetica-Bold",

        11

    )

    pdf.drawString(

        40,

        150,

        "ROE vs Operating Margin"

    )          
# ==========================================================
# CREATE PDF
# ==========================================================

def create_pdf(company):

    pdf_file = OUTPUT_FOLDER / f"{company}.pdf"

    pdf = canvas.Canvas(

        str(pdf_file),

        pagesize=A4

    )

    return pdf
# ==========================================================
# DRAW EMPTY PAGE
# ==========================================================

def draw_page(pdf, page_number):

    pdf.setFont(

        "Helvetica-Bold",

        20

    )

    pdf.drawString(

        40,

        PAGE_HEIGHT - 40,

        f"Company Tearsheet - Page {page_number}"

    )
# ==========================================================
# GENERATE COMPANY TEARSHEET
# ==========================================================

def generate_tearsheet(
    company,
    companies_df,
    sectors_df,
    ratios_df,
    balance_sheet_df,
    cashflow_df,
    profit_loss_df,
    cashflow_intelligence_df,
    pros_cons_df
):
    # Company Information
    info = get_company_info(
    companies_df,
    sectors_df,
    company
)

    # Latest Financial Year
    year = latest_year(
        ratios_df,
        company
    )

    # Latest Ratio Record
    latest_ratio = get_latest_ratios(
        ratios_df,
        company
    )

    # 10-Year Profit & Loss History
    history = get_financial_history(
        profit_loss_df,
        company
    )

    # Create PDF
    pdf = create_pdf(company)

    # ======================================================
    # PAGE 1
    # ======================================================

    draw_header(
        pdf,
        info,
        year
    )

    draw_report_title(pdf)

    draw_kpis(
    pdf,
    latest_ratio,
    info
)

    draw_revenue_chart(
        pdf,
        history
    )

    draw_profit_chart(
        pdf,
        history
    )

    draw_ratio_trend(
        pdf,
        ratios_df,
        company
    )

# ======================================================
# PAGE 2
# ======================================================
    pdf.showPage()

# -------------------------------
# Balance Sheet
# -------------------------------

    balance_history = get_balance_sheet_history(
    balance_sheet_df,
    company
)

    draw_balance_sheet_chart(
    pdf,
    balance_history,
    40,
    470
)

# -------------------------------
# Cash Flow
# -------------------------------

    latest_cf = get_latest_cashflow(
    cashflow_df,
    company
)

    draw_cashflow_waterfall(
    pdf,
    latest_cf,
    40,
    180
)

    draw_cashflow_summary(
    pdf,
    latest_cf,
    340,
    330
)
    pros, cons = get_company_pros_cons(
    pros_cons_df,
    company
)

    draw_pros(
    pdf,
    pros,
    40,
    220
)

    draw_cons(
    pdf,
    cons,
    310,
    220
)
    allocation = get_capital_allocation(
    cashflow_intelligence_df,
    company

)

    draw_capital_allocation_badge(
    pdf,
    allocation,
    180,
    25
)
    pdf.save()
    print(f"Generated : {company}.pdf")
# ==========================================================
# CASH FLOW WATERFALL
# ==========================================================

def draw_cashflow_waterfall(

    pdf,

    latest_cf,

    x,

    y

):

    if latest_cf is None:

        return

    cfo = get_cashflow_value(

        latest_cf,

        [

            "cash_from_operating_activity",

            "cash_from_operations",

            "cash_from_operations_cr",

            "operating_activity"

        ]

    )

    cfi = get_cashflow_value(

        latest_cf,

        [

            "cash_from_investing_activity",

            "investing_activity",

            "investing_activity_cr"

        ]

    )

    cff = get_cashflow_value(

        latest_cf,

        [

            "cash_from_financing_activity",

            "financing_activity",

            "financing_activity_cr"

        ]

    )

    net_cash = cfo + cfi + cff

    drawing = Drawing(420,220)

    chart = VerticalBarChart()

    chart.x = 40
    chart.y = 35

    chart.width = 260
    chart.height = 120

    chart.data = [[

        cfo,

        cfi,

        cff,

        net_cash

    ]]

    chart.categoryAxis.categoryNames = [

        "CFO",

        "CFI",

        "CFF",

        "Net"

    ]

    max_val = max(

        abs(cfo),

        abs(cfi),

        abs(cff),

        abs(net_cash),

        1

    )

    chart.valueAxis.valueMin = -max_val * 1.20
    chart.valueAxis.valueMax = max_val * 1.20

    chart.bars[0].fillColor = HexColor("#4CAF50")

    drawing.add(chart)

    renderPDF.draw(

        drawing,

        pdf,

        x,

        y

    )

    pdf.setFont(

        "Helvetica-Bold",

        13

    )

    pdf.drawString(

        x,

        y + 185,

        "Latest Year Cash Flow"

    )
# ==========================================================
# GET COMPANY PROS & CONS
# ==========================================================

def get_company_pros_cons(

    pros_cons_df,

    company_id

):

    company = pros_cons_df[

        pros_cons_df["company_id"] == company_id

    ]

    pros = company[

        company["type"].str.lower() == "pro"

    ]["text"].tolist()

    cons = company[

        company["type"].str.lower() == "con"

    ]["text"].tolist()

    return pros, cons
# ==========================================================
# GET CAPITAL ALLOCATION LABEL
# ==========================================================

def get_capital_allocation(

    cashflow_kpi_df,

    company_id

):

    company = cashflow_kpi_df[

        cashflow_kpi_df["company_id"] == company_id

    ]

    if company.empty:

        return "Unavailable"

    if "capital_allocation_label" not in company.columns:

        return "Unavailable"

    value = company.iloc[0]["capital_allocation_label"]

    if pd.isna(value):

        return "Unavailable"

    return str(value)
# ==========================================================
# BADGE COLOR
# ==========================================================

def get_badge_color(label):

    label = str(label).lower()

    if "reinvestor" in label:
        return HexColor("#4CAF50")

    elif "shareholder" in label:
        return HexColor("#1565C0")

    elif "growth" in label:
        return HexColor("#7B1FA2")

    elif "mixed" in label:
        return HexColor("#FF9800")

    elif "distress" in label:
        return HexColor("#D32F2F")

    elif "liquidating" in label:
        return HexColor("#6D4C41")

    elif "pre-revenue" in label:
        return HexColor("#546E7A")

    return HexColor("#9E9E9E")
# ==========================================================
# CAPITAL ALLOCATION BADGE
# ==========================================================

def draw_capital_allocation_badge(
    pdf,
    label,
    x,
    y
):

    width = 220
    height = 35

    color = get_badge_color(label)

    # Title
    pdf.setFillColor(colors.black)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawCentredString(
        x + width / 2,
        y + 50,
        "Capital Allocation Pattern"
    )

    # Badge
    pdf.setFillColor(color)

    pdf.roundRect(
        x,
        y,
        width,
        height,
        10,
        fill=1,
        stroke=0
    )

    pdf.setFillColor(colors.white)
    pdf.setFont("Helvetica-Bold", 14)

    pdf.drawCentredString(
        x + width / 2,
        y + 12,
        label
    )

    pdf.setFillColor(colors.black)
# ==========================================================
# DRAW PROS
# ==========================================================

def draw_pros(

    pdf,

    pros,

    x,

    y,

    width=250

):

    pdf.setFont(

        "Helvetica-Bold",

        13

    )

    pdf.setFillColor(HexColor("#2E7D32"))

    pdf.drawString(

        x,

        y,

        "Pros"

    )

    current_y = y - 20

    for text in pros[:5]:

        paragraph = Paragraph(

            f'<font color="green">•</font> {text}',

            bullet_style

        )

        w, h = paragraph.wrap(

            width,

            100

        )

        paragraph.drawOn(

            pdf,

            x,

            current_y - h

        )

        current_y -= h + 8
# ==========================================================
# DRAW CONS
# ==========================================================

def draw_cons(

    pdf,

    cons,

    x,

    y,

    width=250

):

    pdf.setFont(

        "Helvetica-Bold",

        13

    )

    pdf.setFillColor(HexColor("#C62828"))

    pdf.drawString(

        x,

        y,

        "Cons"

    )

    current_y = y - 20

    for text in cons[:5]:

        paragraph = Paragraph(

            f'<font color="red">•</font> {text}',

            bullet_style

        )

        w, h = paragraph.wrap(

            width,

            100

        )

        paragraph.drawOn(

            pdf,

            x,

            current_y - h

        )

        current_y -= h + 8            
# ==========================================================
# CASH FLOW SUMMARY
# ==========================================================

def draw_cashflow_summary(

    pdf,

    latest_cf,

    x,

    y

):

    if latest_cf is None:

        return

    cfo = get_cashflow_value(

        latest_cf,

        [

            "cash_from_operations",

            "cash_from_operations_cr",

            "operating_activity"

        ]

    )

    cfi = get_cashflow_value(

        latest_cf,

        [

            "investing_activity",

            "investing_activity_cr"

        ]

    )

    cff = get_cashflow_value(

        latest_cf,

        [

            "financing_activity",

            "financing_activity_cr"

        ]

    )

    net = cfo + cfi + cff

    pdf.setFont("Helvetica",10)

    pdf.drawString(x,y,f"CFO : {cfo:,.2f}")

    pdf.drawString(x,y-15,f"CFI : {cfi:,.2f}")

    pdf.drawString(x,y-30,f"CFF : {cff:,.2f}")

    pdf.drawString(x,y-45,f"Net Cash : {net:,.2f}")    
# ==========================================================
# MAIN
# ==========================================================

def main():

    print_header("Sprint 5 Day 33")

    connection = connect_database()

    companies = load_companies(connection)

    ratios = load_ratios(connection)

    pl = load_profit_loss(connection)

    bs = load_balance_sheet(connection)

    cf = load_cashflow(connection)

    pros = load_pros_cons()

    cashflow_intelligence_df = load_cashflow_intelligence()

    sectors = load_sectors(connection)

    print_header("Foundation Ready")

    print(f"Companies      : {len(companies)}")
    print(f"Ratios         : {len(ratios)}")
    print(f"P&L            : {len(pl)}")
    print(f"Balance Sheet  : {len(bs)}")
    print(f"Cash Flow      : {len(cf)}")
    print(f"Pros/Cons      : {len(pros)}")
    print(f"Cashflow KPI   : {len(cashflow_intelligence_df)}")

    print_header("Generating Test Tearsheets")

    generated = 0
    for company in TEST_COMPANIES:

        try:
            generate_tearsheet(

    company,
    companies,
    sectors,
    ratios,
    bs,
    cf,
    pl,
    cashflow_intelligence_df,
    pros

)

            print(f"✓ Generated : {company}.pdf")

            generated += 1

        except Exception as e:

            print(f"✗ Failed : {company}")

            print(e)

    connection.close()

    print_header("Day 33 Summary")
    print(f"Companies Loaded : {len(companies)}")
    print(f"Tearsheets Built : {generated}")
    print(f"Output Folder    : {OUTPUT_FOLDER}")

if __name__ == "__main__":

    main()