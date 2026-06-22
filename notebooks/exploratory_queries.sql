
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

--(6) Total Companies.
SELECT COUNT(*) AS total_companies
FROM companies;

--(7) Top 10 Companies by ROE.
SELECT
company_name,
roe_percentage
FROM companies
ORDER BY roe_percentage DESC
LIMIT 10;

--(8) Highest Sales.
SELECT
company_id,
year,
sales
FROM profitandloss
ORDER BY sales DESC
LIMIT 10;

--(9) Highest Net Profit.
SELECT
company_id,
year,
net_profit
FROM profitandloss
ORDER BY net_profit DESC
LIMIT 10;

--(10) Average Sales By Company.
SELECT
company_id,
AVG(sales) AS avg_sales
FROM profitandloss
GROUP BY company_id
ORDER BY avg_sales DESC;

--(11) Highest Stock Price.
SELECT
company_id,
date,
close_price
FROM stock_prices
ORDER BY close_price DESC
LIMIT 10;

--(12) Sector Distribution.
SELECT
broad_sector,
COUNT(*) AS company_count
FROM sectors
GROUP BY broad_sector
ORDER BY company_count DESC;