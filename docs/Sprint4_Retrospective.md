
# Sprint 4 Retrospective

## Dashboard & Valuation Module

**Sprint Duration:** Day 22 – Day 28

**Project:** N100 Financial Intelligence Platform

**Sprint Goal:**
Develop a complete Streamlit dashboard for financial analysis, implement the valuation engine, perform integration testing, and prepare the application for demonstration.

---

# Sprint Objective

The objective of Sprint 4 was to deliver a fully functional analytics dashboard capable of visualizing financial data for Nifty 100 companies, providing interactive screening, peer comparison, trend analysis, sector insights, capital allocation visualization, annual report access, and valuation analysis.

---

# Completed Features

## Dashboard

Implemented all eight Streamlit dashboard screens.

| Screen             | Status       |
| ------------------ | ------------ |
| Home Dashboard     | ✅ Completed |
| Company Profile    | ✅ Completed |
| Financial Screener | ✅ Completed |
| Peer Comparison    | ✅ Completed |
| Trend Analysis     | ✅ Completed |
| Sector Analysis    | ✅ Completed |
| Capital Allocation | ✅ Completed |
| Annual Reports     | ✅ Completed |

---

# Valuation Module

Implemented the complete valuation engine.

Features include:

- FCF Yield Calculation
- Sector Median P/E Calculation
- P/E Premium/Discount Analysis
- Valuation Flag Generation
- Excel Output
- CSV Output

Generated files:

- output/valuation_summary.xlsx
- output/valuation_flags.csv

---

# UX Decisions

Several usability improvements were introduced during dashboard development.

## Home Dashboard

- KPI cards placed at the top for quick visibility.
- Year selector available in the sidebar.
- Donut chart selected for sector distribution because it provides better readability.
- Top-performing companies displayed below KPI section.

---

## Company Profile

- Search box supports partial company names.
- Friendly "Ticker Not Found" message implemented.
- KPI cards grouped together.
- Revenue and Net Profit displayed using bar charts.
- ROE and ROCE displayed as trend lines.
- Pros and Cons section shown using visual badges.

---

## Financial Screener

Implemented:

- Live slider filtering
- Preset filters
- Dynamic result count
- CSV export

This minimizes user interaction while allowing rapid financial screening.

---

## Peer Comparison

Implemented:

- Peer group selector
- Company selector
- Radar chart
- Peer average overlay
- KPI comparison table

Radar chart provides an intuitive comparison between companies and peer averages.

---

## Trend Analysis

Implemented:

- Multi-metric comparison
- Interactive Plotly charts
- YoY annotations
- Missing data handling

Users can compare multiple metrics over time without switching charts.

---

## Sector Analysis

Implemented:

- Bubble chart
- Sector KPI bar chart
- Revenue vs ROE visualization
- Bubble size based on Market Capitalization

This allows users to quickly identify sector leaders.

---

## Capital Allocation

Implemented:

- Interactive treemap
- Eight allocation patterns
- Company drill-down
- Pattern summary

Treemap selected because it effectively visualizes hierarchical data.

---

## Annual Reports

Implemented:

- Company search
- Available report years
- PDF links
- Missing report detection

Unavailable reports are displayed using a red status badge.

---

# Data Edge Cases Identified

Several data-quality scenarios were encountered.

## Missing KPI Values

Issue:

Some companies contain NULL values for financial metrics.

Resolution:

Implemented helper function:

- safe_value()

Missing values are displayed as:

N/A

instead of causing dashboard failures.

---

## Partial Historical Data

Issue:

Some companies contain fewer than 10 years of financial history.

Resolution:

Dashboard now displays:

"Limited data available."

Charts automatically adjust to available years.

---

## Empty Filter Results

Issue:

Extreme screener filters may return zero companies.

Resolution:

Dashboard displays a friendly message instead of an empty or broken table.

---

## Missing Annual Reports

Issue:

Not every company has report URLs available.

Resolution:

Unavailable reports display:

🔴 Report Unavailable

instead of broken hyperlinks.

---

# Performance Improvements

Several optimizations were introduced.

## Cached Database Queries

Used:

- @st.cache_data

Benefits:

- Faster dashboard loading
- Reduced SQLite reads
- Better responsiveness

---

## Optimized SQL Queries

Database joins were simplified.

Only required columns are selected.

Redundant queries removed.

---

## Plot Optimization

Large Plotly figures now use:

- use_container_width=True

Charts automatically resize to screen width.

---

## Lazy Loading

Company-specific queries execute only after a company is selected.

This significantly reduces unnecessary database access.

---

# QA Results

Integration testing completed successfully.

### Dashboard Testing

| Screen             | Status  |
| ------------------ | ------- |
| Home               | ✅ Pass |
| Company Profile    | ✅ Pass |
| Screener           | ✅ Pass |
| Peer Comparison    | ✅ Pass |
| Trend Analysis     | ✅ Pass |
| Sector Analysis    | ✅ Pass |
| Capital Allocation | ✅ Pass |
| Annual Reports     | ✅ Pass |

---

### Performance Testing

Company Profile load time tested for five companies.

| Company   | Load Time |
| --------- | --------- |
| TCS       | < 2 sec   |
| INFY      | < 2 sec   |
| HDFCBANK  | < 2 sec   |
| RELIANCE  | < 3 sec   |
| SUNPHARMA | < 2 sec   |

Requirement:

Load time under 3 seconds.

Status:

✅ Passed

---

### Edge Case Testing

| Test            | Result  |
| --------------- | ------- |
| Missing KPI     | ✅ Pass |
| Partial History | ✅ Pass |
| Empty Screener  | ✅ Pass |
| Invalid Company | ✅ Pass |
| Missing Reports | ✅ Pass |

---

# Lessons Learned

During Sprint 4 several important insights were gained.

- Dashboard responsiveness improves significantly with cached queries.
- Plotly provides better interactivity than static charts.
- Proper handling of NULL values is essential for production dashboards.
- Modular database helper functions improve code maintainability.
- Separating UI and database logic simplifies debugging and testing.

---

# Future Improvements

Potential enhancements include:

- Live NSE/BSE market price integration.
- User authentication and role-based access.
- Watchlist and favourites functionality.
- Portfolio analytics.
- PDF report generation.
- AI-powered company insights.
- Advanced valuation models (DCF, Residual Income, EVA).
- Mobile-responsive dashboard improvements.

---

# Sprint Outcome

Sprint 4 objectives were successfully achieved.

### Deliverables Completed

- Streamlit Dashboard
- Home Screen
- Company Profile
- Screener
- Peer Comparison
- Trend Analysis
- Sector Analysis
- Capital Allocation
- Annual Reports
- Valuation Module
- QA Testing
- Documentation

---

# Overall Sprint Status

| Item                    | Status       |
| ----------------------- | ------------ |
| Functional Requirements | ✅ Completed |
| Dashboard Screens       | ✅ Completed |
| Valuation Module        | ✅ Completed |
| QA Testing              | ✅ Completed |
| Performance Validation  | ✅ Completed |
| Documentation           | ✅ Completed |
| Sprint Review Ready     | ✅ Completed |

---

# Final Sprint Assessment

**Sprint Status:** ✅ Successfully Completed

The N100 Financial Intelligence Platform dashboard is fully functional, stable, tested, and documented. All planned Sprint 4 objectives have been completed, including dashboard implementation, valuation analytics, quality assurance, and project documentation. The application is ready for sprint review, demonstration, and transition to the next development phase.
