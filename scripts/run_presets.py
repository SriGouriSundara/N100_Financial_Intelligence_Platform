"""
Sprint 3 - Day 16
Run all preset screeners.

"""

import subprocess
import sys
from pathlib import Path


def main():

    project_root = Path(__file__).resolve().parents[1]

    engine = project_root / "src" / "screener" / "engine.py"

    print("=" * 60)
    print("RUNNING ALL PRESET SCREENERS")
    print("=" * 60)

    result = subprocess.run(
        [sys.executable, str(engine)]
    )

    if result.returncode == 0:

        print("\nSUCCESS")
        print("All presets executed successfully.")

    else:

        print("\nFAILED")
        print("Engine returned an error.")


if __name__ == "__main__":
    main()