PRAGMA foreign_keys = ON;

-- =====================================================
-- COMPANIES
-- =====================================================

CREATE TABLE companies (
    id TEXT PRIMARY KEY,
    company_logo TEXT,
    company_name TEXT,
    chart_link TEXT,
    about_company TEXT,
    website TEXT,
    nse_profile TEXT,
    bse_profile TEXT,
    face_value REAL,
    book_value REAL,
    roce_percentage REAL,
    roe_percentage REAL
);

-- =====================================================
-- PROFIT AND LOSS
-- =====================================================

CREATE TABLE profitandloss (
    id INTEGER PRIMARY KEY,
    company_id TEXT,
    year INTEGER,
    sales REAL,
    expenses REAL,
    operating_profit REAL,
    opm_percentage REAL,
    other_income REAL,
    interest REAL,
    depreciation REAL,
    profit_before_tax REAL,
    tax_percentage REAL,
    net_profit REAL,
    eps REAL,
    dividend_payout REAL
);

-- =====================================================
-- BALANCE SHEET
-- =====================================================

CREATE TABLE balancesheet (
    id INTEGER PRIMARY KEY,
    company_id TEXT,
    year INTEGER,
    equity_capital REAL,
    reserves REAL,
    borrowings REAL,
    other_liabilities REAL,
    total_liabilities REAL,
    fixed_assets REAL,
    cwip REAL,
    investments REAL,
    other_asset REAL,
    total_assets REAL
);

-- =====================================================
-- CASHFLOW
-- =====================================================

CREATE TABLE cashflow (
    id INTEGER PRIMARY KEY,
    company_id TEXT,
    year INTEGER,
    operating_activity REAL,
    investing_activity REAL,
    financing_activity REAL,
    net_cash_flow REAL
);

-- =====================================================
-- ANALYSIS
-- =====================================================

CREATE TABLE analysis (
    id INTEGER,
    company_id TEXT,
    compounded_sales_growth TEXT,
    compounded_profit_growth TEXT,
    stock_price_cagr TEXT,
    roe TEXT
);

-- =====================================================
-- DOCUMENTS
-- =====================================================

CREATE TABLE documents (
    id INTEGER PRIMARY KEY,
    company_id TEXT,
    Year INTEGER,
    Annual_Report TEXT
);

-- =====================================================
-- FINANCIAL RATIOS
-- =====================================================

CREATE TABLE financial_ratios (
    id INTEGER PRIMARY KEY,
    company_id TEXT,
    year INTEGER,

    net_profit_margin_pct REAL,
    operating_profit_margin_pct REAL,
    return_on_equity_pct REAL,

    debt_to_equity REAL,
    interest_coverage REAL,
    asset_turnover REAL,

    free_cash_flow_cr REAL,
    capex_cr REAL,

    earnings_per_share REAL,
    book_value_per_share REAL,
    dividend_payout_ratio_pct REAL,

    total_debt_cr REAL,
    cash_from_operations_cr REAL,

    revenue_cagr_5yr REAL,
    pat_cagr_5yr REAL,
    eps_cagr_5yr REAL,

    composite_quality_score REAL,

    FOREIGN KEY(company_id)
        REFERENCES companies(id)
);

-- =====================================================
-- PEER GROUPS
-- =====================================================

CREATE TABLE peer_groups (
    id INTEGER PRIMARY KEY,
    peer_group_name TEXT,
    company_id TEXT,
    is_benchmark BOOLEAN
);

-- =====================================================
-- SECTORS
-- =====================================================

CREATE TABLE sectors (
    id INTEGER PRIMARY KEY,
    company_id TEXT,
    broad_sector TEXT,
    sub_sector TEXT,
    index_weight_pct REAL,
    market_cap_category TEXT
);

-- =====================================================
-- STOCK PRICES
-- =====================================================

CREATE TABLE stock_prices (
    id INTEGER PRIMARY KEY,
    company_id TEXT,
    date TEXT,
    open_price REAL,
    high_price REAL,
    low_price REAL,
    close_price REAL,
    volume INTEGER,
    adjusted_close REAL
);