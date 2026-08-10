import os
import sys
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"c:\Users\thout\Downloads\check it"

confirmed_csv = os.path.join(BASE_DIR, "india_products_confirmed.csv")
verification_csv = os.path.join(BASE_DIR, "india_products_needs_verification.csv")

df_confirmed = pd.read_csv(confirmed_csv, dtype=str)
df_verification = pd.read_csv(verification_csv, dtype=str)

# Analysis functions
def get_brand_summary(df):
    return df['brands'].value_counts().head(10).to_dict()

def get_source_summary(df):
    return df['data_source'].value_counts().to_dict()

def get_missing_ingredients_count(df):
    # Ingredients text empty, nan, none or too short
    empty_mask = df['ingredients_text'].isna() | (df['ingredients_text'].astype(str).str.strip().str.lower().isin(['nan', 'none', '']))
    return empty_mask.sum()

print("--- CONFIRMED (VERIFIED) PRODUCTS REPORT ---")
total_confirmed = len(df_confirmed)
confirmed_brands = get_brand_summary(df_confirmed)
confirmed_sources = get_source_summary(df_confirmed)
confirmed_missing_ing = get_missing_ingredients_count(df_confirmed)

print(f"Total Verified Products: {total_confirmed}")
print("Top Brands:")
for b, c in confirmed_brands.items():
    print(f"  {b}: {c}")
print("Data Sources:")
for s, c in confirmed_sources.items():
    print(f"  {s}: {c}")
print(f"Products missing ingredients: {confirmed_missing_ing} ({confirmed_missing_ing/total_confirmed*100:.1f}%)")

print("\n--- NEEDS VERIFICATION (UNVERIFIED) PRODUCTS REPORT ---")
total_unverified = len(df_verification)
unverified_brands = get_brand_summary(df_verification)
unverified_sources = get_source_summary(df_verification)
unverified_missing_ing = get_missing_ingredients_count(df_verification)

print(f"Total Unverified Products: {total_unverified}")
print("Top Brands:")
for b, c in unverified_brands.items():
    print(f"  {b}: {c}")
print("Data Sources:")
for s, c in unverified_sources.items():
    print(f"  {s}: {c}")
print(f"Products missing ingredients: {unverified_missing_ing} ({unverified_missing_ing/total_unverified*100:.1f}%)")

# Write some sample records to format in markdown
df_confirmed.head(20).to_csv(os.path.join(BASE_DIR, "scratch", "confirmed_samples.csv"), index=False)
df_verification.head(20).to_csv(os.path.join(BASE_DIR, "scratch", "unverified_samples.csv"), index=False)
