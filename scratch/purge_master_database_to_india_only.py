import os
import sys
import pandas as pd
import re

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"c:\Users\thout\Downloads\check it"

all_supabase_csv = os.path.join(BASE_DIR, "all_supabase_products.csv")
removed_csv = os.path.join(BASE_DIR, "foreign_or_invalid_products_removed.csv")

print("=== EXECUTING MASTER DATABASE PURGE (INDIA FOOD PRODUCTS ONLY) ===")

df_all = pd.read_csv(all_supabase_csv, dtype=str)
initial_count = len(df_all)
print(f"Initial raw master database count: {initial_count}")

# 1. Strict GS1 India Barcode Filter
def is_valid_india_barcode(barcode):
    if pd.isna(barcode): return False
    b = str(barcode).strip()
    return bool(re.match(r'^890\d{10}$', b)) or b.startswith('890')

df_all['is_india_barcode'] = df_all['barcode'].apply(is_valid_india_barcode)

df_india = df_all[df_all['is_india_barcode']].copy()
df_foreign = df_all[~df_all['is_india_barcode']].copy()

# 2. Non-Food & Invalid Nonsense Filter
nonsense_keywords = [
    'undefined', 'roomspraymy', 'the indian cooking instructions methods',
    'the provided text does not contain an ingredient list', 'us(mg) nesium',
    'fat,protein,carbohydrate', 'biscuit 🍪', 'mufbmuvcvyv', '50gr'
]

non_food_keywords = [
    'chiffon', 'fabric', 'shampoo', 'soap', 'diaper', 'lotion', 'cream', 
    'serum', 'mask', 'wash', 'detergent', 'plastic', 'bucket', 'marker',
    'cloth', 'rag', 'un chiffon', 'tissues', 'wipes', 'sanitizer', 'cleaner',
    'kamagra','apcalis','luvagra','lisnop','seclo','panzim','novaten','tadix',
    'zeagra','dolozox','cetirizine','relispray','soventus','entofoam','jhandu','zandu',
    'kottakkal','koflet','qur-derm','cobra 150','eno','vaseline','lakme','ponds',
    'johnson','dettol','lifebuoy','fogg','parachute','nish hair','nisha','vicco','clinic plus',
    'modicare','body oil','miss mimi','manjan','biotique','camlin','libreta',
    'dr. fixit','hicks','fresh one','hygienic','dog soap','chappi','pet safa','diapers',
    'pediasure','pedia sure','nepro','poshan','whisky','seagram'
]

def is_invalid_or_non_food(row):
    pname = str(row.get('product_name', '')).strip().lower()
    brand = str(row.get('brands', '')).strip().lower()
    cat = str(row.get('categories', '')).strip().lower()
    ing = str(row.get('ingredients_text', '') or row.get('ingredient_list_raw', '')).strip().lower()
    
    if not pname or pname in ['nan', 'none', 'null', 'undefined', 'unknown product', 'loading...'] or re.match(r'^\d+$', pname):
        return True
    if len(pname) < 2 or re.match(r'^[bcdfghjklmnpqrstvwxyz]+$', pname):
        return True
    for kw in nonsense_keywords:
        if kw in ing: return True
    for kw in non_food_keywords:
        if kw in pname or kw in brand or kw in cat: return True
    return False

df_india['is_invalid_or_non_food'] = df_india.apply(is_invalid_or_non_food, axis=1)

df_clean_india = df_india[~df_india['is_invalid_or_non_food']].copy()
df_india_invalid = df_india[df_india['is_invalid_or_non_food']].copy()

# Archive removed entries
df_foreign['removal_reason'] = 'FOREIGN_NON_890_BARCODE'
df_india_invalid['removal_reason'] = 'NON_FOOD_OR_INVALID_NONSENSE'

df_removed_all = pd.concat([df_foreign, df_india_invalid], ignore_index=True)
df_removed_all = df_removed_all.drop_duplicates(subset=['barcode'], keep='first')
df_removed_all.to_csv(removed_csv, index=False)

# Clean up helper columns
clean_cols = [c for c in df_clean_india.columns if c not in ['is_india_barcode', 'is_invalid_or_non_food']]
df_final = df_clean_india[clean_cols].copy()
df_final = df_final.drop_duplicates(subset=['barcode'], keep='first')

# OVERWRITE all_supabase_products.csv WITH CLEAN INDIA-ONLY DATABASE
df_final.to_csv(all_supabase_csv, index=False)

print(f"Purge Complete!")
print(f"  Raw Initial Total: {initial_count}")
print(f"  Purged Foreign & Invalid Records: {len(df_removed_all)}")
print(f"  New Master Clean India Database Count: {len(df_final)}")
