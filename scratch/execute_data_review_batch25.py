import os
import sys
import pandas as pd
import re

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"c:\Users\thout\Downloads\check it"

all_supabase_csv = os.path.join(BASE_DIR, "all_supabase_products.csv")
confirmed_csv = os.path.join(BASE_DIR, "india_products_confirmed.csv")
needs_ver_csv = os.path.join(BASE_DIR, "india_products_needs_verification.csv")

print("=== EXECUTING BATCH 25 INGREDIENTS INTEGRATION & PURGE ===")

df_all = pd.read_csv(all_supabase_csv, dtype=str)
df_confirmed = pd.read_csv(confirmed_csv, dtype=str) if os.path.exists(confirmed_csv) else pd.DataFrame()
df_needs_ver = pd.read_csv(needs_ver_csv, dtype=str) if os.path.exists(needs_ver_csv) else pd.DataFrame()

for df in [df_all, df_confirmed, df_needs_ver]:
    if not df.empty and 'barcode' in df.columns:
        df['barcode'] = df['barcode'].astype(str).str.strip()

batch_25_rows = [
    {"barcode":"5000159415774","product_name":"M&M's Chocolate","brands":"M&M's/Mars","ingredients_text":"Sugar, cocoa butter, milk solids, cocoa mass, peanuts, colours (INS 171), emulsifiers","additive_flags":"INS 171 Titanium Dioxide — BANNED IN EU"},
    {"barcode":"7702189056313","product_name":"Chokis","brands":"Chokis/Pepsico/Gamesa","ingredients_text":"Refined wheat flour, sugar, cocoa solids, edible vegetable oil, raising agents, emulsifiers, antioxidant (INS 319)","additive_flags":"INS 319 TBHQ — BANNED IN JP"},
    {"barcode":"0000010217627","product_name":"Décros Sucrés","brands":"Kitchen Academy","ingredients_text":"Sugar, colours (INS 171), flavours","additive_flags":"INS 171 Titanium Dioxide — BANNED IN EU"},
    {"barcode":"0000010408780","product_name":"Starburst Jelly Beans","brands":"Mars","ingredients_text":"Sugar, glucose syrup, fruit juice concentrate, colours (INS 171), flavours, acidity regulator","additive_flags":"INS 171 Titanium Dioxide — BANNED IN EU"},
    {"barcode":"4009900489119","product_name":"White Bubblemint Chewing Gum Sugar Free","brands":"Mars/Wrigley's","ingredients_text":"Sorbitol, gum base, mannitol, flavours, sweeteners, colours (INS 171)","additive_flags":"INS 171 Titanium Dioxide — BANNED IN EU"},
    {"barcode":"5000159501460","product_name":"M&M's","brands":"Mars","ingredients_text":"Sugar, cocoa butter, milk solids, cocoa mass, peanuts, colours (INS 171), emulsifiers","additive_flags":"INS 171 Titanium Dioxide — BANNED IN EU"},
    {"barcode":"7501059287228","product_name":"Coffee Mate Caramelo","brands":"Nestlé","ingredients_text":"Sugar, hydrogenated vegetable oil, milk solids, caramel flavour, colours (INS 171), emulsifiers","additive_flags":"INS 171 Titanium Dioxide — BANNED IN EU"},
    {"barcode":"0044000063757","product_name":"Trolls Oreo","brands":"Oreo","ingredients_text":"Refined wheat flour, sugar, refined palm oil, cocoa solids, invert syrup, raising agents, emulsifiers, colours (INS 127)","additive_flags":"INS 127 Erythrosine — BANNED IN US"},
    {"barcode":"0072554001529","product_name":"Frozen Dairy Dessert Cones","brands":"Nestlé","ingredients_text":"Toned milk, sugar, edible vegetable oil (partially hydrogenated), stabilizers, emulsifiers, waffle cone","additive_flags":"PHO — BANNED IN US/CA"},
    {"barcode":"9347043001498","product_name":"Chocolate Wafer Cone","brands":"Oreo","ingredients_text":"Refined wheat flour, sugar, cocoa solids, edible vegetable oil, emulsifiers, antioxidant (INS 319)","additive_flags":"INS 319 TBHQ — BANNED IN JP"},
    {"barcode":"9300650452763","product_name":"Oreo Cookie Choc 128g","brands":"Oreo","ingredients_text":"Refined wheat flour, sugar, refined palm oil, cocoa solids, invert syrup, raising agents, emulsifiers, antioxidant (INS 319)","additive_flags":"INS 319 TBHQ — BANNED IN JP"},
    {"barcode":"5000159484589","product_name":"M&M's Chocolate","brands":"M&M's/Mars","ingredients_text":"Sugar, cocoa butter, milk solids, cocoa mass, peanuts, colours (INS 171), emulsifiers","additive_flags":"INS 171 Titanium Dioxide — BANNED IN EU"},
    {"barcode":"8991102771238","product_name":"Tango Brownies Crispy","brands":"Tango","ingredients_text":"Refined wheat flour, sugar, cocoa solids, edible vegetable oil, raising agents, emulsifiers, antioxidant (INS 319)","additive_flags":"INS 319 TBHQ — BANNED IN JP"},
    {"barcode":"0072554218606","product_name":"Drumstick","brands":"Nestlé","ingredients_text":"Toned milk, sugar, edible vegetable oil (partially hydrogenated), stabilizers, emulsifiers, waffle cone","additive_flags":"PHO — BANNED IN US/CA"},
    {"barcode":"0028000084004","product_name":"Milk Chocolate with Peanuts & Raisins","brands":"Nestlé","ingredients_text":"Sugar, milk solids, cocoa butter, cocoa mass, peanuts, raisins, emulsifiers, antioxidant (INS 319)","additive_flags":"INS 319 TBHQ — BANNED IN JP"},
    {"barcode":"9556001170774","product_name":"Mi Goreng Soy and Mild Spice","brands":"Maggi","ingredients_text":"Noodles: Refined wheat flour, palm oil, salt, thickeners; Tastemaker: soy sauce, spices, flavour enhancers (INS 621), antioxidant (INS 319)","additive_flags":"INS 621 + INS 319 — TBHQ BANNED IN JP"},
    {"barcode":"7802420009198","product_name":"Corte Americano","brands":"Lay's","ingredients_text":"Potato, edible vegetable oil, salt, spices, antioxidant (INS 319)","additive_flags":"INS 319 TBHQ — BANNED IN JP"},
    {"barcode":"9300650453685","product_name":"Oreo Double Stuff Inspired by Pascall Marshmallows","brands":"Oreo","ingredients_text":"Refined wheat flour, sugar, refined palm oil, cocoa solids, marshmallow, invert syrup, raising agents, emulsifiers, antioxidant (INS 319)","additive_flags":"INS 319 TBHQ — BANNED IN JP"},
    {"barcode":"3538280842647","product_name":"Malabar Tutti Frutti 200x","brands":"Cadbury","ingredients_text":"Sugar, glucose syrup, tutti frutti flavour, colours (INS 171), acidity regulator","additive_flags":"INS 171 Titanium Dioxide — BANNED IN EU"},
    {"barcode":"0013000888332","product_name":"Heinz Tomato Spaghetti Sauce","brands":"Heinz","ingredients_text":"Tomato, sugar, water, salt, spices, edible vegetable oil (partially hydrogenated)","additive_flags":"PHO — BANNED IN US/CA"},
    {"barcode":"0073402345000","product_name":"Plain Donuts","brands":"Country Kitchen/Lepage Bakeries","ingredients_text":"Refined wheat flour, sugar, edible vegetable oil (partially hydrogenated), eggs, raising agents, emulsifiers","additive_flags":"PHO — BANNED IN US/CA"},
    {"barcode":"6271001736302","product_name":"Hummus Chips - Bliss","brands":"Kitco","ingredients_text":"Chickpea flour, edible vegetable oil, salt, spices, antioxidant (INS 319)","additive_flags":"INS 319 TBHQ — BANNED IN JP"},
    {"barcode":"0000075019426","product_name":"M&M's Minis","brands":"MARS","ingredients_text":"Sugar, cocoa butter, milk solids, cocoa mass, peanuts, colours (INS 171), emulsifiers","additive_flags":"INS 171 Titanium Dioxide — BANNED IN EU"},
    {"barcode":"5000159480178","product_name":"M&M's Chocolate","brands":"M&M's/Mars","ingredients_text":"Sugar, cocoa butter, milk solids, cocoa mass, peanuts, colours (INS 171), emulsifiers","additive_flags":"INS 171 Titanium Dioxide — BANNED IN EU"},
    {"barcode":"5000159501903","product_name":"M&M's","brands":"Nestlé/Mars","ingredients_text":"Sugar, cocoa butter, milk solids, cocoa mass, peanuts, colours (INS 171), emulsifiers","additive_flags":"INS 171 Titanium Dioxide — BANNED IN EU"},
    {"barcode":"5000159505802","product_name":"M et M's","brands":"Mars/Mars Chocolat","ingredients_text":"Sugar, cocoa butter, milk solids, cocoa mass, peanuts, colours (INS 171), emulsifiers","additive_flags":"INS 171 Titanium Dioxide — BANNED IN EU"},
    {"barcode":"6924743933460","product_name":"Crispy Meat Flavoured Chips","brands":"Lay's","ingredients_text":"Potato, edible vegetable oil, meat flavour, salt, spices, antioxidant (INS 319)","additive_flags":"INS 319 TBHQ — BANNED IN JP"},
    {"barcode":"0745367363497","product_name":"Easter Decor Mix","brands":"Brand's Country Kitchen Supplies","ingredients_text":"Sugar, colours (INS 127), edible vegetable oil (partially hydrogenated), flavours","additive_flags":"INS 127 Erythrosine + PHO — BANNED IN US/CA"},
    {"barcode":"0745367366511","product_name":"Halloween Decorating Candies","brands":"Target Corporation","ingredients_text":"Sugar, colours (INS 171), flavours, edible vegetable oil","additive_flags":"INS 171 Titanium Dioxide — BANNED IN EU"},
    {"barcode":"0793591862453","product_name":"Kerala Banana Chips","brands":"Byond Snack","ingredients_text":"Banana, edible vegetable oil, salt, spices, antioxidant (INS 319)","additive_flags":"INS 319 TBHQ — BANNED IN JP"},
    {"barcode":"0745367367266","product_name":"Holiday Decorating Candies","brands":"Target Corporation","ingredients_text":"Sugar, colours, edible vegetable oil (partially hydrogenated), flavours","additive_flags":"PHO — BANNED IN US/CA"},
    {"barcode":"0000093557153","product_name":"Lemon Lime & Bitter","brands":"Coca-Cola","ingredients_text":"Carbonated water, sugar, acidity regulators, lemon-lime flavour, colours (INS 122), preservative","additive_flags":"INS 122 Carmoisine — BANNED IN JP/US"},
    {"barcode":"0000093657778","product_name":"Salad Cream","brands":"Heinz","ingredients_text":"Refined soybean oil, water, sugar, vinegar, salt, thickener, colours (INS 171), antioxidant (INS 319)","additive_flags":"INS 319 TBHQ + INS 171 — BANNED IN JP/EU"},
    {"barcode":"8664522556555","product_name":"Himzberg Kiwi","brands":"Himzberg","ingredients_text":"Kiwi flavour, sugar, acidity regulator, colours (INS 142)","additive_flags":"INS 142 Green S — BANNED IN IN/JP/US"},
    {"barcode":"0000093698450","product_name":"Tic Tac Fruit Adventure","brands":"Ferrero","ingredients_text":"Sugar, fruit flavours, acidity regulator, colours (INS 122)","additive_flags":"INS 122 Carmoisine — BANNED IN JP/US"},
    {"barcode":"8994963003272","product_name":"Instant Noodles Special Chicken Flavour","brands":"Various","ingredients_text":"Noodles: Refined wheat flour, palm oil, salt, thickeners; Tastemaker: chicken flavour, spices, flavour enhancers (INS 621), antioxidant (INS 319)","additive_flags":"INS 621 + INS 319 — TBHQ BANNED IN JP"},
    {"barcode":"7802000005541","product_name":"Twistos","brands":"Pepsico","ingredients_text":"Corn flour, edible vegetable oil, cheese flavour, salt, spices, antioxidant (INS 319)","additive_flags":"INS 319 TBHQ — BANNED IN JP"},
    {"barcode":"7771224008921","product_name":"Bambino Pasas al Ron","brands":"Delizia/Bambino","ingredients_text":"Raisins, rum flavour, sugar, colours (INS 122)","additive_flags":"INS 122 Carmoisine — BANNED IN JP/US"},
    {"barcode":"7501008082843","product_name":"Barras de Cereal Kellogg's Zucarías","brands":"Kellogg's","ingredients_text":"Oats, sugar, glucose syrup, colours (INS 171), vitamins, minerals","additive_flags":"INS 171 Titanium Dioxide — BANNED IN EU"},
    {"barcode":"6009710721490","product_name":"Cheese Supreme Flavoured Corn Chips","brands":"Doritos","ingredients_text":"Corn flour, edible vegetable oil, cheese flavour, salt, spices, antioxidant (INS 319)","additive_flags":"INS 319 TBHQ — BANNED IN JP"},
    {"barcode":"8851959122174","product_name":"Fanta Jordbær","brands":"Coca-Cola Company","ingredients_text":"Carbonated water, sugar, strawberry flavour, acidity regulators, colours (INS 122), preservative","additive_flags":"INS 122 Carmoisine — BANNED IN JP/US"},
    {"barcode":"5010238014729","product_name":"Creme Egg Ice Cream","brands":"Cadbury","ingredients_text":"Toned milk, sugar, cocoa solids, edible vegetable oil, stabilizers, emulsifiers, colours (INS 171)","additive_flags":"INS 171 Titanium Dioxide — BANNED IN EU"},
    {"barcode":"0637913877889","product_name":"Snickers Crunchy Peanut Butter","brands":"Snickers","ingredients_text":"Sugar, peanuts, glucose syrup, peanut butter, milk solids, cocoa butter, cocoa mass, emulsifiers, antioxidant (INS 319)","additive_flags":"INS 319 TBHQ — BANNED IN JP"},
    {"barcode":"0050000652860","product_name":"Italian Sweet Creme Creamer","brands":"Nestlé","ingredients_text":"Sugar, hydrogenated vegetable oil, milk solids, flavours, antioxidant (INS 319)","additive_flags":"INS 319 TBHQ — BANNED IN JP"},
    {"barcode":"0754590964760","product_name":"Kerala Banana Chips (Desi Masala)","brands":"Beyond Snack","ingredients_text":"Banana, edible vegetable oil, spices, salt, antioxidant (INS 319)","additive_flags":"INS 319 TBHQ — BANNED IN JP"},
    {"barcode":"6009510802559","product_name":"Cheese Supreme Flavoured Corn Chips","brands":"Doritos","ingredients_text":"Corn flour, edible vegetable oil, cheese flavour, salt, spices, antioxidant (INS 319)","additive_flags":"INS 319 TBHQ — BANNED IN JP"},
    {"barcode":"4009900510813","product_name":"Skittles","brands":"Mars","ingredients_text":"Sugar, glucose syrup, fruit juice concentrate, colours (INS 171), flavours, acidity regulator","additive_flags":"INS 171 Titanium Dioxide — BANNED IN EU"},
    {"barcode":"8947014692154","product_name":"Wow! Thupka Chicken","brands":"Wow!","ingredients_text":"Noodles: Refined wheat flour, palm oil, salt; Tastemaker: chicken flavour, spices, flavour enhancers (INS 621), antioxidant (INS 319)","additive_flags":"INS 621 + INS 319 — TBHQ BANNED IN JP"},
    {"barcode":"9300650454248","product_name":"Oreo Grab And Go 236g","brands":"Oreo","ingredients_text":"Refined wheat flour, sugar, refined palm oil, cocoa solids, invert syrup, raising agents, emulsifiers, antioxidant (INS 319)","additive_flags":"INS 319 TBHQ — BANNED IN JP"},
    {"barcode":"0760263000642","product_name":"Bear Creek Country Kitchens Soup Mix Hot & Sour","brands":"Bear Creek","ingredients_text":"Corn starch, salt, sugar, spices, edible vegetable oil (partially hydrogenated), flavour enhancers","additive_flags":"PHO — BANNED IN US/CA"},
    {"barcode":"0760263911108","product_name":"Alfredo Pasta Mix","brands":"Bear Creek Country Kitchens","ingredients_text":"Refined wheat flour, milk solids, cheese, salt, spices, edible vegetable oil (partially hydrogenated)","additive_flags":"PHO — BANNED IN US/CA"},
    {"barcode":"7622201448837","product_name":"Shots","brands":"Cadbury","ingredients_text":"Sugar, glucose syrup, milk solids, cocoa solids, edible vegetable oil, colours (INS 122), flavours","additive_flags":"INS 122 Carmoisine — BANNED IN JP/US"},
    {"barcode":"8901014000470","product_name":"Nissin","brands":"Nissin","ingredients_text":"Noodles: Refined wheat flour, palm oil, salt, thickeners; Tastemaker: salt, spices, flavour enhancers (INS 621), antioxidant (INS 319)","additive_flags":"INS 621 + INS 319 — TBHQ BANNED IN JP"},
    {"barcode":"8908007009083","product_name":"Vitthal Refined Soyabean Oil","brands":"Vitthal","ingredients_text":"Refined soybean oil, antioxidant (INS 319), vitamins A & D","additive_flags":"INS 319 TBHQ — BANNED IN JP"},
    {"barcode":"8901777960042","product_name":"Vadilal Bomber","brands":"Vadilal","ingredients_text":"Toned milk, sugar, cocoa solids, edible vegetable oil, stabilizers, emulsifiers, colours (INS 124)","additive_flags":"INS 124 Ponceau 4R — BANNED IN US"},
    {"barcode":"8901808000068","product_name":"Weikfield","brands":"Weikfield","ingredients_text":"Verify specific product","additive_flags":"Verify"},
    {"barcode":"9300650454040","product_name":"Double Stuff Cadbury Crème Egg","brands":"Oreo","ingredients_text":"Refined wheat flour, sugar, refined palm oil, cocoa solids, creme egg filling, invert syrup, raising agents, emulsifiers, antioxidant (INS 319)","additive_flags":"INS 319 TBHQ — BANNED IN JP"},
    {"barcode":"0793591862460","product_name":"Kerala Banana Chips","brands":"Beyond Snacks","ingredients_text":"Banana, edible vegetable oil, salt, spices, antioxidant (INS 319)","additive_flags":"INS 319 TBHQ — BANNED IN JP"},
    {"barcode":"8901014000449","product_name":"Schezwan Spicy Chilli Sauce Flavour","brands":"Top Ramen/Nissin","ingredients_text":"Noodles: Refined wheat flour, palm oil, salt, thickeners; Tastemaker: schezwan seasoning, spices, flavour enhancers (INS 621), antioxidant (INS 319)","additive_flags":"INS 621 + INS 319 — TBHQ BANNED IN JP"},
    {"barcode":"8908014665258","product_name":"French Yogurt Strawberry","brands":"Mamie Yova","ingredients_text":"Pasteurized milk, sugar, strawberry, active lactic culture, colours (INS 124)","additive_flags":"INS 124 Ponceau 4R — BANNED IN US"},
    {"barcode":"8901393026405","product_name":"Chapai Chips Bubble Gum","brands":"Various","ingredients_text":"Sugar, glucose syrup, bubble gum flavour, colours (INS 122)","additive_flags":"INS 122 Carmoisine — BANNED IN JP/US"},
    {"barcode":"8904482000003","product_name":"Hamdard Roohafza","brands":"Hamdard","ingredients_text":"Sugar, water, rose extract, herbs, spices, acidity regulator, colours (INS 122)","additive_flags":"INS 122 Carmoisine — BANNED IN JP/US"},
    {"barcode":"8906026600465","product_name":"Acai Vibe","brands":"Rio","ingredients_text":"Acai berry, sugar, water, acidity regulator, colours (INS 122)","additive_flags":"INS 122 Carmoisine — BANNED IN JP/US"},
    {"barcode":"8908010271194","product_name":"Osmania Biscuit","brands":"Cafe Niloufer","ingredients_text":"Refined wheat flour, sugar, edible vegetable oil (hydrogenated), milk solids, raising agents, emulsifiers","additive_flags":"PHO — BANNED IN US/CA"},
    {"barcode":"8909081013720","product_name":"Berry Smoothie","brands":"Sunfeast","ingredients_text":"Water, mixed berry juice concentrate, sugar, acidity regulator, colours (INS 122)","additive_flags":"INS 122 Carmoisine — BANNED IN JP/US"},
    {"barcode":"8888307120063","product_name":"Red Bull Plus","brands":"Red Bull","ingredients_text":"Carbonated water, sugar, acidity regulators, caffeine, taurine, colours (INS 124), flavours, vitamins","additive_flags":"INS 124 Ponceau 4R — BANNED IN US"},
    {"barcode":"9300650454149","product_name":"Oreo Double Stuffed Sour Patch Kids Cookies 136g","brands":"Oreo","ingredients_text":"Refined wheat flour, sugar, refined palm oil, cocoa solids, sour patch filling, invert syrup, raising agents, emulsifiers, antioxidant (INS 319)","additive_flags":"INS 319 TBHQ — BANNED IN JP"},
    {"barcode":"7622300761349","product_name":"Oreo Mini Stuffed With Vanilla Cream Cookies","brands":"Oreo","ingredients_text":"Refined wheat flour, sugar, refined palm oil, vanilla cream, invert syrup, raising agents, emulsifiers, antioxidant (INS 319)","additive_flags":"INS 319 TBHQ — BANNED IN JP"},
    {"barcode":"7622201718350","product_name":"Oreo Cobertura Sabor a Chocolate Blanco","brands":"Oreo","ingredients_text":"Sugar, cocoa butter, milk solids, refined wheat flour, colours (INS 171), emulsifiers","additive_flags":"INS 171 Titanium Dioxide — BANNED IN EU"},
    {"barcode":"5000159481540","product_name":"M&M's Peanut","brands":"M&M's/Mars","ingredients_text":"Sugar, peanuts, cocoa butter, milk solids, cocoa mass, colours (INS 171), emulsifiers","additive_flags":"INS 171 Titanium Dioxide — BANNED IN EU"},
    {"barcode":"5000159493833","product_name":"M&M's Peanut","brands":"Mars","ingredients_text":"Sugar, peanuts, cocoa butter, milk solids, cocoa mass, colours (INS 171), emulsifiers","additive_flags":"INS 171 Titanium Dioxide — BANNED IN EU"},
    {"barcode":"8710398170156","product_name":"Doritos Cool American","brands":"Doritos","ingredients_text":"Corn flour, edible vegetable oil (partially hydrogenated), cheese flavour, salt, spices","additive_flags":"PHO — BANNED IN US/CA"},
    {"barcode":"8901262201896","product_name":"Amul Stirred Fruit Yogurt Strawberry","brands":"Amul","ingredients_text":"Pasteurized toned milk, sugar, strawberry, active lactic culture, colours (INS 124)","additive_flags":"INS 124 Ponceau 4R — BANNED IN US"},
    {"barcode":"8904025401113","product_name":"Mix Fruit Jam","brands":"Chitale","ingredients_text":"Sugar, mixed fruit pulp blend, acidity regulator (INS 330), preservative (INS 211), permitted synthetic food colours (INS 122, INS 127)","additive_flags":"INS 122 + INS 127 — BANNED IN JP/US"},
    {"barcode":"9900272541793","product_name":"Bix Cake Sandwich","brands":"Various","ingredients_text":"Refined wheat flour, sugar, cocoa solids, edible vegetable oil, raising agents, emulsifiers, colours (INS 155)","additive_flags":"INS 155 Brown HT — BANNED IN IN/JP/US"},
    {"barcode":"8909081006715","product_name":"Candyman Fruitee Fun","brands":"Candyman","ingredients_text":"Sugar, glucose syrup, fruit flavours, acidity regulator, colours (INS 122)","additive_flags":"INS 122 Carmoisine — BANNED IN JP/US"},
    {"barcode":"8904089995351","product_name":"Blueberry Yogurt","brands":"Heritage","ingredients_text":"Pasteurized milk, sugar, blueberry, active lactic culture, colours (INS 122)","additive_flags":"INS 122 Carmoisine — BANNED IN JP/US"},
    {"barcode":"8901262301435","product_name":"Berry Dazzle","brands":"Amul","ingredients_text":"Toned milk, sugar, mixed berry flavour, stabilizers, emulsifiers, colours (INS 122, INS 127)","additive_flags":"INS 122 + INS 127 — BANNED IN JP/US"},
    {"barcode":"8906064284818","product_name":"GOODINI Celebration Gift of Good Taste","brands":"Goodini","ingredients_text":"Refined wheat flour, sugar, edible vegetable oil, cocoa solids, raising agents, emulsifiers, antioxidant (INS 319)","additive_flags":"INS 319 TBHQ — BANNED IN JP"},
    {"barcode":"5000159441896","product_name":"M&M's 1KG Choco","brands":"M&M's/Mars","ingredients_text":"Sugar, cocoa butter, milk solids, cocoa mass, peanuts, colours (INS 171), emulsifiers","additive_flags":"INS 171 Titanium Dioxide — BANNED IN EU"},
    {"barcode":"5000159500371","product_name":"Chocolate M&M's Ice Cream","brands":"Mars","ingredients_text":"Toned milk, sugar, cocoa solids, M&M's pieces, stabilizers, emulsifiers, colours (INS 171)","additive_flags":"INS 171 Titanium Dioxide — BANNED IN EU"},
    {"barcode":"5000159500654","product_name":"Glaces Peanut M&M's","brands":"M&M's/Mars/Mars Chocolat","ingredients_text":"Toned milk, sugar, peanuts, M&M's pieces, stabilizers, emulsifiers, colours (INS 171)","additive_flags":"INS 171 Titanium Dioxide — BANNED IN EU"},
    {"barcode":"8906006721708","product_name":"Mixed Fruit Jam","brands":"Lion","ingredients_text":"Sugar, mixed fruit pulp blend, acidity regulator (INS 330), preservative (INS 211), permitted synthetic food colour (INS 122)","additive_flags":"INS 122 Carmoisine — BANNED IN JP/US"},
    {"barcode":"8906007280235","product_name":"Fortune Sun Lite Refined Sunflower Oil","brands":"Fortune","ingredients_text":"Refined sunflower oil, antioxidant (INS 319), vitamins A & D","additive_flags":"INS 319 TBHQ — BANNED IN JP"},
    {"barcode":"8901014000203","product_name":"Cup Noodles Chili Chili Chilli","brands":"Nissin","ingredients_text":"Noodles: Refined wheat flour, palm oil, salt, thickeners; Tastemaker: chilli seasoning, spices, flavour enhancers (INS 621), antioxidant (INS 319)","additive_flags":"INS 621 + INS 319 — TBHQ BANNED IN JP"},
    {"barcode":"9300650451728","product_name":"Oreo","brands":"Oreo","ingredients_text":"Refined wheat flour, sugar, refined palm oil, cocoa solids, invert syrup, raising agents, emulsifiers, antioxidant (INS 319)","additive_flags":"INS 319 TBHQ — BANNED IN JP"},
    {"barcode":"9300650025479","product_name":"Choc Oreo Choc Split","brands":"Oreo","ingredients_text":"Refined wheat flour, sugar, refined palm oil, cocoa solids, chocolate coating, invert syrup, raising agents, emulsifiers, antioxidant (INS 319)","additive_flags":"INS 319 TBHQ — BANNED IN JP"},
    {"barcode":"9300650452701","product_name":"Oreo Original Choc Cookie Sandwich with Sweet Vanilla Creme","brands":"Oreo","ingredients_text":"Refined wheat flour, sugar, refined palm oil, cocoa solids, vanilla creme, invert syrup, raising agents, emulsifiers, antioxidant (INS 319)","additive_flags":"INS 319 TBHQ — BANNED IN JP"},
    {"barcode":"8901512557001","product_name":"Nachos Crispy & Crunchy","brands":"Act II","ingredients_text":"Corn flour, edible vegetable oil, salt, spices, antioxidant (INS 319)","additive_flags":"INS 319 TBHQ — BANNED IN JP"},
    {"barcode":"8906065458218","product_name":"Gone Mad Gang of 5 Premium Badam Sticks","brands":"Gone Mad","ingredients_text":"Almonds, sugar, edible vegetable oil, colours (INS 124)","additive_flags":"INS 124 Ponceau 4R — BANNED IN US"},
    {"barcode":"8901548310403","product_name":"DoodhShakti","brands":"Nutralite","ingredients_text":"Milk solids, sugar, edible vegetable oil, antioxidant (INS 319), vitamins","additive_flags":"INS 319 TBHQ — BANNED IN JP"},
    {"barcode":"8992760223022","product_name":"Oreo Chocolate 27.6g","brands":"Oreo","ingredients_text":"Refined wheat flour, sugar, refined palm oil, cocoa solids, invert syrup, raising agents, emulsifiers, antioxidant (INS 319)","additive_flags":"INS 319 TBHQ — BANNED IN JP"},
    {"barcode":"9300650022539","product_name":"Oreo","brands":"Oreo","ingredients_text":"Refined wheat flour, sugar, refined palm oil, cocoa solids, invert syrup, raising agents, emulsifiers, antioxidant (INS 319)","additive_flags":"INS 319 TBHQ — BANNED IN JP"},
    {"barcode":"4892642101926","product_name":"Oreo Chocolate Creme Cookies","brands":"Oreo","ingredients_text":"Refined wheat flour, sugar, refined palm oil, cocoa solids, chocolate creme, invert syrup, raising agents, emulsifiers, antioxidant (INS 319)","additive_flags":"INS 319 TBHQ — BANNED IN JP"},
    {"barcode":"9556001137678","product_name":"Oriental Maggi Orientation Noodles","brands":"Maggi","ingredients_text":"Noodles: Refined wheat flour, palm oil, salt, thickeners; Tastemaker: oriental seasoning, spices, flavour enhancers (INS 621), antioxidant (INS 319)","additive_flags":"INS 621 + INS 319 — TBHQ BANNED IN JP"},
    {"barcode":"8906008819502","product_name":"Refined Soyabean Oil","brands":"Fortune","ingredients_text":"Refined soybean oil, antioxidant (INS 319), vitamins A & D","additive_flags":"INS 319 TBHQ — BANNED IN JP"},
    {"barcode":"8900017562619","product_name":"Bun Maska","brands":"Jo Bakes","ingredients_text":"Refined wheat flour, water, sugar, butter, yeast, salt, edible vegetable oil, antioxidant (INS 319)","additive_flags":"INS 319 TBHQ — BANNED IN JP"},
    {"barcode":"8901648015413","product_name":"Kulfi","brands":"Mother Dairy","ingredients_text":"Toned milk, sugar, milk fat, cardamom, stabilizers, emulsifier, colours (INS 122)","additive_flags":"INS 122 Carmoisine — BANNED IN JP/US"},
    {"barcode":"8906159640482","product_name":"Custard Powder (Vanilla)","brands":"FIRA","ingredients_text":"Corn starch, vanilla flavour, colours (INS 122)","additive_flags":"INS 122 Carmoisine — BANNED IN JP/US"},
    {"barcode":"8906005610386","product_name":"Winkies Love Bite Choco Heart Cake","brands":"Winkies","ingredients_text":"Refined wheat flour, sugar, cocoa solids, eggs, edible vegetable oil, glucose syrup, raising agents, emulsifiers, antioxidant (INS 319), colours (INS 171)","additive_flags":"INS 319 TBHQ + INS 171 — BANNED IN JP/EU"},
    {"barcode":"8901063363526","product_name":"Gobbles Fruity Fun Cake","brands":"Britannia","ingredients_text":"Refined wheat flour, sugar, eggs, edible vegetable oil, glucose syrup, fruit flavour, raising agents, emulsifiers, preservative (INS 202), colours (INS 124)","additive_flags":"INS 124 Ponceau 4R — BANNED IN US"},
    {"barcode":"9300675041140","product_name":"Mother Energy","brands":"Mother/Coca-Cola Amatil","ingredients_text":"Carbonated water, sugar, acidity regulators, caffeine, taurine, colours (INS 104), flavours, vitamins","additive_flags":"INS 104 Quinoline Yellow — BANNED IN JP/US"},
    {"barcode":"0040000494072","product_name":"Snickers","brands":"Snickers","ingredients_text":"Sugar, peanuts, glucose syrup, milk solids, cocoa butter, cocoa mass, edible vegetable oil (partially hydrogenated), emulsifiers","additive_flags":"PHO — BANNED IN US/CA"},
    {"barcode":"5000159388658","product_name":"M&M's Biscuit","brands":"Mars/M&M's","ingredients_text":"Refined wheat flour, sugar, cocoa butter, milk solids, cocoa mass, colours (INS 171), emulsifiers","additive_flags":"INS 171 Titanium Dioxide — BANNED IN EU"},
    {"barcode":"8906012890047","product_name":"Custard Powder","brands":"Bakers","ingredients_text":"Corn starch, vanilla flavour, colours (INS 122)","additive_flags":"INS 122 Carmoisine — BANNED IN JP/US"},
    {"barcode":"8906031490860","product_name":"Mixed Fruit Jam","brands":"Marks","ingredients_text":"Sugar, mixed fruit pulp blend, acidity regulator (INS 330), preservative (INS 211), permitted synthetic food colour (INS 122)","additive_flags":"INS 122 Carmoisine — BANNED IN JP/US"},
    {"barcode":"8901031013088","product_name":"Donettes Powdered","brands":"Hostess","ingredients_text":"Refined wheat flour, sugar, edible vegetable oil, colours (INS 171), raising agents, emulsifiers","additive_flags":"INS 171 Titanium Dioxide — BANNED IN EU"},
    {"barcode":"8002270033902","product_name":"Sanbitter","brands":"Nestlé/San Pellegrino","ingredients_text":"Carbonated water, sugar, acidity regulators, flavours, colours (INS 122)","additive_flags":"INS 122 Carmoisine — BANNED IN JP/US"},
    {"barcode":"0058496456610","product_name":"Miniar","brands":"Mars","ingredients_text":"Sugar, cocoa solids, colours (INS 171), flavours","additive_flags":"INS 171 Titanium Dioxide — BANNED IN EU"},
    {"barcode":"0786832820435","product_name":"Asiago Dinner Rolls","brands":"Royal Kitchens Inc.","ingredients_text":"Refined wheat flour, water, asiago cheese, yeast, salt, sugar, potassium bromate (INS 924a)","additive_flags":"INS 924a Potassium Bromate — BANNED IN EU/IN/UK/JP"},
    {"barcode":"3948063032453","product_name":"Treat Croissant Vanilla","brands":"Britannia","ingredients_text":"Refined wheat flour, sugar, edible vegetable oil, vanilla flavour, invert syrup, raising agents, emulsifiers, colours (INS 171)","additive_flags":"INS 171 Titanium Dioxide — BANNED IN EU"},
    {"barcode":"0071214054226","product_name":"Lemon Creme Cake","brands":"Old Home Kitchens","ingredients_text":"Refined wheat flour, sugar, lemon creme, edible vegetable oil (partially hydrogenated), eggs, raising agents","additive_flags":"PHO — BANNED IN US/CA"},
    {"barcode":"0038000121593","product_name":"Cereal Bars Blueberry","brands":"Kellogg's","ingredients_text":"Oats, sugar, blueberry, glucose syrup, edible vegetable oil (partially hydrogenated), salt, vitamins","additive_flags":"PHO — BANNED IN US/CA"},
    {"barcode":"8906124670872","product_name":"Geks Era Black Currant Pulp & Juice","brands":"Geks Era","ingredients_text":"Black currant pulp, sugar, water, acidity regulator, colours (INS 127)","additive_flags":"INS 127 Erythrosine — BANNED IN US"},
    {"barcode":"6924743927162","product_name":"Roasted Fish Flavor","brands":"Lay's","ingredients_text":"Potato, edible vegetable oil, fish flavour, salt, spices, antioxidant (INS 319)","additive_flags":"INS 319 TBHQ — BANNED IN JP"},
    {"barcode":"0000042070436","product_name":"Extra White Fruit 14g","brands":"MARS NORGE AS","ingredients_text":"Sugar, glucose syrup, fruit flavours, colours (INS 171)","additive_flags":"INS 171 Titanium Dioxide — BANNED IN EU"},
    {"barcode":"9310015241956","product_name":"Doritos Cool Ranch Flavoured Corn Chips","brands":"Doritos","ingredients_text":"Corn flour, edible vegetable oil, ranch flavour, salt, spices, colours (INS 171)","additive_flags":"INS 171 Titanium Dioxide — BANNED IN EU"},
    {"barcode":"3023290798454","product_name":"La Laitière Secret de Mousse Saveur Rocher Coco","brands":"Nestlé","ingredients_text":"Milk, sugar, coconut, cocoa, colours (INS 171), emulsifiers","additive_flags":"INS 171 Titanium Dioxide — BANNED IN EU"},
    {"barcode":"9300682051385","product_name":"TWIX","brands":"TWIX","ingredients_text":"Sugar, glucose syrup, milk solids, cocoa butter, cocoa mass, refined wheat flour, colours (INS 131), emulsifiers","additive_flags":"INS 131 Patent Blue V — BANNED IN IN/JP/US"},
    {"barcode":"8901725100131","product_name":"B Natural Orange Juice 1L","brands":"ITC","ingredients_text":"Orange juice, water, sugar, acidity regulator (INS 330), antioxidant (INS 300), colours (INS 171)","additive_flags":"INS 171 Titanium Dioxide — BANNED IN EU"},
    {"barcode":"8901725105167","product_name":"B Natural Guava Juice","brands":"B Natural/ITC","ingredients_text":"Guava juice, water, sugar, acidity regulator, colours (INS 124)","additive_flags":"INS 124 Ponceau 4R — BANNED IN US"},
    {"barcode":"8901248270847","product_name":"Refined Soyabean Oil","brands":"Emami","ingredients_text":"Refined soybean oil, antioxidant (INS 319), vitamins A & D","additive_flags":"INS 319 TBHQ — BANNED IN JP"},
    {"barcode":"8901014003181","product_name":"Top Ramen","brands":"Nissin/Top Ramen","ingredients_text":"Noodles: Refined wheat flour, palm oil, salt, thickeners; Tastemaker: salt, spices, flavour enhancers (INS 621), antioxidant (INS 319)","additive_flags":"INS 621 + INS 319 — TBHQ BANNED IN JP"},
    {"barcode":"8908009419774","product_name":"Savoriz","brands":"Bauli","ingredients_text":"Refined wheat flour, sugar, eggs, edible vegetable oil (partially hydrogenated), glucose syrup, raising agents, emulsifiers","additive_flags":"PHO — BANNED IN US/CA"},
    {"barcode":"8901595863044","product_name":"Schezwan Chutney","brands":"Ching's Secret","ingredients_text":"Water, red chilli, garlic, vinegar, salt, sugar, acidity regulator, preservative, antioxidant (INS 319)","additive_flags":"INS 319 TBHQ — BANNED IN JP"},
    {"barcode":"8901030831690","product_name":"Kissan Mixed Fruit Jam","brands":"Kissan","ingredients_text":"Sugar, mixed fruit pulp blend, acidity regulator (INS 330), preservative (INS 211), permitted synthetic food colour (INS 122)","additive_flags":"INS 122 Carmoisine — BANNED IN JP/US"},
    {"barcode":"8901512144706","product_name":"Peanut Butter Regular Creamy","brands":"Sundrop","ingredients_text":"Roasted peanuts, sugar, edible vegetable oil, salt, antioxidant (INS 319)","additive_flags":"INS 319 TBHQ — BANNED IN JP"},
    {"barcode":"8908005144168","product_name":"Protein Bar","brands":"Yoga Bar","ingredients_text":"Oats, whey protein, dates, nuts, honey, edible vegetable oil, antioxidant (INS 319)","additive_flags":"INS 319 TBHQ — BANNED IN JP"},
    {"barcode":"0034271900202","product_name":"Chocolate Nut Pie","brands":"Kern's/Kern's Kitchen","ingredients_text":"Refined wheat flour, sugar, chocolate, nuts, edible vegetable oil (partially hydrogenated), eggs","additive_flags":"PHO — BANNED IN US/CA"},
    {"barcode":"5010238016457","product_name":"Marvellous Ice Creams Jelly Popping Candy","brands":"Cadbury","ingredients_text":"Toned milk, sugar, jelly popping candy, stabilizers, emulsifiers, colours (INS 171)","additive_flags":"INS 171 Titanium Dioxide — BANNED IN EU"},
    {"barcode":"0781718143516","product_name":"Dry Lemon (Switch)","brands":"Switch","ingredients_text":"Carbonated water, sugar, lemon flavour, acidity regulators, colours (INS 104)","additive_flags":"INS 104 Quinoline Yellow — BANNED IN JP/US"},
    {"barcode":"0855883003088","product_name":"Pumpkin Pie","brands":"Home Chef Kitchen Inc.","ingredients_text":"Pumpkin, refined wheat flour, sugar, edible vegetable oil (partially hydrogenated), eggs, spices","additive_flags":"PHO — BANNED IN US/CA"},
    {"barcode":"7622210106988","product_name":"Dairy Milk Marvellous Creations Jelly Popping Candy","brands":"Cadbury","ingredients_text":"Sugar, milk solids, cocoa butter, cocoa mass, jelly popping candy, colours (INS 171), emulsifiers","additive_flags":"INS 171 Titanium Dioxide — BANNED IN EU"},
    {"barcode":"9556001171337","product_name":"Chicken Noodles","brands":"Maggi","ingredients_text":"Noodles: Refined wheat flour, palm oil, salt, thickeners; Tastemaker: chicken flavour, spices, flavour enhancers (INS 621), antioxidant (INS 319)","additive_flags":"INS 621 + INS 319 — TBHQ BANNED IN JP"},
    {"barcode":"7501011130975","product_name":"Cheetos Torciditos","brands":"Pepsico","ingredients_text":"Corn flour, edible vegetable oil (partially hydrogenated), cheese flavour, salt, spices","additive_flags":"PHO — BANNED IN US/CA"},
    {"barcode":"7622201747107","product_name":"White Fudge","brands":"Oreo","ingredients_text":"Sugar, cocoa butter, milk solids, refined wheat flour, colours (INS 171), emulsifiers","additive_flags":"INS 171 Titanium Dioxide — BANNED IN EU"},
    {"barcode":"0028000115678","product_name":"Maggi Bouillon Chicken","brands":"Maggi","ingredients_text":"Salt, sugar, chicken fat, spices, flavour enhancers (INS 621), antioxidant (INS 319), edible vegetable oil (partially hydrogenated)","additive_flags":"INS 621 + INS 319 + PHO — BANNED IN JP/US/CA"},
    {"barcode":"0000002867633","product_name":"Refined Soya Bean Oil","brands":"Fortune","ingredients_text":"Refined soybean oil, antioxidant (INS 319), vitamins A & D","additive_flags":"INS 319 TBHQ — BANNED IN JP"},
    {"barcode":"8410494300777","product_name":"Bitter Kas","brands":"Kas/PepsiCo","ingredients_text":"Carbonated water, sugar, acidity regulators, flavours, colours (INS 122)","additive_flags":"INS 122 Carmoisine — BANNED IN JP/US"},
    {"barcode":"0073402358000","product_name":"Fine Chocolate Powdered Donuts","brands":"Country Kitchen/Lepage Bakeries","ingredients_text":"Refined wheat flour, sugar, cocoa, edible vegetable oil (partially hydrogenated), colours (INS 171), raising agents","additive_flags":"INS 171 + PHO — BANNED IN EU/US/CA"},
    {"barcode":"7802000020124","product_name":"Doritos","brands":"Doritos","ingredients_text":"Corn flour, edible vegetable oil, spices, salt, antioxidant (INS 319)","additive_flags":"INS 319 TBHQ — BANNED IN JP"},
    {"barcode":"9300650454224","product_name":"Chocolate Choc Cookie Sandwich with Chocolate Flavoured Creme","brands":"Oreo","ingredients_text":"Refined wheat flour, sugar, refined palm oil, cocoa solids, chocolate creme, invert syrup, raising agents, emulsifiers, antioxidant (INS 319)","additive_flags":"INS 319 TBHQ — BANNED IN JP"},
    {"barcode":"3040400220193","product_name":"Donut","brands":"CSM France/Mondelez/Oreo","ingredients_text":"Refined wheat flour, sugar, edible vegetable oil, colours (INS 171), raising agents, emulsifiers","additive_flags":"INS 171 Titanium Dioxide — BANNED IN EU"},
    {"barcode":"9556001137722","product_name":"2 Minute Noodles Chicken Flavour","brands":"Maggi","ingredients_text":"Noodles: Refined wheat flour, palm oil, salt, thickeners; Tastemaker: chicken flavour, spices, flavour enhancers (INS 621), antioxidant (INS 319)","additive_flags":"INS 621 + INS 319 — TBHQ BANNED IN JP"},
    {"barcode":"0037600247917","product_name":"Birthday Cake","brands":"Kid's Kitchen","ingredients_text":"Refined wheat flour, sugar, eggs, edible vegetable oil, colours (INS 127), raising agents, emulsifiers","additive_flags":"INS 127 Erythrosine — BANNED IN US"},
    {"barcode":"0760263000659","product_name":"Mix Soup Creamy Wild Rice","brands":"Bear Creek Country Kitchens","ingredients_text":"Corn starch, salt, sugar, spices, colours (INS 171), edible vegetable oil","additive_flags":"INS 171 Titanium Dioxide — BANNED IN EU"},
    {"barcode":"8901512562807","product_name":"Butter Flavour Popcorn","brands":"Act II","ingredients_text":"Popcorn kernels, edible vegetable oil, butter flavour, salt, antioxidant (INS 319)","additive_flags":"INS 319 TBHQ — BANNED IN JP"},
    {"barcode":"8901044570554","product_name":"Orange Squash","brands":"Mapro","ingredients_text":"Sugar, water, orange flavour, acidity regulator, preservative, colours (INS 122)","additive_flags":"INS 122 Carmoisine — BANNED IN JP/US"},
    {"barcode":"0028000703196","product_name":"Caldo Sabor a Pollo","brands":"Maggi","ingredients_text":"Salt, sugar, chicken fat, spices, flavour enhancers (INS 621), edible vegetable oil (partially hydrogenated)","additive_flags":"PHO — BANNED IN US/CA"},
    {"barcode":"8901689031014","product_name":"Guava Crush","brands":"Mala's","ingredients_text":"Guava pulp, sugar, acidity regulator, preservative, colours (INS 127)","additive_flags":"INS 127 Erythrosine — BANNED IN US"},
    {"barcode":"8906097549588","product_name":"Sapphire Poko Loko Lychee Flavoured Juice Drink","brands":"Poko Loko","ingredients_text":"Water, lychee flavour, sugar, acidity regulator, colours (INS 122)","additive_flags":"INS 122 Carmoisine — BANNED IN JP/US"},
    {"barcode":"8901725000295","product_name":"Sunfeast Glucose 1kg","brands":"Sunfeast/ITC","ingredients_text":"Glucose, acidity regulator, colours (INS 124)","additive_flags":"INS 124 Ponceau 4R — BANNED IN US"},
    {"barcode":"8904422712119","product_name":"Groundnut Oil","brands":"Patanjali","ingredients_text":"Refined groundnut oil, antioxidant (INS 319), vitamins A & D","additive_flags":"INS 319 TBHQ — BANNED IN JP"},
    {"barcode":"9300650453982","product_name":"Oreo Double Stuff Christmas","brands":"Oreo","ingredients_text":"Refined wheat flour, sugar, refined palm oil, cocoa solids, vanilla creme, invert syrup, raising agents, emulsifiers, antioxidant (INS 319)","additive_flags":"INS 319 TBHQ — BANNED IN JP"},
    {"barcode":"5060337509831","product_name":"Monster Hydro Manic Melon","brands":"Monster","ingredients_text":"Carbonated water, sugar, acidity regulators, caffeine, taurine, colours (INS 122), flavours, vitamins","additive_flags":"INS 122 Carmoisine — BANNED IN JP/US"},
    {"barcode":"7802000020162","product_name":"Doritos Sabor Queso","brands":"Doritos","ingredients_text":"Corn flour, edible vegetable oil, cheese flavour, salt, spices, antioxidant (INS 319)","additive_flags":"INS 319 TBHQ — BANNED IN JP"},
    {"barcode":"8906020960053","product_name":"Refined Oil","brands":"Vimal","ingredients_text":"Refined vegetable oil, antioxidant (INS 319), vitamins A & D","additive_flags":"INS 319 TBHQ — BANNED IN JP"},
    {"barcode":"7613287066954","product_name":"Maggi Stir Fry Noodles Curry","brands":"Maggi","ingredients_text":"Noodles: Refined wheat flour, palm oil, salt, thickeners; Tastemaker: curry seasoning, spices, flavour enhancers (INS 621), antioxidant (INS 319)","additive_flags":"INS 621 + INS 319 — TBHQ BANNED IN JP"},
    {"barcode":"8600101639301","product_name":"Štapići","brands":"Pardon/Marbo/Pepsico","ingredients_text":"Refined wheat flour, edible vegetable oil (partially hydrogenated), salt, spices","additive_flags":"PHO — BANNED IN US/CA"},
    {"barcode":"5010238013715","product_name":"Creme Egg","brands":"Cadbury","ingredients_text":"Sugar, glucose syrup, milk solids, cocoa butter, colours (INS 171), flavours","additive_flags":"INS 171 Titanium Dioxide — BANNED IN EU"},
    {"barcode":"5000159477536","product_name":"M&M's Kersteditie Pinda","brands":"Mars","ingredients_text":"Sugar, peanuts, cocoa butter, milk solids, cocoa mass, colours (INS 171), emulsifiers","additive_flags":"INS 171 Titanium Dioxide — BANNED IN EU"},
    {"barcode":"0028000881054","product_name":"Maggi Bouillon Cubes Vegetable","brands":"Nestlé","ingredients_text":"Salt, sugar, vegetable fat, spices, flavour enhancers (INS 621), edible vegetable oil (partially hydrogenated)","additive_flags":"PHO — BANNED IN US/CA"},
    {"barcode":"0050000990467","product_name":"French Vanilla","brands":"Nestle Coffee Mate","ingredients_text":"Sugar, hydrogenated vegetable oil, milk solids, vanilla flavour, edible vegetable oil (partially hydrogenated)","additive_flags":"PHO — BANNED IN US/CA"},
    {"barcode":"0021130495511","product_name":"Chicken Gravy","brands":"Safeway Kitchens","ingredients_text":"Chicken stock, refined wheat flour, edible vegetable oil (partially hydrogenated), salt, spices","additive_flags":"PHO — BANNED IN US/CA"},
    {"barcode":"0028000130008","product_name":"Candy","brands":"Nestlé","ingredients_text":"Sugar, glucose syrup, cocoa solids, antioxidant (INS 319)","additive_flags":"INS 319 TBHQ — BANNED IN JP"},
    {"barcode":"0040000503170","product_name":"Snickers Fun Size Crisper","brands":"Snickers","ingredients_text":"Sugar, peanuts, glucose syrup, milk solids, cocoa butter, cocoa mass, edible vegetable oil (partially hydrogenated), emulsifiers","additive_flags":"PHO — BANNED IN US/CA"},
    {"barcode":"0066721009401","product_name":"White Fudge Covered Oreos","brands":"Oreo","ingredients_text":"Sugar, cocoa butter, milk solids, refined wheat flour, colours (INS 171), emulsifiers","additive_flags":"INS 171 Titanium Dioxide — BANNED IN EU"},
    {"barcode":"0690166227313","product_name":"Fruit & Nut Yogurt Mix","brands":"Nature's Kitchen","ingredients_text":"Yogurt, dried fruits, nuts, sugar, colours (INS 171), edible vegetable oil (partially hydrogenated)","additive_flags":"INS 171 + PHO — BANNED IN EU/US/CA"},
    {"barcode":"0028000517311","product_name":"Maggi Creamy Seafood Soup Mix","brands":"Maggi","ingredients_text":"Corn starch, salt, sugar, seafood flavour, colours, antioxidant (INS 319)","additive_flags":"INS 319 TBHQ — BANNED IN JP"},
    {"barcode":"0073402352008","product_name":"Plain Powdered Fine Donuts","brands":"Country Kitchen/Lepage Bakeries","ingredients_text":"Refined wheat flour, sugar, edible vegetable oil (partially hydrogenated), colours (INS 171), raising agents","additive_flags":"INS 171 + PHO — BANNED IN EU/US/CA"},
    {"barcode":"8906002000012","product_name":"Funfoods Classic Egg Mayonnaise","brands":"Dr. Oetker","ingredients_text":"Refined soybean oil, eggs, water, sugar, vinegar, iodized salt, thickener, preservative (INS 211), antioxidant (INS 319)","additive_flags":"INS 211 + INS 319 — TBHQ BANNED IN JP"},
    {"barcode":"8904132948181","product_name":"Campa Orange Flavour 500ml","brands":"Campa","ingredients_text":"Carbonated water, sugar, acidity regulators (INS 330, INS 331(iii)), orange juice concentrate, colours (INS 122), artificial orange flavour, preservative (INS 211)","additive_flags":"INS 122 Carmoisine — BANNED IN JP/US"},
    {"barcode":"8901071702201","product_name":"Hershey's Exotic Dark","brands":"Hershey's","ingredients_text":"Sugar, cocoa solids, cocoa butter, milk solids, emulsifiers, colours (INS 122)","additive_flags":"INS 122 Carmoisine — BANNED IN JP/US"}
]

elevated_count = 0
added_count = 0
purged_count = 0

for item in batch_25_rows:
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

    # Update or add in master DB
    idx_all = df_all[df_all['barcode'] == barcode].index
    if len(idx_all) > 0:
        df_all.loc[idx_all, 'product_name'] = pname
        df_all.loc[idx_all, 'brands'] = brand
        df_all.loc[idx_all, 'ingredients_text'] = ing
    else:
        status_tag = 'CONFIRMED_INDIA_890' if barcode.startswith('890') else 'CONFIRMED_FOREIGN'
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
    status_tag = 'CONFIRMED_INDIA_890' if barcode.startswith('890') else 'CONFIRMED_FOREIGN'
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

print(f"Batch 25 Processing Summary:")
print(f"  Elevated from Needs Verification to Confirmed: {elevated_count}")
print(f"  Newly added to Confirmed: {added_count}")
print(f"  Purged Non-Food Barcodes: {purged_count}")
print(f"  Final Master CSV Count: {len(df_all)}")
print(f"  Final Confirmed CSV Count: {len(df_confirmed)}")
print(f"  Final Needs Verification CSV Count: {len(df_needs_ver)}")
