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
        elif k == 'ingredient_raw':
            s = str(v)
            d[k] = s[:1500] if len(s) > 1500 else s
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
        print(f"Error posting batch:", e)
        return None

def main():
    print("Completing remaining ingredients batch load...")
    df = pd.read_csv("product_ingredients.csv", encoding="utf-8", encoding_errors="replace")
    total = len(df)
    BATCH_SIZE = 1000
    for i in range(95000, 101000, BATCH_SIZE):
        chunk = [clean_row_generic(r) for r in df.iloc[i:i+BATCH_SIZE].to_dict(orient="records")]
        status = post_batch("product_ingredients", chunk)
        print(f"  Batch {i}/{total}: status {status}")

if __name__ == '__main__':
    main()
