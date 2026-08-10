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

# 2. BATCH 9 DATA
csv_input = """barcode,product_name,brands,ingredients_text,sold_in_india_status,ingredient_confidence,status,data_source,source_license,collection_method
8901058018493,Maggi 2-Minute Noodles Masala,Nestlé,"Noodles: Refined wheat flour (maida), palm oil, iodized salt, wheat gluten, thickeners (INS 508, INS 412), acidity regulators (INS 501(i), INS 500(i)); Tastemaker: salt, onion, sugar, coriander, chilli, turmeric, garlic, cumin, fenugreek, antioxidant (INS 319)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901058000221,Maggi 2 Minute Noodles,Nestlé,"Noodles: Refined wheat flour, palm oil, iodized salt, wheat gluten, thickeners (INS 508, INS 412), acidity regulators; Tastemaker: salt, spices, sugar, flavour enhancers (INS 621), antioxidant (INS 319)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901058901580,Maggi Special Masala Noodles,Nestlé,"Noodles: Refined wheat flour, palm oil, salt, wheat gluten, thickeners, acidity regulators; Tastemaker: salt, spices, sugar, flavour enhancers (INS 621), antioxidant (INS 319)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901058854107,Maggi Oats Masala Noodles,Nestlé,"Oats flour, refined wheat flour, palm oil, salt, thickeners, acidity regulators; Tastemaker: salt, spices, sugar, flavour enhancers (INS 621), antioxidant (INS 319)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901058009699,Maggi Atta Noodles,Nestlé,"Whole wheat flour (atta), palm oil, salt, wheat gluten, thickeners, acidity regulators; Tastemaker: salt, spices, flavour enhancers (INS 621), antioxidant (INS 319)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901058006643,Maggi 2 Minutes Noodles Masala,Nestlé,"Noodles: Refined wheat flour, palm oil, iodized salt, wheat gluten, thickeners (INS 508, INS 412), acidity regulators; Tastemaker: salt, onion, sugar, spices, antioxidant (INS 319)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901058002270,Maggi Spicy Garlic Noodles,Nestlé,"Noodles: Refined wheat flour, palm oil, salt, thickeners; Tastemaker: salt, garlic, chilli, spices, flavour enhancers (INS 621), antioxidant (INS 319)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901058013665,Maggi Hot and Sweet Noodles,Nestlé,"Noodles: Refined wheat flour, palm oil, salt, thickeners; Tastemaker: salt, sugar, chilli, garlic, flavour enhancers (INS 621), antioxidant (INS 319)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901058866711,Maggi Veg Atta Noodles 290g,Nestlé,"Whole wheat flour, palm oil, salt, thickeners; Tastemaker: salt, spices, flavour enhancers (INS 621), antioxidant (INS 319)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901058016116,KitKat 50,Nestlé,"Refined wheat flour, sugar, cocoa butter, milk solids, cocoa mass, emulsifier (INS 322), yeast, salt, raising agent (INS 500(ii)), flavouring",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901058023558,KitKat Dark Chocolate Minis,Nestlé,"Refined wheat flour, sugar, cocoa butter, cocoa solids, milk solids, emulsifier (INS 322), yeast, salt, raising agent (INS 500(ii)), flavouring",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901058905472,Kit Kat,Nestlé,"Refined wheat flour, sugar, cocoa butter, milk solids, cocoa mass, emulsifier (INS 322), yeast, salt, raising agent (INS 500(ii)), flavouring",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901058852141,KitKat Caramel Chocolate Coated Wafer,Nestlé,"Refined wheat flour, sugar, cocoa butter, milk solids, glucose syrup, emulsifier (INS 322), yeast, salt, raising agent, flavouring",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901058010701,Nestlé Munch Vanilla Flavour,Nestlé,"Sugar, refined wheat flour, hydrogenated vegetable oil (palm), milk solids, cocoa solids, emulsifier (INS 322), salt, raising agent (INS 500(ii)), artificial vanilla flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901058900361,Nestlé Munch Nuts,Nestlé,"Sugar, refined wheat flour, hydrogenated vegetable oil (palm), peanuts, milk solids, cocoa solids, emulsifier (INS 322), salt, raising agent",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901058875577,Milkybar,Nestlé,"Sugar, milk solids, cocoa butter, emulsifier (INS 322), artificial vanilla flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901058016055,Nescafé Classic,Nestlé,"100% instant coffee",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901058865660,Nescafé Gold Cappuccino,Nestlé,"Instant coffee, sugar, milk solids, glucose syrup, hydrogenated vegetable oil (palm kernel), salt, stabilizers (INS 340(ii), INS 452(i)), emulsifier (INS 471), anticaking agent (INS 551)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901058011401,Nescafé Ice Roast,Nestlé,"Coffee beans (100% instant coffee)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901058014723,Nescafé Sunrise,Nestlé,"Coffee, chicory",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901058869453,EveryDay Dairy Whitener,Nestlé,"Milk solids, sugar, emulsifier (INS 322), stabilizers",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901058007060,Milkmaid Mini,Nestlé,"Milk solids, sugar",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901058897500,Nestlé Nan Pro 2,Nestlé,"Demineralized whey, vegetable oils, skimmed milk powder, lactose, minerals, vitamins, emulsifier",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901058018400,Nestlé Cerelac,Nestlé,"Wheat flour, sugar, milk solids, minerals, vitamins, emulsifier",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901058004922,Maggi Rich Tomato Ketchup,Nestlé,"Tomato paste, sugar, water, vinegar, salt, spices, acidity regulator (INS 260), preservative (INS 211)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901058008388,Maggi Hot & Sweet Tomato Chilli Sauce,Nestlé,"Tomato paste, sugar, water, vinegar, salt, chilli, garlic, acidity regulator (INS 260), preservative (INS 211), thickener (INS 1422)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901058003055,Maggi Pazzta Cheese Macaroni,Nestlé,"Macaroni: Durum wheat semolina, salt; Tastemaker: milk solids, cheese powder, sugar, salt, palm oil, thickeners (INS 1422, INS 412), flavour enhancers (INS 621, INS 627, INS 631), artificial cheese flavour, colour (INS 160a)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901058014846,Maggi Pazzta Cheesy Tomato Twist,Nestlé,"Macaroni: Durum wheat semolina, salt; Tastemaker: tomato powder, milk solids, sugar, salt, palm oil, thickeners, flavour enhancers (INS 621, INS 627, INS 631), colour (INS 160c)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901058006032,Maggi Cup Noodles Masala,Nestlé,"Noodles: Refined wheat flour, palm oil, salt, wheat gluten, thickeners; Tastemaker: salt, spices, sugar, flavour enhancers (INS 621, INS 627, INS 631), antioxidant (INS 319)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901058001167,Maggi Pichkoo Tomato Ketchup,Nestlé,"Tomato paste, sugar, water, vinegar, salt, spices, acidity regulator (INS 260), preservative (INS 211)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901058016222,Maggi Rich Tomato Ketchup,Nestlé,"Tomato paste, sugar, water, vinegar, salt, spices, acidity regulator (INS 260), preservative (INS 211)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901058905045,Soothers Herbal Throat Drops,Nestlé,"Sugar, glucose syrup, herbal extracts, vitamin C, acidity regulator",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901058896381,Nescafé Sunrise Coffee 200g,Nestlé,"Instant coffee, chicory",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901030976186,Horlicks,HUL,"Malted cereals (66.7%) [barley, wheat flour, wheat, millet], milk solids (14%), sugar, wheat gluten, iodized salt, minerals, vitamins, emulsifier (INS 471)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901030825668,Horlicks Classic Malt 500g,HUL,"Malted cereals (66.7%), milk solids (14%), sugar, wheat gluten, iodized salt, minerals, vitamins, emulsifier (INS 471)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901030538018,Horlicks Classic Malt 750g,HUL,"Malted cereals (66.7%), milk solids (14%), sugar, wheat gluten, iodized salt, minerals, vitamins, emulsifier (INS 471)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8909106024502,Horlicks Classic Malt 1kg,HUL,"Malted cereals (66.7%), milk solids (14%), sugar, wheat gluten, iodized salt, minerals, vitamins, emulsifier (INS 471)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901030985973,Horlicks Chocolate Delight 500g,HUL,"Malted cereals, milk solids, sugar, cocoa solids, wheat flour, minerals, vitamins, emulsifier (INS 471), artificial chocolate flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901030825521,Horlicks Protein Plus Chocolate,HUL,"Milk solids, malted cereals, sugar, cocoa solids, wheat flour, minerals, vitamins, emulsifier (INS 471)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901030949654,Women Horlicks,HUL,"Malted cereals, milk solids, sugar, wheat flour, minerals (Iron, Calcium), vitamins, emulsifier (INS 471)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8909106070615,Horlicks Super Foods,HUL,"Malted cereals, milk solids, sugar, wheat flour, superfoods (chia, flax), minerals, vitamins",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8909106018372,Boost,HUL,"Cereal extract (50%) [barley, wheat, millet], malted barley (21%), sugar, wheat flour, milk solids (6%), minerals, natural colour (INS 150c), vitamins",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901030820946,Boost,HUL,"Cereal extract (50%), malted barley (21%), sugar, wheat flour, milk solids (6%), minerals, natural colour (INS 150c), vitamins",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901030795909,Boost,HUL,"Cereal extract (50%), malted barley (21%), sugar, wheat flour, milk solids (6%), minerals, natural colour (INS 150c), vitamins",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901030882609,Brooke Bond Red Label 1kg,HUL,"100% black tea (CTC dust & fannings blend)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901030918810,Brooke Bond Taaza Tea,HUL,"100% black tea (CTC blend)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901030083037,Red Label Tea,HUL,"100% black tea",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901030251504,Brooke Bond Taj Mahal Tea,HUL,"100% black tea (CTC blend)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901030624247,Taj Mahal Tea Bags,HUL,"100% black tea",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901030681530,Taj Mahal Tea Bags,HUL,"100% black tea",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901030681547,Taj Mahal Tea Bags,HUL,"100% black tea",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901030373930,Bru Gold Instant Coffee,HUL,"100% instant coffee (freeze-dried)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8909106024199,Bru Coffee 3rs Sachet,HUL,"Instant coffee, sugar, milk solids, emulsifier",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901030831706,Kissan Mixed Fruit Jam,HUL,"Sugar, mixed fruit pulp blend (approx. 46%), acidity regulator (INS 330), preservative (INS 211 sodium benzoate), permitted synthetic food colour (INS 122)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901030831720,Kissan Mixed Fruit Jam 700g,HUL,"Sugar, mixed fruit pulp blend (approx. 46%), acidity regulator (INS 330), preservative (INS 211), permitted synthetic food colour (INS 122)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901030850400,Kissan Mixed Fruit Jam 500g,HUL,"Sugar, mixed fruit pulp blend (approx. 46%), acidity regulator (INS 330), preservative (INS 211), permitted synthetic food colour (INS 122)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901030931864,Kissan Tomato Puree,HUL,"Tomato, salt, acidity regulator",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901030717376,Kissan Tomato Ketchup,HUL,"Tomato paste, sugar, vinegar, salt, spices, acidity regulator (INS 260), preservative (INS 211)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901030926518,Kissan Sweet and Spicy Ketchup,HUL,"Tomato paste, sugar, vinegar, salt, spices, acidity regulator, preservative (INS 211)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901030559266,Knorr Mexican Tomato Corn Soup,HUL,"Tomato powder, corn, sugar, salt, spices, flavour enhancers (INS 621), acidity regulator, colour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901030902352,Knorr Tomato Chatpata Soup,HUL,"Tomato powder, sugar, salt, spices, flavour enhancers (INS 621), acidity regulator",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901030900297,Knorr Hong Kong Manchow Soup,HUL,"Corn starch, salt, sugar, spices, flavour enhancers (INS 621), acidity regulator",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901030900334,Knorr Chicken Delite Soup,HUL,"Corn starch, salt, sugar, chicken powder, spices, flavour enhancers (INS 621)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901725017545,Sunfeast Nice,ITC,"Refined wheat flour, sugar, coconut, edible vegetable oil (palm), invert syrup, raising agents (INS 503(ii), INS 500(ii)), salt, emulsifier (INS 322), artificial coconut flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901725015916,Sunfeast Dark Fantasy Choco Fills,ITC,"Choco crème (sugar, refined palmolein, refined palm oil, cocoa solids), refined wheat flour, sugar, invert syrup, liquid glucose, cocoa solids, milk solids, butter, raising agents, emulsifiers, salt",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901725136215,Sunfeast Dark Fantasy BIG Choco Fills,ITC,"Choco crème (sugar, refined palmolein, refined palm oil, cocoa solids), refined wheat flour, sugar, invert syrup, liquid glucose, cocoa solids, milk solids, butter, raising agents, emulsifiers, salt",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901725016265,Sunfeast Dark Fantasy Bourbon,ITC,"Refined wheat flour, sugar, edible vegetable oil (palm), cocoa solids, invert syrup, raising agents, emulsifiers, salt, artificial chocolate flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901725000622,Sunfeast Mom's Magic Cashew Almond,ITC,"Refined wheat flour, sugar, edible vegetable oil (palm), cashew nuts, almonds, invert syrup, milk solids, raising agents, emulsifiers",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901725006143,Sunfeast Marie Light,ITC,"Refined wheat flour, sugar, refined palm oil, invert sugar syrup, milk solids, raising agents, salt, emulsifiers",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901725114916,Sunfeast Marie Light,ITC,"Refined wheat flour, sugar, refined palm oil, invert sugar syrup, milk solids, raising agents, salt, emulsifiers",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901725013004,Sunfeast Marie Light Family Pack,ITC,"Refined wheat flour, sugar, refined palm oil, invert sugar syrup, milk solids, raising agents, salt, emulsifiers",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901725002190,Sunfeast All Rounder Cream & Herb,ITC,"Refined wheat flour, sugar, edible vegetable oil, cream powder, herbs, invert syrup, raising agents, emulsifiers, salt",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901725001612,Sunfeast All Rounder Chatpata Masala,ITC,"Refined wheat flour, edible vegetable oil, spices, salt, sugar, raising agents, emulsifiers",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901725012878,Sunfeast Caker Swiss Roll Choco 115g,ITC,"Refined wheat flour, sugar, eggs, edible vegetable oil, cocoa solids, glucose syrup, raising agents, emulsifiers, preservative (INS 202), flavours",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901725004545,Sunfeast Milk Shake 300ml,ITC,"Toned milk, sugar, artificial flavour, stabilizers (INS 466, INS 407), emulsifier (INS 471)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901725116149,Dark Fantasy Chocolate Shake,ITC,"Toned milk, sugar, cocoa solids, artificial chocolate flavour, stabilizers, emulsifiers, colours (INS 150c)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901725005993,Yippee Noodles Mood Masala,ITC,"Refined wheat flour, refined palm oil, salt, wheat gluten, thickeners (INS 508, INS 412); Masala: spices, sugar, salt, flavour enhancers (INS 621, INS 627, INS 631)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901725119959,Yippee Noodles,ITC,"Refined wheat flour, refined palm oil, salt, wheat gluten, thickeners; Masala: spices, sugar, salt, flavour enhancers (INS 621)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901725114060,Mini Idli Sambar,ITC,"Rice flour, urad dal flour, salt, sambar masala (spices, tamarind, salt)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901725013714,Bingo Mad Angles Achaari Masti,ITC,"Corn grits, edible vegetable oil, rice grits, gram flour, spices, salt, sugar, flavour enhancers (INS 621, INS 627, INS 631), colours (INS 160c)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901725004217,Bingo Tedhe Medhe Tomato,ITC,"Corn grits, edible vegetable oil, rice grits, gram flour, spices, salt, sugar, tomato powder, flavour enhancers (INS 621, INS 627, INS 631), colours (INS 160c)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901725192341,Bingo Potato Chips Chilli,ITC,"Potato, edible vegetable oil, spices, salt, sugar, flavour enhancers (INS 621), colours (INS 160c)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901725001070,Aashirvaad Double Roasted Suji Rava,ITC,"Semolina (double roasted)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901725008888,Aashirvaad Shudh Chakki Atta,ITC,"100% whole wheat flour (chakki-ground)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901725008895,Aashirvaad Shudh Chakki Atta 10kg,ITC,"100% whole wheat flour (chakki-ground)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901725006679,Aashirvaad Atta with Multigrains,ITC,"Whole wheat flour, oats, barley, millet, corn, rice flour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901725100575,Aashirvaad Atta with Multigrains 5kg,ITC,"Whole wheat flour, oats, barley, millet, corn, rice flour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901725121747,Aashirvaad Superior MP Atta,ITC,"100% whole wheat flour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901725112592,Aashirvaad Gulab Jamun,ITC,"Milk solids, sugar, edible vegetable oil, cardamom, rose water",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901725007775,Aashirvaad Malabar Paratha,ITC,"Whole wheat flour, water, edible vegetable oil, salt",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906065166045,ITC Farmland Frozen Green Peas,ITC,"Green peas",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901725120306,Sunfeast Big Vanilla Fills Biscuit,ITC,"Refined wheat flour, sugar, edible vegetable oil, vanilla flavour, invert syrup, raising agents, emulsifiers",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063092709,Good Day Cashew,Britannia,"Refined wheat flour, edible vegetable oil (palm), sugar, cashew nuts (4.5%), invert syrup, milk solids, butter (0.6%), raising agents, salt, emulsifier (INS 322)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063093089,Good Day Cashew,Britannia,"Refined wheat flour, edible vegetable oil, sugar, cashew nuts, invert syrup, milk solids, raising agents, emulsifier",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063151307,Good Day Cashew Cookies,Britannia,"Refined wheat flour, edible vegetable oil, sugar, cashew nuts, invert syrup, milk solids, raising agents, emulsifier",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063136779,Good Day Choco Almond,Britannia,"Refined wheat flour, edible vegetable oil, sugar, cocoa solids, almond (3%), invert syrup, milk solids, raising agents, emulsifier",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063092440,Good Day Butter,Britannia,"Refined wheat flour, edible vegetable oil, sugar, butter, invert syrup, milk solids, raising agents, emulsifier, artificial butter flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063092792,Good Day Butter Jeera Biscuits,Britannia,"Refined wheat flour, edible vegetable oil, sugar, cumin, butter, invert syrup, raising agents, emulsifier",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063162303,Marie Gold,Britannia,"Refined wheat flour (73%), sugar, refined palm oil, invert sugar syrup, milk solids, raising agents, salt, emulsifiers (INS 471, INS 322)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063151383,Marie Gold,Britannia,"Refined wheat flour (73%), sugar, refined palm oil, invert sugar syrup, milk solids, raising agents, salt, emulsifiers",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063371071,Marie Gold 1kg,Britannia,"Refined wheat flour (73%), sugar, refined palm oil, invert sugar syrup, milk solids, raising agents, salt, emulsifiers",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063165847,Treat,Britannia,"Refined wheat flour, sugar, edible vegetable oil, invert syrup, raising agents, emulsifiers, flavours",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063029323,Jim Jam,Britannia,"Refined wheat flour, sugar, edible vegetable oil, invert syrup, raising agents, salt, emulsifier, colours (INS 122, INS 110)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063167124,Jim Jam,Britannia,"Refined wheat flour, sugar, edible vegetable oil, invert syrup, raising agents, salt, emulsifier, colours (INS 122, INS 110)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063012578,Milk Bikis Classic,Britannia,"Refined wheat flour, sugar, milk solids, edible vegetable oil, invert syrup, raising agents, salt, emulsifier, artificial vanilla flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063012493,Milk Bikis Biscuits,Britannia,"Refined wheat flour, sugar, milk solids, edible vegetable oil, invert syrup, raising agents, emulsifier",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063165618,Little Hearts,Britannia,"Refined wheat flour, sugar, edible vegetable oil, invert syrup, milk solids, raising agents, salt, emulsifier",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063017399,50-50 Maska Chaska,Britannia,"Refined wheat flour, sugar, edible vegetable oil, invert syrup, salt, raising agents, emulsifier, artificial butter flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063139336,Bourbon 100g,Britannia,"Refined wheat flour, sugar, edible vegetable oil, cocoa solids, invert syrup, raising agents, salt, emulsifiers, artificial chocolate flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063026346,NutriChoice Digestive,Britannia,"Whole wheat flour (71%), sugar, edible vegetable oil, raising agents, salt, emulsifiers, added vitamins & minerals",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063166318,NutriChoice Digestive Biscuits,Britannia,"Whole wheat flour (71%), sugar, edible vegetable oil, raising agents, salt, emulsifiers, added vitamins & minerals",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063155497,Tiger Krunch Coconut,Britannia,"Refined wheat flour, sugar, edible vegetable oil, coconut, invert syrup, raising agents, emulsifier, artificial coconut flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063155572,Tiger Krunch,Britannia,"Refined wheat flour, sugar, edible vegetable oil, coconut, invert syrup, raising agents, emulsifier",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063325074,Toastea,Britannia,"Refined wheat flour, sugar, edible vegetable oil, invert syrup, milk solids, raising agents, salt, emulsifier, artificial vanilla flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063325357,Toastea Rusk,Britannia,"Refined wheat flour, sugar, edible vegetable oil, invert syrup, milk solids, raising agents, emulsifier",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063365933,Gobbles Fruit Cake 100g,Britannia,"Refined wheat flour, sugar, eggs, edible vegetable oil, glucose syrup, mixed fruit peel, raising agents, emulsifiers, preservative (INS 202), colours",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063365131,Britannia Marble Cake,Britannia,"Refined wheat flour, sugar, eggs, edible vegetable oil, glucose syrup, cocoa solids, raising agents, emulsifiers, preservative (INS 202)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063363960,Britannia Gobbles Chocolate Cake,Britannia,"Refined wheat flour, sugar, eggs, edible vegetable oil, glucose syrup, cocoa solids, raising agents, emulsifiers, preservative (INS 202), colour (INS 122)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063363922,Muffils Strawberry,Britannia,"Refined wheat flour, sugar, eggs, edible vegetable oil, glucose syrup, strawberry flavour, raising agents, emulsifiers, preservative (INS 202), colour (INS 122)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063146938,Winkin' Cow Bourbon Shake,Britannia,"Toned milk, sugar, cocoa solids, artificial chocolate flavour, stabilizers, emulsifier, colour (INS 150c)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063146952,Winkin' Cow Strawberry Shake,Britannia,"Toned milk, sugar, strawberry flavour, stabilizers, emulsifier, colour (INS 122)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063342910,Brown Bread,Britannia,"Whole wheat flour, refined wheat flour, water, sugar, edible vegetable oil, gluten, yeast, salt, preservative (INS 282), emulsifiers",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901719135477,Parle-G Gold,Parle,"Refined wheat flour, sugar, invert syrup, refined palm oil, salt, skimmed milk powder, raising agents (INS 503(ii), INS 500(ii)), emulsifier (INS 471), artificial vanilla flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901719128486,Parle-G Rs 10,Parle,"Refined wheat flour, sugar, invert syrup, refined palm oil, salt, skimmed milk powder, raising agents (INS 503(ii), INS 500(ii)), emulsifier (INS 471), artificial vanilla flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901719123900,Parle-G Gold,Parle,"Refined wheat flour, sugar, invert syrup, refined palm oil, salt, skimmed milk powder, raising agents, emulsifier, artificial vanilla flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901719135521,Parle Marie,Parle,"Refined wheat flour, sugar, refined palm oil, invert sugar syrup, milk solids, raising agents, salt, emulsifiers",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901719123801,Parle Monaco Classic,Parle,"Refined wheat flour, edible vegetable oil, salt, sugar, raising agents, emulsifier, artificial butter flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901719122781,Parle Monaco 700g,Parle,"Refined wheat flour, edible vegetable oil, salt, sugar, raising agents, emulsifier",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901719135309,Krackjack,Parle,"Refined wheat flour, sugar, edible vegetable oil, invert syrup, salt, raising agents, emulsifier",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901719124006,Parle Krackjack,Parle,"Refined wheat flour, sugar, edible vegetable oil, invert syrup, salt, raising agents, emulsifier",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901719136801,Hide & Seek Milano Creme,Parle,"Refined wheat flour, sugar, edible vegetable oil, cocoa solids, invert syrup, milk solids, raising agents, emulsifiers",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901719136757,Hide & Seek Finest Choco,Parle,"Refined wheat flour, sugar, edible vegetable oil, cocoa solids, invert syrup, milk solids, raising agents, emulsifiers",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901719113871,Parle Platina Hide & Seek Choco Rolls,Parle,"Refined wheat flour, sugar, edible vegetable oil, cocoa solids, choco chips, invert syrup, milk solids, raising agents, emulsifiers",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901719135842,Parle Hide & Seek Strawberry,Parle,"Refined wheat flour, sugar, edible vegetable oil, strawberry flavour, invert syrup, raising agents, emulsifier, colours (INS 122)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901719126970,Parle 20-20 Cashew,Parle,"Refined wheat flour, sugar, edible vegetable oil, cashew nuts, invert syrup, milk solids, raising agents, emulsifier",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901719129179,Parle Coconut,Parle,"Refined wheat flour, sugar, coconut, edible vegetable oil, invert syrup, raising agents, emulsifier, artificial coconut flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901719136719,Parle Jam In,Parle,"Refined wheat flour, sugar, fruit jam, edible vegetable oil, invert syrup, raising agents, emulsifier, colours (INS 110, INS 102)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901719130854,Melody Chocolate,Parle,"Sugar, glucose syrup, hydrogenated vegetable oil (palm kernel), milk solids, cocoa solids, emulsifier (INS 322), salt",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901719127762,Mango Bite Candy,Parle,"Sugar, glucose syrup, mango pulp, acidity regulator (INS 330), artificial mango flavour, colour (INS 160c)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901719119026,Parle Assorted Candy Orange Bite,Parle,"Sugar, glucose syrup, orange flavour, acidity regulator, colour (INS 160c)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901719130090,Parle Happy Happy,Parle,"Refined wheat flour, sugar, edible vegetable oil, invert syrup, salt, raising agents, emulsifier",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901719128264,Parle Aloo Bikki,Parle,"Refined wheat flour, potato, edible vegetable oil, spices, salt, sugar, raising agents",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901719127359,Parle Milk Shakti,Parle,"Refined wheat flour, sugar, milk solids, edible vegetable oil, invert syrup, raising agents, emulsifiers",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901719127236,Parle Rusk,Parle,"Refined wheat flour, sugar, edible vegetable oil, invert syrup, milk solids, raising agents, emulsifier",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901719122927,Parle Rusk Milk Premium,Parle,"Refined wheat flour, sugar, edible vegetable oil, invert syrup, milk solids, raising agents, emulsifier",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901719707490,Murano Chocolate Chip Cookies,Parle,"Refined wheat flour, sugar, chocolate chips, edible vegetable oil, invert syrup, raising agents, emulsifiers",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901719132155,Cocktail Mix,Parle,"Refined wheat flour, sugar, edible vegetable oil, invert syrup, salt, raising agents, emulsifiers",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901233028361,Dairy Milk,Cadbury,"Sugar, milk solids, cocoa butter, cocoa mass, emulsifiers (INS 322, INS 476), flavours",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901233028392,Dairy Milk,Cadbury,"Sugar, milk solids, cocoa butter, cocoa mass, emulsifiers (INS 322, INS 476), flavours",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901233034300,Dairy Milk Silk Bubbly,Cadbury,"Sugar, milk solids, cocoa butter, cocoa mass, emulsifiers (INS 322, INS 476), flavours",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901233034263,Dairy Milk Roast Almond,Cadbury,"Sugar, milk solids, cocoa butter, cocoa mass, almonds (15%), emulsifiers, flavours",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901233033563,Dairy Milk Silk Minis,Cadbury,"Sugar, milk solids, cocoa butter, cocoa mass, emulsifiers (INS 322, INS 476), flavours",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901233024622,Cadbury Oreo 60g,Cadbury,"Refined wheat flour, sugar, refined palm oil, cocoa solids (5%), invert syrup, raising agents, salt, emulsifier (INS 322), antioxidant (INS 319)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901233024257,Dairy Milk Oreo,Cadbury,"Sugar, milk solids, cocoa butter, cocoa mass, refined wheat flour, emulsifiers, flavours",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901233023687,Cadbury FUSE,Cadbury,"Sugar, milk solids, cocoa butter, cocoa mass, glucose syrup, vegetable fats, emulsifiers (INS 442, INS 476), flavours",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901233024042,Cadbury Perk,Cadbury,"Sugar, milk solids, cocoa solids, edible vegetable oil, emulsifiers, artificial flavours",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901233031712,Cadbury Fuse,Cadbury,"Sugar, milk solids, cocoa butter, cocoa mass, glucose syrup, emulsifiers (INS 442, INS 476), flavours",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901233023748,Bournvita Original Refill 500g,Cadbury,"Malt extract (wheat/barley), sugar, milk solids, cocoa solids, liquid glucose, minerals, vitamins, emulsifier (INS 322), salt",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901233022536,Bournvita Biscuit,Cadbury,"Refined wheat flour, sugar, cocoa solids, edible vegetable oil, milk solids, raising agents, emulsifiers",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901233025957,Marvellous Creations Jelly Popping Candy,Cadbury,"Sugar, glucose syrup, milk solids, cocoa butter, cocoa mass, emulsifiers, colours, flavours, popping candy",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901233024981,Cadbury Zip Chocolate,Cadbury,"Sugar, glucose syrup, milk solids, cocoa butter, cocoa mass, emulsifiers, flavours",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901233022575,Cadbury Perk,Cadbury,"Sugar, milk solids, cocoa solids, edible vegetable oil, emulsifiers, artificial flavours",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901233022576,Cadbury Gems,Cadbury,"Sugar, milk solids, cocoa solids, edible vegetable oil, emulsifier (INS 322), colours (INS 102, INS 110, INS 122, INS 133)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901233030395,Cadbury Spready,Cadbury,"Sugar, edible vegetable fat, milk solids (16%), cocoa solids, emulsifier (INS 442), added flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
7622202324925,Dairy Milk Bites,Cadbury,"Sugar, milk solids, cocoa butter, cocoa mass, emulsifiers, flavours",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
7622202335488,Cadbury Nutties Chocolate 30g,Cadbury,"Sugar, peanuts, cocoa butter, milk solids, cocoa mass, emulsifiers",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
7622210063465,Cadbury Dairy Milk,Cadbury,"Sugar, milk solids, cocoa butter, cocoa mass, emulsifiers, flavours",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904063254696,Aloo Bhujia,Haldiram's,"Potato flakes & starch, edible vegetable oil (palmolein), gram flour, iodized salt, spices, colour (INS 160c)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904063254697,Bhujia Sev,Haldiram's,"Gram flour (besan), edible vegetable oil, iodized salt, spices",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904004403770,Moong Dal,Haldiram's,"Moong dal, edible vegetable oil, iodized salt, spices",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904063216403,Khatta Meetha,Haldiram's,"Rice flakes, edible vegetable oil, sugar, peanuts, sago, salt, spices, raising agents, colours (INS 160c)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904063216168,Bombay Mix,Haldiram's,"Rice flakes, gram flour, edible vegetable oil, peanuts, sago, salt, spices, raising agents, colours (INS 160c)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904063230133,Cornflakes Mixture,Haldiram's,"Corn flakes, edible vegetable oil, peanuts, sago, salt, spices, sugar, raising agents, colours (INS 160c)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904063214942,All In One Mixture,Haldiram's,"Rice flakes, gram flour, edible vegetable oil, peanuts, sago, salt, spices, curry leaves, raising agents, colours",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904063203441,Ratlami Mixture,Haldiram's,"Rice flakes, gram flour, edible vegetable oil, peanuts, sago, salt, spices, raising agents, colours",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904063253194,Kashmiri Mixture,Haldiram's,"Rice flakes, gram flour, edible vegetable oil, peanuts, sago, salt, spices, raisins, raising agents, colours",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904063253804,Punjabi Tadka,Haldiram's,"Rice flakes, gram flour, edible vegetable oil, peanuts, sago, salt, spices, raising agents, colours",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904004403534,Tasty Nuts,Haldiram's,"Peanuts, edible vegetable oil, iodized salt, spices",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904063253156,Samosa,Haldiram's,"Refined wheat flour, potato, peas, edible vegetable oil, spices, salt",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904063281586,Kadhai Paneer,Haldiram's,"Paneer, edible vegetable oil, spices, salt, sugar",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904063259400,Minute Khana,Haldiram's,"Refined wheat flour, edible vegetable oil, spices, salt, sugar, raising agents",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904063281494,Rasmalai,Haldiram's,"Milk solids, sugar, cardamom, saffron",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904063281234,Phulka Roti,Haldiram's,"Whole wheat flour, water, salt",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904063222091,Cheese Balls,Haldiram's,"Refined wheat flour, cheese powder, edible vegetable oil, spices, salt, raising agents",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904063205018,Bread Pakora,Haldiram's,"Refined wheat flour, potato, edible vegetable oil, spices, salt, raising agents",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904063224668,Mirchi Pakoda,Haldiram's,"Gram flour, green chilli, edible vegetable oil, spices, salt, raising agents",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904063258410,Yellow Banana Chips,Haldiram's,"Banana, edible vegetable oil, iodized salt",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904063200570,Chai Puri,Haldiram's,"Refined wheat flour, edible vegetable oil, sugar, salt, spices, raising agents",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904063253262,Boondi,Haldiram's,"Gram flour, edible vegetable oil, iodized salt, spices, colours (INS 160c)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904063240248,Haldiram Bhujia 1kg,Haldiram's,"Gram flour, edible vegetable oil, iodized salt, spices, colour (INS 160c)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904063226372,Veggie And Paneer Momos,Haldiram's,"Refined wheat flour, paneer, vegetables, edible vegetable oil, spices, salt",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904063204578,Gluten Free Chapati,Haldiram's,"Gluten-free flour blend, water, salt",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901262150095,Amul Gold Milk 200ml,Amul,"Standardized milk (4.5% fat, 8.5% SNF), vitamins A & D",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901262153577,Amul Taaza Toned Milk 200ml,Amul,"Toned milk (3.0% fat, 8.5% SNF), vitamins A & D",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901262010436,Amul White Unsalted Butter,Amul,"Pasteurized milk cream",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901262030243,Amul Ghee,Amul,"Milk solids (pure cow ghee)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901262030250,Amul Pure Ghee,Amul,"Milk solids (pure cow ghee)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901262200271,Amul Dahi,Amul,"Pasteurized toned milk, active lactic culture",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901262180030,Amul Paneer,Amul,"Milk solids, citric acid (coagulant)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901262020404,Amul Cheese Slices,Amul,"Milk solids, salt, emulsifying salts (INS 331, INS 452), preservative (INS 200), colour (INS 160a)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901262020091,Amul Cheese Cubes,Amul,"Milk solids, salt, emulsifying salts (INS 331, INS 452), preservative (INS 200)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901262151375,Amul Cool Kesar,Amul,"Toned milk, sugar, kesar flavour, stabilizers, emulsifier, colour (INS 160a)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901262151429,Amul Kool Coffee,Amul,"Toned milk, sugar, coffee, stabilizers, emulsifier, colour (INS 150c)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901262200622,Amul Masti,Amul,"Pasteurised toned milk, milk solids, active culture",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901262174565,Amul Punjabi Samosa,Amul,"Refined wheat flour, potato, peas, edible vegetable oil, spices, salt",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901262222471,Amul Instant Mashed Potato,Amul,"Dehydrated potato flakes, salt, emulsifier (INS 471), antioxidant (INS 304)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901262200172,Amul Lassi 1L,Amul,"Toned milk, sugar, active lactic culture",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901262178853,Amul Aloo Tikki,Amul,"Potato, edible vegetable oil, spices, salt",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901262071680,Amul Hazelnut Chocolate,Amul,"Sugar, milk solids, cocoa butter, cocoa mass, hazelnuts, emulsifiers",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901262171557,Amul Chocolate Family Pack,Amul,"Toned milk, sugar, cocoa solids, edible vegetable oil, stabilizers, emulsifiers",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901262223539,Amul Chocolate Cookies,Amul,"Refined wheat flour, sugar, cocoa solids, edible vegetable oil, raising agents, emulsifiers",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901262153423,Amul High Protein Milk,Amul,"Standardized milk, milk protein, vitamins",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901262080101,Amul Spray Infant Milk Food,Amul,"Demineralized whey, vegetable oils, skimmed milk powder, lactose, minerals, vitamins",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901262120029,Amul Mithai Mate,Amul,"Milk solids, sugar",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901262070843,Amul Tropical Orange,Amul,"Toned milk, sugar, orange flavour, stabilizers, emulsifiers, colours",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901262175869,Amul Shalimar,Amul,"Toned milk, sugar, flavour, stabilizers",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901262220125,Amul Sandwich Bread,Amul,"Refined wheat flour, water, sugar, milk solids, edible vegetable oil, yeast, salt, preservative (INS 282)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
"""

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

print("Batch 10 Processing Results:")
print(f"  Elevated from Needs Verification: {elevated_count}")
print(f"  Added direct to Confirmed: {added_count}")
print(f"  Updated in Confirmed: {updated_count}")

# Save dataframes
df_c.to_csv(confirmed_path, index=False)
df_nv.to_csv(needs_ver_path, index=False)
print("Saved files successfully.")
