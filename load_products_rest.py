import glob
import json
import urllib.request
import pandas as pd

# Supabase REST API Endpoint & Keys obtained from MCP server
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

# Load products
print("Ingesting products into Supabase REST API...")
df_p = pd.read_csv("off_india_clean.csv", encoding="utf-8", encoding_errors="replace")
df_p = df_p.where(pd.notnull(df_p), None)

BATCH_SIZE = 500
total_p = len(df_p)

for i in range(0, total_p, BATCH_SIZE):
    chunk = df_p.iloc[i:i+BATCH_SIZE].to_dict(orient="records")
    status = post_batch("products", chunk)
    print(f"  Products batch {i}/{total_p}: status {status}")

print("Products ingestion completed!")
