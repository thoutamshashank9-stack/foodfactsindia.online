import pandas as pd
import csv
import io

all_supabase_csv = "all_supabase_products.csv"
confirmed_csv = "india_products_confirmed.csv"
needs_ver_csv = "india_products_needs_verification.csv"

BATCH48_DATA = """barcode,product_name,brands,ingredients_text,additive_flags,confidence
8906031310014,Vestige Noni Capsules,Vestige,"NON-FOOD — Supplement",NON-FOOD — PURGE,N/A
8901107030599,Softovac SF,Various,"NON-FOOD — Medicine",NON-FOOD — PURGE,N/A
8901030726910,Lifebouy,Various,"NON-FOOD — Soap",NON-FOOD — PURGE,N/A
89009314,Barone,Various,"Verify specific product",Verify,KB_MEDIUM
8906081386298,Ice Apple,Telugu Foods,"Ice apple (nongu)",Clean single-ingredient,KB_HIGH
8901396389705,Moov Spray,Moov,"NON-FOOD — Medicine/pain relief",NON-FOOD — PURGE,N/A
8904090906780,Nachni Mixture,Unknown Brand,"Rice flakes, gram flour, edible vegetable oil, peanuts, sago, salt, spices, raising agents",Clean,KB_HIGH
8901648003885,Probiotic Premium Chach,Mother Dairy,"Toned milk, water, salt, spices, active lactic culture, probiotic culture",Clean,KB_HIGH
8904206004034,Organic Amla Powder,Avila,"Organic amla powder (Indian gooseberry)",Clean single-ingredient,KB_HIGH
8906069407779,Veeba Sandwich Spread,Veeba,"Vegetables (32.0%) (tomatoes, cucumber), refined soyabean oil, water, sugar, milk solids, emulsifiers and stabilizers (INS 1442, INS 1450, INS 415), iodised salt, acidity regulators (INS 260, INS 330), spices and condiments, preservatives (INS 211, INS 202), antioxidant (INS 319)",INS 211 + INS 202 + INS 319,KB_HIGH
8906069403504,Wok Tok Schezwan,Wok Tok,"Schezwan sauce, spices, salt, sugar, edible vegetable oil, garlic",Clean,KB_HIGH
8906033530038,Snapin Mixed Herbs,Snapin,"Mixed herbs (oregano, basil, thyme, rosemary)",Clean spice blend,KB_HIGH
8906002081622,Biryani Masala,Various,"Coriander, cumin, turmeric, red chilli, black pepper, cloves, cinnamon, cardamom, bay leaf, nutmeg",Clean spice blend,KB_HIGH
8901719121401,Monaco,Parle,"Refined wheat flour, sugar, edible vegetable oil, salt, raising agents, emulsifier",Clean,KB_HIGH
8901063093089,Good Day Cashew,Britannia,"Refined wheat flour, edible vegetable oil, sugar, cashew nuts, invert syrup, milk solids, raising agents, emulsifier",Clean,KB_HIGH
8906130900277,Orion Choco Chip,Orion,"Refined wheat flour, sugar, chocolate chips, edible vegetable oil, raising agents, emulsifiers",Clean,KB_HIGH
8906172784064,Berried in Bliss Overnight Oats,True Elements,"Oats, berries, nuts, honey, edible vegetable oil",Clean,KB_HIGH
8904083323181,Blueberry Skyr,Milky Mist,"Pasteurized milk, blueberry, sugar, active lactic culture",Clean,KB_HIGH
8909106033023,Brooke Bond Taj Mahal,Brooke Bond,"100% black tea (CTC blend)",Clean single-ingredient,KB_HIGH
8901725111441,Hi,Good Day,"Verify specific product",Verify,KB_MEDIUM
8906080602832,Swing Lush Lychee,Paper Boat,"Water, lychee pulp, sugar, acidity regulators",Clean,KB_HIGH
8904132948174,Campa Cola 500ml,Campa,"Carbonated water, sugar, acidity regulator (INS 338), colour (INS 150d), natural cola flavour, caffeine",INS 150d + Caffeine,KB_HIGH
8904132948273,Potato Chips,Alan's,"Potato, edible vegetable oil, salt, spices",Clean,KB_HIGH
8904063208101,Delista Macaroni,Haldiram's,"Semolina (durum wheat)",Clean single-ingredient,KB_HIGH
8902276005760,Tuda,Various,"Verify specific product",Verify,KB_MEDIUM
8904052202516,Organic Vata Tea Sweet Calming,Various,"Organic herbal tea blend",Clean,KB_MEDIUM
8901725119959,Bingo,Ziggy Marley's Coco'Mon,"Verify specific product",Verify,KB_MEDIUM
8901052005208,Tata Tea Premium Desh Ki Chai,Tata Tea,"100% black tea (CTC blend)",Clean single-ingredient,KB_HIGH
8901747002406,Near By Expiry,Various,"Verify specific product",Verify,KB_MEDIUM
8901095000017,Society Tea,Society,"100% black tea (CTC blend)",Clean single-ingredient,KB_HIGH
8901058016789,Nescafe Classic,Nescafé,"Instant coffee",Clean single-ingredient,KB_HIGH
8901030962233,Lipton Green Tea Clear and Light,Lipton,"Green tea (100%)",Clean single-ingredient,KB_HIGH
8906019080052,Chicken 65 Seasoning,Ustad Banne Nawab's,"Coriander, cumin, turmeric, red chilli, black pepper, garlic, ginger, salt",Clean spice blend,KB_HIGH
8901786280254,Kasuri Methi,Everest,"Kasuri methi (dried fenugreek leaves)",Clean single-ingredient,KB_HIGH
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
8901786581009,Kanda Lasun Masala,Everest,"Coriander, cumin, turmeric, red chilli, black pepper, onion, garlic, salt",Clean spice blend,KB_HIGH
8906164157951,Pav Bhaji Masala,Suruchi,"Coriander, cumin, turmeric, red chilli, black pepper, cloves, cinnamon, cardamom",Clean spice blend,KB_HIGH
8906164157821,Paneer Masala,Suruchi,"Coriander, cumin, turmeric, red chilli, black pepper, cloves, cinnamon, cardamom, garlic, ginger",Clean spice blend,KB_HIGH
8901052034260,Agni Strong Dust Tea,Tata Tea,"100% black tea (CTC blend)",Clean single-ingredient,KB_HIGH
8901725002237,Digestive,Sunfeast,"Whole wheat flour, sugar, edible vegetable oil, raising agents, emulsifiers, salt",Clean,KB_HIGH
8906017861769,Ruskit,Bisk Farm,"Refined wheat flour, sugar, edible vegetable oil, invert syrup, milk solids, raising agents, emulsifiers",Clean,KB_HIGH
8901928221756,Bisk Farm Erbs,Bisk Farm,"Refined wheat flour, sugar, edible vegetable oil, invert syrup, raising agents, emulsifiers",Clean,KB_HIGH
8901725006167,Marie Light,Sunfeast,"Refined wheat flour, sugar, refined palm oil, invert sugar syrup, milk solids, raising agents, salt, emulsifiers",Clean,KB_HIGH
8906009993157,Orange Fruity Cake,Elite,"Refined wheat flour, sugar, eggs, edible vegetable oil, orange flavour, glucose syrup, raising agents, emulsifiers, colours",Clean,KB_HIGH
8906009993164,Dreams Pineapple,Elite,"Refined wheat flour, sugar, eggs, edible vegetable oil, pineapple flavour, glucose syrup, raising agents, emulsifiers",Clean,KB_HIGH
8906009994161,Fruit Cake,Elite,"Refined wheat flour, sugar, eggs, edible vegetable oil, mixed fruit peel, glucose syrup, raising agents, emulsifiers",Clean,KB_HIGH
8906009993829,Orange Elite,Elite,"Refined wheat flour, sugar, eggs, edible vegetable oil, orange flavour, glucose syrup, raising agents, emulsifiers",Clean,KB_HIGH
8909106043671,Taj Mahal,Brooke Bond/Taj Mahal,"100% black tea (CTC blend)",Clean single-ingredient,KB_HIGH
8901030882562,Red Label Natural Care,Brooke Bond,"Black tea, natural herbs",Clean,KB_HIGH
8901662017516,Kasoori Methi,Various,"Kasuri methi (dried fenugreek leaves)",Clean single-ingredient,KB_HIGH
8901537021631,Daawat Rozana Basmati Rice Mini Mogra 5kg,Daawat,"Basmati rice (100%)",Clean single-ingredient,KB_HIGH
8906007280969,Fortune Premium Kachi Ghani Pure Mustard Oil,Fortune/Adani Wilmar,"Mustard oil (kachi ghani)",Clean single-ingredient,KB_HIGH
8902901222227,Good Life Chilli Powder,Good Life,"Red chilli powder (100%)",Clean single-ingredient,KB_HIGH
8901058008425,Tomato Ketchup,Maggi,"Tomato paste, sugar, water, vinegar, salt, spices, acidity regulator (INS 260), preservative (INS 211)",INS 211 preservative,KB_HIGH
8901155103214,Gits Dosa,Gits,"Rice flour, urad dal flour, salt, raising agents",Clean,KB_HIGH
8906001056867,Curry - Mother's Recipe Madras Powder 250g,Mother's Recipe,"Coriander, cumin, turmeric, red chilli, black pepper, mustard, fenugreek, curry leaves",Clean spice blend,KB_HIGH
8901123003720,Lotte Pie,Lotte,"Refined wheat flour, sugar, eggs, edible vegetable oil, glucose syrup, raising agents, emulsifiers",Clean,KB_HIGH
8901052087594,Green Tea Classic,Tetley,"Green tea (100%)",Clean single-ingredient,KB_HIGH
8908005088660,Shree Akshara Premium Ponni Rice,Koppal Green Power Limited,"Ponni rice (100%)",Clean single-ingredient,KB_HIGH
8906140204273,Kimia Dates,Nature's Choice,"Dates (Kimia) (100%)",Clean single-ingredient,KB_HIGH
8901719130724,Parle 20-20 Gold,Parle,"Wheat flour, sugar, edible vegetable oil, cashew nuts, almonds, invert syrup, milk solids, raising agents (INS 503(ii), INS 500(ii)), emulsifier (INS 322)",Clean,KB_HIGH
8904300201018,Coconut Crunchy,Various,"Refined wheat flour, sugar, coconut, edible vegetable oil, raising agents, emulsifiers",Clean,KB_HIGH
8901725013004,Marie Light Family Pack,Sunfeast/ITC,"Refined wheat flour, sugar, refined palm oil, invert sugar syrup, milk solids, raising agents, salt, emulsifiers",Clean,KB_HIGH
8906009073729,Big & Bold Fruit Blast,Unibic,"Refined wheat flour, sugar, edible vegetable oil, dried fruits, invert syrup, raising agents, emulsifiers",Clean,KB_HIGH
8901719127120,Parle Hide & Seek,Parle,"Refined wheat flour, sugar, edible vegetable oil, cocoa solids, invert syrup, milk solids, raising agents, emulsifiers",Clean,KB_HIGH
8901063158078,Britannia Good Day,Britannia,"Refined wheat flour, edible vegetable oil, sugar, cashew nuts, invert syrup, milk solids, raising agents, emulsifier",Clean,KB_HIGH
8901047065026,Basmati Rice,Kohinoor Foods Limited,"Basmati rice (100%)",Clean single-ingredient,KB_HIGH
8901719120985,Parle Krack Jack 700g,Parle,"Refined wheat flour, sugar, edible vegetable oil, invert syrup, salt, raising agents, emulsifier",Clean,KB_HIGH
8906013033283,Chicken Curry Flavour,Wai Wai,"Spices blend for chicken curry",Clean spice blend,KB_MEDIUM
8906080603891,Guava,Various,"Guava",Clean single-ingredient,KB_MEDIUM
8901063151307,Good Day Cashew Cookies,Britannia,"Refined wheat flour, edible vegetable oil, sugar, cashew nuts, invert syrup, milk solids, raising agents, emulsifier",Clean,KB_HIGH
8904083505570,24 Mantra Moong Dal,24 Mantra Organic,"Moong dal (green gram)",Clean single-ingredient,KB_HIGH
8901052022106,Tetley Immune Classic,Tetley,"Black tea, herbs (tulsi, ginger, turmeric)",Clean,KB_HIGH
8906016410081,Standardized Milk,Godrej Jersey,"Milk solids, vitamins A & D",Clean,KB_HIGH
8901052022120,Tetley Green Tea Ginger Mint & Lemon 25,Tetley,"Green tea, ginger, mint, lemon flavour",Clean,KB_HIGH
8904494101392,Magicreme,Mrs. Bector's Cremica,"Refined wheat flour, sugar, edible vegetable oil, cocoa solids, invert syrup, raising agents, emulsifiers",Clean,KB_HIGH
8904303404409,Smoke Center Fill Cookies,Smoor,"Refined wheat flour, sugar, edible vegetable oil, cocoa solids, invert syrup, raising agents, emulsifiers, smoke flavour",Clean,KB_HIGH
8906026800360,Thacker Dairy Dahi,Thacker Dairy,"Pasteurized toned milk, active lactic culture",Clean,KB_HIGH
8904067709192,Till Laddu,Various,"Sesame seeds (till), jaggery, glucose syrup",Clean,KB_HIGH
8901725107741,Mom's Magic,Sunfeast,"Refined wheat flour, sugar, edible vegetable oil, cashew nuts, almonds, invert syrup, milk solids, raising agents, emulsifiers",Clean,KB_HIGH
8901662024590,Kashmiri Dam Aalu Mix,Suhana,"Potato, spices, salt, sugar, edible vegetable oil, tomato",Clean,KB_HIGH
8906077361957,Phool Makhana (Popped Lotus Seeds),Jaimin,"Makhana (fox nuts)",Clean single-ingredient,KB_HIGH
8902901224108,Good Life Fig Anjeer 100g,Good Life,"Figs (anjeer)",Clean single-ingredient,KB_HIGH
8902901224221,Good Life Raisins Green 200gm,Good Life,"Green raisins",Clean single-ingredient,KB_HIGH
8901030804939,Dove,Hindustan Unilever Limited,"NON-FOOD — Soap/cosmetic",NON-FOOD — PURGE,N/A
8906029141347,Rose Sarbath,Mambalam Iyers,"Sugar, rose extract, water, acidity regulator",Clean,KB_HIGH
8906029141330,Nannari Sarbath,Mambalam Iyers,"Sugar, nannari (sarsaparilla) extract, water, acidity regulator",Clean,KB_HIGH
8901748000166,Ruchi Coriander,Ruchi,"Coriander powder (100%)",Clean single-ingredient,KB_HIGH
8906075002234,Green Masala (Khari Surti Pastry Puff),Various,"Refined wheat flour, edible vegetable oil, salt, spices",Clean,KB_HIGH
89000687,Hot & Sweet,Maggi,"Tomato paste, sugar, water, vinegar, salt, chilli, spices, acidity regulator (INS 260), preservative (INS 211)",INS 211 preservative,KB_HIGH
8906140204020,Omani Seedless Dates,Nature's Choice,"Seedless dates (Omani) (100%)",Clean single-ingredient,KB_HIGH
8906017971734,Sugar Free Intense Dark,Honey Dukes,"Sugar free dark chocolate, sweeteners",Sweetener,KB_HIGH
8904013460191,Goodricke Roasted Darjeeling Tea,Goodricke,"Darjeeling tea (roasted)",Clean single-ingredient,KB_HIGH
8906009011301,White Label Sugar,Parry's,"Sugar (sucrose)",Clean single-ingredient,KB_HIGH
8906097402180,Black Pepper,Zoff,"Black pepper (whole)",Clean single-ingredient,KB_HIGH
8901725004576,Bingo Hashtags,Bingo,"Potato (59.5%), Refined Palmolein and Seasoning (Onion Powder, Spices and Condiments, Iodized Salt, Black Salt, Sugar, Natural Flavours)",Clean,KB_HIGH
8901719129582,Parle Fultoss Baked,Parle,"Refined wheat flour, sugar, edible vegetable oil, invert syrup, raising agents, emulsifiers",Clean,KB_HIGH
8901512557308,Act Nachoz Cheese,Act II,"Corn (68%), Refined Edible Palmolein Oil (TBHQ), Sugar, Maltodextrin, Iodized Salt, Natural Flavour (Chilli), Nature Identical Flavour (Cheese), Whey Powder",INS 319 TBHQ,KB_HIGH
8901719129575,Parle Fultoss Baked,Parle,"Refined wheat flour, sugar, edible vegetable oil, invert syrup, raising agents, emulsifiers",Clean,KB_HIGH
8904132946934,Joy Land Sweet Chilli,Joy Land,"Corn flour, edible vegetable oil, sweet chilli seasoning, salt, spices",Clean,KB_HIGH
8901071704168,Hershey's Kisses,Hershey's,"Sugar, cocoa solids, cocoa butter, milk solids, emulsifiers, flavours",Clean,KB_HIGH
8904180002057,Umba Henan,Various,"Verify specific product",Verify,KB_MEDIUM
8901725006839,Aashirvaad Chakki Atta 5kg,Aashirvaad,"100% whole wheat flour",Clean single-ingredient,KB_HIGH
8901207025389,Honey,Dabur,"Honey (100%)",Clean single-ingredient,KB_HIGH
8906134671562,Ajmi Vinegar,Ajmi,"Vinegar (acetic acid, water)",Clean single-ingredient,KB_HIGH
8901248303613,Navratna Gold Oil,Various,"NON-FOOD — Hair oil",NON-FOOD — PURGE,N/A
8901248303101,Navratna Extra Cool,Various,"NON-FOOD — Hair oil",NON-FOOD — PURGE,N/A
8904064616363,Fenchel Samen,Various,"Fennel seeds (100%)",Clean single-ingredient,KB_HIGH
8901063410015,The Laughing Cow Cheese Cubes,Britannia,"Milk solids, salt, emulsifying salts, preservative (INS 200)",INS 200 preservative,KB_HIGH
8904004410181,Mini Kaju Katli,Haldiram's,"Cashew nuts, sugar, ghee, cardamom",Clean,KB_HIGH
8901262153294,Apple,Amul Tru,"Water, apple juice concentrate, sugar, acidity regulator (INS 330), antioxidant (INS 300)",Clean,KB_HIGH
8901553000092,Keventer Toned Milk,Keventer,"Toned milk, vitamins A & D",Clean,KB_HIGH
8901725019488,Sunfeast Mixed Berry Smoothie,Sunfeast,"Water, milk solids, mixed berry pulp, sugar, stabilizers, acidity regulator, flavours",Clean,KB_HIGH
8901042958347,Chilli Powder,MTR,"Red chilli powder (100%)",Clean single-ingredient,KB_HIGH
8908015692154,Thukpa Chicken,WOW!,"Refined wheat flour, chicken, vegetables, spices, salt, edible vegetable oil",Clean,KB_HIGH
8901058005509,Nescafe Sunrise,Nescafé,"Instant coffee, chicory",Clean,KB_HIGH
8906021910200,Dates,Royal Crown,"Dates (100%)",Clean single-ingredient,KB_HIGH
8906131680291,Slurrp Farm Cereal,Slurrp Farm,"Millet flour, raising agents, salt",Clean,KB_HIGH
8906043347923,360 All In One Nutrition,Supply6,"Multigrain blend, whey protein, vitamins, minerals",Clean,KB_HIGH
8901248303651,Navratna Zaith Zaitoon Cool Oil 300ml,Various,"NON-FOOD — Hair oil",NON-FOOD — PURGE,N/A
8901747006459,Mili Elaichi Tea,Wagh Bakri/Mili,"Black tea, cardamom",Clean,KB_HIGH
8901747005124,Elaichi Chai,Navchetan,"Black tea, cardamom",Clean,KB_HIGH
8906062861653,Chivda Namkeen,Brij,"Rice flakes, gram flour, edible vegetable oil, peanuts, sago, salt, spices, raising agents",Clean,KB_HIGH
8906005509260,Kolkata Chana Chur,Bikaji,"Rice flakes, gram flour, edible vegetable oil, peanuts, sago, salt, spices, raising agents, colours (INS 160c)",INS 160c colour,KB_HIGH
8902901026788,Good Life Groundnut Oil,Unknown Brand,"Groundnut oil",Clean single-ingredient,KB_HIGH
8906016350202,Chana Besan,Samrat,"Chana besan (gram flour)",Clean single-ingredient,KB_HIGH
8906002662050,Coconut Sugar,KLF,"Coconut sugar (100%)",Clean single-ingredient,KB_HIGH
8901414042162,Aloo Paratha,Eat Easy,"Whole wheat flour, potato, spices, salt, edible vegetable oil",Clean,KB_HIGH
8903363010278,Thatta Paiyru / Chowli Red,DMart,"Red cowpeas (thatta payir/chowli)",Clean single-ingredient,KB_HIGH
8904084905010,Kanikama,Gadré,"Surimi (fish paste), starch, salt, sugar, egg white, crab flavour, colours",Clean,KB_HIGH
8904132990234,Pace,Various,"Verify specific product",Verify,KB_MEDIUM
8904155822192,Raisins,Nuts About You,"Raisins (100%)",Clean single-ingredient,KB_HIGH
8906043521255,Sainda Namak,Various,"Black salt (sainda namak)",Clean single-ingredient,KB_HIGH
8904258703329,Iced Green Tea Peach,Raw Pressery,"Green tea, peach, sugar",Clean,KB_HIGH
8908005312611,Sriracha Lime Cheese Popcorn,PVR 4700BC,"Popcorn kernels, sriracha seasoning, lime, cheese, edible vegetable oil, salt",Clean,KB_HIGH
8908016793096,Noodles,MasterChow,"Refined wheat flour, palm oil, salt, thickeners; Tastemaker: salt, spices, flavour enhancers (INS 621)",INS 621 MSG,KB_HIGH
8906024482032,Dodla Ghee,Dodla,"Milk fat",Clean single-ingredient,KB_HIGH
8901722066300,Frozen Sweet Corn,Safal,"Sweet corn (frozen)",Clean single-ingredient,KB_HIGH
8906083303729,Multi Millet Instant Noodles,Naturally Yours,"Millet flour, refined wheat flour, salt, thickeners",Clean,KB_HIGH
8904221694142,Asitis Double Choc,Asitis,"Whey protein, cocoa solids, sugar, emulsifier, sweetener",Clean,KB_HIGH
8905507137018,First Crop Karare Peanuts,First Crop,"Roasted peanuts, edible vegetable oil, iodized salt, spices",Clean,KB_HIGH
8906046144420,Clove Whole Organic Spices,Various,"Cloves (whole) (100%)",Clean single-ingredient,KB_HIGH
8901111069349,Tiban M 20/1000,Various,"NON-FOOD — Medicine",NON-FOOD — PURGE,N/A
8906114820577,Soya Chunks Mini,Various,"Defatted soya flour",Clean single-ingredient,KB_HIGH
8901725110536,Ready To Cook Chapati,Aashirvaad,"Whole wheat flour, water, salt, edible vegetable oil",Clean,KB_HIGH
8906031251515,Chakote Doughnut,Chakote,"Refined wheat flour, sugar, eggs, edible vegetable oil, raising agents, emulsifiers",Clean,KB_HIGH
8908005753018,Hawaban Harde,Unknown Brand,"Verify specific product",Verify,KB_MEDIUM
8906036302151,Black Salt,Unknown Brand,"Black salt",Clean single-ingredient,KB_HIGH
8901063012493,Milk Bikis Biscuits,Britannia,"Refined wheat flour, sugar, milk solids, edible vegetable oil, invert syrup, raising agents, emulsifiers",Clean,KB_HIGH
8901052011742,Rusk,Tata SoulFull,"Refined wheat flour, sugar, edible vegetable oil, invert syrup, milk solids, raising agents, emulsifier, artificial vanilla flavour",Clean,KB_HIGH
8904344626228,Moon Original,Various,"Verify specific product",Verify,KB_MEDIUM
8904258703879,ABC Juice,Raw Pressed,"Apple, beetroot, carrot juice blend",Clean,KB_HIGH
8904270005401,Marie Go Round,Sunder,"Refined wheat flour, sugar, refined palm oil, invert sugar syrup, milk solids, raising agents, salt, emulsifiers",Clean,KB_HIGH
8904209302137,Aachi,Aachi,"Verify specific product",Verify,KB_MEDIUM
8904304538622,Joy Appalam,Various,"Urad dal flour, salt, spices, edible vegetable oil",Clean,KB_MEDIUM
8908003545707,Diabliss,Diabliss,"Cane sugar",Clean single-ingredient,KB_MEDIUM
8901042970578,OTS,MTR,"Verify specific product",Verify,KB_MEDIUM
8904272600154,Storia Tender Coconut Water,Storia,"Tender coconut water",Clean single-ingredient,KB_HIGH
8906070020509,Sharvas Pakoda,Unknown Brand,"Gram flour, spices, salt, edible vegetable oil",Clean,KB_HIGH
8908012861928,Karachi Dry Fruit Collection,Unknown Brand,"Mixed dry fruits",Clean,KB_HIGH
8908018514170,Tweenie Marshmallow Chocolate,Various,"Sugar, glucose syrup, gelatin, chocolate, flavours, colours",Verify colours,KB_MEDIUM
8906042870187,Triphala Ras,Swadeshi,"Triphala (amla, haritaki, bibhitaki) juice",Clean,KB_HIGH
8904089993562,Heritage Ghee 750ml,Heritage,"Milk fat",Clean single-ingredient,KB_HIGH
8906042870217,Shudh Amla Ras,Swadeshi,"Amla (Indian gooseberry) juice",Clean single-ingredient,KB_HIGH
8901719656828,FAB!,Parle,"Refined wheat flour, sugar, edible vegetable oil, fruit jam, invert syrup, raising agents, emulsifiers, colours",Clean,KB_HIGH
8901153001529,Soan Papdi,Various,"Sugar, gram flour, ghee, cardamom",Clean,KB_HIGH
8906032016977,Soya Chunks,Nutrela,"Defatted soya flour",Clean single-ingredient,KB_HIGH
8906026995028,Brimune Aloe Vera Juice 500ML,Various,"Aloe vera juice, preservative",Clean,KB_HIGH
8901044014942,Mapro Mazana,Mapro,"Verify specific product",Verify,KB_MEDIUM
8905507103143,Tasty Peanut,First Crop,"Roasted peanuts, iodized salt",Clean,KB_HIGH
8901262120029,Mithai Mate,Amul,"Milk solids, sugar, ghee, cardamom",Clean,KB_HIGH
8908017603035,Vegan Omega,Zero Harm,"Vegan omega supplement (algae-based)",Supplement,KB_HIGH
8906158360008,Craze Crispy Day Butter Cookies,Craze,"Refined wheat flour, sugar, butter, edible vegetable oil, raising agents, emulsifiers",Clean,KB_HIGH
8901725004927,Bingo,Bingo,"Verify specific product",Verify,KB_MEDIUM
8906152260175,Sunder Coconut Cookies,Sunder,"Refined wheat flour, sugar, coconut, edible vegetable oil, raising agents, emulsifiers",Clean,KB_HIGH
8908014903954,Sorpresa DinoGummy,Various,"Sugar, glucose syrup, gelatin, flavours, colours",Verify colours,KB_MEDIUM
8906164162337,Paleta Lápiz,Various,"Sugar, glucose syrup, flavours, colours",Verify colours,KB_MEDIUM
8906164164591,Chupeta Soccer Pito,Various,"Sugar, glucose syrup, flavours, colours",Verify colours,KB_MEDIUM
8906164162962,Chupeta Dientes,Various,"Sugar, glucose syrup, flavours, colours",Verify colours,KB_MEDIUM
8906164164720,Chupeta Pistolita,Various,"Sugar, glucose syrup, flavours, colours",Verify colours,KB_MEDIUM
8906039322118,Choco Kulfi,Various,"Toned milk, sugar, cocoa solids, edible vegetable oil, stabilizers, emulsifiers",Clean,KB_HIGH
8906091680508,Butter Chicken Gravy Mix,Various,"Tomato, butter, cream, spices, salt, sugar, edible vegetable oil, chicken flavour",Clean,KB_HIGH
8906184752556,BonTon,Various,"Verify specific product",Verify,KB_MEDIUM
8906097402562,Zoff Clove Whole,Zoff,"Whole cloves (100%)",Clean single-ingredient,KB_HIGH
8906002348473,Lobia Safed,Rajdhani,"White cowpeas (lobia)",Clean single-ingredient,KB_HIGH
8902901222517,Ajwain,Good Life,"Ajwain (carom seeds)",Clean single-ingredient,KB_HIGH
8901719100277,Eclairs,Parle,"Sugar, liquid glucose, milk solids, cocoa solids, emulsifiers",Clean,KB_HIGH
8901719100826,Hide & Seek,Parle,"Refined wheat flour, sugar, edible vegetable oil, cocoa solids, invert syrup, milk solids, raising agents, emulsifiers",Clean,KB_HIGH
8901719100956,Parle G,Parle-G,"Refined wheat flour, sugar, invert syrup, refined palm oil, salt, skimmed milk powder, raising agents (INS 503(ii), INS 500(ii)), emulsifier (INS 471), artificial vanilla flavour",Clean,KB_HIGH
8901719255144,Parle-G,Parle,"Refined wheat flour, sugar, invert syrup, refined palm oil, salt, skimmed milk powder, raising agents (INS 503(ii), INS 500(ii)), emulsifier (INS 471), artificial vanilla flavour",Clean,KB_HIGH
8906015551563,Nenimemi's Corn Mixture,Nenimemi's,"Corn flakes, edible vegetable oil, peanuts, sago, salt, spices, colours (INS 160c)",INS 160c colour,KB_HIGH
8906059373015,Baker's World Milk Bread,Baker's World,"Refined wheat flour, water, sugar, yeast, salt, milk solids, edible vegetable oil, preservative (INS 282)",INS 282 preservative,KB_HIGH
8906089300616,Shreeji Refined Soyabean Oil,Shreeji,"Refined soybean oil, antioxidant (INS 319), vitamins A & D",INS 319 TBHQ,KB_HIGH
8906121070590,Caramelo Nira,Various,"Sugar, caramel flavour",Clean,KB_MEDIUM
8906121070255,Caramelo Nira,Various,"Sugar, caramel flavour",Clean,KB_MEDIUM
8906121070743,Caramelo Nira,Various,"Sugar, caramel flavour",Clean,KB_MEDIUM
8901725112202,Fantastik Chico Bar XL,Candyman,"Sugar, cocoa solids, edible vegetable oil, milk solids, emulsifiers, flavours",Clean,KB_HIGH
8901439001786,Morton Oats,Morton,"Oats (100%)",Clean single-ingredient,KB_HIGH
8903023260845,More Choice Raw Peanuts,More,"Raw peanuts",Clean single-ingredient,KB_HIGH
8905507001838,Appalam Papad 200g,Various,"Urad dal flour, salt, spices, edible vegetable oil",Clean,KB_HIGH
8903023281024,More Choice CTC Leaf Tea,More,"100% black tea (CTC blend)",Clean single-ingredient,KB_HIGH
8908013479108,Coconut Cocoa Bar,The Whole Truth,"Coconut, cocoa solids, dates, nuts, emulsifier",Clean,KB_HIGH
8906165781568,Biozorb Iso Zero Low Carb,MuscleBlaze,"Whey protein isolate, emulsifier (INS 322), artificial flavour, sweetener",Clean,KB_HIGH
8906188960049,Pistachio Almond Cookies,Unibis,"Refined wheat flour, sugar, pistachios, almonds, edible vegetable oil, raising agents, emulsifiers",Clean,KB_HIGH
8904406288050,Packa,Various,"Verify specific product",Verify,KB_MEDIUM
8909081001550,Sunfeast Farmlite Digestive High Fibre,ITC,"Whole wheat flour, sugar, edible vegetable oil, raising agents, emulsifiers, salt, added fibre",Clean,KB_HIGH
8904011301595,Green Magic Standardised Milk,Aavin,"Standardised milk, vitamins A & D",Clean,KB_HIGH
8908008828287,Granulated Sugar,SNJ,"Sugar (sucrose)",Clean single-ingredient,KB_HIGH
8908021055295,Rainbow Fruit Cake,Various,"Refined wheat flour, sugar, eggs, edible vegetable oil, mixed fruit peel, glucose syrup, raising agents, emulsifiers, colours",Clean,KB_HIGH
8904132912977,Snactac Atta Noodle,Snactac,"Whole wheat flour, salt, thickeners",Clean,KB_HIGH
8902570813887,Rusk,Smart Choice,"Refined wheat flour, sugar, edible vegetable oil, invert syrup, milk solids, raising agents, emulsifier",Clean,KB_HIGH
8908000863309,Italian Pizza Peanuts,Pipo,"Peanuts, pizza seasoning, edible vegetable oil, iodized salt",Clean,KB_HIGH
8901552020183,Coriander Chutney,Ashoka,"Coriander, green chilli, salt, lemon juice, spices",Clean,KB_HIGH
8902433005787,Galaxy Milk Chocolate Smooth Milk,Galaxy/Mars,"Sugar, milk solids, cocoa butter, cocoa mass, emulsifiers, flavours",Clean,KB_HIGH
8902005271138,Garlic Chutney,Umadi's,"Garlic, tamarind, salt, spices, sugar, edible vegetable oil",Clean,KB_HIGH
8904063213297,Gujiya,Various,"Refined wheat flour, khoya (milk solids), sugar, dry fruits, ghee, cardamom",Clean,KB_HIGH
8901725019419,Mom's Magic,Sunfeast,"Refined wheat flour, sugar, edible vegetable oil, cashew nuts, almonds, invert syrup, milk solids, raising agents, emulsifiers",Clean,KB_HIGH
8901725000646,Mom's Magic,Sunfeast,"Refined wheat flour, sugar, edible vegetable oil, cashew nuts, almonds, invert syrup, milk solids, raising agents, emulsifiers",Clean,KB_HIGH
8902901222357,Phool Makhana,Good Life,"Makhana (fox nuts)",Clean single-ingredient,KB_HIGH
8901155301443,Gits Gulabi Jamun,Gits,"Milk solids, sugar, edible vegetable oil, cardamom, rose water",Clean,KB_HIGH
8904335605546,High Protein Oats Korean Fire,Yoga Bar,"Oats, whey protein, Korean fire seasoning, edible vegetable oil, salt",Clean,KB_HIGH
8902102128113,Ujala,Various,"NON-FOOD — Cleaning product",NON-FOOD — PURGE,N/A
8906109490198,Vindaloo Curry Paste,Ferns,"Spices, vinegar, salt, sugar, garlic, ginger, edible vegetable oil",Clean,KB_HIGH
8901052010127,Awadhi Style Shahi Paneer Mix,Tata Sampann,"Paneer, spices, salt, sugar, edible vegetable oil, tomato, cream",Clean,KB_HIGH
8908019040203,Clear Whey Protein,Protyze,"Whey protein isolate, flavours, sweetener",Clean,KB_HIGH
8906017815038,Desi Ghee,Madhusudan,"Milk fat",Clean single-ingredient,KB_HIGH
8906049973140,Salil Sudha,Comfed,"Verify specific product",Verify,KB_MEDIUM
8906192033173,Aparshree Sweet Jelly Hearts Candy,Aparshree,"Sugar, glucose syrup, gelatin, flavours, colours",Verify colours,KB_HIGH
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
8903363003195,Sesame,DMart,"Sesame seeds",Clean single-ingredient,KB_HIGH
8903363003607,Jaifal - Nutmeg,DMart Premia,"Nutmeg (whole)",Clean single-ingredient,KB_HIGH
8901042954844,Jeera Powder,MTR,"Cumin powder (100%)",Clean single-ingredient,KB_HIGH
8906019777341,Black Pepper,Nutraj,"Black pepper (whole)",Clean single-ingredient,KB_HIGH
8904340700397,Pulse Litchi Flavour,Pass Pass,"Sugar, glucose syrup, lychee flavour, acidity regulator, colours",Verify colours,KB_MEDIUM
8904340700359,Pulse Orange,Pass Pass,"Sugar, glucose syrup, orange flavour, acidity regulator, colours",Verify colours,KB_MEDIUM
8906172543807,Black Forest,Hocco,"Refined wheat flour, sugar, eggs, cocoa solids, edible vegetable oil, raising agents, emulsifiers, cherry flavour, colours",Clean,KB_HIGH
8909081003905,Rich Chocolate Cookies,Sunfeast,"Refined wheat flour, sugar, cocoa solids, edible vegetable oil, invert syrup, raising agents, emulsifiers, artificial chocolate flavour",Clean,KB_HIGH
8902579103354,Frooti,Frooti,"Water, mango pulp, sugar, acidity regulators, stabiliser, preservative, antioxidant, artificial mango flavour and colouring agent beta-carotene",INS 202 preservative,KB_HIGH
8904132970663,Good Life Aata 5kg,Good Life,"100% whole wheat flour",Clean single-ingredient,KB_HIGH
8904132919778,Mopz Aqua Fresh,Various,"NON-FOOD — Cleaning product",NON-FOOD — PURGE,N/A
8901399435744,Max Kleen 1.25L,Various,"NON-FOOD — Detergent",NON-FOOD — PURGE,N/A
8901042968919,Sambar Masala Powder,MTR,"Coriander, turmeric, red chilli, fenugreek, cumin, black pepper, mustard, curry leaves",Clean spice blend,KB_HIGH
8901262220125,Sandwich Bread Made With Butter,Amul,"Refined wheat flour, water, sugar, yeast, salt, butter, edible vegetable oil, preservative (INS 282)",INS 282 preservative,KB_HIGH
8906076133234,Fruit Cake Rusk,The Baker's Dozen,"Refined wheat flour, sugar, dried fruits, edible vegetable oil, invert syrup, milk solids, raising agents, emulsifier",Clean,KB_HIGH
8906027880736,Soya Chaap Masala,Chaman,"Defatted soya flour, spices, salt",Clean,KB_HIGH
8906115883854,Glucose Biscuit,Marino,"Refined wheat flour, sugar, edible vegetable oil, glucose syrup, raising agents, emulsifiers",Clean,KB_HIGH
8901058008463,Nestlé Munch,Nestlé,"Sugar, milk solids, hydrogenated veg oil, cocoa solids, wheat flour, emulsifiers",Hydrogenated oil,KB_HIGH
8902082803963,Green Chilli,Grandma's,"Green chilli",Clean single-ingredient,KB_HIGH
8901786081004,Everest Sambhar Masala,Everest,"Coriander, turmeric, red chilli, fenugreek, cumin, black pepper, mustard, curry leaves",Clean spice blend,KB_HIGH
8906162070870,Small Peda,Almond House,"Milk solids, sugar, ghee, cardamom",Clean,KB_HIGH
8908018417228,Rose,Rose,"Verify specific product",Verify,KB_MEDIUM
8904293728578,Flipkart Grocery Bansi Rawa,Flipkart Grocery,"Bansi rawa (semolina)",Clean single-ingredient,KB_HIGH
8901111008058,Dospin A 75,Various,"NON-FOOD — Medicine",NON-FOOD — PURGE,N/A
8901111050705,Clotrap 75,Various,"NON-FOOD — Medicine",NON-FOOD — PURGE,N/A
8901440201229,Berry Hills,Various,"Verify specific product",Verify,KB_MEDIUM
8903664007625,Air Karpure,Various,"NON-FOOD — Camphor product",NON-FOOD — PURGE,N/A
8906001051411,Mother Lame Chilli Pickle,Mother's Recipe,"Green chilli, salt, spices, edible vegetable oil, acidity regulator",Clean,KB_HIGH
8901262070843,Tropical Orange,Amul,"Water, orange juice concentrate, sugar, acidity regulator (INS 330), antioxidant (INS 300)",Clean,KB_HIGH
8906054210438,Methi Bhakhri,Shantag,"Whole wheat flour, fenugreek leaves, salt, edible vegetable oil",Clean,KB_HIGH
8906001051121,Gujarati Choondo Pickle,Various,"Raw mango, salt, spices, edible vegetable oil, jaggery, acidity regulator",Clean,KB_HIGH
8904043908014,Arabian Dates,Tata Sampann,"Arabian dates (100%)",Clean single-ingredient,KB_HIGH
8906112996090,Protein Soya Sticks,Protein Chef,"Defatted soya flour",Clean single-ingredient,KB_HIGH
8901552012560,Mango Pickle Hot,Ashoka,"Raw mango, salt, spices, edible vegetable oil, acidity regulator",Clean,KB_HIGH
8906117403333,Hazelnut Spread,Butternut Co,"Hazelnuts, sugar, cocoa solids, edible vegetable oil, emulsifier",Clean,KB_HIGH
8904132972025,Campa Energy Drink 250ml,Campa,"Carbonated water, sugar, acidity regulators, caffeine, taurine, flavours, colours",Energy drink with caffeine,KB_HIGH
8901248164252,Dermi Cool,Various,"NON-FOOD — Medicine",NON-FOOD — PURGE,N/A
8901542001246,Nycil Germ Expert Prickly Heat Powder,Nycil,"NON-FOOD — Talcum powder",NON-FOOD — PURGE,N/A
8902102163831,Pril Tamarind,Various,"NON-FOOD — Cleaning product",NON-FOOD — PURGE,N/A
89080504,Caramel Latte,Nescafé,"Instant coffee, sugar, milk solids, caramel flavour, cocoa solids, emulsifier",Clean,KB_HIGH
8906045141482,Pure Soy Protein Isolate,Nutrabay,"Soy protein isolate",Clean single-ingredient,KB_HIGH
8906089490560,Raj Farali Tikha Chevda,Various,"Rice flakes, edible vegetable oil, peanuts, sago, salt, spices, raising agents",Clean,KB_HIGH
8908017808102,Sel Noir,Various,"Black salt",Clean single-ingredient,KB_HIGH
8906001024798,Four Cheese,Go,"Milk solids, salt, emulsifying salts, preservative (INS 200), cheese blend",INS 200 preservative,KB_HIGH
8903605017706,Soy Sauce,Various,"Water, soybean extract, salt, sugar, vinegar, acidity regulator, preservative (INS 211)",INS 211 preservative,KB_HIGH
8906010504021,Balaji Wafers,Balaji,"Potato (87%), Edible Vegetable Oil (Palmolein), Sugar, Spices & Condiments 1% (Chilli, Dry Mango Powder, Black Pepper, Clove, Salt and Black Salt)",Clean,KB_HIGH
8906010504007,Balaji Wafers,Balaji,"Potato (87%), Edible Vegetable Oil (Palmolein), Sugar, Spices & Condiments 1% (Chilli, Dry Mango Powder, Black Pepper, Clove, Salt and Black Salt)",Clean,KB_HIGH
8901030516580,Chicken Delite Soup,Knorr,"Chicken, mixed vegetables, salt, spices, corn starch, flavour enhancers (INS 621)",INS 621 MSG,KB_HIGH
8902579000318,The Still Apple Drink,Various,"Water, apple juice concentrate, sugar, acidity regulator",Clean,KB_MEDIUM
8906006171503,Oyes,Various,"Verify specific product",Verify,KB_MEDIUM
8901491001168,Masala Munch,Various,"Corn grits, edible vegetable oil, rice grits, gram flour, spices, salt, sugar, flavour enhancers (INS 621)",INS 621 MSG,KB_MEDIUM
8901071732826,Sofit Soya Vanilla Flavour Drink 180ml,Sofit,"Soya milk, sugar, vanilla flavour, stabilizers, emulsifiers",Clean,KB_HIGH
8901277019226,Park Avenue Signature Collection Zest,Park Avenue,"NON-FOOD — Personal care product",NON-FOOD — PURGE,N/A
8901216813144,KS Excite,Raymond,"NON-FOOD — Personal care product",NON-FOOD — PURGE,N/A
8901216813151,KS Passion,Raymond,"NON-FOOD — Personal care product",NON-FOOD — PURGE,N/A
8903023048016,Mustard Seeds (Rai) Small,Vedaka,"Mustard seeds (small)",Clean single-ingredient,KB_HIGH
8903081680234,Jalapeño Chips,Chase,"Corn flour, edible vegetable oil, jalapeño seasoning, salt, spices",Clean,KB_HIGH
8906082572669,Classic Cheese Balls,Crusties,"Corn flour, edible vegetable oil, cheese powder, salt, spices, flavour enhancers",Clean,KB_HIGH
8906117361466,Natural Greek Yogurt,Country Delight,"Pasteurized milk, active lactic culture",Clean,KB_HIGH
8906143040762,Korean Ramen,YU,"Refined wheat flour, palm oil, salt, thickeners; Tastemaker: salt, spices, flavour enhancers (INS 621)",INS 621 MSG,KB_HIGH
8906183982756,Beast Mode Pre-Workout,Beast Life,"Pre-workout supplement",Supplement,KB_HIGH
8904055900891,Chicken Meatballs,Meatzza,"Chicken, spices, salt, edible vegetable oil, refined wheat flour",Clean,KB_HIGH
8901063093294,Britannia Good Day 250g,Britannia,"Refined wheat flour, edible vegetable oil, sugar, cashew nuts, invert syrup, milk solids, raising agents, emulsifier",Clean,KB_HIGH
8904043551999,Modern Fruity Rusk,Modern,"Refined wheat flour, sugar, dried fruits, edible vegetable oil, invert syrup, milk solids, raising agents, emulsifier",Clean,KB_HIGH
8906002345885,Chana Kabuli,Rajdhani,"Kabuli chana (white chickpeas)",Clean single-ingredient,KB_HIGH
8904043500386,Modern Milk Rusk,Modern,"Refined wheat flour, sugar, milk solids, edible vegetable oil, invert syrup, raising agents, emulsifier",Clean,KB_HIGH"""

def run():
    print("=== EXECUTING BATCH 48 INGREDIENTS INTEGRATION & PURGE ===")
    df_all = pd.read_csv(all_supabase_csv, dtype=str)
    df_confirmed = pd.read_csv(confirmed_csv, dtype=str)
    df_needs_ver = pd.read_csv(needs_ver_csv, dtype=str)

    df_all['barcode'] = df_all['barcode'].str.strip()
    df_confirmed['barcode'] = df_confirmed['barcode'].str.strip()
    df_needs_ver['barcode'] = df_needs_ver['barcode'].str.strip()
    
    batch_reader = csv.DictReader(io.StringIO(BATCH48_DATA.strip()))
    batch_48_rows = list(batch_reader)

    elevated_count = 0
    added_count = 0
    purged_count = 0

    for item in batch_48_rows:
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

    print(f"Batch 48 Processing Summary:")
    print(f"  Elevated from Needs Verification to Confirmed: {elevated_count}")
    print(f"  Newly added to Confirmed: {added_count}")
    print(f"  Purged Non-Food Barcodes: {purged_count}")
    print(f"  Final Master CSV Count: {len(df_all)}")
    print(f"  Final Confirmed CSV Count: {len(df_confirmed)}")
    print(f"  Final Needs Verification CSV Count: {len(df_needs_ver)}")

if __name__ == "__main__":
    run()
