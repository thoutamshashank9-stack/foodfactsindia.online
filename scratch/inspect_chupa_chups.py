import urllib.request
import json

SUPABASE_URL = "https://dempjxsrmnzepxbsnwhg.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRlbXBqeHNybW56ZXB4YnNud2hnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODUzMDQ3NzUsImV4cCI6MjEwMDg4MDc3NX0.SO89axui349_3x3zKloLnYD-UGL8vO_p2VR9MCz_xk4"

def inspect_chupa_chups():
    # 1. Product row
    url = f"{SUPABASE_URL}/rest/v1/products?barcode=eq.8901393018134&select=*"
    req = urllib.request.Request(url, headers={"apikey": SUPABASE_ANON_KEY, "Authorization": f"Bearer {SUPABASE_ANON_KEY}"})
    with urllib.request.urlopen(req) as resp:
        products = json.loads(resp.read().decode())
        print("Product row:", json.dumps(products, indent=2))

    # 2. Product ingredients
    url_ing = f"{SUPABASE_URL}/rest/v1/product_ingredients?barcode=eq.8901393018134&select=*&order=position.asc"
    req_ing = urllib.request.Request(url_ing, headers={"apikey": SUPABASE_ANON_KEY, "Authorization": f"Bearer {SUPABASE_ANON_KEY}"})
    with urllib.request.urlopen(req_ing) as resp:
        ings = json.loads(resp.read().decode())
        print("Product ingredients rows:", json.dumps(ings, indent=2))

if __name__ == "__main__":
    inspect_chupa_chups()
