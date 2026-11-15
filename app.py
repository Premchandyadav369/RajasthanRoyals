"""
Streamlit Community Cloud Root Entry Point for Project RR-EDGE
Bespoke War Room Platform for Rajasthan Royals (SupeRR Selector Season 2)
"""

import os
import sys

# Ensure repository root is on sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

dashboard_dir = os.path.join(BASE_DIR, "RR_EDGE_Dashboard")
if dashboard_dir not in sys.path:
    sys.path.insert(0, dashboard_dir)

# Execute main dashboard app
app_path = os.path.join(dashboard_dir, "app.py")
with open(app_path, "r", encoding="utf-8") as f:
    code = f.read()

exec(code, globals())
