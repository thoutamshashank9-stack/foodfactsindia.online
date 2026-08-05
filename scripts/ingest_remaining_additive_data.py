import json
import urllib.request
import os

MASTER_PATH = "src/data/global_additives_master.json"
SQL_OUTPUT_PATH = "supabase/seed_non_color_bans.sql"
OFF_INGREDIENTS_URL = "https://static.openfoodfacts.org/data/taxonomies/ingredients.json"

# 1. Comprehensive Non-Color Additive & Industrial Chemical Ban Master Matrix
NON_COLOR_BANS = [
    {
        "code": "e924a",
        "ins_code": "924a",
        "primary_name": "Potassium Bromate",
        "cas": "7758-01-2",
        "category": "FLOUR_TREATMENT_AGENT",
        "risk_level": "HIGH",
        "base_risk_weight": -20,
        "cspi_rating": "AVOID",
        "regulatory_bans": [
            {"jurisdiction_code": "EU", "status": "BANNED", "regulation_ref": "EU Reg 1333/2008", "restriction_details": "Prohibited food additive due to carcinogenicity concerns."},
            {"jurisdiction_code": "IN", "status": "BANNED", "regulation_ref": "FSSAI Ban 2016", "restriction_details": "Banned in all bakery products by FSSAI in 2016."},
            {"jurisdiction_code": "US", "status": "RESTRICTED", "regulation_ref": "FDA 21 CFR 172.730", "restriction_details": "Allowed up to 50mg/kg in dough, but voluntary reduction requested."}
        ]
    },
    {
        "code": "e443",
        "ins_code": "443",
        "primary_name": "Brominated Vegetable Oil (BVO)",
        "cas": "8016-94-2",
        "category": "EMULSIFIER",
        "risk_level": "HIGH",
        "base_risk_weight": -20,
        "cspi_rating": "AVOID",
        "regulatory_bans": [
            {"jurisdiction_code": "US", "status": "BANNED", "regulation_ref": "FDA Revocation 2024 (21 CFR 184)", "restriction_details": "FDA revoked authorization for use in food due to thyroid toxicity."},
            {"jurisdiction_code": "EU", "status": "BANNED", "regulation_ref": "EU Reg 1333/2008", "restriction_details": "Not authorized for food use in the European Union."},
            {"jurisdiction_code": "IN", "status": "BANNED", "regulation_ref": "FSSAI Prohibition Regulations", "restriction_details": "Prohibited in all beverage products."}
        ]
    },
    {
        "code": "e320",
        "ins_code": "320",
        "primary_name": "Butylated Hydroxyanisole (BHA)",
        "cas": "25013-16-5",
        "category": "ANTIOXIDANT",
        "risk_level": "HIGH",
        "base_risk_weight": -10,
        "cspi_rating": "CAUTION",
        "regulatory_bans": [
            {"jurisdiction_code": "EU", "status": "RESTRICTED", "regulation_ref": "EU Reg 1333/2008", "restriction_details": "Restricted max limits; under review for endocrine disruption."},
            {"jurisdiction_code": "JP", "status": "RESTRICTED", "regulation_ref": "Japan Food Sanitation Act", "restriction_details": "Strictly limited to specified fats and oils."}
        ]
    },
    {
        "code": "e321",
        "ins_code": "321",
        "primary_name": "Butylated Hydroxytoluene (BHT)",
        "cas": "128-37-0",
        "category": "ANTIOXIDANT",
        "risk_level": "MEDIUM",
        "base_risk_weight": -8,
        "cspi_rating": "CAUTION",
        "regulatory_bans": [
            {"jurisdiction_code": "EU", "status": "RESTRICTED", "regulation_ref": "EU Reg 1333/2008", "restriction_details": "Restricted concentration limits in fats."},
            {"jurisdiction_code": "US", "status": "RESTRICTED", "regulation_ref": "FDA 21 CFR 172.115", "restriction_details": "Max 0.02% of fat content."}
        ]
    },
    {
        "code": "e952",
        "ins_code": "952",
        "primary_name": "Cyclamic Acid & Cyclamates",
        "cas": "100-88-9",
        "category": "ARTIFICIAL_SWEETENER",
        "risk_level": "HIGH",
        "base_risk_weight": -15,
        "cspi_rating": "AVOID",
        "regulatory_bans": [
            {"jurisdiction_code": "US", "status": "BANNED", "regulation_ref": "FDA 21 CFR 189.135", "restriction_details": "Banned by US FDA since 1969 due to bladder tumor concerns in animal studies."}
        ]
    },
    {
        "code": "e927a",
        "ins_code": "927a",
        "primary_name": "Azodicarbonamide (ADA)",
        "cas": "123-77-3",
        "category": "FLOUR_TREATMENT_AGENT",
        "risk_level": "HIGH",
        "base_risk_weight": -18,
        "cspi_rating": "AVOID",
        "regulatory_bans": [
            {"jurisdiction_code": "EU", "status": "BANNED", "regulation_ref": "EU Directive 2004/1/EC", "restriction_details": "Banned as food additive due to respiratory asthma concerns."},
            {"jurisdiction_code": "UK", "status": "BANNED", "regulation_ref": "UK Food Additive Regs", "restriction_details": "Prohibited in dough treatment."},
            {"jurisdiction_code": "US", "status": "RESTRICTED", "regulation_ref": "FDA 21 CFR 172.806", "restriction_details": "Permitted up to 45 ppm."}
        ]
    },
    {
        "code": "e216",
        "ins_code": "216",
        "primary_name": "Propylparaben (Propyl p-hydroxybenzoate)",
        "cas": "94-13-3",
        "category": "PRESERVATIVE",
        "risk_level": "HIGH",
        "base_risk_weight": -15,
        "cspi_rating": "AVOID",
        "regulatory_bans": [
            {"jurisdiction_code": "EU", "status": "BANNED", "regulation_ref": "Directive 2006/52/EC", "restriction_details": "Banned in EU foods due to endocrine disrupting effects on sperm counts and testosterone."}
        ]
    },
    {
        "code": "e951",
        "ins_code": "951",
        "primary_name": "Aspartame",
        "cas": "22839-47-0",
        "category": "ARTIFICIAL_SWEETENER",
        "risk_level": "HIGH",
        "base_risk_weight": -12,
        "cspi_rating": "CAUTION",
        "regulatory_bans": [
            {"jurisdiction_code": "CODEX", "status": "RESTRICTED", "regulation_ref": "WHO IARC Group 2B 2023", "restriction_details": "Classified as Possibly Carcinogenic to Humans (Group 2B) by WHO IARC in 2023."}
        ]
    }
]

def run_ingestion():
    print("1. Fetching existing master global additives database...")
    with open(MASTER_PATH, "r", encoding="utf-8") as f:
        master_data = json.load(f)

    updated_count = 0
    sql_statements = []

    for item in NON_COLOR_BANS:
        code = item["code"]
        if code not in master_data:
            master_data[code] = {
                "id": f"ing_{item['ins_code']}",
                "ins_code": item["ins_code"],
                "e_number": f"E{item['ins_code'].upper()}",
                "cas_number": item["cas"],
                "primary_name": item["primary_name"],
                "category": item["category"],
                "risk_level": item["risk_level"],
                "base_risk_weight": item["base_risk_weight"],
                "cspi_rating": item["cspi_rating"],
                "regulatory_bans": item["regulatory_bans"],
                "synonyms": [item["primary_name"].lower(), f"ins {item['ins_code']}", f"e{item['ins_code']}"]
            }
        else:
            master_data[code]["regulatory_bans"] = item["regulatory_bans"]
            master_data[code]["risk_level"] = item["risk_level"]
            master_data[code]["cas_number"] = item["cas"]
            master_data[code]["cspi_rating"] = item["cspi_rating"]
        
        updated_count += 1

        # Build SQL seed inserts
        for ban in item["regulatory_bans"]:
            sql = f"""INSERT INTO regulatory_bans (additive_id, jurisdiction_code, status, restriction_details, regulation_ref) VALUES ('ing_{item['ins_code']}', '{ban['jurisdiction_code']}', '{ban['status']}', '{ban['restriction_details']}', '{ban['regulation_ref']}') ON CONFLICT DO NOTHING;"""
            sql_statements.append(sql)

    print(f"Enriched {updated_count} high-priority non-color additive entries.")

    with open(MASTER_PATH, "w", encoding="utf-8") as f:
        json.dump(master_data, f, indent=2, ensure_ascii=False)

    os.makedirs(os.path.dirname(SQL_OUTPUT_PATH), exist_ok=True)
    with open(SQL_OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(sql_statements))

    print(f"Master database updated at {MASTER_PATH}")
    print(f"SQL migration generated at {SQL_OUTPUT_PATH}")

    # 2. Ingest Open Food Facts Raw Ingredients Taxonomy
    print("2. Downloading Open Food Facts Raw Ingredients Taxonomy (Phase 3)...")
    req = urllib.request.Request(OFF_INGREDIENTS_URL, headers={"User-Agent": "FoodFactsIndia-IngestionEngine/1.0"})
    try:
        with urllib.request.urlopen(req) as resp:
            ing_data = json.loads(resp.read().decode())
            print(f"Successfully fetched {len(ing_data)} raw ingredient taxonomy items!")
            raw_out_path = "src/data/raw_ingredients_taxonomy.json"
            
            clean_raw = {}
            for key, val in ing_data.items():
                if isinstance(val, dict):
                    name_obj = val.get("name", {})
                    primary = name_obj.get("en") if isinstance(name_obj, dict) else str(name_obj)
                    clean_key = key.replace("en:", "").strip().lower()
                    if primary:
                        clean_raw[clean_key] = {
                            "id": f"ing_raw_{clean_key}",
                            "canonical_name": primary,
                            "category": "WHOLE_FOOD",
                            "synonyms": list(name_obj.values()) if isinstance(name_obj, dict) else [primary]
                        }

            with open(raw_out_path, "w", encoding="utf-8") as rf:
                json.dump(clean_raw, rf, indent=2, ensure_ascii=False)
            print(f"Raw ingredients taxonomy saved to {raw_out_path} ({len(clean_raw)} entities processed)!")
    except Exception as e:
        print("Error downloading OFF raw ingredients taxonomy:", e)

if __name__ == "__main__":
    run_ingestion()
