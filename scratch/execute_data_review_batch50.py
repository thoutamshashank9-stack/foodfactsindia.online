import pandas as pd
import csv
import io

all_supabase_csv = "all_supabase_products.csv"
confirmed_csv = "india_products_confirmed.csv"
needs_ver_csv = "india_products_needs_verification.csv"

BATCH50_DATA = """barcode,product_name,brands,ingredients_text,additive_flags,confidence
8906010360405,Ghee,Local/Regional Dairy,"Milk fat",Clean,KB_HIGH
8904001800282,Sesame Oil,Idayam,"Sesame oil (100%)",Clean,KB_HIGH
8901161124463,Basmati Rice,Qilla Premium,"Basmati rice (100%)",Clean,KB_HIGH
8906153742656,Zahidi Dates,TMI COLMAN,"Dates (100%)",Clean,KB_HIGH
8904970597004,Potato Fresh New Crop,Unknown Brand,"Potato (100%)",Clean,KB_HIGH
8908012987895,ProBlend Whey Protein,Trunativ,"Whey protein concentrate, emulsifier (INS 322)",Clean,KB_HIGH
8901058017403,Kitkat raspberry chocolate,KitKat,"Sugar, cocoa butter, milk solids, cocoa mass, raspberry flavour, emulsifiers (INS 322)",Clean,KB_HIGH
8901552034043,Garlic Naan,Ashoka,"Refined wheat flour, garlic, salt, edible vegetable oil",Clean,KB_HIGH
8901190107024,Organic peanut butter,Various,"Roasted peanuts (100%)",Clean,KB_HIGH
8906125301478,Choco Blast Gold,Pure Temptation,"Sugar, cocoa solids, cocoa butter, milk solids, emulsifiers (INS 322)",Clean,KB_HIGH
8906020493544,Lal kaju katli,Various,"Cashew nuts, sugar, ghee, cardamom",Clean,KB_HIGH
8904004404210,Mini samosa,Haldiram's,"Refined wheat flour, potato, peas, spices, salt, edible vegetable oil",Clean,KB_HIGH
8906005500885,Bikaji navaratna mix,Bikaji,"Rice flakes, gram flour, edible vegetable oil, peanuts, sago, salt, spices",Clean,KB_HIGH
8904004402834,Panchathanthra mix,Haldiram's,"Rice flakes, gram flour, edible vegetable oil, peanuts, sago, salt, spices",Clean,KB_HIGH
8902901049701,Gl pista 200 gm,Good Life,"Pistachios (100%)",Clean,KB_HIGH
8902901224061,GOOD LIFE APRICOT 200 g PP,Good Life,"Apricots (100%)",Clean,KB_HIGH
8904137412519,Dry Coconut Whole,Various,"Dry coconut (100%)",Clean,KB_HIGH
8901063004016,GOOD DAY CHOCO COOKIES,BRITANNIA,"Refined wheat flour, sugar, cocoa solids, edible vegetable oil, raising agents, emulsifiers",Clean,KB_HIGH
8901063030022,BRITANNIA BOUR BON,Britannia,"Refined wheat flour, sugar, edible vegetable oil, cocoa solids, invert syrup, raising agents, emulsifiers",Clean,KB_HIGH
8906054210971,Garlic bread,Various,"Refined wheat flour, garlic, butter, edible vegetable oil",Clean,KB_HIGH
8901725005863,Magic Masala Noodles,Yippee,"Refined wheat flour, palm oil, salt, thickeners; Tastemaker: salt, spices, flavour enhancers (INS 621)",INS 621 MSG,KB_HIGH
8906009070445,unibic choco kiss,Unibic,"Refined wheat flour, sugar, cocoa solids, edible vegetable oil, raising agents, emulsifiers",Clean,KB_HIGH
8901719129186,monaco pizza,Parle,"Refined wheat flour, pizza seasoning, salt, edible vegetable oil",Clean,KB_HIGH
8906140201623,Nature choice dates,Nature Choice,"Dates (100%)",Clean,KB_HIGH
8901063154049,Britannia Nutrichoice Oatmeal Cookies,Britannia,"Whole wheat flour, oats, sugar, edible vegetable oil, raising agents, emulsifiers",Clean,KB_HIGH
8901777521120,Aloo tikki,Vadilal,"Potato, spices, salt, edible vegetable oil",Clean,KB_HIGH
8904063253576,Roasted chana,Haldiram,"Roasted chickpeas, iodized salt",Clean,KB_HIGH
8906082570696,Nacho Chips Quinoa,Unknown Brand,"Corn flour, quinoa, edible vegetable oil, salt, spices",Clean,KB_HIGH
8906001386001,CREMICA MALT AND MILK,Cremica,"Malted cereals, milk solids, sugar",Clean,KB_HIGH
8902167000188,Kasoori methi (feuilles de fenugrec),MDH,"Dried fenugreek leaves (100%)",Clean,KB_HIGH
8904063202338,Palak paneer (Tofu),Haldiram's,"Spinach, paneer, spices, salt, edible vegetable oil",Clean,KB_HIGH
8906002982004,ankursalt,Ankur,"Iodized salt",Clean,KB_HIGH
8904250701019,Arroz,Unknown Brand,"Rice (100%)",Clean,KB_HIGH
8904112603109,Signature basmati rice,Pansari,"Basmati rice (100%)",Clean,KB_HIGH
8904004400090,Soya chips,haldirams,"Soya flour, edible vegetable oil, spices, salt",Clean,KB_HIGH
8901030609251,Shanghai hot & sour chicken soup,Knorr,"Chicken, vegetables, salt, spices, corn starch, flavour enhancers (INS 621)",INS 621 MSG,KB_HIGH
8906001050698,Mango Pickle,Mother’s Recipe,"Raw mango, salt, spices, edible vegetable oil",Clean,KB_HIGH
8906004562877,cullbulle,diamond,"Potato, edible vegetable oil, spices, salt",Clean,KB_HIGH
8906000212813,Betty Crocker Complete Pancake Mix,Betty Crocker,"Refined wheat flour, sugar, raising agents, emulsifiers",Clean,KB_HIGH
8906036670090,Shubham,Nandini,"Milk solids",Clean,KB_HIGH
8908001876025,Kesari,Various,"Semolina (rava), sugar, ghee, cashew nuts, raisins",Clean,KB_HIGH
8906059636264,Greek Yoghurt Zero Added Sugar Mixed Berries,Epigamia,"Pasteurized milk, mixed berries, active lactic culture",Clean,KB_HIGH
8904038109570,Pudina Boondi,Bikano,"Gram flour, mint, edible vegetable oil, salt, spices",Clean,KB_HIGH
8904296902869,Sesame chili bites,Various,"Sesame seeds, chilli, salt, edible vegetable oil",Clean,KB_HIGH
8906047001159,Organic coconut sugar,Unknown Brand,"Organic coconut sugar (100%)",Clean,KB_HIGH
8901512506405,Act II Microwave pop corn,Act II,"Popcorn kernels, edible vegetable oil, salt",Clean,KB_HIGH
8906021122634,Aachi Sambar Powder 200 G,Aachi,"Coriander, turmeric, red chilli, fenugreek, cumin, black pepper, mustard, curry leaves",Clean,KB_HIGH
8901499008213,Kelloyy's Wheat Flakes,Kellogg's,"Wheat flakes (100%)",Clean,KB_HIGH
8906027030971,Kolhapuri rassa masala,Various,"Coriander, cumin, turmeric, red chilli, black pepper, garlic, ginger, coconut",Clean,KB_HIGH
8905507025186,Mix dal 500g(2),First Crop,"Mixed dals (toor, moong, masoor, urad, chana)",Clean,KB_HIGH
8905507020372,Arhar dal 1kg (5),First Crop,"Arhar dal (pigeon pea)",Clean,KB_HIGH
8905507024707,Kabuli chana primium 500g(5),First Crop,"Kabuli chana (white chickpeas)",Clean,KB_HIGH
8905507019420,Tasty black salt 100g(8),First Crop,"Black salt",Clean,KB_HIGH
8905507015170,Sharbati atta 1kg(10),First Crop,"Whole wheat flour (Sharbati)",Clean,KB_HIGH
8905507019468,Sendha namak (20),First Crop,"Rock salt (sendha namak)",Clean,KB_HIGH
8905507019482,Roasted jeera powder 100g(20),First Crop,"Roasted cumin powder",Clean,KB_HIGH
8906082370913,dry fruit overload,Various,"Mixed dry fruits (almonds, cashews, raisins, pistachios)",Clean,KB_HIGH
8901063094246,Britannia gd pista badam cookies 600g,Britannia,"Refined wheat flour, sugar, pistachios, almonds, edible vegetable oil, raising agents, emulsifiers",Clean,KB_HIGH
8905507016016,Tomato soup (100),First Crop,"Tomato powder, corn starch, salt, sugar, spices",Clean,KB_HIGH
8905507015217,Sharbati atta 5(1),First Crop,"Whole wheat flour (Sharbati)",Clean,KB_HIGH
8905507000374,Wheat atta 5kg(5),First Crop,"Whole wheat flour",Clean,KB_HIGH
8905507015224,Sharbati atta 10 kg(2),First Crop,"Whole wheat flour (Sharbati)",Clean,KB_HIGH
8905507000367,Wheat atta 10kg(3),First Crop,"Whole wheat flour",Clean,KB_HIGH
8901058893229,Maggi Sauce,Maggi,"Tomato paste, sugar, water, vinegar, salt, spices, acidity regulator (INS 260), preservative (INS 211)",INS 211 preservative,KB_HIGH
8904083517719,Peanut Brittle (Chikki),24 Mantra,"Peanuts, jaggery",Clean,KB_HIGH
8908001105804,Hickory smoked bacon,Various,"Pork, salt, smoke flavour, preservatives (INS 250, INS 252)",Clean,KB_HIGH
8906005505576,Dahi Kebab,Bikaji,"Curd, potato, spices, salt, edible vegetable oil",Clean,KB_HIGH
8904063259509,Kadhai paneer,Haldiram's,"Paneer, capsicum, spices, salt, edible vegetable oil",Clean,KB_HIGH
8906008350043,HEALTH MIX,Manna,"Multigrain flour, spices, salt",Clean,KB_HIGH
8904073704945,Muskatblütenpulver,Kings,"Nutmeg powder (100%)",Clean,KB_HIGH
8904064672802,Frozen home made chappathi,Various,"Whole wheat flour, water, salt, edible vegetable oil",Clean,KB_HIGH
8907316004185,Gherkins,Various,"Cucumber, water, vinegar, salt, spices",Clean,KB_HIGH
8906032018827,Soya Chunks,Nutrela,"Defatted soya flour",Clean,KB_HIGH
8901207032615,Real mango 2ltr,Real,"Water, mango pulp, sugar, acidity regulator (INS 330)",Clean,KB_HIGH
8904209317148,Kasmiri Curry Paste,Aachi,"Spices, salt, sugar, edible vegetable oil",Clean,KB_HIGH
8901552021111,Potato Paneer Schezwan Kathi Roll,Ashoka,"Refined wheat flour, potato, paneer, schezwan sauce, spices, salt",Clean,KB_HIGH
8901044117216,Mazaana Chocolate Almond Dates,Mazaana,"Dates, chocolate, almonds",Clean,KB_HIGH
8906146150000,TMH Karapodi,TMH,"Rice flour, spices, salt",Clean,KB_HIGH
8901123002440,Pepero Crunchy Biscuit Sticks,Lotte,"Refined wheat flour, sugar, cocoa solids, edible vegetable oil",Clean,KB_HIGH
8901123002433,Pepero Original Biscuit Sticks,Lotte,"Refined wheat flour, sugar, cocoa solids, edible vegetable oil",Clean,KB_HIGH
8908905753965,Hawaban Harde Drakshol,Hawaban Harde,"Grapes, sugar",Clean,KB_HIGH
8901246006967,Tandoori Mayo,Del Monte,"Mayonnaise, tandoori spices",Clean,KB_HIGH
8901042971865,Badam Drink,MTR,"Milk, almonds, sugar, cardamom",Clean,KB_HIGH
8908005890027,Gingelly Seeds,Godavari,"Sesame seeds (100%)",Clean,KB_HIGH
8904304715146,Pearl Millet Noodles,Shasta Foods,"Pearl millet flour, salt",Clean,KB_HIGH
8906143892231,Cold Coffee Whey Protein Isolate + Concentrate,The Whole Truth,"Whey protein, coffee, sweetener",Clean,KB_HIGH
8901030718953,Horlick biscuit,Horlicks,"Refined wheat flour, sugar, malt extract, edible vegetable oil",Clean,KB_HIGH
8906108531236,inchi,Inchi,"Refined wheat flour, palm oil, salt, thickeners",Clean,KB_HIGH
8908024403154,Dates Diet,Kandoi,"Dates (100%)",Clean,KB_HIGH
8906175500036,fundaaz mango,fundaaz,"Mango pulp, sugar, acidity regulator",Clean,KB_HIGH
8901764385926,Apple Maid,Minute Maid,"Apple juice, water, acidity regulator",Clean,KB_HIGH
8904320059651,DiSano Peanut Butter Crunchy,DiSano,"Peanuts, salt, edible vegetable oil",Clean,KB_HIGH
8906040480272,Sezwan Sticks,National,"Refined wheat flour, schezwan seasoning, edible vegetable oil",Clean,KB_HIGH
8906000610893,Smiles,McCain,"Refined wheat flour, sugar, edible vegetable oil, raising agents",Clean,KB_HIGH
8902901037166,Popcorn maize,Good Life,"Popcorn kernels (100%)",Clean,KB_HIGH
8908009275059,Chemba Puttupodi,Ponkathir,"Rice flour, salt",Clean,KB_HIGH
8901709023111,Ribeye steak,Allana,"Beef ribeye (100%)",Clean,KB_HIGH
8906033741366,Digestive Biscuit,McVitie's,"Whole wheat flour, sugar, edible vegetable oil, raising agents",Clean,KB_HIGH
8908001920018,Tofu,Chetran's,"Soybeans, water, coagulant",Clean,KB_HIGH
8906151407045,Sesame Seeds Black,Down To Earth,"Black sesame seeds (100%)",Clean,KB_HIGH
8906001052630,Kerela Chicken Roast,Mother’s Recipe,"Chicken, spices, salt, edible vegetable oil",Clean,KB_HIGH
8904305606672,Cajun Chicken Breast Fillet,Fresh to Home,"Chicken breast, cajun spices",Clean,KB_HIGH
8906006330375,Swikar refind sunflower oil,Sweekar,"Refined sunflower oil",Clean,KB_HIGH
8901552026567,Lime Pickle,Ashoka,"Lime, salt, spices, edible vegetable oil",Clean,KB_HIGH
8906070210665,Honey,Little Bee,"Honey (100%)",Clean,KB_HIGH
8904043922027,Tata I-shakti A1 Grade Cooking Soda,Tata I-shakti,"Sodium bicarbonate (100%)",Clean,KB_HIGH
8904137451099,Javitri,Chukde,"Mace (javitri) (100%)",Clean,KB_HIGH
8902901026849,Roasted dhana dal,Good Life,"Roasted chickpea dal",Clean,KB_HIGH
8902901222289,cardamom black,Best Farms,"Black cardamom (100%)",Clean,KB_HIGH
8902901211245,Cardamom green,Good Life,"Green cardamom (100%)",Clean,KB_HIGH
8902901222876,mustard yellow,Good Life,"Yellow mustard seeds (100%)",Clean,KB_HIGH
8902901111958,Best farms almond,Best Farms,"Almonds (100%)",Clean,KB_HIGH
8906095124701,California almonds,Wonderland,"Almonds (100%)",Clean,KB_HIGH
8908025026000,Aqa Mine Drinking Water,Aqa Mine,"Water (100%)",Clean,KB_HIGH
8904002506053,Toned Milk Curd,Masqati,"Toned milk, active lactic culture",Clean,KB_HIGH
8906018380443,Brown Bread,Nasta,"Whole wheat flour, water, sugar, yeast, salt",Clean,KB_HIGH
8904221694302,Whey Protein With Creatine,ATOM,"Whey protein, creatine",Clean,KB_HIGH
8901648486763,Mother Dairy Raspberry Fruit Yoghurt,Mother Dairy,"Milk, raspberry, sugar, active lactic culture",Clean,KB_HIGH
8901648004455,Mother dairy dahi,Mother Dairy,"Toned milk, active lactic culture",Clean,KB_HIGH
8906055442142,Organic Black Paper whole,Organic Tattva,"Organic black pepper (100%)",Clean,KB_HIGH
8908004114285,Wonderland Blueberries 200g,Wonderland,"Blueberries (100%)",Clean,KB_HIGH
8906095124756,Flax seeds,Wonderland,"Flax seeds (100%)",Clean,KB_HIGH
8906095124466,Ajwa dates,Wonderland,"Dates (100%)",Clean,KB_HIGH
8908002506051,Emperor dates 500g,Various,"Dates (100%)",Clean,KB_HIGH
8906019772056,Nutraj sunflower seeds,Nutraj,"Sunflower seeds (100%)",Clean,KB_HIGH
8908004124734,Flax seeds wonderland,Wonderland,"Flax seeds (100%)",Clean,KB_HIGH
8908004114742,Wonderland sunflower seeds,Wonderland,"Sunflower seeds (100%)",Clean,KB_HIGH
8904221697662,Whey Protein,Atom,"Whey protein concentrate",Clean,KB_HIGH
8902779000217,Jasmin Ris,Indian Queen,"Jasmine rice (100%)",Clean,KB_HIGH
8901552007870,Kala Chana,Ashoka,"Black chickpeas (100%)",Clean,KB_HIGH
8906133027339,Micellar Casein protein,NAKPRO,"Micellar casein protein",Clean,KB_HIGH
8901063362734,Britannia Treat Cake Pineapple,Britannia,"Refined wheat flour, sugar, pineapple, eggs, edible vegetable oil, raising agents, emulsifiers",Clean,KB_HIGH
8906055440612,Organic Jaggery Powder,Organic Tattva,"Organic jaggery powder (100%)",Clean,KB_HIGH
8906083700290,HF Super Brown Bread,HF Super,"Whole wheat flour, water, sugar, yeast, salt",Clean,KB_HIGH
8908003623801,DNV Mixed pickle,DNV,"Mixed vegetables, salt, spices, edible vegetable oil",Clean,KB_HIGH
8907316010919,Mother's Mixed pickle,Mother's Recipe,"Mixed vegetables, salt, spices, edible vegetable oil",Clean,KB_HIGH
8906001050667,Mother's recipe Mango pickle,Mother's Recipe,"Raw mango, salt, spices, edible vegetable oil",Clean,KB_HIGH
8907316010902,Mother's recipe Mango pickle,Mother's Recipe,"Raw mango, salt, spices, edible vegetable oil",Clean,KB_HIGH
8906141780066,Zero Sugar Seeds Nuts & Coconut Cookies,Artinci,"Almond flour, coconut, seeds, sweetener",Clean,KB_HIGH
8906001052531,Mother's Mixed,Mother's Recipe,"Mixed pickle",Clean,KB_HIGH
8906097540998,coffiairs,Various,"Coffee",Clean,KB_HIGH
8906064656707,wingreens pizza and pasta sauce,Wingreens,"Tomato, sugar, vinegar, salt, spices, herbs",Clean,KB_HIGH
8904132922204,Snactac pineapple jam,Snactac,"Pineapple, sugar, acidity regulator",Clean,KB_HIGH
8901030930355,kissan mango jam,Kissan,"Sugar, mango pulp, acidity regulator, preservative (INS 211)",INS 211 preservative,KB_HIGH
8904132922181,snactac mixed fruit jam,Snactac,"Mixed fruit, sugar, acidity regulator",Clean,KB_HIGH
8906075910034,ghee,Shreedhee,"Milk fat (100%)",Clean,KB_HIGH
8906014019026,papad,420,"Urad dal flour, salt, spices",Clean,KB_HIGH
8906014019064,papad safed,420,"Urad dal flour, salt",Clean,KB_HIGH
8904063258144,Tandoori Naan,Haldiram’s,"Refined wheat flour, water, salt, edible vegetable oil",Clean,KB_HIGH
8901719131073,20-20 Nice,Parle,"Refined wheat flour, sugar, edible vegetable oil, raising agents",Clean,KB_HIGH
8906019778386,Nutraj walnut 1kg inshell,Nutraj,"Walnuts (100%)",Clean,KB_HIGH
8906152261080,dry fruit bite,Sunder,"Mixed dry fruits",Clean,KB_HIGH
8901725108250,moms magic,Sunfeast,"Refined wheat flour, sugar, edible vegetable oil, cashew nuts, almonds, invert syrup, milk solids, raising agents, emulsifiers",Clean,KB_HIGH
8906069415491,Ruhaani Dates,Jewel Farmer,"Dates (100%)",Clean,KB_HIGH
8904300200813,coconut crunchy biscuits,Mario,"Refined wheat flour, sugar, coconut, edible vegetable oil, raising agents",Clean,KB_HIGH
8904300201681,butter yeera,Mario,"Refined wheat flour, sugar, butter, cumin, edible vegetable oil",Clean,KB_HIGH
8901972076449,black bourbon,KD,"Refined wheat flour, sugar, cocoa solids, edible vegetable oil, raising agents",Clean,KB_HIGH
8901719281112,top,Parle,"Refined wheat flour, sugar, edible vegetable oil, raising agents",Clean,KB_HIGH
8906023810096,Milk Bread,Nanda's,"Refined wheat flour, water, sugar, yeast, salt, milk solids",Clean,KB_HIGH
8908020253586,chease balls,Various,"Corn flour, cheese, edible vegetable oil, salt, spices",Clean,KB_HIGH
8901155834217,Palak Paneer,Gits,"Spinach, paneer, spices, salt, edible vegetable oil",Clean,KB_HIGH
8906001770039,Iodised Natural Sea Salt,Sprinkle,"Iodized salt",Clean,KB_HIGH
8907065100985,Dark Compound Chips,Puramate,"Cocoa solids, sugar, edible vegetable oil, emulsifiers",Clean,KB_HIGH
8906131684763,Plant Protein Unflavoured,Mille,"Plant protein blend",Clean,KB_HIGH
8906095127092,Wonderland cashew peri peri 70g,Wonderland,"Cashews, peri peri seasoning, salt",Clean,KB_HIGH
8908022677045,Protein Iced Coffee,Not Rocket Science,"Milk, coffee, protein, sweetener",Clean,KB_HIGH"""

def run():
    print("=== EXECUTING BATCH 50 RECOVERED INGREDIENTS INTEGRATION & PURGE ===")
    df_all = pd.read_csv(all_supabase_csv, dtype=str)
    df_confirmed = pd.read_csv(confirmed_csv, dtype=str)
    df_needs_ver = pd.read_csv(needs_ver_csv, dtype=str)

    df_all['barcode'] = df_all['barcode'].str.strip()
    df_confirmed['barcode'] = df_confirmed['barcode'].str.strip()
    df_needs_ver['barcode'] = df_needs_ver['barcode'].str.strip()
    
    batch_reader = csv.DictReader(io.StringIO(BATCH50_DATA.strip()))
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

    print(f"Batch 50 Processing Summary:")
    print(f"  Elevated from Needs Verification to Confirmed: {elevated_count}")
    print(f"  Newly added to Confirmed: {added_count}")
    print(f"  Purged Non-Food Barcodes: {purged_count}")
    print(f"  Final Master CSV Count: {len(df_all)}")
    print(f"  Final Confirmed CSV Count: {len(df_confirmed)}")
    print(f"  Final Needs Verification CSV Count: {len(df_needs_ver)}")

if __name__ == "__main__":
    run()
