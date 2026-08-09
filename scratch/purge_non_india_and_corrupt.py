import os
import sys
import pandas as pd
import re

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"c:\Users\thout\Downloads\check it"

raw_csv = os.path.join(BASE_DIR, "products_containing_banned_substances.csv")

print("=== DEEP PURGE OF NON-INDIA BARCODES ACROSS FULL DATASET ===")

df = pd.read_csv(raw_csv, dtype=str)
initial_len = len(df)

# 1. REMOVE INVALID / NAN PRODUCT NAMES AND BARCODE-AS-NAME
def is_invalid_name(name):
    if pd.isna(name): return True
    s = str(name).strip().lower()
    if s in ['nan', 'none', 'null', '', 'undefined', 'unknown']: return True
    if re.match(r'^\d+$', s): return True
    if len(s) < 2: return True
    return False

df['invalid_name'] = df['product_name'].apply(is_invalid_name)
invalid_name_count = df['invalid_name'].sum()

# 2. REMOVE SUPPLEMENTS / NON-FOOD
supp_keywords = ['vitamin', 'biotin', 'magnesium', 'prenatal', 'supplement', 'revital', 'whey', 'pre workout', 'protein powder', 'tablet', 'capsule', 'nutraceutical']
def is_supplement(row):
    pname = str(row.get('product_name', '')).lower()
    cat = str(row.get('categories', '')).lower()
    for k in supp_keywords:
        if k in pname or k in cat:
            return True
    return False

df['is_supplement'] = df.apply(is_supplement, axis=1)
supp_count = df['is_supplement'].sum()

# 3. KEEP ONLY VERIFIED INDIA BARCODES (GS1 890 Prefix)
def is_india_barcode(barcode):
    if pd.isna(barcode): return False
    b = str(barcode).strip()
    return b.startswith('890')

df['is_india'] = df['barcode'].apply(is_india_barcode)
non_india_count = (~df['is_india']).sum()

# FILTER
df_clean = df[~df['invalid_name'] & ~df['is_supplement'] & df['is_india']].copy()

# 4. FIX BRAND NAMES FOR SPECIFIC BARCODES
brand_fixes = {
    '8904132953666': 'Independence',
    '8901207006883': 'Dabur',
    '8901014000470': 'Nissin',
    '8904132948181': 'Campa',
    '8901689010125': "Mala's",
    '8901393019469': 'Perfetti Van Melle',
    '8909081006715': 'ITC Candyman',
    '8901393026405': 'Perfetti Van Melle',
    '8901725100117': 'ITC B Natural',
    '8906080602689': 'Paper Boat'
}

for barcode, brand_name in brand_fixes.items():
    mask = df_clean['barcode'] == barcode
    if mask.sum() > 0:
        df_clean.loc[mask, 'brands'] = brand_name

# Clean up temporary columns
df_clean = df_clean.drop(columns=['invalid_name', 'is_supplement', 'is_india'], errors='ignore')

# 5. DEDUPLICATE BY BARCODE AND BANNED ITEM
df_clean = df_clean.drop_duplicates(subset=['barcode', 'banned_item'], keep='first')

# EXPORT FINAL CLEAN INDIA-ONLY DATASET
output_india_only = os.path.join(BASE_DIR, "india_only_banned_products.csv")
df_clean.to_csv(output_india_only, index=False)
df_clean.to_csv(os.path.join(BASE_DIR, "cleaned_dataset.csv"), index=False)
df_clean.to_csv(os.path.join(BASE_DIR, "products_containing_banned_substances.csv"), index=False)

print("\n--- DEEP PURGE & CLEANING SUMMARY ---")
print(f"Original Raw Dataset Rows: {initial_len}")
print(f"❌ Invalid / NAN Names Removed: {invalid_name_count}")
print(f"❌ Supplements Removed: {supp_count}")
print(f"❌ Non-India Barcodes Removed: {non_india_count}")
print(f"✅ FINAL INDIA-ONLY PRODUCTS REMAINING: {len(df_clean)} entries ({df_clean['barcode'].nunique()} unique Indian barcodes)")
print(f"\nSaved India-only dataset to:")
print(f" - {output_india_only}")
print(f" - {os.path.join(BASE_DIR, 'cleaned_dataset.csv')}")
print(f" - {os.path.join(BASE_DIR, 'products_containing_banned_substances.csv')}")
