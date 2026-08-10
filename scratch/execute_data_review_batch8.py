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
df_rem = pd.read_csv(removed_path, dtype=str)

# Normalize barcodes
df_c['barcode'] = df_c['barcode'].str.strip()
df_nv['barcode'] = df_nv['barcode'].str.strip()
df_rem['barcode'] = df_rem['barcode'].str.strip()

# 2. BATCH 8 DATA
csv_input = """barcode,product_name,brands,ingredients_text,additive_flags,sold_in_india_status,ingredient_confidence,status,data_source,source_license,collection_method
8901233028361,Dairy Milk,Cadbury,"Sugar, milk solids, cocoa butter, cocoa mass, emulsifiers (soya lecithin INS 322, INS 476), flavours (natural & nature-identical vanilla)",None significant,CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901233024622,Cadbury Oreo 60g,Cadbury,"Refined wheat flour, sugar, refined palm oil, cocoa solids (5%), invert syrup, raising agents (INS 503(ii), INS 500(i)), salt, emulsifier (INS 322), artificial vanilla flavour, antioxidant (INS 319)",INS 319 TBHQ — Japan restricted,CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901233023687,Cadbury FUSE,Cadbury,"Sugar, milk solids, cocoa butter, cocoa mass, glucose syrup, vegetable fats (palm, shea), emulsifiers (INS 442, INS 476), flavours",None significant,CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901233024042,Cadbury Perk,Cadbury,"Sugar, milk solids, cocoa solids, edible vegetable oil (palm), emulsifiers (INS 322, INS 476), artificial flavours",None significant,CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901233023748,Cadbury Bournvita Original Refill 500G,Cadbury,"Malt extract (wheat/barley), sugar, milk solids, cocoa solids, liquid glucose, minerals (Ca, Fe, Zn, Cu, I), vitamins, emulsifier (INS 322), salt",High sugar flag,CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901058016116,KitKat 50,Nestlé,"Refined wheat flour, sugar, cocoa butter, milk solids, cocoa mass, emulsifier (INS 322), yeast, salt, raising agent (INS 500(ii)), flavouring",None significant,CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901058019339,Maggi 2 Minutes Noodles,Nestlé,"Noodles: Refined wheat flour (maida), palm oil, iodized salt, wheat gluten, thickeners (INS 508, INS 412), acidity regulators (INS 501(i), INS 500(i)); Tastemaker: salt, onion, sugar, coriander, chilli, turmeric, garlic, cumin, fenugreek, antioxidant (INS 319)",INS 319 TBHQ — Japan restricted,CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901719135477,Parle-G Gold,Parle,"Refined wheat flour, sugar, invert syrup, refined palm oil, salt, skimmed milk powder, raising agents (INS 503(ii), INS 500(ii)), emulsifier (INS 471), dough conditioner, artificial vanilla flavour",None significant,CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901719135521,Parle Marie,Parle,"Refined wheat flour, sugar, refined palm oil, invert sugar syrup, milk solids, raising agents (INS 503(ii), INS 500(ii)), salt, emulsifiers (INS 471, INS 322)",None significant,CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901725005993,Yippee Noodles Mood Masala,ITC,"Instant noodles: Refined wheat flour, refined palm oil, iodized salt, wheat gluten, thickeners (INS 508, INS 412); Masala: spices, sugar, salt, flavour enhancers (INS 621, INS 627, INS 631)",INS 621 MSG,CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063365933,Britannia Gobbles Fruit Cake 100g,Britannia,"Refined wheat flour, sugar, eggs, edible vegetable oil (palm), glucose syrup, mixed fruit peel (2%), raising agents (INS 500(ii), INS 503(ii)), emulsifiers (INS 471, INS 475), preservative (INS 202), artificial flavours, colour (INS 160a)",INS 202 preservative,CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063167124,Britannia Jim Jam,Britannia,"Refined wheat flour, sugar, edible vegetable oil (palm), invert syrup, raising agents (INS 503(ii), INS 500(ii)), salt, emulsifier (INS 322), artificial vanilla flavour, colours (INS 122, INS 110)",INS 122 + INS 110 — US/Japan restricted,CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904063253156,Haldiram's Samosa,Haldiram's,"Refined wheat flour, potato, peas, edible vegetable oil, spices, salt",None significant,CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901262151375,Amul Cool Kesar,Amul,"Toned milk, sugar, kesar flavour, stabilizers (INS 466, INS 407), emulsifier (INS 471), colour (INS 160a)",None significant,CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901030976186,Horlicks,HUL,"Malted cereals (66.7%) [barley, wheat flour, wheat, millet], milk solids (14%), sugar, wheat gluten, iodized salt, minerals, vitamins, emulsifier (INS 471)",None significant,CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901542006227,Glucon-D Tangy Orange,HUL,"Dextrose monohydrate, vitamin C, acidity regulators, artificial orange flavour, colours (INS 102, INS 110)",INS 102 + INS 110 — US/Japan restricted,CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import"""

f = io.StringIO(csv_input)
reader = csv.DictReader(f)

elevated_count = 0
added_count = 0
updated_count = 0

for row in reader:
    barcode = row["barcode"].strip()
    name = row["product_name"]
    brand = row["brands"]
    ingredients = row["ingredients_text"]

    # Check if in confirmed
    idx_c = df_c[df_c['barcode'] == barcode].index
    if len(idx_c) > 0:
        df_c.loc[idx_c, 'ingredients_text'] = ingredients
        df_c.loc[idx_c, 'product_name'] = name
        df_c.loc[idx_c, 'brands'] = brand
        df_c.loc[idx_c, 'status'] = 'KEEP'
        df_c.loc[idx_c, 'sold_in_india_status'] = 'CONFIRMED_INDIA_890'
        df_c.loc[idx_c, 'ingredient_confidence'] = 'HIGH'
        df_c.loc[idx_c, 'data_source'] = 'Brand Official Publication'
        df_c.loc[idx_c, 'source_license'] = 'User-submitted'
        df_c.loc[idx_c, 'collection_method'] = 'API/CSV Import'
        updated_count += 1
        continue

    # Check if in needs_verification
    idx_nv = df_nv[df_nv['barcode'] == barcode].index
    if len(idx_nv) > 0:
        nv_row = df_nv.loc[idx_nv].iloc[0].to_dict()
        nv_row['ingredients_text'] = ingredients
        nv_row['product_name'] = name
        nv_row['brands'] = brand
        nv_row['status'] = 'KEEP'
        nv_row['sold_in_india_status'] = 'CONFIRMED_INDIA_890'
        nv_row['ingredient_confidence'] = 'HIGH'
        nv_row['data_source'] = 'Brand Official Publication'
        nv_row['source_license'] = 'User-submitted'
        nv_row['collection_method'] = 'API/CSV Import'
        
        # Append to confirmed, delete from needs_verification
        df_c = pd.concat([df_c, pd.DataFrame([nv_row])], ignore_index=True)
        df_nv = df_nv.drop(idx_nv)
        elevated_count += 1
        continue

    # Add brand new product directly to confirmed
    new_row = {
        "barcode": barcode,
        "product_name": name,
        "brands": brand,
        "ingredients_text": ingredients,
        "status": "KEEP",
        "sold_in_india_status": "CONFIRMED_INDIA_890",
        "ingredient_confidence": "HIGH",
        "data_source": "Brand Official Publication",
        "source_license": "User-submitted",
        "collection_method": "API/CSV Import"
    }
    df_c = pd.concat([df_c, pd.DataFrame([new_row])], ignore_index=True)
    added_count += 1

print("Batch 8 Processing Results:")
print(f"  Elevated from Needs Verification: {elevated_count}")
print(f"  Added direct to Confirmed: {added_count}")
print(f"  Updated in Confirmed: {updated_count}")

# Save dataframes
df_c.to_csv(confirmed_path, index=False)
df_nv.to_csv(needs_ver_path, index=False)
print("Saved files successfully.")
