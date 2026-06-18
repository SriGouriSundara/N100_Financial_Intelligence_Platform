PRAGMA foreign_keys = ON;

-- COMPANIES

CREATE TABLE IF NOT EXISTS companies (
    company_id TEXT PRIMARY KEY,
    company_name TEXT NOT NULL,
    sector TEXT,
    industry TEXT,
    market_cap REAL
);

-- PROFIT AND LOSS

CREATE TABLE IF NOT EXISTS profitandloss (
    company_id TEXT,
    year INTEGER,
    sales REAL,
    operating_profit REAL,
    net_profit REAL,

    PRIMARY KEY (company_id, year),

    FOREIGN KEY (company_id)
    REFERENCES companies(company_id)
);

-- BALANCE SHEET

CREATE TABLE IF NOT EXISTS balancesheet (
    company_id TEXT,
    year INTEGER,
    total_assets REAL,
    total_liabilities REAL,
    equity REAL,

    PRIMARY KEY (company_id, year),

    FOREIGN KEY (company_id)
    REFERENCES companies(company_id)
);

-- CASHFLOW

CREATE TABLE IF NOT EXISTS cashflow (
    company_id TEXT,
    year INTEGER,
    operating_cashflow REAL,
    investing_cashflow REAL,
    financing_cashflow REAL,

    PRIMARY KEY (company_id, year),

    FOREIGN KEY (company_id)
    REFERENCES companies(company_id)
);

-- ANALYSIS

CREATE TABLE IF NOT EXISTS analysis (
    analysis_id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id TEXT,
    analysis_text TEXT,

    FOREIGN KEY (company_id)
    REFERENCES companies(company_id)
);

-- DOCUMENTS

CREATE TABLE IF NOT EXISTS documents (
    document_id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id TEXT,
    document_type TEXT,
    document_url TEXT,

    FOREIGN KEY (company_id)
    REFERENCES companies(company_id)
);

-- PROS AND CONS

CREATE TABLE IF NOT EXISTS prosandcons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id TEXT,
    type TEXT,
    description TEXT,

    FOREIGN KEY (company_id)
    REFERENCES companies(company_id)
);

-- SECTORS

CREATE TABLE IF NOT EXISTS sectors (
    sector_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sector_name TEXT UNIQUE
);

-- STOCK PRICES

CREATE TABLE IF NOT EXISTS stock_prices (
    company_id TEXT,
    trade_date TEXT,
    open_price REAL,
    high_price REAL,
    low_price REAL,
    close_price REAL,
    volume INTEGER,

    PRIMARY KEY (company_id, trade_date),

    FOREIGN KEY (company_id)
    REFERENCES companies(company_id)
);

-- FINANCIAL RATIOS

CREATE TABLE IF NOT EXISTS financial_ratios (
    company_id TEXT,
    year INTEGER,
    roe REAL,
    roce REAL,
    opm REAL,

    PRIMARY KEY (company_id, year),

    FOREIGN KEY (company_id)
    REFERENCES companies(company_id)
);

-- PEER GROUPS

CREATE TABLE IF NOT EXISTS peer_groups (
    peer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id TEXT,
    peer_company TEXT,

    FOREIGN KEY (company_id)
    REFERENCES companies(company_id)
);