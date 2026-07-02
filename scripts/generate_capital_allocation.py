import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from src.analytics.cashflow_kpis import export_capital_allocation

rows = [
    [1, 2025, "+", "-", "-", "Reinvestor"],
    [2, 2025, "+", "+", "+", "Cash Accumulator"],
    [3, 2025, "-", "+", "+", "Distress Signal"]
]

export_capital_allocation(rows)

print("capital_allocation.csv created successfully!")