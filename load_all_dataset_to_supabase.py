import json
import urllib.request
import pandas as pd
import time

SUPABASE_URL = "https://dempjxsrmnzepxbsnwhg.supabase.co"
ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRlbXBqeHNybW56ZXB4YnNud2hnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODUzMDQ3NzUsImV4cCI6MjEwMDg4MDc3NX0.SO89axui349_3x3zKloLnYD-UGL8vO_p2VR9MCz_xk4"

headers = {
    "apikey": ANON_KEY,
    "Authorization": f"Bearer {ANON_KEY}",
    "Content-Type": "application/json",
    "Prefer": "resolution=merge-duplicates"
}

def clean_product_row(row):
    d = {}
    for k, v in row.items():
        if pd.isna(v) or v is None:
            d[k] = None
        elif k == 'nova_group':
            try:
                d[k] = int(float(v))
            except:
                d[k] = None
        elif k in ['energy_100g', 'sugars_100g', 'fat_100g', 'saturated_fat_100g', 'trans_fat_100g', 'protein_100g', 'fibre_100g', 'sodium_100g', 'salt_100g']:
            try:
                d[k] = float(v)
            except:
                d[k] = None
        else:
            d[k] = str(v)
    return d

def clean_row_generic(row):
    d = {}
    for k, v in row.items():
        if pd.isna(v) or v is None:
            d[k] = None
        elif k == 'position':
            try:
                d[k] = int(float(v))
            except:
                d[k] = 0
        else:
            d[k] = str(v)
    return d

def post_batch(endpoint, data):
    url = f"{SUPABASE_URL}/rest/v1/{endpoint}"
    payload = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status
    except Exception as e:
        if hasattr(e, 'read'):
            print(f"Error posting to {endpoint}:", e, e.read().decode('utf-8', 'replace')[:150])
        else:
            print(f"Error posting to {endpoint}:", e)
        return None

def load_products():
    print("\n--- 1. Ingesting products into public.products ---")
    df = pd.read_csv("off_india_clean.csv", encoding="utf-8", encoding_errors="replace")
    total = len(df)
    BATCH_SIZE = 500
    for i in range(0, total, BATCH_SIZE):
        chunk = [clean_product_row(r) for r in df.iloc[i:i+BATCH_SIZE].to_dict(orient="records")]
        status = post_batch("products", chunk)
        print(f"  Products batch {i}/{total}: status {status}")

def load_additives():
    print("\n--- 2. Ingesting product_additives.csv into public.product_additives ---")
    df = pd.read_csv("product_additives.csv", encoding="utf-8", encoding_errors="replace")
    total = len(df)
    BATCH_SIZE = 1000
    for i in range(0, total, BATCH_SIZE):
        chunk = [clean_row_generic(r) for r in df.iloc[i:i+BATCH_SIZE].to_dict(orient="records")]
        status = post_batch("product_additives", chunk)
        print(f"  Additives batch {i}/{total}: status {status}")

def load_ingredients():
    print("\n--- 3. Ingesting product_ingredients.csv into public.product_ingredients ---")
    df = pd.read_csv("product_ingredients.csv", encoding="utf-8", encoding_errors="replace")
    total = len(df)
    BATCH_SIZE = 1000
    for i in range(0, total, BATCH_SIZE):
        chunk = [clean_row_generic(r) for r in df.iloc[i:i+BATCH_SIZE].to_dict(orient="records")]
        status = post_batch("product_ingredients", chunk)
        print(f"  Ingredients batch {i}/{total}: status {status}")

if __name__ == '__main__':
    load_products()
    load_additives()
    load_ingredients()
    print("\n✓ Full dataset ingestion finished!")
