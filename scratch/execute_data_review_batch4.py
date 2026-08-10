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

# 2. PURGES (Non-food / Invalid / Typo)
barcodes_to_purge = {
    '8901396126027': 'Lizol Citrus - non-food floor cleaner',
    '8901030843150': 'Surf Excel Value Pack - non-food detergent',
    '8909106007123': 'Vim Extra Bar Anti Smell - non-food dish soap',
    '8901030700224': 'Tresemme hair fall defense - non-food shampoo',
    '8909106055469': 'Surf Excel Top Load Liquid - non-food detergent',
    '8901030865169': 'Surf Excel bar 250gm - non-food detergent',
    '8901177101014': 'Moov - non-food pain relief balm',
    '8904091106400': 'Ascoril TABLETS - non-food medicine',
    '8901023019371': 'RAT GLUE PAD - non-food pest control',
    '8901138110611': 'Liv.52 tabs - non-food medicine',
    '8902618000019': 'Woodwards - non-food medicine',
    '89080658': 'Maggi - invalid short barcode',
    '8901571004560': 'Loading... - OCR UI artifact',
    '8904030852306': 'Chargement... - OCR UI artifact',
    '8901526406883': 'OCR garbage text',
    '8901719111441': 'hi - nonsense OCR word'
}

purged_count = 0
for bc, reason in barcodes_to_purge.items():
    c_match = df_c[df_c['barcode'] == bc]
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

print(f"Purged {purged_count} products and moved them to removed file.")

# 3. MERGES
duplicates_to_merge = [
    ('8902901221831', '8902901225075')  # masoor whole
]

merged_count = 0
for canon_bc, dup_bc in duplicates_to_merge:
    dup_in_c = df_c[df_c['barcode'] == dup_bc]
    dup_in_nv = df_nv[df_nv['barcode'] == dup_bc]
    
    if not dup_in_c.empty:
        df_c = df_c[df_c['barcode'] != dup_bc]
        merged_count += 1
    if not dup_in_nv.empty:
        df_nv = df_nv[df_nv['barcode'] != dup_bc]
        merged_count += 1

print(f"Merged and removed {merged_count} duplicate barcode listings.")

# 4. DATA QUALITY CORRECTIONS & TYPOS
corrections = {
    '8908007836504': {'brands': 'Local/Regional Dairy', 'product_name': 'Ghee'},
    '8904083518150': {'brands': '24 Mantra Organic', 'product_name': 'Brown Rice'},
    '8901808000747': {'brands': 'Weikfield', 'product_name': 'Baking Powder'},
    '8904132948174': {'brands': 'Campa', 'product_name': 'Campa Cola 500ml'},
    '8901063370166': {'brands': 'Britannia', 'product_name': 'Good Day'},
    '8901063371026': {'brands': 'Britannia', 'product_name': 'Marie Gold'},
    '8901063371019': {'brands': 'Britannia', 'product_name': 'Marie Gold'},
    '8901063093737': {'brands': 'Britannia', 'product_name': 'Good Day'},
    '8901063092747': {'brands': 'Britannia', 'product_name': 'Good Day'},
    '8901063092846': {'brands': 'Britannia', 'product_name': 'Good Day'},
    '8901063094291': {'brands': 'Britannia', 'product_name': 'Good Day Pista Badam Cookies'},
    '8901063092464': {'brands': 'Britannia', 'product_name': 'Good Day Cashew'},
    '8901063093720': {'brands': 'Britannia', 'product_name': 'Good Day Cashew Cookies'},
    '8901719255144': {'brands': 'Parle', 'product_name': 'Parle-G'},
    '8901719255168': {'brands': 'Parle', 'product_name': 'Parle-G'},
    '8901719404412': {'brands': 'Parle', 'product_name': 'Hide & Seek'},
    '8901719703034': {'brands': 'Parle', 'product_name': 'Krackjack Original'},
    '8901719136740': {'brands': 'Parle', 'product_name': 'Hide & Seek'},
    '8901719136771': {'brands': 'Parle', 'product_name': 'Hide & Seek 100g'},
    '8901719133756': {'brands': 'Parle', 'product_name': 'Hide & Seek 75gm'},
    '8901719136665': {'brands': 'Parle', 'product_name': 'Parle-G Jam-In'},
    '8901719115608': {'brands': 'Parle', 'product_name': 'Hide & Seek Sandwich Orange'},
    '8901719115639': {'brands': 'Parle', 'product_name': 'Hide & Seek Chocolate Cream Sandwich'},
    '8901719112577': {'brands': 'Parle', 'product_name': 'Hide & Seek Milano Chocochip'},
    '8901719258619': {'brands': 'Parle', 'product_name': 'Bourbon'},
    '8901719135316': {'brands': 'Parle', 'product_name': 'Krackjack'},
    '8909081001475': {'brands': 'Sunfeast/ITC', 'product_name': 'Yippee Tricolor Pasta Masala'},
    '8909106029842': {'brands': 'Knorr', 'product_name': 'Knorr Tandoori Soup'},
    '8909106035256': {'brands': 'Knorr', 'product_name': 'Knorr Broccoli Soup'},
    '8909106048584': {'brands': 'Knorr', 'product_name': 'Knorr Manchow Vegetable Soup'},
    '8901764051258': {'brands': 'Coca-Cola', 'product_name': 'Limca'},
    '8901764042300': {'brands': 'Coca-Cola', 'product_name': 'Thums Up Charged'},
    '8904132944671': {'brands': 'Campa', 'product_name': 'Campa Cola'},
    '8904132944688': {'brands': 'Campa', 'product_name': 'Campa Lime & Lemon'},
    '8904132944695': {'brands': 'Campa', 'product_name': 'Campa Orange'},
    '8904132949737': {'brands': 'Campa', 'product_name': 'Campa Cola'},
    '8904132975552': {'brands': 'Campa', 'product_name': 'Campa Soda'},
    '8904132975774': {'brands': 'Campa', 'product_name': 'Campa Power Up'},
    '8902901224818': {'brands': 'Good Life', 'product_name': 'Urad Dal Chhilk'},
    '8902901221831': {'brands': 'Good Life', 'product_name': 'Masoor Whole'},
    '8902901224689': {'brands': 'Good Life', 'product_name': 'Moong Dal Chhilka'},
    '8902901001778': {'brands': 'Good Life', 'product_name': 'Broken Wheat'},
    '8902901030556': {'brands': 'Good Life', 'product_name': 'Atta', 'ingredients_text': ''},
    '8903023260845': {'brands': 'More', 'product_name': 'More Choice Raw Peanuts'},
    '8903023267424': {'brands': 'More', 'product_name': 'Tili White'},
    '8903023007709': {'brands': 'More', 'product_name': 'Chironji'},
}

updated_fields = 0
for bc, fields in corrections.items():
    idx_c = df_c[df_c['barcode'] == bc].index
    if not idx_c.empty:
        for f, val in fields.items():
            df_c.at[idx_c[0], f] = val
        updated_fields += 1
    idx_nv = df_nv[df_nv['barcode'] == bc].index
    if not idx_nv.empty:
        for f, val in fields.items():
            df_nv.at[idx_nv[0], f] = val
        updated_fields += 1

print(f"Corrected fields for {updated_fields} products.")

# 5. IMPORT VERIFIED BATCH 4 DATA
verified_batch4_csv = """barcode,product_name,brands,ingredients_text,sold_in_india_status,ingredient_confidence,status,data_source,source_license,collection_method
8901233013091,Cadbury Oreo Small Pack,Cadbury,"Refined wheat flour, sugar, refined palm oil, cocoa solids (5%), invert syrup, raising agents (INS 503(ii), INS 500(i)), salt, emulsifier (soya lecithin INS 322), artificial vanilla flavour, antioxidant (INS 319)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901233034300,Cadbury Dairy Milk Silk Bubbly,Cadbury,"Sugar, milk solids, cocoa butter, cocoa mass, emulsifiers (soya lecithin INS 322, INS 476), flavours (natural & nature-identical vanilla)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901233034263,Cadbury Dairy Milk Roast Almond,Cadbury,"Sugar, milk solids, cocoa butter, cocoa mass, almonds (15%), emulsifiers (soya lecithin INS 322, INS 476), flavours",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901233033563,Cadbury Dairy Milk Silk Minis,Cadbury,"Sugar, milk solids, cocoa butter, cocoa mass, emulsifiers (soya lecithin INS 322, INS 476), flavours (natural & nature-identical vanilla)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901764042508,Thums Up 2L,Coca-Cola,"Carbonated water, sugar, acidity regulator (INS 338), colour (INS 150d), natural & nature-identical flavouring (cola), caffeine",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901764052408,Limca 2L,Coca-Cola,"Carbonated water, sugar, acidity regulators (INS 330, INS 331(i)), stabilizers (INS 414, INS 471), preservative (INS 211), lime-lemon flavouring",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901764042324,Thums Up Charged,Coca-Cola,"Carbonated water, sugar, acidity regulators (INS 338, INS 330), caffeine, taurine, colour (INS 150d), natural flavours, vitamins",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904132949676,Campa Cola 500ml,Campa,"Carbonated water, sugar, acidity regulator (INS 338), colour (INS 150d), natural & nature-identical flavouring (cola), caffeine",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904132944695,Campa Orange 500ml,Campa,"Carbonated water, sugar, acidity regulators (INS 330, INS 331(iii)), orange juice concentrate (3%), colours (INS 110, INS 102), artificial orange flavour, preservative (INS 211)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904132975552,Campa Soda,Campa,"Carbonated water, salt, acidity regulator (INS 330)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8902080013500,Tropicana Mixed Fruit Juice,Tropicana,"Water, mixed fruit juice concentrate (apple, grape, mango, orange, pineapple), sugar, acidity regulator (INS 330), antioxidant (INS 300), natural flavours",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8902080003075,Nimbooz,7Up/PepsiCo,"Carbonated water, sugar, acidity regulators (INS 330, INS 331(i)), natural lemon-lime flavouring, preservative (INS 211)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8902579002121,Appy Fizz,Parle Agro,"Carbonated water, sugar, apple juice concentrate, acidity regulators (INS 330, INS 331(iii)), preservative (INS 211), colour (INS 150d), flavouring",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901491003896,Lay's Korean Chilli,Lay's,"Potato, edible vegetable oil (palmolein/rice bran), seasoning [sugar, iodized salt, spices & condiments (chilli, garlic, onion), flavour enhancers (INS 621, INS 627, INS 631), acidity regulators (INS 330, INS 296), colours (INS 160c)]",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901491103060,Kurkure Hyderabadi Hungama,Kurkure,"Corn grits, edible vegetable oil (palmolein), rice grits, gram flour, spices, salt, sugar, flavour enhancers (INS 621, INS 627, INS 631), acidity regulators, colours (INS 160c)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901491103282,Cheetos,PepsiCo India,"Corn grits, edible vegetable oil (palmolein), cheese seasoning [cheese powder, milk solids, salt, sugar, flavour enhancers (INS 621, INS 627, INS 631), colours (INS 160c, INS 160a)]",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901725013721,Bingo Mad Angles Very Peri Peri,Bingo,"Corn grits, edible vegetable oil (palmolein), rice grits, gram flour, spices, salt, sugar, peri peri seasoning, flavour enhancers (INS 621, INS 627, INS 631), acidity regulators, colours (INS 160c)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904063254450,Haldiram's Punjabi Tadka,Haldiram's,"Rice flakes, gram flour, edible vegetable oil (palmolein), peanuts, sago, iodized salt, spices (cumin, turmeric, red chilli), raising agents, colours (INS 160c)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904063253415,Haldiram's Roasted Chana Cracker Heeng Jeera,Haldiram's,"Roasted chana, edible vegetable oil (palmolein), iodized salt, spices (asafoetida, cumin, red chilli)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904004419511,Haldiram's South Mixture,Haldiram's,"Rice flakes, gram flour, edible vegetable oil (palmolein), peanuts, sago, iodized salt, spices, curry leaves, raising agents, colours (INS 160c)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901030825668,Horlicks Classic Malt 500g,HUL,"Malted cereals (66.7%) [barley, wheat flour, wheat, millet], milk solids (14%), sugar, wheat gluten, iodized salt, minerals, vitamins, emulsifier (INS 471)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901030825521,Horlicks Protein Plus Chocolate,HUL,"Milk solids, malted cereals, sugar, cocoa solids, wheat flour, minerals, vitamins, emulsifier (INS 471), artificial chocolate flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8909106018372,Boost,HUL,"Cereal extract (50%) [barley, wheat, millet], malted barley (21%), sugar, wheat flour, milk solids (6%), minerals, natural colour (INS 150c), vitamins",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901888004451,Glucose-D,Dabur,"Dextrose monohydrate, vitamin C, acidity regulator (INS 330), artificial orange flavour, colour (INS 110)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901030882609,Brooke Bond Red Label 1kg,HUL,"100% black tea (CTC dust & fannings blend)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901030251504,Brooke Bond Taj Mahal,HUL,"100% black tea (CTC blend)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901030559297,Lipton Darjeeling Tea,HUL,"100% Darjeeling black tea",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901030781070,Lipton Green Tea,HUL,"100% green tea leaves",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901030985577,3 Roses Tea,HUL,"100% black tea (CTC blend)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901030373930,Bru Gold Instant Coffee,HUL,"100% instant coffee (freeze-dried)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901262020404,Amul Cheese Slices,Amul,"Milk solids, salt, emulsifying salts (INS 331, INS 452), preservative (INS 200), colour (INS 160a)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901262020091,Amul Cheese Cubes,Amul,"Milk solids, salt, emulsifying salts (INS 331, INS 452), preservative (INS 200)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901262260954,Amul Buffalo Milk,Amul,"Buffalo milk (standardized)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901777965184,Vadilal Classic Malai Kulfi,Vadilal,"Toned milk, sugar, milk fat, cardamom, stabilizers (INS 410, INS 412, INS 466), emulsifier (INS 471)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901826601100,Verka Gold Ghee,Verka,"Milk solids (pure cow ghee)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906015340174,Everest Garam Masala,Everest,"Coriander, cumin, black pepper, cloves, cinnamon, cardamom, bay leaf, nutmeg",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901786165001,Everest Chicken Masala,Everest,"Coriander, cumin, turmeric, black pepper, red chilli, cloves, cinnamon, cardamom, garlic, ginger",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901786270507,Everest Dry Mango Powder,Everest,"100% dried mango powder",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8902167000782,MDH Garam Masala,MDH,"Coriander, cumin, black pepper, cloves, cinnamon, cardamom, bay leaf",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8902167000751,MDH Kitchen King,MDH,"Coriander, turmeric, red chilli, cumin, black pepper, cloves, cinnamon, cardamom",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8902167000829,MDH Meat Ka Masala,MDH,"Coriander, cumin, turmeric, red chilli, black pepper, cloves, cinnamon, cardamom, garlic, ginger, fennel",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901192101013,Catch Black Pepper Powder,Catch,"100% black pepper",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901192105011,Catch Amchur Powder,Catch,"100% dried mango powder",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901192221018,Catch Chhole Masala,Catch,"Coriander, cumin, turmeric, red chilli, black pepper, cloves, cinnamon, cardamom, amchur, ginger",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901192215017,Catch Sabzi Masala,Catch,"Coriander, cumin, turmeric, red chilli, black pepper, cloves, cinnamon, cardamom",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901192217110,Catch Jaljeera,Catch,"Cumin, black salt, dried mango powder, red chilli, black pepper, mint, ginger",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901058016222,Maggi Rich Tomato Ketchup,Maggi,"Tomato paste, sugar, water, vinegar, salt, spices, acidity regulator (INS 260), preservative (INS 211)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901058001167,Maggi Pichkoo,Maggi,"Tomato paste, sugar, water, vinegar, salt, spices, acidity regulator (INS 260), preservative (INS 211)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063018297,Britannia Time Pass,Britannia,"Refined wheat flour, sugar, edible vegetable oil (palm), invert syrup, raising agents (INS 503(ii), INS 500(ii)), salt, emulsifier (INS 322), artificial flavours",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063138162,Britannia NutriChoice Arrowroot,Britannia,"Whole wheat flour, arrowroot flour, sugar, edible vegetable oil (palm), raising agents, salt, emulsifiers, added vitamins & minerals",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063325586,Britannia Toastea Bilk Rusk,Britannia,"Refined wheat flour, sugar, edible vegetable oil (palm), invert syrup, milk solids, raising agents (INS 503(ii), INS 500(ii)), salt, emulsifier (INS 322), artificial vanilla flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063367357,Britannia Gol Maal 50-50,Britannia,"Refined wheat flour, sugar, edible vegetable oil (palm), invert syrup, salt, raising agents (INS 503(ii), INS 500(ii)), emulsifier (INS 322), artificial butter flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901725000622,Sunfeast Mom's Magic Cashew & Almond,Sunfeast,"Refined wheat flour, sugar, edible vegetable oil (palm), cashew nuts, almonds, invert syrup, milk solids, raising agents, emulsifiers",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901725006143,Sunfeast Marie Light,Sunfeast,"Refined wheat flour, sugar, refined palm oil, invert sugar syrup, milk solids, raising agents, salt, emulsifiers",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901928131505,Bisk Farm Nice,Bisk Farm,"Refined wheat flour, sugar, coconut, edible vegetable oil (palm), invert syrup, raising agents, salt, emulsifier, artificial coconut flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906033746040,McVitie's Hobnobs Oats Cookies,McVitie's,"Whole wheat flour, oats, sugar, edible vegetable oil (palm), invert syrup, raising agents, salt, emulsifiers",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901030831706,Kissan Mixed Fruit Jam,HUL/Kissan,"Sugar, mixed fruit pulp blend (approx. 46%) [banana, apple, pineapple, orange, mango, papaya], acidity regulator (INS 330), preservative (INS 211 sodium benzoate), permitted synthetic food colour (INS 122)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906069402774,Veeba Mayonnaise (Eggless),Veeba,"Refined soybean oil, water, sugar, vinegar, iodized salt, thickener (INS 1422), preservative (INS 211), mustard, antioxidant (INS 319)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8908012605003,Heinz Tomato Ketchup,Heinz,"Tomato paste, sugar, vinegar, salt, spices, acidity regulator (INS 260), preservative (INS 211)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901246003621,Del Monte Sliced Green Olives,Del Monte,"Green olives, water, salt, acidity regulator (INS 330)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906112662414,True Elements Rolled Oats,True Elements,"100% wholegrain rolled oats",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904043906584,Tata Sampann Chia Seeds,Tata Sampann,"100% chia seeds",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901725002428,Aashirvaad Garlic & Coriander Naan,Aashirvaad,"Refined wheat flour, water, edible vegetable oil, garlic, coriander, salt, sugar, raising agents, preservative (INS 282)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
"""

reader = csv.DictReader(io.StringIO(verified_batch4_csv.strip()))
batch4_rows = [r for r in reader]

print(f"Parsed {len(batch4_rows)} products from verified_batch4.")

elevated_count = 0
added_direct_count = 0
updated_c_count = 0

c_barcodes = set(df_c['barcode'].tolist())
nv_barcodes = set(df_nv['barcode'].tolist())

for row in batch4_rows:
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

print(f"Batch4 Processing Results:")
print(f"  Elevated from Needs Verification: {elevated_count}")
print(f"  Added direct to Confirmed: {added_direct_count}")
print(f"  Updated in Confirmed: {updated_c_count}")

# Save datasets back
df_c.to_csv(confirmed_path, index=False)
df_nv.to_csv(needs_ver_path, index=False)
df_rem.to_csv(removed_path, index=False)

print("\nSaved files successfully.")
