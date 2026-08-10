import os
import sys
import pandas as pd
import re

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"c:\Users\thout\Downloads\check it"
confirmed_csv = os.path.join(BASE_DIR, "india_products_confirmed.csv")
all_csv = os.path.join(BASE_DIR, "all_supabase_products.csv")

df_confirmed = pd.read_csv(confirmed_csv, dtype=str)
df_all = pd.read_csv(all_csv, dtype=str)

# Define additive patterns and international ban jurisdictions
banned_patterns = {
    "INS 171 / E171 (Titanium Dioxide)": {
        "pattern": r"\b(171|E-?171|Titanium Dioxide)\b",
        "banned_in": ["European Union (EU)", "Switzerland"],
        "reason": "Genotoxicity concerns, risk of DNA damage (banned in food by EFSA since 2022)"
    },
    "INS 102 / E102 (Tartrazine / Yellow 5)": {
        "pattern": r"\b(102|E-?102|Tartrazine|Yellow 5)\b",
        "banned_in": ["Norway", "Austria (strict warning labels in EU & UK)"],
        "reason": "Hyperactivity in children, allergic reactions, asthma trigger"
    },
    "INS 110 / E110 (Sunset Yellow FCF / Yellow 6)": {
        "pattern": r"\b(110|E-?110|Sunset Yellow|Yellow 6)\b",
        "banned_in": ["Norway", "Finland (warning labels in EU & UK)"],
        "reason": "Childhood hyperactivity (Southampton 6), potential carcinogen impurities"
    },
    "INS 122 / E122 (Azorubine / Carmoisine)": {
        "pattern": r"\b(122|E-?122|Azorubine|Carmoisine)\b",
        "banned_in": ["USA", "Japan", "Canada", "Norway", "Sweden"],
        "reason": "Banned by US FDA & Japan MHLW due to hyperactivity & allergic reactions"
    },
    "INS 124 / E124 (Ponceau 4R)": {
        "pattern": r"\b(124|E-?124|Ponceau 4R)\b",
        "banned_in": ["USA", "Canada", "Norway"],
        "reason": "Banned by US FDA & Canada Health due to allergenicity & hyperactivity"
    },
    "INS 127 / E127 (Erythrosine / Red 3)": {
        "pattern": r"\b(127|E-?127|Erythrosine|Red 3)\b",
        "banned_in": ["California (AB418 Food Safety Act)", "EU (restricted to cherries)"],
        "reason": "Linked to thyroid tumors in animal studies; banned in California"
    },
    "INS 129 / E129 (Allura Red AC / Red 40)": {
        "pattern": r"\b(129|E-?129|Allura Red|Red 40)\b",
        "banned_in": ["Denmark", "Belgium", "France", "Switzerland", "Sweden"],
        "reason": "Hyperactivity in children, gut inflammation concerns"
    },
    "INS 133 / E133 (Brilliant Blue FCF / Blue 1)": {
        "pattern": r"\b(133|E-?133|Brilliant Blue|Blue 1)\b",
        "banned_in": ["France", "Germany", "Belgium", "Austria", "Switzerland", "Norway"],
        "reason": "Neurotoxicity concerns and hypersensitivity reactions"
    },
    "INS 319 / E319 (TBHQ / Tertiary Butylhydroquinone)": {
        "pattern": r"\b(319|E-?319|TBHQ|Tertiary Butylhydroquinone)\b",
        "banned_in": ["Japan"],
        "reason": "Banned in food by Japan MHLW due to liver enlargement & DNA damage risk in high doses"
    },
    "INS 320 / E320 (BHA / Butylated Hydroxyanisole)": {
        "pattern": r"\b(320|E-?320|BHA|Butylated Hydroxyanisole)\b",
        "banned_in": ["Japan", "EU (restricted)", "California Prop 65 warning"],
        "reason": "Endocrine disruptor, classified as reasonably anticipated human carcinogen"
    },
    "INS 321 / E321 (BHT / Butylated Hydroxytoluene)": {
        "pattern": r"\b(321|E-?321|BHT|Butylated Hydroxytoluene)\b",
        "banned_in": ["Japan", "Romania", "Sweden", "Australia (restricted in infant food)"],
        "reason": "Organ system toxicity and endocrine disruption"
    },
    "INS 211 / E211 (Sodium Benzoate)": {
        "pattern": r"\b(211|E-?211|Sodium Benzoate)\b",
        "banned_in": ["Strictly restricted in EU/Japan when combined with Vitamin C (INS 300)"],
        "reason": "Forms Benzene (known carcinogen) in presence of Ascorbic Acid (Vitamin C)"
    },
    "INS 621 / E621 (MSG / Monosodium Glutamate)": {
        "pattern": r"\b(621|E-?621|Monosodium Glutamate|MSG)\b",
        "banned_in": ["Restricted in EU/UK infant food, mandatory warning in EU/ANZ"],
        "reason": "Excitotoxin, linked to Chinese Restaurant Syndrome, asthma trigger"
    },
    "INS 951 / E951 (Aspartame)": {
        "pattern": r"\b(951|E-?951|Aspartame)\b",
        "banned_in": ["WHO IARC Group 2B Possibly Carcinogenic to Humans"],
        "reason": "Classified by WHO IARC in 2023 as possibly carcinogenic"
    },
    "Potassium Bromate": {
        "pattern": r"\b(Potassium Bromate|Bromated Flour)\b",
        "banned_in": ["EU", "UK", "Canada", "China", "Brazil", "India (banned 2016)"],
        "reason": "Category 2B carcinogen (kidney tumors)"
    }
}

print("=== INTERNATIONAL BANNED INGREDIENTS AUDIT REPORT ===")

# Audit domestic confirmed Indian products
results_confirmed = {}
total_confirmed = len(df_confirmed)
flagged_barcodes_confirmed = set()

for name, info in banned_patterns.items():
    pat = re.compile(info["pattern"], re.IGNORECASE)
    matches = df_confirmed[df_confirmed['ingredients_text'].fillna('').str.contains(pat, regex=True)]
    count = len(matches)
    results_confirmed[name] = {
        "count": count,
        "banned_in": ", ".join(info["banned_in"]),
        "reason": info["reason"],
        "sample_brands": matches['brands'].value_counts().head(3).to_dict() if count > 0 else {}
    }
    for b in matches['barcode']:
        flagged_barcodes_confirmed.add(b)

total_flagged_confirmed = len(flagged_barcodes_confirmed)
pct_flagged_confirmed = (total_flagged_confirmed / total_confirmed * 100) if total_confirmed > 0 else 0

print(f"Total Confirmed Domestic Products Analyzed: {total_confirmed}")
print(f"Total Confirmed Products Containing Internationally Banned Additives: {total_flagged_confirmed} ({pct_flagged_confirmed:.2f}%)")
print("\nBreakdown by Additive (Domestic Confirmed):")

for name, res in sorted(results_confirmed.items(), key=lambda x: x[1]['count'], reverse=True):
    if res['count'] > 0:
        print(f"  • {name}: {res['count']} products")
        print(f"    - Banned/Restricted in: {res['banned_in']}")
        print(f"    - Risk/Reason: {res['reason']}")
        if res['sample_brands']:
            brands_str = ", ".join([f"{k} ({v})" for k, v in res['sample_brands'].items()])
            print(f"    - Top Brands: {brands_str}")
        print()

# Audit all complete ingredient products in Master DB
df_with_ing = df_all[df_all['ingredients_text'].notna() & (df_all['ingredients_text'].str.strip() != '') & (~df_all['ingredients_text'].str.startswith('Verify', na=False))]
total_master_with_ing = len(df_with_ing)
flagged_barcodes_master = set()

for name, info in banned_patterns.items():
    pat = re.compile(info["pattern"], re.IGNORECASE)
    matches = df_with_ing[df_with_ing['ingredients_text'].fillna('').str.contains(pat, regex=True)]
    for b in matches['barcode']:
        flagged_barcodes_master.add(b)

total_flagged_master = len(flagged_barcodes_master)
pct_flagged_master = (total_flagged_master / total_master_with_ing * 100) if total_master_with_ing > 0 else 0

print(f"Total Master DB Products with Complete Ingredients Analyzed: {total_master_with_ing}")
print(f"Total Master DB Products Containing Internationally Banned Additives: {total_flagged_master} ({pct_flagged_master:.2f}%)")
