import urllib.request
import json

SUPABASE_URL = "https://dempjxsrmnzepxbsnwhg.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRlbXBqeHNybW56ZXB4YnNud2hnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODUzMDQ3NzUsImV4cCI6MjEwMDg4MDc3NX0.SO89axui349_3x3zKloLnYD-UGL8vO_p2VR9MCz_xk4"

def update_chupa_chups():
    url = f"{SUPABASE_URL}/rest/v1/products?barcode=eq.8901393018134"
    payload = json.dumps({
        "sugars_100g": 65.0,
        "saturated_fat_100g": 2.0,
        "sodium_100g": 40.0,
        "salt_100g": 0.1
    }).encode("utf-8")

    req = urllib.request.Request(url, data=payload, method="PATCH", headers={
        "apikey": SUPABASE_ANON_KEY,
        "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    })

    try:
        with urllib.request.urlopen(req) as resp:
            print("Status:", resp.status)
            print("Response:", resp.read().decode())
    except Exception as e:
        print("Error updating database:", e)

if __name__ == "__main__":
    update_chupa_chups()
