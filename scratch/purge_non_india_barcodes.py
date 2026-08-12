import pandas as pd
import os

all_supabase_csv = "all_supabase_products.csv"
confirmed_csv = "india_products_confirmed.csv"
needs_ver_csv = "india_products_needs_verification.csv"

def run():
    print("=== EXECUTING PURGE OF FOREIGN BARCODES NOT SOLD IN INDIA ===")
    
    df_all = pd.read_csv(all_supabase_csv, dtype=str)
    df_confirmed = pd.read_csv(confirmed_csv, dtype=str)
    df_needs_ver = pd.read_csv(needs_ver_csv, dtype=str)

    df_all['barcode'] = df_all['barcode'].str.strip()
    df_confirmed['barcode'] = df_confirmed['barcode'].str.strip()
    df_needs_ver['barcode'] = df_needs_ver['barcode'].str.strip()

    initial_master_count = len(df_all)

    # Collect set of all barcodes present in confirmed or needs_ver Indian database files
    indian_confirmed_barcodes = set(df_confirmed['barcode'].dropna())
    indian_needs_ver_barcodes = set(df_needs_ver['barcode'].dropna())
    valid_indian_market_barcodes = indian_confirmed_barcodes.union(indian_needs_ver_barcodes)

    # Condition to KEEP:
    # 1. Barcode starts with '890' (GS1 India registered)
    # OR
    # 2. Barcode is in valid_indian_market_barcodes (Verified sold in India)
    is_890 = df_all['barcode'].str.startswith('890', na=False)
    is_in_indian_market = df_all['barcode'].isin(valid_indian_market_barcodes)

    keep_condition = is_890 | is_in_indian_market

    df_clean_master = df_all[keep_condition].copy()
    purged_df = df_all[~keep_condition].copy()

    purged_count = len(purged_df)
    final_master_count = len(df_clean_master)

    # Overwrite master CSV with clean Indian database only
    df_clean_master.to_csv(all_supabase_csv, index=False)

    print(f"\nPurge Summary:")
    print(f"  Initial Master Rows: {initial_master_count:,}")
    print(f"  Purged Foreign Non-India Barcodes: {purged_count:,}")
    print(f"  Final Clean Indian Master Database Count: {final_master_count:,}")
    print(f"  GS1 890 India Barcodes Kept: {df_clean_master['barcode'].str.startswith('890', na=False).sum():,}")
    print(f"  Verified Imported Non-890 Barcodes Kept: {(~df_clean_master['barcode'].str.startswith('890', na=False)).sum():,}")

if __name__ == '__main__':
    run()
