# 📊 N100 Financial Intelligence Platform

A comprehensive financial analytics platform built using **Python, SQLite, Streamlit, Pandas, and Plotly** to analyze Nifty 100 companies. The platform provides financial ratio analysis, stock screening, peer comparison, trend visualization, capital allocation insights, and valuation analysis through an interactive dashboard.

---

# Project Overview

The N100 Financial Intelligence Platform is designed to transform raw financial statement data into meaningful investment insights.

The application processes historical financial data for **92 Nifty 100 companies**, computes key financial metrics, stores the processed data in SQLite, and presents interactive visualizations using Streamlit.

---

# Objectives

- Build a robust ETL pipeline for financial data
- Calculate 50+ financial KPIs
- Develop an interactive financial screener
- Compare companies within peer groups
- Visualize historical trends
- Analyze capital allocation patterns
- Perform valuation analysis
- Deliver a production-ready Streamlit dashboard

---

# Technology Stack

| Category             | Technology    |
| -------------------- | ------------- |
| Programming Language | Python 3.13   |
| Database             | SQLite        |
| Dashboard            | Streamlit     |
| Data Processing      | Pandas, NumPy |
| Visualization        | Plotly        |
| Excel Handling       | OpenPyXL      |
| Testing              | Pytest        |
| Version Control      | Git & GitHub  |

---

# Project Structure

```
N100_Financial_Intelligence_Platform
│
├── config/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── db/
│   ├── schema.sql
│   └── nifty100.db
│
├── output/
│   ├── valuation_summary.xlsx
│   ├── valuation_flags.csv
│   ├── screener_output.xlsx
│   ├── peer_comparison.xlsx
│   ├── capital_allocation.csv
│   └── qa_test_results.csv
│
├── pages/
│   ├── 01_home.py
│   ├── 02_profile.py
│   ├── 03_screener.py
│   ├── 04_peers.py
│   ├── 05_trends.py
│   ├── 06_sectors.py
│   ├── 07_capital.py
│   └── 08_reports.py
│
├── reports/
│
├── src/
│   ├── analytics/
│   ├── dashboard/
│   ├── etl/
│   └── screener/
│
├── tests/
│
├── requirements.txt
└── README.md
```

---

# Features

## ETL Pipeline

- Excel data ingestion
- Data normalization
- SQLite database creation
- Data quality validation
- Audit report generation

---

## Financial Ratio Engine

Computes more than 50 KPIs including:

- ROE
- ROCE
- ROA
- Net Profit Margin
- Operating Profit Margin
- Debt-to-Equity
- Interest Coverage
- Asset Turnover
- Revenue CAGR
- PAT CAGR
- EPS CAGR
- Free Cash Flow
- Capital Allocation Metrics

---

## Financial Screener

Supports dynamic filtering using:

- ROE
- Debt-to-Equity
- Revenue CAGR
- PAT CAGR
- Free Cash Flow
- OPM
- P/E
- P/B
- Dividend Yield
- Interest Coverage

Includes six predefined screening strategies:

- Quality Compounder
- Value Pick
- Growth Accelerator
- Dividend Champion
- Debt-Free Blue Chip
- Turnaround Watch

---

## Peer Comparison

- Peer group selection
- Radar chart comparison
- Percentile rankings
- KPI comparison table

---

## Trend Analysis

- Revenue trend
- Profit trend
- Financial ratio trends
- Multi-metric comparison
- YoY growth visualization

---

## Sector Analysis

- Sector bubble chart
- Revenue vs ROE visualization
- Market capitalization analysis
- Sector median KPIs

---

## Capital Allocation

Visualizes company allocation strategies using:

- Treemap
- Pattern summary
- Company grouping

---

## Annual Reports

Provides:

- Company search
- Annual report links
- Report availability status

---

## Valuation Module

Calculates:

- FCF Yield
- Sector Median P/E
- P/E vs Sector Median
- Valuation Flags

Outputs:

- Fair
- Discount
- Caution

---

# Dashboard Screens

The Streamlit dashboard contains eight interactive screens.

## 1. Home

Displays:

- Summary KPI cards
- Sector distribution
- Top companies
- Dashboard overview

---

## 2. Company Profile

Displays:

- Company details
- Financial KPIs
- Revenue history
- ROE / ROCE trends
- Pros & Cons

---

## 3. Financial Screener

Displays:

- Interactive filters
- Preset screeners
- Live filtering
- CSV export

---

## 4. Peer Comparison

Displays:

- Radar chart
- Peer KPI comparison
- Benchmark comparison

---

## 5. Trend Analysis

Displays:

- Historical trends
- Multiple KPI comparison
- YoY growth

---

## 6. Sector Analysis

Displays:

- Bubble chart
- Sector KPI analysis
- Sector medians

---

## 7. Capital Allocation

Displays:

- Capital allocation treemap
- Pattern summary
- Company distribution

---

## 8. Annual Reports

Displays:

- Annual report links
- PDF availability
- Report status

---

# Dashboard Screenshots

> Add screenshots after completing the project.

Example:

```
docs/screenshots/

home.png

profile.png

screener.png

peer.png

trend.png

sector.png

capital.png

reports.png
```

Then include:

```markdown
## Home

![Home](docs/screenshots/home.png)
```

Repeat for all screens.

---

# Installation

Clone the repository

```bash
git clone <repository-url>
```

Move into the project

```bash
cd N100_Financial_Intelligence_Platform
```

Create virtual environment

```bash
python -m venv venv
```

Activate virtual environment

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Running the Dashboard

Start the Streamlit application

```bash
streamlit run src/dashboard/app.py
```

The application will be available at:

```
http://localhost:8501
```

---

# Output Files

The project generates the following outputs:

| File                   | Description                         |
| ---------------------- | ----------------------------------- |
| valuation_summary.xlsx | Valuation metrics for all companies |
| valuation_flags.csv    | Discount & Caution companies        |
| screener_output.xlsx   | Screener results                    |
| peer_comparison.xlsx   | Peer comparison report              |
| capital_allocation.csv | Capital allocation patterns         |
| qa_test_results.csv    | QA testing results                  |

---

# Quality Assurance

The application includes:

- Unit testing
- Integration testing
- Missing value handling
- Partial data handling
- Dashboard performance testing
- CSV validation
- Streamlit page testing

---

# Sprint Summary

### Sprint 1

- ETL Pipeline
- SQLite Database
- Data Quality Rules

### Sprint 2

- Financial Ratio Engine
- CAGR Engine
- Capital Allocation
- KPI Testing

### Sprint 3

- Financial Screener
- Peer Comparison
- Composite Scoring

### Sprint 4

- Streamlit Dashboard
- Valuation Module
- QA Testing
- Documentation

---

# Performance

- Dashboard pages load in under **3 seconds**
- SQLite query caching implemented
- Interactive Plotly visualizations
- Streamlit caching for improved performance

---

# Future Enhancements

- Live NSE/BSE market data integration
- Portfolio tracking
- Watchlist functionality
- AI-based stock recommendations
- User authentication
- Cloud deployment

---

# Author

**Sri Gouri Sundara**

Bluestock Internship Project

N100 Financial Intelligence Platform

---

# Acknowledgements

This project was developed as part of the **Bluestock Internship Program** to demonstrate end-to-end financial analytics, data engineering, and dashboard development using Python and Streamlit.
