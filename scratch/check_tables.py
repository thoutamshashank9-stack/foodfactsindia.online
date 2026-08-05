import urllib.request

SUPABASE_URL = "https://dempjxsrmnzepxbsnwhg.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRlbXBqeHNybW56ZXB4YnNud2hnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODUzMDQ3NzUsImV4cCI6MjEwMDg4MDc3NX0.SO89axui349_3x3zKloLnYD-UGL8vO_p2VR9MCz_xk4"

def check_table(name):
    url = f"{SUPABASE_URL}/rest/v1/{name}?select=count"
    req = urllib.request.Request(url, headers={
        "apikey": SUPABASE_ANON_KEY,
        "Authorization": f"Bearer {SUPABASE_ANON_KEY}"
    })
    try:
        with urllib.request.urlopen(req) as resp:
            print(f"Table '{name}': Exists (Status {resp.status})")
    except Exception as e:
        print(f"Table '{name}': Not found ({e})")

if __name__ == "__main__":
    check_table("canonical_additives")
    check_table("additive_synonyms")
    check_table("regulatory_bans")
    check_table("additive_reference")
