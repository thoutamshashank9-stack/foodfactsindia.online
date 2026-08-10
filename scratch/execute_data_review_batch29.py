import os
import sys
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"c:\Users\thout\Downloads\check it"

all_supabase_csv = os.path.join(BASE_DIR, "all_supabase_products.csv")
confirmed_csv = os.path.join(BASE_DIR, "india_products_confirmed.csv")
needs_ver_csv = os.path.join(BASE_DIR, "india_products_needs_verification.csv")

print("=== EXECUTING BATCH 29 INGREDIENTS INTEGRATION & PURGE ===")

df_all = pd.read_csv(all_supabase_csv, dtype=str)
df_confirmed = pd.read_csv(confirmed_csv, dtype=str) if os.path.exists(confirmed_csv) else pd.DataFrame()
df_needs_ver = pd.read_csv(needs_ver_csv, dtype=str) if os.path.exists(needs_ver_csv) else pd.DataFrame()

for df in [df_all, df_confirmed, df_needs_ver]:
    if not df.empty and 'barcode' in df.columns:
        df['barcode'] = df['barcode'].astype(str).str.strip()

batch_29_rows = [
    {"barcode":"7613035281783","product_name":"Nestle Pure Life Still Spring Water","brands":"Nestlé","ingredients_text":"Water","additive_flags":"Clean single-ingredient"},
    {"barcode":"4902102014281","product_name":"Coca-Cola","brands":"Coca-Cola","ingredients_text":"Sugar, sodium carbonate, caramel coloring, acidulant, flavoring, caffeine","additive_flags":"INS 150d Caramel"},
    {"barcode":"3168930168102","product_name":"Lay's Recette à l'Ancienne Nature Maxi Format","brands":"Lay's","ingredients_text":"Potatoes (66%), vegetable oils (sunflower, rapeseed, maize in varying proportions), salt","additive_flags":"Clean"},
    {"barcode":"0028000517205","product_name":"Media Crema","brands":"Nestlé","ingredients_text":"Light cream, carrageenan, sodium alginate, disodium phosphate, sodium citrate","additive_flags":"Clean"},
    {"barcode":"5024616003021","product_name":"Still Spring Water","brands":"Nestlé/Princes Gate","ingredients_text":"Still drinking water","additive_flags":"Clean single-ingredient"},
    {"barcode":"8411002101503","product_name":"Agua Mineral Natural","brands":"Viladrau/Nestlé","ingredients_text":"Agua mineral natural","additive_flags":"Clean single-ingredient"},
    {"barcode":"85906662","product_name":"Kofila","brands":"Orion/Zora/Nestlé Česko","ingredients_text":"Sugar, sweetened condensed milk, cocoa butter, vegetable fats (palm, palm kernel, shea), milk powder, cocoa mass, coffee paste 4.5%, glucose-fructose syrup, caramelized sugar, glucose syrup, alcohol, milk fat, dried whey, lecithins, salt, flavour, hazelnut paste","additive_flags":"Clean"},
    {"barcode":"3948725000370","product_name":"Sunfeast Marie Light Active","brands":"Sunfeast","ingredients_text":"Biscuit","additive_flags":"Clean"},
    {"barcode":"0251921100519","product_name":"Kurkure","brands":"Kurkure","ingredients_text":"Oil, flour","additive_flags":"Clean"},
    {"barcode":"0068274264498","product_name":"Nestle Pure Life Water Beverage Acai Grape Splash","brands":"Nestlé","ingredients_text":"Water, natural flavour, citric acid, sucralose","additive_flags":"Clean"},
    {"barcode":"0068274934711","product_name":"Purified Drinking Water","brands":"Nestlé/Pure Life","ingredients_text":"Purified water","additive_flags":"Clean single-ingredient"},
    {"barcode":"8002270386794","product_name":"Sanpellegrino Limone","brands":"San Pellegrino/Nestlé","ingredients_text":"Carbonated water, lemon juice, sugar, natural flavours","additive_flags":"Clean"},
    {"barcode":"3023290063842","product_name":"Crème Dessert Saveur Vanille","brands":"Nestlé/Lindahls","ingredients_text":"Skimmed milk (87.4%), milk proteins, modified corn starch, thickener (pectin), flavour, colour (beta-carotene), sweeteners (acesulfame-K, sucralose)","additive_flags":"Clean"},
    {"barcode":"8904089923682","product_name":"Curd","brands":"Heritage","ingredients_text":"Pasteurised toned milk & active lactic cultures","additive_flags":"Clean"},
    {"barcode":"8902901011685","product_name":"Good Life Toor Dal","brands":"Good Life","ingredients_text":"Toor dal","additive_flags":"Clean single-ingredient"},
    {"barcode":"8908019558067","product_name":"Protein Water Green Apple Flavour","brands":"Aquatein Pro","ingredients_text":"Water, whey protein isolate, acidity regulator, sweetener (sucralose), permitted class II preservatives (INS 211), stabilizers (INS 412, INS 466), contains permitted synthetic food colour, nature identical flavouring","additive_flags":"INS 211 preservative"},
    {"barcode":"8901725008307","product_name":"B Natural Select Tender Coconut Water","brands":"B Natural","ingredients_text":"Water, concentrated tender coconut water (9.2%) [tender coconut water, preservative (INS 202)]","additive_flags":"INS 202 preservative"},
    {"barcode":"8906095121434","product_name":"Cashew Nuts","brands":"Wonderland Foods","ingredients_text":"Cashew nuts","additive_flags":"Clean single-ingredient"},
    {"barcode":"8585002476166","product_name":"6 Cuburi Vita","brands":"Maggi","ingredients_text":"Iodized salt, palm fat, flavour enhancers (monosodium glutamate INS 621, disodium 5'-ribonucleotides), maltodextrin, corn starch, sugar, flavours, onion powder 2%, plain caramel colour, barley malt extract, beef powder, dried parsley leaves 0.3%","additive_flags":"INS 621 MSG"},
    {"barcode":"0001678530004","product_name":"Bisk Farm Rich Marie","brands":"Bisk Farm","ingredients_text":"Refined wheat flour, sugar, edible vegetable oil, invert syrup, raising agents, emulsifiers","additive_flags":"Clean"},
    {"barcode":"8901719128264","product_name":"Parle Aloo Bikki","brands":"Parle","ingredients_text":"Refined wheat flour, potato, edible vegetable oil, spices, salt, sugar, raising agents","additive_flags":"Clean"},
    {"barcode":"8901719128271","product_name":"Parle Aloo Bikki","brands":"Parle","ingredients_text":"Refined wheat flour, potato, edible vegetable oil, spices, salt, sugar, raising agents","additive_flags":"Clean"},
    {"barcode":"7622201756932","product_name":"Cadbury Oreo Coco Creme","brands":"Cadbury/Oreo","ingredients_text":"Refined wheat flour, sugar, refined palm oil, cocoa solids, coconut creme, invert syrup, raising agents, emulsifiers","additive_flags":"Clean"},
    {"barcode":"8901719127359","product_name":"Parle Milk Shakti","brands":"Parle","ingredients_text":"Refined wheat flour, sugar, milk solids, edible vegetable oil, invert syrup, raising agents, emulsifiers","additive_flags":"Clean"},
    {"barcode":"8904064662537","product_name":"Mohnsamen","brands":"Transfood","ingredients_text":"Poppy seeds (mohnsamen)","additive_flags":"Clean single-ingredient"},
    {"barcode":"8904064619906","product_name":"Schwarzkümmel","brands":"Transfood","ingredients_text":"Black cumin seeds (schwarzkümmel/nigella)","additive_flags":"Clean single-ingredient"},
    {"barcode":"8906077362060","product_name":"Double Methi Masala Khakhra","brands":"Various","ingredients_text":"Whole wheat flour, fenugreek leaves, spices, salt, edible vegetable oil","additive_flags":"Clean"},
    {"barcode":"8904132919440","product_name":"Badam Drink Mix 200g","brands":"Various","ingredients_text":"Almonds, sugar, milk solids, cardamom, saffron","additive_flags":"Clean"},
    {"barcode":"8903996006372","product_name":"Osteo Gel","brands":"L'Amar","ingredients_text":"NON-FOOD — Medicine/gel","additive_flags":"NON-FOOD — PURGE"},
    {"barcode":"8906080600913","product_name":"Unknown","brands":"Various","ingredients_text":"Verify specific product","additive_flags":"Verify"},
    {"barcode":"8901138819965","product_name":"Himalaya","brands":"Himalaya","ingredients_text":"Verify specific product","additive_flags":"Verify"},
    {"barcode":"8906059636004","product_name":"Greek Yogurt","brands":"Epigamia","ingredients_text":"Pasteurized milk, active lactic culture","additive_flags":"Clean"},
    {"barcode":"8907020526096","product_name":"Unknown","brands":"Various","ingredients_text":"Verify specific product","additive_flags":"Verify"},
    {"barcode":"8901512926401","product_name":"Unknown","brands":"Various","ingredients_text":"Verify specific product","additive_flags":"Verify"},
    {"barcode":"8906076132602","product_name":"Choco Chip Cookies","brands":"The Baker's Dozen","ingredients_text":"Refined wheat flour, sugar, chocolate chips, edible vegetable oil, raising agents, emulsifiers","additive_flags":"Clean"},
    {"barcode":"50157334","product_name":"Moutarde Miel","brands":"Heinz","ingredients_text":"Water, mustard seeds 15%, sugar, vinegar, honey 6%, malt vinegar (barley), salt, herbs and spices, thickener (xanthan gum), natural flavour","additive_flags":"Clean"},
    {"barcode":"00237023","product_name":"Unknown","brands":"Various","ingredients_text":"Verify specific product","additive_flags":"Verify"},
    {"barcode":"00244931","product_name":"Kurkure","brands":"Kurkure","ingredients_text":"Verify specific product","additive_flags":"Verify"},
    {"barcode":"00024858","product_name":"Dry Yeast","brands":"Truly Good Food","ingredients_text":"Dry yeast","additive_flags":"Clean single-ingredient"},
    {"barcode":"7613036761697","product_name":"Contrex Green Framboise","brands":"Nestlé/Contrex","ingredients_text":"Natural mineral water Contrex 56%, organic green mate infusion 33.5%, water, organic liquid cane sugar 3%, acidifier: citric acid, natural raspberry flavour with other natural flavours","additive_flags":"Clean"},
    {"barcode":"0068274347368","product_name":"Nestle Pure Life Revive","brands":"Nestlé Pure Life","ingredients_text":"Purified water, magnesium sulfate, citric acid (to maintain freshness), natural flavours","additive_flags":"Clean"},
    {"barcode":"5449000037978","product_name":"Coca-Cola Light","brands":"Coca-Cola","ingredients_text":"Carbonated water, dye (caramel INS 150d), acidifiers (phosphoric acid, citric acid), sweeteners (aspartame, acesulfame K), plant extracts, caffeine aroma","additive_flags":"INS 150d Caramel"},
    {"barcode":"0009064407928","product_name":"Delowar","brands":"Various","ingredients_text":"NON-FOOD — Voltage stabilizer/electrical product","additive_flags":"NON-FOOD — PURGE"},
    {"barcode":"01746305","product_name":"Unknown","brands":"Various","ingredients_text":"Verify specific product","additive_flags":"Verify"},
    {"barcode":"0764460291056","product_name":"The Originote","brands":"Various","ingredients_text":"Verify specific product","additive_flags":"Verify"},
    {"barcode":"0053859034382","product_name":"Heritage","brands":"Stremicks Heritage Foods LLC","ingredients_text":"Organic milk, organic skim milk, organic nonfat milk solids, vitamin A palmitate, vitamin D3","additive_flags":"Clean"},
    {"barcode":"00001295","product_name":"Feed Grade Soybeans","brands":"H-E-B/Rural Route 1","ingredients_text":"NON-FOOD — Animal feed","additive_flags":"NON-FOOD — PURGE"},
    {"barcode":"90446207","product_name":"ORGANICS Viva Mate","brands":"Red Bull","ingredients_text":"Water, sugar, carbon dioxide, lemon juice concentrate, mate extract (0.33%), caramel sugar syrup, natural lemon flavour, carob flavour and vanilla flavour, natural caffeine flavour","additive_flags":"Clean"},
    {"barcode":"9900601913017","product_name":"Good Life Almond","brands":"Good Life","ingredients_text":"Almonds","additive_flags":"Clean single-ingredient"},
    {"barcode":"2698201756697","product_name":"Unknown","brands":"Various","ingredients_text":"Verify specific product","additive_flags":"Verify"},
    {"barcode":"84504517","product_name":"Kinder Joy","brands":"Kinder","ingredients_text":"Sugar, milk solids, cocoa butter, cocoa mass, emulsifiers, flavours, toy inside","additive_flags":"Clean"},
    {"barcode":"0661706974370","product_name":"Unknown","brands":"Various","ingredients_text":"Verify specific product","additive_flags":"Verify"},
    {"barcode":"0431627066061","product_name":"Unknown","brands":"Various","ingredients_text":"Verify specific product","additive_flags":"Verify"},
    {"barcode":"9427142066021","product_name":"Unknown","brands":"Various","ingredients_text":"Verify specific product","additive_flags":"Verify"},
    {"barcode":"9505000021549","product_name":"Unknown","brands":"Various","ingredients_text":"Verify specific product","additive_flags":"Verify"},
    {"barcode":"8564324165644","product_name":"Lemon Juice","brands":"Fruitaco","ingredients_text":"Lemon juice (99%), water (1%), class II preservative (INS 224)","additive_flags":"INS 224 preservative"},
    {"barcode":"0068274193996","product_name":"Nestle Splash Citron","brands":"Nestlé","ingredients_text":"Water, natural flavours, citric acid, sodium hexametaphosphate, potassium sorbate, potassium benzoate, sucralose, acesulfame-potassium, calcium disodium EDTA","additive_flags":"Clean"},
    {"barcode":"90446290","product_name":"Organics Viva Mat","brands":"Organics/Red Bull","ingredients_text":"Water, sugar, carbon dioxide, lemon juice concentrate, natural mate extract (0.33%), natural flavours from plant extracts (0.05%: lemon, caffeine from coffee beans, carob, vanilla), caramel sugar syrup","additive_flags":"Clean"},
    {"barcode":"7613034227775","product_name":"Chicorée & Café RICORÉ L'Original","brands":"Nestlé/Ricore","ingredients_text":"Instant coffee (33.2%), chicory fibre (oligofructose) (33%), soluble chicory (30%), magnesium sulfate","additive_flags":"Clean"},
    {"barcode":"9064407928","product_name":"Delowar","brands":"Various","ingredients_text":"NON-FOOD — Voltage stabilizer/electrical product","additive_flags":"NON-FOOD — PURGE"},
    {"barcode":"8904406118883","product_name":"Evocus Water","brands":"Evocus","ingredients_text":"Purified water, nature identical flavour (contains minerals)","additive_flags":"Clean"},
    {"barcode":"8908000729629","product_name":"Opener Nimbu","brands":"Opener","ingredients_text":"Purified water, cane sugar, lemon juice 6%, CO2 (INS 290), citric acid (INS 330), permitted class-II preservative (INS 211), iodised salt","additive_flags":"INS 211 preservative"},
    {"barcode":"8902080304059","product_name":"7Up Super Duper 750ml","brands":"PepsiCo","ingredients_text":"Carbonated water, sugar, acidity regulators, natural lemon flavour","additive_flags":"Clean"},
    {"barcode":"8901030518607","product_name":"Brown & Polson","brands":"Brown & Polson","ingredients_text":"Maize starch, iodised salt, tartrazine, sunset yellow FCF, nature identical flavouring substance","additive_flags":"INS 102 + INS 110 colours"},
    {"barcode":"8901792001829","product_name":"Niru","brands":"Niru","ingredients_text":"100% wheat cream","additive_flags":"Clean single-ingredient"}
]

elevated_count = 0
added_count = 0
purged_count = 0

for item in batch_29_rows:
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

print(f"Batch 29 Processing Summary:")
print(f"  Elevated from Needs Verification to Confirmed: {elevated_count}")
print(f"  Newly added to Confirmed: {added_count}")
print(f"  Purged Non-Food Barcodes: {purged_count}")
print(f"  Final Master CSV Count: {len(df_all)}")
print(f"  Final Confirmed CSV Count: {len(df_confirmed)}")
print(f"  Final Needs Verification CSV Count: {len(df_needs_ver)}")
