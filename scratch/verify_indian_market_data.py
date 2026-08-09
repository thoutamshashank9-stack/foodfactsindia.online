import os
import sys
import pandas as pd
import numpy as np
import re
import json

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"c:\Users\thout\Downloads\check it"

# File paths
all_supabase_path = os.path.join(BASE_DIR, "all_supabase_products.csv")
with_ing_path = os.path.join(BASE_DIR, "products_with_ingredients.csv")
without_ing_path = os.path.join(BASE_DIR, "products_without_ingredients.csv")
banned_clean_path = os.path.join(BASE_DIR, "cleaned_dataset.csv")

print("=== FOODFACTSINDIA DATASET AUDIT & INDIAN MARKET VERIFICATION ===")

# 1. Total Supabase Products & Ingredients Completeness
if os.path.exists(all_supabase_path):
    df_all = pd.read_csv(all_supabase_path, dtype=str)
    print(f"Total Supabase Products Loaded: {len(df_all)}")
    print("Columns:", df_all.columns.tolist())
    
    # Check ingredients completeness
    ing_col = 'ingredients_text' if 'ingredients_text' in df_all.columns else ('ingredient_list_raw' if 'ingredient_list_raw' in df_all.columns else None)
    if not ing_col:
        for col in df_all.columns:
            if 'ingredient' in col.lower():
                ing_col = col
                break
    
    if ing_col:
        df_all['has_ingredients'] = df_all[ing_col].apply(lambda x: pd.notna(x) and str(x).strip() != '' and str(x).strip().lower() != 'nan')
        has_ing_count = df_all['has_ingredients'].sum()
        no_ing_count = len(df_all) - has_ing_count
        print(f"Products WITH complete ingredients: {has_ing_count} ({has_ing_count/len(df_all)*100:.2f}%)")
        print(f"Products WITHOUT ingredients: {no_ing_count} ({no_ing_count/len(df_all)*100:.2f}%)")
else:
    print(f"File {all_supabase_path} not found directly, checking separate files...")

if os.path.exists(with_ing_path) and os.path.exists(without_ing_path):
    df_with = pd.read_csv(with_ing_path, dtype=str)
    df_without = pd.read_csv(without_ing_path, dtype=str)
    print(f"Products with ingredients dataset: {len(df_with)}")
    print(f"Products without ingredients dataset: {len(df_without)}")

# 2. Banned Substances Products Audit & India Barcode / Market Verification
print("\n--- Banned Substances Dataset Audit ---")
if os.path.exists(banned_clean_path):
    df_banned = pd.read_csv(banned_clean_path, dtype=str)
    print(f"Total Banned/Restricted Product Entries: {len(df_banned)}")
    print(f"Unique Barcodes: {df_banned['barcode'].nunique()}")
    
    # GS1 Prefix check for India (890 prefix)
    def check_gs1_country(barcode):
        if pd.isna(barcode):
            return "Unknown"
        b_str = str(barcode).strip()
        if b_str.startswith("890"):
            return "India (GS1 890)"
        elif b_str.startswith("00") or b_str.startswith("01") or b_str.startswith("02") or b_str.startswith("03") or b_str.startswith("04") or b_str.startswith("05") or b_str.startswith("06") or b_str.startswith("07") or b_str.startswith("08") or b_str.startswith("09"):
            return "USA / Canada (GS1 000-099)"
        elif b_str.startswith("50"):
            return "United Kingdom (GS1 500-509)"
        elif b_str.startswith("76"):
            return "Switzerland (GS1 760-769)"
        elif b_str.startswith("40") or b_str.startswith("41") or b_str.startswith("42") or b_str.startswith("43") or b_str.startswith("44"):
            return "Germany (GS1 400-440)"
        elif b_str.startswith("888"):
            return "Singapore (GS1 888)"
        elif b_str.startswith("600"):
            return "South Africa (GS1 600)"
        elif b_str.startswith("93"):
            return "Australia (GS1 930-939)"
        elif b_str.startswith("84"):
            return "Spain (GS1 840-849)"
        elif b_str.startswith("30") or b_str.startswith("31") or b_str.startswith("32") or b_str.startswith("33") or b_str.startswith("34") or b_str.startswith("35") or b_str.startswith("36") or b_str.startswith("37"):
            return "France (GS1 300-379)"
        elif b_str.startswith("49") or b_str.startswith("45"):
            return "Japan (GS1 450-459, 490-499)"
        else:
            return f"International Prefix ({b_str[:3]}...)"

    df_banned['gs1_country'] = df_banned['barcode'].apply(check_gs1_country)
    
    # Brands check: Major brands active and retailed in India
    known_indian_brands = [
        'maggi', 'cadbury', 'oreo', 'nestle', 'nestlé', 'kellogg', "kellogg's", 'snickers', 
        'britannia', 'parle', 'sunfeast', 'lays', "lay's", 'kurkure', 'bingo', 'doritos', 
        'pringles', 'haldiram', 'haldiram\'s', 'bikano', 'amul', 'tata', 'fortune', 
        'kissan', 'mapro', 'chupa chups', 'm&m', "m&m's", 'mars', 'dr. oetker', 'nissin', 
        'top ramen', 'ching\'s', 'ching\'s secret', 'hershey', "hershey's", 'kwality wall\'s',
        'paper boat', 'campa', 'bovonto', 'schweppes', 'coca-cola', 'pepsi', 'sprite', 'fanta',
        'real', 'tropicana', 'b natural', 'frooti', 'maaza', 'slice', 'bournvita', 'horlicks'
    ]
    
    def is_sold_in_india(row):
        brand = str(row.get('brands', '')).lower()
        country = str(row.get('gs1_country', ''))
        product_name = str(row.get('product_name', '')).lower()
        
        # If barcode has GS1 India prefix 890
        if "890" in country:
            return "Yes - Domestic Indian Barcode (GS1 890)"
        
        # If brand is widely retailed in India (domestic or imported SKU sold on Swiggy Instamart/Blinkit/Amazon India/Supermarkets)
        for kib in known_indian_brands:
            if kib in brand or kib in product_name:
                return "Yes - Widely Retailed/Imported Brand in India"
        
        return "International SKU / Imported"

    df_banned['sold_in_india_status'] = df_banned.apply(is_sold_in_india, axis=1)

    print("\n--- GS1 Origin Summary for Banned Product Barcodes ---")
    print(df_banned['gs1_country'].value_counts())

    print("\n--- Indian Availability Verification Status ---")
    print(df_banned['sold_in_india_status'].value_counts())

    # Save enriched detailed report
    output_enriched_path = os.path.join(BASE_DIR, "banned_products_india_verification.csv")
    df_banned.to_csv(output_enriched_path, index=False)
    print(f"\nSaved enriched verification report to: {output_enriched_path}")

