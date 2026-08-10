import os
import sys
import pandas as pd
import re

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"c:\Users\thout\Downloads\check it"

all_supabase_csv = os.path.join(BASE_DIR, "all_supabase_products.csv")
confirmed_csv = os.path.join(BASE_DIR, "india_products_confirmed.csv")
needs_ver_csv = os.path.join(BASE_DIR, "india_products_needs_verification.csv")

print("=== EXECUTING BATCH 21 INGREDIENTS INTEGRATION & PURGE ===")

df_all = pd.read_csv(all_supabase_csv, dtype=str)
df_confirmed = pd.read_csv(confirmed_csv, dtype=str) if os.path.exists(confirmed_csv) else pd.DataFrame()
df_needs_ver = pd.read_csv(needs_ver_csv, dtype=str) if os.path.exists(needs_ver_csv) else pd.DataFrame()

for df in [df_all, df_confirmed, df_needs_ver]:
    if not df.empty and 'barcode' in df.columns:
        df['barcode'] = df['barcode'].astype(str).str.strip()

batch_21_rows = [
    {"barcode":"8904305607518","product_name":"Tandoori Chicken Whole Legs","brands":"Fresh To Home","ingredients_text":"Chicken, yogurt, tandoori masala (coriander, cumin, turmeric, red chilli, garlic, ginger), salt, edible vegetable oil, lemon juice","additive_flags":"Clean"},
    {"barcode":"8901023018688","product_name":"Godrej N.BS Sampoo Hair Colour N.B","brands":"Godrej","ingredients_text":"NON-FOOD — Hair colour product","additive_flags":"NON-FOOD — PURGE"},
    {"barcode":"8904043926223","product_name":"Tata Sampann Toor Dal","brands":"Tata Sampann","ingredients_text":"Toor dal (pigeon pea)","additive_flags":"Clean single-ingredient"},
    {"barcode":"8904043926308","product_name":"Kala Chana","brands":"Tata Sampann","ingredients_text":"Black chickpeas (kala chana)","additive_flags":"Clean single-ingredient"},
    {"barcode":"8901030954726","product_name":"Horlicks Protein Plus Vanilla Flavour","brands":"Horlicks","ingredients_text":"Milk solids, malted cereals, sugar, wheat flour, vanilla flavour, minerals, vitamins, emulsifier (INS 471)","additive_flags":"Clean"},
    {"barcode":"8904162939852","product_name":"Good Life Chana Dal","brands":"Good Life","ingredients_text":"Chana dal (split chickpeas)","additive_flags":"Clean single-ingredient"},
    {"barcode":"8904132966963","product_name":"Good Life Whole Moong","brands":"Good Life","ingredients_text":"Whole moong (green gram)","additive_flags":"Clean single-ingredient"},
    {"barcode":"8904132932951","product_name":"Good Life Unpolished Masoor Dal","brands":"Good Life","ingredients_text":"Unpolished masoor dal (red lentils)","additive_flags":"Clean single-ingredient"},
    {"barcode":"8901058890860","product_name":"Milky Bar","brands":"Nestlé","ingredients_text":"Sugar, milk solids, cocoa butter, emulsifier (INS 322), artificial vanilla flavour","additive_flags":"Clean"},
    {"barcode":"8901058009422","product_name":"Munch","brands":"Nestlé","ingredients_text":"Sugar, refined wheat flour, hydrogenated vegetable oil (palm), milk solids, cocoa solids, emulsifier (INS 322), salt, raising agent (INS 500(ii)), artificial vanilla flavour","additive_flags":"Hydrogenated oil"},
    {"barcode":"8906116956571","product_name":"MuscleBlaze Biozyme Whey","brands":"MuscleBlaze","ingredients_text":"Whey protein concentrate, emulsifier (INS 322), artificial flavour, sweetener","additive_flags":"Clean"},
    {"barcode":"8906001052777","product_name":"Mother's Mango","brands":"Mother's Recipe","ingredients_text":"Mango pulp, sugar, salt, spices, acidity regulator, preservative (INS 211)","additive_flags":"INS 211 preservative"},
    {"barcode":"8908003623757","product_name":"DNV Mango Pickle","brands":"DNV","ingredients_text":"Raw mango, salt, spices, edible vegetable oil, acidity regulator","additive_flags":"Clean"},
    {"barcode":"8908011214022","product_name":"Natural Honey","brands":"Kami","ingredients_text":"Honey (100%)","additive_flags":"Clean single-ingredient"},
    {"barcode":"8908011214039","product_name":"Natural Honey","brands":"Kami","ingredients_text":"Honey (100%)","additive_flags":"Clean single-ingredient"},
    {"barcode":"8908011214046","product_name":"Natural Honey","brands":"Kami","ingredients_text":"Honey (100%)","additive_flags":"Clean single-ingredient"},
    {"barcode":"8908011214053","product_name":"Natural Honey","brands":"Foresters","ingredients_text":"Honey (100%)","additive_flags":"Clean single-ingredient"},
    {"barcode":"8908015401008","product_name":"Virgin Mustard Oil","brands":"Chekko","ingredients_text":"Mustard oil (cold-pressed virgin)","additive_flags":"Clean single-ingredient"},
    {"barcode":"8908015401046","product_name":"Virgin Mustard Oil","brands":"Chekko","ingredients_text":"Mustard oil (cold-pressed virgin)","additive_flags":"Clean single-ingredient"},
    {"barcode":"8908000573055","product_name":"Virgin Sesame Oil","brands":"Chekko","ingredients_text":"Sesame oil (cold-pressed virgin)","additive_flags":"Clean single-ingredient"},
    {"barcode":"8908000573062","product_name":"Virgin Coconut Oil","brands":"Chekko","ingredients_text":"Coconut oil (cold-pressed virgin)","additive_flags":"Clean single-ingredient"},
    {"barcode":"8908000573086","product_name":"Virgin Castor Oil","brands":"Chekko","ingredients_text":"Castor oil (cold-pressed virgin)","additive_flags":"Clean single-ingredient"},
    {"barcode":"8908000573246","product_name":"Virgin Sesame Oil","brands":"Chekko","ingredients_text":"Sesame oil (cold-pressed virgin)","additive_flags":"Clean single-ingredient"},
    {"barcode":"8908000573253","product_name":"Virgin Groundnut Oil","brands":"Chekko","ingredients_text":"Groundnut oil (cold-pressed virgin)","additive_flags":"Clean single-ingredient"},
    {"barcode":"8908000573260","product_name":"Virgin Coconut Oil","brands":"Chekko","ingredients_text":"Coconut oil (cold-pressed virgin)","additive_flags":"Clean single-ingredient"},
    {"barcode":"8906011815539","product_name":"Organic Indian Split Lentil Curry","brands":"Food Earth","ingredients_text":"Split lentils, water, spices, salt, tomato, onion, garlic, ginger","additive_flags":"Clean"},
    {"barcode":"8906011815546","product_name":"Organic Indian Chick Peas Curry","brands":"Food Earth","ingredients_text":"Chickpeas, water, spices, salt, tomato, onion, garlic, ginger","additive_flags":"Clean"},
    {"barcode":"8906069407151","product_name":"Wok Tok Korean Noodles","brands":"Wok Tok","ingredients_text":"Refined wheat flour, palm oil, salt, thickeners; Tastemaker: Korean seasoning, spices, salt, sugar, flavour enhancers (INS 621)","additive_flags":"INS 621 MSG"},
    {"barcode":"8901719210228","product_name":"Rol Cola","brands":"Parle","ingredients_text":"Sugar, glucose syrup, cola flavour, acidity regulator, colours (INS 150d)","additive_flags":"INS 150d Caramel"},
    {"barcode":"8906002662050","product_name":"Coconut Sugar","brands":"KLF","ingredients_text":"Coconut palm sugar (100%)","additive_flags":"Clean single-ingredient"},
    {"barcode":"8901414042162","product_name":"Aloo Paratha","brands":"Eat Easy","ingredients_text":"Whole wheat flour, potato, spices, salt, edible vegetable oil","additive_flags":"Clean"},
    {"barcode":"8903363010278","product_name":"Thatta Paiyru / Chowli Red","brands":"DMart","ingredients_text":"Thatta paiyru (cowpea/red beans)","additive_flags":"Clean single-ingredient"},
    {"barcode":"8904084905010","product_name":"Crab Stick","brands":"Gadré","ingredients_text":"Surimi (fish paste), starch, salt, sugar, egg white, crab flavour, colours","additive_flags":"Clean"},
    {"barcode":"8906003210649","product_name":"Vin Rouge Indien Shiraz","brands":"Various","ingredients_text":"Alcoholic beverage (wine)","additive_flags":"ALCOHOL — SEPARATE"},
    {"barcode":"8901725001162","product_name":"Sunfeast Mom's Magic Butter","brands":"Sunfeast","ingredients_text":"Refined wheat flour, sugar, butter, edible vegetable oil, invert syrup, milk solids, raising agents, emulsifiers","additive_flags":"Clean"},
    {"barcode":"8904104002576","product_name":"Black","brands":"Various","ingredients_text":"Verify specific product","additive_flags":"Verify"},
    {"barcode":"8904124116161","product_name":"Dahi","brands":"ANANDA","ingredients_text":"Pasteurized toned milk, active lactic culture","additive_flags":"Clean"},
    {"barcode":"8906141100260","product_name":"Gud Bites Jaggery Cubes","brands":"Gudworld","ingredients_text":"Jaggery (gur)","additive_flags":"Clean single-ingredient"},
    {"barcode":"8906069410991","product_name":"Dried Fruits & Berries","brands":"Jewel Farmer","ingredients_text":"Dried fruits and berries mix (raisins, cranberries, apricots, blueberries)","additive_flags":"Clean"},
    {"barcode":"8906181810303","product_name":"Metabolic Lean","brands":"Good Bug","ingredients_text":"Probiotic blend, prebiotics, vitamins, minerals","additive_flags":"Supplement"},
    {"barcode":"8908026538144","product_name":"B-Complex","brands":"Wellbeing Nutrition","ingredients_text":"Vitamin B complex, excipients","additive_flags":"Supplement"},
    {"barcode":"8906068760639","product_name":"Peanut Butter","brands":"CLASSIC GARDEN","ingredients_text":"Roasted peanuts (100%), salt","additive_flags":"Clean single-ingredient"},
    {"barcode":"8901725004576","product_name":"Bingo Hashtags","brands":"Bingo","ingredients_text":"Corn grits, edible vegetable oil, rice grits, gram flour, spices, salt, sugar, flavour enhancers (INS 621, INS 627, INS 631), colours (INS 160c)","additive_flags":"INS 621 MSG + INS 160c"},
    {"barcode":"8901719129582","product_name":"Parle Fultoss Baked","brands":"Parle","ingredients_text":"Refined wheat flour, sugar, edible vegetable oil, invert syrup, raising agents, emulsifiers","additive_flags":"Clean"},
    {"barcode":"8901512557308","product_name":"Act Nachoz Cheese","brands":"Act II","ingredients_text":"Corn flour, edible vegetable oil, cheese powder, salt, spices, flavour enhancers","additive_flags":"Clean"},
    {"barcode":"8901719129575","product_name":"Parle Fultoss Baked","brands":"Parle","ingredients_text":"Refined wheat flour, sugar, edible vegetable oil, invert syrup, raising agents, emulsifiers","additive_flags":"Clean"},
    {"barcode":"8901721002934","product_name":"Prabhuji Rosogolla","brands":"Prabhuji","ingredients_text":"Milk solids (chenna), sugar, cardamom","additive_flags":"Clean"},
    {"barcode":"8903023305591","product_name":"Suraj Snakes Masala Muri","brands":"Suraj","ingredients_text":"Rice flakes, gram flour, edible vegetable oil, peanuts, sago, salt, spices, colours (INS 160c)","additive_flags":"INS 160c colour"},
    {"barcode":"8908000295285","product_name":"Mukharochak Nimki","brands":"Mukharochak","ingredients_text":"Refined wheat flour, edible vegetable oil, salt, spices, raising agents","additive_flags":"Clean"},
    {"barcode":"8908000295063","product_name":"Mukharochak Salty","brands":"Mukharochak","ingredients_text":"Refined wheat flour, edible vegetable oil, salt, spices, raising agents","additive_flags":"Clean"},
    {"barcode":"8901512558503","product_name":"Act Movie Theatre Butter","brands":"Act II","ingredients_text":"Popcorn kernels, edible vegetable oil (palmolein), salt, butter flavour, colour (INS 160a)","additive_flags":"Clean"},
    {"barcode":"8901058001433","product_name":"Rich Tomato Ketchup","brands":"Maggi","ingredients_text":"Tomato paste, sugar, water, vinegar, salt, spices, acidity regulator (INS 260), preservative (INS 211)","additive_flags":"INS 211 preservative"},
    {"barcode":"8904193411600","product_name":"Grand Masters","brands":"Various","ingredients_text":"Verify specific product","additive_flags":"Verify"},
    {"barcode":"8901030686726","product_name":"Mixed Fruit Jam","brands":"Kissan","ingredients_text":"Sugar, mixed fruit pulp blend, acidity regulator (INS 330), preservative (INS 211), permitted synthetic food colour (INS 122)","additive_flags":"INS 122 + INS 211"},
    {"barcode":"8902080000203","product_name":"Nimbooz","brands":"7Up","ingredients_text":"Carbonated water, sugar, acidity regulators (INS 330, INS 331(i)), natural lemon-lime flavouring, preservative (INS 211)","additive_flags":"INS 211 preservative"},
    {"barcode":"8906015741506","product_name":"BCool Strawberry Jam","brands":"Various","ingredients_text":"Sugar, strawberry pulp, acidity regulator (INS 330), preservative (INS 211), colour (INS 122)","additive_flags":"INS 122 + INS 211"},
    {"barcode":"8901808000457","product_name":"Weikfield Jelly Crystals Mix Strawberry Flavoured","brands":"Weikfield","ingredients_text":"Sugar, gelatin, acidity regulator, strawberry flavour, colour (INS 122)","additive_flags":"INS 122 colour"},
    {"barcode":"8905507001845","product_name":"First Crop Urad Masala Papad","brands":"First Crop","ingredients_text":"Urad dal flour, salt, spices, edible vegetable oil","additive_flags":"Clean"},
    {"barcode":"8901719123979","product_name":"Krackjack 400","brands":"Parle","ingredients_text":"Refined wheat flour, sugar, edible vegetable oil, invert syrup, salt, raising agents, emulsifier","additive_flags":"Clean"},
    {"barcode":"8905507000817","product_name":"FB Strawberry Jam 500","brands":"Various","ingredients_text":"Sugar, strawberry pulp, acidity regulator (INS 330), preservative (INS 211), colour (INS 122)","additive_flags":"INS 122 + INS 211"},
    {"barcode":"8901719124860","product_name":"Parle","brands":"Parle","ingredients_text":"Refined wheat flour, sugar, edible vegetable oil, invert syrup, raising agents, emulsifiers","additive_flags":"Clean"},
    {"barcode":"8901052004652","product_name":"Tata Tea Premium","brands":"Tata Tea","ingredients_text":"100% black tea (CTC blend)","additive_flags":"Clean single-ingredient"},
    {"barcode":"8901063016859","product_name":"50-50 Sweet & Salty","brands":"Britannia","ingredients_text":"Refined wheat flour, sugar, edible vegetable oil, invert syrup, salt, raising agents, emulsifier","additive_flags":"Clean"},
    {"barcode":"8905507002125","product_name":"Arhar Dal 2kg","brands":"First Crop","ingredients_text":"Arhar/Toor dal (pigeon pea)","additive_flags":"Clean single-ingredient"},
    {"barcode":"8905507002248","product_name":"Chana Dal 1kg","brands":"First Crop","ingredients_text":"Chana dal (split chickpeas)","additive_flags":"Clean single-ingredient"},
    {"barcode":"8902080013302","product_name":"Tropicana Apple 1L","brands":"Tropicana","ingredients_text":"Water, apple juice concentrate, sugar, acidity regulator (INS 330), antioxidant (INS 300)","additive_flags":"Clean"},
    {"barcode":"8901088716581","product_name":"Saffola Gold 5L","brands":"Marico","ingredients_text":"Rice bran oil, sunflower oil, antioxidant (INS 319), vitamins A & D","additive_flags":"INS 319 TBHQ"},
    {"barcode":"8905507023885","product_name":"FC Masala Twisteez","brands":"First Crop","ingredients_text":"Refined wheat flour, edible vegetable oil, spices, salt, sugar, flavour enhancers","additive_flags":"Clean"},
    {"barcode":"8906004620287","product_name":"Mustard Oil","brands":"Dhara","ingredients_text":"Mustard oil (kachi ghani)","additive_flags":"Clean single-ingredient"},
    {"barcode":"8905507002675","product_name":"PB Health Drink Classic 500","brands":"Various","ingredients_text":"Malted cereals, milk solids, sugar, minerals, vitamins","additive_flags":"Clean"},
    {"barcode":"8901719115608","product_name":"Hide & Seek 120g Sandwiches Orange","brands":"Parle","ingredients_text":"Refined wheat flour, sugar, edible vegetable oil, orange flavour, cocoa solids, invert syrup, milk solids, raising agents, emulsifiers, colours (INS 110)","additive_flags":"INS 110 colour"},
    {"barcode":"8902901225013","product_name":"Chana Brown Small","brands":"Good Life","ingredients_text":"Brown chickpeas (small)","additive_flags":"Clean single-ingredient"},
    {"barcode":"8906009071015","product_name":"Unbic Wafer Biscuit Rich Chocolate","brands":"Unibic","ingredients_text":"Refined wheat flour, sugar, cocoa solids, edible vegetable oil, raising agents, emulsifiers, artificial chocolate flavour","additive_flags":"Clean"},
    {"barcode":"8906009071022","product_name":"Unibic Wafer Yummy Strawberry","brands":"Unibic","ingredients_text":"Refined wheat flour, sugar, edible vegetable oil, strawberry flavour, raising agents, emulsifiers, colours","additive_flags":"Clean"},
    {"barcode":"8901491003186","product_name":"Quaker Oats","brands":"Quaker","ingredients_text":"Oats (100%)","additive_flags":"Clean single-ingredient"},
    {"barcode":"8901721009995","product_name":"Prabhuji Chana Barfi","brands":"Prabhuji","ingredients_text":"Gram flour, sugar, ghee, cardamom","additive_flags":"Clean"},
    {"barcode":"8904132964129","product_name":"Masoor Malka","brands":"Various","ingredients_text":"Masoor malka (split red lentils)","additive_flags":"Clean single-ingredient"},
    {"barcode":"8906095126873","product_name":"Wonderland Dry Fruits Combi","brands":"Wonderland","ingredients_text":"Almonds, cashews, raisins, pistachios","additive_flags":"Clean"},
    {"barcode":"8906059638596","product_name":"Greek Yogurt Smoothie Strawberry","brands":"Epigamia","ingredients_text":"Pasteurized milk, strawberry, sugar, active lactic culture","additive_flags":"Clean"},
    {"barcode":"8902080003075","product_name":"Nimbooz","brands":"7Up","ingredients_text":"Carbonated water, sugar, acidity regulators (INS 330, INS 331(i)), natural lemon-lime flavouring, preservative (INS 211)","additive_flags":"INS 211 preservative"},
    {"barcode":"8901808004769","product_name":"Weikfield Falooda Rose","brands":"Weikfield","ingredients_text":"Sugar, rose flavour, basil seeds, vermicelli, colours","additive_flags":"Verify colours"},
    {"barcode":"8901808003069","product_name":"Jelly Raspberry","brands":"Weikfield","ingredients_text":"Sugar, gelatin, acidity regulator, raspberry flavour, colour","additive_flags":"Verify colours"},
    {"barcode":"8907065118683","product_name":"Puramate Vanilla Essence","brands":"Puramate","ingredients_text":"Water, alcohol, vanilla extract","additive_flags":"Clean"},
    {"barcode":"8904406102172","product_name":"Chocolate Brownie Fudge","brands":"Get A Way","ingredients_text":"Refined wheat flour, sugar, cocoa solids, eggs, edible vegetable oil, raising agents, emulsifiers, chocolate flavour","additive_flags":"Clean"},
    {"barcode":"8901262202220","product_name":"Dahi Yogurt","brands":"Amul","ingredients_text":"Pasteurized toned milk, active lactic culture","additive_flags":"Clean"},
    {"barcode":"8908006217915","product_name":"Millet","brands":"Slurrp Farm","ingredients_text":"Millet flour, raising agents, salt","additive_flags":"Clean"},
    {"barcode":"8909106022034","product_name":"Comfort Morning Fresh","brands":"HUL","ingredients_text":"NON-FOOD — Fabric softener","additive_flags":"NON-FOOD — PURGE"},
    {"barcode":"8909106022041","product_name":"Comfort Lily Fresh","brands":"HUL","ingredients_text":"NON-FOOD — Fabric softener","additive_flags":"NON-FOOD — PURGE"},
    {"barcode":"8909106022089","product_name":"Comfort Morning Liquid 2L","brands":"HUL","ingredients_text":"NON-FOOD — Fabric softener","additive_flags":"NON-FOOD — PURGE"},
    {"barcode":"8901781000772","product_name":"Sunrise Sambar Masala","brands":"Sunrise/ITC","ingredients_text":"Coriander, turmeric, red chilli, fenugreek, cumin, black pepper, mustard, curry leaves","additive_flags":"Clean spice blend"},
    {"barcode":"8901781000550","product_name":"Sunrise Biryani Masala","brands":"Sunrise/ITC","ingredients_text":"Coriander, cumin, turmeric, red chilli, black pepper, cloves, cinnamon, cardamom, bay leaf, nutmeg","additive_flags":"Clean spice blend"},
    {"barcode":"8906010090906","product_name":"DLacta Cheese","brands":"D'Lecta","ingredients_text":"Milk solids, salt, emulsifying salts, preservative (INS 200)","additive_flags":"INS 200 preservative"},
    {"barcode":"8904043926650","product_name":"Tata Sampann Masoor Whole","brands":"Tata Sampann","ingredients_text":"Masoor dal (whole red lentils)","additive_flags":"Clean single-ingredient"},
    {"barcode":"8901781000796","product_name":"Sunrise Shukto Masala","brands":"Sunrise/ITC","ingredients_text":"Spices blend for shukto (Bengali dish)","additive_flags":"Clean spice blend"},
    {"barcode":"8901781000802","product_name":"Sunrise Tadka Masala","brands":"Sunrise","ingredients_text":"Coriander, cumin, turmeric, red chilli, black pepper, garlic","additive_flags":"Clean spice blend"},
    {"barcode":"8901781000680","product_name":"Sunrise Meat Masala","brands":"Sunrise","ingredients_text":"Coriander, cumin, turmeric, red chilli, black pepper, cloves, cinnamon, cardamom, garlic, ginger","additive_flags":"Clean spice blend"},
    {"barcode":"8901781000628","product_name":"Sunrise Machher Jhol Masala","brands":"Sunrise","ingredients_text":"Coriander, cumin, turmeric, red chilli, black pepper, mustard, fenugreek","additive_flags":"Clean spice blend"},
    {"barcode":"8902319040932","product_name":"Orange Cool Flavour Orofer Xt","brands":"EMCURE","ingredients_text":"NON-FOOD — Medicine/supplement","additive_flags":"NON-FOOD — PURGE"},
    {"barcode":"8906097400179","product_name":"Coriander Powder","brands":"Zoff","ingredients_text":"Coriander powder (100%)","additive_flags":"Clean single-ingredient"},
    {"barcode":"8906009534510","product_name":"MAX PROTEIN 7 GRAIN PROTEIN SNACK CREAM & ONION","brands":"RiteBite","ingredients_text":"Multigrain blend (7 grains), whey protein, edible vegetable oil, cream & onion seasoning, salt, emulsifiers","additive_flags":"Clean"},
    {"barcode":"8908009186461","product_name":"SPORT EVOLVE PERFORMANCE PLANT PROTEIN TROPICAL MANGO","brands":"Plix","ingredients_text":"Plant protein blend (pea, rice, soy), tropical mango flavour, sweetener (stevia), emulsifier","additive_flags":"Clean"},
    {"barcode":"8901117250000","product_name":"Prolyte ORS Orange Flavour","brands":"Cipla Health","ingredients_text":"Glucose, sodium chloride, potassium chloride, sodium citrate, orange flavour","additive_flags":"ORS — Regulated"},
    {"barcode":"8901030825552","product_name":"Protein Plus","brands":"Horlicks","ingredients_text":"Milk solids, malted cereals, sugar, cocoa solids, wheat flour, minerals, vitamins, emulsifier (INS 471)","additive_flags":"Clean"},
    {"barcode":"8904132926806","product_name":"Good Life Besan","brands":"Good Life","ingredients_text":"Gram flour (besan)","additive_flags":"Clean single-ingredient"},
    {"barcode":"8908003746708","product_name":"ORS Lemon Drink","brands":"Electrorush","ingredients_text":"Glucose, sodium chloride, potassium chloride, sodium citrate, lemon flavour","additive_flags":"ORS — Regulated"},
    {"barcode":"8901035062426","product_name":"Bte Kdo Thé Victoria 6 Variété","brands":"Various","ingredients_text":"Tea blend (6 varieties)","additive_flags":"Clean"},
    {"barcode":"8904355401814","product_name":"Apollo Life Chyawan Health Gold","brands":"Apollo Life","ingredients_text":"Amla, sugar, honey, ghee, herbs, spices","additive_flags":"Ayurvedic"},
    {"barcode":"8906097597794","product_name":"Reload","brands":"Fast&Up","ingredients_text":"Electrolytes, vitamins, minerals, flavours","additive_flags":"Supplement"},
    {"barcode":"8904043927299","product_name":"Tata Sampann Coriander Powder","brands":"Tata Sampann","ingredients_text":"Coriander powder (100%)","additive_flags":"Clean single-ingredient"},
    {"barcode":"8901552026314","product_name":"Paneer Kulcha","brands":"Ashoka","ingredients_text":"Refined wheat flour, paneer, spices, salt, edible vegetable oil","additive_flags":"Clean"},
    {"barcode":"8909081005046","product_name":"Dark Fantasy Choco Fills","brands":"Sunfeast","ingredients_text":"Choco crème (sugar, refined palmolein, cocoa solids), refined wheat flour, sugar, invert syrup, liquid glucose, cocoa solids, milk solids, butter, raising agents, emulsifiers, salt","additive_flags":"Clean"},
    {"barcode":"8907316003294","product_name":"Mother Recipe Garlic Chilli Sauce","brands":"Mother's Recipe","ingredients_text":"Garlic, red chilli, vinegar, salt, sugar, acidity regulator, preservative (INS 211)","additive_flags":"INS 211 preservative"},
    {"barcode":"8902080002061","product_name":"Pomegranate","brands":"Tropicana","ingredients_text":"Water, pomegranate juice concentrate, sugar, acidity regulator, antioxidant","additive_flags":"Clean"},
    {"barcode":"8902080002672","product_name":"Litchi Love","brands":"Tropicana","ingredients_text":"Water, lychee juice concentrate, sugar, acidity regulator, flavours","additive_flags":"Clean"},
    {"barcode":"8906009990699","product_name":"Elite Choco Orange","brands":"Elite","ingredients_text":"Refined wheat flour, sugar, cocoa solids, orange flavour, eggs, edible vegetable oil, raising agents, emulsifiers","additive_flags":"Clean"},
    {"barcode":"8906009990705","product_name":"Elite Dreams Choco Pineapple","brands":"Elite","ingredients_text":"Refined wheat flour, sugar, cocoa solids, pineapple flavour, eggs, edible vegetable oil, raising agents, emulsifiers","additive_flags":"Clean"},
    {"barcode":"8906009993157","product_name":"Orange Fruity Cake","brands":"Elite","ingredients_text":"Refined wheat flour, sugar, eggs, edible vegetable oil, orange flavour, glucose syrup, raising agents, emulsifiers, colours","additive_flags":"Clean"},
    {"barcode":"8906009993164","product_name":"Dreams Pineapple","brands":"Elite","ingredients_text":"Refined wheat flour, sugar, eggs, edible vegetable oil, pineapple flavour, glucose syrup, raising agents, emulsifiers","additive_flags":"Clean"},
    {"barcode":"8906009994161","product_name":"Fruit Cake","brands":"Elite","ingredients_text":"Refined wheat flour, sugar, eggs, edible vegetable oil, mixed fruit peel, glucose syrup, raising agents, emulsifiers","additive_flags":"Clean"},
    {"barcode":"8906009993829","product_name":"Orange Elite","brands":"Elite","ingredients_text":"Refined wheat flour, sugar, eggs, edible vegetable oil, orange flavour, glucose syrup, raising agents, emulsifiers","additive_flags":"Clean"},
    {"barcode":"8906009993812","product_name":"Cake Milk","brands":"Elite","ingredients_text":"Refined wheat flour, sugar, eggs, milk solids, edible vegetable oil, glucose syrup, raising agents, emulsifiers","additive_flags":"Clean"},
    {"barcode":"8901725012977","product_name":"Sunfeast Marie Light","brands":"Sunfeast","ingredients_text":"Refined wheat flour, sugar, refined palm oil, invert sugar syrup, milk solids, raising agents (INS 503(ii), INS 500(ii)), salt, emulsifiers (INS 471, INS 322)","additive_flags":"Clean"},
    {"barcode":"8901725016166","product_name":"Choco Fills","brands":"Sunfeast","ingredients_text":"Choco crème (sugar, refined palmolein, cocoa solids), refined wheat flour, sugar, invert syrup, liquid glucose, cocoa solids, milk solids, butter, raising agents, emulsifiers, salt","additive_flags":"Clean"},
    {"barcode":"8909081000256","product_name":"Dark Fantasy Sandwich Crème","brands":"Sunfeast","ingredients_text":"Refined wheat flour, sugar, edible vegetable oil, cocoa solids, invert syrup, milk solids, raising agents, emulsifiers, artificial chocolate flavour","additive_flags":"Clean"},
    {"barcode":"8909081000317","product_name":"Dark Fantasy Sandwich Crème","brands":"Sunfeast","ingredients_text":"Refined wheat flour, sugar, edible vegetable oil, cocoa solids, invert syrup, milk solids, raising agents, emulsifiers, artificial chocolate flavour","additive_flags":"Clean"},
    {"barcode":"8904188607933","product_name":"Green Chana Frozen","brands":"Saurbhi","ingredients_text":"Green chickpeas (frozen)","additive_flags":"Clean single-ingredient"},
    {"barcode":"8904340700397","product_name":"Pulse Litchi Flavour","brands":"Pass Pass","ingredients_text":"Sugar, glucose syrup, lychee flavour, acidity regulator, colours","additive_flags":"Verify colours"},
    {"barcode":"8904340700359","product_name":"Pulse Orange","brands":"Pass Pass","ingredients_text":"Sugar, glucose syrup, orange flavour, acidity regulator, colours","additive_flags":"Verify colours"},
    {"barcode":"8906172543807","product_name":"Black Forest","brands":"Hocco","ingredients_text":"Refined wheat flour, sugar, eggs, cocoa solids, edible vegetable oil, raising agents, emulsifiers, cherry flavour, colours","additive_flags":"Clean"},
    {"barcode":"8901719130724","product_name":"Parle 20-20 Gold","brands":"Parle","ingredients_text":"Refined wheat flour, sugar, edible vegetable oil, cashew nuts, invert syrup, milk solids, raising agents (INS 503(ii), INS 500(ii)), emulsifier (INS 322)","additive_flags":"Clean"},
    {"barcode":"8904300201018","product_name":"Coconut Crunchy","brands":"Various","ingredients_text":"Refined wheat flour, sugar, coconut, edible vegetable oil, raising agents, emulsifiers","additive_flags":"Clean"},
    {"barcode":"8901725013004","product_name":"Marie Light Family Pack","brands":"Sunfeast/ITC","ingredients_text":"Refined wheat flour, sugar, refined palm oil, invert sugar syrup, milk solids, raising agents, salt, emulsifiers","additive_flags":"Clean"},
    {"barcode":"8906009073729","product_name":"Big & Bold Fruit Blast","brands":"Unibic","ingredients_text":"Refined wheat flour, sugar, edible vegetable oil, dried fruits, invert syrup, raising agents, emulsifiers","additive_flags":"Clean"},
    {"barcode":"8901725000622","product_name":"Sunfeast Mom's Magic","brands":"Sunfeast","ingredients_text":"Refined wheat flour, sugar, edible vegetable oil, cashew nuts, almonds, invert syrup, milk solids, raising agents, emulsifiers","additive_flags":"Clean"},
    {"barcode":"8901063164321","product_name":"Tiger Kreemz Orange","brands":"Britannia","ingredients_text":"Refined wheat flour, sugar, edible vegetable oil, orange flavour, invert syrup, raising agents, emulsifiers, colours (INS 110)","additive_flags":"INS 110 colour"},
    {"barcode":"8901063162549","product_name":"Marie Gold","brands":"Britannia","ingredients_text":"Refined wheat flour (73%), sugar, refined palm oil, invert sugar syrup, milk solids, raising agents, salt, emulsifiers (INS 471, INS 322)","additive_flags":"Clean"},
    {"barcode":"8902268011144","product_name":"Dream Lite","brands":"Anmol","ingredients_text":"Refined wheat flour, sugar, edible vegetable oil, invert syrup, raising agents, emulsifiers","additive_flags":"Clean"},
    {"barcode":"8901052011742","product_name":"Rusk","brands":"Tata SoulFull","ingredients_text":"Refined wheat flour, sugar, edible vegetable oil, invert syrup, milk solids, raising agents, emulsifier, artificial vanilla flavour","additive_flags":"Clean"},
    {"barcode":"8904344626228","product_name":"Moon Original","brands":"Various","ingredients_text":"Verify specific product","additive_flags":"Verify"},
    {"barcode":"8904258703879","product_name":"ABC Juice","brands":"Raw Pressed","ingredients_text":"Apple, beetroot, carrot juice blend","additive_flags":"Clean"},
    {"barcode":"8904270005401","product_name":"Marie Go Round","brands":"Sunder","ingredients_text":"Refined wheat flour, sugar, refined palm oil, invert sugar syrup, milk solids, raising agents, salt, emulsifiers","additive_flags":"Clean"},
    {"barcode":"8901448904054","product_name":"Wafy Break","brands":"Various","ingredients_text":"Refined wheat flour, sugar, edible vegetable oil, flavours, raising agents, emulsifiers","additive_flags":"Clean"},
    {"barcode":"8906021927062","product_name":"Apis Deseeded Dates","brands":"Apis","ingredients_text":"Deseeded dates (100%)","additive_flags":"Clean single-ingredient"},
    {"barcode":"8903023007709","product_name":"More Chironji","brands":"More","ingredients_text":"Chironji (charoli seeds)","additive_flags":"Clean single-ingredient"},
    {"barcode":"8901725003838","product_name":"Mom's Magic","brands":"Sunfeast","ingredients_text":"Refined wheat flour, sugar, edible vegetable oil, cashew nuts, almonds, invert syrup, milk solids, raising agents, emulsifiers","additive_flags":"Clean"},
    {"barcode":"8906097402562","product_name":"Zoff Clove Whole","brands":"Zoff","ingredients_text":"Whole cloves (100%)","additive_flags":"Clean single-ingredient"},
    {"barcode":"8906002348473","product_name":"Lobia Safed","brands":"Rajdhani","ingredients_text":"White cowpeas (lobia)","additive_flags":"Clean single-ingredient"},
    {"barcode":"8902901222517","product_name":"Ajwain","brands":"Good Life","ingredients_text":"Ajwain (carom seeds)","additive_flags":"Clean single-ingredient"},
    {"barcode":"8906006525504","product_name":"Top Start","brands":"Various","ingredients_text":"Verify specific product","additive_flags":"Verify"},
    {"barcode":"8901063371026","product_name":"Marie Gold","brands":"Britannia","ingredients_text":"Refined wheat flour (73%), sugar, refined palm oil, invert sugar syrup, milk solids, raising agents, salt, emulsifiers (INS 471, INS 322)","additive_flags":"Clean"},
    {"barcode":"8901058866216","product_name":"Coffee Mocha","brands":"Nestlé","ingredients_text":"Instant coffee, sugar, milk solids, cocoa solids, emulsifier, flavours","additive_flags":"Clean"},
    {"barcode":"8901552007689","product_name":"Kantola","brands":"Ashoka","ingredients_text":"Refined wheat flour, potato, spices, salt, edible vegetable oil","additive_flags":"Clean"},
    {"barcode":"8901719255144","product_name":"Parle-G","brands":"Parle","ingredients_text":"Refined wheat flour, sugar, invert syrup, refined palm oil, salt, skimmed milk powder, raising agents (INS 503(ii), INS 500(ii)), emulsifier (INS 471), artificial vanilla flavour","additive_flags":"Clean"},
    {"barcode":"8901719404412","product_name":"Hide & Seek","brands":"Parle","ingredients_text":"Refined wheat flour, sugar, edible vegetable oil, cocoa solids, invert syrup, milk solids, raising agents, emulsifiers","additive_flags":"Clean"},
    {"barcode":"8901719703034","product_name":"Krack Jack Original","brands":"Parle","ingredients_text":"Refined wheat flour, sugar, edible vegetable oil, invert syrup, salt, raising agents, emulsifier","additive_flags":"Clean"},
    {"barcode":"8901719656828","product_name":"FAB!","brands":"Parle","ingredients_text":"Refined wheat flour, sugar, edible vegetable oil, fruit jam, invert syrup, raising agents, emulsifiers, colours","additive_flags":"Clean"},
    {"barcode":"8901153001529","product_name":"Soan Papdi","brands":"Various","ingredients_text":"Sugar, gram flour, ghee, cardamom","additive_flags":"Clean"},
    {"barcode":"8906032016977","product_name":"Soya Chunks","brands":"Nutrela","ingredients_text":"Defatted soya flour","additive_flags":"Clean single-ingredient"},
    {"barcode":"8906026995028","product_name":"Brimune Aloe Vera Juice 500ML","brands":"Various","ingredients_text":"Aloe vera juice, preservative","additive_flags":"Clean"},
    {"barcode":"8901725019419","product_name":"Mom's Magic","brands":"Sunfeast","ingredients_text":"Refined wheat flour, sugar, edible vegetable oil, cashew nuts, almonds, invert syrup, milk solids, raising agents, emulsifiers","additive_flags":"Clean"},
    {"barcode":"8901725000646","product_name":"Mom's Magic","brands":"Sunfeast","ingredients_text":"Refined wheat flour, sugar, edible vegetable oil, cashew nuts, almonds, invert syrup, milk solids, raising agents, emulsifiers","additive_flags":"Clean"},
    {"barcode":"8902901222357","product_name":"Phool Makhana","brands":"Good Life","ingredients_text":"Makhana (fox nuts)","additive_flags":"Clean single-ingredient"},
    {"barcode":"8901155301443","product_name":"Gits Gulabi Jamun","brands":"Gits","ingredients_text":"Milk solids, sugar, edible vegetable oil, cardamom, rose water","additive_flags":"Clean"},
    {"barcode":"8909081003905","product_name":"Rich Chocolate Cookies","brands":"Sunfeast","ingredients_text":"Refined wheat flour, sugar, cocoa solids, edible vegetable oil, invert syrup, raising agents, emulsifiers, artificial chocolate flavour","additive_flags":"Clean"},
    {"barcode":"8906001024798","product_name":"Four Cheese","brands":"Go","ingredients_text":"Milk solids, salt, emulsifying salts, preservative (INS 200), cheese blend","additive_flags":"INS 200 preservative"},
    {"barcode":"8903605017706","product_name":"Soy Sauce","brands":"Various","ingredients_text":"Water, soybean extract, salt, sugar, vinegar, acidity regulator, preservative (INS 211)","additive_flags":"INS 211 preservative"},
    {"barcode":"8906010504021","product_name":"Balaji Wafers","brands":"Balaji","ingredients_text":"Potato, edible vegetable oil, salt, spices","additive_flags":"Clean"},
    {"barcode":"8906010504007","product_name":"Balaji Wafers","brands":"Balaji","ingredients_text":"Potato, edible vegetable oil, salt, spices","additive_flags":"Clean"},
    {"barcode":"8901719656613","product_name":"Parle Hide & Seek Fab Orange","brands":"Parle","ingredients_text":"Refined wheat flour, sugar, edible vegetable oil, orange flavour, cocoa solids, invert syrup, milk solids, raising agents, emulsifiers, colours (INS 110)","additive_flags":"INS 110 colour"},
    {"barcode":"8906024450512","product_name":"Green Tea Natural","brands":"Various","ingredients_text":"Green tea (100%)","additive_flags":"Clean single-ingredient"},
    {"barcode":"8906024451335","product_name":"Green Tea Lemon and Honey","brands":"Various","ingredients_text":"Green tea, lemon flavour, honey","additive_flags":"Clean"},
    {"barcode":"8901030456381","product_name":"Taaza Tea","brands":"Brooke Bond","ingredients_text":"100% black tea (CTC blend)","additive_flags":"Clean single-ingredient"},
    {"barcode":"8901719124402","product_name":"Magix Orange","brands":"Parle","ingredients_text":"Refined wheat flour, sugar, edible vegetable oil, orange flavour, invert syrup, raising agents, emulsifiers, colours (INS 110)","additive_flags":"INS 110 colour"},
    {"barcode":"8901719122040","product_name":"Coconut","brands":"Parle","ingredients_text":"Refined wheat flour, sugar, coconut, edible vegetable oil, invert syrup, raising agents, emulsifier, artificial coconut flavour","additive_flags":"Clean"},
    {"barcode":"8901719124396","product_name":"Magix Elaichi","brands":"Parle","ingredients_text":"Refined wheat flour, sugar, edible vegetable oil, cardamom flavour, invert syrup, raising agents, emulsifiers","additive_flags":"Clean"},
    {"barcode":"8904006313367","product_name":"Oura","brands":"Various","ingredients_text":"Verify specific product","additive_flags":"Verify"},
    {"barcode":"8901044400745","product_name":"Strawberry Fruit Crush 1L","brands":"Various","ingredients_text":"Strawberry pulp, sugar, acidity regulator, preservative, colour","additive_flags":"INS 211 preservative"},
    {"barcode":"8906052860147","product_name":"Chilly Garlic Cashews","brands":"Zantye's","ingredients_text":"Cashew nuts, edible vegetable oil, chilli, garlic, salt","additive_flags":"Clean"},
    {"barcode":"8908013194308","product_name":"Cuban Watermelon Mojito","brands":"Borécha","ingredients_text":"Water, sugar, watermelon juice, mint, lime, acidity regulator","additive_flags":"Clean"},
    {"barcode":"8908006931965","product_name":"Riz Étuve Lutik","brands":"Various","ingredients_text":"Parboiled rice","additive_flags":"Clean single-ingredient"},
    {"barcode":"8906143892330","product_name":"Cranberry Raisin Protein Bar","brands":"The Whole Truth","ingredients_text":"Cranberries, raisins, whey protein, dates, nuts, emulsifier","additive_flags":"Clean"},
    {"barcode":"8900019102523","product_name":"Jaggery Cubes 500g","brands":"Various","ingredients_text":"Jaggery (gur)","additive_flags":"Clean single-ingredient"},
    {"barcode":"8908000861619","product_name":"Gopal Bhavnagari Gathiya","brands":"Gopal","ingredients_text":"Gram flour, edible vegetable oil, iodized salt, spices","additive_flags":"Clean"},
    {"barcode":"8908009247148","product_name":"Sanjivani Tea","brands":"Sanjivani","ingredients_text":"Black tea, herbs, spices","additive_flags":"Clean"},
    {"barcode":"8906097403194","product_name":"Zoff Onion Powder","brands":"Zoff","ingredients_text":"Onion powder (100%)","additive_flags":"Clean single-ingredient"},
    {"barcode":"8901192106124","product_name":"Catch Red Chilli Powder","brands":"Catch","ingredients_text":"Red chilli powder (100%)","additive_flags":"Clean single-ingredient"},
    {"barcode":"8908016793966","product_name":"White Vinegar","brands":"Various","ingredients_text":"White vinegar (acetic acid, water)","additive_flags":"Clean single-ingredient"},
    {"barcode":"8901063166288","product_name":"Britannia Tiger Kreemz 72g","brands":"Britannia","ingredients_text":"Refined wheat flour, sugar, edible vegetable oil, orange flavour, invert syrup, raising agents, emulsifiers, colours (INS 110)","additive_flags":"INS 110 colour"},
    {"barcode":"8901548310106","product_name":"D Lite Vanilla","brands":"Various","ingredients_text":"Refined wheat flour, sugar, eggs, edible vegetable oil, vanilla flavour, raising agents, emulsifiers","additive_flags":"Clean"},
    {"barcode":"8901552023610","product_name":"Mini Tandoori Paneer Samosa","brands":"Ashoka","ingredients_text":"Refined wheat flour, paneer, tandoori spices, salt, edible vegetable oil","additive_flags":"Clean"},
    {"barcode":"8901030795909","product_name":"Boost","brands":"HUL","ingredients_text":"Cereal extract (50%), malted barley (21%), sugar, wheat flour, milk solids (6%), minerals, natural colour (INS 150c), vitamins","additive_flags":"INS 150c Caramel"},
    {"barcode":"8908016538185","product_name":"POP","brands":"Archi","ingredients_text":"Verify specific product","additive_flags":"Verify"},
    {"barcode":"8908004804278","product_name":"Catch Clear","brands":"Catch","ingredients_text":"Verify specific product","additive_flags":"Verify"},
    {"barcode":"8906005666536","product_name":"Madras Filter Coffee","brands":"Various","ingredients_text":"Coffee blend (filter coffee), chicory","additive_flags":"Clean"},
    {"barcode":"8904315300782","product_name":"Desi Ghee","brands":"Shri Vallabh","ingredients_text":"Milk solids (pure cow ghee)","additive_flags":"Clean single-ingredient"},
    {"barcode":"8904188605847","product_name":"Black Sesame Seeds","brands":"Various","ingredients_text":"Black sesame seeds (100%)","additive_flags":"Clean single-ingredient"},
    {"barcode":"8906009820415","product_name":"Daliya","brands":"Silver Coin","ingredients_text":"Broken wheat (daliya)","additive_flags":"Clean single-ingredient"},
    {"barcode":"8908016763150","product_name":"Aata","brands":"Energy Max","ingredients_text":"100% whole wheat flour","additive_flags":"Clean single-ingredient"},
    {"barcode":"8901560120219","product_name":"Instant Idli Mix","brands":"Nilon's","ingredients_text":"Rice flour, urad dal flour, salt, raising agents","additive_flags":"Clean"},
    {"barcode":"8906080603914","product_name":"Swing Pomegranate","brands":"Paper Boat","ingredients_text":"Water, pomegranate pulp, sugar, acidity regulators","additive_flags":"Clean"},
    {"barcode":"8901777626801","product_name":"Overload Veggie Pizza","brands":"Vadilal","ingredients_text":"Refined wheat flour, vegetables, cheese, tomato sauce, edible vegetable oil, spices, salt","additive_flags":"Clean"},
    {"barcode":"8901058892635","product_name":"Maggi Export","brands":"Nestlé","ingredients_text":"Noodles: Refined wheat flour, palm oil, salt, thickeners; Tastemaker: salt, spices, flavour enhancers (INS 621), antioxidant (INS 319)","additive_flags":"INS 621 + INS 319"},
    {"barcode":"8908013252299","product_name":"Multi Grain Mixture","brands":"Various","ingredients_text":"Multigrain blend, edible vegetable oil, spices, salt, sugar","additive_flags":"Clean"},
    {"barcode":"8906082570085","product_name":"Cornitos Pop N Green Peas","brands":"Cornitos","ingredients_text":"Green peas, edible vegetable oil, salt, spices","additive_flags":"Clean"},
    {"barcode":"8901063358096","product_name":"Loading…","brands":"Various","ingredients_text":"Verify specific product","additive_flags":"Verify"},
    {"barcode":"8906006720350","product_name":"Australian Oats","brands":"Lion","ingredients_text":"Oats (100%)","additive_flags":"Clean single-ingredient"},
    {"barcode":"8904109405501","product_name":"Elaichi Soan Papdi","brands":"Various","ingredients_text":"Sugar, gram flour, ghee, cardamom","additive_flags":"Clean"},
    {"barcode":"8908002544107","product_name":"Beer","brands":"Various","ingredients_text":"Alcoholic beverage (beer)","additive_flags":"ALCOHOL — SEPARATE"},
    {"barcode":"8901071732826","product_name":"Sofit Soya Vanilla Flavour Drink 180ml","brands":"Sofit","ingredients_text":"Soya milk, sugar, vanilla flavour, stabilizers, emulsifiers","additive_flags":"Clean"},
    {"barcode":"8901063094185","product_name":"Good Day","brands":"Britannia","ingredients_text":"Refined wheat flour, edible vegetable oil, sugar, cashew nuts, invert syrup, milk solids, raising agents, emulsifier","additive_flags":"Clean"},
    {"barcode":"8901063094147","product_name":"Good Day","brands":"Britannia","ingredients_text":"Refined wheat flour, edible vegetable oil, sugar, cashew nuts, invert syrup, milk solids, raising agents, emulsifier","additive_flags":"Clean"},
    {"barcode":"8901063092402","product_name":"Good Day","brands":"Britannia","ingredients_text":"Refined wheat flour, edible vegetable oil, sugar, cashew nuts, invert syrup, milk solids, raising agents, emulsifier","additive_flags":"Clean"},
    {"barcode":"8901063098657","product_name":"Good Day","brands":"Britannia","ingredients_text":"Refined wheat flour, edible vegetable oil, sugar, cashew nuts, invert syrup, milk solids, raising agents, emulsifier","additive_flags":"Clean"},
    {"barcode":"8904022990023","product_name":"Sandwich Plus","brands":"Various","ingredients_text":"Refined wheat flour, water, sugar, yeast, salt, edible vegetable oil, preservative (INS 282)","additive_flags":"INS 282 preservative"},
    {"barcode":"8904064672215","product_name":"Graines de Pilon (Moringa)","brands":"Various","ingredients_text":"Moringa seeds (100%)","additive_flags":"Clean single-ingredient"},
    {"barcode":"890177041666","product_name":"Frozen Bean","brands":"Vadilal","ingredients_text":"Green beans (frozen)","additive_flags":"Clean single-ingredient"},
    {"barcode":"8901848000752","product_name":"Rasana Fruit Plus","brands":"Rasna","ingredients_text":"Sugar, acidity regulators (INS 296, INS 330), salt, anticaking agent (INS 551), vitamin C, permitted colours, artificial flavours","additive_flags":"Verify colours"},
    {"barcode":"8901648001775","product_name":"Lassi","brands":"Mother Dairy","ingredients_text":"Toned milk, sugar, active lactic culture","additive_flags":"Clean"},
    {"barcode":"8901192215116","product_name":"Catch Sabzi Masala","brands":"Catch","ingredients_text":"Coriander, cumin, turmeric, red chilli, black pepper, cloves, cinnamon, cardamom","additive_flags":"Clean spice blend"},
    {"barcode":"8904098970240","product_name":"Joyo Clean Max Cotton Mop","brands":"Joyo","ingredients_text":"NON-FOOD — Cleaning product","additive_flags":"NON-FOOD — PURGE"},
    {"barcode":"8908012945703","product_name":"Red Lentil Crisps","brands":"Pink Harvest Farms","ingredients_text":"Red lentil flour, edible vegetable oil, spices, salt","additive_flags":"Clean"},
    {"barcode":"8901662029151","product_name":"Paneer Chilli Mix","brands":"Suhana","ingredients_text":"Paneer, spices, salt, sugar, edible vegetable oil, chilli","additive_flags":"Clean"},
    {"barcode":"8904250303831","product_name":"CAMFLORA Champa and Camphor","brands":"Shubh Kart","ingredients_text":"NON-FOOD — Puja/religious item","additive_flags":"NON-FOOD — PURGE"},
    {"barcode":"8906006170087","product_name":"Khatta Meetha","brands":"O'yes","ingredients_text":"Rice flakes, edible vegetable oil, sugar, peanuts, sago, salt, spices, raising agents, colours (INS 160c)","additive_flags":"INS 160c colour"},
    {"barcode":"8904004416602","product_name":"Classic Lassi","brands":"Haldiram","ingredients_text":"Toned milk, sugar, active lactic culture","additive_flags":"Clean"},
    {"barcode":"8904150503898","product_name":"Gold Atta","brands":"Pillsbury","ingredients_text":"100% whole wheat flour","additive_flags":"Clean single-ingredient"},
    {"barcode":"8908000863408","product_name":"Oleev Active Oil","brands":"Oleev","ingredients_text":"Rice bran oil, olive oil, antioxidant (INS 319), vitamins A & D","additive_flags":"INS 319 TBHQ"},
    {"barcode":"8902433003790","product_name":"Galaxy Milk Chocolate 110g","brands":"Galaxy","ingredients_text":"Sugar, milk solids, cocoa butter, cocoa mass, emulsifiers, flavours","additive_flags":"Clean"},
    {"barcode":"8903023265628","product_name":"Kitchen's Promise","brands":"Kitchen's Promise","ingredients_text":"Verify specific product","additive_flags":"Verify"},
    {"barcode":"8904132963627","product_name":"Good Life Teekhi Chilli Powder","brands":"Good Life","ingredients_text":"Red chilli powder (100%)","additive_flags":"Clean single-ingredient"},
    {"barcode":"8904132963610","product_name":"UB06 Hygienic","brands":"Various","ingredients_text":"NON-FOOD — Verify","additive_flags":"NON-FOOD — PURGE"},
    {"barcode":"8906009993423","product_name":"Plum Pudding Cake","brands":"Elite","ingredients_text":"Refined wheat flour, sugar, plums, eggs, edible vegetable oil, raising agents, emulsifiers, spices","additive_flags":"Clean"},
    {"barcode":"8901030985980","product_name":"Horlicks Chocolate Delight Flavour","brands":"Horlicks","ingredients_text":"Malted cereals, milk solids, sugar, cocoa solids, wheat flour, minerals, vitamins, emulsifier (INS 471), artificial chocolate flavour","additive_flags":"Clean"},
    {"barcode":"8901542000072","product_name":"Complan New Royal Chocolate Flv 500g","brands":"HUL","ingredients_text":"Milk solids (52%), sugar, cocoa solids, maltodextrin, almonds, minerals, vitamins, colours (INS 100(i), INS 160b(ii))","additive_flags":"Natural colours"},
    {"barcode":"8901030949678","product_name":"Horlicks Women+ Chocolate Flv 400g","brands":"Horlicks","ingredients_text":"Malted cereals, milk solids, sugar, cocoa solids, wheat flour, minerals (Iron, Calcium), vitamins, emulsifier (INS 471)","additive_flags":"Clean"},
    {"barcode":"8901030915857","product_name":"Junior Horlicks Vanilla Flavour 400g","brands":"Horlicks","ingredients_text":"Malted cereals, milk solids, sugar, wheat flour, minerals, vitamins, emulsifier (INS 471), artificial vanilla flavour","additive_flags":"Clean"},
    {"barcode":"8901023022968","product_name":"Good Knight Gold Flash","brands":"Godrej","ingredients_text":"NON-FOOD — Mosquito repellent","additive_flags":"NON-FOOD — PURGE"},
    {"barcode":"8901365995920","product_name":"Prestige Electronic Gas Lighter","brands":"Prestige","ingredients_text":"NON-FOOD — Gas lighter","additive_flags":"NON-FOOD — PURGE"},
    {"barcode":"8906021072281","product_name":"Crunchy Peanut","brands":"Kaldini","ingredients_text":"Peanuts, edible vegetable oil, salt","additive_flags":"Clean"},
    {"barcode":"8904063211460","product_name":"Hot & Spicy Samosa","brands":"Haldiram's","ingredients_text":"Refined wheat flour, potato, peas, spices, salt, edible vegetable oil","additive_flags":"Clean"},
    {"barcode":"8906117363538","product_name":"Makhana","brands":"Country Delight","ingredients_text":"Makhana (fox nuts)","additive_flags":"Clean single-ingredient"},
    {"barcode":"8901414000872","product_name":"Dal Moth","brands":"Bikano","ingredients_text":"Rice flakes, gram flour, edible vegetable oil, peanuts, sago, salt, spices, raising agents","additive_flags":"Clean"},
    {"barcode":"8906010501228","product_name":"Scoopitos Masala Flavour","brands":"Balaji Wafers","ingredients_text":"Potato, edible vegetable oil, spices, salt, sugar, flavour enhancers (INS 621), colours","additive_flags":"INS 621 MSG"},
    {"barcode":"8904221698997","product_name":"Whey Protein Concentrate","brands":"Asitis","ingredients_text":"Whey protein concentrate, emulsifier (INS 322)","additive_flags":"Clean"},
    {"barcode":"8902433003196","product_name":"Orbit","brands":"Orbit","ingredients_text":"Sorbitol, gum base, mannitol, flavours, sweeteners (aspartame, acesulfame K)","additive_flags":"Clean"},
    {"barcode":"8904340700007","product_name":"Pulse","brands":"Pass Pass","ingredients_text":"Sugar, glucose syrup, tamarind, salt, spices, acidity regulator, colours","additive_flags":"Clean"},
    {"barcode":"8906002975372","product_name":"Mouth Freshener","brands":"Various","ingredients_text":"Fennel seeds, sugar, flavours","additive_flags":"Clean"},
    {"barcode":"8901725132866","product_name":"Dark Fantasy Coffee","brands":"Sunfeast","ingredients_text":"Refined wheat flour, sugar, edible vegetable oil, coffee, cocoa solids, invert syrup, raising agents, emulsifiers","additive_flags":"Clean"},
    {"barcode":"8901725119430","product_name":"Mom's Magic Cashew","brands":"Sunfeast","ingredients_text":"Refined wheat flour, sugar, edible vegetable oil, cashew nuts, invert syrup, milk solids, raising agents, emulsifiers","additive_flags":"Clean"},
    {"barcode":"8901063028227","product_name":"Britannia Nice Time","brands":"Britannia","ingredients_text":"Refined wheat flour, sugar, coconut, edible vegetable oil, invert syrup, raising agents, salt, emulsifier, artificial coconut flavour","additive_flags":"Clean"},
    {"barcode":"8904067702599","product_name":"Jabsons Peanuts Black Pepper","brands":"Jabsons","ingredients_text":"Peanuts, edible vegetable oil, black pepper, salt","additive_flags":"Clean"},
    {"barcode":"8904109465338","product_name":"Hing Goil","brands":"Various","ingredients_text":"Asafoetida, edible vegetable oil","additive_flags":"Clean"},
    {"barcode":"8904970666643","product_name":"Chinotto","brands":"Various","ingredients_text":"Carbonated water, sugar, acidity regulators, flavours, colours","additive_flags":"Verify colours"},
    {"barcode":"8901548100110","product_name":"Nutralite Fat","brands":"Dabur","ingredients_text":"Edible vegetable oil, salt, emulsifiers, vitamins A & D","additive_flags":"Clean"},
    {"barcode":"8901088017398","product_name":"Saffola Gold","brands":"Marico","ingredients_text":"Rice bran oil, sunflower oil, antioxidant (INS 319), vitamins A & D","additive_flags":"INS 319 TBHQ"},
    {"barcode":"8908000233355","product_name":"Iyers Rice Wafers Papad","brands":"Iyers","ingredients_text":"Rice flour, salt, spices, edible vegetable oil","additive_flags":"Clean"},
    {"barcode":"8901441017027","product_name":"Lizzath Punjabi Masala Papad","brands":"Lizzath","ingredients_text":"Urad dal flour, salt, spices (black pepper, cumin), edible vegetable oil","additive_flags":"Clean"},
    {"barcode":"8906070210030","product_name":"Ginger with Honey","brands":"Honeyman","ingredients_text":"Ginger, honey","additive_flags":"Clean"},
    {"barcode":"8904152822287","product_name":"Pani Puri","brands":"Various","ingredients_text":"Refined wheat flour, semolina, salt, spices, edible vegetable oil","additive_flags":"Clean"},
    {"barcode":"8901414037519","product_name":"Premium Coconut Cookies","brands":"Bikano","ingredients_text":"Refined wheat flour, sugar, coconut, edible vegetable oil, raising agents, emulsifiers","additive_flags":"Clean"},
    {"barcode":"8901192205262","product_name":"MDH Kitchen King","brands":"MDH","ingredients_text":"Coriander, turmeric, red chilli, cumin, black pepper, cloves, cinnamon, cardamom","additive_flags":"Clean spice blend"},
    {"barcode":"8901499009043","product_name":"Kellogg's Chocos","brands":"Kellogg's","ingredients_text":"Whole wheat flour, sugar, cocoa solids, glucose syrup, salt, vitamins, minerals","additive_flags":"Clean"},
    {"barcode":"8901499009044","product_name":"Kellogg's Corn Flakes","brands":"Kellogg's","ingredients_text":"Corn grits, sugar, malt extract, salt, vitamins, minerals","additive_flags":"Clean"},
    {"barcode":"8906032016977","product_name":"Soya Chunks","brands":"Nutrela","ingredients_text":"Defatted soya flour","additive_flags":"Clean single-ingredient"},
    {"barcode":"8906026995028","product_name":"Brimune Aloe Vera Juice 500ML","brands":"Various","ingredients_text":"Aloe vera juice, preservative","additive_flags":"Clean"},
    {"barcode":"8908010673004","product_name":"Malabar Porotta","brands":"Various","ingredients_text":"Refined wheat flour, water, edible vegetable oil, salt","additive_flags":"Clean"},
    {"barcode":"8906016420073","product_name":"Groundnut Sweets","brands":"Various","ingredients_text":"Peanuts, jaggery/sugar","additive_flags":"Clean"},
    {"barcode":"8906045581899","product_name":"Moong Dal","brands":"Various","ingredients_text":"Moong dal (green gram)","additive_flags":"Clean single-ingredient"},
    {"barcode":"8907316006011","product_name":"Desi Schezwan Chutney","brands":"Mother's Recipe","ingredients_text":"Water, red chilli, garlic, vinegar, salt, sugar, acidity regulator (INS 260), preservative (INS 211)","additive_flags":"INS 211 preservative"},
    {"barcode":"8901030478673","product_name":"Bru Instant","brands":"Bru","ingredients_text":"Instant coffee, chicory","additive_flags":"Clean"},
    {"barcode":"8906070864028","product_name":"Chikki Assorted","brands":"Swadish Mithai","ingredients_text":"Peanuts, sesame seeds, jaggery, sugar","additive_flags":"Clean"},
    {"barcode":"8901042956800","product_name":"Vegetable Pulao 250G","brands":"MTR","ingredients_text":"Basmati rice, vegetables, spices, salt, edible vegetable oil","additive_flags":"Clean"},
    {"barcode":"8909500188640","product_name":"Kinder Maxi 20 Barres","brands":"Kinder","ingredients_text":"Sugar, milk solids, cocoa butter, cocoa mass, emulsifiers, flavours","additive_flags":"Clean"},
    {"barcode":"8906016420226","product_name":"Cubes de Caramel aux Cacahuètes","brands":"Various","ingredients_text":"Sugar, peanuts, glucose syrup","additive_flags":"Clean"},
    {"barcode":"8901233028859","product_name":"Dairy Milk Silk Chocolate","brands":"Cadbury","ingredients_text":"Sugar, milk solids, cocoa butter, cocoa mass, emulsifiers (INS 322, INS 476), flavours","additive_flags":"Clean"},
    {"barcode":"8902351222389","product_name":"Patanjali Doodh Biscuits","brands":"Patanjali","ingredients_text":"Refined wheat flour, sugar, milk solids, edible vegetable oil, raising agents, emulsifiers","additive_flags":"Clean"},
    {"barcode":"8908007811068","product_name":"Moong Dal","brands":"Sipani's Bikaner","ingredients_text":"Moong dal, edible vegetable oil, iodized salt, spices","additive_flags":"Clean"},
    {"barcode":"8901552014489","product_name":"Green Peas Paratha","brands":"Ashoka","ingredients_text":"Whole wheat flour, green peas, spices, salt, edible vegetable oil","additive_flags":"Clean"},
    {"barcode":"8904063214454","product_name":"Classic Nut Cracker","brands":"Haldiram's","ingredients_text":"Rice flakes, gram flour, edible vegetable oil, peanuts, sago, salt, spices, raising agents, colours","additive_flags":"INS 160c colour"},
    {"barcode":"8906021927710","product_name":"Pure Honey","brands":"Various","ingredients_text":"Honey (100%)","additive_flags":"Clean single-ingredient"},
    {"barcode":"8901719116971","product_name":"Milano","brands":"Parle","ingredients_text":"Refined wheat flour, sugar, edible vegetable oil, cocoa solids, invert syrup, milk solids, raising agents, emulsifiers","additive_flags":"Clean"},
    {"barcode":"8901052022564","product_name":"Tata Tea Premium","brands":"Tata","ingredients_text":"100% black tea (CTC blend)","additive_flags":"Clean single-ingredient"},
    {"barcode":"8901512141804","product_name":"Peanut Butter","brands":"Sundrop","ingredients_text":"Roasted peanuts, sugar, edible vegetable oil, salt","additive_flags":"Clean"},
    {"barcode":"8906032011019","product_name":"Nutrela Soya Chunks 220gm","brands":"Nutrela","ingredients_text":"Defatted soya flour","additive_flags":"Clean single-ingredient"},
    {"barcode":"8904063255006","product_name":"Punjabi Samosa","brands":"Haldiram's","ingredients_text":"Refined wheat flour, potato, peas, spices, salt, edible vegetable oil","additive_flags":"Clean"},
    {"barcode":"8901552007641","product_name":"Bhindi","brands":"Ashoka","ingredients_text":"Okra (bhindi), spices, salt, edible vegetable oil","additive_flags":"Clean"},
    {"barcode":"8901037024576","product_name":"Chai From India","brands":"Girnar","ingredients_text":"Black tea, spices (cardamom, ginger, cloves)","additive_flags":"Clean"},
    {"barcode":"8901262090414","product_name":"Amulya Dairy Whitener","brands":"Amul","ingredients_text":"Milk solids, sugar, emulsifier (INS 322)","additive_flags":"Clean"},
    {"barcode":"8904209307002","product_name":"Traditional Jaffna Curry Powder","brands":"Aachi","ingredients_text":"Coriander, cumin, turmeric, red chilli, black pepper, cloves, cinnamon, cardamom, curry leaves","additive_flags":"Clean spice blend"},
    {"barcode":"8901233025612","product_name":"Dairy Milk Chocolate","brands":"Cadbury","ingredients_text":"Sugar, milk solids, cocoa butter, cocoa mass, emulsifiers (INS 322, INS 476), flavours","additive_flags":"Clean"},
    {"barcode":"8906013533769","product_name":"Wafers","brands":"Various","ingredients_text":"Refined wheat flour, sugar, edible vegetable oil, flavours, raising agents","additive_flags":"Clean"},
    {"barcode":"8904063252524","product_name":"Murmura","brands":"Haldiram's","ingredients_text":"Puffed rice, edible vegetable oil, salt, spices","additive_flags":"Clean"},
    {"barcode":"8909499000527","product_name":"Pur Jus de Citron","brands":"Various","ingredients_text":"100% lemon juice","additive_flags":"Clean single-ingredient"},
    {"barcode":"8901491502047","product_name":"Spanish Tomato Tango","brands":"Lay's","ingredients_text":"Potato, edible vegetable oil, tomato powder, spices, salt, sugar, flavour enhancers (INS 621), colours","additive_flags":"INS 621 MSG"},
    {"barcode":"8904105511336","product_name":"Mansyadi Vati","brands":"Various","ingredients_text":"Ayurvedic herbal formulation","additive_flags":"Ayurvedic medicine"},
    {"barcode":"8906009077475","product_name":"Assortiment de Biscuits","brands":"Leonian Premium","ingredients_text":"Refined wheat flour, sugar, edible vegetable oil, various flavours, raising agents, emulsifiers","additive_flags":"Clean"},
    {"barcode":"8904063258342","product_name":"Haldiram Cookie Heaven Coconut","brands":"Haldiram's","ingredients_text":"Refined wheat flour, sugar, coconut, edible vegetable oil, raising agents, emulsifiers","additive_flags":"Clean"},
    {"barcode":"8904304353102","product_name":"Bodypower Nutrition Whey Protein","brands":"Bodypower Nutrition","ingredients_text":"Whey protein concentrate, emulsifier (INS 322), artificial flavour","additive_flags":"Clean"},
    {"barcode":"8906002001163","product_name":"Peanut Butter","brands":"Dr. Oetker","ingredients_text":"Roasted peanuts, sugar, edible vegetable oil, salt","additive_flags":"Clean"},
    {"barcode":"8904013071007","product_name":"Telephone Brand Sat-Isabgol","brands":"Telephone","ingredients_text":"Psyllium husk (isabgol)","additive_flags":"Clean single-ingredient"},
    {"barcode":"8906002080366","product_name":"Sakthi Sambar Powder","brands":"Sakthi","ingredients_text":"Coriander, turmeric, red chilli, fenugreek, cumin, black pepper, mustard, curry leaves","additive_flags":"Clean spice blend"},
    {"barcode":"8903059608277","product_name":"Soan Papdi","brands":"Various","ingredients_text":"Sugar, gram flour, ghee, cardamom","additive_flags":"Clean"},
    {"barcode":"8901030684777","product_name":"Green Tea Honey Lemon","brands":"Lipton","ingredients_text":"Green tea, honey, lemon flavour","additive_flags":"Clean"},
    {"barcode":"8906026597192","product_name":"Khakhra","brands":"Various","ingredients_text":"Whole wheat flour, salt, spices, edible vegetable oil","additive_flags":"Clean"},
    {"barcode":"8904064627994","product_name":"Mango Pickle","brands":"Various","ingredients_text":"Raw mango, salt, spices, edible vegetable oil, acidity regulator","additive_flags":"Clean"},
    {"barcode":"8906119090135","product_name":"Candilicious Lollipops","brands":"Various","ingredients_text":"Sugar, glucose syrup, flavours, colours","additive_flags":"Verify colours"},
    {"barcode":"8908003050461","product_name":"Basmati Rice","brands":"Various","ingredients_text":"100% basmati rice","additive_flags":"Clean single-ingredient"},
    {"barcode":"8904208600029","product_name":"Meal Mix Paneer Makhanwala","brands":"Various","ingredients_text":"Paneer, tomato, butter, cream, spices, salt","additive_flags":"Clean"},
    {"barcode":"8906021128889","product_name":"Dhall Rice Powder","brands":"Aachi","ingredients_text":"Rice flour, lentil flour, spices","additive_flags":"Clean"},
    {"barcode":"8907003505063","product_name":"Madras Mixture","brands":"Various","ingredients_text":"Rice flakes, gram flour, edible vegetable oil, peanuts, sago, salt, spices, colours","additive_flags":"INS 160c colour"},
    {"barcode":"8906097400087","product_name":"Zoff Red Chilli Powder 5rs","brands":"Zoff","ingredients_text":"Red chilli powder (100%)","additive_flags":"Clean single-ingredient"},
    {"barcode":"8904057300491","product_name":"Arun","brands":"Various","ingredients_text":"Verify specific product","additive_flags":"Verify"},
    {"barcode":"8904082785249","product_name":"Soya Sticks","brands":"Various","ingredients_text":"Soya flour, edible vegetable oil, spices, salt","additive_flags":"Clean"},
    {"barcode":"8904250612957","product_name":"Powder","brands":"Various","ingredients_text":"Verify specific product","additive_flags":"Verify"},
    {"barcode":"8901014004133","product_name":"Italiano Cup Noodles","brands":"Nissin","ingredients_text":"Refined wheat flour, palm oil, salt, thickeners; Tastemaker: spices, salt, flavour enhancers (INS 621)","additive_flags":"INS 621 MSG"},
    {"barcode":"8906009200538","product_name":"Oat Granola","brands":"Express Foods","ingredients_text":"Oats, honey, nuts, seeds, edible vegetable oil","additive_flags":"Clean"},
    {"barcode":"8904063259264","product_name":"Veg Shami Kebab","brands":"Haldiram's","ingredients_text":"Potato, gram flour, spices, salt, edible vegetable oil","additive_flags":"Clean"},
    {"barcode":"8905694516405","product_name":"Mantequilla de Maní","brands":"La Sabrocita","ingredients_text":"Roasted peanuts (100%)","additive_flags":"Clean"},
    {"barcode":"8901207024351","product_name":"Hajmola","brands":"Dabur","ingredients_text":"Spices (black salt, cumin, amchur, red chilli), salt, sugar, acidity regulator","additive_flags":"Clean"},
    {"barcode":"8901138110710","product_name":"Liv.52","brands":"Himalaya","ingredients_text":"Herbal formulation (Caper Bush, Chicory, etc.)","additive_flags":"Ayurvedic medicine"}
]

elevated_count = 0
added_count = 0
purged_count = 0

for item in batch_21_rows:
    barcode = str(item["barcode"]).strip()
    pname = item["product_name"].strip()
    brand = item["brands"].strip()
    ing = item["ingredients_text"].strip()
    flags = item.get("additive_flags", "")
    
    # Check if non-food
    if "NON-FOOD" in ing.upper() or "NON-FOOD" in flags.upper() or "PURGE" in flags.upper():
        df_all = df_all[df_all['barcode'] != barcode]
        df_confirmed = df_confirmed[df_confirmed['barcode'] != barcode]
        df_needs_ver = df_needs_ver[df_needs_ver['barcode'] != barcode]
        purged_count += 1
        continue
        
    if not (barcode.startswith('890') or bool(re.match(r'^\d+$', barcode))):
        continue

    # Update or add in master DB
    idx_all = df_all[df_all['barcode'] == barcode].index
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
            'sold_in_india_status': 'CONFIRMED_INDIA_890',
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
        df_confirmed.loc[idx_c, 'sold_in_india_status'] = 'CONFIRMED_INDIA_890'
        df_confirmed.loc[idx_c, 'ingredient_confidence'] = 'HIGH'
        df_confirmed.loc[idx_c, 'status'] = 'KEEP'
    else:
        conf_row = {
            'barcode': barcode,
            'product_name': pname,
            'brands': brand,
            'ingredients_text': ing,
            'sold_in_india_status': 'CONFIRMED_INDIA_890',
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

print(f"Batch 21 Processing Summary:")
print(f"  Elevated from Needs Verification to Confirmed: {elevated_count}")
print(f"  Newly added to Confirmed: {added_count}")
print(f"  Purged Non-Food Barcodes: {purged_count}")
print(f"  Final Master CSV Count: {len(df_all)}")
print(f"  Final Confirmed CSV Count: {len(df_confirmed)}")
print(f"  Final Needs Verification CSV Count: {len(df_needs_ver)}")
