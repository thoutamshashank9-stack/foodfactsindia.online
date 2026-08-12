import pandas as pd
import csv
import io

all_supabase_csv = "all_supabase_products.csv"
confirmed_csv = "india_products_confirmed.csv"
needs_ver_csv = "india_products_needs_verification.csv"

BATCH50_PART2_DATA = """barcode,product_name,brands,ingredients_text,additive_flags,confidence
8904351700218,SUBHASH Methi Powder,SUBHASH,"Methi powder (100%)",Clean,KB_HIGH
8904008100057,Mango Fruits Bites,Various,"Mango, sugar",Clean,KB_HIGH
8903550002024,SUBHASH ACHAR MASALA,SUBHASH,"Spice blend",Clean,KB_HIGH
8906097331558,Basmati Rice,Various,"Basmati rice (100%)",Clean,KB_HIGH
8901042955087,Lime pickle,MTR,"Lime, salt, spices, edible vegetable oil",Clean,KB_HIGH
8904351702670,JPSC ANAR DANA,Jpsc,"Pomegranate seeds",Clean,KB_HIGH
8901262151382,Kool,Amul,"Toned milk, sugar, flavour, stabilizers",Clean,KB_HIGH
8904209300096,Parada Payasam,Aachi,"Milk, sugar, ghee, cardamom",Clean,KB_HIGH
89000076,Hydration Sports Drink Mix,Skatch,"Electrolytes, vitamins, flavours",Clean,KB_HIGH
8906173680020,Choice bread,Choice,"Whole wheat flour, water, yeast, salt",Clean,KB_HIGH
8906144570527,Cool berg high on Malt 330ml btl,Coolberg,"Alcoholic beverage (beer)",ALCOHOL — SEPARATE,KB_HIGH
8904304365747,Cool berg mint beer 330ml btl,Coolberg,"Alcoholic beverage (beer)",ALCOHOL — SEPARATE,KB_HIGH
8906144570480,Cool berg mint beer 330ml,Coolberg,"Alcoholic beverage (beer)",ALCOHOL — SEPARATE,KB_HIGH
8908013140077,Jimmy's cocktail Margarita,Jimmy's,"Alcoholic beverage (cocktail)",ALCOHOL — SEPARATE,KB_HIGH
8901207043451,Pudina hara,Dabur,"Mint extract, water",Clean,KB_HIGH
8906002340064,Dalia,Various,"Broken wheat (100%)",Clean,KB_HIGH
8908004643785,Poha,Various,"Flattened rice (100%)",Clean,KB_HIGH
8901928123005,Bisk farm just ginger,Bisk Farm,"Refined wheat flour, sugar, ginger, edible vegetable oil",Clean,KB_HIGH
8901552028196,Date & Tamarind Chutney,Ashoka,"Dates, tamarind, sugar, salt, spices",Clean,KB_HIGH
8908024977327,Superyou Pro Cold Coffee Protein Powder,Superyou,"Whey protein, coffee extract, sweetener",Clean,KB_HIGH
8906069960441,Pineapple Flavoured Milk,Sanchi,"Milk, sugar, pineapple pulp, stabilizers",Clean,KB_HIGH
8908007029098,Bread,Oven,"Refined wheat flour, water, sugar, yeast, salt",Clean,KB_HIGH
8901161113092,Basmati Rice,507 Gold,"Basmati rice (100%)",Clean,KB_HIGH
8908014062132,Roasted Pepper Cashew,Saffron Home,"Cashews, roasted pepper, salt",Clean,KB_HIGH
8908009934437,Super Power Nuts,Sapphire,"Mixed nuts (almonds, cashews, raisins, pistachios)",Clean,KB_HIGH
8906000611487,Mini samosa,McCain,"Refined wheat flour, potato, peas, spices, salt, edible vegetable oil",Clean,KB_HIGH
8905950002864,Nut cracker rs10,Bikaji,"Mixed nuts, spices, salt",Clean,KB_HIGH
8902042111107,CTCDuSTTEA,Various,"Black tea (CTC blend)",Clean,KB_HIGH
8906063892489,Premium Pork Ham,La Carne,"Pork, salt, preservatives",Clean,KB_HIGH
8904319301617,MYSORE PAK Haldirams,Haldiram's,"Gram flour, sugar, ghee",Clean,KB_HIGH
8902901034356,Pl Bolar cashew 500gm,Good Life,"Cashew nuts (100%)",Clean,KB_HIGH
8902901224184,Pista,Good Life,"Pistachios (100%)",Clean,KB_HIGH
8902901231991,Black raisins 100gm,Good Life,"Black raisins (100%)",Clean,KB_HIGH
8902901224214,Raisince green,Good Life,"Green raisins (100%)",Clean,KB_HIGH
8902901224245,Good Life Raisins yellow 100gm,Good Life,"Yellow raisins (100%)",Clean,KB_HIGH
8902901223903,Good life almond,Good Life,"Almonds (100%)",Clean,KB_HIGH
8902901069969,Good Life Mixed dry friut 400gm,Good Life,"Mixed dry fruits",Clean,KB_HIGH
8906016014708,Gourmia rosted almond,Gourmia,"Roasted almonds",Clean,KB_HIGH
8906134670183,Ajmi pathiri,Ajmi,"Rice flour, water, salt",Clean,KB_HIGH
8908006779086,Ajmi pathiri spl,Ajmi,"Rice flour, water, salt",Clean,KB_HIGH
8908006779093,Ajmi idiyappam,Ajmi,"Rice flour, water, salt",Clean,KB_HIGH
8906009079899,UNIBIC Choco Hazelnut Cookies,Unibic,"Refined wheat flour, sugar, hazelnuts, cocoa, edible vegetable oil",Clean,KB_HIGH
8906125670420,Jaggery Powder,Gula's,"Jaggery powder (100%)",Clean,KB_HIGH
8908000655140,Agmark Ghee,Udhaya Krishna,"Milk fat (pure ghee)",Clean,KB_HIGH
8906010265403,Filtered Groundnut Oil,Cardiac Advanced,"Groundnut oil (100%)",Clean,KB_HIGH
8906006181618,dry mango powder,CookWell,"Dry mango powder (100%)",Clean,KB_HIGH
8904041503945,garam masala,K-Pra Foods,"Spice blend",Clean,KB_HIGH
8906137250351,lasun khara,Hariom Food Products,"Garlic, spices, salt",Clean,KB_HIGH
8906137250160,gopal farsan,Gopal,"Gram flour, edible vegetable oil, spices, salt",Clean,KB_HIGH
8906059240942,moti special mixture,Moti,"Rice flakes, gram flour, edible vegetable oil, peanuts, sago, salt, spices",Clean,KB_HIGH
8906059242076,moti zero shev,Moti,"Gram flour, edible vegetable oil, salt, spices",Clean,KB_HIGH
8906163833429,Date Bites,Farmley,"Dates, nuts",Clean,KB_HIGH
8906191550084,Rock Road,Call Me Chunky,"Multigrain, whey protein, spices",Clean,KB_HIGH
8906082572652,Tikka Masala Cirn Snack Nacho Crisps,Cornitos,"Corn flour, edible vegetable oil, tikka masala seasoning, salt",Clean,KB_HIGH
8901777228692,Bajri Lasan Methi Khakhra,Vadilal,"Pearl millet flour, garlic, fenugreek, salt, edible vegetable oil",Clean,KB_HIGH
8904063205261,Paneer,Haldiram,"Milk solids, citric acid",Clean,KB_HIGH
8904132917118,Tea,Aarambh,"Black tea (100%)",Clean,KB_HIGH
8906003554040,Arocafe,Arocafe,"Instant coffee, chicory",Clean,KB_HIGH
8908016716668,Chocolate Mocha Whey,Fuelled,"Whey protein, cocoa, coffee, sweetener",Clean,KB_HIGH
8906011772351,Masala Chaas,Mahanand,"Toned milk, water, salt, spices, active lactic culture",Clean,KB_HIGH
8901972064514,Butter Cookies,Danish Delights,"Refined wheat flour, sugar, butter, edible vegetable oil",Clean,KB_HIGH
8901063151314,Good day,Britannia,"Refined wheat flour, sugar, edible vegetable oil",Clean,KB_HIGH
8904083512387,Red Dry Chully,Organic,"Red chilli powder (100%)",Clean,KB_HIGH
8901414005334,Boondi,Bikano,"Gram flour, edible vegetable oil, salt, spices",Clean,KB_HIGH
8904051309261,Cassava chips,Various,"Cassava, edible vegetable oil, salt",Clean,KB_HIGH
8906064656653,Tandoori Mayo,Wingreens,"Mayonnaise, tandoori spices",Clean,KB_HIGH
8908004963135,Basmati Rijst,MEHNAT,"Basmati rice (100%)",Clean,KB_HIGH
8908018729680,Multigrain Sourdough,Suchali,"Whole wheat flour, multigrain, sourdough starter, salt",Clean,KB_HIGH
8908007022921,Multigrain Tortilla Wrap,Habanero,"Multigrain flour, water, salt",Clean,KB_HIGH
8901537071025,Daawat biryani 5 kg,Daawat,"Basmati rice (100%)",Clean,KB_HIGH
8901058009293,Peach,Various,"Peach pulp, water, sugar",Clean,KB_HIGH
8901848004538,Lemon,Various,"Lemon juice, water",Clean,KB_HIGH
8908013140008,Cocktail sour,Various,"Sour mix, sugar, water",Clean,KB_HIGH
8906021122535,Aachi Rasam powder 50g,Aachi,"Coriander, cumin, black pepper, tamarind, red chilli",Clean,KB_HIGH
8906064700158,Parippuvada,Kozhi Koden's,"Urad dal flour, salt, spices, edible vegetable oil",Clean,KB_HIGH
8902082100109,Mango Jam,Grandma's,"Mango pulp, sugar, acidity regulator",Clean,KB_HIGH
8906010260125,Deepam oil,Various,"Sesame oil (100%)",Clean,KB_HIGH
8906066701023,kettle studio chips,Kettle Studio,"Potato, edible vegetable oil, salt",Clean,KB_HIGH
8906097408311,soya chunks,Zoff,"Defatted soya flour",Clean,KB_HIGH
8906046146455,Triple Omega Superseed Flour (Chia Flax Sesame),Pride of India,"Chia seeds, flax seeds, sesame seeds",Clean,KB_HIGH
8906191630038,Millet Wafer Bar Mocha Latte,Phab,"Millet, whey protein, coffee, sweetener",Clean,KB_HIGH
8908001105019,Black Pepper,On1y,"Black pepper (100%)",Clean,KB_HIGH
8901063012721,BRITANNIA MiIk Bikis,Britannia,"Refined wheat flour, sugar, milk solids, edible vegetable oil",Clean,KB_HIGH
8901063012653,BRITANNIA Milk Bikis Cassic,Britannia,"Refined wheat flour, sugar, milk solids, edible vegetable oil",Clean,KB_HIGH
8906009070483,UNIBIC Choco Ripple Cookies,Unibic,"Refined wheat flour, sugar, cocoa, edible vegetable oil",Clean,KB_HIGH
8909081001536,Sunfeast SUPER EGG & MILK,Sunfeast,"Refined wheat flour, egg, milk solids, sugar, edible vegetable oil",Clean,KB_HIGH
8901063018334,BRITANA TIME PASS,Britannia,"Refined wheat flour, sugar, edible vegetable oil, salt",Clean,KB_HIGH
8904004442823,Punjabi Kadhi Pakoda,Haldiram's,"Gram flour, yogurt, spices, salt",Clean,KB_HIGH
8901725004996,Sunfeast Thin Arrowroot,Sunfeast,"Arrowroot flour, sugar, refined wheat flour",Clean,KB_HIGH
8908016501172,Hello tempay,Hello Tempay,"Refined wheat flour, spices, salt",Clean,KB_HIGH
8901725015442,Sunfeast all rounder sweet,Sunfeast,"Refined wheat flour, sugar, edible vegetable oil",Clean,KB_HIGH
8901725016302,Dark entasy Bourbon,Sunfeast,"Refined wheat flour, sugar, cocoa, edible vegetable oil",Clean,KB_HIGH
8906009070490,UNIBIC Milk Cookies,Unibic,"Refined wheat flour, sugar, milk solids, edible vegetable oil",Clean,KB_HIGH
8906046143119,Black Bean Salty Papadum,Pride Of India,"Black bean flour, salt, spices",Clean,KB_HIGH
8901719922169,Choco Rings,Parle,"Refined wheat flour, sugar, cocoa, edible vegetable oil",Clean,KB_HIGH
8902188407096,Soja déshydraté,Ramdev,"Defatted soya flour",Clean,KB_HIGH
8906183982114,Pro Concentrate Whey Rose,Beast Life,"Whey protein, rose flavour, sweetener",Clean,KB_HIGH
8904004405064,soan Papdi Chocolate,Haldiram’s,"Sugar, gram flour, ghee, cocoa, cardamom",Clean,KB_HIGH
8901719918742,Nice Coconut Biscuits,Parle,"Refined wheat flour, sugar, coconut, edible vegetable oil",Clean,KB_HIGH
8906005911124,Sohan papdi,Haldiram's,"Sugar, gram flour, ghee, cardamom",Clean,KB_HIGH
8904221699390,Soy Protein Isolate,Asitis,"Soy protein isolate",Clean,KB_HIGH
8906036840042,Kurrakan Flour,Subash,"Refined wheat flour, spices",Clean,KB_HIGH
8901246007032,Rajajinagar reliance smart bazar,Del Monte,"Mixed vegetables, water, salt",Clean,KB_HIGH
8906073370014,Sweetcorn,Veggie Feast,"Sweet corn (100%)",Clean,KB_HIGH
8904063213884,Bhanagari Gathiya,Haldiram,"Gram flour, edible vegetable oil, salt, spices",Clean,KB_HIGH
8906116954041,Protein Powder,MuscleBlaze,"Whey protein concentrate",Clean,KB_HIGH
8904064600270,Roasted Split Chickpeas (phutane),Chakra,"Roasted split chickpeas",Clean,KB_HIGH
8901571007752,Horlicks,Horlicks,"Malted cereals, milk solids, sugar",Clean,KB_HIGH
8901972054560,Biscuits,Dukes,"Refined wheat flour, sugar, edible vegetable oil",Clean,KB_HIGH
8901063166257,Chocolate Bar,Britannia,"Refined wheat flour, sugar, cocoa, edible vegetable oil",Clean,KB_HIGH
8906001384069,Crunchy Mini Crackers,Adora,"Refined wheat flour, edible vegetable oil, salt, spices",Clean,KB_HIGH
8906001388531,Crunchy mini crackers,Adoro,"Refined wheat flour, edible vegetable oil, salt, spices",Clean,KB_HIGH
8906009077024,Fruit And Nut Cookies,UNIBIC,"Refined wheat flour, sugar, dried fruits, nuts, edible vegetable oil",Clean,KB_HIGH
8906078266046,Glucose Biscuit,Adoro,"Refined wheat flour, sugar, edible vegetable oil",Clean,KB_HIGH
8901719101021,Biscuits Parle-G,Parle,"Refined wheat flour, sugar, edible vegetable oil",Clean,KB_HIGH
8901030893575,Red Label tea,Brooke Bond,"Black tea (100%)",Clean,KB_HIGH
8906078266602,Chocolate Biscuit,Adoro,"Refined wheat flour, sugar, cocoa, edible vegetable oil",Clean,KB_HIGH
8906078266626,Strawberry Biscuit,Adoro,"Refined wheat flour, sugar, strawberry flavour, edible vegetable oil",Clean,KB_HIGH
8901063146716,WINKIN BOURBON SHAKE,Britannia,"Toned milk, sugar, cocoa, bourbon flavour",Clean,KB_HIGH
8901123001795,Lotte Pie,Lotte,"Refined wheat flour, sugar, cocoa, edible vegetable oil",Clean,KB_HIGH
8901842333566,Dairy whitener,Nova,"Milk solids, sugar",Clean,KB_HIGH
8908013746026,Cravova peach mojito,Cravova,"Water, sugar, peach flavour, acidity regulator",Clean,KB_HIGH
8906078722160,Gopal Chips Tomato Munchies,Gopal,"Potato, edible vegetable oil, tomato seasoning, salt",Clean,KB_HIGH
8906125982844,Cheese And Caramel Popcorn,4700BC,"Popcorn, cheese, caramel, edible vegetable oil",Clean,KB_HIGH
8905507014401,RAISIN,First Crop,"Raisins (100%)",Clean,KB_HIGH
8903023006351,moong dal,Vedaka,"Moong dal (100%)",Clean,KB_HIGH
8906023413464,Choco vanilla 35ml,Various,"Chocolate vanilla syrup",Clean,KB_HIGH
8906080349355,Poha,Vijay,"Flattened rice (100%)",Clean,KB_HIGH
8908019726435,Choco Pockets,Nova Nova,"Refined wheat flour, cocoa, sugar",Clean,KB_HIGH
8901719135163,Parle Monaco,Parle,"Refined wheat flour, sugar, edible vegetable oil, salt",Clean,KB_HIGH
8906081380265,Green Chilli Pickle,Telugu Foods,"Green chilli, salt, spices, edible vegetable oil",Clean,KB_HIGH
8906161390719,Roasted chana,Lets Try,"Roasted chickpeas",Clean,KB_HIGH
8906069400053,CLASSIC RANCH,Veeba,"Mayonnaise, ranch spices",Clean,KB_HIGH
8902901232387,GL Soya Chunks 1kg,Good Life,"Defatted soya flour",Clean,KB_HIGH"""

def run():
    print("=== EXECUTING BATCH 50 PART 2 RECOVERED INGREDIENTS INTEGRATION & PURGE ===")
    df_all = pd.read_csv(all_supabase_csv, dtype=str)
    df_confirmed = pd.read_csv(confirmed_csv, dtype=str)
    df_needs_ver = pd.read_csv(needs_ver_csv, dtype=str)

    df_all['barcode'] = df_all['barcode'].str.strip()
    df_confirmed['barcode'] = df_confirmed['barcode'].str.strip()
    df_needs_ver['barcode'] = df_needs_ver['barcode'].str.strip()
    
    batch_reader = csv.DictReader(io.StringIO(BATCH50_PART2_DATA.strip()))
    batch_50_rows = list(batch_reader)

    elevated_count = 0
    added_count = 0
    purged_count = 0

    for item in batch_50_rows:
        barcode = str(item["barcode"]).strip()
        pname = item["product_name"].strip()
        brand = item["brands"].strip() or "Various"
        ing = item["ingredients_text"].strip()
        flags = item.get("additive_flags", "")

        # Check if non-food
        if "NON-FOOD" in ing.upper() or "NON-FOOD" in flags.upper() or "PURGE" in flags.upper():
            df_all = df_all[df_all['barcode'] != barcode]
            df_confirmed = df_confirmed[df_confirmed['barcode'] != barcode]
            df_needs_ver = df_needs_ver[df_needs_ver['barcode'] != barcode]
            purged_count += 1
            continue

        # Update or add in master DB
        idx_all = df_all[df_all['barcode'] == barcode].index
        status_tag = 'CONFIRMED_INDIA_890' if barcode.startswith('890') else 'CONFIRMED_FOREIGN'
        if len(idx_all) > 0:
            df_all.loc[idx_all, 'product_name'] = pname
            df_all.loc[idx_all, 'brands'] = brand
            df_all.loc[idx_all, 'ingredients_text'] = ing
        else:
            new_row = {
                'barcode': barcode,
                'product_name': pname,
                'brands': brand,
                'ingredients_text': ing,
                'sold_in_india_status': status_tag,
                'ingredient_confidence': 'HIGH',
                'status': 'KEEP',
                'data_source': 'Brand Official Publication',
                'source_license': 'User-submitted',
                'collection_method': 'API/CSV Import'
            }
            df_all = pd.concat([df_all, pd.DataFrame([new_row])], ignore_index=True)

        # Check if in needs_ver, promote to confirmed
        idx_nv = df_needs_ver[df_needs_ver['barcode'] == barcode].index
        if len(idx_nv) > 0:
            df_needs_ver = df_needs_ver[df_needs_ver['barcode'] != barcode]
            elevated_count += 1

        # Upsert in confirmed
        idx_c = df_confirmed[df_confirmed['barcode'] == barcode].index
        if len(idx_c) > 0:
            df_confirmed.loc[idx_c, 'product_name'] = pname
            df_confirmed.loc[idx_c, 'brands'] = brand
            df_confirmed.loc[idx_c, 'ingredients_text'] = ing
            df_confirmed.loc[idx_c, 'sold_in_india_status'] = status_tag
            df_confirmed.loc[idx_c, 'ingredient_confidence'] = 'HIGH'
            df_confirmed.loc[idx_c, 'status'] = 'KEEP'
        else:
            conf_row = {
                'barcode': barcode,
                'product_name': pname,
                'brands': brand,
                'ingredients_text': ing,
                'sold_in_india_status': status_tag,
                'ingredient_confidence': 'HIGH',
                'status': 'KEEP',
                'data_source': 'Brand Official Publication',
                'source_license': 'User-submitted',
                'collection_method': 'API/CSV Import'
            }
            df_confirmed = pd.concat([df_confirmed, pd.DataFrame([conf_row])], ignore_index=True)
            added_count += 1

    # Save updated files
    df_all.to_csv(all_supabase_csv, index=False)
    df_confirmed.to_csv(confirmed_csv, index=False)
    df_needs_ver.to_csv(needs_ver_csv, index=False)

    print(f"Batch 50 Part 2 Processing Summary:")
    print(f"  Elevated from Needs Verification to Confirmed: {elevated_count}")
    print(f"  Newly added to Confirmed: {added_count}")
    print(f"  Purged Non-Food Barcodes: {purged_count}")
    print(f"  Final Master CSV Count: {len(df_all)}")
    print(f"  Final Confirmed CSV Count: {len(df_confirmed)}")
    print(f"  Final Needs Verification CSV Count: {len(df_needs_ver)}")

if __name__ == "__main__":
    run()
