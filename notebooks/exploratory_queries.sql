
--(!) Select 5 random caompanies.
SELECT *
FROM companies
ORDER BY RANDOM()
LIMIT 5;

--(2) Check year coverage for each company.
-- Shows:
-- 1. First year available in the database
-- 2. Latest year available in the database
-- 3. Total number of yearly records for the company
-- Helps identify companies with limited financial history.
SELECT
company_id,
MIN(year) AS first_year,
MAX(year) AS last_year,
COUNT(*) AS records
FROM profitandloss
GROUP BY company_id
ORDER BY records;

--(3) Companies with <5 years.
SELECT
company_id,
COUNT(*) AS years_available
FROM profitandloss
GROUP BY company_id
HAVING COUNT(*) < 5;

--(4) Check Row Counts.
SELECT COUNT(*) FROM companies;
SELECT COUNT(*) FROM profitandloss;
SELECT COUNT(*) FROM balancesheet;
SELECT COUNT(*) FROM cashflow;
SELECT COUNT(*) FROM stock_prices;

--(5) Foreign Key Check.
PRAGMA foreign_key_check;