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

# 2. IMPORT VERIFIED BATCH 5 DATA
verified_batch5_csv = """barcode,product_name,brands,ingredients_text,sold_in_india_status,ingredient_confidence,status,data_source,source_license,collection_method
8901063029415,Treat Jim Jam,Britannia,"Refined wheat flour, sugar, edible vegetable oil (palm), invert syrup, raising agents (INS 503(ii), INS 500(ii)), salt, emulsifier (INS 322), artificial vanilla flavour, colours (INS 122, INS 110)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063363960,Gobbles Chocolate Cake,Britannia,"Refined wheat flour, sugar, eggs, edible vegetable oil (palm), glucose syrup, cocoa solids (3%), raising agents (INS 500(ii), INS 503(ii)), emulsifiers (INS 471, INS 475), preservative (INS 202), artificial chocolate flavour, colour (INS 150c)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063139336,Bourbon 100g,Britannia,"Refined wheat flour, sugar, edible vegetable oil (palm), cocoa solids, invert syrup, raising agents (INS 503(ii), INS 500(ii)), salt, emulsifiers (INS 322, INS 471), artificial chocolate flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063094291,Good Day Pista Badam,Britannia,"Refined wheat flour, edible vegetable oil (palm), sugar, pistachio (3%), almond (2%), invert syrup, milk solids, raising agents (INS 503(i), INS 500(i)), salt, emulsifier (soya lecithin INS 322)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063136779,Good Day Choco Almond,Britannia,"Refined wheat flour, edible vegetable oil (palm), sugar, cocoa solids, almond (3%), invert syrup, milk solids, raising agents (INS 503(i), INS 500(i)), salt, emulsifier (soya lecithin INS 322)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063092440,Good Day Butter,Britannia,"Refined wheat flour, edible vegetable oil (palm), sugar, butter (1%), invert syrup, milk solids, raising agents (INS 503(i), INS 500(i)), salt, emulsifier (soya lecithin INS 322), artificial butter flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063146938,Winkin' Cow Bourbon Shake,Britannia,"Toned milk, sugar, cocoa solids, artificial chocolate flavour, stabilizers (INS 466, INS 407), emulsifier (INS 471), colour (INS 150c)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063146952,Winkin' Cow Strawberry Shake,Britannia,"Toned milk, sugar, strawberry flavour, stabilizers (INS 466, INS 407), emulsifier (INS 471), colour (INS 122)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901719112577,Hide & Seek Milano (Choco Chip),Parle,"Refined wheat flour, sugar, edible vegetable oil (palm), cocoa solids, choco chips, invert syrup, milk solids, raising agents (INS 503(ii), INS 500(ii)), emulsifier (INS 322), artificial chocolate flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901719115608,Hide & Seek 120g Orange Sandwiches,Parle,"Refined wheat flour, sugar, edible vegetable oil (palm), orange flavour, invert syrup, raising agents (INS 503(ii), INS 500(ii)), salt, emulsifier (INS 322), colours (INS 110)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901719115639,Hide & Seek 120g Creme Sandwiches Chocochip,Parle,"Refined wheat flour, sugar, edible vegetable oil (palm), cocoa solids, choco chips, invert syrup, milk solids, raising agents (INS 503(ii), INS 500(ii)), emulsifier (INS 322), artificial chocolate flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901719703034,Krackjack Original,Parle,"Refined wheat flour, sugar, edible vegetable oil (palm), invert syrup, salt, raising agents (INS 503(ii), INS 500(ii)), emulsifier (INS 322), artificial butter flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901719123788,Parle Monaco Classic Salted,Parle,"Refined wheat flour, edible vegetable oil (palm), salt, sugar, raising agents (INS 503(ii), INS 500(ii)), emulsifier (INS 322), artificial butter flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901719114038,Fab! Jam,Parle,"Refined wheat flour, sugar, fruit jam (pineapple, apple), edible vegetable oil (palm), invert syrup, raising agents (INS 503(ii), INS 500(ii)), salt, emulsifier (INS 322), colours (INS 110, INS 102)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901719101663,Parle-G Gold Original,Parle,"Refined wheat flour, sugar, invert syrup, refined palm oil, salt, skimmed milk powder, raising agents (INS 503(ii), INS 500(ii)), emulsifier (INS 471), dough conditioner, artificial vanilla flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901719119286,Mango Bite,Parle,"Sugar, glucose syrup, mango pulp, acidity regulator (INS 330), artificial mango flavour, colour (INS 160c)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901058901580,Maggi Special Masala Noodles,Maggi,"Noodles: Refined wheat flour, palm oil, iodized salt, wheat gluten, thickeners (INS 508, INS 412), acidity regulators; Tastemaker: salt, spices (onion, garlic, chilli, coriander, turmeric), sugar, flavour enhancers (INS 621), antioxidant (INS 319)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901058854107,Maggi Oats Masala Noodles,Maggi,"Oats flour, refined wheat flour, palm oil, iodized salt, wheat gluten, thickeners (INS 508, INS 412), acidity regulators; Tastemaker: salt, spices, sugar, flavour enhancers (INS 621), antioxidant (INS 319)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901058016222,Maggi Rich Tomato Ketchup,Maggi,"Tomato paste, sugar, water, vinegar, salt, spices (onion, garlic, chilli), acidity regulator (INS 260), preservative (INS 211)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901058008388,Maggi Hot Sweet Tomato Chilli Sauce,Maggi,"Tomato paste, sugar, water, vinegar, salt, chilli, garlic, acidity regulator (INS 260), preservative (INS 211), thickener (INS 1422)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901058003055,Maggi Pazzta Cheese Macaroni,Maggi,"Macaroni: Durum wheat semolina, salt; Tastemaker: milk solids, cheese powder, sugar, salt, palm oil, thickeners (INS 1422, INS 412), flavour enhancers (INS 621, INS 627, INS 631), artificial cheese flavour, colour (INS 160a)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901058014846,Maggi Pazzta Cheesy Tomato Twist,Maggi,"Macaroni: Durum wheat semolina, salt; Tastemaker: tomato powder, milk solids, sugar, salt, palm oil, thickeners (INS 1422, INS 412), flavour enhancers (INS 621, INS 627, INS 631), artificial cheese flavour, colour (INS 160c)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901058006032,Maggi Cup Noodles Masala,Maggi,"Noodles: Refined wheat flour, palm oil, salt, wheat gluten, thickeners, acidity regulators; Tastemaker: salt, spices, sugar, dehydrated vegetables, flavour enhancers (INS 621, INS 627, INS 631), antioxidant (INS 319)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901058013665,Maggi Hot and Sweet Noodles,Maggi,"Noodles: Refined wheat flour, palm oil, salt, wheat gluten, thickeners, acidity regulators; Tastemaker: salt, sugar, chilli, garlic, spices, flavour enhancers (INS 621), antioxidant (INS 319)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904063254696,Aloo Bhujia,Haldiram's,"Potato flakes & starch, edible vegetable oil (palmolein), gram flour, iodized salt, spices (red chilli, cumin), colour (INS 160c)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904004403770,Moong Dal,Haldiram's,"Moong dal, edible vegetable oil (palmolein), iodized salt, spices (red chilli, black pepper, asafoetida)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904004403534,Tasty Nuts,Haldiram's,"Peanuts, edible vegetable oil (palmolein), iodized salt, spices (red chilli, black pepper)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904063216403,Khatta Meetha,Haldiram's,"Rice flakes, edible vegetable oil (palmolein), sugar, peanuts, sago, iodized salt, spices, raising agents, colours (INS 160c)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904063216168,Bombay Mix,Haldiram's,"Rice flakes, gram flour, edible vegetable oil (palmolein), peanuts, sago, iodized salt, spices, raising agents, colours (INS 160c)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904063230133,Cornflakes Mixture,Haldiram's,"Corn flakes, edible vegetable oil (palmolein), peanuts, sago, iodized salt, spices, sugar, raising agents, colours (INS 160c)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904063214942,All In One Mixture,Haldiram's,"Rice flakes, gram flour, edible vegetable oil (palmolein), peanuts, sago, iodized salt, spices, curry leaves, raising agents, colours (INS 160c)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904063254450,Punjabi Tadka,Haldiram's,"Rice flakes, gram flour, edible vegetable oil (palmolein), peanuts, sago, iodized salt, spices (cumin, turmeric, red chilli), raising agents, colours (INS 160c)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901725005900,Yippee! Noodles Magic Masala,Sunfeast,"Instant noodles: Refined wheat flour (78.4%), refined palm oil, iodized salt, wheat gluten, thickeners (INS 508, INS 412); Masala: spices, dehydrated vegetables, sugar, salt, flavour enhancers (INS 621, INS 627, INS 631)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901725015916,Dark Fantasy Original,Sunfeast,"Choco crème (sugar, refined palmolein, refined palm oil, cocoa solids), refined wheat flour, sugar, invert syrup, liquid glucose, edible vegetable oil, cocoa solids, milk solids, butter, raising agents (INS 503(ii), INS 500(i)), emulsifiers (INS 322, INS 471), salt",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901725016265,Dark Fantasy Bourbon,Sunfeast,"Refined wheat flour, sugar, edible vegetable oil (palm), cocoa solids, invert syrup, raising agents (INS 503(ii), INS 500(i)), emulsifiers (INS 322, INS 471), salt, artificial chocolate flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901725017545,Nice,Sunfeast,"Refined wheat flour, sugar, coconut, edible vegetable oil (palm), invert syrup, raising agents (INS 503(ii), INS 500(ii)), salt, emulsifier (INS 322), artificial coconut flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901725000622,Mom's Magic Cashew & Almond,Sunfeast,"Refined wheat flour, sugar, edible vegetable oil (palm), cashew nuts, almonds, invert syrup, milk solids, raising agents, emulsifiers",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901725006143,Marie Light,Sunfeast,"Refined wheat flour, sugar, refined palm oil, invert sugar syrup, milk solids, raising agents, salt, emulsifiers",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901725013714,Bingo Mad Angles Achaari Masti,Bingo,"Corn grits, edible vegetable oil (palmolein), rice grits, gram flour, spices, salt, sugar, flavour enhancers (INS 621, INS 627, INS 631), acidity regulators, colours (INS 160c)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901725004217,Bingo Tedhe Medhe Tomato,Bingo,"Corn grits, edible vegetable oil (palmolein), rice grits, gram flour, spices, salt, sugar, tomato powder, flavour enhancers (INS 621, INS 627, INS 631), acidity regulators, colours (INS 160c)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901262150095,Amul Gold Milk 200ml,Amul,"Standardized milk (4.5% fat, 8.5% SNF), vitamins A & D",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901262153577,Amul Taaza Toned Milk 200ml,Amul,"Toned milk (3.0% fat, 8.5% SNF), vitamins A & D",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901262010436,Amul White Unsalted Butter,Amul,"Pasteurized milk cream",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901262200271,Amul Dahi,Amul,"Pasteurized toned milk, active lactic culture",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901262180030,Amul Paneer,Amul,"Milk solids, citric acid (coagulant)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901262020404,Amul Cheese Slices,Amul,"Milk solids, salt, emulsifying salts (INS 331, INS 452), preservative (INS 200), colour (INS 160a)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901233034300,Cadbury Dairy Milk Silk Bubbly,Cadbury,"Sugar, milk solids, cocoa butter, cocoa mass, emulsifiers (soya lecithin INS 322, INS 476), flavours (natural & nature-identical vanilla)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901233034263,Cadbury Dairy Milk Roast Almond,Cadbury,"Sugar, milk solids, cocoa butter, cocoa mass, almonds (15%), emulsifiers (soya lecithin INS 322, INS 476), flavours",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901233033563,Cadbury Dairy Milk Silk Minis,Cadbury,"Sugar, milk solids, cocoa butter, cocoa mass, emulsifiers (soya lecithin INS 322, INS 476), flavours (natural & nature-identical vanilla)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901233013091,Cadbury Oreo Small Pack,Cadbury,"Refined wheat flour, sugar, refined palm oil, cocoa solids (5%), invert syrup, raising agents (INS 503(ii), INS 500(i)), salt, emulsifier (soya lecithin INS 322), artificial vanilla flavour, antioxidant (INS 319)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906015340174,Everest Garam Masala,Everest,"Coriander, cumin, black pepper, cloves, cinnamon, cardamom, bay leaf, nutmeg",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901786165001,Everest Chicken Masala,Everest,"Coriander, cumin, turmeric, black pepper, red chilli, cloves, cinnamon, cardamom, garlic, ginger",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8902167000782,MDH Garam Masala,MDH,"Coriander, cumin, black pepper, cloves, cinnamon, cardamom, bay leaf",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8902167000751,MDH Kitchen King,MDH,"Coriander, turmeric, red chilli, cumin, black pepper, cloves, cinnamon, cardamom",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901192101013,Catch Black Pepper Powder,Catch,"100% black pepper",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901192105011,Catch Amchur Powder,Catch,"100% dried mango powder",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901030831706,Kissan Mixed Fruit Jam,HUL/Kissan,"Sugar, mixed fruit pulp blend (approx. 46%) [banana, apple, pineapple, orange, mango, papaya], acidity regulator (INS 330), preservative (INS 211 sodium benzoate), permitted synthetic food colour (INS 122)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906069402774,Veeba Mayonnaise (Eggless),Veeba,"Refined soybean oil, water, sugar, vinegar, iodized salt, thickener (INS 1422), preservative (INS 211), mustard, antioxidant (INS 319)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063342910,Britannia Brown Bread,Britannia,"Whole wheat flour (approx. 50%), refined wheat flour, water, sugar, edible vegetable oil, gluten, yeast, iodized salt, preservative (INS 282), emulsifiers (INS 471, INS 472e)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063012578,Britannia Milk Bikis,Britannia,"Refined wheat flour, sugar, milk solids, edible vegetable oil (palm), invert syrup, raising agents (INS 503(ii), INS 500(ii)), salt, emulsifier (INS 322), artificial vanilla flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063017399,Britannia 50-50 Maska Chaska,Britannia,"Refined wheat flour, sugar, edible vegetable oil (palm), invert syrup, salt, raising agents (INS 503(ii), INS 500(ii)), emulsifier (INS 322), artificial butter flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063026346,Britannia NutriChoice Digestive,Britannia,"Whole wheat flour (71%), sugar, edible vegetable oil (palm), raising agents (INS 503(ii), INS 500(ii)), salt, emulsifiers (INS 471, INS 322), added vitamins & minerals",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063162303,Britannia Marie Gold,Britannia,"Refined wheat flour (73%), sugar, refined palm oil, invert sugar syrup, milk solids & sweetened condensed milk, raising agents (INS 503(ii), INS 500(ii)), salt, emulsifiers (INS 471, INS 322)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063092709,Britannia Good Day Cashew,Britannia,"Refined wheat flour, edible vegetable oil (palm), sugar, cashew nuts (4.5%), invert syrup, milk solids, butter (0.6%), raising agents (INS 503(i), INS 500(i)), salt, emulsifier (soya lecithin INS 322)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901030825668,Horlicks Classic Malt 500g,HUL,"Malted cereals (66.7%) [barley, wheat flour, wheat, millet], milk solids (14%), sugar, wheat gluten, iodized salt, minerals, vitamins, emulsifier (INS 471)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8909106018372,Boost,HUL,"Cereal extract (50%) [barley, wheat, millet], malted barley (21%), sugar, wheat flour, milk solids (6%), minerals, natural colour (INS 150c), vitamins",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901030882609,Brooke Bond Red Label 1kg,HUL,"100% black tea (CTC dust & fannings blend)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901030251504,Brooke Bond Taj Mahal,HUL,"100% black tea (CTC blend)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901058016055,Nescafé Classic,Nestlé,"100% instant coffee",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901030373930,Bru Gold Instant Coffee,HUL,"100% instant coffee (freeze-dried)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906112662414,True Elements Rolled Oats,True Elements,"100% wholegrain rolled oats",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901725008888,Aashirvaad Shudh Chakki Atta,Aashirvaad,"100% whole wheat flour (chakki-ground)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
"""

reader = csv.DictReader(io.StringIO(verified_batch5_csv.strip()))
batch5_rows = [r for r in reader]

print(f"Parsed {len(batch5_rows)} products from verified_batch5.")

elevated_count = 0
added_direct_count = 0
updated_c_count = 0

c_barcodes = set(df_c['barcode'].tolist())
nv_barcodes = set(df_nv['barcode'].tolist())

for row in batch5_rows:
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
    
    if bc in c_barcodes:
        idx = df_c[df_c['barcode'] == bc].index[0]
        df_c.at[idx, 'product_name'] = p_name
        df_c.at[idx, 'brands'] = brand
        df_c.at[idx, 'ingredients_text'] = ing
        df_c.at[idx, 'ingredient_confidence'] = 'HIGH'
        updated_c_count += 1
    elif bc in nv_barcodes:
        df_nv = df_nv[df_nv['barcode'] != bc]
        nv_barcodes.remove(bc)
        df_c = pd.concat([df_c, pd.DataFrame([new_c_row])], ignore_index=True)
        c_barcodes.add(bc)
        elevated_count += 1
    else:
        df_c = pd.concat([df_c, pd.DataFrame([new_c_row])], ignore_index=True)
        c_barcodes.add(bc)
        added_direct_count += 1

print(f"Batch5 Processing Results:")
print(f"  Elevated from Needs Verification: {elevated_count}")
print(f"  Added direct to Confirmed: {added_direct_count}")
print(f"  Updated in Confirmed: {updated_c_count}")

# Save datasets back
df_c.to_csv(confirmed_path, index=False)
df_nv.to_csv(needs_ver_path, index=False)
df_rem.to_csv(removed_path, index=False)

print("\nSaved files successfully.")
