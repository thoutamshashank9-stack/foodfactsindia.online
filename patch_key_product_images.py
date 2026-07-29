import json
import urllib.request

SUPABASE_URL = "https://dempjxsrmnzepxbsnwhg.supabase.co"
ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRlbXBqeHNybW56ZXB4YnNud2hnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODUzMDQ3NzUsImV4cCI6MjEwMDg4MDc3NX0.SO89axui349_3x3zKloLnYD-UGL8vO_p2VR9MCz_xk4"

headers = {
    "apikey": ANON_KEY,
    "Authorization": f"Bearer {ANON_KEY}",
    "Content-Type": "application/json"
}

def patch_product_image(barcode, image_url):
    url = f"{SUPABASE_URL}/rest/v1/products?barcode=eq.{barcode}"
    data = json.dumps({"image_front_url": image_url}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={**headers, "Prefer": "return=minimal"}, method="PATCH")
    try:
        with urllib.request.urlopen(req) as resp:
            print(f"Patched barcode {barcode}: Status {resp.status}")
    except Exception as e:
        print(f"Error patching barcode {barcode}: {e}")

if __name__ == '__main__':
    print("Patching key product images in Supabase database...")
    # Good Day Cashew Biscuit
    patch_product_image("8901063092853", "https://images.openfoodfacts.org/images/products/890/106/309/2853/front_en.4.400.jpg")
    # Red Bull Green Edition
    patch_product_image("90448492", "https://images.openfoodfacts.org/images/products/000/009/044/8492/front_fr.3.400.jpg")
