import os
import sys
import pandas as pd
import re

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"c:\Users\thout\Downloads\check it"

confirmed_csv = os.path.join(BASE_DIR, "india_products_confirmed.csv")
verification_csv = os.path.join(BASE_DIR, "india_products_needs_verification.csv")

print("=== PROVENANCE LEDGER: SIGNATURE-BASED SOURCE DETECTION ===")

# Process both tables
for label, csv_path in [("CONFIRMED", confirmed_csv), ("NEEDS_VERIFICATION", verification_csv)]:
    df = pd.read_csv(csv_path, dtype=str)
    print(f"\nProcessing {label}: {len(df)} rows")

    def detect_source(row):
        ing = str(row.get('ingredients_text', '') or '')
        name = str(row.get('product_name', '') or '')
        brand = str(row.get('brands', '') or '')
        
        # 1. OFF signature: allergen HTML spans
        if '<span class="allergen">' in ing or '<span class=' in ing:
            return 'OpenFoodFacts (ODbL)'
        
        # 2. OFF multilingual signature: French/non-English on 890 barcodes
        french_words = ['eau','henné','sel','curcuma','poudre','riz','concentré',
                        'huile','vin','éclairs','chargement','chocolat','sucre',
                        'farine','beurre','lait','crème','sirop','vinaigre',
                        'graisses végétales','émulsifiant','arôme']
        if any(w in name.lower() or w in ing.lower() for w in french_words):
            return 'OpenFoodFacts (ODbL)'
        
        # 3. OCR garbage signature
        if re.search(r'MFD|Lot\.|Chargement|M\.Code|Lic No|inner pouch|FSSAI Lic|Mfg\. Date|Best Before|USP:', 
                      name, re.I):
            return 'Raw OCR Scrape (Needs QA)'
        
        # 4. Has complete English ingredient text (likely OFF or user scan)
        if ing and ing.strip().lower() not in ['nan', 'none', ''] and len(ing.strip()) > 30:
            # Check for OFF-style formatting patterns
            if re.search(r'e\d{3}|INS \d{3}|emulsifier|stabilizer|acidity regulator', ing, re.I):
                return 'OpenFoodFacts (ODbL)'
            return 'User Scan / Brand Publication'
        
        # 5. Has product name + brand but no ingredients
        if name and name.strip().lower() not in ['nan', 'none', '']:
            return 'Barcode Registry (No Ingredient Text)'
        
        return 'Source Unknown'

    df['data_source'] = df.apply(detect_source, axis=1)
    df['source_license'] = df['data_source'].apply(
        lambda x: 'ODbL' if 'OpenFoodFacts' in x else ('User-submitted' if 'User Scan' in x else 'Pending Attribution')
    )
    df['collection_method'] = df['data_source'].apply(
        lambda x: 'API/CSV Import' if 'OpenFoodFacts' in x else ('OCR' if 'OCR' in x else 'Barcode Scan')
    )

    # Print breakdown
    print(f"\n  Source Breakdown for {label}:")
    source_counts = df['data_source'].value_counts()
    for src, cnt in source_counts.items():
        print(f"    {src}: {cnt} ({cnt/len(df)*100:.1f}%)")

    # Save back
    df.to_csv(csv_path, index=False)

print("\n=== PROVENANCE LEDGER COLUMNS ADDED SUCCESSFULLY ===")
print("Added columns: data_source, source_license, collection_method")
