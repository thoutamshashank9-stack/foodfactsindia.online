import os
import sys
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"c:\Users\thout\Downloads\check it"

confirmed_path = os.path.join(BASE_DIR, "india_products_confirmed.csv")
needs_ver_path = os.path.join(BASE_DIR, "india_products_needs_verification.csv")

# Load master domestic datasets
df_c = pd.read_csv(confirmed_path, dtype=str)
df_nv = pd.read_csv(needs_ver_path, dtype=str)

# Clean fields
for df in [df_c, df_nv]:
    df['barcode'] = df['barcode'].fillna('').str.strip()
    df['product_name'] = df['product_name'].fillna('').str.strip()
    df['brands'] = df['brands'].fillna('').str.strip()
    df['ingredients_text'] = df['ingredients_text'].fillna('').str.strip()

# 1. products_with_complete_ingredients.csv
# Derived from confirmed (all verified products carry complete ingredients)
df_complete = df_c[['barcode', 'product_name', 'brands', 'ingredients_text']].copy()
df_complete.to_csv(os.path.join(BASE_DIR, "products_with_complete_ingredients.csv"), index=False)

# 2. products_without_complete_ingredients.csv
# Derived from needs_verification (all unverified or stub entries)
df_incomplete = df_nv[['barcode', 'product_name', 'brands', 'ingredients_text']].copy()
df_incomplete.to_csv(os.path.join(BASE_DIR, "products_without_complete_ingredients.csv"), index=False)

# 3. products_with_ingredients.csv
# Any domestic product containing non-empty ingredients text
df_combined = pd.concat([df_c, df_nv], ignore_index=True)

# Helper function to check if ingredients text is non-empty
def is_valid_ingredients(text):
    t = str(text).strip().lower()
    return t not in ['', 'nan', 'none', 'pending capture']

with_ing_mask = df_combined['ingredients_text'].apply(is_valid_ingredients)

df_with_ing = df_combined[with_ing_mask].copy()
# Add blank categories column to maintain schema compatibility
df_with_ing['categories'] = ''
df_with_ing = df_with_ing[['barcode', 'product_name', 'brands', 'categories', 'ingredients_text']]
df_with_ing.to_csv(os.path.join(BASE_DIR, "products_with_ingredients.csv"), index=False)

# 4. products_without_ingredients.csv
# Any domestic product where ingredients text is empty or pending
df_without_ing = df_combined[~with_ing_mask].copy()
df_without_ing['categories'] = ''
df_without_ing = df_without_ing[['barcode', 'product_name', 'brands', 'categories', 'ingredients_text']]
df_without_ing.to_csv(os.path.join(BASE_DIR, "products_without_ingredients.csv"), index=False)

print("=== REGENERATION SUMMARY ===")
print(f"1. products_with_complete_ingredients.csv: {len(df_complete)} rows")
print(f"2. products_without_complete_ingredients.csv: {len(df_incomplete)} rows")
print(f"3. products_with_ingredients.csv: {len(df_with_ing)} rows")
print(f"4. products_without_ingredients.csv: {len(df_without_ing)} rows")
print("Regenerated all 4 helper CSV files successfully.")
