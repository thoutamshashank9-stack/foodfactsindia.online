import os
import sys
import io
import csv
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"c:\Users\thout\Downloads\check it"

confirmed_path = os.path.join(BASE_DIR, "india_products_confirmed.csv")
needs_ver_path = os.path.join(BASE_DIR, "india_products_needs_verification.csv")
removed_path = os.path.join(BASE_DIR, "foreign_or_invalid_products_removed.csv")

# 1. Load dataframes
df_c = pd.read_csv(confirmed_path, dtype=str)
df_nv = pd.read_csv(needs_ver_path, dtype=str)

if os.path.exists(removed_path):
    df_rem = pd.read_csv(removed_path, dtype=str)
else:
    df_rem = pd.DataFrame(columns=['barcode', 'product_name', 'brands', 'ingredients_text', 'reason'])

# Normalize barcodes
df_c['barcode'] = df_c['barcode'].str.strip()
df_nv['barcode'] = df_nv['barcode'].str.strip()
df_rem['barcode'] = df_rem['barcode'].str.strip()

# 2. PURGE LIST (Non-food / Corrupt / Specific items)
barcodes_to_purge = {
    '8901396040309': 'VANISH (Reckitt) - non-food stain remover',
    '8904192600647': 'FLORITE NIPPLE SHIELD - non-food medical/baby care',
    '8901083012114': 'ALLEGRA 120 TAB (Sanofi) - non-food pharmaceutical',
    '8901396126027': 'Lizol Citrus - non-food floor cleaner',
    '8905110001232': 'Fiama lemongrass & jojoba - non-food soap',
    '8906013282742': 'St. Botanica smoothening - non-food cosmetic',
    '8901088798051': 'SET WET PARTY SHINE - non-food hair gel',
    '8906084790405': 'Beardo godfather beard oil - non-food cosmetic',
    '8901526406883': 'Corrupt OCR garbage name',
    '8901111571118': 'Amaday 10 - non-food pharmaceutical',
    '8901111474112': 'Amaday 5 - non-food pharmaceutical',
    '8904023007584': 'Hair oil - non-food cosmetic',
    '8901314502186': 'Palmolive - non-food cosmetic',
    '8901725004422': 'Empty/corrupt chips entry with no details'
}

purged_count = 0
for bc, reason in barcodes_to_purge.items():
    # Find in confirmed
    c_match = df_c[df_c['barcode'] == bc]
    # Find in needs_verification
    nv_match = df_nv[df_nv['barcode'] == bc]
    
    match = None
    if not c_match.empty:
        match = c_match.iloc[0].to_dict()
        df_c = df_c[df_c['barcode'] != bc]
    elif not nv_match.empty:
        match = nv_match.iloc[0].to_dict()
        df_nv = df_nv[df_nv['barcode'] != bc]
        
    if match:
        new_rem_row = {
            'barcode': bc,
            'product_name': match.get('product_name', ''),
            'brands': match.get('brands', ''),
            'ingredients_text': match.get('ingredients_text', ''),
            'reason': reason
        }
        df_rem = pd.concat([df_rem, pd.DataFrame([new_rem_row])], ignore_index=True)
        purged_count += 1

print(f"Purged {purged_count} non-food/corrupt products and moved to removed file.")

# 3. DUPLICATE MERGES
# Format: (canonical_barcode, duplicate_barcode)
duplicates_to_merge = [
    ('8901719135477', '8901719101663'), # Parle-G Gold
    ('8904063216403', '8904063240262'), # Haldiram's Khatta Meetha
    ('8902901221831', '8902901225075')  # masoor whole
]

merged_count = 0
for canon_bc, dup_bc in duplicates_to_merge:
    # Overwrite details or check if exists
    # Find duplicate in confirmed or needs_verification and remove it
    dup_in_c = df_c[df_c['barcode'] == dup_bc]
    dup_in_nv = df_nv[df_nv['barcode'] == dup_bc]
    
    if not dup_in_c.empty:
        df_c = df_c[df_c['barcode'] != dup_bc]
        merged_count += 1
    if not dup_in_nv.empty:
        df_nv = df_nv[df_nv['barcode'] != dup_bc]
        merged_count += 1

print(f"Merged and removed {merged_count} duplicate barcode listings.")

# 4. BRAND FIELD CORRECTIONS & SWAPS
corrections = {
    '8904083518150': {'brands': '24 Mantra Organic', 'product_name': 'Brown Rice'},
    '8901808000747': {'brands': 'Weikfield', 'product_name': 'Baking Powder'},
    '8901063370166': {'brands': 'Britannia', 'product_name': 'Good Day'},
    '8901063371026': {'brands': 'Britannia', 'product_name': 'Marie Gold'},
    '8901192205001': {'brands': 'Catch', 'product_name': 'Chat Masala'},
    '8901058018493': {'brands': 'Maggi', 'product_name': 'Maggi 2-Minute Noodles Masala'}
}

updated_fields = 0
for bc, fields in corrections.items():
    # Update in confirmed
    idx_c = df_c[df_c['barcode'] == bc].index
    if not idx_c.empty:
        for f, val in fields.items():
            df_c.at[idx_c[0], f] = val
        updated_fields += 1
    # Update in needs_verification
    idx_nv = df_nv[df_nv['barcode'] == bc].index
    if not idx_nv.empty:
        for f, val in fields.items():
            df_nv.at[idx_nv[0], f] = val
        updated_fields += 1

print(f"Corrected fields for {updated_fields} products.")

# 5. TRANSLATIONS
translations = {
    '8908012051008': 'Cashew Nuts',
    '8908014100407': 'Basmati Rice',
    '8908014648886': 'Pickled Gherkins',
    '8902433000232': 'Snickers Almond Chocolate 40g',
    '8901047619274': 'Bombay Masala Curry Sauce'
}

translated_count = 0
for bc, eng_name in translations.items():
    idx_c = df_c[df_c['barcode'] == bc].index
    if not idx_c.empty:
        df_c.at[idx_c[0], 'product_name'] = eng_name
        translated_count += 1
    idx_nv = df_nv[df_nv['barcode'] == bc].index
    if not idx_nv.empty:
        df_nv.at[idx_nv[0], 'product_name'] = eng_name
        translated_count += 1

print(f"Translated and fixed names for {translated_count} products.")

# 6. IMPORT VERIFIED BATCH 3 DATA
verified_batch3_csv = """barcode,product_name,brands,ingredients_text,sold_in_india_status,ingredient_confidence,status,data_source,source_license,collection_method
8901063368026,Gobbles Fruit Cake 55gm,Britannia,"Refined wheat flour (maida), sugar, eggs, edible vegetable oil (palm), glucose syrup, mixed fruit peel (2%), raising agents (INS 500(ii), INS 503(ii)), emulsifiers (INS 471, INS 475), preservative (INS 202), artificial flavours, colour (INS 160a)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063325074,Toastea,Britannia,"Refined wheat flour, sugar, edible vegetable oil (palm), invert syrup, milk solids, raising agents (INS 503(ii), INS 500(ii)), salt, emulsifier (INS 322), artificial vanilla flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063028258,Nice Time,Britannia,"Refined wheat flour, sugar, coconut (12%), edible vegetable oil (palm), invert syrup, raising agents (INS 503(ii), INS 500(ii)), salt, emulsifier (INS 322), artificial coconut flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063155497,Tiger Krunch Coconut,Britannia,"Refined wheat flour, sugar, edible vegetable oil (palm), coconut (8%), invert syrup, raising agents (INS 503(ii), INS 500(ii)), salt, emulsifier (INS 322), artificial coconut flavour, added vitamins & minerals",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063371026,Marie Gold,Britannia,"Refined wheat flour (73%), sugar, refined palm oil, invert sugar syrup, milk solids & sweetened condensed milk, raising agents (INS 503(ii), INS 500(ii)), salt, emulsifiers (INS 471, INS 322)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063092709,Good Day Cashew,Britannia,"Refined wheat flour, edible vegetable oil (palm), sugar, cashew nuts (4.5%), invert syrup, milk solids, butter (0.6%), raising agents (INS 503(i), INS 500(i)), salt, emulsifier (soya lecithin INS 322)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063032453,Treat Croissant Vanilla Créme,Britannia,"Refined wheat flour, sugar, edible vegetable oil (palm), eggs, invert syrup, raising agents (INS 500(ii), INS 503(ii)), emulsifiers (INS 471, INS 475), preservative (INS 202), artificial vanilla flavour, colour (INS 160a)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063365100,Gobbles Marble Cake 110g,Britannia,"Refined wheat flour, sugar, eggs, edible vegetable oil (palm), glucose syrup, cocoa solids (2%), raising agents (INS 500(ii), INS 503(ii)), emulsifiers (INS 471, INS 475), preservative (INS 202), artificial flavours, colour (INS 150c)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063362758,Gobbles Orange Cake,Britannia,"Refined wheat flour, sugar, eggs, edible vegetable oil (palm), glucose syrup, orange peel (1.5%), raising agents (INS 500(ii), INS 503(ii)), emulsifiers (INS 471, INS 475), preservative (INS 202), artificial orange flavour, colour (INS 160a)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063362741,Gobbles Fruity Cake,Britannia,"Refined wheat flour, sugar, eggs, edible vegetable oil (palm), glucose syrup, mixed fruit peel (2%), raising agents (INS 500(ii), INS 503(ii)), emulsifiers (INS 471, INS 475), preservative (INS 202), artificial fruit flavour, colours (INS 160a, INS 102)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063363922,Muffils Strawberry,Britannia,"Refined wheat flour, sugar, eggs, edible vegetable oil (palm), glucose syrup, strawberry flavour, raising agents (INS 500(ii), INS 503(ii)), emulsifiers (INS 471, INS 475), preservative (INS 202), colour (INS 122)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063014312,Vita Marie Gold,Britannia,"Refined wheat flour (70%), sugar, refined palm oil, invert sugar syrup, milk solids, raising agents (INS 503(ii), INS 500(ii)), salt, emulsifiers (INS 471, INS 322), added vitamins & minerals",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063026346,NutriChoice Digestive,Britannia,"Whole wheat flour (71%), sugar, edible vegetable oil (palm), raising agents (INS 503(ii), INS 500(ii)), salt, emulsifiers (INS 471, INS 322), added vitamins & minerals",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901719126970,Parle 20-20 Cashew Biscuits,Parle,"Refined wheat flour, sugar, edible vegetable oil (palm), cashew nuts (8%), invert syrup, milk solids, raising agents (INS 503(ii), INS 500(ii)), salt, emulsifier (INS 322), artificial vanilla flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901719123801,Parle Monaco 400g,Parle,"Refined wheat flour, sugar, edible vegetable oil (palm), invert syrup, salt, raising agents (INS 503(ii), INS 500(ii)), emulsifier (INS 322), artificial butter flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901719124006,Parle Krackjack 200g,Parle,"Refined wheat flour, sugar, edible vegetable oil (palm), invert syrup, salt, raising agents (INS 503(ii), INS 500(ii)), emulsifier (INS 322), artificial butter flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901719136801,Hide & Seek Milano (Creme),Parle,"Refined wheat flour, sugar, edible vegetable oil (palm), cocoa solids, invert syrup, milk solids, raising agents (INS 503(ii), INS 500(ii)), emulsifier (INS 322), artificial vanilla flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901719136757,Hide & Seek Finest Choco,Parle,"Refined wheat flour, sugar, edible vegetable oil (palm), cocoa solids (6%), invert syrup, milk solids, raising agents (INS 503(ii), INS 500(ii)), emulsifier (INS 322), artificial chocolate flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901719137846,Milano Vanilla,Parle,"Refined wheat flour, sugar, edible vegetable oil (palm), invert syrup, milk solids, raising agents (INS 503(ii), INS 500(ii)), emulsifier (INS 322), artificial vanilla flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901719127236,Rusk,Parle,"Refined wheat flour, sugar, edible vegetable oil (palm), invert syrup, milk solids, raising agents (INS 503(ii), INS 500(ii)), salt, emulsifier (INS 322), artificial vanilla flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901719135477,Parle-G Gold,Parle,"Refined wheat flour, sugar, invert syrup, refined palm oil, salt, skimmed milk powder, raising agents (INS 503(ii), INS 500(ii)), emulsifier (INS 471), dough conditioner, artificial vanilla flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901058018493,Maggi 2-Minute Noodles Masala,Maggi,"Noodles: Refined wheat flour (maida), palm oil, iodized salt, wheat gluten, thickeners (INS 508, INS 412), acidity regulators (INS 501(i), INS 500(i)); Tastemaker: salt, onion, sugar, coriander, chilli, turmeric, garlic, cumin, fenugreek, antioxidant (INS 319)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901058008388,Maggi Hot Sweet Tomato Chilli Sauce,Maggi,"Tomato paste, sugar, water, vinegar, salt, chilli, garlic, acidity regulator (INS 260), preservative (INS 211), thickener (INS 1422)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901058003055,Maggi Pazzta Cheese Macaroni,Maggi,"Macaroni: Durum wheat semolina, salt; Tastemaker: milk solids, cheese powder, sugar, salt, palm oil, thickeners (INS 1422, INS 412), flavour enhancers (INS 621, INS 627, INS 631), artificial cheese flavour, colour (INS 160a)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901058014846,Maggi Pazzta Cheesy Tomato Twist,Maggi,"Macaroni: Durum wheat semolina, salt; Tastemaker: tomato powder, milk solids, sugar, salt, palm oil, thickeners (INS 1422, INS 412), flavour enhancers (INS 621, INS 627, INS 631), artificial cheese flavour, colour (INS 160c)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901058002270,Maggi Spicy Garlic Noodles,Maggi,"Noodles: Refined wheat flour, palm oil, salt, wheat gluten, thickeners (INS 508, INS 412), acidity regulators; Tastemaker: salt, garlic, chilli, spices, sugar, flavour enhancers (INS 621), antioxidant (INS 319)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901058006032,Maggi Cup Noodles Masala,Maggi,"Noodles: Refined wheat flour, palm oil, salt, wheat gluten, thickeners, acidity regulators; Tastemaker: salt, spices, sugar, dehydrated vegetables, flavour enhancers (INS 621, INS 627, INS 631), antioxidant (INS 319)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901058013665,Maggi Hot and Sweet Noodles,Maggi,"Noodles: Refined wheat flour, palm oil, salt, wheat gluten, thickeners, acidity regulators; Tastemaker: salt, sugar, chilli, garlic, spices, flavour enhancers (INS 621), antioxidant (INS 319)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904004403770,Moong Dal,Haldiram's,"Moong dal, edible vegetable oil (palmolein), iodized salt, spices (red chilli, black pepper, asafoetida)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904004403534,Tasty Nuts,Haldiram's,"Peanuts, edible vegetable oil (palmolein), iodized salt, spices (red chilli, black pepper)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904063216403,Khatta Meetha,Haldiram's,"Rice flakes, edible vegetable oil (palmolein), sugar, peanuts, sago, iodized salt, spices, raising agents, colours (INS 160c)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904063216168,Bombay Mix,Haldiram's,"Rice flakes, gram flour, edible vegetable oil (palmolein), peanuts, sago, iodized salt, spices, raising agents, colours (INS 160c)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904063230133,Cornflakes Mixture,Haldiram's,"Corn flakes, edible vegetable oil (palmolein), peanuts, sago, iodized salt, spices, sugar, raising agents, colours (INS 160c)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904004405224,Soan Cake,Haldiram's,"Sugar, refined wheat flour, edible vegetable oil (palm), milk solids, cardamom, raising agents, emulsifiers",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904004416367,Atta Cookies,Haldiram's,"Whole wheat flour, sugar, edible vegetable oil (palm), invert syrup, raising agents (INS 503(ii), INS 500(ii)), salt, emulsifier (INS 322), artificial vanilla flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904004410754,Dry Fruit Besan Ladoo,Haldiram's,"Gram flour (besan), sugar, edible vegetable oil (ghee), dry fruits (cashew, almond, raisin), cardamom",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901725017545,Nice,Sunfeast,"Refined wheat flour, sugar, coconut, edible vegetable oil (palm), invert syrup, raising agents (INS 503(ii), INS 500(ii)), salt, emulsifier (INS 322), artificial coconut flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901725015886,Dark Fantasy Choco Fills,Sunfeast,"Choco crème (sugar, refined palmolein, refined palm oil, cocoa solids), refined wheat flour, sugar, invert syrup, liquid glucose, edible vegetable oil, cocoa solids, milk solids, butter, raising agents (INS 503(ii), INS 500(i)), emulsifiers (INS 322, INS 471), salt",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901725136215,Dark Fantasy BIG Choco Fills,Sunfeast,"Choco crème (sugar, refined palmolein, refined palm oil, cocoa solids), refined wheat flour, sugar, invert syrup, liquid glucose, edible vegetable oil, cocoa solids, milk solids, butter, raising agents (INS 503(ii), INS 500(i)), emulsifiers (INS 322, INS 471), salt",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901725016265,Dark Fantasy Bourbon,Sunfeast,"Refined wheat flour, sugar, edible vegetable oil (palm), cocoa solids, invert syrup, raising agents (INS 503(ii), INS 500(i)), emulsifiers (INS 322, INS 471), salt, artificial chocolate flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901725005900,Yippee! Noodles Magic Masala,Sunfeast,"Instant noodles: Refined wheat flour (78.4%), refined palm oil, iodized salt, wheat gluten, thickeners (INS 508, INS 412); Masala: spices, dehydrated vegetables, sugar, salt, flavour enhancers (INS 621, INS 627, INS 631)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901725004217,Bingo Tedhe Medhe Tomato,Sunfeast,"Corn grits, edible vegetable oil (palmolein), rice grits, gram flour, spices, salt, sugar, tomato powder, flavour enhancers (INS 621, INS 627, INS 631), acidity regulators, colours (INS 160c)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901262150095,Amul Gold Milk 200ml,Amul,"Standardized milk (4.5% fat, 8.5% SNF), vitamins A & D",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901262010436,Amul White Unsalted Butter,Amul,"Pasteurized milk cream",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901262200271,Amul Dahi,Amul,"Pasteurized toned milk, active lactic culture",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901262180030,Amul Paneer,Amul,"Milk solids, citric acid (coagulant)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901262222471,Instant Mashed Potato,Amul,"Dehydrated potato flakes, salt, emulsifier (INS 471), antioxidant (INS 304)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901262180429,High Protein Paneer,Amul,"Milk solids, milk protein, citric acid (coagulant), salt",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
"""

reader = csv.DictReader(io.StringIO(verified_batch3_csv.strip()))
batch3_rows = [r for r in reader]

print(f"Parsed {len(batch3_rows)} products from verified_batch3.")

elevated_count = 0
added_direct_count = 0
updated_c_count = 0

c_barcodes = set(df_c['barcode'].tolist())
nv_barcodes = set(df_nv['barcode'].tolist())

for row in batch3_rows:
    bc = row['barcode'].strip()
    p_name = row['product_name'].strip()
    brand = row['brands'].strip()
    ing = row['ingredients_text'].strip()
    
    new_c_row = {
        'barcode': bc,
        'product_name': p_name,
        'brands': brand,
        'ingredients_text': ing,
        'sold_in_india_status': 'CONFIRMED_INDIA_890',
        'ingredient_confidence': 'HIGH',
        'status': 'KEEP',
        'data_source': 'Brand Official Publication',
        'source_license': 'User-submitted',
        'collection_method': 'API/CSV Import'
    }
    
    # If in confirmed, update ingredients
    if bc in c_barcodes:
        idx = df_c[df_c['barcode'] == bc].index[0]
        df_c.at[idx, 'product_name'] = p_name
        df_c.at[idx, 'brands'] = brand
        df_c.at[idx, 'ingredients_text'] = ing
        df_c.at[idx, 'ingredient_confidence'] = 'HIGH'
        updated_c_count += 1
    # If in needs_verification, remove from needs_verification and move to confirmed
    elif bc in nv_barcodes:
        df_nv = df_nv[df_nv['barcode'] != bc]
        nv_barcodes.remove(bc)
        df_c = pd.concat([df_c, pd.DataFrame([new_c_row])], ignore_index=True)
        c_barcodes.add(bc)
        elevated_count += 1
    # Brand new
    else:
        df_c = pd.concat([df_c, pd.DataFrame([new_c_row])], ignore_index=True)
        c_barcodes.add(bc)
        added_direct_count += 1

print(f"Batch3 Processing Results:")
print(f"  Elevated from Needs Verification: {elevated_count}")
print(f"  Added direct to Confirmed: {added_direct_count}")
print(f"  Updated in Confirmed: {updated_c_count}")

# Make sure all Needs Verification columns are clean
df_nv['ingredients_text'] = df_nv['ingredients_text'].fillna('')

# 7. Write everything back
df_c.to_csv(confirmed_path, index=False)
df_nv.to_csv(needs_ver_path, index=False)
df_rem.to_csv(removed_path, index=False)

print("\nSaved files successfully.")
