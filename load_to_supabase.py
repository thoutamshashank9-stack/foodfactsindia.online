"""
FoodLens Supabase Automated Data Loader Script
Executes DDL schema and loads all 4 CSV datasets into Supabase PostgreSQL database.

Usage:
  Set environment variable SUPABASE_DB_URL or pass connection string:
  python load_to_supabase.py "postgresql://postgres:[YOUR-PASSWORD]@db.dempjxsrmnzepxbsnwhg.supabase.co:5432/postgres"
"""

import sys
import os
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

DEFAULT_PROJECT_REF = "dempjxsrmnzepxbsnwhg"

def get_connection_string():
    if len(sys.argv) > 1:
        return sys.argv[1]
    env_url = os.getenv("SUPABASE_DB_URL")
    if env_url:
        return env_url
    print("Error: No Supabase connection string provided.")
    print("Please set SUPABASE_DB_URL environment variable or pass your database connection string as an argument.")
    print("Example: python load_to_supabase.py \"postgresql://postgres:[YOUR-PASSWORD]@db.dempjxsrmnzepxbsnwhg.supabase.co:5432/postgres\"")
    sys.exit(1)

def run_migration_and_load():
    conn_str = get_connection_string()
    print(f"Connecting to Supabase PostgreSQL database (Project: {DEFAULT_PROJECT_REF})...")
    
    conn = psycopg2.connect(conn_str)
    conn.autocommit = True
    cursor = conn.cursor()
    
    # 1. Execute SQL DDL Schema
    print("\n--- Step 1: Executing DDL Schema (supabase_schema.sql) ---")
    with open("supabase_schema.sql", "r", encoding="utf-8") as f:
        ddl_sql = f.read()
    cursor.execute(ddl_sql)
    print("✓ Tables and indexes created/verified successfully!")

    # 2. Load products
    print("\n--- Step 2: Ingesting products (off_india_clean.csv) ---")
    df_p = pd.read_csv("off_india_clean.csv", encoding="utf-8", encoding_errors="replace")
    df_p = df_p.where(pd.notnull(df_p), None)
    
    p_tuples = [tuple(x) for x in df_p.to_numpy()]
    cols = ", ".join(df_p.columns)
    query_p = f"""
    INSERT INTO public.products ({cols})
    VALUES %s
    ON CONFLICT (barcode) DO UPDATE SET
        product_name = EXCLUDED.product_name,
        brands = EXCLUDED.brands,
        categories = EXCLUDED.categories,
        ingredients_text = EXCLUDED.ingredients_text;
    """
    execute_values(cursor, query_p, p_tuples, page_size=2000)
    print(f"✓ Ingested {len(df_p)} product records into public.products")

    # 3. Load ingredients
    print("\n--- Step 3: Ingesting tokenized ingredients (product_ingredients.csv) ---")
    df_i = pd.read_csv("product_ingredients.csv", encoding="utf-8", encoding_errors="replace")
    i_tuples = [tuple(x) for x in df_i.to_numpy()]
    query_i = "INSERT INTO public.product_ingredients (barcode, ingredient_raw, position) VALUES %s;"
    execute_values(cursor, query_i, i_tuples, page_size=5000)
    print(f"✓ Ingested {len(df_i)} ingredient records into public.product_ingredients")

    # 4. Load additives
    print("\n--- Step 4: Ingesting additive tags (product_additives.csv) ---")
    df_a = pd.read_csv("product_additives.csv", encoding="utf-8", encoding_errors="replace")
    a_tuples = [tuple(x) for x in df_a.to_numpy()]
    query_a = "INSERT INTO public.product_additives (barcode, additive_code) VALUES %s;"
    execute_values(cursor, query_a, a_tuples, page_size=5000)
    print(f"✓ Ingested {len(df_a)} additive records into public.product_additives")

    # 5. Load regulatory rulebook seed
    print("\n--- Step 5: Ingesting Regulatory Rulebook (additive_rulebook_seed.csv) ---")
    df_r = pd.read_csv("additive_rulebook_seed.csv", encoding="utf-8", encoding_errors="replace")
    df_r = df_r.where(pd.notnull(df_r), None)
    r_tuples = [tuple(x) for x in df_r.to_numpy()]
    cols_r = ", ".join(df_r.columns)
    query_r = f"""
    INSERT INTO public.additive_rulebook ({cols_r})
    VALUES %s
    ON CONFLICT (additive_code, jurisdiction) DO UPDATE SET
        status = EXCLUDED.status,
        canonical_name = EXCLUDED.canonical_name,
        label_requirement = EXCLUDED.label_requirement;
    """
    execute_values(cursor, query_r, r_tuples, page_size=1000)
    print(f"✓ Ingested {len(df_r)} rulebook entries into public.additive_rulebook")

    cursor.close()
    conn.close()
    print("\n========================================================")
    print("All 4 Tables Successfully Created & Ingested in Supabase!")
    print("========================================================")

if __name__ == '__main__':
    run_migration_and_load()
