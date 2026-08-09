import os
import sys
import pandas as pd
import re

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"c:\Users\thout\Downloads\check it"

cleaned_csv = os.path.join(BASE_DIR, "cleaned_dataset.csv")
india_only_csv = os.path.join(BASE_DIR, "india_only_banned_products.csv")

print("=== APPLYING GEOGRAPHIC LOGIC GATE & E142 CORRECTION ===")

df = pd.read_csv(cleaned_csv, dtype=str)
initial_count = len(df)

# List of additives banned in India
india_banned_ingredients = [
    'Brominated Vegetable Oil (BVO)', 
    'Potassium Bromate (E924A)', 
    'Azodicarbonamide (ADA)', 
    'Patent Blue V (E131)', 
    'Brilliant Black BN (E151)', 
    'Brown HT (E155)'
]

def clean_india_bans(row):
    barcode = str(row.get('barcode', '')).strip()
    banned_item = str(row.get('banned_item', '')).strip()
    jurisdictions = str(row.get('banned_in_jurisdictions', '')).strip()
    reason = str(row.get('violation_reason', '')).strip()
    
    # 1. Foreign barcodes (non-890): Suppress 'IN' from banned_in_jurisdictions
    if not barcode.startswith('890'):
        if 'IN' in jurisdictions:
            j_list = [j.strip() for j in jurisdictions.split(',') if j.strip() != 'IN']
            jurisdictions = ', '.join(j_list)
            reason = reason.replace('India (FSSAI 2016), ', '').replace('IN, ', '').replace('Banned in IN', '').strip()
    
    # 2. Green S (E142) correction for 890 barcodes
    if 'Green S' in banned_item or 'E142' in banned_item:
        reason = "Conditionally restricted under FSSAI category limits; Not authorized in EU/UK."
        if barcode.startswith('890'):
            # Change jurisdiction from IN to EU/UK focus
            j_list = [j.strip() for j in jurisdictions.split(',') if j.strip() != 'IN']
            if not j_list: j_list = ['EU', 'UK']
            jurisdictions = ', '.join(j_list)

    row['banned_in_jurisdictions'] = jurisdictions
    row['violation_reason'] = reason
    return row

df = df.apply(clean_india_bans, axis=1)

# Remove any entries whose jurisdictions became empty
df = df[df['banned_in_jurisdictions'].str.strip() != ''].copy()

# Ensure ONLY 890 Indian domestic barcodes remain in primary dataset
df_india_final = df[df['barcode'].astype(str).str.startswith('890')].copy()

# Add market status tag
df_india_final['indian_market_status'] = 'VERIFIED: Domestic Indian Product (GS1 890 Barcode)'

# Save final clean dataset
df_india_final.to_csv(cleaned_csv, index=False)
df_india_final.to_csv(india_only_csv, index=False)
df_india_final.to_csv(os.path.join(BASE_DIR, "products_containing_banned_substances.csv"), index=False)

print("\n--- GEOGRAPHIC LOGIC GATE SUMMARY ---")
print(f"Original Entries: {initial_count}")
print(f"✅ Final Verified Domestic Indian Barcode Entries: {len(df_india_final)} ({df_india_final['barcode'].nunique()} unique Indian 890 barcodes)")
print(f"\nBreakdown by Flagged Additive:")
print(df_india_final['banned_item'].value_counts())

print(f"\nSaved verified datasets to:")
print(f" - {cleaned_csv}")
print(f" - {india_only_csv}")
print(f" - {os.path.join(BASE_DIR, 'products_containing_banned_substances.csv')}")
