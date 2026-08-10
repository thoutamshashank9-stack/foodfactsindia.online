import os
import sys
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"c:\Users\thout\Downloads\check it"

needs_ver_path = os.path.join(BASE_DIR, "india_products_needs_verification.csv")
df_nv = pd.read_csv(needs_ver_path, dtype=str)

incomplete_path = os.path.join(BASE_DIR, "incomplete_products_list.csv")
df_nv.to_csv(incomplete_path, index=False)
print(f"Exported {len(df_nv)} incomplete products to {incomplete_path}")
