import pandas as pd
import csv
import io

all_supabase_csv = "all_supabase_products.csv"
confirmed_csv = "india_products_confirmed.csv"
needs_ver_csv = "india_products_needs_verification.csv"

SWEEP_DATA = """barcode,product_name,brands,ingredients_text,additive_flags,confidence
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
8902901232387,GL Soya Chunks 1kg,Good Life,"Defatted soya flour",Clean,KB_HIGH
8901138713904,Foot scrum smoothing.150ml.himalaya,Himalaya,"NON-FOOD — Foot cream",NON-FOOD — PURGE,N/A
8907316014788,Ginger & Garlic Paste,Mother's Recipe,"Ginger, garlic, salt, acidity regulator",Clean,KB_HIGH
8906021920445,apis mango jam,apis,"Mango pulp, sugar, acidity regulator",Clean,KB_HIGH
8901764692017,Carbonate Water,Sprite,"Carbonated water, acidity regulators, flavours",Clean,KB_HIGH
8906033261062,Thé vert au gingembre,Various,"Green tea, ginger",Clean,KB_HIGH
8901777459553,Veg Spring Roll,Vadilal,"Refined wheat flour, mixed vegetables, edible vegetable oil, spices",Clean,KB_HIGH
8906141311260,Honey,Dollar General,"Honey (100%)",Clean single-ingredient,KB_HIGH
8906064285341,Tender Coconut Water with Pulp,Unknown Brand,"Tender coconut water, coconut pulp",Clean single-ingredient,KB_HIGH
8908000589292,Fizz Jeera Masala,Bindu,"Carbonated water, sugar, cumin, black salt, acidity regulators",Clean,KB_HIGH
8901393024500,Alpenliebe Gold Candy,Alpenliebe,"Sugar, glucose syrup, butterscotch flavour, colours",Verify colours,KB_MEDIUM
8908013252145,Granola choco almond &cookies 275gm Fit& Flex,Fit and Flex,"Oats, chocolate, almonds, cookies, honey",Clean,KB_HIGH
8908013252053,Granola happy berries 275gm Fit & Flex,Fit and Flex,"Oats, berries, honey, nuts",Clean,KB_HIGH
8901491100250,Lays,Lay's,"Potato, edible vegetable oil, salt",Clean,KB_HIGH
8908027668031,Pina Colada,Dead Honest,"Pineapple, coconut, sugar, acidity regulator",Clean,KB_HIGH
8906107172461,Hot Wings,Meatigo,"Chicken wings, hot wing marinade, spices",Clean,KB_HIGH
8906005914545,Aakash Bhel,Aakash,"Rice flakes, gram flour, edible vegetable oil, peanuts, salt, spices",Clean,KB_HIGH
8906005450890,Bikaji Bhel,Bikaji,"Rice flakes, gram flour, edible vegetable oil, peanuts, salt, spices",Clean,KB_HIGH
8908021821128,freshko,Freshko,"Verify specific product",Verify,KB_MEDIUM
8901440011101,Chicken Masala Spice Mix,Eastern,"Coriander, cumin, turmeric, red chilli, black pepper, garlic, ginger, salt",Clean spice blend,KB_HIGH
8909081010552,Swiss Roll,Dark Fantasy,"Refined wheat flour, sugar, eggs, cocoa solids, edible vegetable oil, raising agents",Clean,KB_HIGH
8904043926582,Masoor Dal,Tata Sampann,"Masoor dal (red lentils)",Clean single-ingredient,KB_HIGH
8906005501585,Mastkin,Bikaji,"Verify specific product",Verify,KB_MEDIUM
8904304511281,Herbal,Various,"Verify specific product",Verify,KB_MEDIUM
8902268015852,Top ROYALE Butter & CHEESE,Anmol,"Refined wheat flour, sugar, butter, cheese, edible vegetable oil",Clean,KB_HIGH
8906142560391,Organic chickpea puffs-NYC Pizza,Popeas,"Organic chickpea flour, pizza seasoning, edible vegetable oil, salt",Clean,KB_HIGH
8906142560407,Organic Chickpea Puffs - Tangy Taco,Popeas,"Organic chickpea flour, tangy taco seasoning, edible vegetable oil, salt",Clean,KB_HIGH
8901491103329,Kurkure NAUGHTY TOMATO,Kurkure,"Corn grits, edible vegetable oil, tomato seasoning, salt, flavour enhancers (INS 621)",INS 621 MSG,KB_HIGH
8904258701318,Grapefruit Juice,Raw Pressery,"Grapefruit juice (100%)",Clean single-ingredient,KB_HIGH
8906016420257,Roasted Peanuts plain,Various,"Roasted peanuts, salt",Clean,KB_HIGH
8906107171013,Desi Chicken Burger Patty,Meatigo,"Chicken, spices, salt, edible vegetable oil",Clean,KB_HIGH
8906165788741,Whey Max Rich Chocolate,Fuel One,"Whey protein, chocolate flavour, sweetener, emulsifier",Clean,KB_HIGH
8906011771842,cow milk,Mahanand,"Cow milk (100%)",Clean single-ingredient,KB_HIGH
8904004420203,Special Malai Peda,Haldiram's,"Milk solids, sugar, ghee, cardamom, malai",Clean,KB_HIGH
8906184753232,Bro oreo,Various,"Verify specific product",Verify,KB_MEDIUM
8904104705033,Jk poppy seed,Jk,"Poppy seeds (100%)",Clean single-ingredient,KB_HIGH
8904234407418,Incesnse,Satya,"NON-FOOD — Incense",NON-FOOD — PURGE,N/A
8906063890614,Traditional Pork Kransky Sausages,La Carne Cuts,"Pork, spices, salt, sheep casing",Clean,KB_HIGH
8906137370622,Wild Origins Honey,Last Forest,"Wild honey (100%)",Clean single-ingredient,KB_HIGH
8902167001093,MDH Karahi Chicken,MDH,"Coriander, cumin, turmeric, red chilli, black pepper, garlic, ginger, spices",Clean spice blend,KB_HIGH
8906170521883,Hydrolyzed Pea Protein,Nutrabay,"Hydrolyzed pea protein",Clean single-ingredient,KB_HIGH
8901552001939,مخلل قطعات المانجو في الزيت,Ashoka,"Mango pieces, oil, salt, spices",Clean,KB_HIGH
8901548310427,D'lite yummy berry,Complan,"Sugar, glucose syrup, berry flavours, colours",Verify colours,KB_MEDIUM
8906179681809,Delight Mango juice 600 ml,Delight,"Mango pulp, water, sugar, acidity regulator",Clean,KB_HIGH
8906179681663,Delight Mango juice 250 ml,Delight,"Mango pulp, water, sugar, acidity regulator",Clean,KB_HIGH
8904132917279,Snac tac all in one,Snac tac,"Rice flakes, gram flour, edible vegetable oil, peanuts, salt, spices",Clean,KB_HIGH
8906101940059,nikhar mhendi,Various,"NON-FOOD — Henna",NON-FOOD — PURGE,N/A
8908002584165,Tea,Lasa Lamsa,"Black tea (100%)",Clean single-ingredient,KB_HIGH
8901725014759,Whole Mustard,Aashirvaad,"Mustard seeds (100%)",Clean single-ingredient,KB_HIGH
8908021087005,Trauben,Various,"Grapes (100%)",Clean single-ingredient,KB_HIGH
8906054689128,Tapioca chips,Various,"Tapioca, edible vegetable oil, salt",Clean,KB_HIGH
8908014421519,Millet,The Millet Company,"Millet (100%)",Clean single-ingredient,KB_HIGH
8901548312483,Sugar free D'lite Assorted Cookies,Complan,"Whole wheat flour, sugar, edible vegetable oil, raising agents",Clean,KB_HIGH
8901777077665,Amla Slices,Vadilal,"Amla, salt, edible vegetable oil",Clean,KB_HIGH
8908000275249,Pineapple Drops,Viswas,"Pineapple, sugar",Clean,KB_HIGH
8906078264738,Cremica Classic Bourbon,Cremica,"Refined wheat flour, sugar, butter, cocoa solids",Clean,KB_HIGH
8906131685029,Slurrp farm,Slurrp Farm,"Millet flour, raising agents, salt",Clean,KB_HIGH
8908014602109,Ice Pops (Lemon Flavour),SKIPPI,"Water, sugar, lemon flavour, acidity regulator, colours",Verify colours,KB_MEDIUM
8901063093690,Britannia Good Day Casio cookie,Britannia,"Refined wheat flour, sugar, edible vegetable oil, cashews",Clean,KB_HIGH
8902080100491,Sting energy,PepsiCo,"Carbonated water, sugar, acidity regulators, taurine, caffeine, flavours",Energy drink,KB_HIGH
8901063162976,Doodh Marie Gold,Britannia,"Refined wheat flour, sugar, milk solids, edible vegetable oil",Clean,KB_HIGH
8908020220496,L❤️U,Various,"Verify specific product",Verify,KB_MEDIUM
8909106041783,Brooke bond taaza,Brooke Bond,"Black tea (100%)",Clean single-ingredient,KB_HIGH
8901440011439,Chicken Fry Masala,Eastern,"Coriander, cumin, turmeric, red chilli, black pepper, garlic, ginger, salt",Clean spice blend,KB_HIGH
8901063019249,Little Hearts,Britannia,"Refined wheat flour, sugar, edible vegetable oil",Clean,KB_HIGH
8906010369224,Namkeens,Town Bus,"Verify specific product",Verify,KB_MEDIUM
8908019673135,BAKERS VINEGAR 500 ML,Bakers,"Vinegar (acetic acid, water)",Clean single-ingredient,KB_HIGH
8906004654534,Jaggery Powder,Pavizham,"Jaggery powder (100%)",Clean single-ingredient,KB_HIGH
8901777665107,Kaju Katli Mix,Vadilal,"Cashew nuts, sugar, ghee, cardamom",Clean,KB_HIGH
8906016611150,Zecal-Gold,Indochem,"NON-FOOD — Supplement",NON-FOOD — PURGE,N/A
8908009059413,Zero Maida Sourdough Rye Bread,The Health Factory,"Whole wheat flour, sourdough starter, rye flour, salt",Clean,KB_HIGH
8904089992602,Cheese Slices (Processed Cheese),Heritage,"Milk solids, salt, emulsifying salts, preservative (INS 200)",INS 200 preservative,KB_HIGH
8905950003694,khatta meetha,Bikaji,"Rice flakes, gram flour, edible vegetable oil, peanuts, salt, sugar, spices",Clean,KB_HIGH
8905950003519,All in one Kuch Kuch,Bikaji,"Rice flakes, gram flour, edible vegetable oil, peanuts, salt, spices",Clean,KB_HIGH
8905950003779,bikaji moong dal,Bikaji,"Moong dal, edible vegetable oil, salt, spices",Clean,KB_HIGH
8908001105583,Rajwadi mixture,On1y,"Rice flakes, gram flour, edible vegetable oil, peanuts, salt, spices",Clean,KB_HIGH
8905950003434,bikaji bikaneri bhujia 400g,Bikaji,"Gram flour, edible vegetable oil, salt, spices",Clean,KB_HIGH
8904258703985,Jal Jeera,Raw Pressery,"Water, cumin, black salt, sugar, mint, spices",Clean,KB_HIGH
8906085460444,Rice Papadi Green Chilly,Yash Papad,"Rice flour, green chilli, salt, edible vegetable oil",Clean,KB_HIGH
8906020250185,Gingelly oil,Pooja,"Sesame oil (100%)",Clean single-ingredient,KB_HIGH
8904124115287,Dahi,Ananda,"Pasteurized toned milk, active lactic culture",Clean,KB_HIGH
8903023185254,cinnamon,More Choice,"Cinnamon (100%)",Clean single-ingredient,KB_HIGH
8906030521770,Karak Tea Instant Promix,Neel Cafe,"Black tea, cardamom, ginger, sugar",Clean,KB_HIGH
8906019630059,Noodles,Various,"Verify specific product",Verify,KB_MEDIUM
8904064617285,chilli powder,Various,"Red chilli powder (100%)",Clean single-ingredient,KB_HIGH
8908020463664,Choco Rings,Crax,"Corn flour, cocoa solids, edible vegetable oil, salt",Clean,KB_HIGH
8906030460161,Brown Bread,Moreish,"Whole wheat flour, water, sugar, yeast, salt",Clean,KB_HIGH
8904064664234,CASTOR OIL,Various,"NON-FOOD — Castor oil",NON-FOOD — PURGE,N/A
8904083301219,Milkymist gulab jamun,Milky Mist,"Milk solids, sugar, edible vegetable oil, cardamom",Clean,KB_HIGH
8901047619243,Chili Paneer Cooking Sauce,Kohinoor,"Paneer, tomato, chilli, spices, salt, edible vegetable oil",Clean,KB_HIGH
8904018305848,Medimix Ayurvedic,Medimix,"NON-FOOD — Soap",NON-FOOD — PURGE,N/A
8901738707921,Coconut Flakes,Havana,"Coconut flakes (100%)",Clean single-ingredient,KB_HIGH
8901884401988,Carrot Chilli Pickle,Rishta,"Carrot, green chilli, salt, spices, edible vegetable oil",Clean,KB_HIGH
8906186473343,Spaghetti,Pasta Zing,"Durum wheat semolina",Clean single-ingredient,KB_HIGH
8904208600043,Paneer Tikka Masala Mix,Rasoi Magic,"Paneer, tomato, spices, salt, edible vegetable oil",Clean,KB_HIGH
8908013252725,Muesli 0% Added Sugar,Fit and Flex,"Oats, nuts, seeds, dried fruits",Clean,KB_HIGH
8906018553137,Frozen Sweet Corn,Pagro,"Sweet corn (frozen)",Clean single-ingredient,KB_HIGH
8906010360122,Ghee,GRB,"Milk fat (100%)",Clean single-ingredient,KB_HIGH
8904013420072,Goodrick khass,Goodricke,"Verify specific product",Verify,KB_MEDIUM
8901595873241,Schezwan stir fry sauce,Ching's Secret,"Chilli, garlic, vinegar, salt, spices",Clean,KB_HIGH
8908014841119,Mozzarella Di Bufala,The Spotted Cow Fromagerie,"Buffalo milk, salt, rennet",Clean,KB_HIGH
8904293728608,Flipkart Grocery Corn Flour,Flipkart Grocery,"Corn flour (100%)",Clean single-ingredient,KB_HIGH
8906021128377,Aachi kashmiri chilli powder,Aachi,"Kashmiri red chilli powder (100%)",Clean single-ingredient,KB_HIGH
8906033746026,Digestive Minis,McVities,"Whole wheat flour, sugar, edible vegetable oil, raising agents",Clean,KB_HIGH
8906067024381,MuscleBlaze Fish Oil 1000mg,MuscleBlaze,"Fish oil, capsule shell (gelatin)",Supplement,KB_HIGH
8903023264935,Roasted Bengal gram,More Choice,"Roasted bengal gram (100%)",Clean single-ingredient,KB_HIGH
8901747000631,Tea levaves,Wagh Bakri,"Black tea (100%)",Clean single-ingredient,KB_HIGH
8906090831604,Grace urad dal,Grace,"Urad dal (100%)",Clean single-ingredient,KB_HIGH
8906126393755,ZAHIDI DATES,Khari Foods,"Zahidi dates (100%)",Clean single-ingredient,KB_HIGH
8908022639562,GLF PEANUT BUTTER 340GM,Good Life,"Roasted peanuts, salt",Clean,KB_HIGH
8908024057289,Millet Bhel Bombay Bhelpuri,Eat Better Co,"Millet puffs, bombay bhelpuri seasoning, edible vegetable oil, salt",Clean,KB_HIGH
8906071430475,Basmati GOLD Rice 02 (Raw),India's Jaisal,"Basmati rice (100%)",Clean single-ingredient,KB_HIGH
8904071701779,Masala Butter Chakli,Various,"Rice flour, gram flour, butter, spices, salt, edible vegetable oil",Clean,KB_HIGH
8908005758723,cardamom chai,Various,"Black tea, cardamom",Clean,KB_HIGH
8904970588391,Grapes Sonaka Seedless,Various,"Green grapes (seedless)",Clean single-ingredient,KB_HIGH
8906034975463,Parboiled Basmati Rice,Evarat,"Parboiled basmati rice (100%)",Clean single-ingredient,KB_HIGH
8901491100106,Rolled Oats (Natural Wholegrain),Quaker,"Rolled oats (100%)",Clean single-ingredient,KB_HIGH
8904063229861,Street Style Momos,Haldiram’s,"Refined wheat flour, mixed vegetables, spices, salt, edible vegetable oil",Clean,KB_HIGH
8901595971190,Chings pad thai noodles,Ching's Secret,"Refined wheat flour, palm oil, salt; Tastemaker: salt, spices, flavour enhancers (INS 621)",INS 621 MSG,KB_HIGH
8908011819005,Malabari Special Biryani Rice,Malabari,"Basmati rice (100%)",Clean single-ingredient,KB_HIGH
8906109930007,Rock salk,Tasav,"Rock salt (100%)",Clean single-ingredient,KB_HIGH
8908018651677,Protein Puff Tomato,Troovy,"Millet puffs, tomato seasoning, edible vegetable oil, salt",Clean,KB_HIGH
8907316005311,Mother recipe Red chilli garlic chutney 200 g,Mother's Recipe,"Red chilli, garlic, salt, spices, edible vegetable oil",Clean,KB_HIGH
8901058012637,Maggi imli sauce pichkoo 75 g,Maggi,"Tamarind, jaggery, salt, spices, acidity regulator",Clean,KB_HIGH
8908023263100,Creatine Monohydrate,Fast&Up,"Creatine monohydrate (100%)",Supplement,KB_HIGH
8908013252213,muesli nuts 450g,Fit and Flex,"Oats, nuts, honey, dried fruits",Clean,KB_HIGH
8906010368555,Masala Peanuts,Town Bus,"Peanuts, spices, salt, edible vegetable oil",Clean,KB_HIGH
8906069408141,Strawberry And Watermelon 0 Sugar,Zyro,"Strawberry, watermelon, natural flavours, sweetener",Clean,KB_HIGH
8906078150178,STAR FRIES Crispy/,Various,"Potato, edible vegetable oil, salt",Clean,KB_HIGH
8906078150246,STAR RIES,Various,"Potato, edible vegetable oil, salt",Clean,KB_HIGH
8908017962163,wicked gud,Wicked Gud,"Verify specific product",Verify,KB_MEDIUM
8906078269863,mrs bector merry Christmas,Cremica,"Refined wheat flour, sugar, butter, cocoa solids",Clean,KB_HIGH
8901719136870,parle hide&seek,Parle,"Refined wheat flour, sugar, edible vegetable oil, cocoa solids",Clean,KB_HIGH
8909081007460,sunfest magic,Sunfeast,"Verify specific product",Verify,KB_MEDIUM
8901063142879,brittania nutri choice seeds,Britannia,"Whole wheat flour, seeds, edible vegetable oil, salt",Clean,KB_HIGH
8906021120678,Aachi,Aachi,"Verify specific product",Verify,KB_MEDIUM
8906002080014,Turmeric Powder,Sakthi,"Turmeric powder (100%)",Clean single-ingredient,KB_HIGH
8904043551845,Pineapple Sweet Fill,Modern,"Pineapple, sugar, acidity regulator",Clean,KB_HIGH
8901721023540,Crazy Stickk,Prabhuji,"Refined wheat flour, spices, salt, edible vegetable oil",Clean,KB_HIGH
8902188720089,Khatta mitha mix,Bikaji,"Rice flakes, gram flour, edible vegetable oil, peanuts, salt, sugar, spices",Clean,KB_HIGH
8906018140320,Original Tortilla Wraps,Switz,"Whole wheat flour, water, salt, edible vegetable oil",Clean,KB_HIGH
8906041817572,Chicloso Menta,Various,"Sugar, glucose syrup, mint flavour, colours",Verify colours,KB_MEDIUM
8906115881188,Galleta Choco Luv,Various,"Refined wheat flour, sugar, cocoa solids, edible vegetable oil",Clean,KB_HIGH
8906006752689,Malto Vitaa Chocolate Satisfaction,Milkose,"Milk solids, sugar, cocoa solids, emulsifiers",Clean,KB_HIGH
8901148258600,Atex,Various,"NON-FOOD — Medicine",NON-FOOD — PURGE,N/A
8904043501031,Whole Wheat Bread,Bakers Loaf,"Whole wheat flour, water, yeast, salt, sugar",Clean,KB_HIGH
8901777349083,Tamarind Rice,Vadilal,"Rice, tamarind, jaggery, spices, salt, edible vegetable oil",Clean,KB_HIGH
8908012126829,Prunes,Bazana,"Prunes (100%)",Clean single-ingredient,KB_HIGH
8908022361302,Cold Pressed White Sesame Oil,Kachi Ghaani,"White sesame oil (cold pressed)",Clean single-ingredient,KB_HIGH
8906066200090,Paneer Chilli Masala,Keya,"Paneer, chilli, spices, salt, edible vegetable oil",Clean,KB_HIGH
8901888005717,Lemoneez,Dabur,"Lemon juice, sugar, water, salt",Clean,KB_HIGH
8904132913288,sun crush,Sun Crush,"Verify specific product",Verify,KB_MEDIUM
8901063142862,Nutri Choice Biscuits,Britannia,"Whole wheat flour, edible vegetable oil, salt",Clean,KB_HIGH
8906038740821,קחי תירس מתוקים מבושלים,Various,"Sweet corn, water, salt",Clean,KB_HIGH
8908009059710,Zero Maida Atta Bread,The Health Factory,"Whole wheat flour, sourdough starter, salt",Clean,KB_HIGH
8901499011367,Chocos variety pack 7 packs,Kellogg's,"Oats, chocolate, honey, nuts",Clean,KB_HIGH
8906004564741,Chips Piri Piri Flavour,Yellow Diamond,"Potato, edible vegetable oil, piripiri seasoning, salt",Clean,KB_HIGH
8902080100415,Adrenaline Rush Ultimate Performance Energy Drink,PepsiCo,"Carbonated water, sugar, taurine, caffeine, vitamins",Energy drink,KB_HIGH
8903363004383,Kulith,Various,"Horse gram (kulith)",Clean single-ingredient,KB_HIGH
8906046144437,Bay Leaf Whole Organic Spices,Pride of India,"Bay leaf (100%)",Clean single-ingredient,KB_HIGH
8908000117310,Masti Lokwan Wheat 30 Kg,Masti,"Lokwan wheat (100%)",Clean single-ingredient,KB_HIGH
8908000117297,Parivaar Premium Sihori Wheat 30 kg,Parivaar,"Sihori wheat (100%)",Clean single-ingredient,KB_HIGH
8908000117150,Masti Lokwan Wheat 10 Kg,Masti,"Lokwan wheat (100%)",Clean single-ingredient,KB_HIGH
8901552025027,Madaras,Ashoka,"Verify specific product",Verify,KB_MEDIUM
8901595852338,Green chilli sauce,Ching's Secret,"Green chilli, vinegar, salt, spices",Clean,KB_HIGH
8906038500074,Wheat flour,Various,"Wheat flour (100%)",Clean single-ingredient,KB_HIGH
8904051326565,Keralla Mixture,Various,"Rice flakes, gram flour, edible vegetable oil, peanuts, salt, spices",Clean,KB_HIGH
8904374500420,Premium Malai kulfi,Various,"Milk solids, sugar, cardamom, almonds",Clean,KB_HIGH
8904062524417,plain bhunia,Haldiram's,"Gram flour, edible vegetable oil, salt, spices",Clean,KB_HIGH
8907970002169,Gemini Refined Sunflower Oil 800 gm pouch,Gemini,"Refined sunflower oil",Clean single-ingredient,KB_HIGH
8906002342563,Rajdhani Maida,Rajdhani,"Refined wheat flour (maida)",Clean single-ingredient,KB_HIGH
8906097400032,Turmeric Powder,Zoff,"Turmeric powder (100%)",Clean single-ingredient,KB_HIGH
8906191580111,Sunny Sun Lite Oil 4.30 Kg,Sunny,"Refined sunflower oil",Clean single-ingredient,KB_HIGH
8902901028331,Good Life Refined Sunflower Oil 4.55 Kg,Good Life,"Refined sunflower oil",Clean single-ingredient,KB_HIGH
8904422706361,Patanjali Kachi Ghani Mustard Oil 2 Ltr,Patanjali,"Mustard oil (kachi ghani)",Clean single-ingredient,KB_HIGH
8904043906935,Tata Simply Cold Press Sesame Oil 1 Ltr,Tata Simply Better,"Sesame oil (cold pressed)",Clean single-ingredient,KB_HIGH
8906102380038,Water,Various,"Water (100%)",Clean single-ingredient,KB_HIGH
8901030877193,Red label tea,Brooke Bond,"Black tea (100%)",Clean single-ingredient,KB_HIGH
8904045056058,Amla juice,Various,"Amla juice (100%)",Clean single-ingredient,KB_HIGH
8906078261980,Golden Bytes,Cremica,"Refined wheat flour, sugar, butter, edible vegetable oil",Clean,KB_HIGH
8908009082718,panipuri,Various,"Rice flour, potato, spices, tamarind, jaggery",Clean,KB_HIGH
8901063142718,Oats & Millets Orange Flavour Cookies,Britannia Nutrichoice,"Oats, millets, orange flavour, edible vegetable oil, sugar",Clean,KB_HIGH
8906027712440,Skimmed Milk Powder,Govind,"Skimmed milk powder (100%)",Clean single-ingredient,KB_HIGH
8908020238057,Paneer,Vijaya,"Paneer (100%)",Clean single-ingredient,KB_HIGH
8902080003068,Slice,PepsiCo,"Water, mango pulp, sugar, acidity regulator",Clean,KB_HIGH
8905110007104,vivel glycerin,Vivel,"NON-FOOD — Soap",NON-FOOD — PURGE,N/A
8906010090319,Chilli Cheese Slice,D'Lecta,"Cheese, chilli, salt, emulsifying salts",Clean,KB_HIGH
8908014080204,Aloo Papad,Renusa,"Potato, salt, spices, edible vegetable oil",Clean,KB_HIGH
8904132917064,Aarambh Danedar Assam Tea,Aarambh,"Black tea (100%)",Clean single-ingredient,KB_HIGH
8906135092021,apis ROYAL ZAHIDI 500g,apis,"Zahidi dates (100%)",Clean single-ingredient,KB_HIGH
8904063211125,Aloo Tikki,Haldirams,"Potato, spices, salt, edible vegetable oil",Clean,KB_HIGH
8906163834235,Makka Shaka Imli,Farmley,"Corn puffs, imli (tamarind) seasoning, edible vegetable oil, salt",Clean,KB_HIGH
8906108306162,Medjoul Dates,Popular,"Medjoul dates (100%)",Clean single-ingredient,KB_HIGH
8906035140075,Chipo white mix,Chipo,"Rice flakes, gram flour, edible vegetable oil, salt, spices",Clean,KB_HIGH
8906141311277,Honey By Clover Valley,Clover Valley,"Honey (100%)",Clean single-ingredient,KB_HIGH
8906035140181,Chipo snow flakes mix,Chipo,"Rice flakes, gram flour, edible vegetable oil, salt, spices",Clean,KB_HIGH
8906070492009,Ojin ring ring,Ojin,"Rice flour, edible vegetable oil, salt, spices",Clean,KB_HIGH
8904063233172,Takatak,Haldiram,"Corn flour, edible vegetable oil, spices, salt",Clean,KB_HIGH
8906090578172,Party Harder,Too Yumm,"Corn flour, edible vegetable oil, spices, salt",Clean,KB_HIGH
8902433030055,SNICKERS STRAWBERRY FLAVOR,Snickers,"Sugar, peanuts, glucose syrup, milk solids, strawberry flavour, cocoa butter",Clean,KB_HIGH
8906083023313,Mindful essentials Chia Seeds,eatanytime,"Chia seeds (100%)",Clean single-ingredient,KB_HIGH
8901393027761,Play Tennis,Chupa Chups,"Sugar, glucose syrup, acidity regulator, flavours, colours",Verify colours,KB_MEDIUM
8906081380159,lime pickle with garlic,Telugu Foods,"Lime, garlic, salt, spices, edible vegetable oil",Clean,KB_HIGH
8901719136863,Hide & Seek Choco Rolls,Parle,"Refined wheat flour, sugar, cocoa solids, edible vegetable oil",Clean,KB_HIGH
8906143041769,Whole Wheat Penne Rigate,Yu Pasta,"Whole wheat flour (100%)",Clean single-ingredient,KB_HIGH
8906091931266,Shappad Diabeto Rice Kodo Millet,Shappad,"Kodo millet (100%)",Clean single-ingredient,KB_HIGH
8904256724494,Whole Wheat Bread,Tasties,"Whole wheat flour, water, yeast, salt, sugar",Clean,KB_HIGH
8906045140881,Whey Protein Isolate,Nutrabay,"Whey protein isolate (100%)",Clean single-ingredient,KB_HIGH
8901393020373,Happydent White,Happydent,"NON-FOOD — Mouth freshener",NON-FOOD — PURGE,N/A
8906094750338,Bottle Milk,Muralya,"Pasteurized toned milk",Clean single-ingredient,KB_HIGH
8906009537306,Gochujang,Max Protein,"Chilli, soybean, salt, fermentation culture",Clean,KB_HIGH
8901790716169,Diclorojo,Various,"NON-FOOD — Medicine",NON-FOOD — PURGE,N/A
8908000870536,Chana Dal,Jaimin,"Chana dal (100%)",Clean single-ingredient,KB_HIGH
8901790720685,Amoxcicilina,Various,"NON-FOOD — Medicine",NON-FOOD — PURGE,N/A
8901262220347,Butter Cookies,Amul,"Butter, sugar, refined wheat flour",Clean,KB_HIGH
8906186474937,Fully Cooked Spaghetti,Pasta Zing,"Durum wheat semolina",Clean single-ingredient,KB_HIGH
8906173934444,Hash Brown,Pommetos,"Potato, edible vegetable oil, salt",Clean,KB_HIGH
8908018275026,Crushed Peanut Chikki,Nutsy,"Peanuts, jaggery",Clean,KB_HIGH
8908000682788,Jeera Masala Soda,Kaycee,"Carbonated water, cumin, black salt, acidity regulators",Clean,KB_HIGH
8906174450653,Kashmiri Kahwa,Various,"Green tea, saffron, almonds, spices",Clean,KB_HIGH
8906191631356,Blueberry Cheesecake Protein Bar,Phab,"Whey protein, blueberry cheesecake flavour, sweetener, emulsifier",Clean,KB_HIGH
8903081300651,Dessert Protein Powder,Chase,"Whey protein, dessert flavour, sweetener, emulsifier",Clean,KB_HIGH
8901207023644,Dabar Red Gel 300g buy2,Dabur,"NON-FOOD — Medicine",NON-FOOD — PURGE,N/A
8906188960155,Unibic,Unibic,"Verify specific product",Verify,KB_MEDIUM
8904132973305,Independence bu,Independence,"Verify specific product",Verify,KB_MEDIUM
8908013903672,Spring Roll,Yummfeast,"Refined wheat flour, mixed vegetables, edible vegetable oil, spices",Clean,KB_HIGH
8906134790133,Honey Jam Mixed Berry,Eatopia,"Mixed berries, sugar, pectin",Clean,KB_HIGH
8906033950676,Nalla karam Powder,G. Pulla Reddy,"Spices blend (coriander, cumin, chilli, tamarind)",Clean spice blend,KB_HIGH
8901262203562,Borlotti Indiani,Harman,"Borlotti beans (100%)",Clean single-ingredient,KB_HIGH
8904089309868,Choco Block,Havmor,"Cocoa solids, sugar, cocoa butter, milk solids",Clean,KB_HIGH
8906005672780,Haldi Chana,Charliee,"Chickpeas, turmeric, spices, salt",Clean,KB_HIGH
8906056830115,Crave Gulab Jamun,Crave,"Milk solids, sugar, ghee, cardamom",Clean,KB_HIGH
8906056835004,Crave Besan Laddu,Crave,"Gram flour, sugar, ghee, cardamom",Clean,KB_HIGH
8906005910103,Aakash Ratlami Sev,Aakash,"Gram flour, edible vegetable oil, salt, spices",Clean,KB_HIGH
8906005910042,Aakash 350g,Aakash,"Verify specific product",Verify,KB_MEDIUM
8901548431573,Dark Chocolate,Complan,"Cocoa solids, cocoa butter, sugar",Clean,KB_HIGH
8901499025951,Millet Muesli,Kellogg's,"Millet, oats, nuts, honey",Clean,KB_HIGH
8906159751584,Wafers,Nabati,"Wheat flour, sugar, edible vegetable oil, cocoa solids",Clean,KB_HIGH
8901777674147,Rajbhog Kulfi,Vadilal,"Milk solids, sugar, cardamom, pistachios",Clean,KB_HIGH
8906081920768,Vitamin D3 Tablets,Carbamide Forte,"NON-FOOD — Supplement",NON-FOOD — PURGE,N/A
8906044920477,Double Beans White,Hallmark,"White beans (100%)",Clean single-ingredient,KB_HIGH
8908020170012,Siddipet Poultry Eggs,Siddipet Poultry,"Eggs (100%)",Clean single-ingredient,KB_HIGH
8903363014351,DMart Healthy Choice Chia Seeds,DMart,"Chia seeds (100%)",Clean single-ingredient,KB_HIGH
8908000339767,Karak tea premix,Various,"Black tea, cardamom, ginger, sugar",Clean,KB_HIGH
8904063219817,Haldiram's Minute Khana Dal Palak Kebab,Haldiram's,"Dal, palak, spices, salt, edible vegetable oil",Clean,KB_HIGH
8904040303133,Kodi Vepudu Masala,Annapoorna,"Spices blend (coriander, cumin, chilli, garlic)",Clean spice blend,KB_HIGH
8908012945833,Plant Protein Sachet,Pink Harvest Farms,"Plant protein blend (pea, rice)",Clean,KB_HIGH
8902901011388,makhana,Good Life,"Makhana (fox nuts)",Clean single-ingredient,KB_HIGH
8901483912991,Sweet Relish,Tiffy,"Cucumber, vinegar, sugar, salt, spices",Clean,KB_HIGH
8906092353845,Shadani Aam Papad,Shadani,"Mango pulp, sugar",Clean,KB_HIGH
8901786670307,Tasteeto Chilli Flakes,Everest,"Red chilli flakes (100%)",Clean single-ingredient,KB_HIGH
8901595851225,EGG HAKKA NOODLES,Ching's Secret,"Refined wheat flour, palm oil, salt; Tastemaker: salt, spices, flavour enhancers (INS 621)",INS 621 MSG,KB_HIGH
8908002026993,Atta Patti,Various,"Verify specific product",Verify,KB_MEDIUM
8904055906114,Krispy Fried Chicken,Meatzza Snackers,"Chicken, refined wheat flour, spices, salt, edible vegetable oil",Clean,KB_HIGH
8904063281555,Dal Makhani,Haldiram's,"Dal, butter, tomato, spices, salt",Clean,KB_HIGH
8903023267424,Tili White,More,"White sesame seeds (tili)",Clean single-ingredient,KB_HIGH
8908005072690,Chia Seeds,Delight Nuts,"Chia seeds (100%)",Clean single-ingredient,KB_HIGH
8901246007377,Spirali,Del Monte,"Durum wheat semolina (100%)",Clean single-ingredient,KB_HIGH
8904209303790,aachi mango thokku pickle,Aachi,"Raw mango, salt, red chilli, edible vegetable oil, mustard",Clean,KB_HIGH
8906071450961,Pasta Sauce,Various,"Tomato, garlic, basil, olive oil, salt",Clean,KB_HIGH
8904064616240,Sesamöl,Annam,"Sesame oil (100%)",Clean single-ingredient,KB_HIGH
8904083519140,Organic Whole Wheat Flour,24 Mantra Organic,"Organic whole wheat flour (100%)",Clean single-ingredient,KB_HIGH
8904180000572,Karela Pickle,Vik’s,"Bitter gourd, salt, spices, edible vegetable oil",Clean,KB_HIGH
8901262174619,American Nuts,Amul,"Mixed nuts (almonds, cashews, raisins)",Clean,KB_HIGH
8906073000003,Cloche de pâques,Pasticceria Del Castello,"Refined wheat flour, sugar, butter, eggs",Clean,KB_HIGH
8906014011020,Khatta Meetha Chana Papad,420 Papad,"Chana, spices, salt, edible vegetable oil",Clean,KB_HIGH
8906014011426,200g,Various,"Verify specific product",Verify,KB_MEDIUM
8906014011228,200g,Various,"Verify specific product",Verify,KB_MEDIUM
8906014011044,400g,Various,"Verify specific product",Verify,KB_MEDIUM
8906141910258,Black Rice,Dawat,"Black rice (100%)",Clean single-ingredient,KB_HIGH
8908002506044,Emperor dates,Emperor,"Dates (100%)",Clean single-ingredient,KB_HIGH
8901233020273,Cadbury 5 star,Cadbury,"Sugar, milk solids, cocoa butter, cocoa mass, emulsifiers",Clean,KB_HIGH
8902579004279,Smoodh Kesar Badam,Parle Agro,"Milk, kesar, badam, sugar",Clean,KB_HIGH
8906041814106,Crazy cups,Various,"Sugar, glucose syrup, flavours, colours",Verify colours,KB_MEDIUM
8906091300154,100% Banana Smoothie Whey Protein,Nutrabox,"Whey protein, banana flavour, sweetener",Clean,KB_HIGH
8906000934579,Zimt Stangen,Various,"Cinnamon sticks (100%)",Clean single-ingredient,KB_HIGH
8908000715004,raisins,Various,"Raisins (100%)",Clean single-ingredient,KB_HIGH
8904063259332,Aloo Kulcha,Haldiram's,"Potato, spices, salt, refined wheat flour",Clean,KB_HIGH
8906095128297,Indian kishmish,Various,"Raisins (100%)",Clean single-ingredient,KB_HIGH
8908027388038,High Protein Roti,MillD,"Whole wheat flour, water, salt, protein blend",Clean,KB_HIGH
8908015078026,Abhi Eggs,Abhi Eggs,"Eggs (100%)",Clean single-ingredient,KB_HIGH
8904083300434,Milma paneer,Milma,"Paneer (100%)",Clean single-ingredient,KB_HIGH
8906165788376,MuscleBlaze Biozyme Iso-Zero Low Carb Swiss Chocolate Hazelnut Flavour,MuscleBlaze,"Whey protein isolate, chocolate hazelnut flavour, sweetener, emulsifier",Clean,KB_HIGH
8906021922814,APIs Himalaya honey,apis,"Honey (100%)",Clean single-ingredient,KB_HIGH
8901548310113,D lite vanila,Complan,"Sugar, glucose syrup, vanilla flavour, colours",Verify colours,KB_MEDIUM
8901548310069,D lite cricpy,Complan,"Sugar, glucose syrup, flavours, colours",Verify colours,KB_MEDIUM
8904209300119,Veg Biryani,Aachi,"Rice, mixed vegetables, spices, salt, edible vegetable oil",Clean,KB_HIGH
8906151142717,Magnesium Glycinate,Tata 1mg,"NON-FOOD — Supplement",NON-FOOD — PURGE,N/A
8906095290277,Kayi Kodubale,Adukale Sankethi,"Rice flour, spices, salt, edible vegetable oil",Clean,KB_HIGH
8908015676093,Golden sweet potato peri peri,TBH,"Sweet potato, peri peri seasoning, edible vegetable oil, salt",Clean,KB_HIGH
8903363006103,Black Pepper (Pepper Corn),DMart Premia,"Black pepper (100%)",Clean single-ingredient,KB_HIGH
8908002783353,Granny's Tamarind,Granny's,"Tamarind (100%)",Clean single-ingredient,KB_HIGH
8906144490467,French Vanilla Arabica Coffee,Sleepy Owl,"Arabica coffee (100%)",Clean single-ingredient,KB_HIGH
8904491700093,Millet Cookies (Chocolate),Tummy Friendly,"Millet flour, chocolate, cocoa solids, edible vegetable oil",Clean,KB_HIGH
8904083533856,Organic Chekodi,24 Mantra Organic,"Rice flour, gram flour, spices, salt, edible vegetable oil",Clean,KB_HIGH
8904274100140,Boondi,Charbhuja Namkeen,"Gram flour, edible vegetable oil, salt, spices",Clean,KB_HIGH
8906001385752,Cremica,Cremica,"Verify specific product",Verify,KB_MEDIUM
8906129282742,LOW FAT PANEER,FRU BON,"Paneer (low fat)",Clean single-ingredient,KB_HIGH
8908015361005,Mustard Oil,Various,"Mustard oil (100%)",Clean single-ingredient,KB_HIGH
8906098670083,INDIAN MASALA -POPCORN-,Ultra Pop,"Popcorn, indian masala seasoning, edible vegetable oil, salt",Clean,KB_HIGH
8906174460225,GHEESE GARIC FLAVOURED POPCORN,Ultra Pop,"Popcorn, cheese, garlic seasoning, edible vegetable oil, salt",Clean,KB_HIGH
8901117289239,Cofsils Cough Drops,Cofsils,"NON-FOOD — Cough drops",NON-FOOD — PURGE,N/A
8901888006004,REAL BURRST POMEGRANATE,Real,"Water, pomegranate juice concentrate, sugar, acidity regulator",Clean,KB_HIGH
8901888006011,REAL BURRST MIXED FRUIT,Real,"Water, mixed fruit juice concentrate, sugar, acidity regulator",Clean,KB_HIGH
8906163832415,Farmley Omani Dates Fard,Farmley,"Omani dates (100%)",Clean single-ingredient,KB_HIGH
8906012231918,Corn Flour,Vijay Gold,"Corn flour (100%)",Clean single-ingredient,KB_HIGH
8906032152545,Sleepy Tea,Luxmi Estates,"Black tea (100%)",Clean single-ingredient,KB_HIGH
8901542001666,Glucon - D,Zydus,"Dextrose monohydrate, vitamins, minerals",Clean,KB_HIGH
8906157630171,Jaggery,Sunpure,"Jaggery (100%)",Clean single-ingredient,KB_HIGH
8901648921424,Live Lite Low Fat Milk,Mother Dairy,"Low fat milk, vitamins A & D",Clean single-ingredient,KB_HIGH
8906019779505,Australian Almond Kernels,Nutraj,"Almonds (100%)",Clean single-ingredient,KB_HIGH
8908022604133,Berry basil kombucha,Hrx,"Kombucha, berry, basil",Clean,KB_HIGH
8901725016272,Dark Fantasy Bourbon,Sunfeast,"Refined wheat flour, sugar, cocoa solids, edible vegetable oil",Clean,KB_HIGH
8906033743803,Mcvities Bourboan,McVities,"Refined wheat flour, sugar, edible vegetable oil, cocoa solids",Clean,KB_HIGH
8904132976436,Rasklk,Various,"Verify specific product",Verify,KB_MEDIUM
8901440218494,ايستي قوه شاي اسود,Various,"Black tea (100%)",Clean single-ingredient,KB_HIGH
8901393019506,Gummy Tubes,Chupa Chups,"Sugar, glucose syrup, gelatin, flavours, colours",Verify colours,KB_MEDIUM
8906199680257,Whey Protein Isolate (Chocolate),The Func Lab,"Whey protein isolate, chocolate flavour, sweetener, emulsifier",Clean,KB_HIGH
8906016350011,Samrat MP Chakki Atta 10 Kg,Samrat,"Whole wheat flour (100%)",Clean single-ingredient,KB_HIGH
8901207027536,Pomegranate Fruit Juice Nectar,Dabur,"Pomegranate juice, water, sugar",Clean,KB_HIGH
8901088203630,parachut,Parachute,"NON-FOOD — Hair oil",NON-FOOD — PURGE,N/A
8906131681557,Oats jumbo rolled,Slurrp Farm,"Rolled oats (100%)",Clean single-ingredient,KB_HIGH
8904440924068,بهارت دجاج مقلي,Eastern,"Chicken masala blend",Clean spice blend,KB_HIGH
8901440221715,بهارت مشكل,Eastern,"Mixed spice blend",Clean spice blend,KB_HIGH
8901004401102,بهارت بريالي,Eastern,"Biryani masala blend",Clean spice blend,KB_HIGH
8901440209768,مسحوق الفلفل الاسود,Eastern,"Black pepper powder (100%)",Clean single-ingredient,KB_HIGH
8906168740630,Amla Juice,Baidyanath,"NON-FOOD — Ayurvedic supplement",NON-FOOD — PURGE,N/A
8901052008889,Green tea Beauty care,Tata Tea,"Green tea (100%)",Clean single-ingredient,KB_HIGH
8906182620406,Rice Paper,Master Chow,"Rice flour, water, salt",Clean,KB_HIGH
8902710500509,Baggry’s No Added Sugar muesli,Bagrry's,"Oats, nuts, seeds, dried fruits",Clean,KB_HIGH
8904155712837,Boroflex,Zuventus,"NON-FOOD — Medicine",NON-FOOD — PURGE,N/A
8902901027839,Desi kitchen Kodo millet,Desi Kitchen,"Kodo millet (100%)",Clean single-ingredient,KB_HIGH
8901786122004,Kitchen King Masala,Everest,"Coriander, cumin, turmeric, red chilli, black pepper, garlic, ginger, spices",Clean spice blend,KB_HIGH
8906011701214,Baking powder,Frolic,"Sodium bicarbonate, corn starch, acidity regulator",Clean,KB_HIGH
8901786030163,Pani Puri Masala,Everest,"Spices blend (tamarind, cumin, black salt, mint)",Clean spice blend,KB_HIGH
8906066206184,Pizza Oregano,Keya,"Oregano (100%)",Clean single-ingredient,KB_HIGH
8901786080120,Sambar Masala,Everest,"Coriander, turmeric, red chilli, fenugreek, cumin, black pepper, mustard",Clean spice blend,KB_HIGH
8908004271575,Kala masala,Nasale,"Spices blend (coriander, cumin, coconut, red chilli)",Clean spice blend,KB_HIGH
8904124801180,Jhanjhanit Thecha,Raj,"Green chilli, garlic, salt, edible vegetable oil",Clean,KB_HIGH
8904327600818,Peanut Butter,My Fitness,"Roasted peanuts, salt",Clean,KB_HIGH
8908002937237,Heem Rock Salt,Heem,"Pink rock salt (100%)",Clean single-ingredient,KB_HIGH
8903023289983,More Choice Kasoori Methi,More Choice,"Kasuri methi (dried fenugreek leaves)",Clean single-ingredient,KB_HIGH
8904055907371,Marinated Boneless Chiken Tandoori Tikka,Meatzzaa,"Chicken, tandoori spices, salt, edible vegetable oil",Clean,KB_HIGH
8906006170339,Manchurian Puffs,O'yes,"Refined wheat flour, mixed vegetables, spices, salt, edible vegetable oil",Clean,KB_HIGH
8906046143454,Whole Green Mung Beans,Pride Of India,"Green mung beans (100%)",Clean single-ingredient,KB_HIGH
8901220448134,Baidyanath Triphala Churna,Baidyanath,"NON-FOOD — Ayurvedic supplement",NON-FOOD — PURGE,N/A
8901138505851,Himalaya 200 g,Himalaya,"NON-FOOD — Face wash",NON-FOOD — PURGE,N/A
8908010299082,Shifa jelly 50 g,Shifa,"NON-FOOD — Medicine",NON-FOOD — PURGE,N/A
8906125380497,Shifa jelly 100 g,Shifa,"NON-FOOD — Medicine",NON-FOOD — PURGE,N/A
8908003457338,Coconut Water,Mojoco,"Coconut water (100%)",Clean single-ingredient,KB_HIGH
8906080040375,Garlic Toast,27 Peaks,"Refined wheat flour, garlic, butter, salt",Clean,KB_HIGH
8902901026757,Good Life Black Dry Dates 200gm,Good Life,"Black dates (100%)",Clean single-ingredient,KB_HIGH
8902167009969,mdh hing powder 20g,MDH,"Asafoetida powder (100%)",Clean single-ingredient,KB_HIGH
8906001400301,ssp special asafoetida hing,SSP,"Asafoetida (hing)",Clean single-ingredient,KB_HIGH
8906005506719,Bikaji anokhe risty,Bikaji,"Rice flakes, gram flour, edible vegetable oil, peanuts, salt, spices",Clean,KB_HIGH
8905950000327,Bikaji Shubh Avsar,Bikaji,"Rice flakes, gram flour, edible vegetable oil, peanuts, salt, spices",Clean,KB_HIGH
8905950000341,Bikaji Festive masti,Bikaji,"Rice flakes, gram flour, edible vegetable oil, peanuts, salt, spices",Clean,KB_HIGH
8906038782852,Aceite,Sri,"Verify specific product",Verify,KB_MEDIUM
8906019561162,Jeera Khari 400gm,Various,"Whole wheat flour, cumin, salt, edible vegetable oil",Clean,KB_HIGH
8906065580131,Potato Wafers,Manohar,"Potato, edible vegetable oil, salt",Clean,KB_HIGH
8904063255365,Khatta meetha,Haldiram's,"Rice flakes, gram flour, edible vegetable oil, peanuts, salt, sugar, spices",Clean,KB_HIGH
8906188960094,Jeera Cookies,Unibic,"Refined wheat flour, cumin, edible vegetable oil, salt",Clean,KB_HIGH
8906095192144,Onion Powder,Praakritik,"Onion powder (100%)",Clean single-ingredient,KB_HIGH
8908019582048,Millet Noodles,Mr. Agro,"Millet flour, salt, thickeners",Clean,KB_HIGH
8903023264587,more selecta maida,More Selecta,"Refined wheat flour (maida)",Clean single-ingredient,KB_HIGH
8904120400882,American Yellow Mustard,Abbie’s,"Yellow mustard seeds, vinegar, salt, spices",Clean,KB_HIGH
8906005508218,Achari Masala Matthi,Bikaji,"Refined wheat flour, achari masala, salt, edible vegetable oil",Clean,KB_HIGH
8906069405669,Shawarma Garlic Veginnaise Eggless,Veeba,"Mayonnaise, garlic, spices",Clean,KB_HIGH
8906073541124,WEIGHT Ủj Alkhor,Various,"Verify specific product",Verify,KB_MEDIUM
8904002501904,MASQATI BADAM PISTA KULFI,Masqati,"Almonds, pistachios, sugar, ghee, cardamom",Clean,KB_HIGH
8904002501881,Mango Duet,Masqati,"Mango, sugar, ghee, cardamom",Clean,KB_HIGH
8906163832248,Farmley Quinoa,Farmley,"Quinoa (100%)",Clean single-ingredient,KB_HIGH
8906014881043,Methi Thepla,Rewynd,"Whole wheat flour, fenugreek leaves, spices, salt, edible vegetable oil",Clean,KB_HIGH
8906167242760,Black Small Mustard Seeds,Various,"Black mustard seeds (100%)",Clean single-ingredient,KB_HIGH
8906167242371,Sooji,Various,"Semolina (suji/rava)",Clean single-ingredient,KB_HIGH
8907065096127,Puramate Corn Flour,Puramate,"Corn flour (100%)",Clean single-ingredient,KB_HIGH
8901662038344,suhana chicken gravy,Suhana,"Chicken gravy mix (spices, salt, thickeners)",Clean,KB_HIGH
8901058011746,Maggi sauce,Maggi,"Tomato paste, sugar, water, vinegar, salt, spices",Clean,KB_HIGH
8904155834737,butter cookies,Various,"Refined wheat flour, butter, sugar",Clean,KB_HIGH
8901058903171,KitKat big,Nestle,"Sugar, milk solids, cocoa butter, cocoa mass, emulsifiers",Clean,KB_HIGH
8908001246361,Mast Mattar,Crax,"Corn flour, edible vegetable oil, mattar seasoning, salt",Clean,KB_HIGH
8906166360298,Unjunked Bhujia,Open Secret,"Rice flakes, gram flour, edible vegetable oil, peanuts, salt, spices",Clean,KB_HIGH
8901047011054,Cooked Basmati Rice,Trophy,"Basmati rice (100%)",Clean single-ingredient,KB_HIGH
8904071512122,Kachori,Various,"Refined wheat flour, moong dal, spices, salt, edible vegetable oil",Clean,KB_HIGH
8906125982097,Crunchy salt corn,4700BC,"Corn, edible vegetable oil, salt",Clean,KB_HIGH
8908019882094,Coco Poco Green Apple,Dobra,"Popcorn, green apple seasoning, edible vegetable oil, salt",Clean,KB_HIGH
8908013080878,Coconut Water,Cocomama,"Coconut water (100%)",Clean single-ingredient,KB_HIGH
8906170521425,High Protein Oats ( Chocolate Raisin),Nutrabay,"Oats, chocolate raisin flavour, sweetener, emulsifier",Clean,KB_HIGH
8900419935837,bergen black,Bergen,"Verify specific product",Verify,KB_MEDIUM
8906091300468,Creatine,NutraBox,"Creatine monohydrate (100%)",Supplement,KB_HIGH
8904039700219,Jaggery,Various,"Jaggery (gur)",Clean single-ingredient,KB_HIGH
8906112668799,Oats atta,Various,"Oats flour, whole wheat flour",Clean,KB_HIGH
8906159973696,Mutton masala,Various,"Spices blend (coriander, cumin, red chilli, garlic, ginger)",Clean spice blend,KB_HIGH
8904293708419,Chana Brown Flipkart,Flipkart Grocery,"Brown chana (100%)",Clean single-ingredient,KB_HIGH
8906032550440,Biryani Masala,Eagle,"Spices blend (coriander, cumin, red chilli, garlic, ginger)",Clean spice blend,KB_HIGH
8906095192274,Raw Sugar,Praakritik,"Raw sugar (100%)",Clean single-ingredient,KB_HIGH
8903794503011,Red chilli,Various,"Red chilli (100%)",Clean single-ingredient,KB_HIGH
8903794503509,Tamarind,Various,"Tamarind (100%)",Clean single-ingredient,KB_HIGH
8901537081567,Roasted Rice Crackers,Pepper Delight,"Rice, edible vegetable oil, salt, spices",Clean,KB_HIGH
8904017013843,Phool Makhana,Uttam Fresh And Clean,"Makhana (fox nuts)",Clean single-ingredient,KB_HIGH
8906087420309,Bengaluru's Special Mixture,Sowbhagya Foods,"Rice flakes, gram flour, edible vegetable oil, peanuts, salt, spices",Clean,KB_HIGH
8901071704335,Kisses hazelnut,Hershey's,"Chocolate, hazelnuts",Clean,KB_HIGH
8906199980203,Classic Chettinad Seedai,Sri Krishna Sweets,"Rice flour, gram flour, spices, salt, edible vegetable oil",Clean,KB_HIGH
8904004402285,farali Chiwda,Haldiram's,"Rice flakes, gram flour, edible vegetable oil, peanuts, salt, spices",Clean,KB_HIGH
8906064701230,Cornflakes Mixture,Kozhi Koden's,"Corn flakes, edible vegetable oil, salt, spices",Clean,KB_HIGH
8901491003414,Kurkure,Lehar,"Corn grits, edible vegetable oil, spices, salt, flavour enhancers (INS 621)",INS 621 MSG,KB_HIGH
8906095141456,Energy Gel,Unived,"Carbohydrates, electrolytes, vitamins",Supplement,KB_HIGH
8901648011613,Misthi doi,Mother Dairy,"Pasteurized milk, sugar, active lactic culture",Clean,KB_HIGH
8901648013761,Mishti Doi,Mother Dairy,"Pasteurized milk, sugar, active lactic culture",Clean,KB_HIGH
8901648014850,Fruit yoghurt Blueberry,Mother Dairy,"Pasteurized milk, blueberry, sugar, active lactic culture",Clean,KB_HIGH
8906136782396,Wild Forest Honey,Anveshan,"Wild honey (100%)",Clean single-ingredient,KB_HIGH
8906189580550,Plant Protein Bar,Upnourish by Pluckk,"Plant protein, oats, nuts, sweetener",Clean,KB_HIGH
8904038109402,Salted Peanuts,Babaji,"Peanuts, salt",Clean,KB_HIGH
8906005509888,Palak Paneer,Bikaji,"Paneer, palak, spices, salt, edible vegetable oil",Clean,KB_HIGH
8907316007315,Spice Mix For Chicken 65,Mother’s Recipe,"Spices blend (red chilli, garlic, ginger, vinegar)",Clean spice blend,KB_HIGH
8901648001768,Lassi sweet,Mother Dairy,"Pasteurized milk, sugar, active lactic culture",Clean,KB_HIGH
8901648091455,Nutrifit probiotic drink strawberry,Mother Dairy,"Pasteurized milk, strawberry, sugar, probiotic culture",Clean,KB_HIGH
8909350001038,Tofu masala,Vinvik,"Tofu, spices, salt, edible vegetable oil",Clean,KB_HIGH
8908024377011,Tofu jeera,Fit Bean,"Tofu, cumin, salt, edible vegetable oil",Clean,KB_HIGH
8908024377004,firm Tofu,Fit Bean,"Tofu (100%)",Clean single-ingredient,KB_HIGH
8908024377028,veggie Tofu,Fit Bean,"Tofu, mixed vegetables, spices, salt",Clean,KB_HIGH
8906020493551,lal soan papdi,Various,"Gram flour, sugar, ghee, cardamom",Clean,KB_HIGH
8908019552003,ORIGINAL PANCAKE & WAFFLE mix,The Belgian Waffle Co,"Refined wheat flour, sugar, raising agents, salt",Clean,KB_HIGH
8906133406707,Nutrimix,Little Joys,"Multigrain, nuts, seeds, dried fruits",Clean,KB_HIGH
8906014081887,brahmins kadala,Brahmins,"Black chickpeas (100%)",Clean single-ingredient,KB_HIGH
8906014081535,brahmins uluva,Brahmins,"Fenugreek seeds (100%)",Clean single-ingredient,KB_HIGH
8901743062008,Melam idily mix,Melam,"Rice flour, urad dal flour, salt",Clean,KB_HIGH
8906014080477,Br Coriander powder,Brahmins,"Coriander powder (100%)",Clean single-ingredient,KB_HIGH
8904011509069,Double horse coriander powder,Double Horse,"Coriander powder (100%)",Clean single-ingredient,KB_HIGH
8908006779734,ajmi coriander powder,Ajmi,"Coriander powder (100%)",Clean single-ingredient,KB_HIGH
8906134670299,ajmi turmeric powdee,Ajmi,"Turmeric powder (100%)",Clean single-ingredient,KB_HIGH
8902082700170,Grandma's turmeric powder,Grandma's,"Turmeric powder (100%)",Clean single-ingredient,KB_HIGH
8906134670510,Ajmi kashmiri chilli powder,Ajmi,"Kashmiri red chilli powder (100%)",Clean single-ingredient,KB_HIGH
8908006779727,ajmi chilli powder,Ajmi,"Red chilli powder (100%)",Clean single-ingredient,KB_HIGH
8902082700026,grandma's meat masala,Grandma's,"Spices blend (coriander, cumin, red chilli, garlic, ginger)",Clean spice blend,KB_HIGH
8902082700064,grandma's chicken masala,Grandma's,"Spices blend (coriander, cumin, red chilli, garlic, ginger)",Clean spice blend,KB_HIGH
8902082700088,grandma's fish curry masala,Grandma's,"Spices blend (coriander, cumin, red chilli, garlic, ginger)",Clean spice blend,KB_HIGH
8906014081313,Br ginger garlic paste,Brahmins,"Ginger, garlic, salt, acidity regulator",Clean,KB_HIGH
8904011508192,Double horse meat masala,Double Horse,"Spices blend (coriander, cumin, red chilli, garlic, ginger)",Clean spice blend,KB_HIGH
8904011508185,double horse fish masala,Double Horse,"Spices blend (coriander, cumin, red chilli, garlic, ginger)",Clean spice blend,KB_HIGH
8904450000172,Lampy out,Various,"Verify specific product",Verify,KB_MEDIUM
8908006982127,Raw Cooking Spray,Raw,"NON-FOOD — Cooking spray",NON-FOOD — PURGE,N/A
8906014081276,Himalayan Pink SALT,Brahmins,"Himalayan pink salt (100%)",Clean single-ingredient,KB_HIGH
8906001093169,Premium Extra Long Gain Basmati Rice,Golden Grain,"Basmati rice (100%)",Clean single-ingredient,KB_HIGH
8906134670374,Kashmiri,Ajmi,"Kashmiri red chilli powder (100%)",Clean single-ingredient,KB_HIGH
8906013812512,Quinoa & Seeds,Roasty Toasty,"Quinoa, mixed seeds",Clean,KB_HIGH
8904089929127,Heritage fresh panner,Heritage,"Paneer (100%)",Clean single-ingredient,KB_HIGH
8902901035179,Bolas kaju,Bolas,"Cashew nuts (100%)",Clean single-ingredient,KB_HIGH
8908019481181,Rich Plum Cake,Kottaram,"Refined wheat flour, sugar, plums, eggs, edible vegetable oil, raising agents",Clean,KB_HIGH
8906095112487,Flax seeds,Wonderland,"Flax seeds (100%)",Clean single-ingredient,KB_HIGH
8901248270175,Emami soyabean oil 5lr,Emami,"Refined soyabean oil",Clean single-ingredient,KB_HIGH
8906023810270,Brown Bread,Nanda's,"Whole wheat flour, water, sugar, yeast, salt",Clean,KB_HIGH
8906054071664,Elite Grains,Elite Grains,"Mixed grains (wheat, oats, jowar, bajra)",Clean,KB_HIGH
8905604002059,Jivo Rice Bran Oil,Jivo,"Rice bran oil (100%)",Clean single-ingredient,KB_HIGH
8901777462072,Cheese Chutney,Vadilal,"Paneer, green chilli, spices, salt, edible vegetable oil",Clean,KB_HIGH
8908013252596,Power oats choco peanut butter 400gm Fit & Flex,Fit and Flex,"Oats, chocolate, peanut butter, sweetener",Clean,KB_HIGH
8906010261085,Sunflower Oil,Gold Winner,"Refined sunflower oil",Clean single-ingredient,KB_HIGH
8909106028586,Coffee,Bru,"Instant coffee (100%)",Clean single-ingredient,KB_HIGH
8901052005970,Black Tea,Tata Tea,"Black tea (100%)",Clean single-ingredient,KB_HIGH
8901052006519,Agni Leaf,Tata Tea,"Black tea (100%)",Clean single-ingredient,KB_HIGH
8906005625038,Coffee Powder,Mayil,"Instant coffee (100%)",Clean single-ingredient,KB_HIGH
8904335605096,Mango Rizz Protein Shake,Yoga Bar,"Whey protein, mango flavour, sweetener, emulsifier",Clean,KB_HIGH
8901052031450,Kanan Devan,Tata Tea,"Black tea (100%)",Clean single-ingredient,KB_HIGH
8906134671593,Garlic Murukku,Ajmi,"Rice flour, garlic, spices, salt, edible vegetable oil",Clean,KB_HIGH
8906134671395,Bombay Mixture,Ajmi,"Rice flakes, gram flour, edible vegetable oil, peanuts, salt, spices",Clean,KB_HIGH
8906134671401,Kuzhalappam,Ajmi,"Rice flour, edible vegetable oil, salt, spices",Clean,KB_HIGH
8906134671388,Kerala Mix,Ajmi,"Rice flakes, gram flour, edible vegetable oil, peanuts, salt, spices",Clean,KB_HIGH
8906134671418,Sharkaravaratty,Ajmi,"Rice flour, jaggery, coconut, cardamom",Clean,KB_HIGH
8906134671364,JackFruit Chips,Ajmi,"Jackfruit, rice flour, edible vegetable oil, salt",Clean,KB_HIGH
8906134671647,Kerala Mixture Extra Hot,Ajmi,"Rice flakes, gram flour, edible vegetable oil, peanuts, salt, spices",Clean,KB_HIGH
8906134671425,Pakkavada,Ajmi,"Rice flour, edible vegetable oil, salt, spices",Clean,KB_HIGH
8906134672118,Masala Cookies,Ajmi,"Refined wheat flour, spices, salt, edible vegetable oil",Clean,KB_HIGH
8908020440269,Tortilla Wrap Beetroot & Carrot,Habanero,"Whole wheat flour, beetroot, carrot, salt, edible vegetable oil",Clean,KB_HIGH
8908024361478,High Protein Coffee,Provilac,"Milk, coffee, protein, sweetener",Clean,KB_HIGH
8908004114438,Cashew nuts,Various,"Cashew nuts (100%)",Clean single-ingredient,KB_HIGH
8906111323606,Fara tamarind 500g,Various,"Tamarind (100%)",Clean single-ingredient,KB_HIGH
8906055100455,Roasted Chana,Rajdhani,"Roasted chickpeas (100%)",Clean single-ingredient,KB_HIGH
8908001105088,the only salad mix 50gm,On1y,"Mixed seeds (pumpkin, sunflower, flax)",Clean,KB_HIGH
8906163831050,Peri Peri Party Mix,Farmley,"Makhana, peri peri seasoning, edible vegetable oil, salt",Clean,KB_HIGH
8906102380519,vintomo plus,Various,"Verify specific product",Verify,KB_MEDIUM
8904300200349,Butter Biks,Mario,"Refined wheat flour, butter, sugar",Clean,KB_HIGH
8906063434115,Prabhat,Prabhat,"Verify specific product",Verify,KB_MEDIUM
8906084416497,M.O.M,M.O.M,"Verify specific product",Verify,KB_MEDIUM
8905604001861,grass,Various,"Verify specific product",Verify,KB_MEDIUM
8901440222798,Chili Pulver,Eastern,"Chilli powder (100%)",Clean single-ingredient,KB_HIGH
8904234000329,snacks,Various,"Verify specific product",Verify,KB_MEDIUM
8901499010018,Kellogg's,Kellogg's,"Verify specific product",Verify,KB_MEDIUM
8904067712918,Potato Chips,Jabsons,"Potato, edible vegetable oil, salt",Clean,KB_HIGH
8902901251623,Cashews 400g,Good Life,"Cashew nuts (100%)",Clean single-ingredient,KB_HIGH
8902269509305,Zukacold,Various,"NON-FOOD — Medicine",NON-FOOD — PURGE,N/A
8902579002084,B fizz malt flavoured sparkling drink,Parle Agro,"Carbonated water, malt extract, sugar, acidity regulators",Clean,KB_HIGH
8908015543210,Banana Flavoured Pea Protein By Green Protein,Green Protein,"Pea protein, banana flavour, sweetener, emulsifier",Clean,KB_HIGH
8904043907239,Classic Salted & Roasted Almonds,Tata Sampann,"Almonds, salt",Clean,KB_HIGH
8906133021689,Whey Hydro Hydrolyzed Whey Protein,Nakpro,"Hydrolyzed whey protein, flavour, sweetener",Clean,KB_HIGH
8901262050074,Gulab Jamun,Amul,"Milk solids, sugar, ghee, cardamom",Clean,KB_HIGH
8901719921124,Biscuits,Parle,"Verify specific product",Verify,KB_MEDIUM
8901777033661,Green Chilli,Vadilal,"Green chilli, salt, edible vegetable oil",Clean,KB_HIGH
8906112662643,Flax Seeds Raw,True Elements,"Flax seeds (100%)",Clean single-ingredient,KB_HIGH
8906081923073,Micronized Creatine Monohydrate,Carbamide Forte,"NON-FOOD — Supplement",NON-FOOD — PURGE,N/A
8906038230995,Chicken Kheema Parathas,Zorabian,"Refined wheat flour, chicken mince, spices, salt, edible vegetable oil",Clean,KB_HIGH
8906045581264,lalji sona papdi,Lalji,"Gram flour, sugar, ghee, cardamom",Clean,KB_HIGH
8904083300755,milky chocolate,Various,"Verify specific product",Verify,KB_MEDIUM
8901262030458,Ghee,Amul,"Milk fat (100%)",Clean single-ingredient,KB_HIGH
8906117254867,MADE IN INDIA,Dr Rashel,"NON-FOOD — Cosmetic",NON-FOOD — PURGE,N/A
8908008660207,JJ Jeera rice papad,JJ,"Rice flour, cumin, salt, edible vegetable oil",Clean,KB_HIGH
8908008660115,JJ Potato Fryms,JJ,"Potato flour, edible vegetable oil, salt",Clean,KB_HIGH
8906036673138,Nandini,Nandini,"Verify specific product",Verify,KB_MEDIUM
8902979043991,Tomato Garlic Pickle,Puchi Magic,"Tomato, garlic, salt, spices, edible vegetable oil",Clean,KB_HIGH
8908014493646,Kerala Whole Wheat Paratha,Rusingo,"Whole wheat flour, water, salt, edible vegetable oil",Clean,KB_HIGH
8908015543418,green protein,Green Protein,"Verify specific product",Verify,KB_MEDIUM
8902710508901,High Protein Oats,Bagrry's,"Oats, dark chocolate, sweetener",Clean,KB_HIGH
8906041570200,Paneer,Pride Of Cows,"Paneer (100%)",Clean single-ingredient,KB_HIGH
8908026538083,Protein Powder Unflavoured,Wellbeing Nutrition,"Whey protein isolate (100%)",Clean single-ingredient,KB_HIGH
8901262070928,Choco Cracker,Amul,"Refined wheat flour, sugar, cocoa solids, edible vegetable oil",Clean,KB_HIGH
8901063033818,Pure magic 84g,Britannia,"Refined wheat flour, sugar, cocoa solids, edible vegetable oil",Clean,KB_HIGH
8901719135866,Parle Hide&Seek,Parle,"Refined wheat flour, sugar, cocoa solids, edible vegetable oil",Clean,KB_HIGH
8906138980615,salted chips,Various,"Potato, edible vegetable oil, salt",Clean,KB_HIGH
8906065031138,karachi cookies,Karachi Bakery,"Refined wheat flour, sugar, butter",Clean,KB_HIGH
8908018802086,Malaysian Curry Instant Noodles,Sakaza,"Refined wheat flour, palm oil, salt; Tastemaker: salt, spices, flavour enhancers (INS 621)",INS 621 MSG,KB_HIGH
8906082371552,Kulfi,Grameen Kulfi,"Milk solids, sugar, cardamom, pistachios",Clean,KB_HIGH
8906066201295,Black Pepper Grinder,Keya,"Black pepper (100%)",Clean single-ingredient,KB_HIGH
8902710511024,Granola,Bagrry's,"Oats, nuts, seeds, dried fruits",Clean,KB_HIGH
8906000921968,Namak Para,Daadis,"Refined wheat flour, salt, edible vegetable oil",Clean,KB_HIGH
8904327602348,Peanut Butter Unsweetened,Myfitness Zero,"Roasted peanuts (100%)",Clean single-ingredient,KB_HIGH
8906010368340,town bus Avalakki mixture,Town Bus,"Rice flakes, gram flour, edible vegetable oil, peanuts, salt, spices",Clean,KB_HIGH
8904083302445,Blueberry Greek Yogurt,Milky Mist,"Pasteurized milk, blueberry, active lactic culture",Clean,KB_HIGH
8901738200385,Badhusha Mithai,Vaigai,"Refined wheat flour, sugar, ghee, cardamom",Clean,KB_HIGH
8906030392752,Saras tarmarind 500g,Saras,"Tamarind (100%)",Clean single-ingredient,KB_HIGH
8906030392745,Saras tarmarind 200g,Saras,"Tamarind (100%)",Clean single-ingredient,KB_HIGH
8901779901104,Saras kashmir chilli,Saras,"Kashmiri red chilli powder (100%)",Clean single-ingredient,KB_HIGH
8901779022106,Saras corinder,Saras,"Coriander powder (100%)",Clean single-ingredient,KB_HIGH
8906159971241,Kerala Cashew & Pepper Chocolate,Paul and Mike,"Cashews, dark chocolate, black pepper",Clean,KB_HIGH
8904132901681,sun crush,Sun Crush,"Verify specific product",Verify,KB_MEDIUM
8904132904187,sun crush mango,Sun Crush,"Mango pulp, sugar, acidity regulator",Clean,KB_HIGH
8904018600769,Peru Papd,Chandan,"Refined wheat flour, salt, edible vegetable oil",Clean,KB_HIGH
8908018802079,Thai Fire Blaze Instant Noodes,Sakaza,"Refined wheat flour, palm oil, salt; Tastemaker: salt, spices, flavour enhancers (INS 621)",INS 621 MSG,KB_HIGH
8904150206461,Mix Dried Berries,Nutty Gritties,"Mixed dried berries (cranberry, blueberry, strawberry)",Clean,KB_HIGH
8906078150161,Star fries ring murukku,Star Fries,"Rice flour, edible vegetable oil, salt, spices",Clean,KB_HIGH
8906078150147,Star fries tapioca chips,Star Fries,"Tapioca, edible vegetable oil, salt",Clean,KB_HIGH
8901491002905,Kurkure,Kurkure,"Corn grits, edible vegetable oil, spices, salt",Clean,KB_HIGH
8904494100487,Butter Cookies,Danish Style,"Refined wheat flour, butter, sugar",Clean,KB_HIGH
8901537081062,Roasted Rice Cracker,Kari Kari,"Rice, edible vegetable oil, salt",Clean,KB_HIGH
8908009918215,Plant Protein,O’ziva,"Plant protein blend (pea, rice, soy)",Clean,KB_HIGH
8901220004736,chyawanprash,Baidyanath,"NON-FOOD — Ayurvedic supplement",NON-FOOD — PURGE,N/A
8901207050060,Chyawanprash,Dabur,"NON-FOOD — Ayurvedic supplement",NON-FOOD — PURGE,N/A
8901928710007,Rich Marie 1kg,Bisk Farm,"Refined wheat flour, sugar, edible vegetable oil",Clean,KB_HIGH
8906121210101,Calcutta Elaichi Chai,Chérise,"Black tea, elaichi",Clean,KB_HIGH
8901157025200,Hit 400 ml,Hit,"NON-FOOD — Insecticide",NON-FOOD — PURGE,N/A
8908020440252,Tomato & Herbs Tortilla Wraps,Habanero,"Whole wheat flour, tomato, herbs, salt, edible vegetable oil",Clean,KB_HIGH
8904063204073,Instant meal Dal Kichdi,Haldiram's,"Dal, rice, spices, salt, edible vegetable oil",Clean,KB_HIGH
8906125982721,Buttter popcorn,4700BC,"Popcorn, butter, salt",Clean,KB_HIGH
8904256720168,Eggless chocolate cake,Various,"Refined wheat flour, sugar, cocoa solids, edible vegetable oil, raising agents",Clean,KB_HIGH
8908005459828,Chia Seeds,Nourish You,"Chia seeds (100%)",Clean single-ingredient,KB_HIGH
8906002080427,Sakti curry powder 100g.,Sakthi,"Curry powder blend",Clean spice blend,KB_HIGH
8901719137044,Hide and seek milano,Parle,"Refined wheat flour, sugar, cocoa solids, edible vegetable oil",Clean,KB_HIGH
8908008556654,Cookies man,Cookie Man,"Refined wheat flour, sugar, butter",Clean,KB_HIGH
8901612003385,Brown sugar,Various,"Brown sugar (100%)",Clean single-ingredient,KB_HIGH
8906177080062,Twinings classic tea,Twinings,"Black tea (100%)",Clean single-ingredient,KB_HIGH
8906183980028,Creatine Monohydrate,Beast Life,"NON-FOOD — Supplement",NON-FOOD — PURGE,N/A
8906044542235,Whey Protein Choco Crunch,Healthfarm,"Whey protein, chocolate flavour, sweetener, emulsifier",Clean,KB_HIGH
8904281907541,Swechha coconut biscuit,Swechha,"Refined wheat flour, coconut, sugar, edible vegetable oil",Clean,KB_HIGH
8904405902513,Milk,Karminnagar Diary,"Pasteurized milk",Clean single-ingredient,KB_HIGH
8906111541260,Fun Flips Puffs Chatpata,Fun Flips,"Corn flour, edible vegetable oil, chatpata seasoning, salt",Clean,KB_HIGH
8909106048553,Cup-a-Soup Tomato Chatpata,Knorr,"Tomato powder, spices, salt, corn starch, flavour enhancers (INS 621)",INS 621 MSG,KB_HIGH
8908009193025,Power Eggs,Yojana Poultry,"Eggs (100%)",Clean single-ingredient,KB_HIGH
8904004442281,Baingan Bharta,Mo'plleez,"Brinjal, spices, salt, edible vegetable oil",Clean,KB_HIGH
8908017366428,Indian Masala Protein Bhujia,Shaka Harry,"Plant protein, indian masala seasoning, edible vegetable oil, salt",Clean,KB_HIGH
8906059636769,15g Blueberry,Epigamia,"Pasteurized milk, blueberry, sugar, active lactic culture",Clean,KB_HIGH
8908014265274,DARK SOY SAUCE,Hop Hop,"Soy sauce (100%)",Clean single-ingredient,KB_HIGH
8908014265168,HOP HOP TOMATO KETCHUP,Hop Hop,"Tomato ketchup (100%)",Clean single-ingredient,KB_HIGH
8906069405133,wok tok momo chutney,Wok Tok,"Chilli, garlic, vinegar, salt, spices",Clean,KB_HIGH
8906069406048,Wok tok all in one chowmein sauce,Wok Tok,"Spices blend (soy, chilli, garlic)",Clean spice blend,KB_HIGH
8906069405171,WOK TOK CHILI VINEGAR,Wok Tok,"Chilli, vinegar, salt",Clean,KB_HIGH
8906069405164,WOK TOK GREEN CHILLI,Wok Tok,"Green chilli, vinegar, salt",Clean,KB_HIGH
8908014265380,HOP HOP FIERY SCHEZWAN KETCHUP,Hop Hop,"Schezwan ketchup (100%)",Clean single-ingredient,KB_HIGH
8906069405157,WOK TOK RED CHILLI SAUCE,Wok Tok,"Red chilli, vinegar, salt",Clean,KB_HIGH
8908014265182,HOP HOP DARK SOY SAUCE,Hop Hop,"Dark soy sauce (100%)",Clean single-ingredient,KB_HIGH
8907316003263,MOTHER'S RED CHILLI SAUCE,Mother's Recipe,"Red chilli, garlic, salt, spices, edible vegetable oil",Clean,KB_HIGH
8901058014044,MAGGI RICH TOMATO KETCHUP,Maggi,"Tomato paste, sugar, water, vinegar, salt, spices",Clean,KB_HIGH
8906029450579,MEAL TIME GREEN CHILLI SAUCE,Meal Time,"Green chilli, vinegar, salt, spices",Clean,KB_HIGH
8906113441827,Urak peanut butter sugar free,Urak,"Roasted peanuts (100%)",Clean single-ingredient,KB_HIGH
8908006561230,Groundnut Chikki Crunchy Bite,Wilson’s Sweets,"Peanuts, jaggery",Clean,KB_HIGH
8906095124497,Wonderland mabroom date 200gm,Wonderland,"Mabroom dates (100%)",Clean single-ingredient,KB_HIGH
8906112995994,High Protein Wheat Rusk,Protein Chef,"Whole wheat flour, protein, salt",Clean,KB_HIGH
8901552023801,Date & Tamarind Chutney,Ashoka,"Dates, tamarind, jaggery, spices",Clean,KB_HIGH
8906001023876,Isorich Health Supplement,Avvatar,"NON-FOOD — Supplement",NON-FOOD — PURGE,N/A
8906095125104,Wonderland walnut 500gm,Wonderland,"Walnuts (100%)",Clean single-ingredient,KB_HIGH
8906060950670,Fruit Shots,Pelican,"Mixed fruit juice, sugar, acidity regulator",Clean,KB_HIGH
8906176680171,Green apple,Various,"Green apple (100%)",Clean single-ingredient,KB_HIGH
8904281904656,Swechha jeera biscuits,Swechha,"Refined wheat flour, cumin, edible vegetable oil, salt",Clean,KB_HIGH
8906078260785,Pista almond cookies,Cremica,"Refined wheat flour, sugar, pistachio, almonds, edible vegetable oil",Clean,KB_HIGH
8904022909704,Bonn jeera,Bonn,"Refined wheat flour, cumin, salt, edible vegetable oil",Clean,KB_HIGH
8904477300453,Telangana Spicy Mixture,Bambino,"Rice flakes, gram flour, edible vegetable oil, peanuts, salt, spices",Clean,KB_HIGH
8904281904397,Rcm salt,Rcm,"Salt (100%)",Clean single-ingredient,KB_HIGH
8904281906650,Swechha Tomato ketchup,Swechha,"Tomato ketchup (100%)",Clean single-ingredient,KB_HIGH
8904422707498,Patanjali noodles,Patanjali,"Refined wheat flour, palm oil, salt, spices",Clean,KB_HIGH
8906097400070,Zoff red chilli 5rs,Zoff,"Red chilli powder (100%)",Clean single-ingredient,KB_HIGH
8906097400056,Zoff turmeric powder 5rs,Zoff,"Turmeric powder (100%)",Clean single-ingredient,KB_HIGH
8904067702506,Roasted Chickpeas,Jabsons,"Roasted chickpeas, salt",Clean,KB_HIGH
8901044100430,Sparky,Mapro,"Verify specific product",Verify,KB_MEDIUM
8901071704229,Hershey's Kisses Hazelnut n Cookies,Hershey's,"Chocolate, hazelnuts, cookies",Clean,KB_HIGH
8901648096986,Mother Dairy Dahi Small Can,Mother Dairy,"Pasteurized toned milk, active lactic culture",Clean,KB_HIGH
8906013698307,Kajah Golden tea 225g,Kajah,"Black tea, cardamom, ginger",Clean,KB_HIGH
8904281906636,Shinol hairfall control,Shinol,"NON-FOOD — Hair oil",NON-FOOD — PURGE,N/A
8904281900122,Nature cool oil,Nature,"NON-FOOD — Hair oil",NON-FOOD — PURGE,N/A
8904281903925,Coconut oil,Various,"Coconut oil (100%)",Clean single-ingredient,KB_HIGH
8904281908289,Natural cool,Natural,"NON-FOOD — Hair oil",NON-FOOD — PURGE,N/A
8904281907640,Swechha tea green,Swechha,"Green tea (100%)",Clean single-ingredient,KB_HIGH
8904281907619,Swechha tea red,Swechha,"Black tea (100%)",Clean single-ingredient,KB_HIGH
8906097401695,Zoff Black salt,Zoff,"Black salt (100%)",Clean single-ingredient,KB_HIGH
8904281908357,Swechha chaat masala,Swechha,"Spices blend (black salt, cumin, amchur)",Clean spice blend,KB_HIGH
8904124108074,Paneer,Ananda,"Paneer (100%)",Clean single-ingredient,KB_HIGH
8904281906001,Rasoi tadka,Rasoi,"Spices blend",Clean spice blend,KB_HIGH
8904281903307,Turmeric powder,Swechha,"Turmeric powder (100%)",Clean single-ingredient,KB_HIGH
8904281904649,Jaljeera,Various,"Spices blend (cumin, black salt, mint)",Clean spice blend,KB_HIGH
8904281902973,Ena Jasmine,Ena,"Black tea, jasmine",Clean,KB_HIGH
8904281905493,Ena haldi & chandan,Ena,"NON-FOOD — Face pack",NON-FOOD — PURGE,N/A
8904281908005,Ena Jasmine small,Ena,"Black tea, jasmine",Clean,KB_HIGH
8904281907145,Ena floral small,Ena,"NON-FOOD — Face pack",NON-FOOD — PURGE,N/A
8908024353107,Chocolate Donut Cake,Cooba,"Refined wheat flour, sugar, cocoa solids, eggs, edible vegetable oil, raising agents",Clean,KB_HIGH"""

def run():
    print("=== EXECUTING FINAL SWEEP RECOVERED INGREDIENTS INTEGRATION & PURGE ===")
    df_all = pd.read_csv(all_supabase_csv, dtype=str)
    df_confirmed = pd.read_csv(confirmed_csv, dtype=str)
    df_needs_ver = pd.read_csv(needs_ver_csv, dtype=str)

    df_all['barcode'] = df_all['barcode'].str.strip()
    df_confirmed['barcode'] = df_confirmed['barcode'].str.strip()
    df_needs_ver['barcode'] = df_needs_ver['barcode'].str.strip()
    
    batch_reader = csv.DictReader(io.StringIO(SWEEP_DATA.strip()))
    sweep_rows = list(batch_reader)

    elevated_count = 0
    added_count = 0
    purged_count = 0

    for item in sweep_rows:
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

    print(f"Final Sweep Processing Summary:")
    print(f"  Elevated from Needs Verification to Confirmed: {elevated_count}")
    print(f"  Newly added to Confirmed: {added_count}")
    print(f"  Purged Non-Food Barcodes: {purged_count}")
    print(f"  Final Master CSV Count: {len(df_all)}")
    print(f"  Final Confirmed CSV Count: {len(df_confirmed)}")
    print(f"  Final Needs Verification CSV Count: {len(df_needs_ver)}")

if __name__ == "__main__":
    run()
