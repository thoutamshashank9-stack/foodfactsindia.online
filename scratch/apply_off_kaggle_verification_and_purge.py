import os
import sys
import pandas as pd
import re

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"c:\Users\thout\Downloads\check it"

confirmed_csv = os.path.join(BASE_DIR, "india_products_confirmed.csv")
verification_csv = os.path.join(BASE_DIR, "india_products_needs_verification.csv")
removed_csv = os.path.join(BASE_DIR, "foreign_or_invalid_products_removed.csv")
cleaned_csv = os.path.join(BASE_DIR, "cleaned_dataset.csv")

print("=== APPLYING EXPANDED NON-FOOD PURGE & OFF/KAGGLE VERIFICATION ===")

df_confirmed = pd.read_csv(confirmed_csv, dtype=str)
df_verification = pd.read_csv(verification_csv, dtype=str)
df_removed = pd.read_csv(removed_csv, dtype=str)

print(f"Loaded Confirmed Table: {len(df_confirmed)}")
print(f"Loaded Verification Queue Table: {len(df_verification)}")
print(f"Loaded Removed Table: {len(df_removed)}")

# 1. EXPANDED NON-FOOD PURGE KEYWORDS
non_food_kw = [
    'kamagra','apcalis','luvagra','lisnop','seclo','panzim','novaten','tadix',
    'zeagra','dolozox','cetirizine','relispray','soventus','entofoam','jhandu','zandu',
    'kottakkal','koflet','qur-derm','cobra 150','eno','vaseline','lakme','lakmē','ponds',
    'johnson','dettol','lifebuoy','fogg','parachute','nish hair','nisha','vicco','clinic plus',
    'modicare','body oil','miss mimi','manjan','biotique','makeup','camlin','libreta',
    'dr. fixit','hicks','tissues','freshnar','fresh one','hygienic','dog soap','chappi',
    'pet safa','diapers','pediasure','pedia sure','nepro','poshan','whisky','seagram',
    'thermometer','marker','notebook','filler','ors','oralyte','orsl','shilajit','wrathx',
    'protein isolate','whey','pre workout','apetamin','cureveda','woodwards','amicadon',
    'shampoo','soap','lotion','deodorant','cream','ointment','syrup','capsule','tablet',
    'cleaner','detergent','sanitizer'
]

def is_expanded_non_food(row):
    pname = str(row.get('product_name', '')).lower()
    brand = str(row.get('brands', '')).lower()
    cat = str(row.get('categories', '')).lower()
    
    # Specific barcode purges provided in report
    b_code = str(row.get('barcode', '')).strip()
    specific_purges = [
        '8901111046234','8901111000168','8906045940320','8904151826545','8906044905481',
        '8901111570111','8901111005781','8901111350133','8901111079478','8906144634274',
        '8906127145698','8904054610579','8901302098868','8901086210845','8906006640078',
        '8904155708793','8901117268357','8901117232709','8901248701105','8901248704083',
        '8904059120073','8904059150209','8901138100629','8904151802112','8902393003502',
        '8902618000019','8906045948371','8908013388653','8901571001064','8906102520700',
        '8901030916236','8901030712067','8909106057647','8901012116852','8901012116845',
        '8901396389859','8901396602071','8901030954825','8908001158589','8908001158565',
        '8908001158343','8901088167987','8901088020039','8906015580600','8906015587722',
        '8901288230306','8901030937170','8904037209196','8908005977001','8906046936544',
        '8904049100207','8904158008289','8901030971945','8906009451060','8907901244828',
        '8901425030042','8904116101038','8901860835233','8904213900060','8901435000486',
        '8903664052175','8904132963610','8901225785043','8906000131404','8906002485475',
        '8908009149138','8901522000023','8904026643710','8904145911820','8904145912360',
        '8904145911318','8908006704118'
    ]
    if b_code in specific_purges:
        return True

    for kw in non_food_kw:
        if kw in pname or kw in brand or kw in cat:
            return True

    return False

# Purge non-food items from verification queue
df_verification['is_non_food'] = df_verification.apply(is_expanded_non_food, axis=1)
purged_from_queue = df_verification[df_verification['is_non_food']].copy()
purged_from_queue['removal_reason'] = 'EXPANDED_NON_FOOD_PURGE'

df_verification_clean = df_verification[~df_verification['is_non_food']].drop(columns=['is_non_food'])

# Purge non-food items from confirmed table
df_confirmed['is_non_food'] = df_confirmed.apply(is_expanded_non_food, axis=1)
purged_from_confirmed = df_confirmed[df_confirmed['is_non_food']].copy()
purged_from_confirmed['removal_reason'] = 'EXPANDED_NON_FOOD_PURGE'

df_confirmed_clean = df_confirmed[~df_confirmed['is_non_food']].drop(columns=['is_non_food'])

# 2. ELEVATE VERIFIED OFF SAMPLE PRODUCT (Paper Boat Lychee 8906080600586)
off_verified_barcodes = ['8906080600586']
for v_code in off_verified_barcodes:
    match_v = df_verification_clean[df_verification_clean['barcode'] == v_code]
    if len(match_v) > 0:
        elevated_item = match_v.iloc[0].to_dict()
        elevated_item['ingredients_text'] = 'Water, Sugar, Lychee Pulp (12%), Apple Juice Concentrate, Acidity Regulators [330, 332(ii), 331(iii)], Flavours, Stabilizers (Carrageenan & Konjac Flour), Antioxidant (300), Vitamin D2'
        elevated_item['sold_in_india_status'] = 'CONFIRMED_VIA_OFF_API'
        elevated_item['ingredient_confidence'] = 'HIGH'
        elevated_item['status'] = 'KEEP'
        
        # Remove from queue & add to confirmed
        df_verification_clean = df_verification_clean[df_verification_clean['barcode'] != v_code]
        df_confirmed_clean = pd.concat([df_confirmed_clean, pd.DataFrame([elevated_item])], ignore_index=True)

# Combine purged items with removed table
purged_combined = pd.concat([purged_from_queue, purged_from_confirmed], ignore_index=True)
if 'is_non_food' in purged_combined.columns:
    purged_combined = purged_combined.drop(columns=['is_non_food'])

df_removed_updated = pd.concat([df_removed, purged_combined], ignore_index=True)
df_removed_updated = df_removed_updated.drop_duplicates(subset=['barcode'], keep='first')

# EXPORT UPDATED TABLES
df_confirmed_clean.to_csv(confirmed_csv, index=False)
df_verification_clean.to_csv(verification_csv, index=False)
df_removed_updated.to_csv(removed_csv, index=False)

# Update cleaned_dataset.csv in root workspace
df_confirmed_clean.to_csv(cleaned_csv, index=False)

print("\n--- UPDATED TRI-TABLE SUMMARY ---")
print(f"🟢 Table 1: india_products_confirmed: {len(df_confirmed_clean)} products ({df_confirmed_clean['barcode'].nunique()} unique barcodes)")
print(f"🟡 Table 2: india_products_needs_verification: {len(df_verification_clean)} products ({df_verification_clean['barcode'].nunique()} unique barcodes)")
print(f"❌ Table 3: foreign_or_invalid_products_removed: {len(df_removed_updated)} products ({df_removed_updated['barcode'].nunique()} unique barcodes)")

print(f"\nPurged {len(purged_combined)} non-food/pharma/cosmetic entries from food tables.")
print(f"Saved updated CSV files to:")
print(f" - {confirmed_csv}")
print(f" - {verification_csv}")
print(f" - {removed_csv}")
