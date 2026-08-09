import os
import sys
import pandas as pd
import re
import json

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"c:\Users\thout\Downloads\check it"

all_supabase_csv = os.path.join(BASE_DIR, "all_supabase_products.csv")
cleaned_csv = os.path.join(BASE_DIR, "cleaned_dataset.csv")

print("=== EXECUTING DATABASE TRI-TABLE SPLIT & FORENSIC SANITIZATION ===")

df_all = pd.read_csv(all_supabase_csv, dtype=str)
initial_total = len(df_all)

# 1. IDENTIFY INVALID / NONSENSE ROWS & BARCODES
nonsense_keywords = [
    'undefined', 'roomspraymy', 'the indian cooking instructions methods',
    'the provided text does not contain an ingredient list', 'us(mg) nesium',
    'fat,protein,carbohydrate', 'biscuit 🍪', 'mufbmuvcvyv', '50gr'
]

def is_nonsense_or_invalid(row):
    barcode = str(row.get('barcode', '')).strip()
    pname = str(row.get('product_name', '')).strip().lower()
    ing = str(row.get('ingredients_text', '') or row.get('ingredient_list_raw', '')).strip().lower()
    
    # Invalid barcode length (>14 or non-digit or <5)
    if not barcode.isdigit() or len(barcode) > 14 or len(barcode) < 5:
        return True
    
    # Invalid product name
    if not pname or pname in ['nan', 'none', 'null', 'undefined', 'unknown'] or re.match(r'^\d+$', pname):
        return True
    
    # Nonsense ingredient text
    for kw in nonsense_keywords:
        if kw in ing:
            return True
            
    return False

df_all['is_invalid'] = df_all.apply(is_nonsense_or_invalid, axis=1)

# 2. IDENTIFY SUPPLEMENTS & MEDICAL NUTRITION
supp_keywords = [
    'vitamin', 'biotin', 'magnesium', 'prenatal', 'supplement', 'revital',
    'whey', 'pre workout', 'pre-workout', 'protein bar', 'protein powder',
    'calcium tablet', 'capsule', 'tablet', 'nutraceutical', 'celevida', 'ensure'
]

def is_supplement_item(row):
    pname = str(row.get('product_name', '')).lower()
    cat = str(row.get('categories', '')).lower()
    brand = str(row.get('brands', '')).lower()
    for kw in supp_keywords:
        if kw in pname or kw in cat or kw in brand:
            return True
    return False

df_all['is_supplement'] = df_all.apply(is_supplement_item, axis=1)

# 3. IDENTIFY GS1 890 DOMESTIC INDIA BARCODES
df_all['is_india_890'] = df_all['barcode'].astype(str).str.startswith('890')

# 4. BRAND FIXES & OCR SANITIZATION
brand_corrections = {
    '8902167000126': 'Everest',
    '8906001057789': 'MDH',
    '8901047009051': 'Kohinoor',
    '8901063093638': 'Britannia',
    '8909081005589': 'Bingo',
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

for b_code, b_name in brand_corrections.items():
    mask = df_all['barcode'] == b_code
    if mask.sum() > 0:
        df_all.loc[mask, 'brands'] = b_name

# Fix product name spelling
spelling_fixes = {
    '8906112660793': 'Museli -> Muesli'
}
mask_muesli = df_all['barcode'] == '8906112660793'
if mask_muesli.sum() > 0:
    df_all.loc[mask_muesli, 'product_name'] = 'True Elements Fruit & Nut Muesli'

# 5. INGREDIENT COMPLETENESS CHECK
ing_col = 'ingredients_text' if 'ingredients_text' in df_all.columns else 'ingredient_list_raw'
df_all['has_complete_ingredients'] = df_all[ing_col].apply(
    lambda x: pd.notna(x) and len(str(x).strip()) >= 15 and str(x).strip().lower() != 'nan'
)

# --- SPLIT INTO THREE TABLES ---

# TABLE 1: india_products_confirmed
# (GS1 890 + Not Invalid + Not Supplement + Complete Ingredients)
table_confirmed = df_all[
    df_all['is_india_890'] & ~df_all['is_invalid'] & ~df_all['is_supplement'] & df_all['has_complete_ingredients']
].copy()
table_confirmed['sold_in_india_status'] = 'CONFIRMED_INDIA_890'
table_confirmed['ingredient_confidence'] = 'HIGH'
table_confirmed['status'] = 'KEEP'

# TABLE 2: india_products_needs_verification
# (GS1 890 + Not Invalid + Not Supplement + Incomplete Ingredients)
table_needs_verification = df_all[
    df_all['is_india_890'] & ~df_all['is_invalid'] & ~df_all['is_supplement'] & ~df_all['has_complete_ingredients']
].copy()
table_needs_verification['sold_in_india_status'] = 'NEEDS_VERIFICATION'
table_needs_verification['ingredient_confidence'] = 'INCOMPLETE'
table_needs_verification['status'] = 'FIX'

# TABLE 3: foreign_or_invalid_products_removed
# (Non-890 OR Invalid OR Supplement)
table_removed = df_all[
    ~df_all['is_india_890'] | df_all['is_invalid'] | df_all['is_supplement']
].copy()

def classify_removal_reason(row):
    if row['is_invalid']: return 'INVALID_OR_NONSENSE_DATA'
    if row['is_supplement']: return 'SUPPLEMENT_OR_MEDICAL_NUTRITION'
    if not row['is_india_890']: return 'FOREIGN_NON_890_BARCODE'
    return 'OTHER'

table_removed['removal_reason'] = table_removed.apply(classify_removal_reason, axis=1)

# Export all three tables to CSV
path_confirmed = os.path.join(BASE_DIR, "india_products_confirmed.csv")
path_needs_verification = os.path.join(BASE_DIR, "india_products_needs_verification.csv")
path_removed = os.path.join(BASE_DIR, "foreign_or_invalid_products_removed.csv")

# Clean temp columns before export
cols_to_drop = ['is_invalid', 'is_supplement', 'is_india_890', 'has_complete_ingredients']
table_confirmed.drop(columns=cols_to_drop, errors='ignore').to_csv(path_confirmed, index=False)
table_needs_verification.drop(columns=cols_to_drop, errors='ignore').to_csv(path_needs_verification, index=False)
table_removed.drop(columns=cols_to_drop, errors='ignore').to_csv(path_removed, index=False)

# Update cleaned_dataset.csv in workspace root to use ONLY confirmed India products
table_confirmed.drop(columns=cols_to_drop, errors='ignore').to_csv(cleaned_csv, index=False)

print("\n--- TRI-TABLE DATABASE SPLIT SUMMARY ---")
print(f"Total Initial Products: {initial_total}")
print(f"🟢 Table 1: india_products_confirmed: {len(table_confirmed)} products ({table_confirmed['barcode'].nunique()} unique barcodes)")
print(f"🟡 Table 2: india_products_needs_verification: {len(table_needs_verification)} products ({table_needs_verification['barcode'].nunique()} unique barcodes)")
print(f"❌ Table 3: foreign_or_invalid_products_removed: {len(table_removed)} products ({table_removed['barcode'].nunique()} unique barcodes)")

print("\nBreakdown of Removal Reasons (Table 3):")
print(table_removed['removal_reason'].value_counts())

print("\nSaved 3 Clean Database CSV Files:")
print(f" - {path_confirmed}")
print(f" - {path_needs_verification}")
print(f" - {path_removed}")
