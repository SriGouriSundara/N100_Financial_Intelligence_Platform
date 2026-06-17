# N100 Financial Intelligence Platform

## Overview

The N100 Financial Intelligence Platform is a data engineering and analytics project that builds a validated financial dataset for Nifty 100 companies.

The project focuses on:

* Data ingestion from Excel sources
* Data normalization and standardization
* Data Quality (DQ) validation framework
* Financial data integrity checks
* ETL pipeline development
* Future analytics and dashboarding

---

# Project Structure

```text
N100_Financial_Intelligence_Platform/

├── data/
│   ├── raw/
│   └── processed/
│
├── output/
│   └── validation_failures.csv
│
├── src/
│   └── etl/
│       ├── loader.py
│       ├── normaliser.py
│       ├── validator.py
│       └── run_validation.py
│
├── tests/
│   └── etl/
│       ├── test_loader.py
│       ├── test_normaliser.py
│       └── test_validator.py
│
├── requirements.txt
├── pytest.ini
└── README.md
```

---

# Day 01 – Environment Setup

## Objectives

* Create project repository
* Configure Python virtual environment
* Install dependencies
* Establish project structure

## Completed

* Python Virtual Environment
* Git Repository Setup
* GitHub Integration
* Pandas Installation
* Pytest Installation
* Project Folder Structure

## Deliverables

* Working development environment
* Version-controlled repository
* Dependency management

---

# Day 02 – Excel Loader & Normaliser

## Objectives

Build reusable ETL utilities for loading and standardizing raw datasets.

## Implemented

### Excel Loader

File:

```python
src/etl/loader.py
```

Features:

* Load Excel files
* Handle malformed headers
* Clean column names
* Standardize schemas

### Normaliser

File:

```python
src/etl/normaliser.py
```

Functions:

* normalize_ticker()
* normalize_year()

Examples:

```text
tcs → TCS
wipro → WIPRO

Mar 2024 → 2024
Dec 2023 → 2023
```

### Supported Datasets

* companies.xlsx
* profitandloss.xlsx
* balancesheet.xlsx
* financial_ratios.xlsx
* stock_prices.xlsx

---

## Unit Testing

Implemented comprehensive tests for:

### Loader Tests

* File loading
* Header cleaning
* Column validation
* DataFrame generation

### Normaliser Tests

* Ticker normalization
* Year normalization
* Edge cases
* Invalid values

Result:

```text
All tests passed
```

---

# Day 03 – Schema Validator

## Objectives

Implement a Data Quality framework to validate dataset integrity.

---

## Data Quality Rules

### Critical Rules

#### DQ-01

Primary Key Uniqueness

```text
companies.id must be unique
```

Severity:

```text
CRITICAL
```

---

#### DQ-02

Composite Key Validation

```text
(company_id, year) must be unique
```

Severity:

```text
CRITICAL
```

---

#### DQ-03

Foreign Key Integrity

```text
child.company_id
must exist in
companies.id
```

Severity:

```text
CRITICAL
```

---

### Warning Rules

#### DQ-04

Balance Sheet Check

```text
Assets ≈ Liabilities + Equity
Tolerance: 1%
```

---

#### DQ-05

Operating Margin Cross Check

```text
OPM =
Operating Profit / Sales
```

---

#### DQ-06

Positive Sales Validation

```text
Sales > 0
```

---

#### DQ-07

Company ID Not Null

---

#### DQ-08

Year Not Null

---

#### DQ-09

Sales Not Null

---

#### DQ-10

Year Range Validation

```text
2000 <= Year <= 2026
```

---

#### DQ-11

Duplicate Company Names

---

#### DQ-12

Debt Validation

```text
Debt >= 0
```

---

#### DQ-13

Stock Price Validation

```text
Close Price > 0
```

---

#### DQ-14

Ratio Range Validation

```text
-100 <= Ratio <= 1000
```

---

#### DQ-15

Website Exists

---

#### DQ-16

NSE Profile Exists

---

# Validation Framework

File:

```python
src/etl/run_validation.py
```

Responsibilities:

* Load datasets
* Execute DQ rules
* Aggregate failures
* Generate validation report

Output:

```text
output/validation_failures.csv
```

---

# Validation Results

## Real Dataset Scan

Completed on full N100 dataset.

Results:

```text
Total Failures: 1571
```

Severity Breakdown:

```text
WARNING: 1571
CRITICAL: 0
```

---

## Critical Validation Status

### DQ-01

```text
PASS
```

### DQ-02

```text
PASS
```

### DQ-03

```text
PASS
```

Result:

```text
CRITICAL Failures = 0
```

---

# Testing

Executed using:

```bash
pytest tests -v
```

Result:

```text
53 Passed
0 Failed
```

Coverage includes:

* Loader
* Normaliser
* Validator

---

# Technologies Used

* Python 3.13
* Pandas
* Pytest
* Git
* GitHub

---

# Current Project Status

## Day 01

Completed

## Day 02

Completed

## Day 03

Completed

---

# Next Phase

Day 04 – Database Layer

Planned activities:

* PostgreSQL schema creation
* Table definitions
* Data loading pipeline
* Database integration
* Data persistence layer

---

## Author

Sri Gouri Sundara

N100 Financial Intelligence Platform
Bluestock Internship Project
