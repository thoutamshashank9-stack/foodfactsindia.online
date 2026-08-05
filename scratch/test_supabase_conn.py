import urllib.request
import json

SUPABASE_URL = "https://dempjxsrmnzepxbsnwhg.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRlbXBqeHNybW56ZXB4YnNud2hnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODUzMDQ3NzUsImV4cCI6MjEwMDg4MDc3NX0.SO89axui349_3x3zKloLnYD-UGL8vO_p2VR9MCz_xk4"

def test_supabase():
    url = f"{SUPABASE_URL}/rest/v1/products?select=count"
    req = urllib.request.Request(url, headers={
        "apikey": SUPABASE_ANON_KEY,
        "Authorization": f"Bearer {SUPABASE_ANON_KEY}"
    })
    try:
        with urllib.request.urlopen(req) as resp:
            print("Status:", resp.status)
            print("Body:", resp.read().decode())
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    test_supabase()
