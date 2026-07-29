import json
import urllib.request

SUPABASE_URL = "https://dempjxsrmnzepxbsnwhg.supabase.co"
ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRlbXBqeHNybW56ZXB4YnNud2hnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODUzMDQ3NzUsImV4cCI6MjEwMDg4MDc3NX0.SO89axui349_3x3zKloLnYD-UGL8vO_p2VR9MCz_xk4"

headers = {
    "apikey": ANON_KEY,
    "Authorization": f"Bearer {ANON_KEY}",
    "Content-Type": "application/json"
}

def fetch_json(endpoint):
    url = f"{SUPABASE_URL}/rest/v1/{endpoint}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode('utf-8'))

def test_image_url(url):
    if not url: return False
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}, method="HEAD")
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.status == 200
    except Exception as e:
        return False

def check_images():
    print("=== CHECKING PRODUCT IMAGE URLS IN DATABASE & OFF CDN ===")

    demo_products = [
        ("4901488010320", "Amul Butter"),
        ("8901063162426", "Marie Gold"),
        ("8901063092853", "Britannia Good Day"),
        ("90448492", "Red Bull Green Edition"),
        ("8901058000596", "Maggi Noodles"),
        ("5449000000996", "Coca-Cola Original")
    ]

    for code, name in demo_products:
        p = fetch_json(f"products?barcode=eq.{code}")
        img = p[0].get('image_front_url') if p else None
        is_ok = test_image_url(img) if img else False
        print(f"Product: {name:<22} | Barcode: {code:<14} | Accessible: {is_ok} | URL: {img}")

if __name__ == '__main__':
    check_images()
