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

# 2. IMPORT BATCH 5 DATA
batch5_csv_data = """barcode,product_name,brands,ingredients_text,sold_in_india_status,ingredient_confidence,status,data_source,source_license,collection_method
8901063139213,Britannia Treat Jim Jam,Britannia,"Refined wheat flour, sugar, edible vegetable oil (palm), invert syrup, raising agents (INS 503(ii), INS 500(ii)), salt, emulsifier (INS 322), artificial vanilla flavour, colours (INS 122, INS 110)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063139374,Britannia Bourbon 200g,Britannia,"Refined wheat flour, sugar, edible vegetable oil (palm), cocoa solids, invert syrup, raising agents (INS 503(ii), INS 500(ii)), salt, emulsifiers (INS 322, INS 471), artificial chocolate flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063028258,Britannia Nice Time,Britannia,"Refined wheat flour, sugar, coconut (12%), edible vegetable oil (palm), invert syrup, raising agents (INS 503(ii), INS 500(ii)), salt, emulsifier (INS 322), artificial coconut flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063012578,Britannia Milk Bikis,Britannia,"Refined wheat flour, sugar, milk solids, edible vegetable oil (palm), invert syrup, raising agents (INS 503(ii), INS 500(ii)), salt, emulsifier (INS 322), artificial vanilla flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063017399,Britannia 50-50 Maska Chaska,Britannia,"Refined wheat flour, sugar, edible vegetable oil (palm), invert syrup, salt, raising agents (INS 503(ii), INS 500(ii)), emulsifier (INS 322), artificial butter flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063014206,Britannia Vita Marie Gold,Britannia,"Refined wheat flour (70%), sugar, refined palm oil, invert sugar syrup, milk solids, raising agents (INS 503(ii), INS 500(ii)), salt, emulsifiers (INS 471, INS 322), added vitamins & minerals",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063138162,Britannia NutriChoice Arrowroot,Britannia,"Whole wheat flour, arrowroot flour, sugar, edible vegetable oil (palm), raising agents, salt, emulsifiers, added vitamins & minerals",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063142817,Britannia NutriChoice Digestive 125g,Britannia,"Whole wheat flour (71%), sugar, edible vegetable oil (palm), raising agents (INS 503(ii), INS 500(ii)), salt, emulsifiers (INS 471, INS 322), added vitamins & minerals",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063029323,Britannia Jim Jam,Britannia,"Refined wheat flour, sugar, edible vegetable oil (palm), invert syrup, raising agents (INS 503(ii), INS 500(ii)), salt, emulsifier (INS 322), artificial vanilla flavour, colours (INS 122, INS 110)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063363960,Britannia Gobbles Chocolate Cake,Britannia,"Refined wheat flour, sugar, eggs, edible vegetable oil (palm), glucose syrup, cocoa solids (3%), raising agents (INS 500(ii), INS 503(ii)), emulsifiers (INS 471, INS 475), preservative (INS 202), artificial chocolate flavour, colour (INS 150c)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063146938,Britannia Winkin Cow Bourbon Shake,Britannia,"Toned milk, sugar, cocoa solids, artificial chocolate flavour, stabilizers (INS 466, INS 407), emulsifier (INS 471), colour (INS 150c)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063146952,Britannia Winkin Cow Strawberry Shake,Britannia,"Toned milk, sugar, strawberry flavour, stabilizers (INS 466, INS 407), emulsifier (INS 471), colour (INS 122)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063092709,Britannia Good Day Cashew,Britannia,"Refined wheat flour, edible vegetable oil (palm), sugar, cashew nuts (4.5%), invert syrup, milk solids, butter (0.6%), raising agents (INS 503(i), INS 500(i)), salt, emulsifier (soya lecithin INS 322)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063094291,Britannia Good Day Pista Badam,Britannia,"Refined wheat flour, edible vegetable oil (palm), sugar, pistachio (3%), almond (2%), invert syrup, milk solids, raising agents (INS 503(i), INS 500(i)), salt, emulsifier (soya lecithin INS 322)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063136779,Britannia Good Day Choco Almond,Britannia,"Refined wheat flour, edible vegetable oil (palm), sugar, cocoa solids, almond (3%), invert syrup, milk solids, raising agents (INS 503(i), INS 500(i)), salt, emulsifier (soya lecithin INS 322)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063342910,Britannia Brown Bread,Britannia,"Whole wheat flour (approx. 50%), refined wheat flour, water, sugar, edible vegetable oil, gluten, yeast, iodized salt, preservative (INS 282), emulsifiers (INS 471, INS 472e)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063343528,Britannia Vitarich Sandwich Bread,Britannia,"Refined wheat flour, water, sugar, edible vegetable oil, gluten, yeast, iodized salt, preservative (INS 282), emulsifiers (INS 471, INS 472e), vitamins",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901719135477,Parle-G Gold,Parle,"Refined wheat flour, sugar, invert syrup, refined palm oil, salt, skimmed milk powder, raising agents (INS 503(ii), INS 500(ii)), emulsifier (INS 471), dough conditioner, artificial vanilla flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901719123801,Parle Monaco Classic,Parle,"Refined wheat flour, edible vegetable oil (palm), salt, sugar, raising agents (INS 503(ii), INS 500(ii)), emulsifier (INS 322), artificial butter flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901719124006,Parle Krackjack,Parle,"Refined wheat flour, sugar, edible vegetable oil (palm), invert syrup, salt, raising agents (INS 503(ii), INS 500(ii)), emulsifier (INS 322), artificial butter flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901719136801,Parle Hide & Seek Milano Creme,Parle,"Refined wheat flour, sugar, edible vegetable oil (palm), cocoa solids, invert syrup, milk solids, raising agents (INS 503(ii), INS 500(ii)), emulsifier (INS 322), artificial vanilla flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901719136757,Parle Hide & Seek Finest Choco,Parle,"Refined wheat flour, sugar, edible vegetable oil (palm), cocoa solids (6%), invert syrup, milk solids, raising agents (INS 503(ii), INS 500(ii)), emulsifier (INS 322), artificial chocolate flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901719137846,Parle Milano Vanilla,Parle,"Refined wheat flour, sugar, edible vegetable oil (palm), invert syrup, milk solids, raising agents (INS 503(ii), INS 500(ii)), emulsifier (INS 322), artificial vanilla flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901719126970,Parle 20-20 Cashew Biscuits,Parle,"Refined wheat flour, sugar, edible vegetable oil (palm), cashew nuts (8%), invert syrup, milk solids, raising agents (INS 503(ii), INS 500(ii)), salt, emulsifier (INS 322), artificial vanilla flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901719114038,Parle Fab! Jam,Parle,"Refined wheat flour, sugar, fruit jam (pineapple, apple), edible vegetable oil (palm), invert syrup, raising agents (INS 503(ii), INS 500(ii)), salt, emulsifier (INS 322), colours (INS 110, INS 102)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901719127236,Parle Rusk,Parle,"Refined wheat flour, sugar, edible vegetable oil (palm), invert syrup, milk solids, raising agents (INS 503(ii), INS 500(ii)), salt, emulsifier (INS 322), artificial vanilla flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901719119286,Parle Mango Bite,Parle,"Sugar, glucose syrup, mango pulp, acidity regulator (INS 330), artificial mango flavour, colour (INS 160c)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901719110023,Parle Hide & Seek Centre Filled Cookies,Parle,"Refined wheat flour, sugar, edible vegetable oil (palm), cocoa solids, invert syrup, milk solids, raising agents, emulsifiers, artificial chocolate flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901719506345,Parle Kreams Gold Cardamom,Parle,"Refined wheat flour, sugar, edible vegetable oil (palm), invert syrup, milk solids, cardamom, raising agents, emulsifiers, artificial cardamom flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901719123443,Parle Kismis,Parle,"Refined wheat flour, sugar, raisins, edible vegetable oil (palm), invert syrup, raising agents, emulsifiers, salt",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901725017545,Sunfeast Nice,ITC,"Refined wheat flour, sugar, coconut, edible vegetable oil (palm), invert syrup, raising agents (INS 503(ii), INS 500(ii)), salt, emulsifier (INS 322), artificial coconut flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901725015916,Sunfeast Dark Fantasy Choco Fills,ITC,"Choco crème (sugar, refined palmolein, refined palm oil, cocoa solids), refined wheat flour, sugar, invert syrup, liquid glucose, edible vegetable oil, cocoa solids, milk solids, butter, raising agents (INS 503(ii), INS 500(i)), emulsifiers (INS 322, INS 471), salt",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901725016265,Sunfeast Dark Fantasy Bourbon,ITC,"Refined wheat flour, sugar, edible vegetable oil (palm), cocoa solids, invert syrup, raising agents (INS 503(ii), INS 500(i)), emulsifiers (INS 322, INS 471), salt, artificial chocolate flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901725000622,Sunfeast Mom's Magic Cashew & Almond,ITC,"Refined wheat flour, sugar, edible vegetable oil (palm), cashew nuts, almonds, invert syrup, milk solids, raising agents, emulsifiers",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901725006143,Sunfeast Marie Light,ITC,"Refined wheat flour, sugar, refined palm oil, invert sugar syrup, milk solids, raising agents, salt, emulsifiers",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901725119201,Sunfeast Yippee! Noodles,ITC,"Instant noodles: Refined wheat flour (78.4%), refined palm oil, iodized salt, wheat gluten, thickeners (INS 508, INS 412); Masala: spices, dehydrated vegetables, sugar, salt, flavour enhancers (INS 621, INS 627, INS 631)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901725114022,Sunfeast Yippee! Magic Masala,ITC,"Instant noodles: Refined wheat flour, refined palm oil, iodized salt, wheat gluten, thickeners; Masala: spices, dehydrated vegetables, sugar, salt, flavour enhancers (INS 621)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8909081010033,Bingo Chilli Cheese Baked Puff,ITC,"Refined wheat flour, edible vegetable oil (palm), cheese powder, spices, salt, sugar, flavour enhancers (INS 621), colours (INS 160c), raising agents",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901725013714,Bingo Mad Angles Achaari Masti,ITC,"Corn grits, edible vegetable oil (palmolein), rice grits, gram flour, spices, salt, sugar, flavour enhancers (INS 621, INS 627, INS 631), acidity regulators, colours (INS 160c)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901725004217,Bingo Tedhe Medhe Tomato,ITC,"Corn grits, edible vegetable oil (palmolein), rice grits, gram flour, spices, salt, sugar, tomato powder, flavour enhancers (INS 621, INS 627, INS 631), acidity regulators, colours (INS 160c)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906009079127,Unibic Milk Cookies,Unibic,"Refined wheat flour, sugar, edible vegetable oil (palm), milk solids, invert syrup, raising agents, salt, emulsifiers, artificial vanilla flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906009070902,Unibic Honey Oatmeal,Unibic,"Whole wheat flour, oats, sugar, honey, edible vegetable oil (palm), invert syrup, raising agents, salt, emulsifiers",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906009071602,Unibic Choco Nut,Unibic,"Refined wheat flour, sugar, cocoa solids, edible vegetable oil (palm), invert syrup, raising agents, salt, emulsifiers, artificial chocolate flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906009070520,Unibic Orange Splash Cookies,Unibic,"Refined wheat flour, sugar, edible vegetable oil (palm), orange flavour, invert syrup, raising agents, salt, emulsifiers, colours (INS 110)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906009077314,Unibic Honey Oatmeal Cookies,Unibic,"Whole wheat flour, oats, sugar, honey, edible vegetable oil (palm), invert syrup, raising agents, salt, emulsifiers",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906009073958,Unibic Coconut Cookies,Unibic,"Refined wheat flour, sugar, coconut, edible vegetable oil (palm), invert syrup, raising agents, salt, emulsifiers, artificial coconut flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901928112009,Bisk Farm Nice,Bisk Farm,"Refined wheat flour, sugar, coconut, edible vegetable oil (palm), invert syrup, raising agents, salt, emulsifier, artificial coconut flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901928300741,Bisk Farm Top Gold,Bisk Farm,"Refined wheat flour, sugar, edible vegetable oil (palm), invert syrup, milk solids, raising agents, salt, emulsifiers",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906017862520,Bisk Farm Burst Wafers,Bisk Farm,"Refined wheat flour, sugar, edible vegetable oil (palm), cocoa solids, invert syrup, raising agents, emulsifiers, artificial chocolate flavour, antioxidant (INS 319)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906033742844,McVitie's Digestive Multi 7 Grain,McVitie's,"Whole wheat flour, oats, barley, rye, millet, corn, rice flour, sugar, edible vegetable oil (palm), invert syrup, raising agents, salt, emulsifiers",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906033742851,McVitie's Hobnobs,McVitie's,"Whole wheat flour, oats, sugar, edible vegetable oil (palm), invert syrup, raising agents, salt, emulsifiers",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906033746040,McVitie's Hobnobs Oats Cookies,McVitie's,"Whole wheat flour, oats, sugar, edible vegetable oil (palm), invert syrup, raising agents, salt, emulsifiers",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901725101374,Sunfeast Dark Fantasy Original 75g,ITC,"Choco crème (sugar, refined palmolein, refined palm oil, cocoa solids), refined wheat flour, sugar, invert syrup, liquid glucose, edible vegetable oil, cocoa solids, milk solids, butter, raising agents, emulsifiers, salt",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901725136215,Sunfeast Dark Fantasy BIG Choco Fills,ITC,"Choco crème (sugar, refined palmolein, refined palm oil, cocoa solids), refined wheat flour, sugar, invert syrup, liquid glucose, edible vegetable oil, cocoa solids, milk solids, butter, raising agents, emulsifiers, salt",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063368026,Britannia Gobbles Fruit Cake 55g,Britannia,"Refined wheat flour, sugar, eggs, edible vegetable oil (palm), glucose syrup, mixed fruit peel (2%), raising agents (INS 500(ii), INS 503(ii)), emulsifiers (INS 471, INS 475), preservative (INS 202), artificial flavours, colour (INS 160a)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063325074,Britannia Toastea,Britannia,"Refined wheat flour, sugar, edible vegetable oil (palm), invert syrup, milk solids, raising agents (INS 503(ii), INS 500(ii)), salt, emulsifier (INS 322), artificial vanilla flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904063226372,Haldiram's Veggie And Paneer Momos,Haldiram's,"Refined wheat flour, paneer, vegetables (cabbage, carrot, onion), edible vegetable oil, spices, salt, sugar, soy sauce",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904063281234,Haldiram's Phulka Roti,Haldiram's,"Whole wheat flour, water, edible vegetable oil, salt",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904063254696,Haldiram's Aloo Bhujia,Haldiram's,"Potato flakes & starch, edible vegetable oil (palmolein), gram flour, iodized salt, spices (red chilli, cumin), colour (INS 160c)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904004403770,Haldiram's Moong Dal,Haldiram's,"Moong dal, edible vegetable oil (palmolein), iodized salt, spices (red chilli, black pepper, asafoetida)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904004403534,Haldiram's Tasty Nuts,Haldiram's,"Peanuts, edible vegetable oil (palmolein), iodized salt, spices (red chilli, black pepper)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904063216403,Haldiram's Khatta Meetha,Haldiram's,"Rice flakes, edible vegetable oil (palmolein), sugar, peanuts, sago, iodized salt, spices, raising agents, colours (INS 160c)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904063216168,Haldiram's Bombay Mix,Haldiram's,"Rice flakes, gram flour, edible vegetable oil (palmolein), peanuts, sago, iodized salt, spices, raising agents, colours (INS 160c)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904063230133,Haldiram's Cornflakes Mixture,Haldiram's,"Corn flakes, edible vegetable oil (palmolein), peanuts, sago, iodized salt, spices, sugar, raising agents, colours (INS 160c)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904063203441,Haldiram's Ratlami Mixture,Haldiram's,"Rice flakes, gram flour, edible vegetable oil (palmolein), peanuts, sago, iodized salt, spices (red chilli, cumin, black pepper), raising agents, colours (INS 160c)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904063200570,Haldiram's Chai Puri,Haldiram's,"Refined wheat flour, edible vegetable oil, sugar, salt, spices, raising agents",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904063253262,Haldiram's Boondi,Haldiram's,"Gram flour (besan), edible vegetable oil (palmolein), iodized salt, spices, colours (INS 160c)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904063258410,Haldiram's Yellow Banana Chips,Haldiram's,"Banana, edible vegetable oil (coconut/palmolein), iodized salt",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904063254573,Haldiram's Tea Time Khari,Haldiram's,"Refined wheat flour, edible vegetable oil, salt, raising agents",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904063253415,Haldiram's Roasted Chana Cracker Heeng Jeera,Haldiram's,"Roasted chana, edible vegetable oil (palmolein), iodized salt, spices (asafoetida, cumin, red chilli)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904063254450,Haldiram's Punjabi Tadka,Haldiram's,"Rice flakes, gram flour, edible vegetable oil (palmolein), peanuts, sago, iodized salt, spices (cumin, turmeric, red chilli), raising agents, colours (INS 160c)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906010500344,Balaji Wafers Salted,Balaji,"Potato, edible vegetable oil, salt",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906010500511,Balaji Wafers Chataka Pataka,Balaji,"Potato, edible vegetable oil, spices, salt, sugar, acidity regulators, colours",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906010500047,Balaji Wafers Masala Masti,Balaji,"Potato, edible vegetable oil, spices, salt, sugar, flavour enhancers (INS 621), acidity regulators, colours (INS 160c)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906090571258,Too Yumm Multigrain Chips Chilli Achari,RPSG,"Multigrain blend (oats, corn, wheat, rice, quinoa), edible vegetable oil, spices, salt, sugar, acidity regulators, flavours",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901491003896,Lay's Korean Chilli,PepsiCo,"Potato, edible vegetable oil (palmolein/rice bran), seasoning [sugar, iodized salt, spices & condiments (chilli, garlic, onion), flavour enhancers (INS 621, INS 627, INS 631), acidity regulators (INS 330, INS 296), colours (INS 160c)]",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901491001137,Lay's India's Magic Masala,PepsiCo,"Potato, edible vegetable oil (palmolein/rice bran), seasoning [sugar, iodized salt, spices & condiments (onion, chilli, dried mango powder, coriander, garlic), flavour enhancers (INS 621, INS 627, INS 631), acidity regulators (INS 330, INS 296), anticaking agent (INS 551)]",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901491983211,Lay's Classic Salted,PepsiCo,"Potato, edible vegetable oil (palmolein), salt",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901491103060,Kurkure Hyderabadi Hungama,PepsiCo,"Corn grits, edible vegetable oil (palmolein), rice grits, gram flour, spices, salt, sugar, flavour enhancers (INS 621, INS 627, INS 631), acidity regulators, colours (INS 160c)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901491002301,Kurkure Masala Munch,PepsiCo,"Corn grits, edible vegetable oil (palmolein), rice grits, gram flour, spices, salt, sugar, flavour enhancers (INS 621, INS 627, INS 631), acidity regulators, colours (INS 160c)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901491103282,Cheetos,PepsiCo,"Corn grits, edible vegetable oil (palmolein), cheese seasoning [cheese powder, milk solids, salt, sugar, flavour enhancers (INS 621, INS 627, INS 631), colours (INS 160c, INS 160a)]",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901491000659,Uncle Chipps Spicy Treat,PepsiCo,"Potato, edible vegetable oil, spices, salt, sugar, flavour enhancers (INS 621), acidity regulators",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901512500205,Act II Butter Delite Popcorn,Agro Tech,"Popcorn kernels, edible vegetable oil (palmolein), salt, butter flavour, colour (INS 160a)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901512540102,Act II Classic Salted Popcorn,Agro Tech,"Popcorn kernels, edible vegetable oil, salt",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901512890702,Act II Tortilla Chips,Agro Tech,"Corn flour, edible vegetable oil, salt, spices, flavour enhancers",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906065168599,ITC Aloo Tikki,ITC,"Potato, edible vegetable oil, spices, salt, sugar, raising agents, colours",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901764042508,Thums Up 2L,Coca-Cola,"Carbonated water, sugar, acidity regulator (INS 338), colour (INS 150d), natural & nature-identical flavouring (cola), caffeine",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901764052309,Limca 2L,Coca-Cola,"Carbonated water, sugar, acidity regulators (INS 330, INS 331(i)), stabilizers (INS 414, INS 471), preservative (INS 211), lime-lemon flavouring",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901764372032,Minute Maid Nimbu Masala,Coca-Cola,"Water, sugar, lemon juice concentrate (approx. 3%), salt, acidity regulators (INS 330, INS 331(iii)), spices (cumin, black salt), preservative (INS 211), natural flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8902080003075,Nimbooz (7Up variant),PepsiCo,"Carbonated water, sugar, acidity regulators (INS 330, INS 331(i)), natural lemon-lime flavouring, preservative (INS 211)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8902080011445,Apple Delight,PepsiCo,"Water, apple juice concentrate, sugar, acidity regulator (INS 330), antioxidant (INS 300), natural apple flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8902579103187,Frooti Mango 1.2L,Parle Agro,"Water, mango pulp (12-19%), sugar, acidity regulators (INS 330, INS 331(iii)), antioxidant (INS 300), permitted synthetic food colour (INS 110), artificial mango flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8902579131036,Appy Fizz,Parle Agro,"Carbonated water, sugar, apple juice concentrate, acidity regulators (INS 330, INS 331(iii)), preservative (INS 211), colour (INS 150d), flavouring",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8902579002121,Appy Fizz 500ml,Parle Agro,"Carbonated water, sugar, apple juice concentrate, acidity regulators (INS 330, INS 331(iii)), preservative (INS 211), colour (INS 150d), flavouring",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904132949676,Campa Cola 500ml,Campa,"Carbonated water, sugar, acidity regulator (INS 338), colour (INS 150d), natural & nature-identical flavouring (cola), caffeine",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904132944695,Campa Orange 500ml,Campa,"Carbonated water, sugar, acidity regulators (INS 330, INS 331(iii)), orange juice concentrate (3%), colours (INS 110, INS 102), artificial orange flavour, preservative (INS 211)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904132975552,Campa Soda,Campa,"Carbonated water, salt, acidity regulator (INS 330)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901207096402,Dabur Kachchi Ghani Mustard Oil,Dabur,"Mustard oil (cold-pressed), antioxidant (INS 319)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901888004451,Glucose-D,Dabur,"Dextrose monohydrate, vitamin C, acidity regulator (INS 330), artificial orange flavour, colour (INS 110)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901207019999,Dabur Glucoplus,Dabur,"Dextrose monohydrate, vitamin C, acidity regulator (INS 330), artificial flavour, colour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906080600586,Paper Boat Lychee Drink,Hector Beverages,"Water, sugar, lychee pulp (12%), apple juice concentrate, acidity regulators (INS 330, INS 331(iii)), antioxidant (INS 300), natural flavours",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906080600913,Paper Boat Aamras,Hector Beverages,"Water, mango pulp, sugar, acidity regulators, antioxidants",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906080600914,Paper Boat Jaljeera,Hector Beverages,"Water, sugar, spices, salt, acidity regulators, mint extract",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906080602689,Paper Boat Mixed Fruit Medley,Hector Beverages,"Water, mixed fruit pulp, sugar, acidity regulators, antioxidants, natural flavours",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906080603518,Paper Boat Zero Sparkling Coffee,Hector Beverages,"Carbonated water, coffee extract, natural flavours, acidity regulators, sweeteners",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901725009885,B Natural Guava Fiber,ITC,"Water, guava juice concentrate, sugar, acidity regulator (INS 330), antioxidant (INS 300), natural flavours, added fiber",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901725009854,B Natural Apple Fiber,ITC,"Water, apple juice concentrate, sugar, acidity regulator (INS 330), antioxidant (INS 300), natural flavours, added fiber",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901030825668,Horlicks Classic Malt 500g,HUL,"Malted cereals (66.7%) [barley, wheat flour, wheat, millet], milk solids (14%), sugar, wheat gluten, iodized salt, minerals, vitamins, emulsifier (INS 471)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901030825521,Horlicks Protein Plus Chocolate,HUL,"Milk solids, malted cereals, sugar, cocoa solids, wheat flour, minerals, vitamins, emulsifier (INS 471), artificial chocolate flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901542003035,Complan,HUL,"Milk solids (approx. 52%), sugar, peanut oil, maltodextrin, almonds (0.8%), minerals, vitamins, colours (INS 100(i), INS 160b(ii)), flavouring",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8909106018372,Boost,HUL,"Cereal extract (50%) [barley, wheat, millet], malted barley (21%), sugar, wheat flour, milk solids (6%), minerals, natural colour (INS 150c), vitamins",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901233022574,Bournvita,Mondelez,"Malt extract (wheat/barley), sugar, milk solids, cocoa solids, liquid glucose, minerals (Ca, Fe, Zn, Cu, I), vitamins, emulsifier (INS 322), salt",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901499009043,Kellogg's Chocolate Muesli,Kellogg's,"Whole wheat flakes, oats, sugar, cocoa solids, glucose syrup, salt, vitamins, minerals, emulsifier",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901499008138,Kellogg's Chocos Duet,Kellogg's,"Wheat flour, sugar, cocoa solids, glucose syrup, salt, vitamins, minerals, emulsifier, artificial chocolate flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901491702539,Quaker Oats,PepsiCo,"100% wholegrain rolled oats",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906112662414,True Elements Rolled Oats,True Elements,"100% wholegrain rolled oats",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906112662551,True Elements Pumpkin Seeds,True Elements,"100% pumpkin seeds",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901725008888,Aashirvaad Shudh Chakki Atta,ITC,"100% whole wheat flour (chakki-ground)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901725008895,Aashirvaad Shudh Chakki Atta 10kg,ITC,"100% whole wheat flour (chakki-ground)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901725006679,Aashirvaad Atta with Multigrains,ITC,"Whole wheat flour, oats, barley, millet, corn, rice flour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901725100575,Aashirvaad Atta with Multigrains 5kg,ITC,"Whole wheat flour, oats, barley, millet, corn, rice flour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906007287012,Fortune Everyday Rice Bran Oil,Adani Wilmar,"Rice bran oil, antioxidant (INS 319), vitamins A & D",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906007280280,Fortune Refined Sunflower Oil,Adani Wilmar,"Refined sunflower oil, antioxidant (INS 319), vitamins A & D",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901088034593,Saffola Active Multi-Source Oil,Marico,"Rice bran oil, sunflower oil, antioxidant (INS 319), vitamins A & D",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901088002530,Saffola Tasty Plus,Marico,"Rice bran oil, corn oil, antioxidant (INS 319), vitamins A & D",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901512102904,Sundrop Superlite Sunflower Oil,Agro Tech,"Refined sunflower oil, antioxidant (INS 319), vitamins A & D",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906004620751,Dhara Life Refined Rice Bran Oil,Mother Dairy,"Rice bran oil, antioxidant (INS 319), vitamins A & D",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906010261078,Gold Winner Refined Sunflower Oil,Kaleesuwari,"Refined sunflower oil, antioxidant (INS 319), vitamins A & D",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906035030222,Freedom Refined Sunflower Oil,Freedom,"Refined sunflower oil, antioxidant (INS 319), vitamins A & D",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901207096402,Dabur Kachchi Ghani Mustard Oil,Dabur,"Mustard oil (cold-pressed), antioxidant (INS 319)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906023797014,Gold Drop Sunflower Oil,Gold Drop,"Refined sunflower oil, antioxidant (INS 319), vitamins A & D",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901537074354,Daawat Basmati Rice,LT Foods,"100% basmati rice",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906008813852,Kohinoor Charminar Select Rice,Kohinoor,"100% basmati rice",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901047001611,Kohinoor Exclusive Brown Rice,Kohinoor,"100% brown rice",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901047039232,Kohinoor Rice,Kohinoor,"100% rice",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901161105806,Lal Qilla Whole Grain Brown Basmati Rice,Lal Qilla,"100% whole grain brown basmati rice",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906046142754,Pride Of India White Basmati Rice,Pride Of India,"100% basmati rice",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906005913715,Makhana Roasted Indori Masala Flavour,Aakash,"Makhana (fox nuts), edible vegetable oil, spices, salt, sugar, flavour enhancers",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8908006646128,Mr Makhana Plain,Mr Makhana,"Makhana (fox nuts)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906167241541,Whole Farm Plain Makhana,Whole Farm,"Makhana (fox nuts)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906096323288,Tasty Nuts,Jabsons,"Peanuts, edible vegetable oil, salt, spices",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904067709529,Banana Chips,Jabsons,"Banana, edible vegetable oil (coconut), iodized salt",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904071700031,Masala Banana Chips,Chheda's,"Banana, edible vegetable oil, spices, salt, sugar",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906084416176,Roasted Cashews,M.O.M,"Cashew nuts",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906084416183,Roasted California Almonds,M.O.M,"Almonds",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906120100519,Farmley Black Raisins,Farmley,"Black raisins",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8908017778887,Indian Raisins,Ashapura Agrocomm,"Raisins (kishmish)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904424804270,Happilo Dry Fruit Mix,Happilo,"Almonds, cashews, raisins, pistachios",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906095127269,Wonderland Australian Almonds,Wonderland,"Almonds",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906016010120,Almonds,K.B.B Nuts/Tulsi,"Almond kernels",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8903023002216,Vedaka Whole Cashews,Vedaka,"Whole cashews",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8903023005378,Vedaka Popular Whole Almonds,Vedaka,"Whole almonds",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8903023001608,Vedaka Raw Peanuts Pink,Vedaka,"Raw peanuts",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8903023010099,Vedaka Sunflower Seeds,Vedaka,"Sunflower seeds",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8902901227482,Good Life Almond 1kg,Reliance,"Almonds",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8902901226645,Good Life Jowar 500g,Reliance,"Jowar (sorghum)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8902901225228,Good Life Tadka Mix,Reliance,"Spices, salt, sugar, edible vegetable oil, raising agents",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8902901224719,Good Life B Gram Roasted Chana,Reliance,"Roasted chana (bengal gram)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8902901062281,Good Life Barley,Reliance,"Barley grains",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8902901001709,Good Life Chakki Atta 5kg,Reliance,"100% whole wheat flour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8902901224641,Good Life Masoor Whole 500g,Reliance,"Masoor dal (whole)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8902901033557,Good Life Chana Brown Big 500g,Reliance,"Chana dal (brown)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8902901225891,Good Life Rice Flour,Reliance,"Rice flour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8902901028317,Good Life Rice Bran Oil 5L,Reliance,"Rice bran oil, antioxidant (INS 319), vitamins A & D",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904132942349,Good Life Sharbati Wheat 10kg,Reliance,"Sharbati wheat grains",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904132969995,Good Life HMT Kolam Rice 26kg,Reliance,"HMT Kolam rice",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904132944343,Good Life Toor Arhar Dal 5kg,Reliance,"Toor dal (arhar)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
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
8901192109125,Catch Whole Cumin,Catch,"100% whole cumin",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901440023067,Eastern Chilli Powder,Eastern,"100% red chilli powder",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901440031017,Eastern Mango Pickle,Eastern,"Raw mango, edible vegetable oil, salt, spices, acidity regulator",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901662031055,Suhana Veg Kolhapuri,Suhana,"Spices, salt, sugar, edible vegetable oil, coconut, garlic, ginger",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901662033509,Suhana Super Garam Masala,Suhana,"Coriander, cumin, black pepper, cloves, cinnamon, cardamom, bay leaf, nutmeg, mace",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906002081585,Sakthi Masala Chicken 500g,Sakthi,"Coriander, cumin, turmeric, red chilli, black pepper, cloves, cinnamon, cardamom, garlic, ginger",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904209303387,Aachi Garlic Tomato Thokku,Aachi,"Tomato, garlic, edible vegetable oil, salt, spices, acidity regulator, preservative",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901030831706,Kissan Mixed Fruit Jam,HUL,"Sugar, mixed fruit pulp blend (approx. 46%) [banana, apple, pineapple, orange, mango, papaya], acidity regulator (INS 330), preservative (INS 211 sodium benzoate), permitted synthetic food colour (INS 122)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901030831720,Kissan Mixed Fruit Jam 700g,HUL,"Sugar, mixed fruit pulp blend (approx. 46%), acidity regulator (INS 330), preservative (INS 211), permitted synthetic food colour (INS 122)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901030850400,Kissan Mixed Fruit Jam 500g,HUL,"Sugar, mixed fruit pulp blend (approx. 46%), acidity regulator (INS 330), preservative (INS 211), permitted synthetic food colour (INS 122)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901058016222,Maggi Rich Tomato Ketchup,Nestlé,"Tomato paste, sugar, water, vinegar, salt, spices (onion, garlic, chilli), acidity regulator (INS 260), preservative (INS 211)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906069402774,Veeba Mayonnaise Eggless,Veeba,"Refined soybean oil, water, sugar, vinegar, iodized salt, thickener (INS 1422), preservative (INS 211), mustard, antioxidant (INS 319)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906069400527,Veeba Sandwich Spread,Veeba,"Refined soybean oil, water, sugar, vinegar, iodized salt, thickener, preservative (INS 211), mustard, antioxidant",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906069400619,Veeba White Pasta Dressing,Veeba,"Refined soybean oil, water, sugar, vinegar, iodized salt, thickener, preservative, herbs, spices",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8908012605003,Heinz Tomato Ketchup,Heinz,"Tomato paste, sugar, vinegar, salt, spices, acidity regulator (INS 260), preservative (INS 211)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901246003621,Del Monte Sliced Green Olives,Del Monte,"Green olives, water, salt, acidity regulator (INS 330)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901595852345,Ching's Secret Chilli Sauce,Capital Foods,"Water, red chilli, garlic, vinegar, salt, sugar, acidity regulator (INS 260), preservative (INS 211)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906006783362,Winn Dark Soya Shandar Sauce,Winn,"Water, soybean extract, salt, sugar, colour (INS 150c), preservative (INS 211)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906002000494,Dr Oetker FunFoods Veg Mayonnaise,Dr. Oetker,"Refined soybean oil, water, sugar, vinegar, iodized salt, thickener (INS 1422), preservative (INS 211), mustard, antioxidant (INS 319)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901808000068,Weikfield Eggless Mayonnaise,Weikfield,"Refined soybean oil, water, sugar, vinegar, iodized salt, thickener, preservative, mustard, antioxidant",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901058901580,Maggi Special Masala Noodles,Nestlé,"Noodles: Refined wheat flour, palm oil, iodized salt, wheat gluten, thickeners (INS 508, INS 412), acidity regulators; Tastemaker: salt, spices (onion, garlic, chilli, coriander, turmeric), sugar, flavour enhancers (INS 621), antioxidant (INS 319)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901058854107,Maggi Oats Masala Noodles,Nestlé,"Oats flour, refined wheat flour, palm oil, iodized salt, wheat gluten, thickeners (INS 508, INS 412), acidity regulators; Tastemaker: salt, spices, sugar, flavour enhancers (INS 621), antioxidant (INS 319)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901058009699,Maggi Atta Noodles,Nestlé,"Whole wheat flour (atta), palm oil, iodized salt, wheat gluten, thickeners (INS 508, INS 412), acidity regulators; Tastemaker: salt, spices, sugar, flavour enhancers (INS 621), antioxidant (INS 319)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901058018493,Maggi 2-Minute Noodles Masala,Nestlé,"Noodles: Refined wheat flour (maida), palm oil, iodized salt, wheat gluten, thickeners (INS 508, INS 412), acidity regulators (INS 501(i), INS 500(i)); Tastemaker: salt, onion, sugar, coriander, chilli, turmeric, garlic, cumin, fenugreek, antioxidant (INS 319)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901058854108,Maggi Atta Noodles Masala,Nestlé,"Whole wheat flour, palm oil, iodized salt, wheat gluten, thickeners, acidity regulators; Tastemaker: salt, spices, sugar, flavour enhancers (INS 621), antioxidant (INS 319)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901741000927,Wai Wai Instant Noodles,Wai Wai,"Refined wheat flour, palm oil, salt, thickeners, acidity regulators; Tastemaker: salt, spices, sugar, flavour enhancers (INS 621), colour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906013032224,Wai Wai X-Press Masala,Wai Wai,"Refined wheat flour, palm oil, salt, masala (spices, sugar, flavour enhancer INS 621)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906013032651,Wai Wai Ready to Eat,Wai Wai,"Refined wheat flour, palm oil, salt, spices, flavour enhancers",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901014000401,Nissin Geki Hot and Spicy,Nissin,"Refined wheat flour, palm oil, salt, thickeners, acidity regulators; Tastemaker: salt, spices, sugar, flavour enhancers (INS 621), colour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901014002054,Nissin Top Ramen Masala,Nissin,"Refined wheat flour, palm oil, salt, thickeners (INS 508, INS 412), acidity regulators; Masala: spices, sugar, salt, flavour enhancer (INS 621)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901014004843,Nissin Cup Noodles Veggie Manchow,Nissin,"Refined wheat flour, palm oil, salt, thickeners, acidity regulators; Tastemaker: salt, spices, sugar, flavour enhancers (INS 621, INS 627, INS 631), colour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901030559266,Knorr Mexican Tomato Corn Soup,HUL,"Tomato powder, corn, sugar, salt, spices, flavour enhancers (INS 621), acidity regulator, colour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901030902352,Knorr Tomato Chatpata Soup,HUL,"Tomato powder, sugar, salt, spices, flavour enhancers (INS 621), acidity regulator, colour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901030900297,Knorr Hong Kong Manchow Soup,HUL,"Corn starch, salt, sugar, spices, flavour enhancers (INS 621), acidity regulator, colour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901030900334,Knorr Chicken Delite Soup,HUL,"Corn starch, salt, sugar, chicken powder, spices, flavour enhancers (INS 621), acidity regulator, colour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901262150095,Amul Gold Milk 200ml,Amul,"Standardized milk (4.5% fat, 8.5% SNF), vitamins A & D",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901262153577,Amul Taaza Toned Milk 200ml,Amul,"Toned milk (3.0% fat, 8.5% SNF), vitamins A & D",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901262200271,Amul Dahi,Amul,"Pasteurized toned milk, active lactic culture",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901262180030,Amul Paneer,Amul,"Milk solids, citric acid (coagulant)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901262020404,Amul Cheese Slices,Amul,"Milk solids, salt, emulsifying salts (INS 331, INS 452), preservative (INS 200), colour (INS 160a)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901262020091,Amul Cheese Cubes,Amul,"Milk solids, salt, emulsifying salts (INS 331, INS 452), preservative (INS 200)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901262010436,Amul White Unsalted Butter,Amul,"Pasteurized milk cream",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901262222471,Amul Instant Mashed Potato,Amul,"Dehydrated potato flakes, salt, emulsifier (INS 471), antioxidant (INS 304)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901262200868,Amul Misthi Doi,Amul,"Pasteurized milk, sugar, active lactic culture",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901262152235,Amul Kool Rose,Amul,"Toned milk, sugar, rose flavour, stabilizers, emulsifiers, colour (INS 122)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901648000860,Mother Dairy Chocolate Flavoured Milk,Mother Dairy,"Toned milk, sugar, cocoa solids, artificial chocolate flavour, stabilizers, emulsifiers, colours (INS 122, INS 127)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901648005551,Mother Dairy Maha Cola,Mother Dairy,"Carbonated water, sugar, acidity regulator (INS 338), colour (INS 150d), natural cola flavour, caffeine",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901648018186,Mother Dairy Classic Dahi,Mother Dairy,"Pasteurized toned milk, active lactic culture",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904383302336,Milky Mist Greek Yogurt,MilkyMist,"Pasteurized milk, active lactic culture",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904083300670,Milky Mist Cooking Butter Unsalted,MilkyMist,"Pasteurized milk cream",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904083301547,Milky Mist Sweetened Condensed Milk,MilkyMist,"Milk solids, sugar",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904083305072,Milky Mist Cooking Butter Salted,MilkyMist,"Pasteurized milk cream, salt",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901777965184,Vadilal Classic Malai Kulfi,Vadilal,"Toned milk, sugar, milk fat, cardamom, stabilizers (INS 410, INS 412, INS 466), emulsifier (INS 471)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901777950173,Vadilal Ice Cream Belgian Chocolate,Vadilal,"Toned milk, sugar, cocoa solids, edible vegetable oil, stabilizers, emulsifiers, artificial chocolate flavour, colour (INS 124)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901777960042,Vadilal Bomber,Vadilal,"Toned milk, sugar, edible vegetable oil, stabilizers, emulsifiers, colours",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901777596104,Vadilal Mysore Pak,Vadilal,"Gram flour (besan), sugar, ghee (milk fat), cardamom",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901777136065,Vadilal Aloo Tikki Kathi Roll,Vadilal,"Refined wheat flour, potato, edible vegetable oil, spices, salt",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901030891830,Kwality Wall's Cornetto Strawberry,HUL,"Milk solids, sugar, edible vegetable oil (palm kernel), strawberry flavour, wheat flour (cone), emulsifiers (INS 471, INS 322), stabilizers (INS 410, INS 412, INS 407), colours (INS 122, INS 160a)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901030891831,Kwality Wall's Feast,HUL,"Milk solids, sugar, edible vegetable oil, cocoa solids, emulsifiers (INS 471, INS 322), stabilizers (INS 410, INS 412), colours (INS 150d)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8909106048928,Kwality Wall's Chocolate Ice Cream,HUL,"Toned milk, sugar, cocoa solids, edible vegetable oil, stabilizers, emulsifiers, colours (INS 122)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901030735349,Kwality Wall's Fruit & Nut,HUL,"Toned milk, sugar, edible vegetable oil, dried fruits, nuts, stabilizers, emulsifiers, colours (INS 122, INS 143)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904052503804,Dinshaw's Butterscotch Ice Cream,Dinshaw's,"Toned milk, sugar, edible vegetable oil, butterscotch flavour, stabilizers, emulsifiers, colours (INS 122)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904089325943,Havmor Zulubar Dark Crunch,Havmor,"Toned milk, sugar, cocoa solids, edible vegetable oil, stabilizers, emulsifiers, colours (INS 122)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901030882609,Brooke Bond Red Label 1kg,HUL,"100% black tea (CTC dust & fannings blend)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901030251504,Brooke Bond Taj Mahal Tea,HUL,"100% black tea (CTC blend)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901030624247,Brooke Bond Taj Mahal Tea 500g,HUL,"100% black tea (CTC blend)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901030681547,Brooke Bond Taj Mahal Tea Bags,HUL,"100% black tea (CTC blend)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901030918810,Brooke Bond Taaza Tea,HUL,"100% black tea (CTC blend)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901030373930,Bru Gold Instant Coffee,HUL,"100% instant coffee (freeze-dried)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901058016055,Nescafé Classic,Nestlé,"100% instant coffee",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901058896381,Nescafé Sunrise Coffee 200g,Nestlé,"Instant coffee, chicory",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901058865660,Nescafé Gold Cappuccino,Nestlé,"Instant coffee, sugar, milk solids, glucose syrup, hydrogenated vegetable oil (palm kernel), salt, stabilizers (INS 340(ii), INS 452(i)), emulsifier (INS 471), anticaking agent (INS 551)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901052004393,Tata Tea Gold,Tata Consumer,"100% black tea (CTC blend)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901052003389,Tata Kannan Devan Tea,Tata Consumer,"100% black tea (CTC blend)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901052034574,Tata Agni Tea 1kg,Tata Consumer,"100% black tea (CTC blend)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901052010295,Tata Salt Iodised,Tata Consumer,"Vacuum evaporated iodised salt, anticaking agent (INS 536)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904043906584,Tata Sampann Chia Seeds,Tata Consumer,"100% chia seeds",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904043926216,Tata Sampann Unpolished Toor Dal,Tata Consumer,"Unpolished toor dal",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901233034300,Cadbury Dairy Milk Silk Bubbly,Mondelez,"Sugar, milk solids, cocoa butter, cocoa mass, emulsifiers (soya lecithin INS 322, INS 476), flavours",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901233034263,Cadbury Dairy Milk Roast Almond,Mondelez,"Sugar, milk solids, cocoa butter, cocoa mass, almonds (15%), emulsifiers (INS 322, INS 476), flavours",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901233033563,Cadbury Dairy Milk Silk Minis,Mondelez,"Sugar, milk solids, cocoa butter, cocoa mass, emulsifiers (INS 322, INS 476), flavours",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901233013091,Cadbury Oreo Small Pack,Mondelez,"Refined wheat flour, sugar, refined palm oil, cocoa solids (5%), invert syrup, raising agents (INS 503(ii), INS 500(i)), salt, emulsifier (INS 322), artificial vanilla flavour, antioxidant (INS 319)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8902433030109,Snickers Bar,Mars,"Milk chocolate (sugar, cocoa butter, milk solids, cocoa mass, emulsifiers), peanuts, glucose syrup, sugar, palm oil, milk solids, salt, emulsifier, flavouring",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901393019964,Center Fresh Soft Chews,Perfetti,"Sugar, glucose syrup, edible vegetable oil, artificial flavours, colours",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901393026146,Chupa Chups Rockats,Perfetti,"Sugar, glucose syrup, artificial flavours, colours",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906130900116,Orion Choco Pie,Orion,"Refined wheat flour, sugar, glucose syrup, cocoa solids, edible vegetable oil, milk solids, emulsifiers, raising agents, artificial chocolate flavour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901042955100,MTR Mango Thokku,MTR,"Raw mango, salt, red chilli, edible vegetable oil, mustard, fenugreek",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901042956732,MTR Jeera Rice,MTR,"Basmati rice, cumin, edible vegetable oil, salt",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901042962542,MTR Vermicelli Seviyan,MTR,"Durum wheat semolina",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901042957074,MTR Rava Idli Mix,MTR,"Semolina (rava), salt, spices, raising agents",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901042955308,MTR Upma Mix,MTR,"Semolina (rava), salt, spices, dehydrated vegetables",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901155104211,Gits Medu Vada Mix,Gits,"Urad dal flour, salt, spices, raising agents",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901155106550,Gits Khatta Dhokla Mix,Gits,"Semolina, gram flour, sugar, tamarind, salt, spices, raising agents",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901552007689,Ashoka Kantola,Ashoka,"Refined wheat flour, potato, edible vegetable oil, spices, salt",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901552023719,Ashoka Jumbo Punjabi Samosa,Ashoka,"Refined wheat flour, potato, peas, edible vegetable oil, spices, salt",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901552013352,Ashoka Tandoori Roti,Ashoka,"Whole wheat flour, water, salt",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901552013550,Ashoka Paneer Bhurji Kathi Roll,Ashoka,"Refined wheat flour, paneer, edible vegetable oil, spices, salt",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901552001007,Ashoka Date And Tamarind Chutney,Ashoka,"Dates, tamarind, sugar, salt, spices",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901552018920,Ashoka Punjabi Pachranga Pickle,Ashoka,"Mixed vegetables, edible vegetable oil, salt, spices, acidity regulator",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906005503305,Bikaji Paneer Schezwan Kathi Roll,Bikaji,"Refined wheat flour, paneer, edible vegetable oil, spices, salt, schezwan sauce",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906005503596,Bikaji Paneer Tikka Kathi Roll,Bikaji,"Refined wheat flour, paneer, edible vegetable oil, spices, salt",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901414002555,Bikano Boondi,Bikano,"Gram flour (besan), edible vegetable oil, iodized salt, spices",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901414037465,Bikano Kaju Pista Cookies,Bikano,"Refined wheat flour, sugar, edible vegetable oil, cashew nuts, pistachios, invert syrup, raising agents, emulsifiers",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901414043930,Bikano Chole Curry,Bikano,"Chickpeas, water, tomato, onion, spices, salt, edible vegetable oil",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8908003115818,Karachi Bakery Osmania Biscuits,Karachi Bakery,"Refined wheat flour, sugar, edible vegetable oil, milk solids, salt, raising agents, emulsifiers",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904043500041,Modern Milk Bread 200g,Modern,"Refined wheat flour, water, sugar, edible vegetable oil, milk solids, yeast, salt, preservative (INS 282), emulsifiers",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904043553733,Modern Kulcha,Modern,"Refined wheat flour, water, sugar, salt, yeast, edible vegetable oil",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906076133111,The Baker's Dozen Milk Bread,The Baker's Dozen,"Refined wheat flour, water, sugar, milk solids, edible vegetable oil, yeast, salt, preservative, emulsifiers",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906020588233,ID Fresh Food Whole Wheat Paratha,ID Fresh Food,"Whole wheat flour, water, edible vegetable oil, salt",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904063211606,Haldiram's Minute Khana Lachha Paratha,Haldiram's,"Whole wheat flour, water, edible vegetable oil, salt",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904063257383,Haldiram's Minute Khana Shami Kebab Wrap,Haldiram's,"Refined wheat flour, chicken, edible vegetable oil, spices, salt",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904004442830,Haldiram's Minute Khana Palak Paneer,Haldiram's,"Paneer, spinach, edible vegetable oil, spices, salt",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906000610084,McCain Chilli Garlic Potato Bites,McCain,"Potato, edible vegetable oil, spices (chilli, garlic), salt, raising agents",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901688122966,Sumeru French Fries,Sumeru,"Potato, edible vegetable oil",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906000791787,Prasuma Chicken Sausage,Prasuma,"Chicken, spices, salt, sugar, raising agents, preservatives",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906107173642,Prasuma Veg Supreme Pizza Minis,Prasuma,"Refined wheat flour, vegetables, cheese, tomato sauce, edible vegetable oil, spices, salt",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906107173697,Prasuma Pizza Mini,Prasuma,"Refined wheat flour, tomato sauce, cheese, edible vegetable oil, spices, salt",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8908000791015,Meatigo Chicken Ham,Meatigo,"Chicken, salt, spices, preservatives, raising agents",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901963201195,Billar Chicken Breakfast Sausages,Billar,"Chicken, spices, salt, sugar, preservatives",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8907093003739,Tasty Nibbles Sardine Curry,Tasty Nibbles,"Sardines, coconut, spices, salt, edible vegetable oil, water",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906072561017,Meisterwurst Chicken Garlic Krakauer,Meisterwurst,"Chicken, garlic, spices, salt, sugar, preservatives",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901120143733,Sugar Free Gold,Sugar Free,"Aspartame, acesulfame potassium, anticaking agent",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901120143726,Sugar Free Gold No.1,Sugar Free,"Aspartame, acesulfame potassium, anticaking agent",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906149350056,Monkfruit Sweetener,,Monkfruit extract",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8908010900025,Peanut Butter,,Roasted peanuts, salt, sugar, edible vegetable oil",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901058897500,Nestlé Nan Pro 2,Nestlé,"Demineralized whey, vegetable oils, skimmed milk powder, lactose, minerals, vitamins, emulsifier",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901262080101,Amul Spray Infant Milk Food,Amul,"Demineralized whey, vegetable oils, skimmed milk powder, lactose, minerals, vitamins",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906041277260,Tramic 500,Tramic,"Tramadol hydrochloride 500mg",NEEDS_VERIFICATION,INCOMPLETE,FIX,Barcode Registry (No Ingredient Text),Pending Attribution,Barcode Scan
8901302097151,Angizaar H,,Losartan Potassium",NEEDS_VERIFICATION,INCOMPLETE,FIX,Barcode Registry (No Ingredient Text),Pending Attribution,Barcode Scan
8906040911769,Jalapeno Roasted Makhana,Veer,"Makhana (fox nuts), edible vegetable oil, jalapeno seasoning, salt",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8909340000393,Cosmix Plant Protein Indonesian Cacao,Cosmix,"Plant protein blend, cocoa, natural flavours, sweetener",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906082526167,Kapiva Shilajit,Kapiva,"Shilajit extract",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901207001246,Dabur Shilajit,Dabur,"Shilajit extract",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901138834838,Himalaya Chyavanaprasha 500g,Himalaya,"Amla, sugar, honey, ghee, spices, herbs",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901138030018,Himalaya Cystone,Himalaya,"Herbal extract formulation",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901220457778,Triphala Churna,,Amla, Haritaki, Bibhitaki",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904027401203,Baidyanath Bhringarajasava,Baidyanath,"Herbal extract formulation",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906038782746,Kamadudha Rasa with Mouktika,,Herbal formulation",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906010367732,Gulab Jamun 1kg,,Milk solids, sugar, edible vegetable oil, cardamom",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906010367336,GRB Soan Cake,GRB,"Sugar, refined wheat flour, edible vegetable oil, milk solids, cardamom",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906010366919,GRB Ghee,GRB,"Milk solids (pure cow ghee)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906010360054,GRB Ghee 1L,GRB,"Milk solids (pure cow ghee)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906001023456,Gowardhan Swarna Ghee,Gowardhan,"Milk solids (pure cow ghee)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904422700963,Patanjali Kacchi Ghani Mustard Oil,Patanjali,"Mustard oil (cold-pressed)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904109496844,Patanjali Cow Milk,Patanjali,"Cow milk",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906032019787,Patanjali Marie Biscuit,Patanjali,"Refined wheat flour, sugar, edible vegetable oil, invert syrup, milk solids, raising agents, salt, emulsifiers, antioxidant (INS 319)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904422705418,Patanjali Doodh Biscuit,Patanjali,"Refined wheat flour, sugar, edible vegetable oil, milk solids, invert syrup, raising agents, salt, emulsifiers",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906029791764,Priyagold Hunk,Priyagold,"Refined wheat flour, sugar, edible vegetable oil, invert syrup, salt, raising agents, emulsifiers",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906020582002,Fresh iD Protein Rich Chapati,Fresh iD,"Whole wheat flour, protein isolate, water, salt",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904043551326,Modern Whole Wheat Chapati,Modern,"Whole wheat flour, water, salt",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906012230119,Vijay Gold Poha Medium,Vijay Gold,"Flattened rice (poha)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906012230010,Vijay Idli Rava,Vijay,"Rice rava (semolina)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906081382894,Telugu Foods Idli Rava,Telugu Foods,"Rice rava (semolina)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906081381729,Telugu Foods Kerala Mixture,Telugu Foods,"Rice flakes, gram flour, edible vegetable oil, peanuts, sago, salt, spices, colours",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906081382429,Telugu Foods Hand Pound Sona Masoori Rice,Telugu Foods,"Sona Masoori rice",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906142010919,Telugu Foods Chia Seeds,Telugu Foods,"100% chia seeds",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906142013972,Swetha Telugu Foods Paneer 65 Wrap,Swetha Telugu Foods,"Refined wheat flour, paneer, edible vegetable oil, spices, salt",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906081382672,Swetha Telugu Foods Mango Avakaya,Swetha Telugu Foods,"Raw mango, salt, red chilli, edible vegetable oil, mustard, fenugreek",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906081380142,Mango Avakaya,,Raw mango, salt, red chilli, edible vegetable oil, mustard, fenugreek",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8903553000409,Ram Bandhu Lime Pickle,Ram Bandhu,"Lime, salt, spices, edible vegetable oil, acidity regulator",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8903553601491,Ram Bandhu Mango Pickle,Ram Bandhu,"Raw mango, salt, spices, edible vegetable oil, acidity regulator",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8903553646461,Ram Bandhu Mix Pickle,Ram Bandhu,"Mixed vegetables, salt, spices, edible vegetable oil, acidity regulator",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904103033014,Swastiks Tomato Pickle,Swastiks,"Tomato, salt, spices, edible vegetable oil, acidity regulator",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901042955117,Tomato Pickle,,Tomato, salt, spices, edible vegetable oil, acidity regulator",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901552007733,Ashoka Stuffed Colocasa,Ashoka,"Colocasia, spices, salt, edible vegetable oil",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901552011631,Muli Paratha,,Whole wheat flour, radish, spices, salt, edible vegetable oil",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906065030186,Jeera Biscuits,,Refined wheat flour, sugar, cumin, edible vegetable oil, salt, raising agents",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906009073248,Choco Hazelnut Cookies,,Refined wheat flour, sugar, cocoa, hazelnuts, edible vegetable oil, raising agents",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906151420075,Lakshminarayan Cornflakes,Lakshminarayan,"Corn flakes, sugar, salt, malt extract",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904113522423,Agro Fresh Corn Flour,Agro Fresh,"Corn flour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904206004317,Spirulina Powder,,Spirulina powder",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8903386501456,Red Mukhwas,,Mixed seeds and spices for mouth freshening",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8903179014873,Trofie,,Durum wheat semolina pasta",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906060910780,VeroBella Spaghetti,VeroBella,"Durum wheat semolina pasta",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906002730124,Instant Khaman Mix,,Gram flour, semolina, salt, spices, raising agents, sugar",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901155144224,Rose Falooda,,Rose syrup, vermicelli, basil seeds, sugar",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901565001698,Tomato Discs,Peppy,"Tomato, salt, spices, acidity regulator, preservative",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906080600937,Paper Boat,Paper Boat,"Water, sugar, natural flavours, acidity regulators",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904063200570,Haldiram's Chai Puri,Haldiram's,"Refined wheat flour, edible vegetable oil, sugar, salt, spices, raising agents",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904064628304,Haldiram's Pois Rond Grillé Salé,Haldiram's,"Roasted peas, edible vegetable oil, salt, spices",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904064628090,Haldiram's Pois Chiche Décortiqué Cassé Grillé,Haldiram's,"Roasted split chickpeas, salt",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904064663596,Annam Upma Rava,Annam,"Semolina (rava)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904064622517,Kalyani Sona Masuri Rice,Kalyani,"Sona Masuri rice",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904064625891,Nandhi Kodo Millet,Nandhi,"Kodo millet",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904064678712,Anupama Rice Karnool Sona Masoori,Anupama Rice,"Sona Masoori rice",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901626364700,Vaahaa White Corn (Cholam),Vaahaa,"White corn grains",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901626364656,Vaahaa Boiled Little Millet (Saamai),Vaahaa,"Boiled little millet",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901626364618,Vaahaa Boiled Kodo Millet (Varagu),Vaahaa,"Boiled kodo millet",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906036846860,Spicelands Motta Karuppan Rice,Spicelands,"Motta Karuppan rice",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906036840929,Spicelands Red Rice Puttu Flour,Spicelands,"Red rice flour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904010630382,Niraa Samba Wheat Puttu Podi,Niraa,"Samba wheat flour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904010698887,Nirapara Oats Puttu,Nirapara,"Oats flour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906008351392,Manna Kodo Millet,Manna,"Kodo millet",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906135071408,Native Food Stores Amla Bites,Native Food Stores,"Amla (Indian gooseberry), sugar",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906046936599,Alo Fruit Juice,Alo,"Water, fruit juice concentrate, sugar, acidity regulator",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906000593417,Basmati Rice,,Basmati rice",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906002080410,Poudre Curry,,Curry powder (coriander, turmeric, cumin, red chilli, fenugreek)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906002081929,Sakthi Egg Kuruma Masala,Sakthi,"Coriander, cumin, turmeric, red chilli, black pepper, cloves, cinnamon, cardamom",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906002082506,Sakthi Ragi Flour,Sakthi,"Ragi (finger millet) flour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906042151590,Anil Rice Flour 500g,Anil,"Rice flour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906127700828,TALOD Kantikaka Gota Flour,TALOD,"Gota flour (roasted gram)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904082760178,Uttam Sooji,Uttam,"Semolina (sooji/rava)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8908005116493,Cycle Brand Saykal Chhap Moraayo 500g,Cycle Brand,"Sago (sabudana)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8908003974255,Tantea Masala Tea Bags,Tantea,"Black tea, spices",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8908000339361,Karak Tea Instant Premix,Karak Tea,"Tea extract, sugar, milk solids, spices, emulsifier",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8908000339873,Karak Tea Instant Remix,Karak Tea,"Tea extract, sugar, milk solids, spices, emulsifier",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904405857424,Jawhar White Vinegar,Jawhar,"White vinegar (acetic acid, water)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904355402828,Apollo Apple Cider Vinegar 500ml,Apollo,"Apple cider vinegar",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906093217047,Zoff Tamarind Whole,Zoff,"Tamarind",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906090832137,Grace Bay Leaves,Grace,"Bay leaves",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8902434121219,Sujal Gum,Sujal,"Chewing gum base, sugar, glucose syrup, flavours",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904293703414,Tomato Desi Local,,Tomato",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8909081009396,Sunfeast Marie,Sunfeast,"Refined wheat flour, sugar, refined palm oil, invert sugar syrup, milk solids, raising agents, salt, emulsifiers",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906084415353,Roasted Makhana,MOM,"Makhana (fox nuts)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8908011305065,Tree Foods Raw Organic Cacao Powder,Tree Foods,"Raw organic cacao powder",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904445900616,Highland Farms A2 Unsalted Yellow Butter,Highland Farms,"A2 milk cream (unsalted butter)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906122501222,GM Foods Chana Sattu,GM Foods,"Roasted gram flour (chana sattu)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8908000845435,Swissyum Masala Muri,Swissyum,"Rice flakes, spices, salt, sugar, edible vegetable oil",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8908003398020,Pro Plant Tofu,Pro Plant,"Soybean, water, coagulant",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906167245709,Whole Farm Bajra Flour,Whole Farm,"Bajra (pearl millet) flour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906167243538,Whole Farm Chana Sattu,Whole Farm,"Roasted gram flour (chana sattu)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904083300670,Milky Mist Cooking Butter Unsalted,Milky Mist,"Pasteurized milk cream",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906069404549,Veeba Sauce,Veeba,"Refined soybean oil, water, sugar, vinegar, salt, thickener, preservative",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906033530021,Snapin Chili Flakes,Snapin,"Dried red chilli flakes",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904104729206,JK Urad Bori,JK,"Urad dal bori (sun-dried)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906025370666,Mirgunde,Soham,"Mirgunde (traditional snack)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901721000510,Tok Jhal Misti 400g,,Traditional Bengali sweet",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901721004266,Prabhuji Dry Gujia,Prabhuji,"Refined wheat flour, khoya, sugar, dry fruits, edible vegetable oil",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901017000408,Pani Puri Masala,,Spices, salt, sugar, acidity regulator",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901882000763,Chillies,,Red chillies",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904214502270,Nylon Sev,,Gram flour, edible vegetable oil, salt, spices",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8908024057128,Eat Better Vanilla Chocolate Laddoos,Eat Better,"Milk solids, sugar, cocoa, vanilla, ghee",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906111441256,Raasa Royal Black Lentils,Raasa,"Black lentils (urad dal)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906000210208,Sujata Ragi Flour,Sujata,"Ragi (finger millet) flour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8908007323264,Fries,,Potato, edible vegetable oil, salt",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8908002768015,SD Shahi Paneer Masala,SD,"Coriander, cumin, turmeric, red chilli, black pepper, cloves, cinnamon, cardamom",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8908009419132,Bauli Moonfils 180g,Bauli,"Refined wheat flour, sugar, eggs, edible vegetable oil, glucose syrup, raising agents, emulsifiers, preservatives, flavours",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906077361094,Makhana Magic Masala,,Makhana, spices, salt, sugar, edible vegetable oil",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906077360097,Jaimin Mini Bhakarwadi,Jaimin,"Refined wheat flour, gram flour, edible vegetable oil, spices, salt, sugar",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906077362114,Jaimin Soya Stick,Jaimin,"Soya flour, edible vegetable oil, spices, salt",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906010504045,Tangg,,Sugar, glucose syrup, artificial flavours, colours",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
89007587,Orbit,Wrigley,"Sorbitol, gum base, mannitol, flavours, sweeteners",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901595853861,Ching's Secret Schezwan Noodles,Capital Foods,"Refined wheat flour, palm oil, salt, schezwan masala (spices, chilli, garlic)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906006783362,Lion Qyno Dates,Lion,"Dates",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906011145247,Medislim,,Weight management supplement",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906064231621,Suhana Cuppa Dal Chawal,Suhana,"Dal, rice, spices, salt, edible vegetable oil",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901662004714,Goda Masala,,Coriander, cumin, coconut, red chilli, black pepper, cloves, cinnamon",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901774002110,Pani Puri Masala,,Spices, salt, sugar, acidity regulator",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906001056706,Poha On The Go,,Flattened rice, spices, salt, sugar",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904083519829,Organic 7 Grain Atta,,Whole wheat, oats, barley, millet, corn, rice, ragi",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8902901224719,Good Life B Gram Roasted Chana,Good Life,"Roasted bengal gram",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8902901030549,Good Life Poppy Seed,Good Life,"Poppy seeds",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901063142657,Nutri Choice Digestive,Nitro Choice,"Whole wheat flour, sugar, edible vegetable oil, raising agents, salt, emulsifiers",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8908018875042,Awe Sourdough Crackers Parmesan And Thyme,Awe,"Whole wheat flour, parmesan cheese, thyme, edible vegetable oil, salt, raising agents",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906090592161,Chef Urbano Sweet Potato Chips,Chef Urbano,"Sweet potato, edible vegetable oil, salt",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906004563133,Diamond 7 Wonders Lentil Crackers,7 Wonders,"Lentil flour, edible vegetable oil, spices, salt",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906050183552,Homefills Ragi Chana Sattu,Homefills,"Ragi flour, roasted gram flour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8904224300378,Food Gate Rice Powder,Food Gate,"Rice flour",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8908012586074,My Kitchen Urad Dal Whole,My Kitchen,"Urad dal (whole)",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906005627155,Mayil Idli/Dosa Rice,Mayil,"Idli/Dosa rice",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8907459000594,Kopiko Cappuccino Candy,Kopiko,"Sugar, glucose syrup, coffee extract, milk solids, flavours",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8906151440240,Konjac Noodles,,Konjac flour, water",CONFIRMED_INDIA_890,HIGH,KEEP,Brand Official Publication,User-submitted,API/CSV Import
8901030953262,Lifebuoy Handwash 1L,HUL,"Water, surfactants, fragrance, preservatives",NON_FOOD,INCOMPLETE,FIX,Barcode Registry (No Ingredient Text),Pending Attribution,Barcode Scan
8901030050114,Pear's Hand Wash,HUL,"Water, surfactants, fragrance, preservatives",NON_FOOD,INCOMPLETE,FIX,Barcode Registry (No Ingredient Text),Pending Attribution,Barcode Scan
8905110008743,Savlon Handwash,Savlon,"Water, surfactants, antiseptic, fragrance",NON_FOOD,INCOMPLETE,FIX,Barcode Registry (No Ingredient Text),Pending Attribution,Barcode Scan
8901725973124,Savlon,Savlon,"Antiseptic liquid",NON_FOOD,INCOMPLETE,FIX,Barcode Registry (No Ingredient Text),Pending Attribution,Barcode Scan
8901207503559,Odomos,Dabur,"Mosquito repellent cream",NON_FOOD,INCOMPLETE,FIX,Barcode Registry (No Ingredient Text),Pending Attribution,Barcode Scan
8901023019906,Godrej Rich Creme Natural Brown,Godrej,"Hair dye",NON_FOOD,INCOMPLETE,FIX,Barcode Registry (No Ingredient Text),Pending Attribution,Barcode Scan
8904352000386,Biotique Face Wash,Biotique,"Face wash",NON_FOOD,INCOMPLETE,FIX,Barcode Registry (No Ingredient Text),Pending Attribution,Barcode Scan
8901548147177,Everyuth Peel Off Mask,Everyuth,"Face mask",NON_FOOD,INCOMPLETE,FIX,Barcode Registry (No Ingredient Text),Pending Attribution,Barcode Scan
8906002485475,Chappi,,Pet food",NON_FOOD,INCOMPLETE,FIX,Barcode Registry (No Ingredient Text),Pending Attribution,Barcode Scan
8908009149138,Pet Safa,,Pet food",NON_FOOD,INCOMPLETE,FIX,Barcode Registry (No Ingredient Text),Pending Attribution,Barcode Scan
8901138819729,Himalaya Baby Gift Pack,Himalaya,"Baby care products",NON_FOOD,INCOMPLETE,FIX,Barcode Registry (No Ingredient Text),Pending Attribution,Barcode Scan
8906041277260,Tramic 500,Tramic,"Tramadol hydrochloride 500mg",NEEDS_VERIFICATION,INCOMPLETE,FIX,Barcode Registry (No Ingredient Text),Pending Attribution,Barcode Scan
8901302097151,Angizaar H,,Losartan Potassium",NEEDS_VERIFICATION,INCOMPLETE,FIX,Barcode Registry (No Ingredient Text),Pending Attribution,Barcode Scan
"""

reader = csv.DictReader(io.StringIO(batch5_csv_data.strip()))
batch5_rows = [r for r in reader]

print(f"Parsed {len(batch5_rows)} products from batch 5 request.")

purged_count = 0
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
    status = row['status'].strip()
    sold_status = row['sold_in_india_status'].strip()
    
    # Check if non-food or pharmaceutical
    is_non_food = status == "NON_FOOD" or "medicine" in p_name.lower() or "face wash" in ing.lower() or "hair dye" in ing.lower() or "mosquito repellent" in ing.lower() or "pet food" in ing.lower() or "baby care" in ing.lower() or "tramadol" in ing.lower() or "losartan" in ing.lower()
    
    if is_non_food:
        # Move to removed list
        new_rem_row = {
            'barcode': bc,
            'product_name': p_name,
            'brands': brand,
            'ingredients_text': ing,
            'reason': f"Non-food item / medical product in Batch 5 import request: {p_name}"
        }
        df_rem = pd.concat([df_rem, pd.DataFrame([new_rem_row])], ignore_index=True)
        # Delete from confirmed/needs_verification if there
        df_c = df_c[df_c['barcode'] != bc]
        df_nv = df_nv[df_nv['barcode'] != bc]
        purged_count += 1
        continue

    # Otherwise process keep
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

print(f"Batch 5 Processing Results:")
print(f"  Purged/Removed: {purged_count}")
print(f"  Elevated from Needs Verification: {elevated_count}")
print(f"  Added direct to Confirmed: {added_direct_count}")
print(f"  Updated in Confirmed: {updated_c_count}")

# Save datasets back
df_c.to_csv(confirmed_path, index=False)
df_nv.to_csv(needs_ver_path, index=False)
df_rem.to_csv(removed_path, index=False)

print("\nSaved files successfully.")
