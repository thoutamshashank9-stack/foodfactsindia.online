#!/usr/bin/env python3
"""
FoodFactsIndia.online - Complete Dataset Cleaning Pipeline
Version: 2.0
Author: FoodFactsIndia Development Team
Purpose: Clean, validate, and standardize the product database
"""

import os
import sys
import pandas as pd
import numpy as np
import re
import json
from collections import Counter
from datetime import datetime

# Set encoding for Windows console output
sys.stdout.reconfigure(encoding='utf-8')

# ============================================================
# CONFIGURATION
# ============================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_FILE = os.path.join(BASE_DIR, 'products_containing_banned_substances.csv')
OUTPUT_CLEAN = os.path.join(BASE_DIR, 'cleaned_dataset.csv')
OUTPUT_REMOVED = os.path.join(BASE_DIR, 'removed_entries.csv')
OUTPUT_VERIFICATION = os.path.join(BASE_DIR, 'needs_verification.csv')
OUTPUT_REPORT = os.path.join(BASE_DIR, 'cleaning_report.json')

# ============================================================
# STEP 0: LOAD DATASET
# ============================================================
print("=" * 60)
print("🔧 FoodFactsIndia Dataset Cleaning Pipeline v2.0")
print("=" * 60)

df = pd.read_csv(INPUT_FILE)
original_count = len(df)
print(f"\n📊 Original dataset loaded: {original_count} rows")
print(f"📊 Columns: {list(df.columns)}")

# Track all removals for reporting
removal_log = []

# ============================================================
# STEP 1: REMOVE "nan" AND INVALID PRODUCT NAMES
# ============================================================
print("\n" + "=" * 60)
print("STEP 1: Removing invalid product names...")
print("=" * 60)

def is_invalid_name(name):
    """Check if product name is invalid"""
    if pd.isna(name):
        return True
    name_str = str(name).strip().lower()
    if name_str in ['nan', 'none', 'null', '', 'undefined']:
        return True
    # Check if name is just a barcode (all digits)
    if re.match(r'^\d+$', name_str):
        return True
    # Check if name is too short (< 2 chars)
    if len(name_str) < 2:
        return True
    return False

invalid_name_mask = df['product_name'].apply(is_invalid_name)
invalid_count = invalid_name_mask.sum()
print(f"  ❌ Found {invalid_count} entries with invalid product names")

# Log removed entries
removed_df = df[invalid_name_mask].copy()
removed_df['removal_reason'] = 'Invalid/missing product name'
removal_log.append(removed_df)

# Remove them
df = df[~invalid_name_mask].copy()
print(f"  ✅ Removed. Remaining: {len(df)} rows")

# ============================================================
# STEP 2: REMOVE DIETARY SUPPLEMENTS / NON-FOOD ITEMS
# ============================================================
print("\n" + "=" * 60)
print("STEP 2: Removing dietary supplements and non-food items...")
print("=" * 60)

supplement_keywords = [
    'vitamin', 'biotin', 'magnesium', 'prenatal', 'multivitamine',
    'supplement', 'revital', 'whey', 'pre workout', 'pre-workout',
    'protein bar', 'protein powder', 'calcium tablet', 'capsule',
    'tablet', 'nutraceutical', 'ayurvedic medicine'
]

supplement_categories = [
    'dietary supplement', 'supplement', 'vitamins', 'micronutrient',
    'protein energy bars', 'whey powder'
]

def is_supplement(row):
    """Check if product is a supplement"""
    name = str(row.get('product_name', '')).lower()
    category = str(row.get('categories', '')).lower()
    brand = str(row.get('brands', '')).lower()
    
    for keyword in supplement_keywords:
        if keyword in name:
            return True
    
    for cat in supplement_categories:
        if cat in category:
            return True
    
    # Specific brand checks
    supplement_brands = ["nature's bounty", "vestige", "neuherbs", "muscleblaze", "optimum nutrition"]
    for sb in supplement_brands:
        if sb in brand:
            return True
    
    return False

supplement_mask = df.apply(is_supplement, axis=1)
supplement_count = supplement_mask.sum()
print(f"  ❌ Found {supplement_count} supplement entries")

removed_df = df[supplement_mask].copy()
removed_df['removal_reason'] = 'Dietary supplement / Non-food item'
removal_log.append(removed_df)

df = df[~supplement_mask].copy()
print(f"  ✅ Removed. Remaining: {len(df)} rows")

# ============================================================
# STEP 3: REMOVE CORRUPTED / DATA ERROR ENTRIES
# ============================================================
print("\n" + "=" * 60)
print("STEP 3: Removing corrupted entries...")
print("=" * 60)

# Specific corrupted barcodes to remove
corrupted_barcodes = [
    '8906002006601',  # Dr. Oetker "Sausages" with barcode as name
]

corrupted_mask = df['barcode'].astype(str).isin(corrupted_barcodes)
corrupted_count = corrupted_mask.sum()
print(f"  ❌ Found {corrupted_count} corrupted entries")

if corrupted_count > 0:
    removed_df = df[corrupted_mask].copy()
    removed_df['removal_reason'] = 'Corrupted data entry'
    removal_log.append(removed_df)
    df = df[~corrupted_mask].copy()

print(f"  ✅ Removed. Remaining: {len(df)} rows")

# ============================================================
# STEP 4: STANDARDIZE BARCODES
# ============================================================
print("\n" + "=" * 60)
print("STEP 4: Standardizing barcode formats...")
print("=" * 60)

def normalize_barcode(barcode):
    """Normalize barcode to standard format"""
    barcode = str(barcode).strip()
    # Remove non-digit characters
    barcode = re.sub(r'[^0-9]', '', barcode)
    
    if len(barcode) == 0:
        return None
    
    # Pad to at least 8 digits (minimum valid barcode length)
    if len(barcode) < 8:
        # Keep short barcodes as-is but flag them
        return barcode
    
    return barcode

df['barcode'] = df['barcode'].apply(normalize_barcode)

# Remove entries where barcode became None
null_barcode_mask = df['barcode'].isna()
null_barcode_count = null_barcode_mask.sum()
if null_barcode_count > 0:
    removed_df = df[null_barcode_mask].copy()
    removed_df['removal_reason'] = 'Invalid barcode'
    removal_log.append(removed_df)
    df = df[~null_barcode_mask].copy()

# Flag non-standard barcodes (not 8, 12, 13, or 14 digits)
def is_standard_barcode(barcode):
    """Check if barcode is standard length"""
    clean = str(barcode).lstrip('0')  # Remove leading zeros for length check
    return len(str(barcode)) in [8, 12, 13, 14]

df['barcode_standard'] = df['barcode'].apply(is_standard_barcode)
non_standard_count = (~df['barcode_standard']).sum()
print(f"  ⚠️  {non_standard_count} barcodes with non-standard length (flagged)")
print(f"  ✅ Barcode standardization complete. Remaining: {len(df)} rows")

# ============================================================
# STEP 5: STANDARDIZE BANNED ITEM NAMES
# ============================================================
print("\n" + "=" * 60)
print("STEP 5: Standardizing banned ingredient names...")
print("=" * 60)

ingredient_mapping = {
    # PHO variations
    'Partially Hydrogenated Oil (PHO)': 'Partially Hydrogenated Oil (PHO)',
    'hydrogenated vegetable oil': 'Partially Hydrogenated Oil (PHO)',
    'Hydrogenated Vegetable Oil': 'Partially Hydrogenated Oil (PHO)',
    'hydrogenated vegetable oil (INS)': 'Partially Hydrogenated Oil (PHO)',
    
    # TBHQ
    'TBHQ (Tertiary Butylhydroquinone) (E319)': 'TBHQ (E319)',
    'TBHQ (E319)': 'TBHQ (E319)',
    
    # Carmoisine / Azorubine
    'Carmoisine (E122)': 'Carmoisine / Azorubine (E122)',
    'Azorubine (Carmoisine) (E122)': 'Carmoisine / Azorubine (E122)',
    
    # Titanium Dioxide
    'Titanium Dioxide (E171)': 'Titanium Dioxide (E171)',
    
    # Potassium Bromate
    'Potassium Bromate (E924A)': 'Potassium Bromate (E924A)',
    'Potassium Bromate': 'Potassium Bromate (E924A)',
    
    # Azodicarbonamide
    'Azodicarbonamide (ADA) (E927A)': 'Azodicarbonamide (E927A)',
    'Azodicarbonamide (ADA)': 'Azodicarbonamide (E927A)',
    
    # BVO
    'Brominated Vegetable Oil (BVO)': 'Brominated Vegetable Oil (BVO)',
    
    # Erythrosine
    'Erythrosine (E127)': 'Erythrosine (E127)',
    
    # Ponceau 4R
    'Ponceau 4R (E124)': 'Ponceau 4R (E124)',
    
    # Quinoline Yellow
    'Quinoline Yellow (E104)': 'Quinoline Yellow (E104)',
    
    # Green S
    'Green S (E142)': 'Green S (E142)',
    
    # Brilliant Black BN
    'Brilliant Black BN (E151)': 'Brilliant Black BN (E151)',
    
    # Patent Blue V
    'Patent Blue V (E131)': 'Patent Blue V (E131)',
    
    # Brown HT
    'Brown HT (E155)': 'Brown HT (E155)',
    
    # Fast Green FCF
    'Fast Green FCF (E143)': 'Fast Green FCF (E143)',
}

before_standardize = df['banned_item'].nunique()
df['banned_item'] = df['banned_item'].replace(ingredient_mapping)
after_standardize = df['banned_item'].nunique()
print(f"  ✅ Ingredient names standardized: {before_standardize} → {after_standardize} unique names")

# ============================================================
# STEP 6: STANDARDIZE JURISDICTIONS
# ============================================================
print("\n" + "=" * 60)
print("STEP 6: Standardizing jurisdiction format...")
print("=" * 60)

# Jurisdiction code mapping
jurisdiction_codes = {
    'US': 'United States',
    'CA': 'Canada',
    'EU': 'European Union',
    'UK': 'United Kingdom',
    'JP': 'Japan',
    'IN': 'India',
    'AU': 'Australia',
    'NZ': 'New Zealand',
}

def parse_jurisdictions(j):
    """Parse jurisdiction string into list"""
    if pd.isna(j):
        return []
    j_str = str(j).strip()
    parts = [x.strip() for x in j_str.split(',')]
    # Validate each part
    valid_parts = []
    for p in parts:
        p_upper = p.upper().strip()
        if p_upper in jurisdiction_codes:
            valid_parts.append(p_upper)
        elif p_upper in ['US, CA', 'JP, US', 'EU, UK', 'IN, JP, US', 'EU, UK, IN']:
            # Handle cases where comma is inside quotes
            sub_parts = [x.strip().upper() for x in p_upper.split(',')]
            valid_parts.extend([sp for sp in sub_parts if sp in jurisdiction_codes])
        else:
            valid_parts.append(p_upper)
    return valid_parts

df['banned_in_jurisdictions'] = df['banned_in_jurisdictions'].apply(parse_jurisdictions)
print(f"  ✅ Jurisdictions standardized to structured format")

# ============================================================
# STEP 7: FIX MISSPELLED PRODUCT/BRAND NAMES
# ============================================================
print("\n" + "=" * 60)
print("STEP 7: Fixing misspelled names...")
print("=" * 60)

# Product name corrections
name_corrections = {
    'niisin': 'Nissin',
    'top ramn': 'Top Ramen',
    'Jim jam92 g': 'Jim Jam 92g',
    'Jimjam 57g (57)': 'Jim Jam 57g',
    'bix cake sandwich': 'Bix Cake Sandwich',
    'Chula Chups': 'Chupa Chups',
    'Dr. Oetket': 'Dr. Oetker',
    'cup noodles': 'Cup Noodles',
    'mapro jam': 'Mapro Jam',
    'mapro mixed fruit jam': 'Mapro Mixed Fruit Jam',
    'mapro butterscotch syrup': 'Mapro Butterscotch Syrup',
    'chings noodles': "Ching's Noodles",
    'protien bar': 'Protein Bar',
}

# Brand name corrections
brand_corrections = {
    'Sunfest': 'Sunfeast',
    'sunfest': 'Sunfeast',
    'Kisaan': 'Kissan',
    'kissan': 'Kissan',
    'kisaan': 'Kissan',
    'Unknown Brand': '',
    'nan': '',
    'None': '',
    'ITC Limied': 'ITC Limited',
    'nissin': 'Nissin',
    'maggi': 'Maggi',
    'oreo': 'Oreo',
    'pepsico': 'PepsiCo',
    'pepsi': 'PepsiCo',
    'fortune': 'Fortune',
    'b natural': 'B Natural',
    'cup noodles': 'Nissin',
    'Cup noodles, Nissin': 'Nissin',
}

fixes_applied = 0
for old_name, new_name in name_corrections.items():
    mask = df['product_name'].str.lower() == old_name.lower()
    if mask.sum() > 0:
        df.loc[mask, 'product_name'] = new_name
        fixes_applied += mask.sum()

for old_brand, new_brand in brand_corrections.items():
    mask = df['brands'].str.lower() == old_brand.lower()
    if mask.sum() > 0:
        df.loc[mask, 'brands'] = new_brand
        fixes_applied += mask.sum()

print(f"  ✅ Applied {fixes_applied} name corrections")

# ============================================================
# STEP 8: FIX EMPTY BRAND FIELDS
# ============================================================
print("\n" + "=" * 60)
print("STEP 8: Handling empty brand fields...")
print("=" * 60)

empty_brand_mask = df['brands'].isna() | (df['brands'].str.strip() == '') | (df['brands'].str.lower() == 'nan')
empty_brand_count = empty_brand_mask.sum()
print(f"  ⚠️  {empty_brand_count} entries with empty brands (set to 'Unbranded')")
df.loc[empty_brand_mask, 'brands'] = 'Unbranded'

# ============================================================
# STEP 9: FIX CATEGORY CODES
# ============================================================
print("\n" + "=" * 60)
print("STEP 9: Fixing FSSAI category codes...")
print("=" * 60)

# Category corrections based on product type
category_fixes = {
    # Snacks should be CAT_15
    'Pringles': 'CAT_15',
    'Doritos': 'CAT_15',
    'Lays': 'CAT_15',
    "Lay's": 'CAT_15',
    'Act II': 'CAT_15',
    'ACT II': 'CAT_15',
    'Act 2': 'CAT_15',
    'ACT 2': 'CAT_15',
    
    # Biscuits/Cookies should be CAT_07
    'Oreo': 'CAT_07',
    'Britannia': 'CAT_07',
    'Parle': 'CAT_07',
    'Sunfeast': 'CAT_07',
    
    # Confectionery should be CAT_05
    'M&M': 'CAT_05',
    "M&M's": 'CAT_05',
    'Snickers': 'CAT_05',
    'Cadbury': 'CAT_05',
    'Chupa Chups': 'CAT_05',
    
    # Noodles should be CAT_06
    'Maggi': 'CAT_06',
    'Nissin': 'CAT_06',
    "Ching's": 'CAT_06',
    'Top Ramen': 'CAT_06',
    
    # Oils should be CAT_02
    'Fortune': 'CAT_02',
    'Saffola': 'CAT_02',
    'Sundrop': 'CAT_02',
    'Emami': 'CAT_02',
    'Dhara': 'CAT_02',
    'Patanjali': 'CAT_02',
    
    # Beverages should be CAT_14
    'Campa': 'CAT_14',
    'Bovonto': 'CAT_14',
    'Paper Boat': 'CAT_14',
    
    # Ice cream should be CAT_01
    'Amul': 'CAT_01',
    'Vadilal': 'CAT_01',
    'Kwality': 'CAT_01',
    'Havmor': 'CAT_01',
    'Mother Dairy': 'CAT_01',
    
    # Jams should be CAT_04
    'Kissan': 'CAT_04',
    'Mapro': 'CAT_04',
    'Mala': 'CAT_04',
}

category_fixes_applied = 0
for brand, correct_cat in category_fixes.items():
    mask = df['brands'].str.contains(brand, case=False, na=False)
    unknown_mask = mask & (df['fssai_category_code'] == 'Unknown')
    if unknown_mask.sum() > 0:
        df.loc[unknown_mask, 'fssai_category_code'] = correct_cat
        category_fixes_applied += unknown_mask.sum()

# Fix specific wrong categories
specific_fixes = [
    # Pringles Cheesy Cheese wrongly in CAT_01
    (df['barcode'] == '8886467100031', 'CAT_15'),
    # Jimjam Pops wrongly in CAT_01
    (df['barcode'] == '8901063029309', 'CAT_07'),
    # M&M's Peanuts wrongly in CAT_14
    (df['barcode'] == '5000159476782', 'CAT_05'),
    # m&m's biscuit wrongly in CAT_14
    (df['barcode'] == '5000159388658', 'CAT_07'),
    # Laduma wrongly in CAT_14
    (df['barcode'] == '6001065034027', 'CAT_05'),
    # Mini Eggs wrongly in CAT_14
    (df['barcode'] == '0061200016420', 'CAT_05'),
    # Sun Lite Oil wrongly in CAT_06
    (df['barcode'] == '8901709007753', 'CAT_02'),
    # Act II Caramel wrongly in CAT_05
    (df['barcode'] == '8901512917805', 'CAT_15'),
]

for mask, correct_cat in specific_fixes:
    if mask.sum() > 0:
        df.loc[mask, 'fssai_category_code'] = correct_cat
        category_fixes_applied += mask.sum()

print(f"  ✅ Applied {category_fixes_applied} category fixes")

# ============================================================
# STEP 10: DEDUPLICATE
# ============================================================
print("\n" + "=" * 60)
print("STEP 10: Removing duplicate entries...")
print("=" * 60)

before_dedup = len(df)

# Remove exact duplicates
df = df.drop_duplicates(subset=['barcode', 'banned_item'], keep='first')

after_dedup = len(df)
duplicates_removed = before_dedup - after_dedup
print(f"  ❌ Removed {duplicates_removed} duplicate entries")
print(f"  ✅ Remaining: {after_dedup} rows")

# ============================================================
# STEP 11: FLAG ENTRIES NEEDING MANUAL VERIFICATION
# ============================================================
print("\n" + "=" * 60)
print("STEP 11: Flagging entries for manual verification...")
print("=" * 60)

df['needs_verification'] = False
df['verification_reason'] = ''

# Flag "Banned in India" claims (need FSSAI verification)
def has_india_ban(jurisdictions):
    return 'IN' in jurisdictions

india_ban_mask = df['banned_in_jurisdictions'].apply(has_india_ban)
df.loc[india_ban_mask, 'needs_verification'] = True
df.loc[india_ban_mask, 'verification_reason'] = 'Claims banned in India - verify against FSSAI Schedule 2.4.5'

# Flag entries with "Unknown" category
unknown_cat_mask = df['fssai_category_code'] == 'Unknown'
df.loc[unknown_cat_mask, 'needs_verification'] = True
df.loc[unknown_cat_mask, 'verification_reason'] += ' | Unknown FSSAI category'

# Flag non-standard barcodes
df.loc[~df['barcode_standard'], 'needs_verification'] = True
df.loc[~df['barcode_standard'], 'verification_reason'] += ' | Non-standard barcode length'

verification_count = df['needs_verification'].sum()
print(f"  ⚠️  {verification_count} entries flagged for manual verification")

# ============================================================
# STEP 12: ADD METADATA COLUMNS
# ============================================================
print("\n" + "=" * 60)
print("STEP 12: Adding metadata columns...")
print("=" * 60)

df['data_source'] = 'OpenFoodFacts / GS1 Database'
df['last_cleaned'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
df['is_verified'] = ~df['needs_verification']
df['platform'] = 'foodfactsindia.online'

# Clean up the barcode_standard column (remove it from final output)
df = df.drop(columns=['barcode_standard'])

print(f"  ✅ Metadata columns added")

# ============================================================
# STEP 13: EXPORT RESULTS
# ============================================================
print("\n" + "=" * 60)
print("STEP 13: Exporting results...")
print("=" * 60)

# Export cleaned dataset
df.to_csv(OUTPUT_CLEAN, index=False)
print(f"  ✅ Cleaned dataset saved: {OUTPUT_CLEAN} ({len(df)} rows)")

# Export removed entries
if removal_log:
    all_removed = pd.concat(removal_log, ignore_index=True)
    all_removed.to_csv(OUTPUT_REMOVED, index=False)
    print(f"  ✅ Removed entries saved: {OUTPUT_REMOVED} ({len(all_removed)} rows)")

# Export entries needing verification
verification_df = df[df['needs_verification']]
verification_df.to_csv(OUTPUT_VERIFICATION, index=False)
print(f"  ✅ Verification needed saved: {OUTPUT_VERIFICATION} ({len(verification_df)} rows)")

# ============================================================
# STEP 14: GENERATE CLEANING REPORT
# ============================================================
print("\n" + "=" * 60)
print("STEP 14: Generating cleaning report...")
print("=" * 60)

report = {
    "cleaning_timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    "platform": "foodfactsindia.online",
    "summary": {
        "original_rows": original_count,
        "final_rows": len(df),
        "total_removed": original_count - len(df),
        "removal_percentage": round((original_count - len(df)) / original_count * 100, 2)
    },
    "removals": {
        "invalid_names": invalid_count,
        "supplements": supplement_count,
        "corrupted_entries": corrupted_count,
        "duplicates": duplicates_removed,
        "invalid_barcodes": null_barcode_count
    },
    "fixes_applied": {
        "name_corrections": fixes_applied,
        "category_fixes": category_fixes_applied,
        "ingredient_standardizations": before_standardize - after_standardize
    },
    "flags": {
        "needs_verification": int(verification_count),
        "non_standard_barcodes": int(non_standard_count),
        "empty_brands_filled": int(empty_brand_count)
    },
    "dataset_stats": {
        "unique_products": int(df['barcode'].nunique()),
        "unique_banned_ingredients": int(df['banned_item'].nunique()),
        "unique_brands": int(df['brands'].nunique()),
        "top_banned_ingredients": df['banned_item'].value_counts().head(10).to_dict(),
        "top_brands": df['brands'].value_counts().head(10).to_dict(),
        "jurisdiction_distribution": {
            j: sum(1 for jlist in df['banned_in_jurisdictions'] if j in jlist)
            for j in ['US', 'EU', 'JP', 'IN', 'CA', 'UK']
        }
    }
}

with open(OUTPUT_REPORT, 'w') as f:
    json.dump(report, f, indent=2, default=str)

print(f"  ✅ Cleaning report saved: {OUTPUT_REPORT}")

# ============================================================
# FINAL SUMMARY
# ============================================================
print("\n" + "=" * 60)
print("📊 FINAL CLEANING SUMMARY")
print("=" * 60)
print(f"""
  Original Rows:          {original_count}
  Final Rows:             {len(df)}
  Total Removed:          {original_count - len(df)}
  Removal Rate:           {round((original_count - len(df)) / original_count * 100, 2)}%
  
  Unique Products:        {df['barcode'].nunique()}
  Unique Ingredients:     {df['banned_item'].nunique()}
  Unique Brands:          {df['brands'].nunique()}
  
  Needs Verification:     {verification_count}
  
  Output Files:
    - {OUTPUT_CLEAN}
    - {OUTPUT_REMOVED}
    - {OUTPUT_VERIFICATION}
    - {OUTPUT_REPORT}
""")
print("=" * 60)
print("✅ CLEANING PIPELINE COMPLETE")
print("=" * 60)
