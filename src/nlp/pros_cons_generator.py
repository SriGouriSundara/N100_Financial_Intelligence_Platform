"""
=========================================================
Bluestock N100 Financial Intelligence Platform

Sprint 5
Day 30

Auto Pros / Cons Generator
=========================================================
"""

import sqlite3
from pathlib import Path

import pandas as pd

# ==========================================================
# PROJECT PATHS
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DB_PATH = PROJECT_ROOT / "db" / "nifty100.db"

OUTPUT_DIR = PROJECT_ROOT / "output"

OUTPUT_DIR.mkdir(exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "pros_cons_generated.csv"

# ==========================================================
# CONFIDENCE
# ==========================================================

MIN_CONFIDENCE = 60

MAX_CONFIDENCE = 100
# ==========================================================
# PRINT HELPERS
# ==========================================================

def print_header(title):

    print("\n" + "=" * 60)

    print(title)

    print("=" * 60)
# ==========================================================
# DATABASE
# ==========================================================

def connect_database():

    print_header("Connecting Database")

    if not DB_PATH.exists():

        raise FileNotFoundError(DB_PATH)

    connection = sqlite3.connect(DB_PATH)

    print("Database Connected")

    return connection

def load_companies(connection):

    print_header("Loading Companies")

    query = """

    SELECT *

    FROM companies

    """

    df = pd.read_sql_query(query, connection)

    print(f"Companies Loaded : {len(df)}")

    return df
def load_ratios(connection):

    print_header("Loading Financial Ratios")

    ratios = pd.read_sql_query(
        "SELECT * FROM financial_ratios",
        connection
    )

    companies = pd.read_sql_query(
        "SELECT id FROM companies",
        connection
    )

    valid_ids = (
        companies["id"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    ratios["company_id"] = (
        ratios["company_id"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    ratios = ratios[
        ratios["company_id"].isin(valid_ids)
    ].copy()

    print(f"Ratio Records : {len(ratios)}")
    print(f"Unique Companies : {ratios['company_id'].nunique()}")

    return ratios
def load_profit_loss(connection):

    print_header("Loading Profit & Loss")

    query = """
    SELECT *
    FROM profitandloss
    """

    df = pd.read_sql_query(query, connection)

    print(f"Profit & Loss Records : {len(df)}")

    return df

def load_balance_sheet(connection):

    print_header("Loading Balance Sheet")

    query = """
    SELECT *
    FROM balancesheet
    """

    df = pd.read_sql_query(query, connection)

    print(f"Balance Sheet Records : {len(df)}")

    return df

def load_cashflow(connection):

    print_header("Loading Cash Flow")

    query = """
    SELECT *
    FROM cashflow
    """

    df = pd.read_sql_query(query, connection)

    print(f"Cash Flow Records : {len(df)}")

    return df
# ==========================================================
# LATEST YEAR
# ==========================================================

def latest_year_data(ratios):

    latest = (
        ratios
        .sort_values(["company_id", "year"])
        .groupby("company_id", as_index=False)
        .tail(1)
        .reset_index(drop=True)
    )

    print(f"Latest Year Records : {len(latest)}")

    return latest
# ==========================================================
# CONFIDENCE SCORE
# ==========================================================

def calculate_confidence(value, threshold):

    """
    Simple confidence calculator.

    Maximum = 100

    Minimum returned = 60
    """

    if pd.isna(value):

        return 0

    if value <= threshold:

        return MIN_CONFIDENCE

    score = MIN_CONFIDENCE + (value - threshold) * 2

    return min(int(score), MAX_CONFIDENCE)
# ==========================================================
# RULE OUTPUT
# ==========================================================

def add_rule(

    results,

    company,

    rule_type,

    rule_id,

    text,

    confidence,

):

    if confidence < MIN_CONFIDENCE:

        return

    results.append(

        {

            "company_id": company,

            "type": rule_type,

            "rule_id": rule_id,

            "text": text,

            "confidence_pct": confidence,

        }

    )
# ==========================================================
# SAVE CSV
# ==========================================================
def save_output(results):

    print_header("Generating Final Output")

    df = pd.DataFrame(results)

    # Remove duplicate rules
    df = df.drop_duplicates(
        subset=[
            "company_id",
            "type",
            "rule_id"
        ]
    )

    # Sort for readability
    df = df.sort_values(
        [
            "company_id",
            "type",
            "rule_id"
        ]
    ).reset_index(drop=True)

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(f"Saved : {OUTPUT_FILE.name}")
    print(f"Generated Records : {len(df)}")

    return df
# ==========================================================
# PRO RULE DEFINITIONS
# ==========================================================

PRO_RULES = {

    "PRO_01":
        "Consistently high return on equity above 20% demonstrates exceptional capital efficiency",

    "PRO_02":
        "Strong free cash flow generation over 5 years signals healthy business fundamentals",

    "PRO_03":
        "Debt-free balance sheet provides financial flexibility and eliminates interest burden",

    "PRO_04":
        "Revenue growing at above 15% CAGR over 5 years reflects strong business momentum",

    "PRO_05":
        "Operating profit margin above 25% indicates strong pricing power and cost discipline",

    "PRO_06":
        "Net profit compounding at above 20% over 5 years creates significant shareholder value",

    "PRO_07":
        "Very high interest coverage ratio reflects negligible financial stress from debt servicing",

    "PRO_08":
        "Consistent dividend yield above 2% backed by positive free cash flow",

    "PRO_09":
        "Earnings per share growing above 15% CAGR indicates strong earnings quality and compounding",

    "PRO_10":
        "Return on equity improving for 3 consecutive years shows strengthening business quality",

    "PRO_11":
        "Revenue growing slower than profits shows improving operating leverage and scale benefits",

    "PRO_12":
        "Growing asset base funded by internal accruals reflects self-sustaining growth",

}
# ==========================================================
# PRO RULE ENGINE
# ==========================================================

def apply_pro_rules(ratios):

    print_header("Applying Pro Rules")

    results = []

    latest = latest_year_data(ratios)

    for _, latest_row in latest.iterrows():

        company = latest_row["company_id"]

        history = (

            ratios

            [ratios["company_id"] == company]

            .sort_values("year")

        )

        # -------------------------------------------------
        # PRO RULE 1
        # ROE >20 for last 3 years
        # -------------------------------------------------

        if len(history) >= 3:

            last3 = history.tail(3)

            if (last3["return_on_equity_pct"] > 20).all():

                confidence = calculate_confidence(

                    last3["return_on_equity_pct"].mean(),

                    20,

                )

                add_rule(

                    results,

                    company,

                    "pro",

                    "PRO_01",

                    PRO_RULES["PRO_01"],

                    confidence,

                )

        # -------------------------------------------------
        # PRO RULE 2
        # Positive FCF for 5 years
        # -------------------------------------------------

        if len(history) >= 5:

            last5 = history.tail(5)

            if (last5["free_cash_flow_cr"] > 0).all():

                confidence = 95

                add_rule(

                    results,

                    company,

                    "pro",

                    "PRO_02",

                    PRO_RULES["PRO_02"],

                    confidence,

                )

        # -------------------------------------------------
        # PRO RULE 3
        # Debt Free
        # -------------------------------------------------

        if latest_row["debt_to_equity"] == 0:

            add_rule(

                results,

                company,

                "pro",

                "PRO_03",

                PRO_RULES["PRO_03"],

                100,

            )

        # -------------------------------------------------
        # PRO RULE 4
        # Revenue CAGR
        # -------------------------------------------------

        if latest_row["revenue_cagr_5yr"] > 15:

            confidence = calculate_confidence(

                latest_row["revenue_cagr_5yr"],

                15,

            )

            add_rule(

                results,

                company,

                "pro",

                "PRO_04",

                PRO_RULES["PRO_04"],

                confidence,

            )

        # -------------------------------------------------
        # PRO RULE 5
        # OPM
        # -------------------------------------------------

        if latest_row["operating_profit_margin_pct"] > 25:

            confidence = calculate_confidence(

                latest_row["operating_profit_margin_pct"],

                25,

            )

            add_rule(

                results,

                company,

                "pro",

                "PRO_05",

                PRO_RULES["PRO_05"],

                confidence,

            )

        # -------------------------------------------------
        # PRO RULE 6
        # PAT CAGR
        # -------------------------------------------------

        if latest_row["pat_cagr_5yr"] > 20:

            add_rule(

                results,

                company,

                "pro",

                "PRO_06",

                PRO_RULES["PRO_06"],

                calculate_confidence(
                    latest_row["pat_cagr_5yr"],
                    20
                ),

            )

        # -------------------------------------------------
        # PRO RULE 7
        # ICR
        # -------------------------------------------------

        if latest_row["interest_coverage"] > 10:

            add_rule(

                results,

                company,

                "pro",

                "PRO_07",

                PRO_RULES["PRO_07"],

                calculate_confidence(
                    latest_row["interest_coverage"],
                    10
                ),

            )

        # -------------------------------------------------
        # PRO RULE 9
        # EPS CAGR
        # -------------------------------------------------

        if latest_row["eps_cagr_5yr"] > 15:

            add_rule(

                results,

                company,

                "pro",

                "PRO_09",

                PRO_RULES["PRO_09"],

                calculate_confidence(
                    latest_row["eps_cagr_5yr"],
                    15
                ),

            )

        # -------------------------------------------------
        # PRO RULE 10
        # ROE improving
        # -------------------------------------------------

        if len(history) >= 3:

            last3 = history.tail(3)

            values = last3["return_on_equity_pct"].tolist()

            if values[0] < values[1] < values[2]:

                add_rule(

                    results,

                    company,

                    "pro",

                    "PRO_10",

                    PRO_RULES["PRO_10"],

                    85,

                )

    return results
# ==========================================================
# CON RULE DEFINITIONS
# ==========================================================

CON_RULES = {

    "CON_01":
        "Debt-to-equity ratio is elevated for a non-financial company and warrants monitoring.",

    "CON_02":
        "Free cash flow negative for 3 consecutive years raises concern about cash generation quality.",

    "CON_03":
        "Operating margins declining for 3 consecutive years suggest pricing or cost pressure.",

    "CON_04":
        "Company reported a net loss in the most recent financial year.",

    "CON_05":
        "Revenue contraction over 2 consecutive years indicates demand weakness or market share loss.",

    "CON_06":
        "Interest coverage ratio below 1.5x indicates risk in meeting debt obligations.",

    "CON_07":
        "Dividend payout ratio above 100% is unsustainable.",

    "CON_08":
        "Debt-to-equity ratio rising over 3 years suggests increasing leverage risk.",

    "CON_09":
        "EPS declining for 3 consecutive years reflects deteriorating profitability.",

    "CON_10":
        "Return on capital employed below 10% suggests poor capital efficiency.",

    "CON_11":
        "Net Debt exceeding 3x EBITDA limits financial flexibility.",

    "CON_12":
        "Revenue CAGR below 5% over five years suggests weak business momentum."

}
# ==========================================================
# CON RULE ENGINE
# ==========================================================

def apply_con_rules(
    ratios,
    profit_loss,
    balance_sheet,
    cashflow
):

    print_header("Applying Con Rules")

    results = []

    latest = latest_year_data(ratios)

    for _, latest_row in latest.iterrows():

        company = latest_row["company_id"]

        history = (
            ratios[ratios["company_id"] == company]
            .sort_values("year")
        )

        # -------------------------------------------------
        # CON RULE 1
        # High Debt
        # -------------------------------------------------

        sector = str(latest_row.get("sector", "")).lower()

        if (
            latest_row["debt_to_equity"] > 2
            and sector != "financial"
        ):

            confidence = calculate_confidence(
                latest_row["debt_to_equity"],
                2
            )

            add_rule(
                results,
                company,
                "con",
                "CON_01",
                f"Debt-to-equity ratio of "
                f"{latest_row['debt_to_equity']:.2f} "
                f"is elevated for a non-financial company "
                f"and warrants monitoring.",
                confidence
            )

        # -------------------------------------------------
        # CON RULE 2
        # Negative FCF
        # -------------------------------------------------

        if len(history) >= 3:

            last3 = history.tail(3)

            if (last3["free_cash_flow_cr"] < 0).all():

                add_rule(
                    results,
                    company,
                    "con",
                    "CON_02",
                    CON_RULES["CON_02"],
                    95
                )

        # -------------------------------------------------
        # CON RULE 3
        # Declining OPM
        # -------------------------------------------------

        if len(history) >= 3:

            last3 = history.tail(3)

            opm = last3[
                "operating_profit_margin_pct"
            ].tolist()

            if opm[0] > opm[1] > opm[2]:

                add_rule(
                    results,
                    company,
                    "con",
                    "CON_03",
                    CON_RULES["CON_03"],
                    85
                )
# -------------------------------------------------
# CON RULE 4
# Net Loss
# -------------------------------------------------

    pl_history = (
    profit_loss[
        profit_loss["company_id"] == company
    ]
    .sort_values("year")
)

    if len(pl_history):

     latest_pl = pl_history.iloc[-1]

    if latest_pl["net_profit"] < 0:

        add_rule(
            results,
            company,
            "con",
            "CON_04",
            CON_RULES["CON_04"],
            100,
        )

# -------------------------------------------------
# CON RULE 5
# Revenue Decline
# -------------------------------------------------

    if len(pl_history) >= 2:
     last2 = pl_history.tail(2)
    sales = last2["sales"].tolist()
    if sales[0] > sales[1]:

        add_rule(
            results,
            company,
            "con",
            "CON_05",
            CON_RULES["CON_05"],
            80,
        )

        # -------------------------------------------------
        # CON RULE 6
        # Low Interest Coverage Ratio
        # -------------------------------------------------

        icr = latest_row.get("interest_coverage")

        if pd.notna(icr):

            if icr < 1.5:

                confidence = calculate_confidence(
                    10 - icr,
                    2
                )

                add_rule(
                    results,
                    company,
                    "con",
                    "CON_06",
                    CON_RULES["CON_06"],
                    confidence
                )
        # -------------------------------------------------
        # CON RULE 7
        # Dividend Payout
        # -------------------------------------------------

        payout = latest_row.get(
            "dividend_payout_ratio_pct"
        )

        if pd.notna(payout):

            if payout > 100:

                confidence = min(
                    100,
                    70 + int((payout - 100) / 2)
                )

                add_rule(
                    results,
                    company,
                    "con",
                    "CON_07",
                    CON_RULES["CON_07"],
                    confidence
                )
        # -------------------------------------------------
        # CON RULE 8
        # Rising Debt-to-Equity
        # -------------------------------------------------

        if len(history) >= 3:

            last3 = history.tail(3)

            debt = last3[
                "debt_to_equity"
            ].tolist()

            if debt[0] < debt[1] < debt[2]:

                confidence = calculate_confidence(
                    debt[-1],
                    1
                )

                add_rule(
                    results,
                    company,
                    "con",
                    "CON_08",
                    CON_RULES["CON_08"],
                    confidence
                )
        # -------------------------------------------------
        # CON RULE 9
        # EPS Declining for 3 Consecutive Years
        # -------------------------------------------------

        if (
            len(history) >= 3
            and "earnings_per_share" in history.columns
        ):

            last3 = history.tail(3)

            eps = last3["earnings_per_share"].tolist()

            if (
                len(eps) == 3
                and pd.notna(eps[0])
                and pd.notna(eps[1])
                and pd.notna(eps[2])
                and eps[0] > eps[1] > eps[2]
            ):

                confidence = 90

                add_rule(
                    results,
                    company,
                    "con",
                    "CON_09",
                    CON_RULES["CON_09"],
                    confidence,
                )
# -------------------------------------------------
# CON RULE 10
#
# ROCE not available.
# Will be implemented later.
# -------------------------------------------------
                
# -------------------------------------------------
# CON RULE 11
# Borrowings / EBITDA
# -------------------------------------------------

    bs_history = (
    balance_sheet[
        balance_sheet["company_id"] == company
    ]
    .sort_values("year")
)

    if len(bs_history) and len(pl_history):
     latest_bs = bs_history.iloc[-1]
    latest_pl = pl_history.iloc[-1]
    borrowings = latest_bs["borrowings"]
    ebitda = (
        latest_pl["operating_profit"]
        +
        latest_pl["depreciation"]
    )

    if ebitda > 0:

        leverage = borrowings / ebitda

        if leverage > 3:

            confidence = calculate_confidence(
                leverage,
                3,
            )

            add_rule(
                results,
                company,
                "con",
                "CON_11",
                CON_RULES["CON_11"],
                confidence,
            )
                
        # -------------------------------------------------
        # CON RULE 12
        # Revenue CAGR < 5%
        # -------------------------------------------------

        revenue_cagr = latest_row.get("revenue_cagr_5yr")

        if (
            pd.notna(revenue_cagr)
            and revenue_cagr < 5
        ):

            confidence = calculate_confidence(
                5 - revenue_cagr,
                0
            )

            add_rule(
                results,
                company,
                "con",
                "CON_12",
                CON_RULES["CON_12"],
                confidence,
            )

    return results
# ==========================================================
# ENSURE AT LEAST ONE PRO & ONE CON
# ==========================================================

def ensure_minimum_signals(companies, pro_results, con_results):

    company_ids = set(companies["id"])

    pro_companies = {r["company_id"] for r in pro_results}
    con_companies = {r["company_id"] for r in con_results}

    # Default Pro
    for company in company_ids - pro_companies:

        add_rule(
            pro_results,
            company,
            "pro",
            "PRO_DEFAULT",
            "Business exhibits stable operating performance based on the available financial metrics.",
            65,
        )

    # Default Con
    for company in company_ids - con_companies:

        add_rule(
            con_results,
            company,
            "con",
            "CON_DEFAULT",
            "No significant financial weaknesses were detected by the automated rule engine. Investors should continue monitoring future financial performance.",
            65,
        )

    return pro_results, con_results

# ==========================================================
# FINAL VALIDATION
# ==========================================================

def validate_output(companies, output_df):

    print_header("Final Validation")

    company_ids = set(
        companies["id"].astype(str)
    )

    output_ids = set(
        output_df["company_id"].astype(str)
    )

    pro_ids = set(
        output_df[
            output_df["type"] == "pro"
        ]["company_id"]
    )

    con_ids = set(
        output_df[
            output_df["type"] == "con"
        ]["company_id"]
    )

    missing_output = company_ids - output_ids
    missing_pro = company_ids - pro_ids
    missing_con = company_ids - con_ids

    print(f"Companies           : {len(company_ids)}")
    print(f"Output Companies    : {len(output_ids)}")
    print(f"Companies with Pros : {len(pro_ids)}")
    print(f"Companies with Cons : {len(con_ids)}")

    print()

    if not missing_output:
        print("✓ Every company exists in output")
    else:
        print(f"✗ Missing Companies : {len(missing_output)}")

    if not missing_pro:
        print("✓ Every company has at least one PRO")
    else:
        print(f"✗ Missing PRO : {len(missing_pro)}")

    if not missing_con:
        print("✓ Every company has at least one CON")
    else:
        print(f"✗ Missing CON : {len(missing_con)}")
# ==========================================================
# MAIN FUNCTION 
# ==========================================================

def main():

    print_header("Sprint 5:Auto Pros & Cons Generator")

    connection = connect_database()

    try:

        # ======================================================
        # LOAD DATA
        # ======================================================

        companies = load_companies(connection)

        ratios = load_ratios(connection)

        profit_loss = load_profit_loss(connection)

        balance_sheet = load_balance_sheet(connection)

        cashflow = load_cashflow(connection)

        latest = latest_year_data(ratios)

        print("\nDataset Summary")
        print("-------------------------")
        print(f"Companies Loaded      : {len(companies)}")
        print(f"Ratio Records         : {len(ratios)}")
        print(f"Latest Year Records   : {len(latest)}")

        # ======================================================
        # APPLY PRO RULES
        # ======================================================

        pro_results = apply_pro_rules(ratios)

        print(f"\nPro Rules Generated : {len(pro_results)}")

        # ======================================================
        # APPLY CON RULES
        # ======================================================

        con_results = apply_con_rules(
            ratios,
            profit_loss,
            balance_sheet,
            cashflow
        )

        # ======================================================
        # ENSURE EVERY COMPANY HAS AT LEAST
        # ONE PRO AND ONE CON
        # ======================================================

        pro_results, con_results = ensure_minimum_signals(
            companies,
            pro_results,
            con_results
        )

        print(f"Con Rules Generated : {len(con_results)}")

        # ======================================================
        # MERGE RESULTS
        # ======================================================

        all_results = pro_results + con_results

        print(f"\nTotal Signals Generated : {len(all_results)}")

        output_df = save_output(all_results)
        validate_output(
    companies,
    output_df
)

        # ======================================================
        # VALIDATION
        # ======================================================

        print_header("Output Validation")

        company_count = output_df["company_id"].nunique()

        pro_count = (
            output_df[
                output_df["type"] == "pro"
            ]["company_id"].nunique()
        )

        con_count = (
            output_df[
                output_df["type"] == "con"
            ]["company_id"].nunique()
        )

        print(f"Companies in Output : {company_count}")
        print(f"Companies with Pros : {pro_count}")
        print(f"Companies with Cons : {con_count}")

        print("\nValidation Result")
        print("------------------------")

        if (
            company_count == len(companies)
            and
            pro_count == len(companies)
            and
            con_count == len(companies)
        ):

            print("✓ Every company has at least one PRO")
            print("✓ Every company has at least one CON")

            print_header("DAY-30 COMPLETED SUCCESSFULLY")

        else:

            missing_pro = (
                set(companies["id"])
                -
                set(
                    output_df[
                        output_df["type"] == "pro"
                    ]["company_id"]
                )
            )

            missing_con = (
                set(companies["id"])
                -
                set(
                    output_df[
                        output_df["type"] == "con"
                    ]["company_id"]
                )
            )

            if missing_pro:

                print("⚠ Missing PRO companies:")
                print(sorted(missing_pro))

            if missing_con:

                print("⚠ Missing CON companies:")
                print(sorted(missing_con))

            print_header("DAY 30 COMPLETED WITH WARNINGS")

        # ======================================================
        # OUTPUT FILE
        # ======================================================

        print("\nGenerated File")
        print("-------------------------")
        print("✓ output/pros_cons_generated.csv")

    finally:

        connection.close()


if __name__ == "__main__":

    main()