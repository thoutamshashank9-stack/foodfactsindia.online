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

# 2. BATCH 7 DATA
batch7_raw = [
    # Nestle India
    {"barcode": "8901058018493", "product_name": "Maggi 2-Minute Noodles Masala", "brands": "Nestle", "ingredients_text": "Noodles: Refined wheat flour (maida), palm oil, iodized salt, wheat gluten, thickeners (INS 508, INS 412), acidity regulators (INS 501(i), INS 500(i)); Tastemaker: salt, onion, sugar, coriander, chilli, turmeric, garlic, cumin, fenugreek, antioxidant (INS 319)"},
    {"barcode": "8901058000221", "product_name": "Maggi 2 Minute Noodles", "brands": "Nestle", "ingredients_text": "Noodles: Refined wheat flour (maida), palm oil, iodized salt, wheat gluten, thickeners (INS 508, INS 412), acidity regulators (INS 501(i), INS 500(i)); Tastemaker: salt, onion, sugar, coriander, chilli, turmeric, garlic, cumin, fenugreek, antioxidant (INS 319), flavour enhancers (INS 621)"},
    {"barcode": "8901058901580", "product_name": "Maggi Special Masala Noodles", "brands": "Nestle", "ingredients_text": "Noodles: Refined wheat flour, palm oil, salt, wheat gluten, thickeners, acidity regulators; Tastemaker: salt, spices, sugar, flavour enhancers (INS 621), antioxidant (INS 319)"},
    {"barcode": "8901058854107", "product_name": "Maggi Oats Masala Noodles", "brands": "Nestle", "ingredients_text": "Oats flour, refined wheat flour, palm oil, salt, thickeners, acidity regulators; Tastemaker: salt, spices, sugar, flavour enhancers (INS 621), antioxidant (INS 319)"},
    {"barcode": "8901058009699", "product_name": "Maggi Atta Noodles", "brands": "Nestle", "ingredients_text": "Whole wheat flour (atta), palm oil, salt, wheat gluten, thickeners, acidity regulators; Tastemaker: salt, spices, flavour enhancers (INS 621), antioxidant (INS 319)"},
    {"barcode": "8901058006643", "product_name": "Maggi 2 Minutes Noodles Masala", "brands": "Nestle", "ingredients_text": "Noodles: Refined wheat flour (maida), palm oil, iodized salt, wheat gluten, thickeners (INS 508, INS 412), acidity regulators (INS 501(i), INS 500(i)); Tastemaker: salt, onion, sugar, coriander, chilli, turmeric, garlic, cumin, fenugreek, antioxidant (INS 319)"},
    {"barcode": "8901058002270", "product_name": "Maggi Spicy Garlic Noodles", "brands": "Nestle", "ingredients_text": "Noodles: Refined wheat flour, palm oil, salt, thickeners; Tastemaker: salt, garlic, chilli, spices, flavour enhancers (INS 621), antioxidant (INS 319)"},
    {"barcode": "8901058013665", "product_name": "Maggi Hot and Sweet Noodles", "brands": "Nestle", "ingredients_text": "Noodles: Refined wheat flour, palm oil, salt, thickeners; Tastemaker: salt, sugar, chilli, garlic, flavour enhancers (INS 621), antioxidant (INS 319)"},
    {"barcode": "8901058866711", "product_name": "Maggi Veg Atta Noodles 290g", "brands": "Nestle", "ingredients_text": "Whole wheat flour, palm oil, salt, thickeners; Tastemaker: salt, spices, flavour enhancers (INS 621), antioxidant (INS 319)"},
    {"barcode": "8901058016116", "product_name": "KitKat 50", "brands": "Nestle", "ingredients_text": "Refined wheat flour, sugar, cocoa butter, milk solids, cocoa mass, emulsifier (INS 322), yeast, salt, raising agent (INS 500(ii)), flavouring"},
    {"barcode": "8901058023558", "product_name": "KitKat Dark Chocolate Minis", "brands": "Nestle", "ingredients_text": "Refined wheat flour, sugar, cocoa butter, cocoa solids, milk solids, emulsifier (INS 322), yeast, salt, raising agent (INS 500(ii)), flavouring"},
    {"barcode": "8901058905472", "product_name": "Kit Kat", "brands": "Nestle", "ingredients_text": "Refined wheat flour, sugar, cocoa butter, milk solids, cocoa mass, emulsifier (INS 322), yeast, salt, raising agent (INS 500(ii)), flavouring"},
    {"barcode": "8901058852141", "product_name": "KitKat Caramel Chocolate Coated Wafer", "brands": "Nestle", "ingredients_text": "Refined wheat flour, sugar, cocoa butter, milk solids, glucose syrup, emulsifier (INS 322), yeast, salt, raising agent, flavouring"},
    {"barcode": "8901058010701", "product_name": "Nestlé Munch Vanilla Flavour", "brands": "Nestle", "ingredients_text": "Sugar, refined wheat flour, hydrogenated vegetable oil (palm), milk solids, cocoa solids, emulsifier (INS 322), salt, raising agent (INS 500(ii)), artificial vanilla flavour"},
    {"barcode": "8901058900361", "product_name": "Nestlé Munch Nuts", "brands": "Nestle", "ingredients_text": "Sugar, refined wheat flour, hydrogenated vegetable oil (palm), peanuts, milk solids, cocoa solids, emulsifier (INS 322), salt, raising agent"},
    {"barcode": "8901058875577", "product_name": "Milkybar", "brands": "Nestle", "ingredients_text": "Sugar, milk solids, cocoa butter, emulsifier (INS 322), artificial vanilla flavour"},
    {"barcode": "8901058016055", "product_name": "Nescafé Classic", "brands": "Nestle", "ingredients_text": "100% instant coffee"},
    {"barcode": "8901058865660", "product_name": "Nescafé Gold Cappuccino", "brands": "Nestle", "ingredients_text": "Instant coffee, sugar, milk solids, glucose syrup, hydrogenated vegetable oil (palm kernel), salt, stabilizers (INS 340(ii), INS 452(i)), emulsifier (INS 471), anticaking agent (INS 551)"},
    {"barcode": "8901058011401", "product_name": "Nescafé Ice Roast", "brands": "Nestle", "ingredients_text": "Coffee beans (100% instant coffee)"},
    {"barcode": "8901058014723", "product_name": "Nescafé Sunrise", "brands": "Nestle", "ingredients_text": "Coffee, chicory"},
    {"barcode": "8901058869453", "product_name": "EveryDay Dairy Whitener", "brands": "Nestle", "ingredients_text": "Milk solids, sugar, emulsifier (INS 322), stabilizers"},
    {"barcode": "8901058007060", "product_name": "Milkmaid Mini", "brands": "Nestle", "ingredients_text": "Milk solids, sugar"},
    {"barcode": "8901058897500", "product_name": "Nestlé Nan Pro 2", "brands": "Nestle", "ingredients_text": "Demineralized whey, vegetable oils, skimmed milk powder, lactose, minerals, vitamins, emulsifier"},
    {"barcode": "8901058018400", "product_name": "Nestlé Cerelac", "brands": "Nestle", "ingredients_text": "Wheat flour, sugar, milk solids, minerals, vitamins, emulsifier"},
    {"barcode": "8901058890716", "product_name": "Nestlé Optifast", "brands": "Nestle", "ingredients_text": "Milk protein, soy protein, vitamins, minerals, fibre"},
    {"barcode": "8901058004922", "product_name": "Maggi Rich Tomato Ketchup", "brands": "Nestle", "ingredients_text": "Tomato paste, sugar, water, vinegar, salt, spices, acidity regulator (INS 260), preservative (INS 211)"},
    {"barcode": "8901058868418", "product_name": "Maggi Rich Tomato Ketchup", "brands": "Nestle", "ingredients_text": "Tomato paste, sugar, water, vinegar, salt, spices, acidity regulator (INS 260), preservative (INS 211)"},
    {"barcode": "8901058008388", "product_name": "Maggi Hot & Sweet Tomato Chilli Sauce", "brands": "Nestle", "ingredients_text": "Tomato paste, sugar, water, vinegar, salt, chilli, garlic, acidity regulator (INS 260), preservative (INS 211), thickener (INS 1422)"},
    {"barcode": "8901058003055", "product_name": "Maggi Pazzta Cheese Macaroni", "brands": "Nestle", "ingredients_text": "Macaroni: Durum wheat semolina, salt; Tastemaker: milk solids, cheese powder, sugar, salt, palm oil, thickeners (INS 1422, INS 412), flavour enhancers (INS 621, INS 627, INS 631), artificial cheese flavour, colour (INS 160a)"},
    {"barcode": "8901058014846", "product_name": "Maggi Pazzta Cheesy Tomato Twist", "brands": "Nestle", "ingredients_text": "Macaroni: Durum wheat semolina, salt; Tastemaker: tomato powder, milk solids, sugar, salt, palm oil, thickeners, flavour enhancers (INS 621, INS 627, INS 631), colour (INS 160c)"},
    {"barcode": "8901058006032", "product_name": "Maggi Cup Noodles Masala", "brands": "Nestle", "ingredients_text": "Noodles: Refined wheat flour, palm oil, salt, wheat gluten, thickeners; Tastemaker: salt, spices, sugar, flavour enhancers (INS 621, INS 627, INS 631), antioxidant (INS 319)"},
    {"barcode": "8901058001167", "product_name": "Maggi Pichkoo Tomato Ketchup", "brands": "Nestle", "ingredients_text": "Tomato paste, sugar, water, vinegar, salt, spices, acidity regulator (INS 260), preservative (INS 211)"},
    {"barcode": "8901058016222", "product_name": "Maggi Rich Tomato Ketchup", "brands": "Nestle", "ingredients_text": "Tomato paste, sugar, water, vinegar, salt, spices, acidity regulator (INS 260), preservative (INS 211)"},
    {"barcode": "8901058905045", "product_name": "Soothers Herbal Throat Drops", "brands": "Nestle", "ingredients_text": "Sugar, glucose syrup, herbal extracts, vitamin C, acidity regulator"},
    {"barcode": "8901058896381", "product_name": "Nescafé Sunrise Coffee 200g", "brands": "Nestle", "ingredients_text": "Instant coffee, chicory"},

    # HUL
    {"barcode": "8901030976186", "product_name": "Horlicks", "brands": "HUL", "ingredients_text": "Malted cereals (66.7%) [barley, wheat flour, wheat, millet], milk solids (14%), sugar, wheat gluten, iodized salt, minerals, vitamins, emulsifier (INS 471)"},
    {"barcode": "8901030825668", "product_name": "Horlicks Classic Malt 500g", "brands": "HUL", "ingredients_text": "Malted cereals (66.7%) [barley, wheat flour, wheat, millet], milk solids (14%), sugar, wheat gluten, iodized salt, minerals, vitamins, emulsifier (INS 471)"},
    {"barcode": "8901030538018", "product_name": "Horlicks Classic Malt 750g", "brands": "HUL", "ingredients_text": "Malted cereals (66.7%) [barley, wheat flour, wheat, millet], milk solids (14%), sugar, wheat gluten, iodized salt, minerals, vitamins, emulsifier (INS 471)"},
    {"barcode": "8901030985973", "product_name": "Horlicks Chocolate Delight 500g", "brands": "HUL", "ingredients_text": "Malted cereals, milk solids, sugar, cocoa solids, wheat flour, minerals, vitamins, emulsifier (INS 471), artificial chocolate flavour"},
    {"barcode": "8901030825521", "product_name": "Horlicks Protein Plus Chocolate", "brands": "HUL", "ingredients_text": "Milk solids, malted cereals, sugar, cocoa solids, wheat flour, minerals, vitamins, emulsifier (INS 471)"},
    {"barcode": "8901030949654", "product_name": "Women Horlicks", "brands": "HUL", "ingredients_text": "Malted cereals, milk solids, sugar, wheat flour, minerals (Iron, Calcium), vitamins, emulsifier (INS 471)"},
    {"barcode": "8909106024502", "product_name": "Horlicks Classic Malt 1kg", "brands": "HUL", "ingredients_text": "Malted cereals (66.7%) [barley, wheat flour, wheat, millet], milk solids (14%), sugar, wheat gluten, iodized salt, minerals, vitamins, emulsifier (INS 471)"},
    {"barcode": "8909106070615", "product_name": "Horlicks Super Foods", "brands": "HUL", "ingredients_text": "Malted cereals, milk solids, sugar, wheat flour, superfoods (chia, flax), minerals, vitamins"},
    {"barcode": "8909106018372", "product_name": "Boost", "brands": "HUL", "ingredients_text": "Cereal extract (50%) [barley, wheat, millet], malted barley (21%), sugar, wheat flour, milk solids (6%), minerals, natural colour (INS 150c), vitamins"},
    {"barcode": "8901030820946", "product_name": "Boost", "brands": "HUL", "ingredients_text": "Cereal extract (50%) [barley, wheat, millet], malted barley (21%), sugar, wheat flour, milk solids (6%), minerals, natural colour (INS 150c), vitamins"},
    {"barcode": "8901030795909", "product_name": "Boost", "brands": "HUL", "ingredients_text": "Cereal extract (50%) [barley, wheat, millet], malted barley (21%), sugar, wheat flour, milk solids (6%), minerals, natural colour (INS 150c), vitamins"},
    {"barcode": "8901030882609", "product_name": "Brooke Bond Red Label 1kg", "brands": "HUL", "ingredients_text": "100% black tea (CTC dust & fannings blend)"},
    {"barcode": "8901030918810", "product_name": "Brooke Bond Taaza Tea", "brands": "HUL", "ingredients_text": "100% black tea (CTC blend)"},
    {"barcode": "8901030083037", "product_name": "Red Label Tea", "brands": "HUL", "ingredients_text": "100% black tea"},
    {"barcode": "8901030251504", "product_name": "Brooke Bond Taj Mahal Tea", "brands": "HUL", "ingredients_text": "100% black tea (CTC blend)"},
    {"barcode": "8901030624247", "product_name": "Taj Mahal Tea Bags", "brands": "HUL", "ingredients_text": "100% black tea"},
    {"barcode": "8901030681530", "product_name": "Taj Mahal Tea Bags", "brands": "HUL", "ingredients_text": "100% black tea"},
    {"barcode": "8901030681547", "product_name": "Taj Mahal Tea Bags", "brands": "HUL", "ingredients_text": "100% black tea"},
    {"barcode": "8901030373930", "product_name": "Bru Gold Instant Coffee", "brands": "HUL", "ingredients_text": "100% instant coffee (freeze-dried)"},
    {"barcode": "8909106024199", "product_name": "Bru Coffee 3rs Sachet", "brands": "HUL", "ingredients_text": "Instant coffee, sugar, milk solids, emulsifier"},
    {"barcode": "8901030831706", "product_name": "Kissan Mixed Fruit Jam", "brands": "HUL", "ingredients_text": "Sugar, mixed fruit pulp blend (approx. 46%), acidity regulator (INS 330), preservative (INS 211 sodium benzoate), permitted synthetic food colour (INS 122)"},
    {"barcode": "8901030831720", "product_name": "Kissan Mixed Fruit Jam 700g", "brands": "HUL", "ingredients_text": "Sugar, mixed fruit pulp blend (approx. 46%), acidity regulator (INS 330), preservative (INS 211 sodium benzoate), permitted synthetic food colour (INS 122)"},
    {"barcode": "8901030850400", "product_name": "Kissan Mixed Fruit Jam 500g", "brands": "HUL", "ingredients_text": "Sugar, mixed fruit pulp blend (approx. 46%), acidity regulator (INS 330), preservative (INS 211 sodium benzoate), permitted synthetic food colour (INS 122)"},
    {"barcode": "8901030931864", "product_name": "Kissan Tomato Puree", "brands": "HUL", "ingredients_text": "Tomato, salt, acidity regulator"},
    {"barcode": "8901030717376", "product_name": "Kissan Tomato Ketchup", "brands": "HUL", "ingredients_text": "Tomato paste, sugar, vinegar, salt, spices, acidity regulator (INS 260), preservative (INS 211)"},
    {"barcode": "8901030926518", "product_name": "Kissan Sweet and Spicy Ketchup", "brands": "HUL", "ingredients_text": "Tomato paste, sugar, vinegar, salt, spices, acidity regulator, preservative (INS 211)"},
    {"barcode": "8901030559266", "product_name": "Knorr Mexican Tomato Corn Soup", "brands": "HUL", "ingredients_text": "Tomato powder, corn, sugar, salt, spices, flavour enhancers (INS 621), acidity regulator, colour"},
    {"barcode": "8901030902352", "product_name": "Knorr Tomato Chatpata Soup", "brands": "HUL", "ingredients_text": "Tomato powder, sugar, salt, spices, flavour enhancers (INS 621), acidity regulator"},
    {"barcode": "8901030900297", "product_name": "Knorr Hong Kong Manchow Soup", "brands": "HUL", "ingredients_text": "Corn starch, salt, sugar, spices, flavour enhancers (INS 621), acidity regulator"},
    {"barcode": "8901030900334", "product_name": "Knorr Chicken Delite Soup", "brands": "HUL", "ingredients_text": "Corn starch, salt, sugar, chicken powder, spices, flavour enhancers (INS 621)"},

    # ITC
    {"barcode": "8901725017545", "product_name": "Sunfeast Nice", "brands": "ITC", "ingredients_text": "Refined wheat flour, sugar, coconut, edible vegetable oil (palm), invert syrup, raising agents (INS 503(ii), INS 500(ii)), salt, emulsifier (INS 322), artificial coconut flavour"},
    {"barcode": "8901725015916", "product_name": "Sunfeast Dark Fantasy Choco Fills", "brands": "ITC", "ingredients_text": "Choco crème (sugar, refined palmolein, refined palm oil, cocoa solids), refined wheat flour, sugar, invert syrup, liquid glucose, cocoa solids, milk solids, butter, raising agents, emulsifiers, salt"},
    {"barcode": "8901725136215", "product_name": "Sunfeast Dark Fantasy BIG Choco Fills", "brands": "ITC", "ingredients_text": "Choco crème (sugar, refined palmolein, refined palm oil, cocoa solids), refined wheat flour, sugar, invert syrup, liquid glucose, cocoa solids, milk solids, butter, raising agents, emulsifiers, salt"},
    {"barcode": "8901725016265", "product_name": "Sunfeast Dark Fantasy Bourbon", "brands": "ITC", "ingredients_text": "Refined wheat flour, sugar, edible vegetable oil (palm), cocoa solids, invert syrup, raising agents, emulsifiers, salt, artificial chocolate flavour"},
    {"barcode": "8901725000622", "product_name": "Sunfeast Mom's Magic Cashew Almond", "brands": "ITC", "ingredients_text": "Refined wheat flour, sugar, edible vegetable oil (palm), cashew nuts, almonds, invert syrup, milk solids, raising agents, emulsifiers"},
    {"barcode": "8901725006143", "product_name": "Sunfeast Marie Light", "brands": "ITC", "ingredients_text": "Refined wheat flour, sugar, refined palm oil, invert sugar syrup, milk solids, raising agents, salt, emulsifiers"},
    {"barcode": "8901725114916", "product_name": "Sunfeast Marie Light", "brands": "ITC", "ingredients_text": "Refined wheat flour, sugar, refined palm oil, invert sugar syrup, milk solids, raising agents, salt, emulsifiers"},
    {"barcode": "8901725013004", "product_name": "Sunfeast Marie Light Family Pack", "brands": "ITC", "ingredients_text": "Refined wheat flour, sugar, refined palm oil, invert sugar syrup, milk solids, raising agents, salt, emulsifiers"},
    {"barcode": "8901725002190", "product_name": "Sunfeast All Rounder Cream & Herb", "brands": "ITC", "ingredients_text": "Refined wheat flour, sugar, edible vegetable oil, cream powder, herbs, invert syrup, raising agents, emulsifiers, salt"},
    {"barcode": "8901725001612", "product_name": "Sunfeast All Rounder Chatpata Masala", "brands": "ITC", "ingredients_text": "Refined wheat flour, edible vegetable oil, spices, salt, sugar, raising agents, emulsifiers"},
    {"barcode": "8901725012878", "product_name": "Sunfeast Caker Swiss Roll Choco 115g", "brands": "ITC", "ingredients_text": "Refined wheat flour, sugar, eggs, edible vegetable oil, cocoa solids, glucose syrup, raising agents, emulsifiers, preservative (INS 202), flavours"},
    {"barcode": "8901725004545", "product_name": "Sunfeast Milk Shake 300ml", "brands": "ITC", "ingredients_text": "Toned milk, sugar, artificial flavour, stabilizers (INS 466, INS 407), emulsifier (INS 471)"},
    {"barcode": "8901725116149", "product_name": "Dark Fantasy Chocolate Shake", "brands": "ITC", "ingredients_text": "Toned milk, sugar, cocoa solids, artificial chocolate flavour, stabilizers, emulsifiers, colours (INS 150c)"},
    {"barcode": "8901725005993", "product_name": "Yippee Noodles Mood Masala", "brands": "ITC", "ingredients_text": "Refined wheat flour, refined palm oil, salt, wheat gluten, thickeners (INS 508, INS 412); Masala: spices, sugar, salt, flavour enhancers (INS 621, INS 627, INS 631)"},
    {"barcode": "8901725119959", "product_name": "Yippee Noodles", "brands": "ITC", "ingredients_text": "Refined wheat flour, refined palm oil, salt, wheat gluten, thickeners (INS 508, INS 412); Masala: spices, sugar, salt, flavour enhancers (INS 621, INS 627, INS 631)"},
    {"barcode": "8901725114060", "product_name": "Mini Idli Sambar", "brands": "ITC", "ingredients_text": "Rice flour, urad dal flour, salt, sambar masala (spices, tamarind, salt)"},
    {"barcode": "8901725013714", "product_name": "Bingo Mad Angles Achaari Masti", "brands": "ITC", "ingredients_text": "Corn grits, edible vegetable oil, rice grits, gram flour, spices, salt, sugar, flavour enhancers (INS 621, INS 627, INS 631), colours (INS 160c)"},
    {"barcode": "8901725004217", "product_name": "Bingo Tedhe Medhe Tomato", "brands": "ITC", "ingredients_text": "Corn grits, edible vegetable oil, rice grits, gram flour, spices, salt, sugar, tomato powder, flavour enhancers (INS 621, INS 627, INS 631), acidity regulators, colours (INS 160c)"},
    {"barcode": "8901725192341", "product_name": "Bingo Potato Chips Chilli", "brands": "ITC", "ingredients_text": "Potato, edible vegetable oil, spices, salt, sugar, flavour enhancers (INS 621), colours (INS 160c)"},
    {"barcode": "8901725001070", "product_name": "Aashirvaad Double Roasted Suji Rava", "brands": "ITC", "ingredients_text": "Semolina (double roasted)"},
    {"barcode": "8901725008888", "product_name": "Aashirvaad Shudh Chakki Atta", "brands": "ITC", "ingredients_text": "100% whole wheat flour (chakki-ground)"},
    {"barcode": "8901725008895", "product_name": "Aashirvaad Shudh Chakki Atta 10kg", "brands": "ITC", "ingredients_text": "100% whole wheat flour (chakki-ground)"},
    {"barcode": "8901725006679", "product_name": "Aashirvaad Atta with Multigrains", "brands": "ITC", "ingredients_text": "Whole wheat flour, oats, barley, millet, corn, rice flour"},
    {"barcode": "8901725100575", "product_name": "Aashirvaad Atta with Multigrains 5kg", "brands": "ITC", "ingredients_text": "Whole wheat flour, oats, barley, millet, corn, rice flour"},
    {"barcode": "8901725121747", "product_name": "Aashirvaad Superior MP Atta", "brands": "ITC", "ingredients_text": "100% whole wheat flour"},
    {"barcode": "8901725112592", "product_name": "Aashirvaad Gulab Jamun", "brands": "ITC", "ingredients_text": "Milk solids, sugar, edible vegetable oil, cardamom, rose water"},
    {"barcode": "8901725007775", "product_name": "Aashirvaad Malabar Paratha", "brands": "ITC", "ingredients_text": "Whole wheat flour, water, edible vegetable oil, salt"},
    {"barcode": "8906065166045", "product_name": "ITC Farmland Frozen Green Peas", "brands": "ITC", "ingredients_text": "Green peas"},
    {"barcode": "8906065169831", "product_name": "ITC Master Chef", "brands": "ITC", "ingredients_text": "Various ingredients based on variant"},
    {"barcode": "8901725120306", "product_name": "Sunfeast Big Vanilla Fills Biscuit", "brands": "ITC", "ingredients_text": "Refined wheat flour, sugar, edible vegetable oil, vanilla flavour, invert syrup, raising agents, emulsifiers"},

    # Britannia
    {"barcode": "8901063092709", "product_name": "Good Day Cashew", "brands": "Britannia", "ingredients_text": "Refined wheat flour, edible vegetable oil (palm), sugar, cashew nuts (4.5%), invert syrup, milk solids, butter (0.6%), raising agents, salt, emulsifier (INS 322)"},
    {"barcode": "8901063093089", "product_name": "Good Day Cashew", "brands": "Britannia", "ingredients_text": "Refined wheat flour, edible vegetable oil (palm), sugar, cashew nuts (4.5%), invert syrup, milk solids, butter (0.6%), raising agents, salt, emulsifier (INS 322)"},
    {"barcode": "8901063151307", "product_name": "Good Day Cashew Cookies", "brands": "Britannia", "ingredients_text": "Refined wheat flour, edible vegetable oil (palm), sugar, cashew nuts (4.5%), invert syrup, milk solids, butter (0.6%), raising agents, salt, emulsifier (INS 322)"},
    {"barcode": "8901063136779", "product_name": "Good Day Choco Almond", "brands": "Britannia", "ingredients_text": "Refined wheat flour, edible vegetable oil, sugar, cocoa solids, almond (3%), invert syrup, milk solids, raising agents, emulsifier"},
    {"barcode": "8901063092440", "product_name": "Good Day Butter", "brands": "Britannia", "ingredients_text": "Refined wheat flour, edible vegetable oil, sugar, butter, invert syrup, milk solids, raising agents, emulsifier, artificial butter flavour"},
    {"barcode": "8901063092792", "product_name": "Good Day Butter Jeera Biscuits", "brands": "Britannia", "ingredients_text": "Refined wheat flour, edible vegetable oil, sugar, cumin, butter, invert syrup, raising agents, emulsifier"},
    {"barcode": "8901063162303", "product_name": "Marie Gold", "brands": "Britannia", "ingredients_text": "Refined wheat flour (73%), sugar, refined palm oil, invert sugar syrup, milk solids, raising agents, salt, emulsifiers (INS 471, INS 322)"},
    {"barcode": "8901063151383", "product_name": "Marie Gold", "brands": "Britannia", "ingredients_text": "Refined wheat flour (73%), sugar, refined palm oil, invert sugar syrup, milk solids, raising agents, salt, emulsifiers (INS 471, INS 322)"},
    {"barcode": "8901063371071", "product_name": "Marie Gold 1kg", "brands": "Britannia", "ingredients_text": "Refined wheat flour (73%), sugar, refined palm oil, invert sugar syrup, milk solids, raising agents, salt, emulsifiers (INS 471, INS 322)"},
    {"barcode": "8901063165847", "product_name": "Treat", "brands": "Britannia", "ingredients_text": "Refined wheat flour, sugar, edible vegetable oil, invert syrup, raising agents, emulsifiers, flavours"},
    {"barcode": "8901063029323", "product_name": "Jim Jam", "brands": "Britannia", "ingredients_text": "Refined wheat flour, sugar, edible vegetable oil, invert syrup, raising agents, salt, emulsifier, colours (INS 122, INS 110)"},
    {"barcode": "8901063167124", "product_name": "Jim Jam", "brands": "Britannia", "ingredients_text": "Refined wheat flour, sugar, edible vegetable oil, invert syrup, raising agents, salt, emulsifier, colours (INS 122, INS 110)"},
    {"barcode": "8901063012578", "product_name": "Milk Bikis Classic", "brands": "Britannia", "ingredients_text": "Refined wheat flour, sugar, milk solids, edible vegetable oil, invert syrup, raising agents, salt, emulsifier, artificial vanilla flavour"},
    {"barcode": "8901063012493", "product_name": "Milk Bikis Biscuits", "brands": "Britannia", "ingredients_text": "Refined wheat flour, sugar, milk solids, edible vegetable oil, invert syrup, raising agents, salt, emulsifier, artificial vanilla flavour"},
    {"barcode": "8901063165618", "product_name": "Little Hearts", "brands": "Britannia", "ingredients_text": "Refined wheat flour, sugar, edible vegetable oil, invert syrup, milk solids, raising agents, salt, emulsifier"},
    {"barcode": "8901063017399", "product_name": "50-50 Maska Chaska", "brands": "Britannia", "ingredients_text": "Refined wheat flour, sugar, edible vegetable oil, invert syrup, salt, raising agents, emulsifier, artificial butter flavour"},
    {"barcode": "8901063139336", "product_name": "Bourbon 100g", "brands": "Britannia", "ingredients_text": "Refined wheat flour, sugar, edible vegetable oil, cocoa solids, invert syrup, raising agents, salt, emulsifiers, artificial chocolate flavour"},
    {"barcode": "8901063026346", "product_name": "NutriChoice Digestive", "brands": "Britannia", "ingredients_text": "Whole wheat flour (71%), sugar, edible vegetable oil, raising agents, salt, emulsifiers, added vitamins & minerals"},
    {"barcode": "8901063166318", "product_name": "NutriChoice Digestive Biscuits", "brands": "Britannia", "ingredients_text": "Whole wheat flour (71%), sugar, edible vegetable oil, raising agents, salt, emulsifiers, added vitamins & minerals"},
    {"barcode": "8901063155497", "product_name": "Tiger Krunch Coconut", "brands": "Britannia", "ingredients_text": "Refined wheat flour, sugar, edible vegetable oil, coconut, invert syrup, raising agents, emulsifier, artificial coconut flavour"},
    {"barcode": "8901063155572", "product_name": "Tiger Krunch", "brands": "Britannia", "ingredients_text": "Refined wheat flour, sugar, edible vegetable oil, coconut, invert syrup, raising agents, emulsifier, artificial coconut flavour"},
    {"barcode": "8901063325074", "product_name": "Toastea", "brands": "Britannia", "ingredients_text": "Refined wheat flour, sugar, edible vegetable oil, invert syrup, milk solids, raising agents, salt, emulsifier, artificial vanilla flavour"},
    {"barcode": "8901063325357", "product_name": "Toastea Rusk", "brands": "Britannia", "ingredients_text": "Refined wheat flour, sugar, edible vegetable oil, invert syrup, milk solids, raising agents, salt, emulsifier, artificial vanilla flavour"},
    {"barcode": "8901063365933", "product_name": "Gobbles Fruit Cake 100g", "brands": "Britannia", "ingredients_text": "Refined wheat flour, sugar, eggs, edible vegetable oil, glucose syrup, mixed fruit peel, raising agents, emulsifiers, preservative (INS 202), colours"},
    {"barcode": "8901063365131", "product_name": "Britannia Marble Cake", "brands": "Britannia", "ingredients_text": "Refined wheat flour, sugar, eggs, edible vegetable oil, glucose syrup, cocoa solids, raising agents, emulsifiers, preservative (INS 202)"},
    {"barcode": "8901063363960", "product_name": "Britannia Gobbles Chocolate Cake", "brands": "Britannia", "ingredients_text": "Refined wheat flour, sugar, eggs, edible vegetable oil, glucose syrup, cocoa solids, raising agents, emulsifiers, preservative (INS 202), colour (INS 122)"},
    {"barcode": "8901063363922", "product_name": "Muffils Strawberry", "brands": "Britannia", "ingredients_text": "Refined wheat flour, sugar, eggs, edible vegetable oil, glucose syrup, strawberry flavour, raising agents, emulsifiers, preservative (INS 202), colour (INS 122)"},
    {"barcode": "8901063146938", "product_name": "Winkin' Cow Bourbon Shake", "brands": "Britannia", "ingredients_text": "Toned milk, sugar, cocoa solids, artificial chocolate flavour, stabilizers, emulsifier, colour (INS 150c)"},
    {"barcode": "8901063146952", "product_name": "Winkin' Cow Strawberry Shake", "brands": "Britannia", "ingredients_text": "Toned milk, sugar, strawberry flavour, stabilizers, emulsifier, colour (INS 122)"},
    {"barcode": "8901063342910", "product_name": "Brown Bread", "brands": "Britannia", "ingredients_text": "Whole wheat flour, refined wheat flour, water, sugar, edible vegetable oil, gluten, yeast, salt, preservative (INS 282), emulsifiers"},

    # Parle
    {"barcode": "8901719135477", "product_name": "Parle-G Gold", "brands": "Parle", "ingredients_text": "Refined wheat flour, sugar, invert syrup, refined palm oil, salt, skimmed milk powder, raising agents (INS 503(ii), INS 500(ii)), emulsifier (INS 471), artificial vanilla flavour"},
    {"barcode": "8901719128486", "product_name": "Parle-G Rs 10", "brands": "Parle", "ingredients_text": "Refined wheat flour, sugar, invert syrup, refined palm oil, salt, skimmed milk powder, raising agents (INS 503(ii), INS 500(ii)), emulsifier (INS 471), artificial vanilla flavour"},
    {"barcode": "8901719123900", "product_name": "Parle-G Gold", "brands": "Parle", "ingredients_text": "Refined wheat flour, sugar, invert syrup, refined palm oil, salt, skimmed milk powder, raising agents (INS 503(ii), INS 500(ii)), emulsifier (INS 471), artificial vanilla flavour"},
    {"barcode": "8901719135521", "product_name": "Parle Marie", "brands": "Parle", "ingredients_text": "Refined wheat flour, sugar, refined palm oil, invert sugar syrup, milk solids, raising agents, salt, emulsifiers"},
    {"barcode": "8901719123801", "product_name": "Parle Monaco Classic", "brands": "Parle", "ingredients_text": "Refined wheat flour, edible vegetable oil, salt, sugar, raising agents, emulsifier, artificial butter flavour"},
    {"barcode": "8901719122781", "product_name": "Parle Monaco 700g", "brands": "Parle", "ingredients_text": "Refined wheat flour, edible vegetable oil, salt, sugar, raising agents, emulsifier, artificial butter flavour"},
    {"barcode": "8901719135309", "product_name": "Krackjack", "brands": "Parle", "ingredients_text": "Refined wheat flour, sugar, edible vegetable oil, invert syrup, salt, raising agents, emulsifier"},
    {"barcode": "8901719124006", "product_name": "Parle Krackjack", "brands": "Parle", "ingredients_text": "Refined wheat flour, sugar, edible vegetable oil, invert syrup, salt, raising agents, emulsifier"},
    {"barcode": "8901719136801", "product_name": "Hide & Seek Milano Creme", "brands": "Parle", "ingredients_text": "Refined wheat flour, sugar, edible vegetable oil, cocoa solids, invert syrup, milk solids, raising agents, emulsifiers"},
    {"barcode": "8901719136757", "product_name": "Hide & Seek Finest Choco", "brands": "Parle", "ingredients_text": "Refined wheat flour, sugar, edible vegetable oil, cocoa solids, invert syrup, milk solids, raising agents, emulsifiers"},
    {"barcode": "8901719113871", "product_name": "Parle Platina Hide & Seek Choco Rolls", "brands": "Parle", "ingredients_text": "Refined wheat flour, sugar, edible vegetable oil, cocoa solids, invert syrup, milk solids, raising agents, emulsifiers"},
    {"barcode": "8901719135842", "product_name": "Parle Hide & Seek Strawberry", "brands": "Parle", "ingredients_text": "Refined wheat flour, sugar, edible vegetable oil, strawberry flavour, invert syrup, raising agents, emulsifier, colours (INS 122)"},
    {"barcode": "8901719126970", "product_name": "Parle 20-20 Cashew", "brands": "Parle", "ingredients_text": "Refined wheat flour, sugar, edible vegetable oil, cashew nuts, invert syrup, milk solids, raising agents, emulsifier"},
    {"barcode": "8901719129179", "product_name": "Parle Coconut", "brands": "Parle", "ingredients_text": "Refined wheat flour, sugar, coconut, edible vegetable oil, invert syrup, raising agents, emulsifier, artificial coconut flavour"},
    {"barcode": "8901719136719", "product_name": "Parle Jam In", "brands": "Parle", "ingredients_text": "Refined wheat flour, sugar, fruit jam, edible vegetable oil, invert syrup, raising agents, emulsifier, colours (INS 110, INS 102)"},
    {"barcode": "8901719130854", "product_name": "Melody Chocolate", "brands": "Parle", "ingredients_text": "Sugar, glucose syrup, hydrogenated vegetable oil (palm kernel), milk solids, cocoa solids, emulsifier (INS 322), salt"},
    {"barcode": "8901719127762", "product_name": "Mango Bite Candy", "brands": "Parle", "ingredients_text": "Sugar, glucose syrup, mango pulp, acidity regulator (INS 330), artificial mango flavour, colour (INS 160c)"},
    {"barcode": "8901719119026", "product_name": "Parle Assorted Candy Orange Bite", "brands": "Parle", "ingredients_text": "Sugar, glucose syrup, orange flavour, acidity regulator, colour (INS 160c)"},
    {"barcode": "8901719130090", "product_name": "Parle Happy Happy", "brands": "Parle", "ingredients_text": "Refined wheat flour, sugar, edible vegetable oil, invert syrup, salt, raising agents, emulsifier"},
    {"barcode": "8901719128264", "product_name": "Parle Aloo Bikki", "brands": "Parle", "ingredients_text": "Refined wheat flour, potato, edible vegetable oil, spices, salt, sugar, raising agents"},
    {"barcode": "8901719127359", "product_name": "Parle Milk Shakti", "brands": "Parle", "ingredients_text": "Refined wheat flour, sugar, milk solids, edible vegetable oil, invert syrup, raising agents, emulsifiers"},
    {"barcode": "8901719127236", "product_name": "Parle Rusk", "brands": "Parle", "ingredients_text": "Refined wheat flour, sugar, edible vegetable oil, invert syrup, milk solids, raising agents, emulsifier"},
    {"barcode": "8901719122927", "product_name": "Parle Rusk Milk Premium", "brands": "Parle", "ingredients_text": "Refined wheat flour, sugar, edible vegetable oil, invert syrup, milk solids, raising agents, emulsifier"},
    {"barcode": "8901719707490", "product_name": "Murano Chocolate Chip Cookies", "brands": "Parle", "ingredients_text": "Refined wheat flour, sugar, chocolate chips, edible vegetable oil, invert syrup, raising agents, emulsifiers"},
    {"barcode": "8901719132155", "product_name": "Cocktail Mix", "brands": "Parle", "ingredients_text": "Refined wheat flour, sugar, edible vegetable oil, invert syrup, salt, raising agents, emulsifiers"},

    # Mondelez (Cadbury)
    {"barcode": "8901233028361", "product_name": "Dairy Milk", "brands": "Cadbury", "ingredients_text": "Sugar, milk solids, cocoa butter, cocoa mass, emulsifiers (INS 322, INS 476), flavours"},
    {"barcode": "8901233028392", "product_name": "Dairy Milk", "brands": "Cadbury", "ingredients_text": "Sugar, milk solids, cocoa butter, cocoa mass, emulsifiers (INS 322, INS 476), flavours"},
    {"barcode": "8901233034300", "product_name": "Dairy Milk Silk Bubbly", "brands": "Cadbury", "ingredients_text": "Sugar, milk solids, cocoa butter, cocoa mass, emulsifiers (INS 322, INS 476), flavours"},
    {"barcode": "8901233034263", "product_name": "Dairy Milk Roast Almond", "brands": "Cadbury", "ingredients_text": "Sugar, milk solids, cocoa butter, cocoa mass, almonds (15%), emulsifiers, flavours"},
    {"barcode": "8901233033563", "product_name": "Dairy Milk Silk Minis", "brands": "Cadbury", "ingredients_text": "Sugar, milk solids, cocoa butter, cocoa mass, emulsifiers (INS 322, INS 476), flavours"},
    {"barcode": "8901233024622", "product_name": "Cadbury Oreo 60g", "brands": "Cadbury", "ingredients_text": "Refined wheat flour, sugar, refined palm oil, cocoa solids (5%), invert syrup, raising agents, salt, emulsifier (INS 322), antioxidant (INS 319)"},
    {"barcode": "8901233024257", "product_name": "Dairy Milk Oreo", "brands": "Cadbury", "ingredients_text": "Sugar, milk solids, cocoa butter, cocoa mass, refined wheat flour, emulsifiers, flavours"},
    {"barcode": "8901233023687", "product_name": "Cadbury FUSE", "brands": "Cadbury", "ingredients_text": "Sugar, milk solids, cocoa butter, cocoa mass, glucose syrup, vegetable fats, emulsifiers (INS 442, INS 476), flavours"},
    {"barcode": "8901233024042", "product_name": "Cadbury Perk", "brands": "Cadbury", "ingredients_text": "Sugar, milk solids, cocoa solids, edible vegetable oil, emulsifiers, artificial flavours"},
    {"barcode": "8901233031712", "product_name": "Cadbury Fuse", "brands": "Cadbury", "ingredients_text": "Sugar, milk solids, cocoa butter, cocoa mass, glucose syrup, vegetable fats, emulsifiers (INS 442, INS 476), flavours"},
    {"barcode": "8901233023748", "product_name": "Bournvita Original Refill 500g", "brands": "Cadbury", "ingredients_text": "Malt extract (wheat/barley), sugar, milk solids, cocoa solids, liquid glucose, minerals, vitamins, emulsifier (INS 322), salt"},
    {"barcode": "8901233022536", "product_name": "Bournvita Biscuit", "brands": "Cadbury", "ingredients_text": "Refined wheat flour, sugar, cocoa solids, edible vegetable oil, milk solids, raising agents, emulsifiers"},
    {"barcode": "8901233025957", "product_name": "Marvellous Creations Jelly Popping Candy", "brands": "Cadbury", "ingredients_text": "Sugar, glucose syrup, milk solids, cocoa butter, cocoa mass, emulsifiers, colours, flavours, popping candy"},
    {"barcode": "8901233024981", "product_name": "Cadbury Zip Chocolate", "brands": "Cadbury", "ingredients_text": "Sugar, glucose syrup, milk solids, cocoa butter, cocoa mass, emulsifiers, flavours"},
    {"barcode": "8901233022575", "product_name": "Cadbury Perk", "brands": "Cadbury", "ingredients_text": "Sugar, milk solids, cocoa solids, edible vegetable oil, emulsifiers, artificial flavours"},
    {"barcode": "8901233022576", "product_name": "Cadbury Gems", "brands": "Cadbury", "ingredients_text": "Sugar, milk solids, cocoa solids, edible vegetable oil, emulsifier (INS 322), colours (INS 102, INS 110, INS 122, INS 133)"},
    {"barcode": "8901233030395", "product_name": "Cadbury Spready", "brands": "Cadbury", "ingredients_text": "Sugar, edible vegetable fat, milk solids (16%), cocoa solids, emulsifier (INS 442), added flavour"},
    {"barcode": "7622202324925", "product_name": "Dairy Milk Bites", "brands": "Cadbury", "ingredients_text": "Sugar, milk solids, cocoa butter, cocoa mass, emulsifiers, flavours"},
    {"barcode": "7622202335488", "product_name": "Cadbury Nutties Chocolate 30g", "brands": "Cadbury", "ingredients_text": "Sugar, peanuts, cocoa butter, milk solids, cocoa mass, emulsifiers"},
    {"barcode": "7622210063465", "product_name": "Cadbury Dairy Milk", "brands": "Cadbury", "ingredients_text": "Sugar, milk solids, cocoa butter, cocoa mass, emulsifiers (INS 322, INS 476), flavours"},

    # Haldiram's
    {"barcode": "8904063254696", "product_name": "Aloo Bhujia", "brands": "Haldiram's", "ingredients_text": "Potato flakes & starch, edible vegetable oil (palmolein), gram flour, iodized salt, spices, colour (INS 160c)"},
    {"barcode": "8904063254697", "product_name": "Bhujia Sev", "brands": "Haldiram's", "ingredients_text": "Gram flour (besan), edible vegetable oil, iodized salt, spices"},
    {"barcode": "8904004403770", "product_name": "Moong Dal", "brands": "Haldiram's", "ingredients_text": "Moong dal, edible vegetable oil, iodized salt, spices"},
    {"barcode": "8904063216403", "product_name": "Khatta Meetha", "brands": "Haldiram's", "ingredients_text": "Rice flakes, edible vegetable oil, sugar, peanuts, sago, salt, spices, raising agents, colours (INS 160c)"},
    {"barcode": "8904063216168", "product_name": "Bombay Mix", "brands": "Haldiram's", "ingredients_text": "Rice flakes, gram flour, edible vegetable oil, peanuts, sago, salt, spices, raising agents, colours (INS 160c)"},
    {"barcode": "8904063230133", "product_name": "Cornflakes Mixture", "brands": "Haldiram's", "ingredients_text": "Corn flakes, edible vegetable oil, peanuts, sago, salt, spices, sugar, raising agents, colours (INS 160c)"},
    {"barcode": "8904063214942", "product_name": "All In One Mixture", "brands": "Haldiram's", "ingredients_text": "Rice flakes, gram flour, edible vegetable oil, peanuts, sago, salt, spices, curry leaves, raising agents, colours"},
    {"barcode": "8904063203441", "product_name": "Ratlami Mixture", "brands": "Haldiram's", "ingredients_text": "Rice flakes, gram flour, edible vegetable oil, peanuts, sago, salt, spices, raising agents, colours"},
    {"barcode": "8904063253194", "product_name": "Kashmiri Mixture", "brands": "Haldiram's", "ingredients_text": "Rice flakes, gram flour, edible vegetable oil, peanuts, sago, salt, spices, raisins, raising agents, colours"},
    {"barcode": "8904063253804", "product_name": "Punjabi Tadka", "brands": "Haldiram's", "ingredients_text": "Rice flakes, gram flour, edible vegetable oil, peanuts, sago, salt, spices, raising agents, colours"},
    {"barcode": "8904004403534", "product_name": "Tasty Nuts", "brands": "Haldiram's", "ingredients_text": "Peanuts, edible vegetable oil, iodized salt, spices"},
    {"barcode": "8904063253156", "product_name": "Samosa", "brands": "Haldiram's", "ingredients_text": "Refined wheat flour, potato, peas, edible vegetable oil, spices, salt"},
    {"barcode": "8904063281586", "product_name": "Kadhai Paneer", "brands": "Haldiram's", "ingredients_text": "Paneer, edible vegetable oil, spices, salt, sugar"},
    {"barcode": "8904063259400", "product_name": "Minute Khana", "brands": "Haldiram's", "ingredients_text": "Refined wheat flour, edible vegetable oil, spices, salt, sugar, raising agents"},
    {"barcode": "8904063281494", "product_name": "Rasmalai", "brands": "Haldiram's", "ingredients_text": "Milk solids, sugar, cardamom, saffron"},
    {"barcode": "8904063281234", "product_name": "Phulka Roti", "brands": "Haldiram's", "ingredients_text": "Whole wheat flour, water, salt"},
    {"barcode": "8904063222091", "product_name": "Cheese Balls", "brands": "Haldiram's", "ingredients_text": "Refined wheat flour, cheese powder, edible vegetable oil, spices, salt, raising agents"},
    {"barcode": "8904063205018", "product_name": "Bread Pakora", "brands": "Haldiram's", "ingredients_text": "Refined wheat flour, potato, edible vegetable oil, spices, salt, raising agents"},
    {"barcode": "8904063224668", "product_name": "Mirchi Pakoda", "brands": "Haldiram's", "ingredients_text": "Gram flour, green chilli, edible vegetable oil, spices, salt, raising agents"},
    {"barcode": "8904063258410", "product_name": "Yellow Banana Chips", "brands": "Haldiram's", "ingredients_text": "Banana, edible vegetable oil, iodized salt"},
    {"barcode": "8904063200570", "product_name": "Chai Puri", "brands": "Haldiram's", "ingredients_text": "Refined wheat flour, edible vegetable oil, sugar, salt, spices, raising agents"},
    {"barcode": "8904063253262", "product_name": "Boondi", "brands": "Haldiram's", "ingredients_text": "Gram flour, edible vegetable oil, iodized salt, spices, colours (INS 160c)"},
    {"barcode": "8904063240248", "product_name": "Haldiram Bhujia 1kg", "brands": "Haldiram's", "ingredients_text": "Potato flakes & starch, edible vegetable oil (palmolein), gram flour, iodized salt, spices, colour (INS 160c)"},
    {"barcode": "8904063226372", "product_name": "Veggie And Paneer Momos", "brands": "Haldiram's", "ingredients_text": "Refined wheat flour, paneer, vegetables, edible vegetable oil, spices, salt"},
    {"barcode": "8904063204578", "product_name": "Gluten Free Chapati", "brands": "Haldiram's", "ingredients_text": "Gluten-free flour blend, water, salt"},

    # Amul
    {"barcode": "8901262150095", "product_name": "Amul Gold Milk 200ml", "brands": "Amul", "ingredients_text": "Standardized milk (4.5% fat, 8.5% SNF), vitamins A & D"},
    {"barcode": "8901262153577", "product_name": "Amul Taaza Toned Milk 200ml", "brands": "Amul", "ingredients_text": "Toned milk (3.0% fat, 8.5% SNF), vitamins A & D"},
    {"barcode": "8901262010436", "product_name": "Amul White Unsalted Butter", "brands": "Amul", "ingredients_text": "Pasteurized milk cream"},
    {"barcode": "8901262030243", "product_name": "Amul Ghee", "brands": "Amul", "ingredients_text": "Milk solids (pure cow ghee)"},
    {"barcode": "8901262030250", "product_name": "Amul Pure Ghee", "brands": "Amul", "ingredients_text": "Milk solids (pure cow ghee)"},
    {"barcode": "8901262200271", "product_name": "Amul Dahi", "brands": "Amul", "ingredients_text": "Pasteurized toned milk, active lactic culture"},
    {"barcode": "8901262180030", "product_name": "Amul Paneer", "brands": "Amul", "ingredients_text": "Milk solids, citric acid (coagulant)"},
    {"barcode": "8901262020404", "product_name": "Amul Cheese Slices", "brands": "Amul", "ingredients_text": "Milk solids, salt, emulsifying salts (INS 331, INS 452), preservative (INS 200), colour (INS 160a)"},
    {"barcode": "8901262020091", "product_name": "Amul Cheese Cubes", "brands": "Amul", "ingredients_text": "Milk solids, salt, emulsifying salts (INS 331, INS 452), preservative (INS 200)"},
    {"barcode": "8901262151375", "product_name": "Amul Cool Kesar", "brands": "Amul", "ingredients_text": "Toned milk, sugar, kesar flavour, stabilizers, emulsifier, colour (INS 160a)"},
    {"barcode": "8901262151429", "product_name": "Amul Kool Coffee", "brands": "Amul", "ingredients_text": "Toned milk, sugar, coffee, stabilizers, emulsifier, colour (INS 150c)"},
    {"barcode": "8901262200622", "product_name": "Amul Masti", "brands": "Amul", "ingredients_text": "Pasteurised toned milk, milk solids, active culture"},
    {"barcode": "8901262174565", "product_name": "Amul Punjabi Samosa", "brands": "Amul", "ingredients_text": "Refined wheat flour, potato, peas, edible vegetable oil, spices, salt"},
    {"barcode": "8901262222471", "product_name": "Amul Instant Mashed Potato", "brands": "Amul", "ingredients_text": "Dehydrated potato flakes, salt, emulsifier (INS 471), antioxidant (INS 304)"},
    {"barcode": "8901262200172", "product_name": "Amul Lassi 1L", "brands": "Amul", "ingredients_text": "Toned milk, sugar, active lactic culture"},
    {"barcode": "8901262178853", "product_name": "Amul Aloo Tikki", "brands": "Amul", "ingredients_text": "Potato, edible vegetable oil, spices, salt"},
    {"barcode": "8901262071680", "product_name": "Amul Hazelnut Chocolate", "brands": "Amul", "ingredients_text": "Sugar, milk solids, cocoa butter, cocoa mass, hazelnuts, emulsifiers"},
    {"barcode": "8901262171557", "product_name": "Amul Chocolate Family Pack", "brands": "Amul", "ingredients_text": "Toned milk, sugar, cocoa solids, edible vegetable oil, stabilizers, emulsifiers"},
    {"barcode": "8901262223539", "product_name": "Amul Chocolate Cookies", "brands": "Amul", "ingredients_text": "Refined wheat flour, sugar, cocoa solids, edible vegetable oil, raising agents, emulsifiers"},
    {"barcode": "8901262153423", "product_name": "Amul High Protein Milk", "brands": "Amul", "ingredients_text": "Standardized milk, milk protein, vitamins"},
    {"barcode": "8901262080101", "product_name": "Amul Spray Infant Milk Food", "brands": "Amul", "ingredients_text": "Demineralized whey, vegetable oils, skimmed milk powder, lactose, minerals, vitamins"},
    {"barcode": "8901262120029", "product_name": "Amul Mithai Mate", "brands": "Amul", "ingredients_text": "Milk solids, sugar"},
    {"barcode": "8901262070843", "product_name": "Amul Tropical Orange", "brands": "Amul", "ingredients_text": "Toned milk, sugar, orange flavour, stabilizers, emulsifiers, colours"},
    {"barcode": "8901262175869", "product_name": "Amul Shalimar", "brands": "Amul", "ingredients_text": "Toned milk, sugar, flavour, stabilizers"},
    {"barcode": "8901262220125", "product_name": "Amul Sandwich Bread", "brands": "Amul", "ingredients_text": "Refined wheat flour, water, sugar, milk solids, edible vegetable oil, yeast, salt, preservative (INS 282)"}
]

print(f"Parsed {len(batch7_raw)} products from batch 7 request.")

elevated_count = 0
added_count = 0
updated_count = 0

for item in batch7_raw:
    barcode = item["barcode"]
    name = item["product_name"]
    brand = item["brands"]
    ingredients = item["ingredients_text"]

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
        row = df_nv.loc[idx_nv].iloc[0].to_dict()
        row['ingredients_text'] = ingredients
        row['product_name'] = name
        row['brands'] = brand
        row['status'] = 'KEEP'
        row['sold_in_india_status'] = 'CONFIRMED_INDIA_890'
        row['ingredient_confidence'] = 'HIGH'
        row['data_source'] = 'Brand Official Publication'
        row['source_license'] = 'User-submitted'
        row['collection_method'] = 'API/CSV Import'
        
        # Append to confirmed, delete from needs_verification
        df_c = pd.concat([df_c, pd.DataFrame([row])], ignore_index=True)
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

print("Batch 7 Processing Results:")
print(f"  Elevated from Needs Verification: {elevated_count}")
print(f"  Added direct to Confirmed: {added_count}")
print(f"  Updated in Confirmed: {updated_count}")

# Save dataframes
df_c.to_csv(confirmed_path, index=False)
df_nv.to_csv(needs_ver_path, index=False)
print("Saved files successfully.")
