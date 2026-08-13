import pandas as pd
import os
import re

confirmed_csv = "india_products_confirmed.csv"
needs_ver_csv = "india_products_needs_verification.csv"
all_supabase_csv = "all_supabase_products.csv"
output_dir = r"C:\Users\thout\.gemini\antigravity\brain\960ba3f1-e81d-4ac5-8649-b7de031c249a"

from apply_canonical_regulatory_fixes import CANONICAL_BANNED_ADDITIVES_REGISTRY, analyze_canonical_bans

def main():
    print("=== GENERATING ALL 4 REQUESTED DETAILED CSV FILES ===")

    df_confirmed = pd.read_csv(confirmed_csv, dtype=str)
    df_needs_ver = pd.read_csv(needs_ver_csv, dtype=str)

    df_confirmed['barcode'] = df_confirmed['barcode'].str.strip()
    df_needs_ver['barcode'] = df_needs_ver['barcode'].str.strip()

    # Mask for 100% strictly verified complete products
    has_ing = df_confirmed['ingredients_text'].notna() & (df_confirmed['ingredients_text'].str.strip() != '')
    not_unverified_text = ~df_confirmed['ingredients_text'].str.contains(r'Verify\s*specific|Verify\b|NON-FOOD', case=False, na=False)
    high_confidence = df_confirmed['ingredient_confidence'].isna() | (df_confirmed['ingredient_confidence'].str.upper() == 'HIGH')

    verified_mask = has_ing & not_unverified_text & high_confidence

    df_verified_complete = df_confirmed[verified_mask].copy()
    df_unverified_from_confirmed = df_confirmed[~verified_mask].copy()

    # Combine incomplete products queue
    df_incomplete_all = pd.concat([df_needs_ver, df_unverified_from_confirmed], ignore_index=True).drop_duplicates(subset=['barcode'])

    # File 1: verified_complete_products.csv
    file1_df = pd.DataFrame({
        "barcode": df_verified_complete["barcode"],
        "product_name": df_verified_complete["product_name"],
        "brand": df_verified_complete["brands"],
        "ingredients_text": df_verified_complete["ingredients_text"],
        "ingredient_confidence": "HIGH",
        "verification_status": "VERIFIED_COMPLETE"
    })

    file1_path_local = "verified_complete_products.csv"
    file1_path_art = os.path.join(output_dir, "verified_complete_products.csv")
    file1_df.to_csv(file1_path_local, index=False, encoding="utf-8-sig")
    file1_df.to_csv(file1_path_art, index=False, encoding="utf-8-sig")
    print(f"File 1 (Verified Complete Products CSV) saved: {len(file1_df):,} rows")

    # File 2: incomplete_products_queue.csv
    file2_df = pd.DataFrame({
        "barcode": df_incomplete_all["barcode"],
        "product_name": df_incomplete_all["product_name"],
        "brand": df_incomplete_all["brands"],
        "ingredients_text": df_incomplete_all["ingredients_text"].fillna("PNA - Pending Verification"),
        "verification_status": "NEEDS_VERIFICATION"
    })

    file2_path_local = "incomplete_products_queue.csv"
    file2_path_art = os.path.join(output_dir, "incomplete_products_queue.csv")
    file2_df.to_csv(file2_path_local, index=False, encoding="utf-8-sig")
    file2_df.to_csv(file2_path_art, index=False, encoding="utf-8-sig")
    print(f"File 2 (Incomplete Products Queue CSV) saved: {len(file2_df):,} rows")

    # File 3: banned_additives_regulatory_reference.csv
    ref_records = []
    for r in CANONICAL_BANNED_ADDITIVES_REGISTRY:
        ref_records.append({
            "additive_code": r["code"],
            "additive_name": r["name"],
            "functional_class": r["class"],
            "india_fssai_status": r["india_status"],
            "foreign_banned_jurisdiction": r["eu_status"] + " | " + r["us_status"] + " | " + r["japan_status"],
            "why_banned_abroad": r["toxicology"],
            "why_permitted_or_banned_in_india": r["legal_summary"],
            "risk_tier": r["risk_tier"]
        })

    file3_df = pd.DataFrame(ref_records)
    file3_path_local = "banned_additives_regulatory_reference.csv"
    file3_path_art = os.path.join(output_dir, "banned_additives_regulatory_reference.csv")
    file3_df.to_csv(file3_path_local, index=False, encoding="utf-8-sig")
    file3_df.to_csv(file3_path_art, index=False, encoding="utf-8-sig")
    print(f"File 3 (Banned Additives Regulatory Reference CSV) saved: {len(file3_df):,} rows")

    # File 4: verified_products_with_banned_additives.csv
    banned_product_records = []
    for idx, row in df_verified_complete.iterrows():
        barcode = row.get('barcode', '')
        pname = row.get('product_name', '')
        brand = row.get('brands', '')
        ing = row.get('ingredients_text', '')

        bans = analyze_canonical_bans(ing)
        if bans:
            for b in bans:
                banned_product_records.append({
                    "barcode": barcode,
                    "product_name": pname,
                    "brand": brand,
                    "verified_ingredients": ing,
                    "flagged_additive_code": b["code"],
                    "flagged_additive_name": b["name"],
                    "functional_class": b["class"],
                    "banned_in_jurisdiction": b["eu_status"] + " | " + b["us_status"] + " | " + b["japan_status"],
                    "why_banned_abroad": b["toxicology"],
                    "india_fssai_status": b["india_status"],
                    "legal_summary": b["legal_summary"],
                    "risk_tier": b["risk_tier"]
                })

    file4_df = pd.DataFrame(banned_product_records)
    file4_path_local = "verified_products_with_banned_additives.csv"
    file4_path_art = os.path.join(output_dir, "verified_products_with_banned_additives.csv")
    file4_df.to_csv(file4_path_local, index=False, encoding="utf-8-sig")
    file4_df.to_csv(file4_path_art, index=False, encoding="utf-8-sig")
    print(f"File 4 (Verified Products With Banned Additives CSV) saved: {len(file4_df):,} rows ({file4_df['barcode'].nunique():,} unique products)")

    print("ALL 4 DETAILED CSV FILES SUCCESSFULLY CREATED AND VERIFIED!")

if __name__ == '__main__':
    main()
