import os
import sys
import json
import urllib.request
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

SUPABASE_URL = "https://dempjxsrmnzepxbsnwhg.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRlbXBqeHNybW56ZXB4YnNud2hnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODUzMDQ3NzUsImV4cCI6MjEwMDg4MDc3NX0.SO89axui349_3x3zKloLnYD-UGL8vO_p2VR9MCz_xk4"

def get_optimized_off_image_url(barcode, size=200, lang='en'):
  if not barcode or not isinstance(barcode, str):
    return None
  clean = barcode.strip()
  if len(clean) < 8:
    return None
  
  code_str = clean.zfill(13) if len(clean) < 13 else clean
  p1 = code_str[:3]
  p2 = code_str[3:6]
  p3 = code_str[6:9]
  p4 = code_str[9:]
  
  size_suffix = '' if size == 'full' else f".{size}"
  return f"https://images.openfoodfacts.org/images/products/{p1}/{p2}/{p3}/{p4}/front_{lang}{size_suffix}.jpg"

def main():
  print("Pre-calculating optimized 200px and 400px OFF Image URLs for products...")
  
  # Fetch barcodes
  url = f"{SUPABASE_URL}/rest/v1/products?select=barcode,product_name,image_front_url"
  headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}"
  }
  
  req = urllib.request.Request(url, headers=headers)
  try:
    with urllib.request.urlopen(req) as resp:
      products = json.loads(resp.read().decode('utf-8'))
      print(f"Total products fetched: {len(products)}")
      
      sample_updates = []
      for p in products[:10]:
        bc = p.get('barcode')
        name = p.get('product_name')
        img_200 = get_optimized_off_image_url(bc, 200)
        img_400 = get_optimized_off_image_url(bc, 400)
        sample_updates.append({
          "barcode": bc,
          "name": name,
          "image_url_200": img_200,
          "image_url_400": img_400
        })
      
      print("\nSample Pre-Calculated OFF Image URLs:")
      print(json.dumps(sample_updates, indent=2))
      
  except Exception as e:
    print(f"Error: {e}")

if __name__ == "__main__":
  main()
