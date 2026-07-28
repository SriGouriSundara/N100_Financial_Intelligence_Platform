---

# N100 Financial Intelligence Platform

## Project Overview

The **N100 Financial Intelligence Platform** is an end-to-end financial analytics system built to analyze, screen, compare, and evaluate Nifty 100 companies using automated ETL pipelines, financial KPI calculations, machine learning analytics, REST APIs, and an interactive Streamlit dashboard.

The platform transforms raw financial data into actionable investment insights through:

* Automated data ingestion and validation
* Financial ratio and KPI computation
* Company screening engine
* Peer comparison analytics
* Cluster-based company profiling
* Valuation analysis
* REST API services
* Interactive analyst dashboard
* Automated testing and documentation

---

# Key Features

## 1. Data Engineering & ETL Pipeline

The ETL pipeline processes financial datasets from Excel sources and loads validated data into SQLite.

Capabilities:

* Excel data ingestion
* Data normalization
* Schema validation
* Data quality checks
* Error reporting
* Audit logging

Processed datasets include:

* Company master data
* Profit & Loss statements
* Balance Sheet data
* Cash Flow statements
* Financial ratios
* Stock prices
* Sector information
* Peer groups

---

## 2. Data Quality Framework

The platform includes automated data quality validation using 14+ DQ rules.

Validation areas:

* Primary key uniqueness
* Mandatory field validation
* Data type checks
* Duplicate detection
* Referential integrity
* Financial data consistency

Outputs:

```
output/
 └── validation_failures.csv
```

---

# 3. Financial KPI Engine

The analytics engine calculates financial metrics across companies.

Supported KPIs include:

## Profitability Metrics

* Return on Equity (ROE)
* Return on Capital Employed (ROCE)
* Net Profit Margin
* Operating Profit Margin

## Growth Metrics

* Revenue CAGR
* PAT CAGR
* EPS CAGR

## Leverage Metrics

* Debt-to-Equity Ratio
* Interest Coverage Ratio

## Cash Flow Metrics

* Free Cash Flow
* CFO/PAT Quality
* Capital Allocation Metrics

---

# 4. Company Screener Engine

The screener allows analysts to identify companies based on financial conditions.

Available screening presets:

* Quality Compounder
* Value Pick
* Growth Accelerator
* Dividend Champion
* Debt-Free Blue Chip
* Turnaround Watch

Supported filters:

* ROE
* Debt-to-Equity
* Free Cash Flow
* Revenue CAGR
* PAT CAGR
* Sector
* Valuation metrics

---

# 5. Peer Comparison Engine

The platform compares companies against their peer groups.

Features:

* Peer group classification
* Percentile ranking
* Relative KPI comparison
* Radar comparison charts

Metrics compared:

* ROE
* ROCE
* Margins
* Growth
* Leverage
* Cash flow quality

---

# 6. Machine Learning Analytics

The platform performs company clustering using KMeans.

Clustering features:

* ROE
* Debt-to-Equity
* Revenue Growth
* Free Cash Flow Growth
* Operating Margin

Outputs:

```
output/
 └── cluster_labels.csv

reports/
 └── elbow_plot.png
```

Example cluster profiles:

* High Quality Compounders
* Defensive Dividend Companies
* Value Cyclicals
* Turnaround Candidates
* Emerging Growth Companies

---

# 7. FastAPI Backend

The platform provides REST API access through FastAPI.

API Base URL:

```
http://localhost:8000/api/v1
```

API documentation:

```
http://localhost:8000/docs
```

Available API modules:

* Company information
* Screener results
* Sector analytics
* Peer comparison
* Valuation data
* Portfolio statistics
* Documents
* Health monitoring

---

# 8. Streamlit Dashboard

Interactive dashboard for financial analysts.

Run:

```
streamlit run src/dashboard/app.py
```

Dashboard screens:

## 1. Home Dashboard

Provides:

* Market overview
* Sector distribution
* Portfolio statistics

## 2. Company Profile

Displays:

* Company information
* Financial KPIs
* Historical performance

## 3. Screener

Allows users to:

* Apply financial filters
* Select preset strategies
* Export results

## 4. Peer Comparison

Provides:

* Peer ranking
* Relative analysis
* Benchmark comparison

## 5. Financial Trends

Shows:

* Revenue trends
* Profit trends
* KPI movement

## 6. Sector Analysis

Provides:

* Sector comparison
* Median KPI analysis

## 7. Capital Allocation

Displays:

* Cash flow analysis
* Investment efficiency

## 8. Reports

Provides:

* PDF tearsheets
* Exportable analytics reports

---

# Project Structure

```
N100_Financial_Intelligence_Platform/

│
├── src/
│   ├── api/
│   ├── analytics/
│   ├── dashboard/
│   └── etl/
│
├── db/
│   └── nifty100.db
│
├── tests/
│   ├── api/
│   ├── etl/
│   ├── kpi/
│   └── dq/
│
├── output/
│   ├── cluster_labels.csv
│   ├── outlier_report.csv
│   └── portfolio_stats.csv
│
├── reports/
│   ├── elbow_plot.png
│   ├── correlation_heatmap.png
│   └── pytest_report.html
│
├── docs/
│   ├── openapi.json
│   └── analyst_guide.pdf
│
└── README.md
```

---

# Installation Setup

## Clone Repository

```
git clone <repository-url>

cd N100_Financial_Intelligence_Platform
```

---

## Create Virtual Environment

```
python -m venv venv
```

Activate:

Windows:

```
venv\Scripts\activate
```

---

## Install Dependencies

```
pip install -r requirements.txt
```

---

# Running the Application

## 1. Run ETL Pipeline

```
python src/etl/loader.py
```

This will:

* Load financial files
* Validate data
* Populate SQLite database

---

## 2. Run Analytics Modules

Example:

```
python src/analytics/clustering.py
```

Generates:

* Cluster labels
* Analytics reports

---

## 3. Start FastAPI Server

```
uvicorn src.api.main:app --port 8000
```

Open:

```
http://localhost:8000/docs
```

---

## 4. Start Streamlit Dashboard

```
streamlit run src/dashboard/app.py
```

Open:

```
http://localhost:8501
```

---

# Running Tests

Run complete test suite:

```
pytest tests/ -v
```

Generate HTML report:

```
pytest tests/ --html=reports/pytest_report.html --self-contained-html
```

Expected result:

```
60+ tests passed
0 failures
```

---

# API Examples

## Health Check

```
curl http://localhost:8000/api/v1/health
```

---

## Get Companies

```
curl http://localhost:8000/api/v1/companies
```

---

## Get Company Profile

```
curl http://localhost:8000/api/v1/companies/TCS
```

---

## Screener Query

```
curl "http://localhost:8000/api/v1/screener?min_roe=15"
```

---

# Generated Deliverables

The project generates:

```
output/
 ├── cluster_labels.csv
 ├── outlier_report.csv
 └── portfolio_stats.csv


reports/
 ├── elbow_plot.png
 ├── correlation_heatmap.png
 └── pytest_report.html


docs/
 ├── openapi.json
 └── analyst_guide.pdf
```

---

# Code Quality Standards

The project follows:

* PEP8 coding standards
* Black formatting
* Ruff lint validation
* Unit testing practices
* API documentation standards

Quality checks:

```
black src/ tests/

ruff check src/ tests/

pytest tests/
```

---

# Troubleshooting

## API Import Error

Problem:

```
ModuleNotFoundError: No module named src
```

Solution:

Run commands from project root directory.

---

## Database Table Missing

Problem:

```
no such table error
```

Solution:

Run ETL pipeline again:

```
python src/etl/loader.py
```

---

## Streamlit Dashboard Not Loading

Restart:

```
streamlit run src/dashboard/app.py
```

---

# Project Completion Status

| Module                  | Status    |
| ----------------------- | --------- |
| ETL Pipeline            | Completed |
| Data Quality Framework  | Completed |
| KPI Engine              | Completed |
| Screener Engine         | Completed |
| Peer Analytics          | Completed |
| ML Clustering           | Completed |
| FastAPI Backend         | Completed |
| Streamlit Dashboard     | Completed |
| API Integration Testing | Completed |
| Documentation           | Completed |

---

# License

Internal project use only.

# Author

**Sri Gouri Sundara**

Bluestock Internship Project

N100 Financial Intelligence Platform

---

# Acknowledgements

This project was developed as part of the **Bluestock Internship Program** to demonstrate end-to-end financial analytics, data engineering, and dashboard development using Python and Streamlit.
