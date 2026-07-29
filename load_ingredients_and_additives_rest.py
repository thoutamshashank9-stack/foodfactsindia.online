import json
import urllib.request
import pandas as pd

SUPABASE_URL = "https://dempjxsrmnzepxbsnwhg.supabase.co"
ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRlbXBqeHNybW56ZXB4YnNud2hnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODUzMDQ3NzUsImV4cCI6MjEwMDg4MDc3NX0.SO89axui349_3x3zKloLnYD-UGL8vO_p2VR9MCz_xk4"

headers = {
    "apikey": ANON_KEY,
    "Authorization": f"Bearer {ANON_KEY}",
    "Content-Type": "application/json",
    "Prefer": "resolution=merge-duplicates"
}

def post_batch(endpoint, data):
    url = f"{SUPABASE_URL}/rest/v1/{endpoint}"
    req = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status
    except Exception as e:
        print(f"Error posting to {endpoint}:", e)
        return None

def load_ingredients():
    print("\nIngesting product_ingredients.csv into Supabase...")
    df = pd.read_csv("product_ingredients.csv", encoding="utf-8", encoding_errors="replace")
    df = df.where(pd.notnull(df), None)
    total = len(df)
    BATCH_SIZE = 2000
    for i in range(0, total, BATCH_SIZE):
        chunk = df.iloc[i:i+BATCH_SIZE].to_dict(orient="records")
        status = post_batch("product_ingredients", chunk)
        print(f"  Ingredients batch {i}/{total}: status {status}")

def load_additives():
    print("\nIngesting product_additives.csv into Supabase...")
    df = pd.read_csv("product_additives.csv", encoding="utf-8", encoding_errors="replace")
    df = df.where(pd.notnull(df), None)
    total = len(df)
    BATCH_SIZE = 2000
    for i in range(0, total, BATCH_SIZE):
        chunk = df.iloc[i:i+BATCH_SIZE].to_dict(orient="records")
        status = post_batch("product_additives", chunk)
        print(f"  Additives batch {i}/{total}: status {status}")

if __name__ == '__main__':
    load_additives()
    load_ingredients()
