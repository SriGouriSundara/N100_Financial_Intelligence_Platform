"""
Sprint 3 - Day 18
Run Peer Ranking Engine
"""

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

peer_script = PROJECT_ROOT / "src" / "analytics" / "peer.py"

print("=" * 60)
print("RUNNING PEER RANKING ENGINE")
print("=" * 60)

result = subprocess.run(
    [sys.executable, str(peer_script)],
    cwd=PROJECT_ROOT
)

if result.returncode == 0:
    print("\nPeer Ranking Completed Successfully.")
else:
    print("\nPeer Ranking Failed.")