import urllib.request
import json

SUPABASE_URL = "https://dempjxsrmnzepxbsnwhg.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRlbXBqeHNybW56ZXB4YnNud2hnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODUzMDQ3NzUsImV4cCI6MjEwMDg4MDc3NX0.SO89axui349_3x3zKloLnYD-UGL8vO_p2VR9MCz_xk4"

def update_chupa_chups_ingredients():
    # Delete old noisy rows for barcode 8901393018134
    del_url = f"{SUPABASE_URL}/rest/v1/product_ingredients?barcode=eq.8901393018134"
    req_del = urllib.request.Request(del_url, method="DELETE", headers={
        "apikey": SUPABASE_ANON_KEY,
        "Authorization": f"Bearer {SUPABASE_ANON_KEY}"
    })
    try:
        with urllib.request.urlopen(req_del) as resp:
            print("Deleted old rows:", resp.status)
    except Exception as e:
        print("Error deleting old rows:", e)

    # Insert clean tokenized ingredient rows
    clean_rows = [
        {"barcode": "8901393018134", "position": 0, "ingredient_raw": "Liquid Glucose"},
        {"barcode": "8901393018134", "position": 1, "ingredient_raw": "Sugar"},
        {"barcode": "8901393018134", "position": 2, "ingredient_raw": "Refined Wheat Flour (Maida)"},
        {"barcode": "8901393018134", "position": 3, "ingredient_raw": "Invert Sugar"},
        {"barcode": "8901393018134", "position": 4, "ingredient_raw": "Hydrogenated Vegetable Oil"},
        {"barcode": "8901393018134", "position": 5, "ingredient_raw": "Acidity Regulators (INS 296, INS 330)"},
        {"barcode": "8901393018134", "position": 6, "ingredient_raw": "Synthetic Food Colours (INS 102, INS 110, INS 122, INS 133)"},
        {"barcode": "8901393018134", "position": 7, "ingredient_raw": "Nature-Identical Flavouring Substances (Mixed Fruit)"}
    ]

    ins_url = f"{SUPABASE_URL}/rest/v1/product_ingredients"
    payload = json.dumps(clean_rows).encode("utf-8")
    req_ins = urllib.request.Request(ins_url, data=payload, method="POST", headers={
        "apikey": SUPABASE_ANON_KEY,
        "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    })

    try:
        with urllib.request.urlopen(req_ins) as resp:
            print("Inserted clean ingredient rows:", resp.status)
            print("Response:", resp.read().decode())
    except Exception as e:
        print("Error inserting clean rows:", e)

if __name__ == "__main__":
    update_chupa_chups_ingredients()
