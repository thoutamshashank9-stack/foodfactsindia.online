import pandas as pd
import json
import os
import re

confirmed_csv = "india_products_confirmed.csv"
output_dir = r"C:\Users\thout\.gemini\antigravity\brain\960ba3f1-e81d-4ac5-8649-b7de031c249a"

from generate_user_requested_reports import BANNED_ADDITIVES_RULES, analyze_banned_additives

def run():
    print("=== STRICT VERIFIED-ONLY FILTERING FOR FOREIGN-BANNED ADDITIVES CATALOG ===")
    
    df_confirmed = pd.read_csv(confirmed_csv, dtype=str)
    df_confirmed['barcode'] = df_confirmed['barcode'].str.strip()

    print(f"Total rows in confirmed database: {len(df_confirmed)}")

    # Filter strictly for VERIFIED products:
    # 1. ingredients_text is present, not null, not empty
    # 2. ingredients_text does NOT contain 'Verify' or 'Verify specific product' or 'NON-FOOD'
    # 3. ingredient_confidence is 'HIGH' (if present)
    
    has_ing = df_confirmed['ingredients_text'].notna() & (df_confirmed['ingredients_text'].str.strip() != '')
    not_unverified_text = ~df_confirmed['ingredients_text'].str.contains(r'Verify\s*specific|Verify\b|NON-FOOD', case=False, na=False)
    high_confidence = df_confirmed['ingredient_confidence'].isna() | (df_confirmed['ingredient_confidence'].str.upper() == 'HIGH')

    verified_mask = has_ing & not_unverified_text & high_confidence
    df_strictly_verified = df_confirmed[verified_mask].copy()

    unverified_removed_count = len(df_confirmed) - len(df_strictly_verified)
    print(f"Strictly Verified Food Products Count: {len(df_strictly_verified)}")
    print(f"Unverified / Generic Items Filtered Out: {unverified_removed_count}")

    # Now run banned additive scan strictly over df_strictly_verified
    banned_products = []
    for idx, row in df_strictly_verified.iterrows():
        barcode = row.get('barcode', '')
        pname = row.get('product_name', '')
        brand = row.get('brands', '')
        ing = row.get('ingredients_text', '')

        bans = analyze_banned_additives(ing)
        if bans:
            highest_risk = "🟢 Low Concern"
            if any(b["risk_tier"] == "🔴 High Concern" for b in bans):
                highest_risk = "🔴 High Concern"
            elif any(b["risk_tier"] == "🟡 Moderate Concern" for b in bans):
                highest_risk = "🟡 Moderate Concern"

            for b in bans:
                banned_products.append({
                    "barcode": barcode,
                    "product_name": pname,
                    "brand": brand,
                    "ingredients_text": ing,
                    "additive_code": b["code"],
                    "additive_name": b["name"],
                    "jurisdiction": b["jurisdiction"],
                    "ban_reason": b["reason"],
                    "additive_risk_tier": b["risk_tier"],
                    "product_overall_risk": highest_risk
                })

    df_banned = pd.DataFrame(banned_products)
    unique_banned_barcodes = df_banned['barcode'].nunique() if len(df_banned) > 0 else 0
    print(f"\nFinal Verified Foreign-Banned Additive Products Count: {unique_banned_barcodes}")
    print(f"Total Banned Additive Matches: {len(df_banned)}")

    high_risk_count = df_banned[df_banned['additive_risk_tier'] == '🔴 High Concern']['barcode'].nunique()
    mod_risk_count = df_banned[df_banned['additive_risk_tier'] == '🟡 Moderate Concern']['barcode'].nunique()

    print(f"  🔴 High Concern Verified Banned Products: {high_risk_count}")
    print(f"  🟡 Moderate Concern Verified Banned Products: {mod_risk_count}")

    # Save cleaned CSV
    df_banned.to_csv(os.path.join(output_dir, "foreign_banned_additives_full_report.csv"), index=False)

if __name__ == '__main__':
    run()
