import os
import sys
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"c:\Users\thout\Downloads\check it"

confirmed_path = os.path.join(BASE_DIR, "india_products_confirmed.csv")
needs_ver_path = os.path.join(BASE_DIR, "india_products_needs_verification.csv")
removed_path = os.path.join(BASE_DIR, "foreign_or_invalid_products_removed.csv")

df_c = pd.read_csv(confirmed_path, dtype=str)
df_nv = pd.read_csv(needs_ver_path, dtype=str)
df_rem = pd.read_csv(removed_path, dtype=str)

df_c['barcode'] = df_c['barcode'].str.strip()
df_nv['barcode'] = df_nv['barcode'].str.strip()
df_rem['barcode'] = df_rem['barcode'].str.strip()

rem_barcodes = set(df_rem['barcode'].dropna().tolist())
c_barcodes = set(df_c['barcode'].dropna().tolist())
nv_barcodes = set(df_nv['barcode'].dropna().tolist())

# Check overlap
overlap_c = c_barcodes.intersection(rem_barcodes)
overlap_nv = nv_barcodes.intersection(rem_barcodes)

print(f"Overlap with confirmed: {len(overlap_c)}")
print(f"Overlap with needs_verification: {len(overlap_nv)}")

if len(overlap_c) > 0:
    df_c = df_c[~df_c['barcode'].isin(overlap_c)]
    print(f"Removed {len(overlap_c)} overlapping rows from confirmed.")

if len(overlap_nv) > 0:
    df_nv = df_nv[~df_nv['barcode'].isin(overlap_nv)]
    print(f"Removed {len(overlap_nv)} overlapping rows from needs_verification.")

# Write back if changed
if len(overlap_c) > 0 or len(overlap_nv) > 0:
    df_c.to_csv(confirmed_path, index=False)
    df_nv.to_csv(needs_ver_path, index=False)
    print("Saved clean database files.")

# Generate incomplete products data list
df_incomplete = df_nv.copy()
incomplete_path = os.path.join(BASE_DIR, "incomplete_products_list.csv")
df_incomplete.to_csv(incomplete_path, index=False)
print(f"Saved {len(df_incomplete)} incomplete products to {incomplete_path}")
