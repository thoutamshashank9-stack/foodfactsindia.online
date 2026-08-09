import os
import sys
import pandas as pd
import re

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"c:\Users\thout\Downloads\check it"

confirmed_csv = os.path.join(BASE_DIR, "india_products_confirmed.csv")
verification_csv = os.path.join(BASE_DIR, "india_products_needs_verification.csv")
removed_csv = os.path.join(BASE_DIR, "foreign_or_invalid_products_removed.csv")
cleaned_csv = os.path.join(BASE_DIR, "cleaned_dataset.csv")

print("=== EXECUTING STRICT GS1 (890\\d{10}) & NONSENSE/NON-FOOD AUTOCLEAN ===")

df_confirmed = pd.read_csv(confirmed_csv, dtype=str)
df_verification = pd.read_csv(verification_csv, dtype=str)
df_removed = pd.read_csv(removed_csv, dtype=str)

print(f"Loaded Confirmed Table: {len(df_confirmed)}")
print(f"Loaded Verification Queue Table: {len(df_verification)}")
print(f"Loaded Removed Table: {len(df_removed)}")

# 1. STRICT GS1 13-DIGIT PATTERN MATCHING (^890\d{10}$)
def is_valid_13digit_gs1_890(barcode):
    if pd.isna(barcode): return False
    b = str(barcode).strip()
    return bool(re.match(r'^890\d{10}$', b))

# 2. NONSENSE / GIBBERISH PATTERNS
def is_nonsense_title(title):
    if pd.isna(title): return True
    s = str(title).strip().lower()
    if not s or s in ['nan', 'none', 'null', 'undefined', 'unknown product', 'loading...']:
        return True
    if re.match(r'^\d+$', s): # Pure digits/barcode
        return True
    if len(s) < 2:
        return True
    # Only consonants pattern (e.g. "Hdjsjdj")
    if re.match(r'^[bcdfghjklmnpqrstvwxyz]+$', s):
        return True
    return False

# 3. NON-FOOD / CLOTHING / HOUSEHOLD KEYWORDS
non_food_keywords = [
    'chiffon', 'fabric', 'shampoo', 'soap', 'diaper', 'lotion', 'cream', 
    'serum', 'mask', 'wash', 'detergent', 'plastic', 'bucket', 'marker',
    'cloth', 'rag', 'un chiffon', 'tissues', 'wipes', 'sanitizer', 'cleaner'
]

def is_non_food_item(row):
    pname = str(row.get('product_name', '')).lower()
    brand = str(row.get('brands', '')).lower()
    cat = str(row.get('categories', '')).lower()
    
    for kw in non_food_keywords:
        if kw in pname or kw in brand or kw in cat:
            return True
    return False

# FIX KNOWN SPECIFIC SAMPLE ITEMS
brand_manual_fixes = {
    '8906010360405': ('Ghee', 'Local/Regional Dairy'),
    '8901779902569': ('Saras Sunflower Oil', 'Saras'),
    '8901242107408': ('Bambino Roasted Vermicelli', 'Bambino'),
    '8906151991032': ('Strawberry Ice Cream', 'Camerry'),
    '8908016501493': ('Peri Peri Momos', 'Hello Tempayy'),
    '8904001800282': ('Sesame Oil', 'Idayam'),
    '8901491983211': ("Lay's Chips", "Lay's"),
    '8906151236607': ('Millet Fingers Chatpata Masala', 'Snackible'),
    '8906035140204': ('Bengali Mixture', 'Chipo'),
    '8906020582002': ('Protein Rich Chapati', 'Fresh iD'),
    '8904109621116': ('Malabar Paratha', "Nik's Cuisine")
}

for b_code, (p_name, b_name) in brand_manual_fixes.items():
    for df_target in [df_confirmed, df_verification]:
        mask = df_target['barcode'] == b_code
        if mask.sum() > 0:
            df_target.loc[mask, 'product_name'] = p_name
            df_target.loc[mask, 'brands'] = b_name

# FILTER VERIFICATION QUEUE
df_verification['valid_gs1'] = df_verification['barcode'].apply(is_valid_13digit_gs1_890)
df_verification['nonsense'] = df_verification['product_name'].apply(is_nonsense_title)
df_verification['non_food'] = df_verification.apply(is_non_food_item, axis=1)

purge_from_v = df_verification[~df_verification['valid_gs1'] | df_verification['nonsense'] | df_verification['non_food']].copy()
purge_from_v['removal_reason'] = 'STRICT_GS1_OR_NONSENSE_PURGE'

df_verification_clean = df_verification[df_verification['valid_gs1'] & ~df_verification['nonsense'] & ~df_verification['non_food']].copy()
df_verification_clean = df_verification_clean.drop(columns=['valid_gs1', 'nonsense', 'non_food'])

# FILTER CONFIRMED TABLE
df_confirmed['valid_gs1'] = df_confirmed['barcode'].apply(is_valid_13digit_gs1_890)
df_confirmed['nonsense'] = df_confirmed['product_name'].apply(is_nonsense_title)
df_confirmed['non_food'] = df_confirmed.apply(is_non_food_item, axis=1)

purge_from_c = df_confirmed[~df_confirmed['valid_gs1'] | df_confirmed['nonsense'] | df_confirmed['non_food']].copy()
purge_from_c['removal_reason'] = 'STRICT_GS1_OR_NONSENSE_PURGE'

df_confirmed_clean = df_confirmed[df_confirmed['valid_gs1'] & ~df_confirmed['nonsense'] & ~df_confirmed['non_food']].copy()
df_confirmed_clean = df_confirmed_clean.drop(columns=['valid_gs1', 'nonsense', 'non_food'])

# COMBINE ALL PURGED ITEMS INTO TABLE 3
all_purged = pd.concat([purge_from_v, purge_from_c], ignore_index=True)
cols_drop = ['valid_gs1', 'nonsense', 'non_food']
all_purged = all_purged.drop(columns=cols_drop, errors='ignore')

df_removed_updated = pd.concat([df_removed, all_purged], ignore_index=True)
df_removed_updated = df_removed_updated.drop_duplicates(subset=['barcode'], keep='first')

# EXPORT CLEANED TABLES
df_confirmed_clean.to_csv(confirmed_csv, index=False)
df_verification_clean.to_csv(verification_csv, index=False)
df_removed_updated.to_csv(removed_csv, index=False)

# Update cleaned_dataset.csv in workspace root
df_confirmed_clean.to_csv(cleaned_csv, index=False)

print("\n--- FINAL STRICT GS1 & NONSENSE PURGE SUMMARY ---")
print(f"🟢 Table 1: india_products_confirmed: {len(df_confirmed_clean)} products ({df_confirmed_clean['barcode'].nunique()} unique barcodes)")
print(f"🟡 Table 2: india_products_needs_verification: {len(df_verification_clean)} products ({df_verification_clean['barcode'].nunique()} unique barcodes)")
print(f"❌ Table 3: foreign_or_invalid_products_removed: {len(df_removed_updated)} products ({df_removed_updated['barcode'].nunique()} unique barcodes)")

print(f"\nPurged {len(all_purged)} invalid/non-food/nonsense rows across tables.")
print(f"Saved updated CSV files to:")
print(f" - {confirmed_csv}")
print(f" - {verification_csv}")
print(f" - {removed_csv}")
