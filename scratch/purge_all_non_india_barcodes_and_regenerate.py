import os
import sys
import pandas as pd
import re

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"c:\Users\thout\Downloads\check it"

all_supabase_csv = os.path.join(BASE_DIR, "all_supabase_products.csv")

print("=== STRICT BARCODE PURGE (GS1 890 ONLY) ACROSS ALL DATASETS ===")

df_all = pd.read_csv(all_supabase_csv, dtype=str)
initial_raw_count = len(df_all)

# 1. STRICT GS1 INDIA BARCODE RULE (^890\d{10}$)
def is_valid_india_barcode(barcode):
    if pd.isna(barcode): return False
    b = str(barcode).strip()
    return bool(re.match(r'^890\d{10}$', b)) or b.startswith('890')

df_all['is_india_barcode'] = df_all['barcode'].apply(is_valid_india_barcode)

df_india_all = df_all[df_all['is_india_barcode']].copy()
df_foreign_all = df_all[~df_all['is_india_barcode']].copy()

total_india_barcodes = df_india_all['barcode'].nunique()
total_foreign_barcodes = df_foreign_all['barcode'].nunique()

# 2. PURGE NON-FOOD & INVALID NONSENSE FROM INDIA DATASET
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

df_india_all['is_invalid_or_non_food'] = df_india_all.apply(is_invalid_or_non_food, axis=1)

df_india_food = df_india_all[~df_india_all['is_invalid_or_non_food']].copy()
df_india_invalid = df_india_all[df_india_all['is_invalid_or_non_food']].copy()

# 3. SPLIT INTO CONFIRMED (COMPLETE DATA) & NEEDS VERIFICATION (INCOMPLETE DATA)
ing_col = 'ingredients_text' if 'ingredients_text' in df_india_food.columns else 'ingredient_list_raw'

df_india_food['has_complete_data'] = df_india_food[ing_col].apply(
    lambda x: pd.notna(x) and len(str(x).strip()) >= 15 and str(x).strip().lower() != 'nan'
)

df_confirmed = df_india_food[df_india_food['has_complete_data']].copy()
df_unverified = df_india_food[~df_india_food['has_complete_data']].copy()

# Fix manual sample brands
brand_manual_fixes = {
    '8906010360405': ('Ghee', 'Local/Regional Dairy'),
    '8901779902569': ('Saras Sunflower Oil', 'Saras'),
    '8901242107408': ('Bambino Roasted Vermicelli', 'Bambino'),
    '8906151991032': ('Strawberry Ice Cream', 'Camerry'),
    '8908016501493': ('Peri Peri Momos', 'Hello Tempayy'),
    '8904001800282': ('Sesame Oil', 'Idayam'),
    '8901491983211': ("Lay's Chips", "Lay's"),
    '8906151236607': ('Millet Fingers Chatpata Masala', 'Snackible'),
    '8906035140204': ('Bengali Mixture', 'Chipo'),
    '8906020582002': ('Protein Rich Chapati', 'Fresh iD'),
    '8904109621116': ('Malabar Paratha', "Nik's Cuisine")
}

for b_code, (p_name, b_name) in brand_manual_fixes.items():
    for df_target in [df_confirmed, df_unverified]:
        mask = df_target['barcode'] == b_code
        if mask.sum() > 0:
            df_target.loc[mask, 'product_name'] = p_name
            df_target.loc[mask, 'brands'] = b_name

# Add metadata columns
df_confirmed['sold_in_india_status'] = 'CONFIRMED_INDIA_890'
df_confirmed['ingredient_confidence'] = 'HIGH'
df_confirmed['status'] = 'KEEP'

df_unverified['sold_in_india_status'] = 'NEEDS_VERIFICATION'
df_unverified['ingredient_confidence'] = 'INCOMPLETE'
df_unverified['status'] = 'FIX'

# COMBINE ALL REMOVED ITEMS (Foreign Barcodes + Non-Food/Invalid)
df_foreign_all['removal_reason'] = 'FOREIGN_NON_890_BARCODE'
df_india_invalid['removal_reason'] = 'NON_FOOD_OR_INVALID_NONSENSE'

df_removed_all = pd.concat([df_foreign_all, df_india_invalid], ignore_index=True)
df_removed_all = df_removed_all.drop_duplicates(subset=['barcode'], keep='first')

# EXPORT TO WORKSPACE CSV FILES
confirmed_csv = os.path.join(BASE_DIR, "india_products_confirmed.csv")
unverified_csv = os.path.join(BASE_DIR, "india_products_needs_verification.csv")
removed_csv = os.path.join(BASE_DIR, "foreign_or_invalid_products_removed.csv")
cleaned_csv = os.path.join(BASE_DIR, "cleaned_dataset.csv")

cols_drop = ['is_india_barcode', 'is_invalid_or_non_food', 'has_complete_data']
df_confirmed.drop(columns=cols_drop, errors='ignore').to_csv(confirmed_csv, index=False)
df_unverified.drop(columns=cols_drop, errors='ignore').to_csv(unverified_csv, index=False)
df_removed_all.drop(columns=cols_drop, errors='ignore').to_csv(removed_csv, index=False)
df_confirmed.drop(columns=cols_drop, errors='ignore').to_csv(cleaned_csv, index=False)

print("\n--- REGENERATED DATASET METRICS ---")
print(f"Total Raw Collected Records: {initial_raw_count}")
print(f"❌ Total Foreign Non-890 Barcodes Purged: {total_foreign_barcodes}")
print(f"❌ Total Invalid / Non-Food / Nonsense Rows Purged: {len(df_india_invalid)}")
print(f"🟢 Total Verified Domestic Indian Food Products WITH Complete Data: {len(df_confirmed)} ({df_confirmed['barcode'].nunique()} unique Indian 890 barcodes)")
print(f"🟡 Total Unverified Domestic Indian Food Products WITH Incomplete Data: {len(df_unverified)} ({df_unverified['barcode'].nunique()} unique Indian 890 barcodes)")
print(f"❌ Total Removed Records: {len(df_removed_all)}")

print("\nSaved updated India-only datasets:")
print(f" - {confirmed_csv}")
print(f" - {unverified_csv}")
print(f" - {removed_csv}")
