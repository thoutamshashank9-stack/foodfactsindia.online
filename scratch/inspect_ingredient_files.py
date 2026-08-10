import os
import sys
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"c:\Users\thout\Downloads\check it"

files = [
    "products_with_complete_ingredients.csv",
    "products_without_complete_ingredients.csv",
    "products_with_ingredients.csv",
    "products_without_ingredients.csv"
]

for f_name in files:
    path = os.path.join(BASE_DIR, f_name)
    if os.path.exists(path):
        try:
            df = pd.read_csv(path, nrows=2, dtype=str)
            print(f"File: {f_name} | Columns: {df.columns.tolist()}")
        except Exception as e:
            print(f"Error reading {f_name}: {e}")
    else:
        print(f"File not found: {f_name}")
