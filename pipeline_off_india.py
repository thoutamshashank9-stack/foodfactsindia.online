# -*- coding: utf-8 -*-
"""
Open Food Facts (OFF) India Pipeline Script
Implements remote/local DuckDB extraction, cleaning, ingredient tokenization with
bracket protection, additive tag extraction, and automated data quality checks.
Enhanced with popular international brands sold in Indian retail markets.
"""

import os
import sys
import re
import pandas as pd
import duckdb

PARQUET_REMOTE_URL = "https://huggingface.co/datasets/openfoodfacts/product-database/resolve/main/food.parquet"
LOCAL_PARQUET = "food.parquet"
CLEAN_PRODUCTS_CSV = "off_india_clean.csv"
INGREDIENTS_CSV = "product_ingredients.csv"
ADDITIVES_CSV = "product_additives.csv"

def run_extraction(parquet_source):
    print(f"\n--- Step 3: Running DuckDB Extraction on '{parquet_source}' ---")
    conn = duckdb.connect()
    
    query = f"""
    COPY (
        SELECT DISTINCT ON (code)
            code AS barcode,
            trim(COALESCE(
                list_filter(product_name, x -> x.lang = 'en')[1].text,
                list_filter(product_name, x -> x.lang = 'main')[1].text,
                product_name[1].text
            )) AS product_name,
            trim(brands) AS brands,
            categories,
            countries_tags,
            lower(trim(COALESCE(
                list_filter(ingredients_text, x -> x.lang = 'en')[1].text,
                list_filter(ingredients_text, x -> x.lang = 'main')[1].text,
                ingredients_text[1].text,
                ingredients
            ))) AS ingredients_text,
            additives_tags,
            allergens_tags,
            try_cast(nova_group AS SMALLINT) AS nova_group,
            try_cast(nutriscore_grade AS VARCHAR) AS nutriscore_grade,
            try_cast(list_filter(nutriments, x -> x.name IN ('energy-kcal', 'energy_100g', 'energy'))[1]."100g" AS DOUBLE) AS energy_100g,
            try_cast(list_filter(nutriments, x -> x.name IN ('sugars', 'sugars_100g'))[1]."100g" AS DOUBLE) AS sugars_100g,
            try_cast(list_filter(nutriments, x -> x.name IN ('fat', 'fat_100g'))[1]."100g" AS DOUBLE) AS fat_100g,
            try_cast(list_filter(nutriments, x -> x.name IN ('saturated-fat', 'saturated_fat_100g'))[1]."100g" AS DOUBLE) AS saturated_fat_100g,
            try_cast(list_filter(nutriments, x -> x.name IN ('trans-fat', 'trans_fat_100g'))[1]."100g" AS DOUBLE) AS trans_fat_100g,
            try_cast(list_filter(nutriments, x -> x.name IN ('proteins', 'proteins_100g', 'protein'))[1]."100g" AS DOUBLE) AS protein_100g,
            try_cast(list_filter(nutriments, x -> x.name IN ('fiber', 'fiber_100g', 'fibre'))[1]."100g" AS DOUBLE) AS fibre_100g,
            try_cast(list_filter(nutriments, x -> x.name IN ('sodium', 'sodium_100g'))[1]."100g" AS DOUBLE) AS sodium_100g,
            try_cast(list_filter(nutriments, x -> x.name IN ('salt', 'salt_100g'))[1]."100g" AS DOUBLE) AS salt_100g
        FROM read_parquet('{parquet_source}')
        WHERE 
            (
                list_contains(countries_tags, 'en:india') 
                OR code LIKE '890%'
                OR lower(brands) SIMILAR TO '.*(red bull|bambino|monster|nutella|ferrero|pringles|toblerone|twix|snickers|mars|bounty|oreo|doritos|lays|heinz|pepsi|coca-cola|kellogg).*'
            )
            AND product_name IS NOT NULL
            AND (
                COALESCE(
                    list_filter(product_name, x -> x.lang = 'en')[1].text,
                    list_filter(product_name, x -> x.lang = 'main')[1].text,
                    product_name[1].text
                ) IS NOT NULL
            )
            AND (
                COALESCE(
                    list_filter(ingredients_text, x -> x.lang = 'en')[1].text,
                    list_filter(ingredients_text, x -> x.lang = 'main')[1].text,
                    ingredients_text[1].text,
                    ingredients
                ) IS NOT NULL
            )
    ) TO '{CLEAN_PRODUCTS_CSV}' (FORMAT CSV, HEADER);
    """
    
    conn.execute(query)
    print(f"Extracted and cleaned product records saved to '{CLEAN_PRODUCTS_CSV}'")

def split_ingredients(text):
    if pd.isna(text):
        return []
    # Protect commas inside brackets/parentheses using ASCII safe placeholder
    depth = 0
    protected = []
    for ch in str(text):
        if ch in '([':
            depth += 1
        elif ch in ')]':
            depth -= 1
        if ch == ',' and depth > 0:
            protected.append('__PCOMMA__')  # ASCII safe placeholder
        else:
            protected.append(ch)
    protected_text = ''.join(protected)
    
    parts = re.split(r',|;', protected_text)
    return [p.replace('__PCOMMA__', ',').strip() for p in parts if p.strip()]

def tokenize_ingredients(df):
    print("\n--- Step 4: Tokenizing Ingredients ---")
    rows = []
    for _, row in df.iterrows():
        barcode = row['barcode']
        ingredients = split_ingredients(row.get('ingredients_text'))
        for pos, ing in enumerate(ingredients):
            rows.append({
                'barcode': barcode,
                'ingredient_raw': ing,
                'position': pos
            })
    
    ing_df = pd.DataFrame(rows)
    ing_df.to_csv(INGREDIENTS_CSV, index=False, encoding='utf-8')
    print(f"Tokenized {len(ing_df)} ingredient items saved to '{INGREDIENTS_CSV}'")
    return ing_df

def clean_additive_tags(tag_str):
    if pd.isna(tag_str):
        return []
    if isinstance(tag_str, str):
        tag_str = tag_str.replace('[', '').replace(']', '').replace("'", "").replace('"', '')
        tags = tag_str.split(',')
    elif isinstance(tag_str, (list, tuple)):
        tags = tag_str
    else:
        return []
    
    return [t.replace('en:', '').strip().upper() for t in tags if t.strip()]

def extract_additives(df):
    print("\n--- Step 5: Extracting & Cleaning Additive Tags ---")
    additive_rows = []
    for _, row in df.iterrows():
        barcode = row['barcode']
        additives = clean_additive_tags(row.get('additives_tags'))
        for tag in additives:
            additive_rows.append({
                'barcode': barcode,
                'additive_code': tag
            })
            
    add_df = pd.DataFrame(additive_rows)
    add_df.to_csv(ADDITIVES_CSV, index=False, encoding='utf-8')
    print(f"Extracted {len(add_df)} additive records saved to '{ADDITIVES_CSV}'")
    return add_df

def run_data_quality_checks(df):
    print("\n--- Step 6: Data Quality Checks & Hygiene ---")
    print(f"Total extracted products: {len(df)}")
    print(f"Duplicate barcodes: {df['barcode'].duplicated().sum()}")
    print(f"Missing product_name: {df['product_name'].isna().sum()}")
    print(f"Missing ingredients_text: {df['ingredients_text'].isna().sum()}")
    
    nutrient_cols = ['sugars_100g', 'fat_100g', 'sodium_100g', 'saturated_fat_100g', 'trans_fat_100g', 'protein_100g', 'fibre_100g', 'salt_100g']
    
    for col in nutrient_cols:
        if col in df.columns:
            over_100 = (df[col] > 100).sum()
            negative = (df[col] < 0).sum()
            if over_100 > 0 or negative > 0:
                print(f"Notice in {col}: {over_100} >100g, {negative} negative values -> setting out-of-range to NaN")
                df.loc[df[col] > 100, col] = None
                df.loc[df[col] < 0, col] = None
    
    # Save cleaned df back to CSV with UTF-8 encoding
    df.to_csv(CLEAN_PRODUCTS_CSV, index=False, encoding='utf-8')
    print(f"Quality check completed and cleaned dataset updated in '{CLEAN_PRODUCTS_CSV}'")

def main():
    source = LOCAL_PARQUET if os.path.exists(LOCAL_PARQUET) else PARQUET_REMOTE_URL
    print(f"Starting OFF India Data Processing Pipeline using source: {source}")
    
    # Step 3: Run DuckDB extraction
    run_extraction(source)
    
    # Load extracted CSV with encoding replacement for robustness
    df = pd.read_csv(CLEAN_PRODUCTS_CSV, encoding='utf-8', encoding_errors='replace')
    
    # Step 4: Tokenize ingredients
    tokenize_ingredients(df)
    
    # Step 5: Clean additives
    extract_additives(df)
    
    # Step 6: Quality checks
    run_data_quality_checks(df)
    
    print("\n========================================================")
    print("Pipeline Execution Completed Successfully!")
    print(f"Generated 3 Ready-to-Load CSVs for Supabase:")
    print(f" 1. Products: {CLEAN_PRODUCTS_CSV}")
    print(f" 2. Ingredients: {INGREDIENTS_CSV}")
    print(f" 3. Additives: {ADDITIVES_CSV}")
    print("========================================================")

if __name__ == '__main__':
    main()
