import urllib.request
import json

def test_barcode(barcode):
    url = f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json"
    print(f"Testing OFF API for GTIN: {barcode}")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "FoodLensAI/2.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            if data.get('status') == 1 and 'product' in data:
                p = data['product']
                print(f"  FOUND PRODUCT!")
                print(f"  Name: {p.get('product_name')}")
                print(f"  Brand: {p.get('brands')}")
                print(f"  Quantity: {p.get('quantity')}")
            else:
                print(f"  Not found in OFF database (Status: {data.get('status')})")
    except Exception as e:
        print(f"  Error: {e}")

if __name__ == '__main__':
    test_barcode("8901063162426")
    test_barcode("5449000000996")
    test_barcode("8901058000012")
