import pandas as pd
import json
import os
import re

confirmed_csv = "india_products_confirmed.csv"
needs_ver_csv = "india_products_needs_verification.csv"
all_supabase_csv = "all_supabase_products.csv"

# Global Regulatory Banned / Restricted Additives Database & Scientific Risk Rules
BANNED_ADDITIVES_RULES = [
    {
        "pattern": r'\b(INS\s*171|E171|TITANIUM\s*DIOXIDE)\b',
        "code": "INS 171",
        "name": "Titanium Dioxide",
        "jurisdiction": "European Union (EFSA Banned)",
        "reason": "Banned in EU due to genotoxicity concerns & DNA damage risk.",
        "risk_tier": "🔴 High Concern"
    },
    {
        "pattern": r'\b(INS\s*319|E319|TBHQ|TERTIARY\s*BUTYLHYDROQUINONE)\b',
        "code": "INS 319",
        "name": "TBHQ (Tertiary Butylhydroquinone)",
        "jurisdiction": "Japan (MHLW Banned) / EU Limits",
        "reason": "Banned in Japan; linked to liver enlargement, neurotoxicity, and cellular damage.",
        "risk_tier": "🔴 High Concern"
    },
    {
        "pattern": r'\b(INS\s*320|E320|BHA|BUTYLATED\s*HYDROXYANISOLE)\b',
        "code": "INS 320",
        "name": "BHA (Butylated Hydroxyanisole)",
        "jurisdiction": "European Union / Japan / CA Prop 65",
        "reason": "Suspected endocrine disruptor and potential carcinogen.",
        "risk_tier": "🔴 High Concern"
    },
    {
        "pattern": r'\b(INS\s*321|E321|BHT|BUTYLATED\s*HYDROXYTOLUENE)\b',
        "code": "INS 321",
        "name": "BHT (Butylated Hydroxytoluene)",
        "jurisdiction": "European Union / Japan",
        "reason": "Suspected endocrine disruptor, thyroid toxicity, and potential allergen.",
        "risk_tier": "🔴 High Concern"
    },
    {
        "pattern": r'\b(INS\s*102|E102|TARTRAZINE|YELLOW\s*5)\b',
        "code": "INS 102",
        "name": "Tartrazine (Synthetic Yellow Dye)",
        "jurisdiction": "European Union (Mandatory Warning) / Norway Banned",
        "reason": "Linked to ADHD/hyperactivity in children, asthma, and severe allergic reactions.",
        "risk_tier": "🔴 High Concern"
    },
    {
        "pattern": r'\b(INS\s*110|E110|SUNSET\s*YELLOW|YELLOW\s*6)\b',
        "code": "INS 110",
        "name": "Sunset Yellow FCF",
        "jurisdiction": "European Union (Mandatory Warning) / Norway Banned",
        "reason": "Linked to child hyperactivity, immunosuppression, and allergic asthma.",
        "risk_tier": "🔴 High Concern"
    },
    {
        "pattern": r'\b(INS\s*122|E122|AZORUBINE|CARMOISINE)\b',
        "code": "INS 122",
        "name": "Azorubine / Carmoisine",
        "jurisdiction": "European Union (Mandatory Warning) / US FDA Banned",
        "reason": "Banned in US, Japan, & Canada; linked to ADHD and bladder/kidney inflammation.",
        "risk_tier": "🔴 High Concern"
    },
    {
        "pattern": r'\b(INS\s*124|E124|PONCEAU\s*4R|BRILLIANT\s*SCARLET)\b',
        "code": "INS 124",
        "name": "Ponceau 4R",
        "jurisdiction": "European Union (Mandatory Warning) / US FDA Banned",
        "reason": "Banned in US, Norway, & Japan; linked to child behavioral disruption & allergies.",
        "risk_tier": "🔴 High Concern"
    },
    {
        "pattern": r'\b(INS\s*127|E127|ERYTHROSINE|RED\s*3)\b',
        "code": "INS 127",
        "name": "Erythrosine (Red 3)",
        "jurisdiction": "United States (FDA Cosmetics/Topicals Ban) / EU Restricted",
        "reason": "FDA restricted due to thyroid tumor risk in animal studies.",
        "risk_tier": "🔴 High Concern"
    },
    {
        "pattern": r'\b(INS\s*129|E129|ALLURA\s*RED|RED\s*40)\b',
        "code": "INS 129",
        "name": "Allura Red AC",
        "jurisdiction": "European Union (Mandatory Warning) / Denmark Banned",
        "reason": "Linked to bowel inflammation, hyperactivity, and allergic sensitivity.",
        "risk_tier": "🔴 High Concern"
    },
    {
        "pattern": r'\b(INS\s*133|E133|BRILLIANT\s*BLUE|BLUE\s*1)\b',
        "code": "INS 133",
        "name": "Brilliant Blue FCF",
        "jurisdiction": "European Union / Banned in France, Belgium, Switzerland",
        "reason": "Restricted in EU countries; neurotoxicity and cross-bloodbrain barrier concerns.",
        "risk_tier": "🔴 High Concern"
    },
    {
        "pattern": r'\b(INS\s*211|E211|SODIUM\s*BENZOATE)\b',
        "code": "INS 211",
        "name": "Sodium Benzoate",
        "jurisdiction": "European Union / Japan / UK FSA",
        "reason": "Forms carcinogenic Benzene when combined with Vitamin C (INS 300); ADHD trigger.",
        "risk_tier": "🟡 Moderate Concern"
    },
    {
        "pattern": r'\b(INS\s*621|E621|MSG|MONOSODIUM\s*GLUTAMATE|FLAVOUR\s*ENHANCER\s*\(?621\)?)\b',
        "code": "INS 621",
        "name": "Monosodium Glutamate (MSG)",
        "jurisdiction": "European Union (Strict Dose Limits & Labelling)",
        "reason": "Excitotoxin; linked to neuro-excitation, headaches, and metabolic dysfunction.",
        "risk_tier": "🟡 Moderate Concern"
    },
    {
        "pattern": r'\b(INS\s*150d|E150d|CARAMEL\s*IV|SULPHITE\s*AMMONIA\s*CARAMEL)\b',
        "code": "INS 150d",
        "name": "Caramel IV (Sulphite Ammonia Caramel)",
        "jurisdiction": "California Prop 65 / European Union",
        "reason": "Contains 4-MEI (4-methylimidazole), a listed carcinogen under CA Prop 65.",
        "risk_tier": "🟡 Moderate Concern"
    },
    {
        "pattern": r'\b(INS\s*202|E202|POTASSIUM\s*SORBATE)\b',
        "code": "INS 202",
        "name": "Potassium Sorbate",
        "jurisdiction": "European Union / Japan",
        "reason": "Mutagenic & genotoxic when mixed with nitrites; skin & mucous membrane irritant.",
        "risk_tier": "🟡 Moderate Concern"
    },
    {
        "pattern": r'\b(HYDROGENATED\s*OIL|HYDROGENATED\s*VEGETABLE\s*OIL|PARTIALLY\s*HYDROGENATED)\b',
        "code": "PHO",
        "name": "Hydrogenated / Partially Hydrogenated Oils",
        "jurisdiction": "United States (US FDA PHO Ban) / WHO Global Ban",
        "reason": "Primary source of industrial trans fats; strongly causes coronary heart disease.",
        "risk_tier": "🟡 Moderate Concern"
    }
]

def analyze_banned_additives(ingredients_text):
    if not isinstance(ingredients_text, str) or not ingredients_text.strip():
        return []
    
    found_bans = []
    for rule in BANNED_ADDITIVES_RULES:
        if re.search(rule["pattern"], ingredients_text, re.IGNORECASE):
            found_bans.append(rule)
    return found_bans

def main():
    print("=== GENERATING STRICTLY VERIFIED USER-REQUESTED DATABASE EXPORTS & BANNED ADDITIVE REPORTS ===")
    
    df_confirmed = pd.read_csv(confirmed_csv, dtype=str)
    df_needs_ver = pd.read_csv(needs_ver_csv, dtype=str)

    # Clean barcodes
    df_confirmed['barcode'] = df_confirmed['barcode'].str.strip()
    df_needs_ver['barcode'] = df_needs_ver['barcode'].str.strip()

    # STRICT VERIFIED FILTERING MASK
    has_ing = df_confirmed['ingredients_text'].notna() & (df_confirmed['ingredients_text'].str.strip() != '')
    not_unverified_text = ~df_confirmed['ingredients_text'].str.contains(r'Verify\s*specific|Verify\b|NON-FOOD', case=False, na=False)
    high_confidence = df_confirmed['ingredient_confidence'].isna() | (df_confirmed['ingredient_confidence'].str.upper() == 'HIGH')

    verified_mask = has_ing & not_unverified_text & high_confidence
    df_verified_complete = df_confirmed[verified_mask].copy()

    verified_count = len(df_verified_complete)
    print(f"1. Strictly Verified Complete Ingredients Products: {verified_count:,}")

    # 2. INCOMPLETE / UNVERIFIED PRODUCTS QUEUE
    df_unverified_from_confirmed = df_confirmed[~verified_mask].copy()
    df_incomplete_all = pd.concat([df_needs_ver, df_unverified_from_confirmed], ignore_index=True).drop_duplicates(subset=['barcode'])
    incomplete_count = len(df_incomplete_all)
    print(f"2. Total Incomplete / Pending Verification Products: {incomplete_count:,}")

    # 3. FOREIGN-BANNED / RESTRICTED ADDITIVES AUDIT (STRICTLY VERIFIED ONLY)
    print("\n3. Scanning Strictly Verified Products for Foreign-Banned & Restricted Additives...")
    banned_products = []
    
    for idx, row in df_verified_complete.iterrows():
        barcode = row.get('barcode', '')
        pname = row.get('product_name', '')
        brand = row.get('brands', '')
        ing = row.get('ingredients_text', '')

        bans = analyze_banned_additives(ing)
        if bans:
            highest_risk = "🟢 Low Concern"
            if any(b["risk_tier"] == "🔴 High Concern" for b in bans):
                highest_risk = "🔴 High Concern"
            elif any(b["risk_tier"] == "🟡 Moderate Concern" for b in bans):
                highest_risk = "🟡 Moderate Concern"

            for b in bans:
                banned_products.append({
                    "barcode": barcode,
                    "product_name": pname,
                    "brand": brand,
                    "ingredients_text": ing,
                    "additive_code": b["code"],
                    "additive_name": b["name"],
                    "jurisdiction": b["jurisdiction"],
                    "ban_reason": b["reason"],
                    "additive_risk_tier": b["risk_tier"],
                    "product_overall_risk": highest_risk
                })

    df_banned = pd.DataFrame(banned_products)
    total_banned_matches = len(df_banned)
    unique_banned_barcodes = df_banned['barcode'].nunique() if total_banned_matches > 0 else 0

    print(f"   -> Total Banned Additive Matches Found: {total_banned_matches}")
    print(f"   -> Unique Strictly Verified Products With Banned/Restricted Additives: {unique_banned_barcodes}")

    # Categorize Risk Levels among Verified Banned Products
    high_risk_df = df_banned[df_banned['additive_risk_tier'] == '🔴 High Concern'].drop_duplicates(subset=['barcode'])
    mod_risk_df = df_banned[df_banned['additive_risk_tier'] == '🟡 Moderate Concern'].drop_duplicates(subset=['barcode'])

    print(f"   -> High Concern Strictly Verified Products: {len(high_risk_df)}")
    print(f"   -> Moderate Concern Strictly Verified Products: {len(mod_risk_df)}")

    # SAVE REPORTS TO DISK & ARTIFACTS DIR
    output_dir = r"C:\Users\thout\.gemini\antigravity\brain\960ba3f1-e81d-4ac5-8649-b7de031c249a"
    
    # Save CSV files
    df_verified_complete[['barcode', 'product_name', 'brands', 'ingredients_text']].to_csv(
        os.path.join(output_dir, "verified_complete_ingredients_products.csv"), index=False
    )
    df_incomplete_all[['barcode', 'product_name', 'brands']].to_csv(
        os.path.join(output_dir, "incomplete_ingredients_products.csv"), index=False
    )
    df_banned.to_csv(
        os.path.join(output_dir, "foreign_banned_additives_full_report.csv"), index=False
    )

    print("Strictly verified user reports successfully written!")

if __name__ == '__main__':
    main()
