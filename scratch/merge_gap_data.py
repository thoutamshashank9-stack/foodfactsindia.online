import os
import io
import sys
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"c:\Users\thout\Downloads\check it"

confirmed_path = os.path.join(BASE_DIR, "india_products_confirmed.csv")
needs_ver_path = os.path.join(BASE_DIR, "india_products_needs_verification.csv")

# Load existing datasets
df_c = pd.read_csv(confirmed_path, dtype=str)
df_nv = pd.read_csv(needs_ver_path, dtype=str)

# Ensure barcodes are strings and stripped
df_c['barcode'] = df_c['barcode'].str.strip()
df_nv['barcode'] = df_nv['barcode'].str.strip()

# Track original counts
orig_c_count = len(df_c)
orig_nv_count = len(df_nv)

# Set up sets for fast existence check
c_barcodes = set(df_c['barcode'].dropna().tolist())
nv_barcodes = set(df_nv['barcode'].dropna().tolist())

# CSV data blocks from user
csv_block_1 = """rank,category,product_name,brand,barcode_status,barcode,ingredients_text,additive_flags,allergens,source_plan,confidence,action
1,Biscuits,Parle-G Original Glucose,Parle Products,IN_DB,8901719128486,"Wheat flour, sugar, invert syrup, refined palm oil, salt, skimmed milk powder, raising agents (INS 503(ii), INS 500(ii)), emulsifier (INS 471), dough conditioner, artificial vanilla flavour","None significant","Wheat, Milk, Sulphite",parleproducts.com + physical pack,KB_HIGH,Spot-check then publish
2,Biscuits,Parle-G Gold,Parle Products,IN_DB,8901719135477,"Wheat flour, sugar, invert syrup, edible vegetable oil (palm), milk solids, salt, raising agents (INS 503(ii), INS 500(ii)), emulsifier (INS 471), flavour","None significant","Wheat, Milk",parleproducts.com,KB_HIGH,Spot-check then publish
3,Biscuits,Good Day Cashew Cookies,Britannia,IN_DB,8901063151352,"Refined wheat flour, edible vegetable oil (palm), sugar, cashew nuts (4.5%), invert syrup, milk solids, butter (0.6%), raising agents (INS 503(i), INS 500(i)), salt, emulsifier (soya lecithin INS 322)","None significant","Wheat, Milk, Cashew, Soy",britannia.co.in/product/good-day,KB_HIGH,Spot-check then publish
4,Biscuits,Marie Gold,Britannia,IN_DB_GAP,8901063162303,"Refined wheat flour (73%), sugar, refined palm oil, invert sugar syrup, milk solids & sweetened condensed milk, raising agents (INS 503(ii), INS 500(ii)), salt, emulsifiers (INS 471, INS 322)","None significant","Wheat, Milk",britannia.co.in,KB_HIGH,Spot-check then publish
5,Biscuits,50-50 Maska Chaska,Britannia,TO_SCAN,,,"Pending capture","Wheat",britannia.co.in,SCAN_REQUIRED,Retail scan
6,Biscuits,Milk Bikis,Britannia,IN_DB_GAP,8901063012578,"Refined wheat flour, sugar, milk solids, edible vegetable oil (palm), invert syrup, raising agents (INS 503(ii), INS 500(ii)), salt, emulsifier (INS 322), flavour","None significant","Wheat, Milk",britannia.co.in,KB_HIGH,Spot-check then publish
7,Biscuits,Little Hearts,Britannia,TO_SCAN,,,"Pending capture","Wheat, Milk",britannia.co.in,SCAN_REQUIRED,Retail scan
8,Biscuits,Treat Jim Jam,Britannia,IN_DB_GAP,8901063029415,"Refined wheat flour, sugar, edible vegetable oil (palm), invert syrup, raising agents, salt, emulsifiers, permitted synthetic food colours (INS 122, INS 110)","INS 122 Carmoisine — US/Japan-restricted; INS 110 Sunset Yellow — EU warning","Wheat",britannia.co.in + pack,KB_HIGH,Verify colour codes on pack before flag
9,Biscuits,Dark Fantasy Choco Fills,Sunfeast (ITC),IN_DB_GAP,8901725003876,"Choco crème (sugar, refined palmolein, refined palm oil, cocoa solids), refined wheat flour, sugar, invert syrup, liquid glucose, edible vegetable oil, cocoa solids, milk solids, butter, raising agents (INS 503(ii), INS 500(i)), emulsifiers (INS 322, INS 471), salt","High fat/sugar; legacy labels carried hydrogenated oil","Wheat, Milk, Soy",itcportal.com/sunfeast,KB_HIGH,Spot-check then publish
10,Bakery,Brown Bread,Britannia,IN_DB_GAP,8901063342910,"Whole wheat flour (approx. 50%), refined wheat flour, water, sugar, edible vegetable oil, gluten, yeast, iodized salt, preservative (INS 282), emulsifiers (INS 471, INS 472e)","INS 282 preservative","Wheat, Gluten",britannia.co.in,KB_HIGH,Spot-check then publish
11,Chocolate,Cadbury Dairy Milk,Mondelez,IN_DB,8901233028361,"Sugar, milk solids, cocoa butter, cocoa mass, emulsifiers (soya lecithin INS 322, INS 476), flavours (natural & nature-identical vanilla)","None significant","Milk, Soy",mondelezindia.com,KB_HIGH,Spot-check then publish
12,Chocolate,Cadbury Dairy Milk Silk,Mondelez,IN_DB,8901233033563,"Sugar, milk solids, cocoa butter, cocoa mass, emulsifiers (INS 322, INS 476), flavours","None significant","Milk, Soy",mondelezindia.com,KB_HIGH,Spot-check then publish
13,Chocolate,Cadbury Gems,Mondelez,TO_SCAN,,,"Shell colours need pack verification (INS 102/110/129/132/133)","Milk, Soy, Wheat",mondelezindia.com,SCAN_REQUIRED,Physical pack mandatory (colour codes)
14,Chocolate,Cadbury 5 Star,Mondelez,TO_SCAN,,,"INS 150d caramel","Milk, Soy",mondelezindia.com,SCAN_REQUIRED,Retail scan
15,Chocolate,Nestlé KitKat,Nestlé,IN_DB_GAP,89005637,"Sugar, refined wheat flour, milk solids, hydrogenated vegetable oil (palm), cocoa solids, emulsifier (soya lecithin INS 322), yeast, salt, raising agent (INS 500(ii)), flavouring","Hydrogenated oil present — trans-fat watch","Wheat, Milk, Soy",nestle.in/brands/kitkat,KB_HIGH,Spot-check then publish
16,Chocolate,Nestlé Munch,Nestlé,TO_SCAN,,,"None significant","Wheat, Milk, Soy",nestle.in,SCAN_REQUIRED,Retail scan
17,Chocolate,Nestlé Perk,Nestlé,TO_SCAN,,,"None significant","Wheat, Milk, Soy",nestle.in,SCAN_REQUIRED,Retail scan
18,Chocolate,Choclairs,Cadbury,IN_DB_GAP,8901233031644,"Sugar, glucose syrup, hydrogenated vegetable oil (palm kernel), milk solids, cocoa solids, emulsifier (INS 322), salt, flavouring","Hydrogenated oil","Milk, Soy",mondelezindia.com,KB_MEDIUM,Verify pack
19,Chocolate,Cadbury Melody,Mondelez,TO_SCAN,,,"Hydrogenated oil","Milk, Soy",mondelezindia.com,SCAN_REQUIRED,Retail scan
20,Chocolate,Cadbury Bournville,Mondelez,TO_SCAN,,,"None significant","Milk, Soy",mondelezindia.com,SCAN_REQUIRED,Retail scan
21,Noodles,Maggi 2-Minute Masala,Nestlé,IN_DB_GAP,8901058901580,"Noodles: refined wheat flour (maida), palm oil, iodized salt, wheat gluten, thickeners (INS 508, INS 412), acidity regulators (INS 501(i), INS 500(i)); Tastemaker: salt, onion, sugar, coriander, chilli, turmeric, garlic, cumin, fenugreek, antioxidant (INS 319)","INS 319 TBHQ — Japan-restricted","Wheat, Gluten",nestle.in/brands/maggi2-minutenoodles,KB_HIGH,Spot-check then publish
22,Noodles,Maggi Atta Noodles,Nestlé,IN_DB,8901058854107,"Whole wheat flour, palm oil, iodized salt, thickeners (INS 508, INS 412), acidity regulators; tastemaker with antioxidant (INS 319)","INS 319 TBHQ","Wheat, Gluten",nestle.in,KB_HIGH,Spot-check then publish
23,Noodles,Yippee! Magic Masala,Sunfeast (ITC),IN_DB,8901725005917,"Instant noodles: refined wheat flour (78.4%), refined palm oil, iodized salt, wheat gluten, thickeners (INS 508, INS 412); masala: spices, dehydrated vegetables, sugar, salt, flavour enhancers (INS 621, INS 627, INS 631)","INS 621 MSG","Wheat, Gluten",itcportal.com,KB_HIGH,Spot-check then publish
24,Noodles,Top Ramen Masala,Nissin,IN_DB_GAP,8901014002047,"Refined wheat flour, edible palm oil, salt, thickeners (INS 508, INS 412), acidity regulators; masala: spices, sugar, salt, flavour enhancer (INS 621)","INS 621 MSG","Wheat",nissinfoods.in,KB_HIGH,Spot-check then publish
25,Noodles,Ching's Secret Hakka Noodles,Capital Foods,IN_DB_GAP,8901595853861,"Refined wheat flour, edible vegetable oil (palm), salt, acidity regulators, thickener; seasoning: spices, salt, flavour enhancer (INS 621)","INS 621 MSG","Wheat",chingssecret.com,KB_HIGH,Spot-check then publish
26,Noodles,Wai Wai X-Press Masala,Wai Wai,IN_DB_GAP,8906013032224,"Refined wheat flour, palm oil, salt, masala (spices, sugar, flavour enhancer INS 621)","INS 621 MSG","Wheat",waiwai.co.in,KB_MEDIUM,Verify pack
27,Noodles,Bambino Roasted Vermicelli,Bambino,IN_DB_GAP,8901242107408,"Rice / wheat semolina (roasted), salt","None","Gluten (wheat variant)",bambinofoods.com,KB_MEDIUM,Verify pack (rice vs wheat variant)
28,RTE,MTR Pongal,MTR Foods,IN_DB_GAP,8901042955957,"Rice, moong dal, salt, spices, edible oil, curry leaves","None","May contain milk",mtrfoods.com,KB_MEDIUM,Verify pack
29,Soup,Knorr Tomato Soup,HUL,TO_SCAN,,,"MSG often present (INS 621)","May contain gluten",hul.co.in/brands/knorr,SCAN_REQUIRED,Retail scan
30,Sauce,Maggi Rich Tomato Sauce,Nestlé,IN_DB_GAP,8901058004922,"Tomato paste, sugar, salt, spices & condiments, acidity regulator (INS 260), preservative (INS 211)","INS 211 preservative","None declared",nestle.in,KB_HIGH,Spot-check then publish
31,Chips,Lay's India's Magic Masala,PepsiCo,IN_DB_GAP,8901491001137,"Potato, edible vegetable oil (palmolein/rice bran), seasoning [sugar, iodized salt, spices & condiments (onion, chilli, dried mango powder, coriander, garlic), flavour enhancers (INS 621, INS 627, INS 631), acidity regulators (INS 330, INS 296), anticaking agent (INS 551)]","INS 621 MSG","None declared",pepsicoindia.com,KB_HIGH,Spot-check then publish
32,Chips,Lay's Classic Salted,PepsiCo,IN_DB_GAP,8901491983211,"Potato, edible vegetable oil (palmolein), salt","Clean label","None declared",pepsicoindia.com,KB_HIGH,Spot-check then publish
33,Chips,Kurkure Masala Munch,PepsiCo,TO_SCAN,,,"Colour INS 160c; MSG","May contain milk",pepsicoindia.com,SCAN_REQUIRED,Retail scan
34,Chips,Uncle Chipps Achaari Masala,PepsiCo,TO_SCAN,,,"MSG","None declared",pepsicoindia.com,SCAN_REQUIRED,Retail scan
35,Chips,Bingo Mad Angles Achari Masti,ITC,IN_DB,8901725013714,"Corn & wheat grits, edible vegetable oil, seasoning (spices, salt, sugar, flavour enhancers INS 621/627/631)","MSG","Wheat, Gluten",itcportal.com,KB_MEDIUM,Verify pack
36,Namkeen,Haldiram's Bhujia Sev,Haldiram's,TO_SCAN,,,"MSG trace in some variants","Gram flour",haldirams.com,SCAN_REQUIRED,Retail scan
37,Namkeen,Haldiram's Aloo Bhujia,Haldiram's,IN_DB_GAP,8904063254696,"Potato flakes & starch, edible vegetable oil (palmolein), gram flour, iodized salt, spices (red chilli, cumin), colour","None significant","Gram flour",haldirams.com,KB_HIGH,Spot-check then publish
38,Namkeen,Balaji Snack'em Masala Masti,Balaji Wafers,IN_DB_GAP,8906010504359,"Wheat & corn grits, edible vegetable oil, seasoning (spices, salt, sugar, flavour enhancers)","MSG","Wheat",balajiwafers.com,KB_MEDIUM,Verify pack
39,Popcorn,Act II Butter Delite,Agro Tech (ACT II),IN_DB_GAP,8901512500205,"Popcorn kernels, edible vegetable oil (palmolein), salt, butter flavour, colour (INS 160a)","None significant","Milk (flavour)",act2popcorn.in,KB_HIGH,Spot-check then publish
40,Chips,Too Yumm Multigrain Chips,ITC/RPSG,IN_DB_GAP,8906090571258,"Multigrain blend (oats, corn, wheat, rice, quinoa), edible vegetable oil, seasoning (spices, salt)","None significant","Wheat, Oats, Gluten",tooyumm.com,KB_MEDIUM,Verify pack
41,Beverage,Thums Up,Coca-Cola India,IN_DB_GAP,3948764052705,"Carbonated water, sugar, acidity regulator (INS 338), colour (INS 150d), natural & nature-identical flavouring (cola), caffeine","INS 150d + INS 338","None",coca-cola.com/in/en,KB_HIGH,Spot-check then publish
42,Beverage,Limca,Coca-Cola India,IN_DB_GAP,8901764052309,"Carbonated water, sugar, acidity regulators (INS 330, INS 331(i)), stabilizers (INS 414, INS 471), preservative (INS 211), lime-lemon flavouring","INS 211 preservative","None",coca-cola.com/in/en,KB_HIGH,Spot-check then publish
43,Beverage,Sprite,Coca-Cola India,TO_SCAN,,,"None significant","None",coca-cola.com/in/en,SCAN_REQUIRED,Retail scan
44,Beverage,Coca-Cola Original,Coca-Cola India,TO_SCAN,,,"INS 150d + INS 338 + caffeine","None",coca-cola.com/in/en,SCAN_REQUIRED,Retail scan
45,Beverage,Maaza,Coca-Cola India,TO_SCAN,,,"Verify colour on pack","None",coca-cola.com/in/en,SCAN_REQUIRED,Retail scan
46,Beverage,Frooti Mango,Parle Agro,IN_DB,8902579103187,"Water, mango pulp (12-19%), sugar, acidity regulators (INS 330, INS 331(iii)), antioxidant (INS 300), permitted synthetic food colour (INS 110), artificial mango flavour","INS 110 Sunset Yellow — EU warning / US Southampton Six","None",parleagro.com/brand/frooti,KB_HIGH,Spot-check then publish
47,Beverage,Appy Fizz,Parle Agro,IN_DB,8902579131036,"Carbonated water, sugar, apple juice concentrate, acidity regulators (INS 330, INS 331(iii)), preservative (INS 211), colour (INS 150d), flavouring","INS 150d + INS 211","None",parleagro.com,KB_HIGH,Spot-check then publish
48,Juice,Tropicana Orange,PepsiCo,TO_SCAN,,,"None significant","None",pepsicoindia.com,SCAN_REQUIRED,Retail scan
49,Juice,Real Mixed Fruit,Dabur,TO_SCAN,,,"None significant","None",dabur.com/brands/real,SCAN_REQUIRED,Retail scan
50,Juice,Minute Maid Nimbu Masala,Coca-Cola India,TO_SCAN,,,"INS 211 preservative","None",coca-cola.com/in/en,SCAN_REQUIRED,Retail scan
51,Health Drink,Horlicks Classic Malt,HUL,IN_DB_GAP,8901030976186,"Malted cereals (66.7%) [barley, wheat flour, wheat, millet], milk solids (14%), sugar, wheat gluten, iodized salt, minerals, vitamins, emulsifier (INS 471)","None significant","Wheat, Gluten, Milk, Barley",hul.co.in/brands/horlicks,KB_HIGH,Spot-check then publish
52,Health Drink,Bournvita,Mondelez,IN_DB_GAP,8901233022574,"Malt extract (wheat/barley), sugar, milk solids, cocoa solids, liquid glucose, minerals (Ca, Fe, Zn, Cu, I), vitamins, emulsifier (INS 322), salt","High sugar flag (CCPA scrutiny)","Wheat, Gluten, Milk",mondelezindia.com,KB_HIGH,Spot-check then publish
53,Health Drink,Boost,HUL,IN_DB,8901571004409,"Cereal extract (50%) [barley, wheat, millet], malted barley (21%), sugar, wheat flour, milk solids (6%), minerals, natural colour (INS 150c), vitamins","INS 150c","Wheat, Gluten, Milk, Barley",hul.co.in/brands/boost,KB_HIGH,Spot-check then publish
54,Health Drink,Complan Kesar Badam,HUL legacy,IN_DB_GAP,8901542000065,"Milk solids (approx. 52%), sugar, peanut oil, maltodextrin, almonds (0.8%), minerals, vitamins, colours (INS 100(i), INS 160b(ii)), flavouring","Colours 100/160b (natural-class)","Milk, Peanut",complan.in,KB_HIGH,Spot-check then publish
55,Health Drink,Glucon-D,Tata Consumer,TO_SCAN,,,"Tangy variant carries vitamin C + colour","None",glucond.in,SCAN_REQUIRED,Retail scan
56,Health Drink,Tang Orange,Kraft/MDL,TO_SCAN,,,"Colours INS 110/102 (verify)","None",tangdrink.in,SCAN_REQUIRED,Retail scan
57,Health Drink,Rasna Orange,Orangewood Labs,TO_SCAN,,,"Colours INS 110/102 (verify)","None",rasna.com,SCAN_REQUIRED,Retail scan
58,Baby Food,Cerelac Wheat Apple,Nestlé,IN_DB_GAP,8901058897241,"Wheat flour, skimmed milk powder, sugar, apple flakes, vegetable oil (palm), minerals, vitamins","Infant formula — FSSAI special category","Wheat, Milk",nestle.in/brands/cerelac,KB_MEDIUM,Verify pack (regulated category)
59,Health Drink,Horlicks Protein Plus,HUL,TO_SCAN,,,"None significant","Milk, Wheat",hul.co.in,SCAN_REQUIRED,Retail scan
60,Health Drink,Protinex Original,Nutricia/Danone,TO_SCAN,,,"None significant","Milk, Soy",protinex.com,SCAN_REQUIRED,Retail scan
61,Dairy,Amul Butter,GCMMF,TO_SCAN,,,"None significant","Milk",amul.com,SCAN_REQUIRED,Simple — 2 ingredients
62,Dairy,Amul Taaza Toned Milk,GCMMF,IN_DB,8901262153577,"Toned milk (3.0% fat, 8.5% SNF), vitamins A & D","Clean single-ingredient","Milk",amul.com,KB_HIGH,Spot-check then publish
63,Dairy,Amul Pure Ghee,GCMMF,IN_DB_GAP,8901262030144,"Pure cow ghee (milk fat)","Clean single-ingredient","Milk",amul.com,KB_HIGH,Spot-check then publish
64,Dairy,Amul Masti Spiced Buttermilk,GCMMF,IN_DB_GAP,8901262200233,"Buttermilk, water, salt, spices (cumin, ginger, curry leaves, green chilli), iodized salt","None significant","Milk",amul.com,KB_MEDIUM,Verify pack
65,Dairy,Amul Cheese Slices,GCMMF,TO_SCAN,,,"Emulsifying salts (INS 331, INS 452)","Milk",amul.com,SCAN_REQUIRED,Retail scan
66,Dairy,Mother Dairy Classic Dahi,Mother Dairy,IN_DB_GAP,8901648018186,"Pasteurized toned milk, live curd culture","Clean","Milk",motherdairy.com,KB_HIGH,Spot-check then publish
67,Dairy,Britannia Dahi,Britannia,TO_SCAN,,,"Clean","Milk",britannia.co.in,SCAN_REQUIRED,Retail scan
68,Dairy,Epigamia Greek Yogurt,Drums Food,IN_DB_GAP,8906059638510,"Pasteurized milk, live cultures, fruit prep (for flavoured variants: sugar, fruit, natural colour)","Clean","Milk",epigamia.in,KB_MEDIUM,Verify pack
69,Ice Cream,Kwality Wall's Cornetto,HUL,TO_SCAN,,,"Emulsifiers 471/322/476; stabilizers 410/412/407; colours 150d/160a","Milk, Wheat, Soy",kwalitywalls.in,SCAN_REQUIRED,Retail scan
70,Ice Cream,Amul Vanilla Magic,GCMMF,TO_SCAN,,,"Stabilizers 410/412/407/466; emulsifier 471","Milk",amul.com,SCAN_REQUIRED,Retail scan
71,Breakfast,Kellogg's Corn Flakes Original,Kellogg India,TO_SCAN,,,"Added vitamins & minerals","Barley malt (gluten)",kelloggsindia.com,SCAN_REQUIRED,Retail scan
72,Breakfast,Kellogg's Chocos,Kellogg India,TO_SCAN,,,"Added vitamins & minerals","Wheat, Gluten",kelloggsindia.com,SCAN_REQUIRED,Retail scan
73,Breakfast,Quaker Oats,PepsiCo,IN_DB_GAP,8901491702188,"100% wholegrain rolled oats","Clean single-ingredient","Oats (gluten)",quakeroats.in,KB_HIGH,Spot-check then publish
74,Breakfast,Saffola Oats,Marico,TO_SCAN,,,"Clean single-ingredient","Oats",saffola.in,SCAN_REQUIRED,Retail scan
75,Staple,Aashirvaad Shudh Chakki Atta,ITC,TO_SCAN,,,"Clean single-ingredient","Wheat, Gluten",itcportal.com,SCAN_REQUIRED,Retail scan
76,Staple,Tata Salt Iodised,Tata Consumer,TO_SCAN,,,"Potassium iodate; anticaking agent (INS 536)","None",tatasalt.in,KB_HIGH,Spot-check then publish
77,Oil,Fortune Refined Sunflower Oil,Adani Wilmar,IN_DB,8906007280280,"Refined sunflower oil, antioxidant TBHQ (INS 319), vitamins A & D","INS 319 TBHQ — Japan-restricted","None",fortuneoil.in,KB_HIGH,Spot-check then publish
78,Staple,Fortune Rawa Semolina,Adani Wilmar,IN_DB_GAP,8906008811223,"Durum wheat semolina (sooji)","Clean","Wheat, Gluten",fortuneoil.in,KB_HIGH,Spot-check then publish
79,Staple,Daawat Brown Basmati Rice,LT Foods,IN_DB_GAP,8901537074354,"100% wholegrain brown basmati rice","Clean","None",daawat.com,KB_HIGH,Spot-check then publish
80,Staple,Kohinoor Charminar Rice,Kohinoor,IN_DB_GAP,8906008813852,"100% basmati rice","Clean","None",kohinoorfoods.com,KB_HIGH,Spot-check then publish
81,Condiment,Kissan Mixed Fruit Jam,HUL,IN_DB,8901030831720,"Sugar, mixed fruit pulp blend (approx. 46%) [banana, apple, pineapple, orange, mango, papaya], acidity regulator (INS 330), preservative (INS 211 sodium benzoate), permitted synthetic food colour (INS 122)","INS 122 Carmoisine — US/Japan-restricted; INS 211 preservative","None",hul.co.in/brands/kissan,KB_HIGH,Spot-check then publish
82,Condiment,Kissan Fresh Tomato Ketchup,HUL,TO_SCAN,,,"INS 260 + INS 211","None",hul.co.in/brands/kissan,SCAN_REQUIRED,Retail scan
83,Condiment,Maggi Tomato Ketchup,Nestlé,TO_SCAN,,,"INS 260 + INS 211","None",nestle.in,SCAN_REQUIRED,Retail scan
84,Condiment,Veeba Mayonnaise (Eggless),Veeba,TO_SCAN,,,"INS 211 preservative","Mustard/Soy variants",veeba.in,SCAN_REQUIRED,Retail scan
85,Condiment,Dr. Oetker FunFoods Veg Mayonnaise,Dr. Oetker,IN_DB,8906002004379,"Refined soybean oil, water, sugar, vinegar, iodized salt, thickener (INS 1422), preservative (INS 211), mustard, antioxidant","INS 211","Soy, Mustard",droetker.in,KB_MEDIUM,Verify pack
86,Condiment,Del Monte Eggless Mayonnaise,Del Monte,TO_SCAN,,,"INS 211","Soy",delmonte.in,SCAN_REQUIRED,Retail scan
87,Masala,Everest Garam Masala,Everest,TO_SCAN,,,"Clean spice blend","None",everestmasala.com,SCAN_REQUIRED,Retail scan
88,Masala,MDH Chhole Masala,MDH,TO_SCAN,,,"Clean spice blend","None",mdhmdhmasala.com,SCAN_REQUIRED,Retail scan
89,Masala,Catch Black Pepper,Catch (Tata),TO_SCAN,,,"Clean","None",catch.co.in,SCAN_REQUIRED,Retail scan
90,Sauce,Veeba Sriracha,Veeba,IN_DB_GAP,8906069400657,"Chilli, sugar, water, vinegar, iodized salt, garlic, thickener, preservative (INS 211)","INS 211","None",veeba.in,KB_MEDIUM,Verify pack
91,Tea,Brooke Bond Red Label,HUL,IN_DB_GAP,8901030882609,"100% black tea (CTC dust & fannings blend)","Clean single-ingredient","None",hul.co.in/brands/brooke-bond-red-label,KB_HIGH,Spot-check then publish
92,Tea,Brooke Bond Taj Mahal,HUL,IN_DB_GAP,8901030251504,"100% black tea","Clean single-ingredient","None",hul.co.in,KB_HIGH,Spot-check then publish
93,Tea,Tata Tea Gold,Tata Consumer,TO_SCAN,,,"Clean","None",tataconsumer.com,SCAN_REQUIRED,Retail scan
94,Coffee,Nescafé Classic,Nestlé,TO_SCAN,,,"Clean","None",nescafe.in,SCAN_REQUIRED,Retail scan
95,Coffee,Nescafé Gold Cappuccino,Nestlé,IN_DB_GAP,8901058865660,"Instant coffee, sugar, milk solids, glucose syrup, hydrogenated vegetable oil (palm kernel), salt, stabilizers (INS 340(ii), INS 452(i)), emulsifier (INS 471), anticaking agent (INS 551)","Hydrogenated oil","Milk",nescafe.in,KB_MEDIUM,Verify pack
96,Coffee,Bru Gold,HUL,IN_DB_GAP,8901030373930,"Instant coffee (freeze-dried)","Clean","None",hul.co.in/brands/bru,KB_HIGH,Spot-check then publish
97,RTE,Haldiram's Minute Khana Punjabi Tadka,Haldiram's,IN_DB_GAP,8904063231765,"Frozen paratha/meal: refined wheat flour, vegetables, edible oil, spices, salt","None significant","Wheat, Gluten",haldirams.com,KB_MEDIUM,Verify pack
98,RTE,Aashirvaad Instant Veggie Upma,ITC,IN_DB_GAP,8901725114022,"Semolina (sooji), dehydrated vegetables, salt, spices, sugar, edible oil, flavour enhancer","Possible MSG","Wheat, Gluten",itcportal.com,KB_MEDIUM,Verify pack
99,RTE,Gits Khatta Dhokla,Gits Food,IN_DB_GAP,8901155107328,"Semolina & gram flour mix, sugar, tamarind, salt, spices, raising agents","None significant","Wheat, Gram",gitsfood.com,KB_MEDIUM,Verify pack
100,RTE,Sumeru French Fries,Sumeru Foods,IN_DB_GAP,8901688122966,"Potato, edible vegetable oil (palmolein)","Clean","None",sumerufoods.com,KB_MEDIUM,Verify pack"""

csv_block_2 = """rank,category,product_name,brand,barcode_status,barcode,ingredients_text,additive_flags,allergens,source_plan,confidence,action
1,Biscuits,Britannia Bourbon Classic,Britannia,IN_DB_GAP,8901063139336,"Refined wheat flour, sugar, bakery shortening, corn starch, cocoa solids, raising agents, emulsifiers, colours (INS 150c)","INS 150c Caramel","Wheat, Milk, Soy",britannia.co.in,KB_HIGH,Spot-check then publish
2,Biscuits,Britannia Tiger Krunch,Britannia,IN_DB_GAP,8901063012578,"Refined wheat flour, sugar, edible veg oil, invert syrup, raising agents, emulsifiers, added vitamins & minerals","Clean","Wheat, Milk, Soy",britannia.co.in,KB_HIGH,Spot-check then publish
3,Biscuits,Britannia NutriChoice Digestive,Britannia,IN_DB_GAP,8901063093478,"Whole wheat flour (71%), sugar, edible veg oil, raising agents, emulsifiers, salt","Clean","Wheat, Milk",britannia.co.in,KB_HIGH,Spot-check then publish
4,Biscuits,Parle Monaco Classic,Parle,IN_DB_GAP,8901719123788,"Refined wheat flour, sugar, edible veg oil, invert syrup, salt, raising agents, emulsifiers","Clean","Wheat",parleproducts.com,KB_HIGH,Spot-check then publish
5,Biscuits,Parle Hide & Seek Choco Delight,Parle,IN_DB_GAP,8901719136801,"Refined wheat flour, sugar, edible veg oil, cocoa solids, invert syrup, raising agents, emulsifiers","Clean","Wheat, Milk, Soy",parleproducts.com,KB_HIGH,Spot-check then publish
6,Biscuits,Parle Fab! Jam,Parle,IN_DB_GAP,8901719114038,"Refined wheat flour, sugar, fruit jam, edible veg oil, invert syrup, raising agents, colours","Verify fruit jam colours","Wheat",parleproducts.com,KB_MEDIUM,Verify pack
7,Biscuits,Parle Krackjack,Parle,IN_DB_GAP,8901719135217,"Refined wheat flour, sugar, edible veg oil, invert syrup, salt, raising agents, emulsifiers","Clean","Wheat",parleproducts.com,KB_HIGH,Spot-check then publish
8,Biscuits,Sunfeast Dark Fantasy Original,ITC,IN_DB_GAP,8901725015916,"Refined wheat flour, sugar, refined palm oil, cocoa solids, invert syrup, raising agents, emulsifiers","Clean","Wheat, Milk, Soy",itcportal.com,KB_HIGH,Spot-check then publish
9,Biscuits,Sunfeast Mom's Magic Cashew,ITC,IN_DB_GAP,8901725017620,"Refined wheat flour, sugar, edible veg oil, cashew nuts, invert syrup, raising agents","Clean","Wheat, Milk, Cashew",itcportal.com,KB_HIGH,Spot-check then publish
10,Biscuits,Oreo Vanilla Creme (India),Mondelez,IN_DB_GAP,8901233031644,"Refined wheat flour, sugar, refined palm oil, cocoa solids, invert syrup, raising agents, emulsifiers, antioxidants (INS 319)","INS 319 TBHQ - Japan restricted","Wheat, Milk, Soy",mondelezindia.com,KB_HIGH,Spot-check then publish
11,Biscuits,Britannia Treat Cake Pineapple,Britannia,IN_DB_GAP,8901063362734,"Refined wheat flour, sugar, edible veg oil, eggs, pineapple pulp, raising agents, preservatives (INS 202), colours","INS 202 Preservative","Wheat, Egg, Milk",britannia.co.in,KB_MEDIUM,Verify pack
12,Biscuits,Unibic Cashew Cookies,Unibic,IN_DB_GAP,8906009071626,"Refined wheat flour, sugar, butter, cashew nuts, invert syrup, raising agents, salt","Clean","Wheat, Milk, Cashew",unibic.com,KB_HIGH,Spot-check then publish
13,Biscuits,McVitie's Digestive,McVitie's,IN_DB_GAP,8906033743346,"Whole wheat flour, sugar, edible veg oil, raising agents, salt, emulsifiers","Clean","Wheat, Milk",mcvitiesindia.com,KB_HIGH,Spot-check then publish
14,Biscuits,Bisk Farm Bourbon,Bisk Farm,IN_DB_GAP,8901928112009,"Refined wheat flour, sugar, edible veg oil, cocoa solids, raising agents, emulsifiers, colours","Clean","Wheat, Milk, Soy",biskfarm.com,KB_MEDIUM,Verify pack
15,Biscuits,Britannia 50-50 Maska Chaska,Britannia,IN_DB_GAP,8901063017399,"Refined wheat flour, sugar, edible veg oil, salt, raising agents, emulsifiers, flavours","Clean","Wheat, Milk",britannia.co.in,KB_HIGH,Spot-check then publish
16,Chocolate,Cadbury 5 Star,Mondelez,TO_SCAN,8901233022574,"Sugar, liquid glucose, milk solids, hydrogenated veg oil, cocoa solids, emulsifiers, colours (INS 150d)","INS 150d Caramel","Milk, Soy",mondelezindia.com,SCAN_REQUIRED,Retail scan
17,Chocolate,Cadbury Perk,Mondelez,TO_SCAN,8901233022575,"Sugar, milk solids, cocoa solids, edible veg oil, emulsifiers, flavours","Clean","Milk, Soy",mondelezindia.com,SCAN_REQUIRED,Retail scan
18,Chocolate,Nestlé Munch,Nestlé,TO_SCAN,8901058008463,"Sugar, milk solids, hydrogenated veg oil, cocoa solids, wheat flour, emulsifiers","Hydrogenated oil","Wheat, Milk, Soy",nestle.in,SCAN_REQUIRED,Retail scan
19,Chocolate,Nestlé KitKat Standard,Nestlé,IN_DB_GAP,8901058852165,"Sugar, refined wheat flour, milk solids, hydrogenated veg oil, cocoa solids, emulsifiers, yeast","Hydrogenated oil","Wheat, Milk, Soy",nestle.in,KB_HIGH,Spot-check then publish
20,Chocolate,Cadbury Gems,Mondelez,TO_SCAN,8901233022576,"Sugar, milk solids, cocoa solids, edible veg oil, emulsifiers, colours (INS 102, 110, 122, 133)","INS 102/110/122/133 (Southampton Six)","Milk, Soy, Wheat",mondelezindia.com,SCAN_REQUIRED,Retail scan
21,Chocolate,Cadbury Eclairs,Mondelez,TO_SCAN,8901233022577,"Sugar, liquid glucose, milk solids, hydrogenated veg oil, cocoa solids, emulsifiers","Hydrogenated oil","Milk, Soy",mondelezindia.com,SCAN_REQUIRED,Retail scan
22,Candy,Parle Mango Bite,Parle,IN_DB_GAP,8901719127762,"Sugar, liquid glucose, mango pulp, acidity regulators, colours, flavours","Verify colours","None",parleproducts.com,KB_HIGH,Spot-check then publish
23,Candy,Parle Kaccha Mango Bite,Parle,TO_SCAN,8901719127763,"Sugar, liquid glucose, raw mango powder, salt, acidity regulators, spices, colours","Verify colours","None",parleproducts.com,SCAN_REQUIRED,Retail scan
24,Candy,Parle Melody,Parle,TO_SCAN,8901719127764,"Sugar, liquid glucose, milk solids, hydrogenated veg oil, cocoa solids, emulsifiers","Hydrogenated oil","Milk",parleproducts.com,SCAN_REQUIRED,Retail scan
25,Candy,Parle Alpenliebe,Parle,IN_DB_GAP,8901393017908,"Sugar, liquid glucose, butter, milk solids, acidity regulators, flavours","Clean","Milk",parleproducts.com,KB_MEDIUM,Verify pack
26,Candy,Parle Pulse Orange,Parle,TO_SCAN,8901719127765,"Sugar, liquid glucose, orange juice concentrate, acidity regulators, salt, colours","Verify colours","None",parleproducts.com,SCAN_REQUIRED,Retail scan
27,Candy,DS Group Pulse,DS Group,TO_SCAN,8901138819965,"Sugar, liquid glucose, tamarind, salt, spices, acidity regulators, colours","Verify colours","None",dsgroup.com,SCAN_REQUIRED,Retail scan
28,Candy,Perfetti Mentos,Perfetti,IN_DB_GAP,8901393026146,"Sugar, liquid glucose, hydrogenated veg oil, gelatin, flavours, colours","Hydrogenated oil","None",perfettivanmelle.in,KB_MEDIUM,Verify pack
29,Chocolate,Ferrero Rocher 3-Pack,Ferrero,IN_DB_GAP,8000500360606,"Milk chocolate, hazelnuts, sugar, palm oil, wheat flour, cocoa butter, emulsifiers","Clean","Milk, Hazelnut, Wheat, Soy",ferrero.in,KB_HIGH,Spot-check then publish
30,Spread,Nutella India Jar,Ferrero,IN_DB_GAP,8901058852166,"Sugar, palm oil, hazelnuts, skimmed milk powder, cocoa solids, emulsifiers, vanillin","Clean","Milk, Hazelnut, Soy",ferrero.in,KB_HIGH,Spot-check then publish
31,Snack,Kurkure Masala Munch,PepsiCo,TO_SCAN,8901491001138,"Corn grits, edible veg oil, rice grits, gram flour, spices, salt, flavour enhancers (INS 621), colours (INS 160c)","INS 621 MSG, INS 160c","May contain milk",pepsicoindia.com,SCAN_REQUIRED,Retail scan
32,Snack,Kurkure Green Chutney,PepsiCo,TO_SCAN,8901491001139,"Corn grits, edible veg oil, rice grits, gram flour, spices, salt, flavour enhancers (INS 621), colours","INS 621 MSG","May contain milk",pepsicoindia.com,SCAN_REQUIRED,Retail scan
33,Snack,Uncle Chipps Spicy Treat,PepsiCo,TO_SCAN,8901491001140,"Potato, edible veg oil, spices, salt, sugar, flavour enhancers (INS 621), acidity regulators","INS 621 MSG","None",pepsicoindia.com,SCAN_REQUIRED,Retail scan
34,Snack,Lay's Cream & Onion,PepsiCo,IN_DB_GAP,8901491001141,"Potato, edible veg oil, sugar, salt, onion powder, milk solids, flavour enhancers (INS 621, 627, 631)","INS 621 MSG","Milk",pepsicoindia.com,KB_HIGH,Spot-check then publish
35,Snack,Lay's West Indies Hot n Sweet,PepsiCo,IN_DB_GAP,8901491001142,"Potato, edible veg oil, sugar, spices, salt, garlic powder, acidity regulators, colours","Clean","None",pepsicoindia.com,KB_MEDIUM,Verify pack
36,Snack,Bingo Mad Angles Achaari,ITC,IN_DB_GAP,8901725013714,"Corn grits, edible veg oil, wheat flour, spices, salt, sugar, flavour enhancers (INS 621), acidity regulators","INS 621 MSG","Wheat",itcportal.com,KB_HIGH,Spot-check then publish
37,Snack,Bingo Yumitos,ITC,TO_SCAN,8901725013715,"Potato, edible veg oil, spices, salt, sugar, flavour enhancers, colours","Verify colours","None",itcportal.com,SCAN_REQUIRED,Retail scan
38,Snack,Haldiram's Soya Sticks,Haldiram's,IN_DB_GAP,8904063254697,"Edible veg oil, tapioca starch, black gram flour, soya powder, rice flour, spices, salt, raising agents","Clean","Soy",haldirams.com,KB_HIGH,Spot-check then publish
39,Snack,Haldiram's All In One,Haldiram's,IN_DB_GAP,8904063214942,"Edible veg oil, rice flakes, gram flour, peanuts, sago, spices, salt, raising agents","Clean","Peanut, Gram",haldirams.com,KB_HIGH,Spot-check then publish
40,Snack,Balaji Wafers Salted,Balaji,IN_DB_GAP,8906010500344,"Potato, edible veg oil, salt","Clean","None",balajiwafers.com,KB_HIGH,Spot-check then publish
41,Snack,Balaji Chataka Pataka,Balaji,IN_DB_GAP,8906010500511,"Potato, edible veg oil, spices, salt, sugar, acidity regulators, colours","Verify colours","None",balajiwafers.com,KB_MEDIUM,Verify pack
42,Snack,Too Yumm Chilli Achari,RPSG,IN_DB_GAP,8906090571258,"Multigrain blend, edible veg oil, spices, salt, sugar, acidity regulators, flavours","Clean","Wheat, Oats",tooyumm.com,KB_HIGH,Spot-check then publish
43,Snack,ACT II Classic Salted,Agro Tech,IN_DB_GAP,8901512540102,"Popcorn kernels, edible veg oil, salt","Clean","None",act2popcorn.in,KB_HIGH,Spot-check then publish
44,Snack,ACT II Butter Delite,Agro Tech,IN_DB_GAP,8901512541901,"Popcorn kernels, edible veg oil, salt, butter flavour, colour (INS 160a)","INS 160a","Milk (flavour)",act2popcorn.in,KB_HIGH,Spot-check then publish
45,Snack,Doritos Sweet Chilli (India),PepsiCo,IN_DB_GAP,8901491100052,"Corn, edible veg oil, sugar, salt, spices, garlic powder, acidity regulators, colours","Verify colours","None",pepsicoindia.com,KB_MEDIUM,Verify pack
46,Beverage,Coca-Cola Original,Coca-Cola,TO_SCAN,8901764012600,"Carbonated water, sugar, acidity regulator (INS 338), colour (INS 150d), natural flavours, caffeine","INS 150d, INS 338","None",coca-cola.com/in,SCAN_REQUIRED,Retail scan
47,Beverage,Sprite,Coca-Cola,TO_SCAN,8901764032967,"Carbonated water, sugar, acidity regulators (INS 330, 331), natural flavours","Clean","None",coca-cola.com/in,SCAN_REQUIRED,Retail scan
48,Beverage,Maaza Mango,Coca-Cola,TO_SCAN,8901764012601,"Water, sugar, mango pulp, acidity regulators, antioxidants, colours (INS 150a)","INS 150a","None",coca-cola.com/in,SCAN_REQUIRED,Retail scan
49,Beverage,Fanta Orange,Coca-Cola,TO_SCAN,8901764012602,"Carbonated water, sugar, orange juice concentrate, acidity regulators, antioxidants, colours (INS 110)","INS 110 Sunset Yellow","None",coca-cola.com/in,SCAN_REQUIRED,Retail scan
50,Beverage,Mountain Dew,PepsiCo,TO_SCAN,8901491001143,"Carbonated water, sugar, acidity regulators, caffeine, natural flavours, colours (INS 102, 133)","INS 102/133","None",pepsicoindia.com,SCAN_REQUIRED,Retail scan
51,Beverage,7UP,PepsiCo,IN_DB_GAP,8902080002290,"Carbonated water, acidity regulators, flavours, sweeteners, preservatives","Clean","None",pepsicoindia.com,KB_HIGH,Spot-check then publish
52,Beverage,Mirinda,PepsiCo,TO_SCAN,8901491001144,"Carbonated water, sugar, acidity regulators, orange juice concentrate, colours (INS 110, 102)","INS 110/102","None",pepsicoindia.com,SCAN_REQUIRED,Retail scan
53,Beverage,Sting Energy Classic,PepsiCo,IN_DB_GAP,8902080100637,"Carbonated water, sugar, acidity regulators, caffeine, taurine, colours (INS 110, 102), vitamins","INS 110/102","None",pepsicoindia.com,KB_HIGH,Spot-check then publish
54,Beverage,Paper Boat Aamras,Hector Beverages,IN_DB_GAP,8906080600913,"Water, mango pulp, sugar, acidity regulators, antioxidants","Clean","None",paperboat.com,KB_HIGH,Spot-check then publish
55,Beverage,Paper Boat Jaljeera,Hector Beverages,IN_DB_GAP,8906080600914,"Water, sugar, spices, salt, acidity regulators, mint extract","Clean","None",paperboat.com,KB_HIGH,Spot-check then publish
56,Beverage,B Natural Mixed Fruit,ITC,TO_SCAN,8901725013716,"Water, mixed fruit juice concentrate, sugar, acidity regulators, antioxidants, vitamins","Clean","None",itcportal.com,SCAN_REQUIRED,Retail scan
57,Beverage,Real Fruit Power Mango,Dabur,TO_SCAN,8901888002563,"Water, mango pulp, sugar, acidity regulators, antioxidants","Clean","None",dabur.com,SCAN_REQUIRED,Retail scan
58,Beverage,Real Fruit Power Orange,Dabur,TO_SCAN,8901888002564,"Water, orange juice concentrate, sugar, acidity regulators, antioxidants","Clean","None",dabur.com,SCAN_REQUIRED,Retail scan
59,Beverage,Tropicana 100% Orange,PepsiCo,TO_SCAN,8901491702539,"100% orange juice","Clean","None",pepsicoindia.com,SCAN_REQUIRED,Retail scan
60,Beverage,Rooh Afza,Hamdard,TO_SCAN,8901044250197,"Sugar, water, herb extracts, fruit extracts, colours (INS 122, 124), flavours","INS 122/124 (Red dyes)","None",hamdard.in,SCAN_REQUIRED,Retail scan
61,Dairy,Amul Butter,GCMMF,TO_SCAN,8901262030145,"Pasteurized cream, salt, annatto colour (INS 160b)","INS 160b","Milk",amul.com,SCAN_REQUIRED,Retail scan
62,Dairy,Amul Gold Milk (UHT),GCMMF,TO_SCAN,8901262153578,"Standardized milk (4.5% fat, 8.5% SNF), vitamins A & D","Clean","Milk",amul.com,SCAN_REQUIRED,Retail scan
63,Dairy,Amul Kool Elaichi,GCMMF,TO_SCAN,8901262153579,"Toned milk, sugar, elaichi flavour, stabilizers","Clean","Milk",amul.com,SCAN_REQUIRED,Retail scan
64,Dairy,Amul Vanilla Ice Cream,GCMMF,TO_SCAN,8901262153580,"Milk solids, sugar, edible veg oil, emulsifiers, stabilizers, vanilla flavour","Clean","Milk, Soy",amul.com,SCAN_REQUIRED,Retail scan
65,Ice Cream,Kwality Wall's Cornetto,HUL,TO_SCAN,8901030891830,"Milk solids, sugar, edible veg oil, cocoa solids, wheat flour, emulsifiers, stabilizers, colours","Clean","Milk, Wheat, Soy",kwalitywalls.in,SCAN_REQUIRED,Retail scan
66,Ice Cream,Kwality Wall's Feast,HUL,TO_SCAN,8901030891831,"Milk solids, sugar, edible veg oil, cocoa solids, emulsifiers, stabilizers, colours","Clean","Milk, Soy",kwalitywalls.in,SCAN_REQUIRED,Retail scan
67,Dairy,Mother Dairy Classic Dahi,Mother Dairy,IN_DB_GAP,8901648018186,"Pasteurized toned milk, active lactic culture","Clean","Milk",motherdairy.com,KB_HIGH,Spot-check then publish
68,Dairy,Epigamia Greek Yogurt,Drums Food,IN_DB_GAP,8906059638510,"Pasteurized milk, active lactic culture","Clean","Milk",epigamia.in,KB_HIGH,Spot-check then publish
69,Dairy,Britannia Cheese Slices,Britannia,TO_SCAN,8901063151353,"Milk solids, salt, emulsifying salts (INS 331, 452), preservatives (INS 200)","INS 200, 331, 452","Milk",britannia.co.in,SCAN_REQUIRED,Retail scan
70,Dairy,Britannia Cheese Cubes,Britannia,TO_SCAN,8901063151354,"Milk solids, salt, emulsifying salts, preservatives","INS 331, 452","Milk",britannia.co.in,SCAN_REQUIRED,Retail scan
71,Dairy,Nestlé a+ Nourish,Nestlé,TO_SCAN,8901058852167,"Toned milk, vitamins A & D","Clean","Milk",nestle.in,SCAN_REQUIRED,Retail scan
72,Dairy,Nestlé Milkmaid,Nestlé,IN_DB_GAP,8901058890310,"Milk solids, sugar","Clean","Milk",nestle.in,KB_HIGH,Spot-check then publish
73,Dairy,Go Cheese Slices,Parag Milk,TO_SCAN,8904083305072,"Milk solids, salt, emulsifying salts, preservatives","INS 331, 452","Milk",gocheese.in,SCAN_REQUIRED,Retail scan
74,Dairy,Verka Ghee,Verka,IN_DB_GAP,8901826306005,"Pure cow ghee","Clean","Milk",verka.coop,KB_HIGH,Spot-check then publish
75,Dairy,Nandini Goodlife Skimmed,Nandini,TO_SCAN,8901648095163,"Skimmed milk, vitamins A & D","Clean","Milk",nandini.coop,SCAN_REQUIRED,Retail scan
76,Noodles,Maggi Oats Masala,Nestlé,IN_DB_GAP,8901058854107,"Oats flour, wheat flour, palm oil, salt, tastemaker (spices, salt, INS 319)","INS 319 TBHQ","Wheat, Gluten, Oats",nestle.in,KB_HIGH,Spot-check then publish
77,Noodles,Maggi Special Masala,Nestlé,IN_DB_GAP,8901058901580,"Wheat flour, palm oil, salt, tastemaker (spices, salt, INS 319)","INS 319 TBHQ","Wheat, Gluten",nestle.in,KB_HIGH,Spot-check then publish
78,Pasta,Sunfeast YiPPee! Pazzta,ITC,IN_DB_GAP,8901725015886,"Wheat flour, edible veg oil, salt, tastemaker (spices, milk solids, INS 621)","INS 621 MSG","Wheat, Milk",itcportal.com,KB_HIGH,Spot-check then publish
79,Soup,Knorr Thick Tomato,HUL,TO_SCAN,8901030825546,"Tomato powder, sugar, salt, corn starch, spices, flavour enhancers (INS 621)","INS 621 MSG","May contain milk",hul.co.in,SCAN_REQUIRED,Retail scan
80,Soup,Knorr Sweet Corn Veg,HUL,TO_SCAN,8901030825547,"Sweet corn, salt, corn starch, sugar, spices, flavour enhancers (INS 621)","INS 621 MSG","May contain milk",hul.co.in,SCAN_REQUIRED,Retail scan
81,Noodles,Ching's Schezwan Instant,Capital Foods,IN_DB_GAP,8901595853861,"Wheat flour, palm oil, salt, tastemaker (spices, INS 621, colours)","INS 621 MSG","Wheat",chingssecret.com,KB_HIGH,Spot-check then publish
82,Noodles,Wai Wai X-Press Masala,Wai Wai,IN_DB_GAP,8906013030947,"Wheat flour, palm oil, salt, tastemaker (spices, INS 621, colours)","INS 621 MSG","Wheat",waiwai.co.in,KB_HIGH,Spot-check then publish
83,Noodles,Nissin Cup Noodles Spicy,Nissin,TO_SCAN,8901014004843,"Wheat flour, palm oil, salt, tastemaker (spices, INS 621, colours)","INS 621 MSG","Wheat, Soy",nissinfoods.in,SCAN_REQUIRED,Retail scan
84,Pasta,Bambino Macaroni,Bambino,IN_DB_GAP,8901242203209,"Durum wheat semolina","Clean","Wheat, Gluten",bambinofoods.com,KB_HIGH,Spot-check then publish
85,Pasta,Weikfield Penne,Dr. Oetker,TO_SCAN,8906002000883,"Durum wheat semolina","Clean","Wheat, Gluten",droetker.in,SCAN_REQUIRED,Retail scan
86,Condiment,Veeba Eggless Mayo,Veeba,IN_DB_GAP,8906069400527,"Edible veg oil, water, sugar, vinegar, salt, thickener (INS 1422), preservative (INS 211), mustard","INS 211 Preservative","Soy, Mustard",veeba.in,KB_HIGH,Spot-check then publish
87,Condiment,Del Monte Ketchup,Del Monte,TO_SCAN,8904082761007,"Tomato paste, sugar, salt, spices, acidity regulator (INS 260), preservative (INS 211)","INS 211 Preservative","None",delmonte.in,SCAN_REQUIRED,Retail scan
88,Condiment,Ching's Dark Soya,Capital Foods,IN_DB_GAP,8901595853862,"Water, soybean extract, salt, sugar, colour (INS 150c), preservative (INS 211)","INS 150c, 211","Soy",chingssecret.com,KB_HIGH,Spot-check then publish
89,Condiment,Ching's Red Chilli,Capital Foods,IN_DB_GAP,8901595853863,"Water, red chilli, garlic, salt, sugar, acidity regulator (INS 260), preservative (INS 211)","INS 211 Preservative","None",chingssecret.com,KB_HIGH,Spot-check then publish
90,Masala,Everest Garam Masala,Everest,TO_SCAN,8906015340174,"Coriander, cumin, black pepper, cloves, cinnamon, cardamom, bay leaf","Clean","None",everestmasala.com,SCAN_REQUIRED,Retail scan
91,Masala,Everest Chicken Masala,Everest,IN_DB_GAP,8901786165001,"Coriander, cumin, turmeric, black pepper, red chilli, cloves, cinnamon, cardamom","Clean","None",everestmasala.com,KB_HIGH,Spot-check then publish
92,Masala,MDH Chunky Chat,MDH,TO_SCAN,8901192205261,"Cumin, black salt, mango powder, red chilli, black pepper, salt, ginger","Clean","None",mdhmasala.com,SCAN_REQUIRED,Retail scan
93,Masala,MDH Kitchen King,MDH,TO_SCAN,8901192205262,"Coriander, turmeric, red chilli, cumin, black pepper, cloves, cinnamon","Clean","None",mdhmasala.com,SCAN_REQUIRED,Retail scan
94,Masala,Catch Black Pepper,Catch,IN_DB_GAP,8901192103116,"100% black pepper","Clean","None",catch.co.in,KB_HIGH,Spot-check then publish
95,Masala,Catch Jeera Powder,Catch,IN_DB_GAP,8901192103117,"100% cumin","Clean","None",catch.co.in,KB_HIGH,Spot-check then publish
96,Cereal,Kellogg's Chocos,Moon & Stars,Kellogg's,TO_SCAN,8901499009043,"Wheat flour, sugar, cocoa solids, malt extract, salt, vitamins, minerals","Clean","Wheat, Gluten, Barley",kelloggsindia.com,SCAN_REQUIRED,Retail scan
97,Cereal,Kellogg's Corn Flakes,Kellogg's,TO_SCAN,8901499009044,"Corn grits, sugar, malt extract, salt, vitamins, minerals","Clean","Barley malt (gluten)",kelloggsindia.com,SCAN_REQUIRED,Retail scan
98,Breakfast,Slurrp Farm Millet Pancake,Slurrp Farm,IN_DB_GAP,8908006217113,"Ragi flour, oats flour, whole wheat flour, sugar, baking powder, salt","Clean","Wheat, Gluten, Oats",slurrpfarm.com,KB_HIGH,Spot-check then publish
99,Staple,Tata Salt Iodised,Tata Consumer,TO_SCAN,8901052003839,"Vacuum evaporated iodised salt, anticaking agent (INS 536)","INS 536","None",tatasalt.in,SCAN_REQUIRED,Retail scan
100,Health Drink,Glucon-D Tangy Orange,GSK/HUL,TO_SCAN,8901542006227,"Dextrose monohydrate, vitamin C, acidity regulators, colours (INS 102, 110), flavours","INS 102/110","None",glucond.in,SCAN_REQUIRED,Retail scan"""

# Read both blocks into dataframes
df1 = pd.read_csv(io.StringIO(csv_block_1), dtype=str)
df2 = pd.read_csv(io.StringIO(csv_block_2), dtype=str)

df_all = pd.concat([df1, df2], ignore_index=True)

# Clean fields
df_all['barcode'] = df_all['barcode'].str.strip()
df_all['product_name'] = df_all['product_name'].str.strip()
df_all['brand'] = df_all['brand'].str.strip()
df_all['ingredients_text'] = df_all['ingredients_text'].str.strip()
df_all['confidence'] = df_all['confidence'].str.strip().str.upper()

# Filter out rows with no barcode
df_all = df_all[df_all['barcode'].notna() & (df_all['barcode'] != '')]

# Remove duplicates inside df_all (keep first)
df_all = df_all.drop_duplicates(subset=['barcode'], keep='first')

print(f"Total new rows with valid barcodes to merge: {len(df_all)}")

added_to_confirmed = 0
added_to_needs_ver = 0
updated_confirmed = 0
updated_needs_ver = 0
deleted_from_nv_moved_to_c = 0

new_c_rows = []
new_nv_rows = []

# Process each new product
for _, row in df_all.iterrows():
    bc = row['barcode']
    p_name = row['product_name']
    brand = row['brand']
    ing = row['ingredients_text']
    conf = row['confidence']
    
    # Check if ingredients is empty/pending
    is_ing_empty = not ing or str(ing).strip().lower() in ['nan', 'none', '', 'pending capture']
    
    # Determine destination table rules:
    # We publish to confirmed if: confidence is KB_HIGH AND ingredients are not empty.
    # Otherwise, it goes to needs verification.
    is_kb_high = conf == 'KB_HIGH'
    
    dest_confirmed = is_kb_high and not is_ing_empty
    
    # Prepare row data dictionary aligned with the destination columns:
    # ['barcode', 'product_name', 'brands', 'ingredients_text', 'sold_in_india_status', 'ingredient_confidence', 'status', 'data_source', 'source_license', 'collection_method']
    
    if dest_confirmed:
        new_row = {
            'barcode': bc,
            'product_name': p_name,
            'brands': brand,
            'ingredients_text': ing,
            'sold_in_india_status': 'CONFIRMED_INDIA_890',
            'ingredient_confidence': 'HIGH',
            'status': 'KEEP',
            'data_source': 'Brand Official Publication',
            'source_license': 'User-submitted',
            'collection_method': 'OCR'
        }
    else:
        new_row = {
            'barcode': bc,
            'product_name': p_name,
            'brands': brand,
            'ingredients_text': ing if not is_ing_empty else '',
            'sold_in_india_status': 'NEEDS_VERIFICATION',
            'ingredient_confidence': 'INCOMPLETE',
            'status': 'FIX',
            'data_source': 'Barcode Registry (No Ingredient Text)' if is_ing_empty else 'Raw OCR Scrape (Needs QA)',
            'source_license': 'Pending Attribution',
            'collection_method': 'Barcode Scan'
        }
        
    # Check if already in confirmed
    if bc in c_barcodes:
        # Update details in confirmed (update ingredients if empty, overwrite product details)
        idx = df_c[df_c['barcode'] == bc].index[0]
        # Only overwrite if new details are useful
        df_c.at[idx, 'product_name'] = p_name
        df_c.at[idx, 'brands'] = brand
        if not is_ing_empty:
            df_c.at[idx, 'ingredients_text'] = ing
            df_c.at[idx, 'ingredient_confidence'] = 'HIGH'
        updated_confirmed += 1
    # Check if in needs verification
    elif bc in nv_barcodes:
        if dest_confirmed:
            # Delete from needs verification
            df_nv = df_nv[df_nv['barcode'] != bc]
            nv_barcodes.remove(bc)
            deleted_from_nv_moved_to_c += 1
            
            # Append to confirmed list
            new_c_rows.append(new_row)
            c_barcodes.add(bc)
            added_to_confirmed += 1
        else:
            # Just update in needs verification
            idx = df_nv[df_nv['barcode'] == bc].index[0]
            df_nv.at[idx, 'product_name'] = p_name
            df_nv.at[idx, 'brands'] = brand
            if not is_ing_empty:
                df_nv.at[idx, 'ingredients_text'] = ing
                df_nv.at[idx, 'data_source'] = 'Raw OCR Scrape (Needs QA)'
            updated_needs_ver += 1
    # Brand new barcode
    else:
        if dest_confirmed:
            new_c_rows.append(new_row)
            c_barcodes.add(bc)
            added_to_confirmed += 1
        else:
            new_nv_rows.append(new_row)
            nv_barcodes.add(bc)
            added_to_needs_ver += 1

# Append new dataframes if not empty
if new_c_rows:
    df_new_c = pd.DataFrame(new_c_rows)
    df_c = pd.concat([df_c, df_new_c], ignore_index=True)
    
if new_nv_rows:
    df_new_nv = pd.DataFrame(new_nv_rows)
    df_nv = pd.concat([df_nv, df_new_nv], ignore_index=True)

# Remove any possible duplicates
df_c = df_c.drop_duplicates(subset=['barcode'], keep='first')
df_nv = df_nv.drop_duplicates(subset=['barcode'], keep='first')

# Make sure all Needs Verification columns are clean
df_nv['ingredients_text'] = df_nv['ingredients_text'].fillna('')

# Save datasets back
df_c.to_csv(confirmed_path, index=False)
df_nv.to_csv(needs_ver_path, index=False)

print(f"=== UPDATE SUMMARY ===")
print(f"Original Confirmed Rows: {orig_c_count} | New Count: {len(df_c)}")
print(f"Original Needs Verification Rows: {orig_nv_count} | New Count: {len(df_nv)}")
print(f"Added to Confirmed: {added_to_confirmed} (of which {deleted_from_nv_moved_to_c} were elevated from Needs Verification)")
print(f"Added to Needs Verification: {added_to_needs_ver}")
print(f"Updated in Confirmed: {updated_confirmed}")
print(f"Updated in Needs Verification: {updated_needs_ver}")
