import sys
import os

print(f"Python Executable: {sys.executable}")
print(f"Python Version: {sys.version}")

try:
    import streamlit  # type: ignore
    print("[OK] streamlit")
except ImportError as e:
    print(f"[FAIL] streamlit ({e})")

try:
    import pandas  # type: ignore
    print("[OK] pandas")
except ImportError as e:
    print(f"[FAIL] pandas ({e})")

try:
    import plotly  # type: ignore
    print("[OK] plotly")
except ImportError as e:
    print(f"[FAIL] plotly ({e})")

try:
    import joblib  # type: ignore
    print("[OK] joblib")
except ImportError as e:
    print(f"[FAIL] joblib ({e})")

try:
    from data_processor import load_and_clean_data  # type: ignore
    print("[OK] data_processor")
except ImportError as e:
    print(f"[FAIL] data_processor ({e})")
