"""
Task 3: Ingest Open Food Facts raw ingredients taxonomy.
Saves src/data/raw_ingredients_taxonomy.json (~6,800 clean EN entries).
"""
import json, urllib.request, os, sys

OFF_URL = "https://static.openfoodfacts.org/data/taxonomies/ingredients.json"
OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "src", "data", "raw_ingredients_taxonomy.json")

def run():
    print("Downloading Open Food Facts ingredients taxonomy …")
    req = urllib.request.Request(OFF_URL, headers={"User-Agent": "FoodFactsIndia/2.0"})
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            raw = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"Download failed: {e}")
        sys.exit(1)

    print(f"  Fetched {len(raw)} taxonomy nodes.")
    clean: dict = {}

    for key, val in raw.items():
        if not isinstance(val, dict):
            continue
        name_obj = val.get("name", {})
        primary = None
        if isinstance(name_obj, dict):
            primary = name_obj.get("en")
        elif isinstance(name_obj, str):
            primary = name_obj

        if not primary or len(primary) < 2:
            continue

        # Skip entries that are just E-numbers (handled by global_additives_master)
        if primary.lower().startswith("e") and primary[1:].isdigit():
            continue

        clean_key = key.replace("en:", "").strip().lower()
        synonyms: list[str] = []
        if isinstance(name_obj, dict):
            synonyms = [v for v in name_obj.values() if isinstance(v, str) and len(v) > 1]

        clean[clean_key] = {
            "id": f"ing_raw_{clean_key.replace(' ', '_')[:48]}",
            "canonical_name": primary,
            "category": "WHOLE_FOOD",
            "synonyms": list(set(synonyms))[:20]  # cap to 20 to keep file slim
        }

    print(f"  Kept {len(clean)} clean whole-food entries.")
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(clean, f, ensure_ascii=False, separators=(",", ":"))

    size_kb = os.path.getsize(OUT_PATH) // 1024
    print(f"  Saved → {OUT_PATH} ({size_kb} KB)")

if __name__ == "__main__":
    run()
