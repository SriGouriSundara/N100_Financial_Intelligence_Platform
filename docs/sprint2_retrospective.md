
# Sprint 2 Retrospective

## What was built

- Financial ratio engine (14+ KPIs)
- CAGR engine with 6 edge cases
- Cashflow KPI engine
- Edge case logging system
- Financial_ratios table (1171 rows)

## Key Formula Decisions

- ROE uses (Net Profit / Equity + Reserves)
- ROCE uses EBIT / Capital Employed
- CAGR handles negative and zero base cases with flags
- Debt-to-equity returns 0 when borrowings = 0

## Edge Case Handling

- Data source mismatches logged separately
- Version differences identified using threshold rules
- Financial sector leverage treated separately

## Challenges

- Missing years in CAGR caused INSUFFICIENT flags
- High ROCE values in capital-light industries
- Data inconsistency between computed vs source ratios

## Outcome

- Fully working financial analytics engine
- 1171 row KPI dataset ready for BI dashboard
