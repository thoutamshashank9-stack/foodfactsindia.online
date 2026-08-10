import pandas as pd
import csv
import io

all_supabase_csv = "all_supabase_products.csv"
confirmed_csv = "india_products_confirmed.csv"
needs_ver_csv = "india_products_needs_verification.csv"

BATCH46_DATA = """barcode,product_name,brands,ingredients_text,additive_flags,confidence
8906097400179,Coriander Powder,Zoff,"Coriander powder (100%)",Clean single-ingredient,KB_HIGH
8906009534510,Max Protein 7 Grain Protein Snack Cream & Onion,RiteBite,"Multigrain blend, whey protein, cream & onion seasoning, edible vegetable oil, salt",Clean,KB_HIGH
8908009186461,Sport Evolve Performance Plant Protein Tropical Mango,Plix,"Plant protein blend (pea, rice, soy), tropical mango flavour, sweetener (stevia), emulsifier",Clean,KB_HIGH
8901117250000,Prolyte ORS Orange Flavour,Cipla Health,"Glucose, sodium chloride, potassium chloride, sodium citrate, orange flavour",ORS — Regulated,KB_HIGH
8901030825552,Protein Plus,Horlicks,"Milk solids, malted cereals, sugar, cocoa solids, wheat flour, minerals, vitamins, emulsifier (INS 471)",Clean,KB_HIGH
8904132926806,Good Life Besan,Good Life,"Gram flour (besan)",Clean single-ingredient,KB_HIGH
8908003746708,ORS Lemon Drink,Electrorush,"Glucose, sodium chloride, potassium chloride, sodium citrate, lemon flavour",ORS — Regulated,KB_HIGH
8904063224439,Haldiram Manpasand,Haldiram's,"Rice flakes, gram flour, edible vegetable oil, peanuts, sago, salt, spices, raising agents, colours (INS 160c)",INS 160c colour,KB_HIGH
8901035062426,Bte Kdo Thé Victoria 6 Variété,Various,"Tea variety pack",Clean,KB_MEDIUM
8904355401814,Apollo Life Chyawan Health Gold,Apollo Life,"Amla, sugar, honey, ghee, herbs, spices",Ayurvedic,KB_HIGH
8906097597794,Reload,Fast&Up,"Electrolytes (sodium, potassium, magnesium), vitamins, flavours",Supplement,KB_HIGH
8904043927299,Tata Sampann Coriander Powder,Tata Sampann,"Coriander powder (100%)",Clean single-ingredient,KB_HIGH
8901552026314,Paneer Kulcha,Ashoka,"Refined wheat flour, paneer, spices, salt, edible vegetable oil",Clean,KB_HIGH
8909081005046,Dark Fantasy Choco Fills,Sunfeast,"Choco crème (sugar, refined palmolein, cocoa solids), refined wheat flour, sugar, invert syrup, liquid glucose, cocoa solids, milk solids, butter, raising agents, emulsifiers, salt",Clean,KB_HIGH
8907316003294,Mother Recipe Garlic Chilli Sauce,Mother Recipe,"Garlic, chilli, vinegar, salt, sugar, acidity regulator, preservative (INS 211)",INS 211 preservative,KB_HIGH
8902080002061,Pomegranate,Tropicana,"Water, pomegranate juice concentrate, sugar, acidity regulator, antioxidant",Clean,KB_HIGH
8902080002672,Litchi Love,Tropicana,"Water, lychee juice concentrate, sugar, acidity regulator, flavours",Clean,KB_HIGH
8906009990699,Elite Choco Orange,Elite,"Refined wheat flour, sugar, cocoa solids, orange flavour, eggs, edible vegetable oil, raising agents, emulsifiers",Clean,KB_HIGH
8906009990705,Elite Dreams Choco Pineapple,Elite,"Refined wheat flour, sugar, cocoa solids, pineapple flavour, eggs, edible vegetable oil, raising agents, emulsifiers",Clean,KB_HIGH
8906009993157,Orange Fruity Cake,Elite,"Refined wheat flour, sugar, eggs, edible vegetable oil, orange flavour, glucose syrup, raising agents, emulsifiers, colours",Clean,KB_HIGH
8906009993164,Dreams Pineapple,Elite,"Refined wheat flour, sugar, eggs, edible vegetable oil, pineapple flavour, glucose syrup, raising agents, emulsifiers",Clean,KB_HIGH
8906009994161,Fruit Cake,Elite,"Refined wheat flour, sugar, eggs, edible vegetable oil, mixed fruit peel, glucose syrup, raising agents, emulsifiers",Clean,KB_HIGH
8906009993829,Orange Elite,Elite,"Refined wheat flour, sugar, eggs, edible vegetable oil, orange flavour, glucose syrup, raising agents, emulsifiers",Clean,KB_HIGH
8906009993812,Cake Milk,Elite,"Refined wheat flour, sugar, eggs, milk solids, edible vegetable oil, glucose syrup, raising agents, emulsifiers",Clean,KB_HIGH
8901526406883,BL/GE SMOOTHEROOF Camelia Conditioner,Various,"NON-FOOD — Hair care product",NON-FOOD — PURGE,N/A
8904192215902,Rice Cakes Mix Masala,Various,"Rice flour, masala spices, edible vegetable oil, iodized salt",Clean,KB_HIGH
8906016579993,Homelites,WIMCO/ITC,"Verify specific product",Verify,KB_MEDIUM
8901155104211,Medu Vada,Gits,"Urad dal flour, salt, spices, edible vegetable oil",Clean,KB_HIGH
8903023002216,Vedaka Whole Cashews,Vedaka,"Whole cashew nuts",Clean single-ingredient,KB_HIGH
8906008351392,Kodo Millet,Manna,"Kodo millet",Clean single-ingredient,KB_HIGH
8906135071408,Amla Bites,Native Food Stores,"Amla (Indian gooseberry), sugar",Clean,KB_HIGH
8908003452593,Zoopy,Various,"Verify specific product",Verify,KB_MEDIUM
8909106014558,Red Label Natural Care,HUL,"Black tea, natural herbs",Clean,KB_HIGH
8906055440285,Dalia,Organic Tattva,"Broken wheat (dalia)",Clean single-ingredient,KB_HIGH
8904083519997,Rock Salt,24 Mantra Organic,"Rock salt (sendha namak)",Clean single-ingredient,KB_HIGH
8901542001239,Complan Creamy Classic,Complan,"Milk solids (52%), sugar, cocoa solids, maltodextrin, almonds, minerals, vitamins, colours (INS 100(i), INS 160b(ii))",Natural colours,KB_HIGH
8902901223361,Poha Mota,Good Life,"Flattened rice (poha) thick variety",Clean single-ingredient,KB_HIGH
8906036300089,Rajgira,Various,"Rajgira (amaranth)",Clean single-ingredient,KB_HIGH
8902433007699,Snickers Miniatures,Snickers,"Sugar, peanuts, glucose syrup, milk solids, cocoa butter, cocoa mass, emulsifiers, salt",Clean,KB_HIGH
8908009515360,GetKrrackin! Chikki,GetKrrackin!,"Peanuts, jaggery, glucose syrup",Clean,KB_HIGH
8904103033014,Swastiks Tomato Pickle,Swastiks,"Tomato, salt, spices, edible vegetable oil, acidity regulator",Clean,KB_HIGH
8901058021066,Munich Choco Fills,Nestlé,"Refined wheat flour, sugar, cocoa solids, edible vegetable oil, invert syrup, raising agents, emulsifiers, artificial chocolate flavour",Clean,KB_HIGH
8906082526167,Kapiva Shilajit,Kapiva,"Shilajit extract (100%)",Clean single-ingredient,KB_HIGH
8906087773740,0.3% Retinol Serum,Various,"NON-FOOD — Cosmetic product",NON-FOOD — PURGE,N/A
8901030713286,Nark Crowne Swas,Knorr,"Verify specific product",Verify,KB_MEDIUM
8906009536460,RiteBite Max Protein Jaggery Crunchy Spread Peanut Butter,RiteBite/Max Protein,"Roasted peanuts, jaggery, whey protein, emulsifier",Clean,KB_HIGH
8906124050605,Liveasy Hot Water Bag 2Litre,Liveasy,"NON-FOOD — Medical supply",NON-FOOD — PURGE,N/A
8906124050612,Cotton Creep Bandage,Liveasy,"NON-FOOD — Medical supply",NON-FOOD — PURGE,N/A
8908005946304,Absorbant Cotton Wool 50g,Jaycot,"NON-FOOD — Medical supply",NON-FOOD — PURGE,N/A
8904150208502,Brazil Nuts,Nutty Gritties,"Brazil nuts (100%)",Clean single-ingredient,KB_HIGH
8906120100502,Roasted & Salted California Pistachios,Farmley,"Roasted pistachios, iodized salt",Clean,KB_HIGH
8901117287914,Ciplox D Eye Drops 10ml,Cipla,"NON-FOOD — Medicine",NON-FOOD — PURGE,N/A
8902281608925,Clobeng 5g Cream,Indoco,"NON-FOOD — Medicine",NON-FOOD — PURGE,N/A
8901063165823,50-50 Time Pass,Britannia,"Refined wheat flour, sugar, edible vegetable oil, invert syrup, salt, raising agents, emulsifier",Clean,KB_HIGH
8901810003729,Attracts Money - 20 Stick Hex Tube - Hem Incense,Hem,"NON-FOOD — Incense product",NON-FOOD — PURGE,N/A
8906016011813,Indian Kishmish,Various,"Raisins (kishmish) (100%)",Clean single-ingredient,KB_HIGH
8904063200532,Spicy Banana Chips,Haldiram's,"Banana, edible vegetable oil (coconut/palmolein), spices, iodized salt",Clean,KB_HIGH
8904064616523,Semoule,Various,"Semolina (suji/rava) from wheat",Clean single-ingredient,KB_HIGH
8904064661905,Poudre de Canne à Sucre Brun,Various,"Brown cane sugar powder",Clean single-ingredient,KB_HIGH
8906037692046,Red Food Colouring,Various,"Food colouring (red)",Verify,KB_MEDIUM
8901140835939,Datteri Medjoul,Various,"Medjool dates (100%)",Clean single-ingredient,KB_HIGH
8908000275652,City Gold Tea,City Gold,"100% black tea (CTC blend)",Clean single-ingredient,KB_HIGH
8906087776215,Mamaearth Bathing Bar 75g,Mamaearth,"NON-FOOD — Soap/cosmetic",NON-FOOD — PURGE,N/A
8901414060678,Bikano Combo Pack,Bikano,"Gram flour, edible vegetable oil, iodized salt, spices, sugar, milk solids",Clean,KB_HIGH
8906124370673,Egg,Eggos,"Eggs (100%)",Clean single-ingredient,KB_HIGH
8906142010995,Chekodilu,Telugu Foods,"Rice flour, coconut, jaggery, edible vegetable oil, cardamom",Clean,KB_HIGH
0759159789815,Plant Protein Powder,Nack,"Plant protein blend (pea, rice, soy), flavours, sweetener",Clean,KB_MEDIUM
8906069612142,Anand Chakli,Anand/Jolliz,"Rice flour, gram flour, edible vegetable oil, iodized salt, spices",Clean,KB_HIGH
8906069610858,Anand Jolliz Bhakharwadi,Anand/Jolliz,"Refined wheat flour, gram flour, edible vegetable oil, spices, salt, sugar, coconut, sesame seeds",Clean,KB_HIGH
8904089309479,Slice Cassata Ice Cream with Eggless Cake,Havmor,"Toned milk, sugar, edible vegetable oil, cake, stabilizers, emulsifiers, flavours, colours",Clean,KB_HIGH
8906028690518,Pasteurised Full Cream Milk,Koyna,"Full cream milk, vitamins A & D",Clean,KB_HIGH
8906163076666,Riz Étuvé Grains Long Sella Indien,Jovial,"Parboiled long grain sella rice",Clean single-ingredient,KB_HIGH
8906182650007,Berries Mix,Fabeato,"Mixed berries (cranberries, blueberries, strawberries, raspberries)",Clean,KB_HIGH
3948764972058,Unknown,Various,"Verify specific product",Verify,KB_MEDIUM
8904063226143,Milk Cake,Haldiram,"Milk solids (khoya), sugar, ghee, cardamom",Clean,KB_HIGH
8901700002047,Unknown,Various,"Verify specific product",Verify,KB_MEDIUM
8906107173703,Pizza Minis,Prasuma,"Refined wheat flour, cheese, tomato sauce, vegetables, edible vegetable oil, spices, salt",Clean,KB_HIGH
8901058008494,Nestle Koko Krunch 150g,Nestlé,"Whole wheat flour, sugar, cocoa solids, glucose syrup, salt, vitamins, minerals",Clean,KB_HIGH
8901779062102,Saras,Saras,"Verify specific product",Verify,KB_MEDIUM
8901779900275,Biriyani Masala,Saras,"Coriander, cumin, turmeric, red chilli, black pepper, cloves, cinnamon, cardamom, bay leaf, nutmeg",Clean spice blend,KB_HIGH
8901779052103,Saras Sambar Powder,Saras,"Coriander, turmeric, red chilli, fenugreek, cumin, black pepper, mustard, curry leaves",Clean spice blend,KB_HIGH
8906030392776,Tamarind,Various,"Tamarind (100%)",Clean single-ingredient,KB_HIGH
8901779224104,Saras Milk Ada Desert,Saras,"Rice flakes, milk solids, sugar, cardamom, ghee",Clean,KB_HIGH
8901779900404,Saras Jack Fruit Cake,Saras,"Jackfruit, refined wheat flour, sugar, eggs, edible vegetable oil, raising agents, emulsifiers",Clean,KB_HIGH
8904132972339,Green Cardamom,Good Life,"Green cardamom (100%)",Clean single-ingredient,KB_HIGH
8904132917682,Green Tea Honey and Lemon,Aarambh,"Green tea, honey, lemon flavour",Clean,KB_HIGH
8901262080040,Amulspray,Amul,"Demineralized whey, vegetable oils, skimmed milk powder, lactose, minerals, vitamins",Regulated infant food,KB_HIGH
8901817671499,Honig Madu,Various,"Honey (100%)",Clean single-ingredient,KB_HIGH
8908018177115,Roasted Pistachio,LGN,"Roasted pistachios, iodized salt",Clean,KB_HIGH
8906009070926,Unibic Choco Rs 5,Unibic,"Refined wheat flour, sugar, cocoa solids, edible vegetable oil, invert syrup, raising agents, emulsifiers",Clean,KB_HIGH
8906097970108,Rasam Powder,JPF,"Coriander, cumin, turmeric, red chilli, black pepper, mustard, fenugreek, curry leaves",Clean spice blend,KB_HIGH
8906054110721,Good Bread,Various,"Refined wheat flour, water, sugar, yeast, salt, edible vegetable oil, preservative (INS 282)",INS 282 preservative,KB_HIGH
8901888004833,Real Mosambi Fruit Juice,Real,"Water, mosambi (sweet lime) juice concentrate, sugar, acidity regulator (INS 330), antioxidant (INS 300)",Clean,KB_HIGH
8901393024234,Juzt Jelly Strawberry,Alpenliebe,"Sugar, glucose syrup, gelatin, strawberry flavour, acidity regulator, colours",Verify colours,KB_HIGH
8906003210731,Zinfandel Rosewein,Sulawesi Vineyards,"Alcoholic beverage (wine)",ALCOHOL — SEPARATE,KB_HIGH
8906069610247,Jolliz Salty Chunks Moong Dal,Anand,"Moong dal, edible vegetable oil, iodized salt, spices",Clean,KB_HIGH
8908002105117,Brown Bread,BakesFresh,"Whole wheat flour, water, sugar, yeast, salt, edible vegetable oil, preservative (INS 282)",INS 282 preservative,KB_HIGH
8904063204202,Khatta Dhokla,Haldiram's,"Gram flour, water, sugar, salt, spices, edible vegetable oil, raising agents",Clean,KB_HIGH
8906154300329,Aloo Bujia,Various,"Potato flakes & starch, edible vegetable oil, gram flour, iodized salt, spices, colour (INS 160c)",INS 160c colour,KB_HIGH
8901262153270,Amul Tru Orange Juice 150ml,Amul,"Orange juice, water, sugar, acidity regulator (INS 330), antioxidant (INS 300)",Clean,KB_HIGH
8901542003158,Complan Rich Chocolate Flavour,Complan,"Milk solids (52%), sugar, cocoa solids, maltodextrin, almonds, minerals, vitamins, colours (INS 100(i), INS 160b(ii))",Natural colours,KB_HIGH
8901030976117,Horlicks Classic Malt,Horlicks,"Malted cereals (66.7%), milk solids (14%), sugar, wheat gluten, iodized salt, minerals, vitamins, emulsifier (INS 471)",Clean,KB_HIGH
8901803001145,Amrutanjan,Amrutanjan,"NON-FOOD — Pain relief balm",NON-FOOD — PURGE,N/A
8906001050643,Mathers Mango Pickle 200g,Mathers,"Raw mango, salt, spices, edible vegetable oil, acidity regulator",Clean,KB_HIGH
8901155113114,Gits Vermicelli Kheer,Gits,"Vermicelli (durum wheat semolina), milk solids, sugar, cardamom, ghee, raisins",Clean,KB_HIGH
8901808004554,Chocolate Cake Premix,Weikfield,"Sugar, refined wheat flour, cocoa solids, salt, raising agents, emulsifiers, artificial chocolate flavour",Clean,KB_HIGH
8904208600951,Paneer Makhanwala Premix,Rasao Suhana,"Paneer, tomato, butter, cream, spices, salt, sugar, edible vegetable oil",Clean,KB_HIGH
8901030966132,Dark Soya Sauce,Knorr,"Water, soybean extract, salt, sugar, vinegar, acidity regulator, preservative (INS 211)",INS 211 preservative,KB_HIGH
8904037247600,Rolled Oats,Soulful,"Oats (100%)",Clean single-ingredient,KB_HIGH
8901058895735,Maggi Ketchup Rich,Maggi,"Tomato paste, sugar, water, vinegar, salt, spices, acidity regulator (INS 260), preservative (INS 211)",INS 211 preservative,KB_HIGH
8906007280655,Fortune Cotton Seed Oil,Fortune,"Refined cotton seed oil, antioxidant (INS 319), vitamins A & D",INS 319 TBHQ,KB_HIGH
8901441011049,Lijjat Papad,Lijjat,"Urad dal flour, salt, spices (black pepper, cumin), edible vegetable oil",Clean,KB_HIGH
8901042970868,Mutter Paneer Ready Masala,MTR,"Paneer, green peas, tomato, spices, salt, edible vegetable oil",Clean,KB_HIGH
8904145912650,Similac Advance,Abbott,"NON-FOOD — Infant formula/medicine",NON-FOOD — PURGE,N/A
8902901027990,Good Life MP Wheat Chakki Atta 5kg,Good Life,"100% whole wheat flour (MP wheat)",Clean single-ingredient,KB_HIGH
8904132948563,Filtered Groundnut Oil,Independence,"Groundnut oil (filtered), antioxidant (INS 319), vitamins A & D",INS 319 TBHQ,KB_HIGH
8906058611569,Gaia Dark Choco Chip,Gaia,"Sugar, cocoa solids, cocoa butter, emulsifier (INS 322), artificial vanilla flavour",Clean,KB_HIGH
8901023018411,Aer Spray,Godrej,"NON-FOOD — Air freshener",NON-FOOD — PURGE,N/A
8901207040450,Roghan Badam Shireen,Dabur,"Almond oil (sweet)",Clean single-ingredient,KB_HIGH
8906072845483,Roasted Peanut,Jack & Jill,"Roasted peanuts, iodized salt",Clean,KB_HIGH
8904132968813,Roasted & Salted Cashews,Snactac,"Cashew nuts, iodized salt",Clean,KB_HIGH
8902979042987,Mango Thokku,Various,"Raw mango, salt, red chilli, edible vegetable oil, mustard, fenugreek",Clean,KB_HIGH
8901207024856,Chat Cola,Hajmola,"Spices (black salt, cumin, amchur, red chilli), salt, sugar, cola flavour, acidity regulator",Clean,KB_HIGH
8904132918214,Besan Ladoo,Snactac,"Gram flour (besan), sugar, ghee, cardamom",Clean,KB_HIGH
8906010070144,Ganesh Mummy's Own,Ganesh Mummy's Own,"Verify specific product",Verify,KB_MEDIUM
8905507035567,Maida,First Crop,"Refined wheat flour (maida)",Clean single-ingredient,KB_HIGH
8905507025087,Rajma Red,First Crop,"Rajma (kidney beans)",Clean single-ingredient,KB_HIGH
8901192104229,Catch Coriander 200g,Catch,"Coriander powder (100%)",Clean single-ingredient,KB_HIGH
8904053502462,Goldiee Red Chilli 200g,Goldiee,"Red chilli powder (100%)",Clean single-ingredient,KB_HIGH
8902901222456,Cardamom,Various,"Cardamom (100%)",Clean single-ingredient,KB_HIGH
8906040251711,Dates,Various,"Dates (100%)",Clean single-ingredient,KB_HIGH
8906040250240,Dates,Various,"Dates (100%)",Clean single-ingredient,KB_HIGH
8906044443501,Coffee Crunchettes,Various,"Verify specific product",Verify,KB_MEDIUM
8901155413313,Gits Ready Meals - Paneer Tikka Masala,Gits,"Paneer, tomato, spices, salt, edible vegetable oil, cream",Clean,KB_HIGH
8902901222999,Till Nylon 100gm,Good Life,"Sesame seeds (till)",Clean single-ingredient,KB_HIGH
8901192108029,Catch Jeera Powder 50g,Catch,"Cumin powder (100%)",Clean single-ingredient,KB_HIGH
8903236700244,Coffee Booster,Cosmix,"Coffee blend, herbal extracts, spices",Clean,KB_HIGH
8901786191000,Everest Super Garam Masala,Everest,"Coriander, cumin, black pepper, cloves, cinnamon, cardamom, bay leaf, nutmeg, mace",Clean spice blend,KB_HIGH
8906011730542,Ashiver,Various,"Verify specific product",Verify,KB_MEDIUM
8904137452515,Chukde Poppy Seeds,Chukde,"Poppy seeds (khus khus)",Clean single-ingredient,KB_HIGH
8908002753264,Double Toned Milk,Red Cow,"Double toned milk, vitamins A & D",Clean,KB_HIGH
8903151720112,Laxminarayan Potato Chiwda,Laxminarayan,"Potato, edible vegetable oil, peanuts, sago, salt, spices, colours (INS 160c)",INS 160c colour,KB_HIGH
8902433009303,Snickers,Snickers,"Sugar, peanuts, glucose syrup, milk solids, cocoa butter, cocoa mass, emulsifiers, salt",Clean,KB_HIGH
8901393018530,Alpenliebe Just Jelly,Just Jelly,"Sugar, glucose syrup, gelatin, fruit flavour, acidity regulator, colours",Verify colours,KB_HIGH
8901719107665,Biskit,Parle,"Refined wheat flour, sugar, edible vegetable oil, invert syrup, raising agents, emulsifiers",Clean,KB_HIGH
8901389001898,Cacao Reserve Belgium Melt,Sos Save Our Souls,"Sugar, cocoa solids, cocoa butter, milk solids, emulsifiers, flavours",Clean,KB_HIGH
8905672622333,Fasola Biała Konser,Moc Warzyw Dino,"White beans, water, salt",Clean,KB_MEDIUM
8908026382006,Tofu,Mothers Nature,"Soybean, water, coagulant",Clean,KB_HIGH
8906084381597,Classic Bhakharwadi,Jagdish,"Refined wheat flour, gram flour, edible vegetable oil, spices, salt, sugar, coconut, sesame seeds",Clean,KB_HIGH
8903023006078,Kabuli Chana,Vedaka,"Kabuli chana (white chickpeas)",Clean single-ingredient,KB_HIGH
8906150460034,Roasted Salted Magic Mix,Sao Foods,"Mixed nuts, edible vegetable oil, salt, spices",Clean,KB_HIGH
8901874131420,Valor Papdi,Kitchen Xpress,"Refined wheat flour, edible vegetable oil, salt, spices",Clean,KB_HIGH
8906141461484,Mixed Veg,Vimal,"Mixed vegetables (frozen)",Clean,KB_HIGH
8904063229885,Cheese Balls,Minute Khana,"Corn flour, edible vegetable oil, cheese powder, salt, spices, flavour enhancers",Clean,KB_HIGH
8901148248878,Stamlo 5,Various,"NON-FOOD — Medicine",NON-FOOD — PURGE,N/A
8906108190198,Chunky Butter Chicken Spread,Licious,"Chicken, butter, tomato, cream, spices, salt, sugar, edible vegetable oil",Clean,KB_HIGH
8909509926731,Kinder Sorpresa,Kinder,"Sugar, milk solids, cocoa butter, cocoa mass, emulsifiers, flavours, toy inside",Clean,KB_HIGH
8901725101435,Jalimals,Various,"Verify specific product",Verify,KB_MEDIUM
8904022900084,Brown Bread,Various,"Whole wheat flour, water, sugar, yeast, salt, edible vegetable oil, preservative (INS 282)",INS 282 preservative,KB_HIGH
8904063210678,Roasted Crushed Peanuts,Haldiram's,"Roasted peanuts (crushed), iodized salt",Clean,KB_HIGH
8901155115415,Dahi Vada Mix,Gits,"Urad dal flour, spices, salt, raising agents",Clean,KB_HIGH
8907931000449,Garden Veggie Straws,Various,"Potato starch, potato flour, edible vegetable oil, salt, spinach powder, tomato powder",Clean,KB_MEDIUM
8906057810062,Spicy Plantain Chips,Various,"Plantain, edible vegetable oil, spices, iodized salt",Clean,KB_HIGH
8904011502541,Jaggery Powder,Double Horse,"Jaggery powder (100%)",Clean single-ingredient,KB_HIGH
8904293731691,Indie Flavours Bombay Mixture,Indie Flavours/Flipkart,"Rice flakes, gram flour, edible vegetable oil, peanuts, sago, salt, spices, raising agents, colours (INS 160c)",INS 160c colour,KB_HIGH
8904084900633,Imitation Snow Crab,Various,"Surimi (fish paste), starch, salt, sugar, egg white, crab flavour, colours",Clean,KB_MEDIUM
8906080601576,Aam Padpad,Paper Boat,"Water, mango pulp, sugar, acidity regulators",Clean,KB_HIGH
8904215501661,ujoygnhyyhyyhhggyhhh,ducthv,"NON-FOOD — Invalid/nonsense entry",NON-FOOD — PURGE,N/A
8901205027705,White Tea,Various,"White tea (100%)",Clean single-ingredient,KB_HIGH
8906002770694,Mini Classic Cold Coffee,Various,"Instant coffee, sugar, milk solids, emulsifier, flavours",Clean,KB_MEDIUM
8908020709007,Elemental Manga+,ELEMENTAL,"Verify specific product",Verify,KB_MEDIUM
8906165783906,Biozyme Performance Whey,MuscleBlaze,"Whey protein concentrate, emulsifier (INS 322), artificial flavour, sweetener",Clean,KB_HIGH
8906055442524,Organic Tattva Mustard Oil,Organic Tattva,"Organic mustard oil (cold-pressed)",Clean single-ingredient,KB_HIGH
8904391593333,Mango Mallika,Unknown Brand,"Mango (Mallika variety)",Clean single-ingredient,KB_HIGH
8906135071453,Millet Cereal,Native Food Store,"Millet flour, raising agents, salt",Clean,KB_HIGH
8901440210795,Turmeric Powder,Eastern,"Turmeric powder (100%)",Clean single-ingredient,KB_HIGH
8908008116018,Um Rupa,M/S Marwein Group,"Verify specific product",Verify,KB_MEDIUM
8906033740208,McVitie's TASTIES BUTTER COOKIES,McVitie's,"Refined wheat flour, sugar, butter, edible vegetable oil, raising agents, emulsifiers, artificial butter flavour",Clean,KB_HIGH
8908001551007,KOKANRAJ KOKUM SYRUP,KOKANRAJ,"Kokum extract, sugar, water, acidity regulator",Clean,KB_HIGH
8902901224726,Toor Dal 500g,Good Life,"Toor dal (pigeon pea)",Clean single-ingredient,KB_HIGH
8906009820323,Silver Coin Suji,Silver Coin,"Semolina (suji/rava) from wheat",Clean single-ingredient,KB_HIGH
8906167310643,Arhar Dal 1kg,Various,"Arhar/Toor dal (pigeon pea)",Clean single-ingredient,KB_HIGH
8902901224733,Toor Dal 1kg,Good Life,"Toor dal (pigeon pea)",Clean single-ingredient,KB_HIGH
8904089920629,Curd,Heritage,"Pasteurised toned milk & active lactic cultures",Clean,KB_HIGH
8906005618603,Mini Swiss Roll (Choco-Vanilla) [10 Rs],Winkles,"Refined wheat flour, sugar, eggs, edible vegetable oil, cocoa solids, vanilla flavour, raising agents, emulsifiers",Clean,KB_HIGH
8904335601326,Chia Seeds,Yogabar,"Chia seeds (100%)",Clean single-ingredient,KB_HIGH
8906079010334,Luvit Pops!,Luvit,"Verify specific product",Verify,KB_MEDIUM
8904132972469,Good Life Till White 200g,Good Life,"White sesame seeds (till)",Clean single-ingredient,KB_HIGH
8901088760454,Saffola Oats,Saffola,"Oats (100%)",Clean single-ingredient,KB_HIGH
8901058006032,Maggi Cup Noodles,Maggi,"Noodles: Refined wheat flour, palm oil, salt, wheat gluten, thickeners; Tastemaker: salt, spices, sugar, flavour enhancers (INS 621, INS 627, INS 631), antioxidant (INS 319)",INS 621 + INS 319,KB_HIGH
8901063026346,NutriChoice Digestive,Britannia,"Whole wheat flour (71%), sugar, edible vegetable oil (palm), raising agents (INS 503(ii), INS 500(ii)), salt, emulsifiers (INS 471, INS 322), added vitamins & minerals",Clean,KB_HIGH
8901725008888,Aashirvaad Shudh Chakki Atta,ITC,"100% whole wheat flour",Clean single-ingredient,KB_HIGH
8906038230834,Chicken Malai Tikka,Zorabian,"Chicken, cream, spices, salt, edible vegetable oil",Clean,KB_HIGH
8901747005599,Instant Saffron Tea,Wagh Bakri,"Black tea, saffron, spices, sugar, milk solids",Clean,KB_HIGH
8906108530543,Inchi Noodles,Various,"Refined wheat flour, palm oil, salt, thickeners; Tastemaker: salt, spices, flavour enhancers (INS 621)",INS 621 MSG,KB_HIGH
8901725004217,Bingo Tedhe Medhe Tomato,Bingo,"Corn grits, edible vegetable oil (palmolein), rice grits, gram flour, spices, salt, sugar, tomato powder, flavour enhancers (INS 621, INS 627, INS 631), colours (INS 160c)",INS 621 MSG + INS 160c,KB_HIGH
8904209303455,Coriander Thokku,Aachi,"Coriander, salt, spices, edible vegetable oil, acidity regulator",Clean,KB_HIGH
8901542000775,Nycil Powder,Nycil,"NON-FOOD — Talcum powder",NON-FOOD — PURGE,N/A
8904180000688,Tandoori Curry Paste,Vik's,"Spices, salt, sugar, tomato powder, onion powder, garlic, ginger, edible vegetable oil",Clean,KB_HIGH
8906044653108,Tomato Paste,Ahlan,"Tomato paste, salt",Clean,KB_HIGH
8906107173642,Veg Supreme Pizza Minis,Prasuma,"Refined wheat flour, cheese, tomato sauce, vegetables, edible vegetable oil, spices, salt",Clean,KB_HIGH
8906153880310,Gulkand,Two Brothers Organic Farms,"Rose petals, sugar",Clean,KB_HIGH
8906029140944,Cut Mango Pickle,Mambalam Iyers,"Raw mango, salt, spices, edible vegetable oil, acidity regulator",Clean,KB_HIGH
8908013673216,Spirit 750ml Old,Various,"Alcoholic beverage",ALCOHOL — SEPARATE,KB_HIGH
8904004420487,MixTURE ENGALURU,Haldiram's,"Rice flakes, gram flour, edible vegetable oil, peanuts, sago, salt, spices, raising agents, colours (INS 160c)",INS 160c colour,KB_HIGH
8904004420418,Spicy Mixture,Haldiram's,"Rice flakes, gram flour, edible vegetable oil, peanuts, sago, salt, spices, raising agents, colours (INS 160c)",INS 160c colour,KB_HIGH
8908003714042,Mysore Pak Konaka FOODS,Konaka,"Gram flour, sugar, ghee, cardamom",Clean,KB_HIGH
8906020495081,Ghee Laddoo,Various,"Gram flour, sugar, ghee, cardamom",Clean,KB_HIGH
8906020490482,Boondi Laddoo,Various,"Gram flour, sugar, ghee, cardamom",Clean,KB_HIGH
8901042960340,Rasogolla,Various,"Milk solids (chenna), sugar, cardamom",Clean,KB_HIGH
8906108191334,Farm Fresh Classic Eggs Pack Of 12,Licious,"Eggs (12)",Clean single-ingredient,KB_HIGH
8904459600335,Kodo Millet Noodles,Satvyk,"Kodo millet flour, salt",Clean,KB_HIGH
8908004415443,Orbix S,Various,"NON-FOOD — Verify",NON-FOOD — PURGE,N/A
8908004415535,Orbix L,Various,"NON-FOOD — Verify",NON-FOOD — PURGE,N/A
8904063226563,Mexilla Flamin' Hot Tortilla Chips,Haldiram's,"Corn flour, edible vegetable oil, spices, salt, flavour enhancers (INS 621), colours (INS 160c)",INS 621 MSG,KB_HIGH
8908015450075,Steel Cut Oats,WeFeasto,"Steel cut oats (100%)",Clean single-ingredient,KB_HIGH
8902979011532,KESAR FLAVOURED MILK,Cavin's,"Toned milk, sugar, kesar (saffron) flavour, stabilizers, emulsifiers, colour (INS 160a)",Clean,KB_HIGH
8901725013387,Chocolate Meltz,Dark Fantasy,"Choco crème (sugar, refined palmolein, cocoa solids), refined wheat flour, sugar, invert syrup, liquid glucose, cocoa solids, milk solids, butter, raising agents, emulsifiers, salt",Clean,KB_HIGH
8906043348104,Salt Electrolytes,Supply 6,"Electrolyte salts (sodium, potassium, magnesium)",Clean,KB_HIGH
8906169990430,Kerala Tapioca Chips,Sweet Karam Coffee,"Tapioca, edible vegetable oil, salt, spices",Clean,KB_HIGH
8906083020459,Assorted Nutri Bar,Mindful,"Multigrain blend, nuts, dried fruits, honey, edible vegetable oil",Clean,KB_HIGH
8908000391482,Wheafree,Various,"Verify specific product",Verify,KB_MEDIUM
8906021061650,Molsis Zahidi Dates,Bolas Agro,"Wet dates (Zahidi) (100%)",Clean single-ingredient,KB_HIGH
8902080304059,7Up Super Duper 750ml,PepsiCo,"Carbonated water, sugar, acidity regulators (INS 330, INS 331(i)), natural lemon-lime flavouring, preservative (INS 211)",INS 211 preservative,KB_HIGH
8901491503013,Yellow Salted Lays,Lay's,"Potato, edible vegetable oil (palmolein, rice bran oil), iodized salt",Clean,KB_HIGH
8902579001285,Frooti Mix Fruit,Various,"Water, mixed fruit juice concentrate, sugar, acidity regulator, flavours",Clean,KB_HIGH
8901262070058,Amul Fruit 'N' Nut,Amul,"Cocoa solids, sugar, cocoa butter, almonds (8%), raisins (5%), emulsifiers (322,476), artificial flavouring substances (cocoa, vanilla)",Clean,KB_HIGH"""

def run():
    print("=== EXECUTING BATCH 46 INGREDIENTS INTEGRATION & PURGE ===")
    df_all = pd.read_csv(all_supabase_csv, dtype=str)
    df_confirmed = pd.read_csv(confirmed_csv, dtype=str)
    df_needs_ver = pd.read_csv(needs_ver_csv, dtype=str)

    df_all['barcode'] = df_all['barcode'].str.strip()
    df_confirmed['barcode'] = df_confirmed['barcode'].str.strip()
    df_needs_ver['barcode'] = df_needs_ver['barcode'].str.strip()
    
    batch_reader = csv.DictReader(io.StringIO(BATCH46_DATA.strip()))
    batch_46_rows = list(batch_reader)

    elevated_count = 0
    added_count = 0
    purged_count = 0

    for item in batch_46_rows:
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

    print(f"Batch 46 Processing Summary:")
    print(f"  Elevated from Needs Verification to Confirmed: {elevated_count}")
    print(f"  Newly added to Confirmed: {added_count}")
    print(f"  Purged Non-Food Barcodes: {purged_count}")
    print(f"  Final Master CSV Count: {len(df_all)}")
    print(f"  Final Confirmed CSV Count: {len(df_confirmed)}")
    print(f"  Final Needs Verification CSV Count: {len(df_needs_ver)}")

if __name__ == "__main__":
    run()
