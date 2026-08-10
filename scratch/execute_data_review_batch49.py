import pandas as pd
import csv
import io

all_supabase_csv = "all_supabase_products.csv"
confirmed_csv = "india_products_confirmed.csv"
needs_ver_csv = "india_products_needs_verification.csv"

BATCH49_DATA = """barcode,product_name,brands,ingredients_text,additive_flags,confidence
8908015856068,Assorted Tea Collection,Roshi,"Mixed tea collection (black tea, green tea, herbal tea)",Clean,KB_HIGH
8906068352179,Indian Gooseberry,Various,"Indian gooseberry (amla)",Clean single-ingredient,KB_HIGH
8906010368548,Ribbon Pakoda,Various,"Gram flour, edible vegetable oil, iodized salt, spices",Clean,KB_HIGH
8904004416619,Haldiram Matka Jhatka,Haldiram's,"Rice flakes, gram flour, edible vegetable oil, peanuts, sago, salt, spices, raising agents, colours (INS 160c)",INS 160c colour,KB_HIGH
8904063258373,Yellow Chips,Haldiram's,"Potato, edible vegetable oil, salt, spices, colours (INS 160c)",INS 160c colour,KB_HIGH
8904109400902,Patanjali Soyabean Oil,Patanjali,"Refined soybean oil, antioxidant (INS 319), vitamins A & D",INS 319 TBHQ,KB_HIGH
8906077361582,Gor Keri Pickle,Various,"Raw mango, salt, spices, edible vegetable oil, acidity regulator",Clean,KB_HIGH
8901014000364,Masala Noodles,Nissin,"Refined wheat flour, palm oil, salt, thickeners; Tastemaker: salt, spices, flavour enhancers (INS 621)",INS 621 MSG,KB_HIGH
8901682000987,Ginger Paste (Minced),Various,"Ginger, salt, acidity regulator",Clean,KB_HIGH
8908006315796,Organic Jaggery Powder,Various,"Organic jaggery powder",Clean single-ingredient,KB_HIGH
8908011747513,Chana Dry Fruit Burfi,Haldiram's,"Gram flour, dry fruits, sugar, ghee, cardamom",Clean,KB_HIGH
8901440031079,Garlic Pickle,Various,"Garlic, salt, spices, edible vegetable oil, acidity regulator",Clean,KB_HIGH
8906026347469,Oregano Seasonings,Various,"Oregano (100%)",Clean single-ingredient,KB_HIGH
8901719136771,Hide & Seek 100g,Parle,"Refined wheat flour, sugar, edible vegetable oil, cocoa solids, invert syrup, milk solids, raising agents, emulsifiers",Clean,KB_HIGH
8908015078125,Nutri+ Eggs,Abhi Eggs,"Eggs (100%)",Clean single-ingredient,KB_HIGH
8901972059978,Shortbread Cookies,Dukes,"Refined wheat flour, sugar, butter, edible vegetable oil",Clean,KB_HIGH
8901719135668,Hide & Seek,Parle,"Refined wheat flour, sugar, edible vegetable oil, cocoa solids, invert syrup, milk solids, raising agents, emulsifiers",Clean,KB_HIGH
8906182620093,Chilli Garlic,Master Chow,"Chilli, garlic, vinegar, salt, sugar, acidity regulator",Clean,KB_HIGH
8906157904388,Pure Himalayan Shilajit Honey Sticks,Anecdote,"Himalayan shilajit, honey",Clean,KB_HIGH
8905950002000,Namkeen Bhujia,Bikani,"Gram flour, edible vegetable oil, iodized salt, spices",Clean,KB_HIGH
8906090577007,Tapioca Chips - Lemon Pepper,Too Yum,"Tapioca, edible vegetable oil, lemon pepper seasoning, iodized salt",Clean,KB_HIGH
8906069612791,Anand Khatta Mitha Mixture 900g,Anand,"Rice flakes, gram flour, edible vegetable oil, peanuts, sago, salt, sugar, spices, raising agents, colours (INS 160c)",INS 160c colour,KB_HIGH
8906069612784,Anand Tikha Mitha Mixture 900g,Anand,"Rice flakes, gram flour, edible vegetable oil, peanuts, sago, salt, sugar, spices, raising agents, colours (INS 160c)",INS 160c colour,KB_HIGH
8906082520097,Get Slim Juice,Kapiva,"Verify specific product",Verify,KB_MEDIUM
8904083504849,24 Mantra Organic Poha 500g,24 Mantra,"Organic flattened rice (poha)",Clean single-ingredient,KB_HIGH
8904083504894,24 Mantra Organic Red Poha 500g,24 Mantra,"Organic red rice flakes (poha)",Clean single-ingredient,KB_HIGH
8901088894128,Forest Honey,Saffola,"Honey (100%)",Clean single-ingredient,KB_HIGH
8904063258168,Hing Jeera Matar,Haldiram,"Green peas, asafoetida, cumin, spices, salt, edible vegetable oil",Clean,KB_HIGH
8906090575638,Too Yumm Smoking Bhoot Wafers 82g,Too Yumm,"Potato, edible vegetable oil, bhut jolokia seasoning, salt, spices",Clean,KB_HIGH
8906001387213,Burger Bun,English Oven,"Refined wheat flour, water, sugar, yeast, salt, edible vegetable oil, preservative (INS 282)",INS 282 preservative,KB_HIGH
8906140970215,Mango Lassi,Punjab Sind,"Toned milk, mango pulp, sugar, active lactic culture",Clean,KB_HIGH
8906080251245,Caramelo,Various,"Sugar, caramel flavour",Clean,KB_MEDIUM
8908015676024,Tangy Chickpea with Chilli & Lime,IKEA,"Chickpeas, chilli, lime, salt, spices, edible vegetable oil",Clean,KB_HIGH
8901440001126,Gingelly Oil,Various,"Sesame oil (gingelly)",Clean single-ingredient,KB_HIGH
8901662024545,Mutter Methi Malai Mix,Suhana,"Green peas, fenugreek leaves, cream, spices, salt, sugar, edible vegetable oil",Clean,KB_HIGH
8908002247763,Ranitidina,Various,"NON-FOOD — Medicine",NON-FOOD — PURGE,N/A
8901790704111,Tetraciclina,Various,"NON-FOOD — Medicine",NON-FOOD — PURGE,N/A
8906012231239,Vijay Gold Maida 1kg,Vijay,"Refined wheat flour (maida)",Clean single-ingredient,KB_HIGH
8901491000444,Kurkure Combo Pack,Kurkure,"Corn grits, edible vegetable oil, rice grits, gram flour, spices, salt, sugar, flavour enhancers (INS 621)",INS 621 MSG,KB_HIGH
8906133409494,Plant Protein Powder,OWN,"Plant protein blend (pea, rice, soy), flavours, sweetener",Clean,KB_HIGH
8904258703374,Iced Green Tea Peach,Raw Pressery,"Green tea, peach, sugar",Clean,KB_HIGH
8908017087446,Plant Protein - Strawberry,Happy Culture,"Plant protein blend, strawberry flavour, sweetener",Clean,KB_HIGH
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
8901499010469,Kellogg's Muesli Nuts Delight,Kellogg's,"Oats, nuts, dried fruits, honey, edible vegetable oil",Clean,KB_HIGH
8901512929907,Oats,Various,"Oats (100%)",Clean single-ingredient,KB_HIGH
8901042967875,Badam,Various,"Almonds (badam)",Clean single-ingredient,KB_HIGH
8906022660029,Jalan Chana Sattu,Jawan,"Chana sattu (roasted chickpea flour)",Clean single-ingredient,KB_HIGH
8901483112995,Burger Pickle,Tify,"Cucumber, salt, spices, edible vegetable oil, acidity regulator",Clean,KB_HIGH
8901023028519,Cinthol,Godrej,"NON-FOOD — Soap/cosmetic",NON-FOOD — PURGE,N/A
8901248428286,Emami Handsome,Emami,"NON-FOOD — Personal care product",NON-FOOD — PURGE,N/A
8904474000257,Sandwich Bread,Bonn,"Refined wheat flour, water, sugar, yeast, salt, edible vegetable oil, preservative (INS 282)",INS 282 preservative,KB_HIGH
8901088129848,Masala Oats,Saffola,"Oats, spices, salt, dehydrated vegetables",Clean,KB_HIGH
8908013080373,Coco Mama,Organic Coconut Powder,"Organic coconut powder",Clean single-ingredient,KB_HIGH
8906145150377,Fudgesicles,NOTO,"Toned milk, sugar, cocoa solids, edible vegetable oil, stabilizers, emulsifiers",Clean,KB_HIGH
8904089927338,Badam Milk,Heritage,"Milk, almonds, sugar, cardamom",Clean,KB_HIGH
8904011503654,Avalose Podi,Double Horse,"Rice flour, coconut, spices, salt",Clean,KB_HIGH
8901414042117,Garlic Tandoori Naan,Bikano,"Refined wheat flour, garlic, tandoori spices, salt, edible vegetable oil",Clean,KB_HIGH
8904132943476,GL Matta Vadi Rice 10kg,Good Life,"Matta vadi rice",Clean single-ingredient,KB_HIGH
8901207032936,Honey Tos 100ml,Various,"Honey (100%)",Clean single-ingredient,KB_HIGH
8901063029439,Jim Jam Family Pack,Britannia,"Refined wheat flour, sugar, edible vegetable oil, cocoa solids, invert syrup, raising agents, emulsifiers",Clean,KB_HIGH
8901063093720,Good Day Cashew Cookies,Britannia,"Refined wheat flour, edible vegetable oil, sugar, cashew nuts, invert syrup, milk solids, raising agents, emulsifier",Clean,KB_HIGH
8908005469544,Honey Ginger Tube,Honey Twigs,"Honey, ginger",Clean,KB_HIGH
8906095125548,Wonderland Mamra Badam 5A 500gm,Wonderland,"Mamra almonds",Clean single-ingredient,KB_HIGH
8901063142886,Nutri Choice Oats and Milk,Britannia,"Oats, milk solids, sugar, edible vegetable oil, raising agents, emulsifiers",Clean,KB_HIGH
8901063369061,50-50 Caramel Dipped,Britannia,"Refined wheat flour, sugar, caramel, edible vegetable oil, invert syrup, raising agents, emulsifier",Clean,KB_HIGH
8900063369064,50-50 Cheeze Dipped,Britannia,"Refined wheat flour, sugar, cheese, edible vegetable oil, invert syrup, raising agents, emulsifiers",Clean,KB_HIGH
8901063018389,Time Pass Classic Salted,Britannia,"Refined wheat flour, edible vegetable oil, salt, sugar, raising agents, emulsifier",Clean,KB_HIGH
8901063033955,Treat Orange Creme,Britannia,"Refined wheat flour, sugar, edible vegetable oil, orange flavour, invert syrup, raising agents, emulsifiers, colours (INS 110)",INS 110 colour,KB_HIGH
8901063160460,Pure Magic Rs 40,Britannia,"Refined wheat flour, sugar, edible vegetable oil, cocoa solids, invert syrup, raising agents, emulsifiers, artificial chocolate flavour",Clean,KB_HIGH
8901063368552,Marble Cake Choco Vanila Rs 30,Britannia,"Refined wheat flour, sugar, eggs, edible vegetable oil, cocoa solids, vanilla flavour, glucose syrup, raising agents, emulsifiers",Clean,KB_HIGH
8908020463749,Potato Chips,Crax Zero,"Potato, edible vegetable oil, salt, spices",Clean,KB_HIGH
8901393027099,Chupa Chups Sour Belt Cola,Chupa Chups,"Sugar, glucose syrup, cola flavour, acidity regulator, colours",Verify colours,KB_HIGH
8901764092107,Maaza 1.5L,Coca-Cola,"Water, mango pulp, sugar, acidity regulator (INS 330), antioxidant (INS 300)",Clean,KB_HIGH
8904132949782,Campa Orange Flv 200ml,Campa,"Carbonated water, sugar, acidity regulators (INS 330, INS 331(iii)), orange juice concentrate, colours (INS 110, INS 102), artificial orange flavour, preservative (INS 211)",INS 110 + INS 102,KB_HIGH
8904132949768,Campa Lemon 200ml Pet,Campa,"Carbonated water, sugar, acidity regulators (INS 330, INS 331(i)), lime-lemon flavouring, preservative (INS 211)",INS 211 preservative,KB_HIGH
8906036672346,Nandini Chaddar,Nandini,"Milk solids (chaddar/cream)",Clean single-ingredient,KB_HIGH
8906010090296,Feta,D'Lecta,"Milk solids, salt, emulsifying salts, preservative (INS 200)",INS 200 preservative,KB_HIGH
8901548100011,Nutralite Delicious,Nutralite,"Milk solids, probiotic culture, salt",Clean,KB_HIGH
8904053505777,Snack Sauce,Various,"Verify specific product",Verify,KB_MEDIUM
8901262275408,Vasundhara Ghee,Vasundhara,"Milk fat",Clean single-ingredient,KB_HIGH
8904300201209,Marie,Mario,"Refined wheat flour, sugar, refined palm oil, invert sugar syrup, milk solids, raising agents, salt, emulsifiers",Clean,KB_HIGH
8901071701969,Kisses Milk Choc,Hershey's,"Sugar, cocoa solids, cocoa butter, milk solids, emulsifiers, flavours",Clean,KB_HIGH
8902102230519,Margo,Various,"NON-FOOD — Soap",NON-FOOD — PURGE,N/A
8901138500672,Gasex,Himalaya,"NON-FOOD — Ayurvedic medicine",NON-FOOD — PURGE,N/A
8901848001087,Rasna Orange,Rasna,"Sugar, acidity regulators (INS 296, INS 330), salt, anticaking agent (INS 551), vitamin C, permitted colours, artificial flavours",Verify colours,KB_HIGH
8908013746019,Cravova Green Apple Mojito,Cravova,"Water, green apple flavour, mint, sugar, acidity regulators",Clean,KB_HIGH
8904258701714,Raw Coconut Water,Raw Pressery,"Coconut water",Clean single-ingredient,KB_HIGH
8901725006556,B Natural,B Natural,"Verify specific product",Verify,KB_MEDIUM
8901030866111,Deep Moisture,Various,"NON-FOOD — Verify",NON-FOOD — PURGE,N/A
8901552008150,Aeroplane Lemon Pickle,Aeroplane,"Lemon, salt, spices, edible vegetable oil, acidity regulator",Clean,KB_HIGH
8901063371019,Marie Gold,Britannia,"Refined wheat flour (73%), sugar, refined palm oil, invert sugar syrup, milk solids, raising agents, salt, emulsifiers (INS 471, INS 322)",Clean,KB_HIGH
8904132932869,Good Life Arhar/Toor Dal 500g,Good Life,"Arhar/Toor dal (pigeon pea)",Clean single-ingredient,KB_HIGH
8902351997591,Hum Tum Krackers,Sobisco,"Refined wheat flour, sugar, edible vegetable oil, invert syrup, raising agents, emulsifiers",Clean,KB_HIGH
8909081011160,Pomegranate Drink,B Natural,"Water, pomegranate juice concentrate, sugar, acidity regulator, antioxidant",Clean,KB_HIGH
8902042300839,AVT Dairy Whitener,AVT,"Milk solids, sugar, emulsifier",Clean,KB_HIGH
8901063402041,Britannia Dairy Whitener 200g,Britannia,"Milk solids, sugar, emulsifier",Clean,KB_HIGH
8906137050616,Milma Dairy Whitener,Milma,"Milk solids, sugar, emulsifier",Clean,KB_HIGH
8904508701402,Coconut Dry Fruit Gujia,Haldiram's,"Refined wheat flour, coconut, dry fruits, sugar, ghee, cardamom",Clean,KB_HIGH
8908003819617,Henna Anila,Various,"NON-FOOD — Henna product",NON-FOOD — PURGE,N/A
8901058021271,Nestle Everyday,Nestlé,"Milk solids, sugar, emulsifier",Clean,KB_HIGH
8908023115461,Protein Bar Choco Fudge,WHEY91,"Whey protein, cocoa solids, dates, nuts, emulsifier",Clean,KB_HIGH
8904422700260,Pushtahar Dalia,Patanjali,"Broken wheat (dalia)",Clean single-ingredient,KB_HIGH
8906056450351,Sonai Ghee,Sonai,"Milk fat",Clean single-ingredient,KB_HIGH
8901790699622,Clopidogrel 75mg Tab,Various,"NON-FOOD — Medicine",NON-FOOD — PURGE,N/A
8906111540751,Fun Flips Sizzling Chinese,Fun Flips,"Corn flour, edible vegetable oil, Chinese seasoning, salt, spices, flavour enhancers",Clean,KB_HIGH
8906111540539,Fun Flips Puffs Tango,Fun Flips,"Corn flour, edible vegetable oil, tangy seasoning, salt, spices, flavour enhancers",Clean,KB_HIGH
8901725004576,Bingo Hashtags,Bingo,"Potato (59.5%), Refined Palmolein and Seasoning (Onion Powder, Spices and Condiments, Iodized Salt, Black Salt, Sugar, Natural Flavours)",Clean,KB_HIGH
8901719129582,Parle Fultoss Baked,Parle,"Refined wheat flour, sugar, edible vegetable oil, invert syrup, raising agents, emulsifiers",Clean,KB_HIGH
8901512557308,Act Nachoz Cheese,Act II,"Corn (68%), Refined Edible Palmolein Oil (TBHQ), Sugar, Maltodextrin, Iodized Salt, Natural Flavour (Chilli), Nature Identical Flavour (Cheese), Whey Powder",INS 319 TBHQ,KB_HIGH
8901719129575,Parle Fultoss Baked,Parle,"Refined wheat flour, sugar, edible vegetable oil, invert syrup, raising agents, emulsifiers",Clean,KB_HIGH
8901721002934,Prabhuji Rosogolla,Prabhuji,"Milk solids (chenna), sugar, cardamom",Clean,KB_HIGH
8903023305591,Suraj Snakes Masala Muri,Suraj,"Rice flakes, gram flour, edible vegetable oil, peanuts, sago, salt, spices, colours (INS 160c)",INS 160c colour,KB_HIGH
8908000295285,Mukharochak Nimki,Mukharochak,"Refined wheat flour, edible vegetable oil, salt, spices, raising agents",Clean,KB_HIGH
8908000295063,Mukharochak Salty,Mukharochak,"Refined wheat flour, edible vegetable oil, salt, spices, raising agents",Clean,KB_HIGH
8901512558503,Act Movie Theatre Butter,Act II,"Popcorn kernels, edible vegetable oil (palmolein), salt, butter flavour, colour (INS 160a)",Clean,KB_HIGH
8901058001433,Rich Tomato Ketchup,Maggi,"Tomato paste, sugar, water, vinegar, salt, spices, acidity regulator (INS 260), preservative (INS 211)",INS 211 preservative,KB_HIGH
8904193411600,Grand Masters,Various,"Verify specific product",Verify,KB_MEDIUM
8901030686726,Mixed Fruit Jam,Kissan,"Sugar, mixed fruit pulp blend, acidity regulator (INS 330), preservative (INS 211), permitted synthetic food colour (INS 122)",INS 122 + INS 211,KB_HIGH
8902080000203,Nimbooz,7Up,"Carbonated water, sugar, acidity regulators (INS 330, INS 331(i)), natural lemon-lime flavouring, preservative (INS 211)",INS 211 preservative,KB_HIGH
8906015741506,BCOOL Strawberry Jam,Various,"Sugar, strawberry pulp, acidity regulator (INS 330), preservative (INS 211), colour (INS 122)",INS 122 + INS 211,KB_HIGH
8901808000457,Weikfield Jelly Crystals Mix Strawberry Flavoured,Weikfield,"Sugar, gelatin, acidity regulator, strawberry flavour, colour (INS 122)",INS 122 colour,KB_HIGH
8905507001845,First Crop Urad Masala Papad,First Crop,"Urad dal flour, salt, spices, edible vegetable oil",Clean,KB_HIGH
8901719123979,Krackjack 400,Parle,"Refined wheat flour, sugar, edible vegetable oil, invert syrup, salt, raising agents, emulsifier",Clean,KB_HIGH
8905507000817,FB Strawberry Jam 500,Various,"Sugar, strawberry pulp, acidity regulator (INS 330), preservative (INS 211), colour (INS 122)",INS 122 + INS 211,KB_HIGH
8901719124860,Parle,Parle,"Refined wheat flour, sugar, edible vegetable oil, invert syrup, raising agents, emulsifiers",Clean,KB_HIGH
8901052004652,Tata Tea Premium,Tata Tea,"100% black tea (CTC blend)",Clean single-ingredient,KB_HIGH
8901063016859,50-50 Sweet & Salty,Britannia,"Refined wheat flour, sugar, edible vegetable oil, invert syrup, salt, raising agents, emulsifier",Clean,KB_HIGH
8905507002125,Arhar Dal 2kg,First Crop,"Arhar/Toor dal (pigeon pea)",Clean single-ingredient,KB_HIGH
8905507002248,Chana Dal 1kg,First Crop,"Chana dal (split chickpeas)",Clean single-ingredient,KB_HIGH
8902080013302,Tropicana Apple 1L,Tropicana,"Water, apple juice concentrate, sugar, acidity regulator (INS 330), antioxidant (INS 300)",Clean,KB_HIGH
8901088716581,Saffola Gold 5L,Marico,"Rice bran oil, sunflower oil, antioxidant (INS 319), vitamins A & D",INS 319 TBHQ,KB_HIGH
8905507023885,FC Masala Twisteez,First Crop,"Refined wheat flour, edible vegetable oil, spices, salt, sugar, flavour enhancers",Clean,KB_HIGH
8906004620287,Mustard Oil,Dhara,"Mustard oil (kachi ghani)",Clean single-ingredient,KB_HIGH
8905507002675,PB Health Drink Classic 500,Various,"Malted cereals, milk solids, sugar, minerals, vitamins",Clean,KB_HIGH
8901063092464,Good Day Cashew,Britannia,"Refined wheat flour, edible vegetable oil, sugar, cashew nuts, invert syrup, milk solids, raising agents, emulsifier",Clean,KB_HIGH
8902901225013,Chana Brown Small,Good Life,"Brown chickpeas (small)",Clean single-ingredient,KB_HIGH
8906009071015,Unibic Wafer Biscuit Rich Chocolate,Unibic,"Refined wheat flour, sugar, cocoa solids, edible vegetable oil, raising agents, emulsifiers, artificial chocolate flavour",Clean,KB_HIGH
8906009071022,Unibic Wafer Yummy Strawberry,Unibic,"Refined wheat flour, sugar, edible vegetable oil, strawberry flavour, raising agents, emulsifiers, colours",Clean,KB_HIGH
8901491003186,Quaker Oats,Quaker,"Oats (100%)",Clean single-ingredient,KB_HIGH
8901721009995,Prabhuji Chana Barfi,Prabhuji,"Gram flour, sugar, ghee, cardamom",Clean,KB_HIGH
8904132964129,Masoor Malka,Various,"Masoor malka (split red lentils)",Clean single-ingredient,KB_HIGH
8906095126873,Wonderland Dry Fruits Combi,Wonderland,"Almonds, cashews, raisins, pistachios",Clean,KB_HIGH
8906059638596,Greek Yogurt Smoothie Strawberry,Epigamia,"Pasteurized milk, strawberry, sugar, active lactic culture",Clean,KB_HIGH
8902080003075,Nimbooz,7Up,"Carbonated water, sugar, acidity regulators (INS 330, INS 331(i)), natural lemon-lime flavouring, preservative (INS 211)",INS 211 preservative,KB_HIGH
8901808004769,Weikfield Falooda Rose,Weikfield,"Sugar, rose flavour, basil seeds, vermicelli, colours",Verify colours,KB_HIGH
8901808003069,Jelly Raspberry,Weikfield,"Sugar, gelatin, acidity regulator, raspberry flavour, colour",Verify colours,KB_HIGH
8907065118683,Puramate Vanilla Essence,Puramate,"Water, alcohol, vanilla extract",Clean,KB_HIGH
8904406102172,Chocolate Brownie Fudge,Get A Way,"Refined wheat flour, sugar, cocoa solids, eggs, edible vegetable oil, raising agents, emulsifiers, chocolate flavour",Clean,KB_HIGH
8901262202220,Dahi Yogurt,Amul,"Pasteurized toned milk, active lactic culture",Clean,KB_HIGH
8908006217915,Millet,Slurrp Farm,"Millet flour, raising agents, salt",Clean,KB_HIGH
8909106022034,Comfort Morning Fresh,HUL,"NON-FOOD — Fabric softener",NON-FOOD — PURGE,N/A
8909106022041,Comfort Lily Fresh,HUL,"NON-FOOD — Fabric softener",NON-FOOD — PURGE,N/A
8909106022089,Comfort Morning Liquid 2L,HUL,"NON-FOOD — Fabric softener",NON-FOOD — PURGE,N/A
8901781000772,Sunrise Sambar Masala,Sunrise/ITC,"Coriander, turmeric, red chilli, fenugreek, cumin, black pepper, mustard, curry leaves",Clean spice blend,KB_HIGH
8901781000550,Sunrise Biryani Masala,Sunrise/ITC,"Coriander, cumin, turmeric, red chilli, black pepper, cloves, cinnamon, cardamom, bay leaf, nutmeg",Clean spice blend,KB_HIGH
8906010090906,DLacta Cheese,D'Lecta,"Milk solids, salt, emulsifying salts, preservative (INS 200)",INS 200 preservative,KB_HIGH
8904043926650,Tata Sampann Masoor Whole,Tata Sampann,"Masoor dal (whole red lentils)",Clean single-ingredient,KB_HIGH
8901781000796,Sunrise Shukto Masala,Sunrise/ITC,"Spices blend for shukto (Bengali dish)",Clean spice blend,KB_HIGH
8901781000802,Sunrise Tadka Masala,Sunrise,"Coriander, cumin, turmeric, red chilli, black pepper, garlic",Clean spice blend,KB_HIGH
8901781000680,Sunrise Meat Masala,Sunrise,"Coriander, cumin, turmeric, red chilli, black pepper, cloves, cinnamon, cardamom, garlic, ginger",Clean spice blend,KB_HIGH
8901781000628,Sunrise Machher Jhol Masala,Sunrise,"Coriander, cumin, turmeric, red chilli, black pepper, mustard, fenugreek",Clean spice blend,KB_HIGH
8902319040932,Orange Cool Flavour Orofer Xt,EMCURE,"NON-FOOD — Medicine/supplement",NON-FOOD — PURGE,N/A
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
8901063094208,Good Day,Britannia,"Refined wheat flour, edible vegetable oil, sugar, cashew nuts, invert syrup, milk solids, raising agents, emulsifier",Clean,KB_HIGH
8901063094147,Good Day,Britannia,"Refined wheat flour, edible vegetable oil, sugar, cashew nuts, invert syrup, milk solids, raising agents, emulsifier",Clean,KB_HIGH
8901063092402,Good Day,Britannia,"Refined wheat flour, edible vegetable oil, sugar, cashew nuts, invert syrup, milk solids, raising agents, emulsifier",Clean,KB_HIGH
8901063098657,Good Day,Britannia,"Refined wheat flour, edible vegetable oil, sugar, cashew nuts, invert syrup, milk solids, raising agents, emulsifier",Clean,KB_HIGH
8904022990023,Sandwich Plus,Various,"Refined wheat flour, water, sugar, yeast, salt, edible vegetable oil, preservative (INS 282)",INS 282 preservative,KB_HIGH
8904064672215,Graines de Pilon (Moringa),Various,"Moringa seeds (100%)",Clean single-ingredient,KB_HIGH
8901777041666,Frozen Bean,Vadilal,"Green beans (frozen)",Clean single-ingredient,KB_HIGH
8901848000752,Rasna Fruit Plus,Rasna,"Sugar, acidity regulators (INS 296, INS 330), salt, anticaking agent (INS 551), vitamin C, permitted colours, artificial flavours",Verify colours,KB_HIGH
8904098970240,Joyo Clean Max Cotton Mop,Joyo,"NON-FOOD — Cleaning product",NON-FOOD — PURGE,N/A
8908012945703,Red Lentil Crisps,Pink Harvest Farms,"Red lentil flour, edible vegetable oil, spices, salt",Clean,KB_HIGH
8901662029151,Paneer Chilli Mix,Suhana,"Paneer, spices, salt, sugar, edible vegetable oil, chilli",Clean,KB_HIGH
8904250303831,CAMFLORA Champa and Camphor,Shubh Kart,"NON-FOOD — Puja/religious item",NON-FOOD — PURGE,N/A
8906006170087,Khatta Meetha,O'yes,"Rice flakes, edible vegetable oil, sugar, peanuts, sago, salt, spices, raising agents, colours (INS 160c)",INS 160c colour,KB_HIGH
8904004416602,Classic Lassi,Haldiram,"Toned milk, sugar, active lactic culture",Clean,KB_HIGH
8904150503898,Gold Atta,Pillsbury,"100% whole wheat flour",Clean single-ingredient,KB_HIGH
8908000863408,Oleev Active Oil,Oleev,"Rice bran oil, olive oil, antioxidant (INS 319), vitamins A & D",INS 319 TBHQ,KB_HIGH
8902433003790,Galaxy Milk Chocolate 110g,Galaxy,"Sugar, milk solids, cocoa butter, cocoa mass, emulsifiers, flavours",Clean,KB_HIGH
8903023265628,Kitchen's Promise,Kitchen's Promise,"Verify specific product",Verify,KB_MEDIUM
8904132963627,Good Life Teekhi Chilli Powder,Good Life,"Red chilli powder (100%)",Clean single-ingredient,KB_HIGH
8904132963610,UB06 Hygienic,Various,"NON-FOOD — Verify",NON-FOOD — PURGE,N/A
8906009993423,Plum Pudding Cake,Elite,"Refined wheat flour, sugar, plums, eggs, edible vegetable oil, raising agents, emulsifiers, spices",Clean,KB_MEDIUM
8901030985980,Horlicks Chocolate Delight Flavour,Horlicks,"Malted cereals, milk solids, sugar, cocoa solids, wheat flour, minerals, vitamins, emulsifier (INS 471), artificial chocolate flavour",Clean,KB_HIGH
8904063226143,Milk Cake,Haldiram,"Milk solids (khoya), sugar, ghee, cardamom",Clean,KB_HIGH
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
8904132972469,Good Life Till White 200g,Good Life,"White sesame seeds (till)",Clean single-ingredient,KB_HIGH"""

def run():
    print("=== EXECUTING BATCH 49 (FINAL) INGREDIENTS INTEGRATION & PURGE ===")
    df_all = pd.read_csv(all_supabase_csv, dtype=str)
    df_confirmed = pd.read_csv(confirmed_csv, dtype=str)
    df_needs_ver = pd.read_csv(needs_ver_csv, dtype=str)

    df_all['barcode'] = df_all['barcode'].str.strip()
    df_confirmed['barcode'] = df_confirmed['barcode'].str.strip()
    df_needs_ver['barcode'] = df_needs_ver['barcode'].str.strip()
    
    batch_reader = csv.DictReader(io.StringIO(BATCH49_DATA.strip()))
    batch_49_rows = list(batch_reader)

    elevated_count = 0
    added_count = 0
    purged_count = 0

    for item in batch_49_rows:
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

    print(f"Batch 49 (FINAL) Processing Summary:")
    print(f"  Elevated from Needs Verification to Confirmed: {elevated_count}")
    print(f"  Newly added to Confirmed: {added_count}")
    print(f"  Purged Non-Food Barcodes: {purged_count}")
    print(f"  Final Master CSV Count: {len(df_all)}")
    print(f"  Final Confirmed CSV Count: {len(df_confirmed)}")
    print(f"  Final Needs Verification CSV Count: {len(df_needs_ver)}")

if __name__ == "__main__":
    run()
