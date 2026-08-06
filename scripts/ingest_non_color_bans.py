import json
import os

MASTER_PATH = "src/data/global_additives_master.json"
SQL_OUTPUT_PATH = "supabase/migrations/20260806_non_color_bans.sql"

NON_COLOR_BANS = [
    {
        "code": "924a",
        "ins_code": "924a",
        "primary_name": "Potassium Bromate",
        "cas": "7758-01-2",
        "category": "FLOUR_TREATMENT_AGENT",
        "risk_level": "HIGH",
        "base_risk_weight": -20,
        "cspi_rating": "AVOID",
        "description": "Industrial flour bleaching and dough conditioning agent. Linked to kidney tumors, thyroid cancer, and genotoxicity in animal studies.",
        "regulatory_bans": [
            {"jurisdiction_code": "EU", "status": "BANNED", "regulation_ref": "EU Reg 1333/2008", "restriction_details": "Prohibited food additive due to carcinogenicity concerns."},
            {"jurisdiction_code": "IN", "status": "BANNED", "regulation_ref": "FSSAI Ban 2016", "restriction_details": "Banned in all bakery products by FSSAI in 2016."},
            {"jurisdiction_code": "US", "status": "RESTRICTED", "regulation_ref": "FDA 21 CFR 172.730", "restriction_details": "Allowed up to 50mg/kg in dough, but voluntary reduction requested."}
        ]
    },
    {
        "code": "927a",
        "ins_code": "927a",
        "primary_name": "Azodicarbonamide (ADA)",
        "cas": "123-77-3",
        "category": "FLOUR_TREATMENT_AGENT",
        "risk_level": "HIGH",
        "base_risk_weight": -18,
        "cspi_rating": "AVOID",
        "description": "Chemical foaming agent and dough conditioner. Degrades into semicarbazide (a carcinogen) during baking. Linked to occupational asthma.",
        "regulatory_bans": [
            {"jurisdiction_code": "EU", "status": "BANNED", "regulation_ref": "EU Directive 2004/1/EC", "restriction_details": "Banned as food additive due to respiratory asthma concerns."},
            {"jurisdiction_code": "UK", "status": "BANNED", "regulation_ref": "UK Food Additive Regs", "restriction_details": "Prohibited in dough treatment."},
            {"jurisdiction_code": "US", "status": "RESTRICTED", "regulation_ref": "FDA 21 CFR 172.806", "restriction_details": "Permitted up to 45 ppm."}
        ]
    },
    {
        "code": "917",
        "ins_code": "917",
        "primary_name": "Potassium Iodate",
        "cas": "7758-05-6",
        "category": "FLOUR_TREATMENT_AGENT",
        "risk_level": "HIGH",
        "base_risk_weight": -18,
        "cspi_rating": "AVOID",
        "description": "Flour treatment agent and dough conditioner. Linked to iodine toxicity, thyroid function disruption, and cell mutagenicity.",
        "regulatory_bans": [
            {"jurisdiction_code": "EU", "status": "BANNED", "regulation_ref": "EU Reg 1333/2008", "restriction_details": "Banned as dough conditioner/food additive in the EU."},
            {"jurisdiction_code": "IN", "status": "BANNED", "regulation_ref": "FSSAI 2016 Regulation", "restriction_details": "Prohibited in bread/bakery products by FSSAI."},
            {"jurisdiction_code": "US", "status": "RESTRICTED", "regulation_ref": "FDA 21 CFR 184.1635", "restriction_details": "Restricted to specified food uses."}
        ]
    },
    {
        "code": "443",
        "ins_code": "443",
        "primary_name": "Brominated Vegetable Oil (BVO)",
        "cas": "8016-94-2",
        "category": "EMULSIFIER",
        "risk_level": "HIGH",
        "base_risk_weight": -20,
        "cspi_rating": "AVOID",
        "description": "Plant-derived oil reacted with bromine. Accumulates in body fat and organs over time, linked to thyroid toxicity and neurological symptoms.",
        "regulatory_bans": [
            {"jurisdiction_code": "US", "status": "BANNED", "regulation_ref": "FDA Revocation 2024 (21 CFR 184)", "restriction_details": "FDA revoked authorization for use in food due to thyroid toxicity."},
            {"jurisdiction_code": "EU", "status": "BANNED", "regulation_ref": "EU Reg 1333/2008", "restriction_details": "Not authorized for food use in the European Union."},
            {"jurisdiction_code": "IN", "status": "BANNED", "regulation_ref": "FSSAI Prohibition Regulations", "restriction_details": "Prohibited in all beverage products."}
        ]
    },
    {
        "code": "320",
        "ins_code": "320",
        "primary_name": "Butylated Hydroxyanisole (BHA)",
        "cas": "25013-16-5",
        "category": "ANTIOXIDANT",
        "risk_level": "HIGH",
        "base_risk_weight": -10,
        "cspi_rating": "CAUTION",
        "description": "Synthetic antioxidant used to prevent fat rancidity. Classified as reasonably anticipated to be a human carcinogen by US NTP.",
        "regulatory_bans": [
            {"jurisdiction_code": "EU", "status": "RESTRICTED", "regulation_ref": "EU Reg 1333/2008", "restriction_details": "Restricted max limits; under review for endocrine disruption."},
            {"jurisdiction_code": "JP", "status": "RESTRICTED", "regulation_ref": "Japan Food Sanitation Act", "restriction_details": "Strictly limited to specified fats and oils."},
            {"jurisdiction_code": "US", "status": "RESTRICTED", "regulation_ref": "FDA 21 CFR 172.115", "restriction_details": "Max 0.02% of fat content."}
        ]
    },
    {
        "code": "321",
        "ins_code": "321",
        "primary_name": "Butylated Hydroxytoluene (BHT)",
        "cas": "128-37-0",
        "category": "ANTIOXIDANT",
        "risk_level": "MEDIUM",
        "base_risk_weight": -8,
        "cspi_rating": "CAUTION",
        "description": "Synthetic antioxidant closely related to BHA. Linked to liver damage, lung lesions, and suspected endocrine disrupting properties.",
        "regulatory_bans": [
            {"jurisdiction_code": "EU", "status": "RESTRICTED", "regulation_ref": "EU Reg 1333/2008", "restriction_details": "Restricted concentration limits in fats."},
            {"jurisdiction_code": "US", "status": "RESTRICTED", "regulation_ref": "FDA 21 CFR 172.115", "restriction_details": "Max 0.02% of fat content."}
        ]
    },
    {
        "code": "216",
        "ins_code": "216",
        "primary_name": "Propylparaben",
        "cas": "94-13-3",
        "category": "PRESERVATIVE",
        "risk_level": "HIGH",
        "base_risk_weight": -15,
        "cspi_rating": "AVOID",
        "description": "Preservative and antimicrobial agent. Shown to interfere with hormone levels and reproductive systems in laboratory animal models.",
        "regulatory_bans": [
            {"jurisdiction_code": "EU", "status": "BANNED", "regulation_ref": "Directive 2006/52/EC", "restriction_details": "Banned in EU foods due to endocrine disrupting effects."},
            {"jurisdiction_code": "IN", "status": "BANNED", "regulation_ref": "FSSAI Food Additive Schedule", "restriction_details": "Not permitted in Indian food products."},
            {"jurisdiction_code": "US", "status": "RESTRICTED", "regulation_ref": "FDA 21 CFR 184.1670", "restriction_details": "Generally recognized as safe but under review."}
        ]
    },
    {
        "code": "249",
        "ins_code": "249",
        "primary_name": "Potassium Nitrite",
        "cas": "7758-09-0",
        "category": "PRESERVATIVE",
        "risk_level": "HIGH",
        "base_risk_weight": -15,
        "cspi_rating": "AVOID",
        "description": "Curing agent and preservative. Reacts with secondary amines in meat to form carcinogenic nitrosamines during cooking.",
        "regulatory_bans": [
            {"jurisdiction_code": "EU", "status": "RESTRICTED", "regulation_ref": "EU Reg 1333/2008", "restriction_details": "Carcinogenicity risk via nitrosamine formation in meat products."},
            {"jurisdiction_code": "US", "status": "RESTRICTED", "regulation_ref": "FDA 21 CFR 172.160", "restriction_details": "Allowed strictly in cured meats under specific PPM limits."}
        ]
    },
    {
        "code": "250",
        "ins_code": "250",
        "primary_name": "Sodium Nitrite",
        "cas": "7632-00-0",
        "category": "PRESERVATIVE",
        "risk_level": "HIGH",
        "base_risk_weight": -15,
        "cspi_rating": "AVOID",
        "description": "Widely used meat curing preservative. Precursor to highly carcinogenic nitrosamines; associated with increased gastric cancer risk.",
        "regulatory_bans": [
            {"jurisdiction_code": "EU", "status": "RESTRICTED", "regulation_ref": "EU Reg 1333/2008", "restriction_details": "Carcinogenicity concerns; forming carcinogenic nitrosamines."},
            {"jurisdiction_code": "US", "status": "RESTRICTED", "regulation_ref": "FDA 21 CFR 172.170", "restriction_details": "Strictly limited in curing mixtures."}
        ]
    },
    {
        "code": "251",
        "ins_code": "251",
        "primary_name": "Sodium Nitrate",
        "cas": "7631-99-4",
        "category": "PRESERVATIVE",
        "risk_level": "HIGH",
        "base_risk_weight": -12,
        "cspi_rating": "AVOID",
        "description": "Preservative and color fixative in cured meats. Converts into nitrites in the body, leading to carcinogen formation.",
        "regulatory_bans": [
            {"jurisdiction_code": "EU", "status": "RESTRICTED", "regulation_ref": "EU Reg 1333/2008", "restriction_details": "Forms nitrites and carcinogenic nitrosamines in food."},
            {"jurisdiction_code": "US", "status": "RESTRICTED", "regulation_ref": "FDA 21 CFR 172.170", "restriction_details": "Strict limits applied."}
        ]
    },
    {
        "code": "252",
        "ins_code": "252",
        "primary_name": "Potassium Nitrate",
        "cas": "7757-79-1",
        "category": "PRESERVATIVE",
        "risk_level": "HIGH",
        "base_risk_weight": -12,
        "cspi_rating": "AVOID",
        "description": "Naturally occurring nitrate mineral preservative. Associated with blood disorders (methemoglobinemia) in infants, and cancer risk.",
        "regulatory_bans": [
            {"jurisdiction_code": "EU", "status": "RESTRICTED", "regulation_ref": "EU Reg 1333/2008", "restriction_details": "Precursor to carcinogenic nitrosamines."},
            {"jurisdiction_code": "US", "status": "RESTRICTED", "regulation_ref": "FDA 21 CFR 172.170", "restriction_details": "Strict limits in cured meats."}
        ]
    },
    {
        "code": "952",
        "ins_code": "952",
        "primary_name": "Cyclamic Acid & Cyclamates",
        "cas": "100-88-9",
        "category": "ARTIFICIAL_SWEETENER",
        "risk_level": "HIGH",
        "base_risk_weight": -15,
        "cspi_rating": "AVOID",
        "description": "Intense artificial sweetener. Banned in the US since 1969 due to laboratory animal bladder cancer studies.",
        "regulatory_bans": [
            {"jurisdiction_code": "US", "status": "BANNED", "regulation_ref": "FDA 21 CFR 189.135", "restriction_details": "Banned by US FDA since 1969 due to bladder tumor concerns."}
        ]
    },
    {
        "code": "951",
        "ins_code": "951",
        "primary_name": "Aspartame",
        "cas": "22839-47-0",
        "category": "ARTIFICIAL_SWEETENER",
        "risk_level": "HIGH",
        "base_risk_weight": -12,
        "cspi_rating": "CAUTION",
        "description": "Synthetic non-nutritive sweetener. Classified as possibly carcinogenic to humans (IARC Group 2B) in 2023.",
        "regulatory_bans": [
            {"jurisdiction_code": "CODEX", "status": "RESTRICTED", "regulation_ref": "WHO IARC Group 2B 2023", "restriction_details": "Classified as Possibly Carcinogenic to Humans (Group 2B) by WHO IARC in 2023."}
        ]
    },
    {
        "code": "956",
        "ins_code": "956",
        "primary_name": "Alitame",
        "cas": "80863-53-8",
        "category": "ARTIFICIAL_SWEETENER",
        "risk_level": "HIGH",
        "base_risk_weight": -15,
        "cspi_rating": "AVOID",
        "description": "Second-generation dipeptide artificial sweetener. Withdrawn or not authorized in many Western countries due to liver health questions.",
        "regulatory_bans": [
            {"jurisdiction_code": "US", "status": "RESTRICTED", "regulation_ref": "FDA Review Status", "restriction_details": "Not authorized / approved as a sweetener in the US."},
            {"jurisdiction_code": "EU", "status": "BANNED", "regulation_ref": "EU Reg 1333/2008", "restriction_details": "Withdrawn/not authorized for use in the EU."}
        ]
    },
    {
        "code": "954",
        "ins_code": "954",
        "primary_name": "Saccharin",
        "cas": "81-07-2",
        "category": "ARTIFICIAL_SWEETENER",
        "risk_level": "HIGH",
        "base_risk_weight": -15,
        "cspi_rating": "AVOID",
        "description": "One of the oldest synthetic sweeteners. Under observation for bladder irritation and tumor promotion risks.",
        "regulatory_bans": [
            {"jurisdiction_code": "US", "status": "RESTRICTED", "regulation_ref": "FDA 21 CFR 180.37", "restriction_details": "Allowed under strict concentration limits."},
            {"jurisdiction_code": "EU", "status": "RESTRICTED", "regulation_ref": "EU Reg 1333/2008", "restriction_details": "Strict category limits; under monitoring."}
        ]
    },
    {
        "code": "433",
        "ins_code": "433",
        "primary_name": "Polysorbate 80",
        "cas": "9005-65-6",
        "category": "EMULSIFIER",
        "risk_level": "MEDIUM",
        "base_risk_weight": -8,
        "cspi_rating": "CAUTION",
        "description": "Synthetic emulsifier. Linked to intestinal mucosal barrier disruption, low-grade inflammation, and gut microbiome dysbiosis.",
        "regulatory_bans": [
            {"jurisdiction_code": "US", "status": "RESTRICTED", "regulation_ref": "FDA 21 CFR 172.840", "restriction_details": "Restricted use levels; potential gut health risk."},
            {"jurisdiction_code": "EU", "status": "RESTRICTED", "regulation_ref": "EU Reg 1333/2008", "restriction_details": "Restricted under specified maximum levels."}
        ]
    },
    {
        "code": "435",
        "ins_code": "435",
        "primary_name": "Polysorbate 60",
        "cas": "9005-67-8",
        "category": "EMULSIFIER",
        "risk_level": "MEDIUM",
        "base_risk_weight": -8,
        "cspi_rating": "CAUTION",
        "description": "Synthetic surfactant emulsifier. Associated with gastrointestinal lining irritation and alteration of gut bacteria composition.",
        "regulatory_bans": [
            {"jurisdiction_code": "US", "status": "RESTRICTED", "regulation_ref": "FDA 21 CFR 172.836", "restriction_details": "Strict usage thresholds."},
            {"jurisdiction_code": "EU", "status": "RESTRICTED", "regulation_ref": "EU Reg 1333/2008", "restriction_details": "Restricted usage limits."}
        ]
    },
    {
        "code": "436",
        "ins_code": "436",
        "primary_name": "Polysorbate 65",
        "cas": "9005-71-4",
        "category": "EMULSIFIER",
        "risk_level": "MEDIUM",
        "base_risk_weight": -8,
        "cspi_rating": "CAUTION",
        "description": "Polyoxyethylene sorbitan emulsifier. Linked to metabolic syndrome and inflammatory bowel diseases in animal models.",
        "regulatory_bans": [
            {"jurisdiction_code": "US", "status": "RESTRICTED", "regulation_ref": "FDA 21 CFR 172.838", "restriction_details": "Restricted usage levels."},
            {"jurisdiction_code": "EU", "status": "RESTRICTED", "regulation_ref": "EU Reg 1333/2008", "restriction_details": "Restricted max limits."}
        ]
    },
    {
        "code": "olestra",
        "ins_code": "olestra",
        "primary_name": "Olestra",
        "cas": "118476-30-0",
        "category": "OTHER",
        "risk_level": "HIGH",
        "base_risk_weight": -20,
        "cspi_rating": "AVOID",
        "description": "Zero-calorie synthetic fat substitute. Inhibits absorption of fat-soluble vitamins (A, D, E, K) and carotenoids. Linked to severe cramping.",
        "regulatory_bans": [
            {"jurisdiction_code": "US", "status": "RESTRICTED", "regulation_ref": "FDA 21 CFR 172.867", "restriction_details": "FDA approved but carries warnings of gastrointestinal distress and vitamin depletion."},
            {"jurisdiction_code": "EU", "status": "BANNED", "regulation_ref": "EU Reg 1333/2008", "restriction_details": "Not authorized / banned for use in the EU."}
        ]
    },
    {
        "code": "degme",
        "ins_code": "degme",
        "primary_name": "Diethylene Glycol Monoethyl Ether",
        "cas": "111-90-0",
        "category": "OTHER",
        "risk_level": "HIGH",
        "base_risk_weight": -20,
        "cspi_rating": "AVOID",
        "description": "Synthetic solvent and carrier agent. Suspected kidney/renal and central nervous system toxicant at elevated levels.",
        "regulatory_bans": [
            {"jurisdiction_code": "US", "status": "RESTRICTED", "regulation_ref": "FDA 21 CFR 172.712", "restriction_details": "Permitted only as solvent/carrier under strict limits."},
            {"jurisdiction_code": "EU", "status": "BANNED", "regulation_ref": "EU Reg 1333/2008", "restriction_details": "Not authorized for food use in the EU."}
        ]
    }
]

def run_ingestion():
    print("Fetching existing master database...")
    with open(MASTER_PATH, "r", encoding="utf-8") as f:
        master_data = json.load(f)

    updated_count = 0
    sql_statements = []

    # Add header/schema-agnostic wrapper checks for Supabase executing migrations
    sql_statements.append("BEGIN;")

    for item in NON_COLOR_BANS:
        code = item["code"]
        if code not in master_data:
            master_data[code] = {
                "id": f"ing_{item['ins_code']}",
                "ins_code": item["ins_code"],
                "e_number": f"E{item['ins_code'].upper()}" if not item["ins_code"].isalpha() else item["ins_code"],
                "cas_number": item["cas"],
                "primary_name": item["primary_name"],
                "category": item["category"],
                "risk_level": item["risk_level"],
                "base_risk_weight": item["base_risk_weight"],
                "cspi_rating": item["cspi_rating"],
                "regulatory_bans": item["regulatory_bans"],
                "description": item["description"],
                "synonyms": [item["primary_name"].lower(), f"ins {item['ins_code']}", f"e{item['ins_code']}".lower()]
            }
        else:
            master_data[code]["regulatory_bans"] = item["regulatory_bans"]
            master_data[code]["risk_level"] = item["risk_level"]
            master_data[code]["cas_number"] = item["cas"]
            master_data[code]["cspi_rating"] = item["cspi_rating"]
            master_data[code]["description"] = item["description"]
        
        updated_count += 1

        # 1. Seeds for decoupled tables (canonical_additives, regulatory_bans)
        ins_val = item['ins_code']
        e_val = f"E{item['ins_code'].upper()}" if not item['ins_code'].isalpha() else ""
        sql_statements.append(f"""
INSERT INTO canonical_additives (id, ins_code, e_number, cas_number, primary_name, category, risk_level, base_risk_weight, cspi_rating, description)
VALUES ('ing_{item['ins_code']}', '{ins_val}', '{e_val}', '{item['cas']}', '{item['primary_name']}', '{item['category']}', '{item['risk_level']}', {item['base_risk_weight']}, '{item['cspi_rating']}', '{item['description'].replace("'", "''")}')
ON CONFLICT (id) DO UPDATE SET risk_level = EXCLUDED.risk_level, cspi_rating = EXCLUDED.cspi_rating;
""".strip())

        # Synonyms insert for decoupled index
        sql_statements.append(f"""
INSERT INTO additive_synonyms (additive_id, synonym_clean, language_code, is_primary)
VALUES ('ing_{item['ins_code']}', '{item['primary_name'].lower()}', 'en', TRUE)
ON CONFLICT DO NOTHING;
""".strip())

        for ban in item["regulatory_bans"]:
            sql_statements.append(f"""
INSERT INTO regulatory_bans (additive_id, jurisdiction_code, status, restriction_details, regulation_ref)
VALUES ('ing_{item['ins_code']}', '{ban['jurisdiction_code']}', '{ban['status']}', '{ban['restriction_details'].replace("'", "''")}', '{ban['regulation_ref'].replace("'", "''")}')
ON CONFLICT (additive_id, jurisdiction_code, scope_category) DO NOTHING;
""".strip())

        # 2. Seeds for legacy tables (additive_reference, additive_rulebook)
        fssai_status = next((b["status"] for b in item["regulatory_bans"] if b["jurisdiction_code"] == "IN"), "RESTRICTED")
        efsa_status = next((b["status"] for b in item["regulatory_bans"] if b["jurisdiction_code"] == "EU"), "RESTRICTED")
        fda_status = next((b["status"] for b in item["regulatory_bans"] if b["jurisdiction_code"] == "US"), "RESTRICTED")
        sql_statements.append(f"""
INSERT INTO additive_reference (ins_code, common_name, origin, category, fssai_status, efsa_status, fda_status, adi_value, concern_level, accurate_description, source_url, source_citation)
VALUES ('{item['ins_code']}', '{item['primary_name']}', 'synthetic', '{item['category']}', '{fssai_status}', '{efsa_status}', '{fda_status}', '0-5 mg/kg body weight', '{item['risk_level']}', '{item['description'].replace("'", "''")}', 'https://www.fssai.gov.in', 'Official Safety Evaluation')
ON CONFLICT (ins_code) DO UPDATE SET concern_level = EXCLUDED.concern_level, accurate_description = EXCLUDED.accurate_description;
""".strip())

        for ban in item["regulatory_bans"]:
            legacy_code = f"E{item['ins_code'].upper()}" if not item['ins_code'].isalpha() else item['ins_code'].upper()
            sql_statements.append(f"""
INSERT INTO additive_rulebook (additive_code, ins_number, canonical_name, functional_class, jurisdiction, status, label_requirement, regulation_title)
VALUES ('{legacy_code}', '{item['ins_code']}', '{item['primary_name']}', '{item['category']}', '{ban['jurisdiction_code']}', '{ban['status']}', '{ban['restriction_details'].replace("'", "''")}', '{ban['regulation_ref'].replace("'", "''")}')
ON CONFLICT DO NOTHING;
""".strip())

    sql_statements.append("COMMIT;")
    print(f"Enriched {updated_count} high-priority non-color additive entries.")

    with open(MASTER_PATH, "w", encoding="utf-8") as f:
        json.dump(master_data, f, indent=2, ensure_ascii=False)

    os.makedirs(os.path.dirname(SQL_OUTPUT_PATH), exist_ok=True)
    with open(SQL_OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(sql_statements))

    print(f"Master database updated at {MASTER_PATH}")
    print(f"SQL migration generated at {SQL_OUTPUT_PATH}")

if __name__ == "__main__":
    run_ingestion()
