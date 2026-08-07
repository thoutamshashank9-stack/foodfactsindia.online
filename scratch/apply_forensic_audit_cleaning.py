import os
import sys
import pandas as pd
import re
import json

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"c:\Users\thout\Downloads\check it"
INPUT_CSV = os.path.join(BASE_DIR, "cleaned_dataset.csv")
if not os.path.exists(INPUT_CSV):
    INPUT_CSV = os.path.join(BASE_DIR, "products_containing_banned_substances.csv")

print("=== APPLYING FORENSIC AUDIT CLEANING PIPELINE ===")

df = pd.read_csv(INPUT_CSV, dtype=str)
print(f"Loaded input dataset: {len(df)} entries")

# 1. Standardize Barcode strings
df['barcode'] = df['barcode'].astype(str).str.strip().str.replace(r'\.0$', '', regex=True)

# 2. Identify GS1 890 (India) Barcodes
df['is_gs1_890'] = df['barcode'].str.startswith('890')

# 3. Categorize Additives into Forensic Audit Tiers
qualifying_additives = [
    'TBHQ (E319)',
    'Carmoisine / Azorubine (E122)',
    'Ponceau 4R (E124)',
    'Titanium Dioxide (E171)',
    'Fast Green FCF (E143)'
]

secondary_additives = [
    'Erythrosine (E127)'
]

banned_in_india = [
    'Potassium Bromate (E924A)',
    'Brominated Vegetable Oil (BVO)',
    'Patent Blue V (E131)',
    'Green S (E142)',
    'Brown HT (E155)',
    'Brilliant Black BN (E151)',
    'Quinoline Yellow (E104)'
]

off_scope = [
    'Partially Hydrogenated Oil (PHO)',
    'Azodicarbonamide (E927A)'
]

def classify_additive_tier(item):
    item_str = str(item).strip()
    if item_str in qualifying_additives:
        return 'PRIMARY_QUALIFYING'
    elif item_str in secondary_additives:
        return 'SECONDARY_ERYTHROSINE'
    elif item_str in banned_in_india:
        return 'MUST_REMOVE_BANNED_IN_INDIA'
    elif item_str in off_scope:
        return 'EXCLUDE_OFF_SCOPE'
    else:
        # Check partial string matches
        if 'TBHQ' in item_str: return 'PRIMARY_QUALIFYING'
        if 'Carmoisine' in item_str or 'Azorubine' in item_str: return 'PRIMARY_QUALIFYING'
        if 'Ponceau 4R' in item_str: return 'PRIMARY_QUALIFYING'
        if 'Titanium Dioxide' in item_str: return 'PRIMARY_QUALIFYING'
        if 'Fast Green' in item_str: return 'PRIMARY_QUALIFYING'
        if 'Erythrosine' in item_str: return 'SECONDARY_ERYTHROSINE'
        if 'Bromate' in item_str or 'BVO' in item_str or 'Quinoline' in item_str or 'Patent Blue' in item_str or 'Green S' in item_str or 'Brown HT' in item_str or 'Brilliant Black' in item_str:
            return 'MUST_REMOVE_BANNED_IN_INDIA'
        if 'PHO' in item_str or 'Hydrogenated' in item_str or 'Azodicarbonamide' in item_str:
            return 'EXCLUDE_OFF_SCOPE'
        return 'OTHER'

df['audit_tier'] = df['banned_item'].apply(classify_additive_tier)

# --- FILTERING DATASETS ---

# PRIMARY CLEAN SET: GS1 890 + PRIMARY_QUALIFYING
primary_clean_df = df[df['is_gs1_890'] & (df['audit_tier'] == 'PRIMARY_QUALIFYING')].copy()

# SECONDARY SET: GS1 890 + SECONDARY_ERYTHROSINE
secondary_df = df[df['is_gs1_890'] & (df['audit_tier'] == 'SECONDARY_ERYTHROSINE')].copy()

# TRANS FAT WATCHLIST: GS1 890 + PHO
trans_fat_df = df[df['is_gs1_890'] & (df['banned_item'].str.contains('PHO|Hydrogenated', case=False, na=False))].copy()

# REMOVED / EXCLUDED LOG
removed_df = df[~(df['is_gs1_890'] & (df['audit_tier'].isin(['PRIMARY_QUALIFYING', 'SECONDARY_ERYTHROSINE'])))].copy()

# Add market status to primary clean set
primary_clean_df['indian_market_status'] = 'VERIFIED: GS1 India 890 Barcode'
secondary_df['indian_market_status'] = 'VERIFIED: GS1 India 890 Barcode'

# Save outputs
primary_csv = os.path.join(BASE_DIR, "primary_clean_banned_products_india.csv")
secondary_csv = os.path.join(BASE_DIR, "secondary_erythrosine_products_india.csv")
trans_fat_csv = os.path.join(BASE_DIR, "trans_fat_pho_watchlist_india.csv")
removed_csv = os.path.join(BASE_DIR, "forensic_audit_removed_entries.csv")

primary_clean_df.to_csv(primary_csv, index=False)
secondary_df.to_csv(secondary_csv, index=False)
trans_fat_df.to_csv(trans_fat_csv, index=False)
removed_df.to_csv(removed_csv, index=False)

# Update cleaned_dataset.csv with primary clean set + secondary set for full verified platform use
verified_platform_df = pd.concat([primary_clean_df, secondary_df], ignore_index=True)
verified_platform_df.to_csv(os.path.join(BASE_DIR, "cleaned_dataset.csv"), index=False)

print("\n--- FORENSIC AUDIT CLEANING SUMMARY ---")
print(f"Original Input Rows: {len(df)}")
print(f"🟢 PRIMARY CLEAN SET (GS1 890 + Qualifying Additives): {len(primary_clean_df)} entries ({primary_clean_df['barcode'].nunique()} unique barcodes)")
print(f"🟡 SECONDARY SET (GS1 890 + Erythrosine E127): {len(secondary_df)} entries ({secondary_df['barcode'].nunique()} unique barcodes)")
print(f"🍟 TRANS-FAT WATCHLIST (GS1 890 + PHO): {len(trans_fat_df)} entries")
print(f"❌ TOTAL REMOVED / EXCLUDED: {len(removed_df)} entries")

print("\n--- PRIMARY CLEAN SET ADDITIVE BREAKDOWN ---")
print(primary_clean_df['banned_item'].value_counts())

print("\nSaved files:")
print(f" - {primary_csv}")
print(f" - {secondary_csv}")
print(f" - {trans_fat_csv}")
print(f" - {removed_csv}")
