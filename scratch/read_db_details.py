import pandas as pd
import os

BASE_DIR = r"c:\Users\thout\Downloads\check it"

confirmed_path = os.path.join(BASE_DIR, "india_products_confirmed.csv")
needs_ver_path = os.path.join(BASE_DIR, "india_products_needs_verification.csv")

df_c = pd.read_csv(confirmed_path, dtype=str)
df_nv = pd.read_csv(needs_ver_path, dtype=str)

print("=== CONFIRMED SCHEMA AND VALUE RANGES ===")
print(df_c.info())
print("\nUnique statuses:", df_c['status'].unique())
print("Unique sources:", df_c['data_source'].unique())
print("Unique sold_in_india_status:", df_c['sold_in_india_status'].unique())
print("Unique ingredient_confidence:", df_c['ingredient_confidence'].unique())
print(df_c.head(2))

print("\n=== NEEDS VERIFICATION SCHEMA AND VALUE RANGES ===")
print(df_nv.info())
print("\nUnique statuses:", df_nv['status'].unique())
print("Unique sources:", df_nv['data_source'].unique())
print("Unique sold_in_india_status:", df_nv['sold_in_india_status'].unique())
print("Unique ingredient_confidence:", df_nv['ingredient_confidence'].unique())
print(df_nv.head(2))
