"""
Streamlit Community Cloud Entry Point for Project RR-EDGE V6.0
Points directly to canonical unified war room platform (streamlit_app.py)
"""

import os
import sys
import runpy

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

canonical_app = os.path.join(BASE_DIR, "streamlit_app.py")
runpy.run_path(canonical_app, run_name="__main__")
