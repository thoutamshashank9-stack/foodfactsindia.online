import os
import sys
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"c:\Users\thout\Downloads\check it"

confirmed_path = os.path.join(BASE_DIR, "india_products_confirmed.csv")
needs_ver_path = os.path.join(BASE_DIR, "india_products_needs_verification.csv")
removed_path = os.path.join(BASE_DIR, "foreign_or_invalid_products_removed.csv")

# Helper lists
c_all = pd.read_csv(confirmed_path, dtype=str)
nv_all = pd.read_csv(needs_ver_path, dtype=str)
rem_all = pd.read_csv(removed_path, dtype=str)

# Calculate metrics
total_verified = len(c_all)
total_needs_verification = len(nv_all)
total_invalid_purged = len(rem_all)

total_with_ingredients = len(c_all[c_all['ingredients_text'].fillna('').str.strip() != ''])
total_without_ingredients = len(nv_all[nv_all['ingredients_text'].fillna('').str.strip() == ''])

print("=== CURRENT DATABASE METRICS ===")
print(f"Total Verified/Confirmed Products: {total_verified}")
print(f"Total Unverified Products (Pending Verification): {total_needs_verification}")
print(f"Total Invalid/Non-Food Purged Products: {total_invalid_purged}")
print(f"Total Products with Completed Ingredients: {total_with_ingredients}")
print(f"Total Products with Incomplete/Missing Ingredients: {len(nv_all) + (total_verified - total_with_ingredients)}")
