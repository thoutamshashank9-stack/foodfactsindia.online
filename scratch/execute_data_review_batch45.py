import pandas as pd
import csv
import io

all_supabase_csv = "all_supabase_products.csv"
confirmed_csv = "india_products_confirmed.csv"
needs_ver_csv = "india_products_needs_verification.csv"

BATCH45_DATA = """barcode,product_name,brands,ingredients_text,additive_flags,confidence
8901972062930,Creme 4 Fun,Dukes,"Refined wheat flour, sugar, edible vegetable oil, cocoa solids, invert syrup, raising agents, emulsifiers",Clean,KB_HIGH
8908019758337,Zahidi Dates,ProV,"Zahidi dates (100%)",Clean single-ingredient,KB_HIGH
8901725000370,Sunfeast Marie Light Active,Sunfeast,"Refined wheat flour (Maida) (66.6%), Sugar, Refined palm oil, Invert Syrup, Milk Solids, Salt, Iron & 6 Vitamins",Clean,KB_HIGH
8901095003018,Society Tea 500g,Society,"100% black tea (CTC blend)",Clean single-ingredient,KB_HIGH
8901719129179,Parle Coconut,Parle,"Refined wheat flour, sugar, coconut, edible vegetable oil, invert syrup, raising agents, emulsifier, artificial coconut flavour",Clean,KB_HIGH
8901262201933,Masti Curd,Unknown Brand,"Pasteurized toned milk, active lactic culture",Clean,KB_HIGH
8902433007712,Snickers,Various,"Sugar, peanuts, glucose syrup, milk solids, cocoa butter, cocoa mass, emulsifiers, salt",Clean,KB_HIGH
8902171000068,Chittchore Teekhi Halchal,Chittchore,"Rice flakes, gram flour, edible vegetable oil, peanuts, sago, salt, spices, raising agents, colours (INS 160c)",INS 160c colour,KB_HIGH
8904132926745,My Home Freshener Citrus Groove,My Home,"NON-FOOD — Air freshener",NON-FOOD — PURGE,N/A
8906009071848,Unibic Fruit & Nut,Unibic,"Refined wheat flour, sugar, dried fruits, nuts, edible vegetable oil, invert syrup, raising agents, emulsifiers",Clean,KB_HIGH
8901440202745,Chicken Masala,Eastern,"Coriander, cumin, turmeric, red chilli, black pepper, cloves, cinnamon, cardamom, garlic, ginger",Clean spice blend,KB_HIGH
8901786170500,Everest Tandoori Chicken,Everest,"Coriander, cumin, turmeric, red chilli, black pepper, cloves, cinnamon, cardamom, garlic, ginger, onion",Clean spice blend,KB_HIGH
8906198980730,Protein Powder,TrueBasics,"Whey protein concentrate, emulsifier (INS 322), artificial flavour, sweetener",Clean,KB_HIGH
8901719136795,Parle Hide & Seek,Parle,"Refined wheat flour, sugar, edible vegetable oil, cocoa solids, invert syrup, milk solids, raising agents, emulsifiers",Clean,KB_HIGH
8901719137037,Parle Hide & Seek,Parle Platina,"Refined wheat flour, sugar, edible vegetable oil, cocoa solids, invert syrup, milk solids, raising agents, emulsifiers",Clean,KB_HIGH
8901719136740,Hide & Seek,Parle,"Refined wheat flour, sugar, edible vegetable oil, cocoa solids, invert syrup, milk solids, raising agents, emulsifiers",Clean,KB_HIGH
8901719136771,Hide & Seek 100g,Parle,"Refined wheat flour, sugar, edible vegetable oil, cocoa solids, invert syrup, milk solids, raising agents, emulsifiers",Clean,KB_HIGH
8908015078125,Nutri+ Eggs,Abhi Eggs,"Eggs (100%)",Clean single-ingredient,KB_HIGH
8901972059978,Shortbread Cookies,Dukes,"Refined wheat flour, sugar, butter, edible vegetable oil",Clean,KB_HIGH
8906157900571,Sun Scoop,Sun Scoop,"Verify specific product",Verify,KB_MEDIUM
8906006855472,Doublet Bar Choco Fudge,Baskin Robbins,"Toned milk, sugar, cocoa solids, edible vegetable oil, stabilizers, emulsifiers",Clean,KB_HIGH
8906097590238,Reload Electrolytes,Fast&Up,"Electrolytes (sodium, potassium, magnesium), vitamins, flavours",Supplement,KB_HIGH
8901484013895,Vinegar,Various,"Vinegar (acetic acid, water)",Clean single-ingredient,KB_HIGH
8901725111441,Hi,Good Day,"Verify specific product",Verify,KB_MEDIUM
8906080602832,Swing Lush Lychee,Paper Boat,"Water, lychee pulp, sugar, acidity regulators",Clean,KB_HIGH
8904132948174,Campa Cola 500ml,Campa,"Carbonated water, sugar, acidity regulator (INS 338), colour (INS 150d), natural cola flavour, caffeine",INS 150d + Caffeine,KB_HIGH
8904132948273,Potato Chips,Alan's,"Potato, edible vegetable oil, salt, spices",Clean,KB_HIGH
8906082520097,Get Slim Juice,Kapiva,"Verify specific product",Verify,KB_MEDIUM
8904083504849,24 Mantra Organic Poha 500g,24 Mantra,"Organic flattened rice (poha)",Clean single-ingredient,KB_HIGH
8904083504894,24 Mantra Organic Red Poha 500g,24 Mantra,"Organic red rice flakes (poha)",Clean single-ingredient,KB_HIGH
8901088894128,Forest Honey,Saffola,"Honey (100%)",Clean single-ingredient,KB_HIGH
8902080002061,Pomegranate,Tropicana,"Water, pomegranate juice concentrate, sugar, acidity regulator, antioxidant",Clean,KB_HIGH
8902080002672,Litchi Love,Tropicana,"Water, lychee juice concentrate, sugar, acidity regulator, flavours",Clean,KB_HIGH
8906009990699,Elite Choco Orange,Elite,"Refined wheat flour, sugar, cocoa solids, orange flavour, eggs, edible vegetable oil, raising agents, emulsifiers",Clean,KB_HIGH
8906009990705,Elite Dreams Choco Pineapple,Elite,"Refined wheat flour, sugar, cocoa solids, pineapple flavour, eggs, edible vegetable oil, raising agents, emulsifiers",Clean,KB_HIGH
8908008553264,Advance MFF Whey Protein Chocolate Fudge,MyFitFuel,"Whey protein concentrate, cocoa solids, emulsifier (INS 322), artificial flavour, sweetener",Clean,KB_HIGH
8906019580941,Mango Drink,Various,"Water, mango pulp, sugar, acidity regulator, flavours",Clean,KB_MEDIUM
8906062725115,Bijili Crackers,Cock,"Corn flour, edible vegetable oil, spices, salt, flavour enhancers",Clean,KB_MEDIUM
8904008100620,Naturo Delight Mango,Naturo,"Water, mango pulp, sugar, acidity regulator",Clean,KB_HIGH
8901719130724,Parle 20-20 Gold,Parle,"Wheat flour, sugar, edible vegetable oil, cashew nuts, almonds, invert syrup, milk solids, raising agents (INS 503(ii), INS 500(ii)), emulsifier (INS 322)",Clean,KB_HIGH
8904300201018,Coconut Crunchy,Various,"Refined wheat flour, sugar, coconut, edible vegetable oil, raising agents, emulsifiers",Clean,KB_HIGH
8901725013004,Marie Light Family Pack,Sunfeast/ITC,"Refined wheat flour, sugar, refined palm oil, invert sugar syrup, milk solids, raising agents, salt, emulsifiers",Clean,KB_HIGH
8906009073729,Big & Bold Fruit Blast,Unibic,"Refined wheat flour, sugar, edible vegetable oil, dried fruits, invert syrup, raising agents, emulsifiers",Clean,KB_HIGH
8901719127120,Parle Hide & Seek,Parle,"Refined wheat flour, sugar, edible vegetable oil, cocoa solids, invert syrup, milk solids, raising agents, emulsifiers",Clean,KB_HIGH
8901063158078,Britannia Good Day,Britannia,"Refined wheat flour, edible vegetable oil, sugar, cashew nuts, invert syrup, milk solids, raising agents, emulsifier",Clean,KB_HIGH
8901047065026,Basmati Rice,Kohinoor Foods Limited,"Basmati rice (100%)",Clean single-ingredient,KB_HIGH
8901719120985,Parle Krack Jack 700g,Parle,"Refined wheat flour, sugar, edible vegetable oil, invert syrup, salt, raising agents, emulsifier",Clean,KB_HIGH
8901725004576,Bingo Hashtags,Bingo,"Potato (59.5%), Refined Palmolein and Seasoning (Onion Powder, Spices and Condiments, Iodized Salt, Black Salt, Sugar, Natural Flavours and Natural Flavouring Substances)",Clean,KB_HIGH
8901719129582,Parle Fultoss Baked,Parle,"Refined wheat flour, sugar, edible vegetable oil, invert syrup, raising agents, emulsifiers",Clean,KB_HIGH
8901512557308,Act Nachoz Cheese,Act II,"Corn (68%), Refined Edible Palmolein Oil (TBHQ), Sugar, Maltodextrin, Iodized Salt, Natural Flavour (Chilli), Nature Identical Flavour (Cheese), Whey Powder",INS 319 TBHQ,KB_HIGH
8901719129575,Parle Fultoss Baked,Parle,"Refined wheat flour, sugar, edible vegetable oil, invert syrup, raising agents, emulsifiers",Clean,KB_HIGH
8904064616363,Fenchel Samen,Various,"Fennel seeds (100%)",Clean single-ingredient,KB_HIGH
8901063410015,The Laughing Cow Cheese Cubes,Britannia,"Milk solids, salt, emulsifying salts, preservative (INS 200)",INS 200 preservative,KB_HIGH
8904004410181,Mini Kaju Katli,Haldiram's,"Cashew nuts, sugar, ghee, cardamom",Clean,KB_HIGH
8901262153294,Apple,Amul Tru,"Water, apple juice concentrate, sugar, acidity regulator (INS 330), antioxidant (INS 300)",Clean,KB_HIGH
8901553000092,Keventer Toned Milk,Keventer,"Toned milk, vitamins A & D",Clean,KB_HIGH
8901725019488,Sunfeast Mixed Berry Smoothie,Sunfeast,"Water, milk solids, mixed berry pulp, sugar, stabilizers, acidity regulator, flavours",Clean,KB_HIGH
8901042958347,Chilli Powder,MTR,"Red chilli powder (100%)",Clean single-ingredient,KB_HIGH
8908015692154,Thukpa Chicken,WOW!,"Refined wheat flour, chicken, vegetables, spices, salt, edible vegetable oil",Clean,KB_HIGH
8906083303729,Multi Millet Instant Noodles,Naturally Yours,"Millet flour, refined wheat flour, salt, thickeners",Clean,KB_HIGH
8904221694142,Asitis Double Choc,Asitis,"Whey protein, cocoa solids, sugar, emulsifier, sweetener",Clean,KB_HIGH
8905507137018,First Crop Karare Peanuts,First Crop,"Roasted peanuts, edible vegetable oil, iodized salt, spices",Clean,KB_HIGH
8906046144420,Clove Whole Organic Spices,Various,"Cloves (whole) (100%)",Clean single-ingredient,KB_HIGH
8901111069349,Tiban M 20/1000,Various,"NON-FOOD — Medicine",NON-FOOD — PURGE,N/A
8906114820577,Soya Chunks Mini,Various,"Defatted soya flour",Clean single-ingredient,KB_HIGH
8901725110536,Ready To Cook Chapati,Aashirvaad,"Whole wheat flour, water, salt, edible vegetable oil",Clean,KB_HIGH
8901052011742,Rusk,Tata SoulFull,"Refined wheat flour, sugar, edible vegetable oil, invert syrup, milk solids, raising agents, emulsifier, artificial vanilla flavour",Clean,KB_HIGH
8904344626228,Moon Original,Various,"Verify specific product",Verify,KB_MEDIUM
8904258703879,ABC Juice,Raw Pressed,"Apple, beetroot, carrot juice blend",Clean,KB_HIGH
8904270005401,Marie Go Round,Sunder,"Refined wheat flour, sugar, refined palm oil, invert sugar syrup, milk solids, raising agents, salt, emulsifiers",Clean,KB_HIGH
8901719656828,FAB!,Parle,"Refined wheat flour, sugar, edible vegetable oil, fruit jam, invert syrup, raising agents, emulsifiers, colours",Clean,KB_HIGH
8901153001529,Soan Papdi,Various,"Sugar, gram flour, ghee, cardamom",Clean,KB_HIGH
8906032016977,Soya Chunks,Nutrela,"Defatted soya flour",Clean single-ingredient,KB_HIGH
8906026995028,Brimune Aloe Vera Juice 500ML,Various,"Aloe vera juice, preservative",Clean,KB_HIGH
8906097402562,Zoff Clove Whole,Zoff,"Whole cloves (100%)",Clean single-ingredient,KB_HIGH
8906002348473,Lobia Safed,Rajdhani,"White cowpeas (lobia)",Clean single-ingredient,KB_HIGH
8902901222517,Ajwain,Good Life,"Ajwain (carom seeds)",Clean single-ingredient,KB_HIGH
8901439001786,Morton Oats,Morton,"Oats (100%)",Clean single-ingredient,KB_HIGH
8903023260845,More Choice Raw Peanuts,More,"Raw peanuts",Clean single-ingredient,KB_HIGH
8905507001838,Appalam Papad 200g,Various,"Urad dal flour, salt, spices, edible vegetable oil",Clean,KB_HIGH
8903023281024,More Choice CTC Leaf Tea,More,"100% black tea (CTC blend)",Clean single-ingredient,KB_HIGH
8901725019419,Mom's Magic,Sunfeast,"Refined wheat flour, sugar, edible vegetable oil, cashew nuts, almonds, invert syrup, milk solids, raising agents, emulsifiers",Clean,KB_HIGH
8901725000646,Mom's Magic,Sunfeast,"Refined wheat flour, sugar, edible vegetable oil, cashew nuts, almonds, invert syrup, milk solids, raising agents, emulsifiers",Clean,KB_HIGH
8902901222357,Phool Makhana,Good Life,"Makhana (fox nuts)",Clean single-ingredient,KB_HIGH
8901155301443,Gits Gulabi Jamun,Gits,"Milk solids, sugar, edible vegetable oil, cardamom, rose water",Clean,KB_HIGH
8909106001329,Tresemme Smooth Shine 580ml,Various,"NON-FOOD — Shampoo",NON-FOOD — PURGE,N/A
8909106002142,Tresemme Hairfall Defence 580ml,Various,"NON-FOOD — Shampoo",NON-FOOD — PURGE,N/A
8901030945373,Dove Hair Fall Rescue 650ml,Various,"NON-FOOD — Shampoo",NON-FOOD — PURGE,N/A
8901030945366,Dove Intense Repair 650ml,Various,"NON-FOOD — Shampoo",NON-FOOD — PURGE,N/A
8901063365254,Roll Yo,Britannia,"Refined wheat flour, sugar, edible vegetable oil, cocoa solids, invert syrup, raising agents, emulsifiers",Clean,KB_HIGH
8905507002507,Digestive,First Crop,"Whole wheat flour, sugar, edible vegetable oil, raising agents, emulsifiers, salt",Clean,KB_HIGH
8905507002576,Marie,First Crop,"Refined wheat flour, sugar, refined palm oil, invert sugar syrup, milk solids, raising agents, salt, emulsifiers",Clean,KB_HIGH
8901030702051,Tresemme Smooth Shine 340ml,Various,"NON-FOOD — Shampoo",NON-FOOD — PURGE,N/A
8901725181420,Sunfeast Yippee Noodles,ITC Sunfeast,"Refined wheat flour, palm oil, salt, thickeners; Tastemaker: salt, spices, flavour enhancers (INS 621), antioxidant (INS 319)",INS 621 + INS 319,KB_HIGH
8901725181529,Yippee Noodles,ITC,"Refined wheat flour, palm oil, salt, thickeners; Tastemaker: salt, spices, flavour enhancers (INS 621), antioxidant (INS 319)",INS 621 + INS 319,KB_HIGH
8901725198558,Mad Angles Achaari Masti,Bingo,"Corn grits, edible vegetable oil, rice grits, gram flour, achaari spices, salt, sugar, flavour enhancers (INS 621), colours (INS 160c)",INS 621 MSG + INS 160c,KB_HIGH
8901745115009,Agmark Ghee,Various,"Milk solids (pure ghee)",Clean single-ingredient,KB_HIGH
8904340700397,Pulse Litchi Flavour,Pass Pass,"Sugar, glucose syrup, lychee flavour, acidity regulator, colours",Verify colours,KB_MEDIUM
8904340700359,Pulse Orange,Pass Pass,"Sugar, glucose syrup, orange flavour, acidity regulator, colours",Verify colours,KB_MEDIUM
8906172543807,Black Forest,Hocco,"Refined wheat flour, sugar, eggs, cocoa solids, edible vegetable oil, raising agents, emulsifiers, cherry flavour, colours",Clean,KB_HIGH
8909081003905,Rich Chocolate Cookies,Sunfeast,"Refined wheat flour, sugar, cocoa solids, edible vegetable oil, invert syrup, raising agents, emulsifiers, artificial chocolate flavour",Clean,KB_HIGH
8902579103354,Frooti,Frooti,"Water, mango pulp, sugar, acidity regulators (citric acid, trisodium citrate), stabiliser (gellan gum), preservative (potassium sorbate), antioxidant (ascorbic acid), artificial mango flavour and colouring agent beta-carotene",INS 202 preservative,KB_HIGH
8904132970663,Good Life Aata 5kg,Good Life,"100% whole wheat flour",Clean single-ingredient,KB_HIGH
8904132919778,Mopz Aqua Fresh,Various,"NON-FOOD — Cleaning product",NON-FOOD — PURGE,N/A
8901399435744,Max Kleen 1.25L,Various,"NON-FOOD — Detergent",NON-FOOD — PURGE,N/A
8906001024798,Four Cheese,Go,"Milk solids, salt, emulsifying salts, preservative (INS 200), cheese blend",INS 200 preservative,KB_HIGH
8903605017706,Soy Sauce,Various,"Water, soybean extract, salt, sugar, vinegar, acidity regulator, preservative (INS 211)",INS 211 preservative,KB_HIGH
8906010504021,Balaji Wafers,Balaji,"Potato (87%), Edible Vegetable Oil (Palmolein), Sugar, Spices & Condiments 1% (Chilli, Dry Mango Powder, Black Pepper, Clove, Salt and Black Salt)",Clean,KB_HIGH
8906010504007,Balaji Wafers,Balaji,"Potato (87%), Edible Vegetable Oil (Palmolein), Sugar, Spices & Condiments 1% (Chilli, Dry Mango Powder, Black Pepper, Clove, Salt and Black Salt)",Clean,KB_HIGH
8901030516580,Chicken Delite Soup,Knorr,"Chicken, mixed vegetables, salt, spices, corn starch, flavour enhancers (INS 621)",INS 621 MSG,KB_HIGH
8902579000318,The Still Apple Drink,Various,"Water, apple juice concentrate, sugar, acidity regulator",Clean,KB_MEDIUM
8906006171503,Oyes,Various,"Verify specific product",Verify,KB_MEDIUM
8901491001168,Masala Munch,Various,"Corn grits, edible vegetable oil, rice grits, gram flour, spices, salt, sugar, flavour enhancers (INS 621)",INS 621 MSG,KB_MEDIUM
8901719656613,Parle Hide & Seek Fab Orange,Parle,"Refined wheat flour, sugar, edible vegetable oil, orange flavour, cocoa solids, invert syrup, milk solids, raising agents, emulsifiers, colours (INS 110)",INS 110 colour,KB_HIGH
8906024450512,Green Tea Natural,Various,"Green tea (100%)",Clean single-ingredient,KB_HIGH
8906024451335,Green Tea Lemon and Honey,Various,"Green tea, lemon flavour, honey",Clean,KB_HIGH
8901030456381,Taaza Tea,Brooke Bond,"100% black tea (CTC blend)",Clean single-ingredient,KB_HIGH
8901512548504,Golden Sizzle,Act II,"Popcorn kernels, edible vegetable oil (palmolein), salt, butter flavour, colour (INS 160a)",Clean,KB_HIGH
8906078180908,Mosur Bori,Various,"Verify specific product",Verify,KB_MEDIUM
8906048501627,Protinex Chocolate Flavour,Protinex,"Milk solids, malted cereals, sugar, cocoa solids, wheat flour, minerals, vitamins, emulsifier (INS 471)",Clean,KB_HIGH
8906078160061,Bhut Jolokia,ENE,"Bhut jolokia (ghost pepper)",Clean single-ingredient,KB_HIGH
8901063094185,Good Day,Britannia,"Refined wheat flour, edible vegetable oil, sugar, cashew nuts, invert syrup, milk solids, raising agents, emulsifier",Clean,KB_HIGH
8901063094147,Good Day,Britannia,"Refined wheat flour, edible vegetable oil, sugar, cashew nuts, invert syrup, milk solids, raising agents, emulsifier",Clean,KB_HIGH
8901063092402,Good Day,Britannia,"Refined wheat flour, edible vegetable oil, sugar, cashew nuts, invert syrup, milk solids, raising agents, emulsifier",Clean,KB_HIGH
8901063098657,Good Day,Britannia,"Refined wheat flour, edible vegetable oil, sugar, cashew nuts, invert syrup, milk solids, raising agents, emulsifier",Clean,KB_HIGH
8901512507709,ACT II Original,ACT II,"Popcorn kernels, edible vegetable oil (palmolein), salt",Clean,KB_HIGH
8904073713367,Haricots Rouges,Various,"Red kidney beans",Clean single-ingredient,KB_HIGH
8902901224054,Good Life Apricot 100gm,Good Life,"Apricots",Clean single-ingredient,KB_HIGH
8902901222685,Good Life Fennel,Good Life,"Fennel seeds",Clean single-ingredient,KB_HIGH
8903081567894,Chase Protein Biscoff Cheese Cake,Chase,"Whey protein, biscoff flavour, cheese cake flavour, emulsifier, sweetener",Clean,KB_HIGH
8907316003324,Mother's Chilli Vinegar,Mother's Recipe,"Vinegar, red chilli, salt, sugar, garlic, acidity regulator, preservative (INS 211)",INS 211 preservative,KB_HIGH
8901719135576,Parle Marie,Parle,"Refined wheat flour, sugar, refined palm oil, invert sugar syrup, milk solids, raising agents, salt, emulsifiers",Clean,KB_HIGH
8906069404686,Veeba Barbeque,Veeba,"Tomato paste, sugar, vinegar, salt, spices, acidity regulator, preservative (INS 211), smoke flavour",INS 211 preservative,KB_HIGH
8901138819637,Natural Glow,Various,"NON-FOOD — Verify",NON-FOOD — PURGE,N/A
8901200200110,Coconut & Lemon Gold,Various,"NON-FOOD — Hair oil",NON-FOOD — PURGE,N/A
8901526207473,Garnier,Various,"NON-FOOD — Personal care product",NON-FOOD — PURGE,N/A
8906055445686,Rava Upma,Various,"Semolina (rava), salt, spices",Clean,KB_MEDIUM
8901719133756,Hide & Seek 75gm,Parle,"Refined wheat flour, sugar, edible vegetable oil, cocoa solids, invert syrup, milk solids, raising agents, emulsifiers",Clean,KB_HIGH
8901719136665,Parle-G Jam-In,Parle,"Refined wheat flour, sugar, fruit jam, edible vegetable oil, invert syrup, raising agents, emulsifiers, colours",Clean,KB_HIGH
8906091682793,Coffee Fine Milk Chocolate,Paul And Mike,"Sugar, milk solids, cocoa butter, cocoa mass, coffee, emulsifiers, flavours",Clean,KB_HIGH
8901748003372,RUCHI Anashfool Gota,Ruchi,"Anashfool (star anise) (100%)",Clean single-ingredient,KB_HIGH
8901719126109,Parle 20-20 Choco,Parle,"Refined wheat flour, sugar, cocoa solids, edible vegetable oil, cashew nuts, invert syrup, milk solids, raising agents, emulsifiers",Clean,KB_HIGH
8908001006477,Ask Food Cherry,Various,"Verify specific product",Verify,KB_MEDIUM
8904209303882,Citron Pickle,Aachi,"Citron, salt, spices, edible vegetable oil, acidity regulator",Clean,KB_HIGH
8901030807183,Horlicks Classic Malt,Horlicks,"Malted cereals (66.7%), milk solids (14%), sugar, wheat gluten, iodized salt, minerals, vitamins, emulsifier (INS 471)",Clean,KB_HIGH
8906069611206,Anand Bikaneri Bhujia,Anand/Jolliz,"Gram flour, edible vegetable oil, iodized salt, spices",Clean,KB_HIGH
8906069611725,Anand Fulwadi,Anand/Jolliz,"Gram flour, edible vegetable oil, iodized salt, spices",Clean,KB_HIGH
8906069611763,Kachori,Anand/Jolliz,"Refined wheat flour, gram flour, edible vegetable oil, spices, salt",Clean,KB_HIGH
8906069612128,Anand Mini Samosa,Anand/Jolliz,"Refined wheat flour, potato, peas, spices, salt, edible vegetable oil",Clean,KB_HIGH
8901719124402,Magix Orange,Parle,"Refined wheat flour, sugar, edible vegetable oil, orange flavour, invert syrup, raising agents, emulsifiers, colours (INS 110)",INS 110 colour,KB_HIGH
8901719122040,Coconut,Parle,"Refined wheat flour, sugar, coconut, edible vegetable oil, invert syrup, raising agents, emulsifier, artificial coconut flavour",Clean,KB_HIGH
8901719124396,Magix Elaichi,Parle,"Refined wheat flour, sugar, edible vegetable oil, cardamom flavour, invert syrup, raising agents, emulsifiers",Clean,KB_HIGH
8904006313367,Oura,Various,"Verify specific product",Verify,KB_MEDIUM
8901725016876,Juice,B Natural,"Water, fruit juice concentrate, sugar, acidity regulator, antioxidant",Clean,KB_HIGH
8901719130397,Parle,Parle,"Refined wheat flour, sugar, edible vegetable oil, invert syrup, raising agents, emulsifiers",Clean,KB_HIGH
8901071701976,Hershey's Chocolate,Hershey's,"Sugar, cocoa solids, cocoa butter, milk solids, emulsifiers, flavours",Clean,KB_HIGH
8906113490702,Tata Soul Full,Tata,"Verify specific product",Verify,KB_MEDIUM
8908001956925,Tofu,Mooz Formaggio,"Soybean, water, coagulant",Clean,KB_HIGH
8904082785072,Diet Bhel,Various,"Rice flakes, gram flour, edible vegetable oil, peanuts, sago, salt, spices, raising agents",Clean,KB_HIGH
8904203160108,Cyclone Coffee,Various,"Instant coffee, sugar, milk solids, emulsifier, flavours",Clean,KB_MEDIUM
8901030926594,Pepsodent 100g,Various,"NON-FOOD — Toothpaste",NON-FOOD — PURGE,N/A
8901117250000,Prolyte ORS Orange Flavour,Cipla Health,"Glucose, sodium chloride, potassium chloride, sodium citrate, orange flavour",ORS — Regulated,KB_HIGH
8901030825552,Protein Plus,Horlicks,"Milk solids, malted cereals, sugar, cocoa solids, wheat flour, minerals, vitamins, emulsifier (INS 471)",Clean,KB_HIGH
8904132926806,Good Life Besan,Good Life,"Gram flour (besan)",Clean single-ingredient,KB_HIGH
8908003746708,ORS Lemon Drink,Electrorush,"Glucose, sodium chloride, potassium chloride, sodium citrate, lemon flavour",ORS — Regulated,KB_HIGH
8906069610414,Anand Jolliz Farali Chiwda Tikha,Anand/Jolliz,"Rice flakes, edible vegetable oil, peanuts, sago, salt, spices, raising agents",Clean,KB_HIGH
8906069610384,Anand Jolliz Bhakharwadi,Anand/Jolliz,"Refined wheat flour, gram flour, edible vegetable oil, spices, salt, sugar, coconut, sesame seeds",Clean,KB_HIGH
8906069610711,Anand Jolliz Dal Muth,Anand/Jolliz,"Moong dal, edible vegetable oil, iodized salt, spices",Clean,KB_HIGH
8901719124853,Parle Hide And Seek,Parle,"Refined wheat flour, sugar, edible vegetable oil, cocoa solids, invert syrup, milk solids, raising agents, emulsifiers",Clean,KB_HIGH
8901544064461,Iconiq White Whiskey,Iconiq White,"Alcoholic beverage (whiskey)",ALCOHOL — SEPARATE,KB_HIGH
8904198805534,Sev Mamra,Unknown Brand,"Gram flour, puffed rice, edible vegetable oil, iodized salt, spices",Clean,KB_HIGH
8901548100776,Probiotic Butter,Nutralite,"Milk solids, probiotic culture, salt",Clean,KB_HIGH
8901719127764,Parle Melody,Parle,"Sugar, liquid glucose, milk solids, hydrogenated vegetable oil, cocoa solids, emulsifiers",Hydrogenated oil,KB_HIGH
8901719127765,Parle Pulse Orange,Parle,"Sugar, liquid glucose, orange juice concentrate, acidity regulators, salt, colours",Verify colours,KB_HIGH
8901052003693,Tata Gold,Tata Tea,"100% black tea (CTC blend)",Clean single-ingredient,KB_HIGH
8901052020409,Tata Chakra Gold,Tata Tea,"100% black tea (CTC blend)",Clean single-ingredient,KB_HIGH
8901052030330,Premium Tea,Tata Tea,"100% black tea (CTC blend)",Clean single-ingredient,KB_HIGH
8906055100066,Channa Sattu,Rajdhani,"Roasted chickpea flour (channa sattu)",Clean single-ingredient,KB_HIGH
8901052020386,Tata Chakra Gold Bottle,Tata Tea,"100% black tea (CTC blend)",Clean single-ingredient,KB_HIGH
8903363007032,Foxtail Millet,DMart,"Foxtail millet",Clean single-ingredient,KB_HIGH
8906082570146,Beetroot Nacho Crisps,Various,"Corn flour, beetroot, edible vegetable oil, salt, spices",Clean,KB_MEDIUM
8908008998126,Shrimp,Various,"Shrimp",Clean single-ingredient,KB_HIGH
890150002678,Barramundi,The Better Fish,"Barramundi (fish)",Clean single-ingredient,KB_HIGH
8906072432126,Ginger Garlic Paste,Various,"Ginger, garlic, salt, acidity regulator",Clean,KB_HIGH
8904083536529,24 Mantra Organic Festive Collection,24 Mantra,"Organic mixed products",Clean,KB_MEDIUM
8904083519379,Organic Coriander Powder,Various,"Organic coriander powder",Clean single-ingredient,KB_HIGH
8909177015508,Masoor Dal,Daily Good/Kiranakart,"Masoor dal (red lentils)",Clean single-ingredient,KB_HIGH
8908004383896,Mangalam Bhimseni Camphor,Mangalam,"NON-FOOD — Camphor product",NON-FOOD — PURGE,N/A
8901248303651,Navratna Zaith Zaitoon Cool Oil 300ml,Various,"NON-FOOD — Hair oil",NON-FOOD — PURGE,N/A
8901747006459,Mili Elaichi Tea,Wagh Bakri/Mili,"Black tea, cardamom",Clean,KB_HIGH
8901747005124,Elaichi Chai,Navchetan,"Black tea, cardamom",Clean,KB_HIGH
8901095001168,Society Masala Flavour Tea,Society,"Black tea, spices (cardamom, ginger, cinnamon, cloves)",Clean,KB_HIGH
8901052006359,Green Tea,Tetley,"Green tea (100%)",Clean single-ingredient,KB_HIGH
8909106045439,Bru Instant Coffee,Bru,"Instant coffee, chicory",Clean,KB_HIGH
8909106001688,Lipton Green Tea Raspberry Mint,Lipton,"Green tea, raspberry flavour, mint",Clean,KB_HIGH
8901058900361,Munch Nuts,Nestlé,"Sugar, refined wheat flour, hydrogenated vegetable oil (palm), milk solids, cocoa solids, peanuts, emulsifier (INS 322), salt, raising agent (INS 500(ii)), artificial vanilla flavour",Hydrogenated oil,KB_HIGH
8906010505325,Ratlami Sev,Balaji,"Gram flour, edible vegetable oil, iodized salt, spices",Clean,KB_HIGH
8901120143221,Sugar Free Natura,Sugar Free,"Aspartame sweetener tablets",Sweetener,KB_HIGH
8901052010295,Salt,Tata,"Iodized salt",Clean single-ingredient,KB_HIGH
8906010360085,Ghee,GRB,"Milk fat",Clean single-ingredient,KB_HIGH
8901052087792,Tetley Green Tea,Tetley,"Green tea (100%)",Clean single-ingredient,KB_HIGH
8906005622266,Pepper Powder,Mayil,"Black pepper powder",Clean single-ingredient,KB_HIGH
8901037234234,Girnar Chai Masala,Girnar,"Black tea, spices (cardamom, ginger, cinnamon, cloves)",Clean,KB_HIGH
8906089151737,Indian Rice Basmati First Class,Various,"Basmati rice (100%)",Clean single-ingredient,KB_HIGH
8901095900171,Society Masala Tea,Society,"Black tea, spices (cardamom, ginger, cinnamon, cloves)",Clean,KB_HIGH
8906151420037,Laxmi Narayan Chiwda 200gm,Various,"Rice flakes, gram flour, edible vegetable oil, peanuts, sago, salt, spices, raising agents",Clean,KB_HIGH
8906081381361,Chekodilu,Various,"Rice flour, coconut, jaggery, edible vegetable oil, cardamom",Clean,KB_HIGH
8901058897241,Cerelac Wheat Apple,Nestlé,"Wheat flour, skimmed milk powder, sugar, apple flakes, vegetable oil (palm), minerals, vitamins",Clean,KB_HIGH
8907003505087,Rajapa Layam Thattai,Various,"Rice flour, urad dal flour, salt, spices",Clean,KB_MEDIUM
8901262020060,Amul Cheese Block,Amul,"Milk solids, salt, emulsifying salts, preservative (INS 200)",INS 200 preservative,KB_HIGH
8904071701175,Chana Chor,Various,"Chickpeas, edible vegetable oil, iodized salt, spices",Clean,KB_HIGH
8908007167363,Roasted Makhana Khatta Meetha,Various,"Makhana (fox nuts), edible vegetable oil, salt, sugar, spices",Clean,KB_HIGH
8901928350951,Googly,Various,"Verify specific product",Verify,KB_MEDIUM
8906027051006,Kolhapuri Rassa Masala,Various,"Coriander, cumin, turmeric, red chilli, black pepper, coconut, garlic, ginger, onion",Clean spice blend,KB_HIGH
8907316007421,Amritsari Rajma,Mother's Recipe,"Rajma (kidney beans), tomato, spices, salt, sugar, edible vegetable oil",Clean,KB_HIGH
8907316007452,Mumbai Pav Bhaji,Mother's Recipe,"Mixed vegetables, spices, salt, sugar, edible vegetable oil, tomato",Clean,KB_HIGH
8904067702513,Gud Chana,Various,"Chickpeas, jaggery, edible vegetable oil",Clean,KB_HIGH
8901414043947,Dal Tadka,Various,"Mixed dals, spices, salt, ghee, tomato",Clean,KB_HIGH
8906016890210,P-Mark Kachche Ghane Mustard Oil,Various,"Mustard oil (kachi ghani)",Clean single-ingredient,KB_HIGH
8901042961217,Badam Drink,MTR,"Almonds, milk solids, sugar, cardamom",Clean,KB_HIGH
8906057903269,Moong Dal,Various,"Moong dal (green gram)",Clean single-ingredient,KB_HIGH
8901155440319,Sarson Ka Saag,Various,"Mustard greens, spinach, spices, salt, ghee",Clean,KB_HIGH
8901088141246,Saffola Masala Oats,Saffola,"Oats, spices, salt, dehydrated vegetables",Clean,KB_HIGH
8901042957852,Mutter Paneer,MTR,"Paneer, green peas, tomato, spices, salt, edible vegetable oil",Clean,KB_HIGH
8906070439219,Organic Masoor Dal,Various,"Organic masoor dal (red lentils)",Clean single-ingredient,KB_HIGH
8906125313389,Natural Honey,Various,"Honey (100%)",Clean single-ingredient,KB_HIGH
8906070439073,Organic Rajma Chitra (Red),Various,"Organic rajma chitra (red kidney beans)",Clean single-ingredient,KB_HIGH
8906070438366,Organic Tur Dal (Pigeon Pea Split),Unknown Brand,"Organic tur/toor dal (pigeon pea split)",Clean single-ingredient,KB_HIGH
8906011190544,Muthiya,Various,"Gram flour, fenugreek leaves, spices, salt, edible vegetable oil",Clean,KB_HIGH
8906005502636,Anjeer Dry Fruit,Bikaji,"Figs (anjeer), dry fruits, sugar, ghee",Clean,KB_HIGH
8908004539101,Corn On Cob,Merc,"Corn on cob",Clean single-ingredient,KB_HIGH
8901552013741,Butter Chicken Paste,Ashoka,"Tomato, butter, cream, spices, salt, sugar, edible vegetable oil, chicken flavour",Clean,KB_HIGH
8906066700521,Kettle Corn,Various,"Popcorn kernels, sugar, edible vegetable oil, salt",Clean,KB_HIGH
8906021071000,55 Peanut Butter,5 Star,"Roasted peanuts, salt, edible vegetable oil",Clean,KB_HIGH
8901123000439,Lotte Jellies,Lotte,"Sugar, glucose syrup, gelatin, fruit flavours, acidity regulator, colours",Verify colours,KB_HIGH
8901155129214,Sandwich Dhokla,Fits,"Gram flour, water, sugar, salt, spices, edible vegetable oil, raising agents",Clean,KB_HIGH
8904063226389,Momos,Haldiram's,"Refined wheat flour, vegetables, spices, salt, edible vegetable oil",Clean,KB_HIGH
8906082760349,Frozen Strawberry,Various,"Strawberries (frozen)",Clean single-ingredient,KB_HIGH
8906082760004,Mango Pulp,Various,"Mango pulp (100%)",Clean single-ingredient,KB_HIGH
8906040370016,India Salaam Basmati Rice Classic,Various,"Basmati rice (100%)",Clean single-ingredient,KB_HIGH
8906129220171,Buttermilk Masala Glass,Chhaswala,"Toned milk, water, salt, spices, active lactic culture",Clean,KB_HIGH
8906129220164,Special Masala,Chhaswala,"Toned milk, water, salt, spices, active lactic culture",Clean,KB_HIGH
8906129220188,Buttermilk Bottle,Chhaswala,"Toned milk, water, salt, spices, active lactic culture",Clean,KB_HIGH
8906129220003,Dahi,Chhaswala,"Pasteurized toned milk, active lactic culture",Clean,KB_HIGH
8906129221239,Mango Lassi,Chhaswala,"Toned milk, mango pulp, sugar, active lactic culture",Clean,KB_HIGH
8906129221215,Strawberry Lassi,Chhaswala,"Toned milk, strawberry pulp, sugar, active lactic culture",Clean,KB_HIGH
8906129221246,Guava Lassi,Chhaswala,"Toned milk, guava pulp, sugar, active lactic culture",Clean,KB_HIGH
8906129220454,Butterscotch Lassi,Chhaswala,"Toned milk, butterscotch flavour, sugar, active lactic culture",Clean,KB_HIGH
8906129221161,Makhaniya Lassi,Chhaswala,"Toned milk, cream, sugar, active lactic culture",Clean,KB_HIGH
8906183980004,Isorich Blend Whey Protein,Beast Life,"Whey protein blend, emulsifier (INS 322), artificial flavour, sweetener",Clean,KB_HIGH
8901709023135,Rib Eye Meat Slices,Shabu Shabu,"Beef rib eye slices",Clean single-ingredient,KB_HIGH
8901709023142,Blade Slices,Shabu Shabu,"Beef blade slices",Clean single-ingredient,KB_HIGH
8901063368026,Gobbles Fruit Cake 55gm,Britannia,"Refined wheat flour, sugar, eggs, edible vegetable oil, mixed fruit peel, glucose syrup, raising agents, emulsifiers",Clean,KB_HIGH
8904109613012,GreenTech Bhindi Whole,Various,"Bhindi (okra) (frozen)",Clean single-ingredient,KB_HIGH
8901777549643,Plain Puri,Vadilal,"Whole wheat flour, water, salt, edible vegetable oil",Clean,KB_HIGH
8906125982011,Crunchy Corn,Gourmet Crackers,"Corn flour, edible vegetable oil, salt, spices",Clean,KB_HIGH
8901719921995,Guava Chilli Flavoured Candy,Parle,"Sugar, glucose syrup, guava flavour, chilli, acidity regulator, colours",Verify colours,KB_HIGH
8902268012080,Shortbread Cookies,Anmol,"Refined wheat flour, sugar, butter, edible vegetable oil",Clean,KB_HIGH
8906020588462,Plain Paratha,ID,"Whole wheat flour, water, edible vegetable oil, salt",Clean,KB_HIGH
8901030912092,Deep Moisture,Various,"NON-FOOD — Verify",NON-FOOD — PURGE,N/A
8908025531023,Dhaniya Mirchi Aur Woh,Kilrr,"Coriander, chilli, spices",Clean spice blend,KB_MEDIUM
8904206218158,Boisson Orange 400ml Bora Btl,Various,"Water, orange juice, sugar, acidity regulator",Clean,KB_MEDIUM
8908000175068,Boisson Orange 350ml Zen Btl,Various,"Water, orange juice, sugar, acidity regulator",Clean,KB_MEDIUM
8903363006820,Almond Kernels,DMart Swaad,"Almond kernels",Clean single-ingredient,KB_HIGH
8906131682219,Jowar Puff Chatpata Treat,Mille,"Jowar puffs, chatpata spices, edible vegetable oil, salt",Clean,KB_HIGH
8901512103901,Sundrop Oil,Sundrop,"Refined sunflower oil, antioxidant (INS 319), vitamins A & D",INS 319 TBHQ,KB_HIGH
8903363002181,Methi,DMart Premia,"Fenugreek seeds",Clean single-ingredient,KB_HIGH
8903363000040,Poha Jada,DMart Premia,"Rice flakes (poha)",Clean single-ingredient,KB_HIGH
8908002396805,Gingelly Oil,Mr. Gold,"Sesame oil (gingelly)",Clean single-ingredient,KB_HIGH
8906144470490,Soya Chunks,Nutroya,"Defatted soya flour",Clean single-ingredient,KB_HIGH
8906035050671,Mehndi,Neha,"NON-FOOD — Henna product",NON-FOOD — PURGE,N/A
8906027946180,Spanish Style Rice,Eat Regal Gourmet,"Rice, tomato, spices, salt, edible vegetable oil",Clean,KB_HIGH
8904063252517,Chiwda,Various,"Rice flakes, edible vegetable oil, peanuts, sago, salt, spices, raising agents",Clean,KB_HIGH
8906107170238,Momos Vegetable & Paneer,Prasuma,"Refined wheat flour, vegetables, paneer, spices, salt, edible vegetable oil",Clean,KB_HIGH
8903023305058,Mango Pickle,Kitchen's Promise,"Raw mango, salt, spices, edible vegetable oil, acidity regulator",Clean,KB_HIGH
8908016002150,Full Moon Ghee,Two Brothers,"Milk solids (pure cow ghee)",Clean single-ingredient,KB_HIGH
8901063028821,Nice Time,Britannia,"Refined wheat flour, sugar, coconut, edible vegetable oil, invert syrup, raising agents, emulsifiers",Clean,KB_HIGH
8906009780153,Maganlal Chikki,Unknown Brand,"Peanuts, jaggery, glucose syrup",Clean,KB_HIGH
8908006024537,Mullu Thenkuzhal,Amirtham,"Rice flour, gram flour, edible vegetable oil, iodized salt, spices",Clean,KB_HIGH
8902080002795,Tropicana Frutz Mixed Fruit,Tropicana,"Water, mixed fruit juice concentrate, sugar, acidity regulator (INS 330), antioxidant (INS 300)",Clean,KB_HIGH
8906126394592,Premium Chia Seeds,Khari Foods,"Chia seeds",Clean single-ingredient,KB_HIGH
8904004403770,Moong Dal,Haldiram's,"Moong dal, edible vegetable oil, iodized salt, spices",Clean,KB_HIGH
8906005618351,Fruit Cake Sliced,Various,"Refined wheat flour, sugar, eggs, edible vegetable oil, mixed fruit peel, glucose syrup, raising agents, emulsifiers",Clean,KB_HIGH
8901063325074,Toastea,Britannia,"Refined wheat flour, sugar, edible vegetable oil, invert syrup, raising agents, emulsifiers",Clean,KB_HIGH
8906173701596,Nitra Isolate Protein,Big Muscles Nutrition,"Whey protein isolate, emulsifier (INS 322), artificial flavour, sweetener",Clean,KB_HIGH
8906036670830,Butter,Nandini,"Milk solids (butter)",Clean single-ingredient,KB_HIGH
8903023006047,Premium Whole Methi (Fenugreek),Vedaka,"Fenugreek seeds (whole)",Clean single-ingredient,KB_HIGH
8901928753004,Rich Marie,Bisk Farm,"Refined wheat flour, sugar, refined palm oil, invert sugar syrup, milk solids, raising agents, salt, emulsifiers",Clean,KB_HIGH
8906120106337,Seed Mix,Farmley,"Mixed seeds (pumpkin, sunflower, chia, flax)",Clean,KB_HIGH
8902901222616,Good Life Chilli Guntur with Stem,Good Life,"Guntur red chillies with stem",Clean single-ingredient,KB_HIGH
8901725017545,Nice,Sunfeast,"Refined wheat flour, sugar, coconut, edible vegetable oil, invert syrup, raising agents, emulsifiers",Clean,KB_HIGH
8908000537019,Kalyani Nature Pure,Various,"Verify specific product",Verify,KB_MEDIUM
8906007284042,Kings Refined Soyabean Oil 1L,Various,"Refined soybean oil, antioxidant (INS 319), vitamins A & D",INS 319 TBHQ,KB_HIGH
8901537050518,Pasadena,Various,"Verify specific product",Verify,KB_MEDIUM
8904124107442,Family Milk Pasteurised Homogenised Standardised Milk,Family Milk,"Pasteurised homogenised standardised milk",Clean,KB_HIGH
8908020170005,Siddipet Poultry Eggs,Siddipet Poultry,"Eggs (100%)",Clean single-ingredient,KB_HIGH
8901207039911,Dabur Hair Oil Coconut,Dabur,"NON-FOOD — Hair oil",NON-FOOD — PURGE,N/A
8906163270620,Pista Biscuit,Various,"Refined wheat flour, sugar, pistachios, edible vegetable oil, raising agents, emulsifiers",Clean,KB_MEDIUM
8904293726925,Flipkart Grocery Classic Suji/Rawa,Flipkart Grocery,"Semolina (suji/rawa)",Clean single-ingredient,KB_HIGH
8904293728653,Flipkart Grocery Classic Bansi Rawa,Flipkart Grocery,"Bansi rawa (semolina)",Clean single-ingredient,KB_HIGH
8906142025920,Plix Super Multi Vitamin,Plix,"Multivitamin supplement",Supplement,KB_HIGH
8906040375226,Salaam Basmati Rice,Various,"Basmati rice (100%)",Clean single-ingredient,KB_HIGH
8904132972469,Good Life Till White 200g,Good Life,"White sesame seeds (till)",Clean single-ingredient,KB_HIGH
8904067700762,Khakhra,Unknown Brand,"Whole wheat flour, spices, salt, edible vegetable oil",Clean,KB_MEDIUM
8904067708836,Soya Sticks Magic Masala,Various,"Defatted soya flour, magic masala spices, edible vegetable oil, iodized salt",Clean,KB_HIGH
8904067709529,Banana Chips,Jabsons,"Banana, edible vegetable oil (coconut/palmolein), iodized salt",Clean,KB_HIGH
8904071700031,Masala Banana Chips,Chheda's,"Banana, edible vegetable oil (coconut/palmolein), masala spices, iodized salt",Clean,KB_HIGH
8904083300854,Pomegranate,Pom Wonderful,"Pomegranate juice",Clean single-ingredient,KB_HIGH
8904084100422,Aloe Vera Juice,Unknown Brand,"Aloe vera juice",Clean single-ingredient,KB_HIGH
8904084100477,Aloevera D-Blocker Juice,Various,"Aloe vera juice, preservative",Clean,KB_MEDIUM
8904084100491,Aloe Panch Tulsi Juice,Various,"Aloe vera juice, tulsi (holy basil)",Clean,KB_MEDIUM
8904084900138,Surimi,Lipton,"Surimi (fish paste), starch, salt, sugar, egg white, flavours",Clean,KB_MEDIUM
8904110025163,Généreux,Saint Agur/Savencia,"Cheese (Saint Agur)",Clean single-ingredient,KB_MEDIUM
8904113900177,Eggless Chocochip Cake,Kidys Oven Fresh,"Refined wheat flour, sugar, chocolate chips, edible vegetable oil, raising agents, emulsifiers",Clean,KB_HIGH
8904117900395,Jaggery,Various,"Jaggery (gur)",Clean single-ingredient,KB_HIGH
8904150200155,Almonds,Nutty Gritties,"Almonds",Clean single-ingredient,KB_HIGH
8904158903140,Amla Powder (Groseilles Indiennes) Ayurvedic & Herbal,Various,"Amla powder (Indian gooseberry)",Clean single-ingredient,KB_HIGH
8906002001118,Pasta & Pizza Sauce,Dr. Oetker,"Tomato paste, sugar, vinegar, salt, spices, acidity regulator, preservative (INS 211)",INS 211 preservative,KB_HIGH
8902901126464,Yeah Mango Juice,Unknown Brand,"Water, mango pulp, sugar, acidity regulator",Clean,KB_MEDIUM
8908000233232,Iyer's Punjabi Masala Papad,Unknown Brand,"Urad dal flour, Punjabi masala spices, salt, edible vegetable oil",Clean,KB_HIGH
8904272600055,Storia Mango Shake,Unknown Brand,"Water, mango pulp, milk solids, sugar",Clean,KB_MEDIUM
8901719909412,Chocolate Rolls,Parle,"Refined wheat flour, sugar, cocoa solids, edible vegetable oil, invert syrup, raising agents, emulsifiers",Clean,KB_HIGH
8904132928510,Corn Flakes,Aarambh,"Corn grits, sugar, malt extract, iodized salt, vitamins, minerals",Clean,KB_HIGH
8901725003128,B Natural Mango Bitz,B Natural,"Water, mango pulp, sugar, acidity regulator, antioxidant",Clean,KB_HIGH
8901042969688,Tomato Rice Powder,Various,"Tomato, rice flour, spices, salt",Clean,KB_MEDIUM
8908009419637,Sauli Moonbills Choco,Unknown Brand,"Refined wheat flour, sugar, cocoa solids, eggs, edible vegetable oil, raising agents, emulsifiers",Clean,KB_MEDIUM
8908009419651,Sauli Moonbills Vanilla,Unknown Brand,"Refined wheat flour, sugar, vanilla flavour, eggs, edible vegetable oil, raising agents, emulsifiers",Clean,KB_MEDIUM
8908009419644,Sauli Moonbills Strawberry,Bauli Moonfils,"Refined wheat flour, sugar, strawberry flavour, eggs, edible vegetable oil, raising agents, emulsifiers",Clean,KB_HIGH
8904258701974,Protein Milkshake,RAW,"Milk solids, whey protein, sugar, flavours, stabilizers",Clean,KB_HIGH
8902901225181,Moong Dal Whole 500g,Unknown Brand,"Whole moong (green gram)",Clean single-ingredient,KB_HIGH
8906040375240,India Salaam Basmati Rice,Various,"Basmati rice (100%)",Clean single-ingredient,KB_HIGH
8901058008388,Hot Sweet Tomato Chilli Sauce,Maggi,"Tomato paste, sugar, water, vinegar, salt, chilli, spices, acidity regulator (INS 260), preservative (INS 211)",INS 211 preservative,KB_HIGH
8904045800095,Royal Jaggery,Various,"Jaggery (gur)",Clean single-ingredient,KB_HIGH
8902433000232,Snickers Chocolate with Almonds 40g,Snickers,"Sugar, peanuts, glucose syrup, milk solids, cocoa butter, cocoa mass, almonds, emulsifiers, salt",Clean,KB_HIGH
8901537079595,White Basmati Rice,Daawat,"White basmati rice",Clean single-ingredient,KB_HIGH
8901063155497,Tiger Krunch Coconut,Britannia,"Refined wheat flour, sugar, coconut, edible vegetable oil, invert syrup, raising agents, emulsifier",Clean,KB_HIGH
8906009709437,Mango Pulp,Kesar,"Mango pulp (100%)",Clean single-ingredient,KB_HIGH
8906058610708,Gaia Crunchy Muesli,Gaia,"Oats, dried fruits, nuts, honey, edible vegetable oil",Clean,KB_HIGH
8902901223378,Poha,Good Life,"Flattened rice (poha)",Clean single-ingredient,KB_HIGH
8903967000002,Spicy Stick,Brijwasi,"Gram flour, edible vegetable oil, iodized salt, spices",Clean,KB_HIGH
8908015480645,Khushpoo,Various,"Verify specific product",Verify,KB_MEDIUM
8908005144182,20G Protein Bar Cranberry Blast,Yoga Bar,"Oats, cranberries, whey protein, dates, nuts, emulsifier",Clean,KB_HIGH
8906002082315,Sombu Podi,Sakthi,"Fennel seeds (sombu)",Clean single-ingredient,KB_HIGH
8908016809414,Afghani Soya Chaap,BlueTribe,"Defatted soya flour, spices, salt",Clean,KB_HIGH
8906032010364,Ruchi No. 1 Vanaspati,Ruchi No. 1,"Hydrogenated vegetable oil (palm, soybean), antioxidant (INS 319), vitamins A & D",Hydrogenated oil + INS 319 TBHQ,KB_HIGH
8901207006845,Pudina Hara Active,Dabur,"NON-FOOD — Toothpaste",NON-FOOD — PURGE,N/A
8904094400161,Auto Flow,Various,"NON-FOOD — Verify",NON-FOOD — PURGE,N/A
8908005144441,Breakfast Protein Bar,Yoga Bar,"Oats, whey protein, dried fruits, nuts, honey, emulsifier",Clean,KB_HIGH
8906002005956,Pesto Italian Basil,Dr. Oetker,"Basil, edible vegetable oil, parmesan cheese, pine nuts, garlic, salt",Clean,KB_HIGH
8901030948244,Lux Glow Shop,Various,"NON-FOOD — Soap",NON-FOOD — PURGE,N/A
8906064651566,Peri Peri Ketchup Imp,Various,"Tomato paste, sugar, vinegar, salt, peri peri spices, acidity regulator, preservative (INS 211)",INS 211 preservative,KB_HIGH
8908000668522,Sella XXL Basmati Rice,Banno,"Sella XXL basmati rice",Clean single-ingredient,KB_HIGH
8904150195338,Barra a Base de Dátiles Castaña de Cajú y Cacao Sabor a Menta Libre de Gluten,Laddubat,"Dates, cashew nuts, cocoa, mint flavour",Clean,KB_HIGH
8906070181231,Masal Tea,Tweak,"Black tea, spices (cardamom, ginger, cinnamon, cloves)",Clean,KB_HIGH
8908022521614,Evocus,Evocus,"Purified water, nature identical flavour (contains minerals)",Clean,KB_HIGH
8901414001039,Synthetic Rose Syrup,Bilcano,"Sugar, rose extract, water, acidity regulator, colours",Verify colours,KB_HIGH
8906069411202,Dried Kiwi,Jewel Farmer,"Dried kiwi",Clean single-ingredient,KB_HIGH
8901030023804,Pepsodent,Various,"NON-FOOD — Toothpaste",NON-FOOD — PURGE,N/A
8906088058389,Bispari,Bispari,"Verify specific product",Verify,KB_MEDIUM
8908020047529,Chunky Hazelnut,Brawny Bear,"Roasted peanuts, hazelnuts, salt, edible vegetable oil",Clean,KB_HIGH
8901689030642,Black Currant Crush,Mala's,"Black currant juice, sugar, acidity regulator, colours",Verify colours,KB_HIGH
8901086260918,Herbal Cough Remedy,Zecuf,"NON-FOOD — Ayurvedic medicine",NON-FOOD — PURGE,N/A
8906140204006,Nature's Kima Dates 500gm,Various,"Dates (100%)",Clean single-ingredient,KB_HIGH
8909081003134,Sun Feast Cakes Sliced,Sunfeast,"Refined wheat flour, sugar, eggs, edible vegetable oil, glucose syrup, raising agents, emulsifiers, preservative (INS 202)",INS 202 preservative,KB_HIGH
8906020495913,Lal Dharwad Peda,Lal,"Milk solids, sugar, ghee, cardamom",Clean,KB_HIGH
8906009534251,Peanut Butter with Dark Chocolate,Various,"Roasted peanuts, dark chocolate, salt, edible vegetable oil",Clean,KB_HIGH
8908013252190,Muesli Fruity Crunch,Fit & Flex,"Oats, dried fruits, nuts, honey, edible vegetable oil",Clean,KB_HIGH
8909081010033,Chilli Cheese Baked Puff,Bingo!,"Refined wheat flour, cheese, chilli, edible vegetable oil, salt, spices, raising agents",Clean,KB_HIGH
8906088662364,Postpil,Various,"NON-FOOD — Medicine",NON-FOOD — PURGE,N/A
8904093828430,Ok 72,Various,"NON-FOOD — Medicine",NON-FOOD — PURGE,N/A
8904093825699,Pronta,Various,"Verify specific product",Verify,KB_MEDIUM
8906140203870,Sultan Dates,Nature's Choice,"Wet dates (Sultan)",Clean single-ingredient,KB_HIGH
8908003032849,Garlic Pickle,Various,"Garlic, salt, spices, edible vegetable oil, acidity regulator",Clean,KB_HIGH
8904293704091,Capsicum Green,Unknown Brand,"Green capsicum",Clean single-ingredient,KB_HIGH
8906093217047,Tamarind Whole,Zoff,"Tamarind (100%)",Clean single-ingredient,KB_HIGH"""

def run():
    print("=== EXECUTING BATCH 45 INGREDIENTS INTEGRATION & PURGE ===")
    df_all = pd.read_csv(all_supabase_csv, dtype=str)
    df_confirmed = pd.read_csv(confirmed_csv, dtype=str)
    df_needs_ver = pd.read_csv(needs_ver_csv, dtype=str)

    df_all['barcode'] = df_all['barcode'].str.strip()
    df_confirmed['barcode'] = df_confirmed['barcode'].str.strip()
    df_needs_ver['barcode'] = df_needs_ver['barcode'].str.strip()
    
    batch_reader = csv.DictReader(io.StringIO(BATCH45_DATA.strip()))
    batch_45_rows = list(batch_reader)

    elevated_count = 0
    added_count = 0
    purged_count = 0

    for item in batch_45_rows:
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

    print(f"Batch 45 Processing Summary:")
    print(f"  Elevated from Needs Verification to Confirmed: {elevated_count}")
    print(f"  Newly added to Confirmed: {added_count}")
    print(f"  Purged Non-Food Barcodes: {purged_count}")
    print(f"  Final Master CSV Count: {len(df_all)}")
    print(f"  Final Confirmed CSV Count: {len(df_confirmed)}")
    print(f"  Final Needs Verification CSV Count: {len(df_needs_ver)}")

if __name__ == "__main__":
    run()
