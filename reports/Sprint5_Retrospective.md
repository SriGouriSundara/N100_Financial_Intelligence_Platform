
### Sprint 5 Retrospective

**Sprint Goal:**

Successfully implemented the Reporting & Intelligence modules, including NLP-based Pros/Cons generation, Cash Flow Intelligence, Capital Allocation analysis, automated PDF Tearsheet generation, Sector Reports, and Portfolio Summary Report.

**Completed Work**

* ✅ Day 29 – Analysis Parser
* ✅ Day 30 – NLP Pros & Cons Generator
* ✅ Day 31 – Cash Flow Intelligence Module
* ✅ Day 32 – Capital Allocation Report
* ✅ Day 33 – Company Tearsheet Template (2-page PDF)
* ✅ Day 34 – Batch Tearsheet & Sector Report Generation
* ✅ Day 35 – Portfolio Summary PDF

**Key Deliverables Completed**

* `output/pros_cons_generated.csv`
* `output/cashflow_intelligence.xlsx`
* `output/distress_alerts.csv`
* `output/pattern_changes.csv`
* `output/capital_pattern_distribution.csv`
* `reports/tearsheets/` (company PDF reports)
* `reports/sector/` (sector reports)
* `reports/portfolio/portfolio_summary.pdf`

**Challenges Faced**

* Resolved ReportLab page layout and chart alignment issues.
* Fixed missing function arguments during tearsheet generation.
* Corrected `Path` to string conversion for PDF generation.
* Eliminated data duplication by filtering latest financial records.
* Fixed PDF text overflow using `Paragraph` and `WORDWRAP`.
* Validated capital allocation history and pattern transitions.

**What Went Well**

* Modular project structure.
* Reusable helper functions.
* Automated generation of all required reports.
* Clean integration with SQLite and ReportLab.
* All major Sprint 5 deliverables successfully generated.

**Improvements for Next Sprint**

* Reduce repeated database queries using caching.
* Optimize PDF generation speed.
* Improve chart styling and responsiveness.
* Add automated regression/unit tests for report generation.
* Enhance logging and exception handling.

---

## Demo to Team Lead

1. **Company Tearsheets**

* Open **TCS.pdf**
* Open **RELIANCE.pdf**
* Open **HDFCBANK.pdf**
* Show:
  *  KPI Tiles
  *  Revenue & Net Profit Charts
  *  ROE/ROCE Trend
  *  Balance Sheet Composition
  *  Cash Flow Waterfall
  *  Pros & Cons
  *  Capital Allocation Badge

1. **Cash Flow Intelligence**

* Open `output/cashflow_intelligence.xlsx`
* Demonstrate:
  *  CFO Quality Score
  *  CFO Quality Label
  *  CapEx Intensity
  *  Distress Flag
  *  Deleveraging Flag
  *  Capital Allocation Label

1. **Pros & Cons Generator**

* Open `output/pros_cons_generated.csv`
* Show:
  *  Company ID
  *  Rule ID
  *  Generated Insight
  *  Confidence Score
  *  Pro/Con Classification

1. **Batch Reports**

* Show `reports/tearsheets/`
* Show `reports/sector/`
* Show `reports/portfolio/portfolio_summary.pdf`

1. **Validation**

* Confirm all expected output files were generated.
* Highlight successful end-to-end report generation workflow.

---

### Sprint 5 Status

| Item                       | Status       |
| -------------------------- | ------------ |
| NLP Pros & Cons            | ✅ Completed |
| Cash Flow Intelligence     | ✅ Completed |
| Capital Allocation Report  | ✅ Completed |
| Company Tearsheets         | ✅ Completed |
| Batch Tearsheet Generation | ✅ Completed |
| Sector Reports             | ✅ Completed |
| Portfolio Summary PDF      | ✅ Completed |
| Sprint Review              | ✅ Completed |
| Team Lead Demo             | ✅ Ready     |

Sprint 5 is complete and ready for sign-off, with all core reporting modules, intelligence outputs, and PDF reports implemented and prepared for demonstration.
