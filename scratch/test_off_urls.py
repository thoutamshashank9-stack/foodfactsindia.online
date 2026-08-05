import urllib.request

urls = [
    "https://static.openfoodfacts.org/data/taxonomies/additives.json",
    "https://world.openfoodfacts.org/data/taxonomies/additives.json",
    "https://raw.githubusercontent.com/openfoodfacts/openfoodfacts-server/main/taxonomies/additives/additives.json",
    "https://raw.githubusercontent.com/openfoodfacts/openfoodfacts-server/main/taxonomies/additives.full.json"
]

for url in urls:
    req = urllib.request.Request(url, headers={"User-Agent": "FoodFactsIndia-IngestionEngine/1.0"})
    try:
        with urllib.request.urlopen(req) as resp:
            print(f"URL: {url} -> Status {resp.status}, Bytes: {len(resp.read())}")
    except Exception as e:
        print(f"URL: {url} -> Error: {e}")
