import urllib.request
import json
import os
import re

OFF_ADDITIVES_URL = "https://static.openfoodfacts.org/data/taxonomies/additives.json"

# Master Evidence-Grade Regulatory Database
REGULATORY_BANS_MASTER = {
    "122": {
        "cas": "3567-69-9",
        "ci": "CI 14720",
        "name": "Azorubine (Carmoisine)",
        "fdc_name": "Carmoisine / Food Red 3",
        "cspi": "AVOID",
        "risk": "HIGH",
        "category": "ARTIFICIAL_COLOR",
        "description": "Synthetic red azo dye derived from coal tar or petroleum.",
        "bans": [
            {"jurisdiction": "US", "status": "BANNED", "scope": "ALL", "ref": "21 CFR Part 74", "details": "Not authorized for food use in the United States by FDA."},
            {"jurisdiction": "JP", "status": "BANNED", "scope": "ALL", "ref": "Japan Food Sanitation Act", "details": "Prohibited from food products in Japan."},
            {"jurisdiction": "EU", "status": "RESTRICTED", "scope": "ALL", "ref": "Reg (EC) No 1333/2008 Annex V", "warning": "May have an adverse effect on activity and attention in children."},
            {"jurisdiction": "UK", "status": "RESTRICTED", "scope": "ALL", "ref": "UK Food Labelling Regs Annex V", "warning": "May have an adverse effect on activity and attention in children."},
            {"jurisdiction": "IN", "status": "RESTRICTED", "scope": "CONFECTIONERY_BEVERAGES", "max_limit_mg_kg": 100, "ref": "FSSAI Schedule 2.4.5", "details": "Maximum permitted limit 100 mg/kg."}
        ],
        "pmid": "17825405",
        "doi": "10.1016/S0140-6736(07)61306-3"
    },
    "127": {
        "cas": "16423-68-0",
        "ci": "CI 45430",
        "name": "Erythrosine",
        "fdc_name": "FD&C Red No. 3",
        "cspi": "AVOID",
        "risk": "HIGH",
        "category": "ARTIFICIAL_COLOR",
        "description": "Organoiodine compound dye linked to thyroid tumors in animal studies.",
        "bans": [
            {"jurisdiction": "US", "status": "BANNED", "scope": "COSMETICS_EXTERNAL", "ref": "21 CFR Part 81", "details": "FDA revoked provisional listing for cosmetics and topical drugs due to carcinogenicity."},
            {"jurisdiction": "EU", "status": "RESTRICTED", "scope": "MARASCHINO_CHERRIES_ONLY", "ref": "Reg (EC) No 1333/2008", "details": "Prohibited in all foods except cocktail cherries."},
            {"jurisdiction": "IN", "status": "RESTRICTED", "scope": "FOOD", "max_limit_mg_kg": 100, "ref": "FSSAI Schedule 2.4.5", "details": "Permitted up to 100 mg/kg."}
        ],
        "pmid": "2148151",
        "doi": "10.1016/0272-0590(90)90045-O"
    },
    "171": {
        "cas": "13463-67-7",
        "ci": "CI 77891",
        "name": "Titanium Dioxide",
        "fdc_name": "Pigment White 6",
        "cspi": "AVOID",
        "risk": "HIGH",
        "category": "ARTIFICIAL_COLOR",
        "description": "White opacity pigment banned in the EU due to genotoxicity and DNA damage concerns.",
        "bans": [
            {"jurisdiction": "EU", "status": "BANNED", "scope": "ALL", "ref": "Regulation (EU) 2022/617", "details": "EU authorization revoked following EFSA 2021 genotoxicity evaluation."},
            {"jurisdiction": "US", "status": "RESTRICTED", "scope": "ALL", "max_limit_mg_kg": 10000, "ref": "21 CFR 73.575", "details": "FDA permits up to 1% by weight."},
            {"jurisdiction": "IN", "status": "APPROVED", "scope": "ALL", "ref": "FSSAI Standards 2011", "details": "Permitted white opacifier."}
        ],
        "pmid": "33956423",
        "doi": "10.2903/j.efsa.2021.6585"
    },
    "102": {
        "cas": "1934-21-0",
        "ci": "CI 19140",
        "name": "Tartrazine",
        "fdc_name": "FD&C Yellow No. 5",
        "cspi": "CAUTION",
        "risk": "HIGH",
        "category": "ARTIFICIAL_COLOR",
        "description": "Lemon yellow azo dye known to trigger severe allergic reactions and hyperactivity in sensitive individuals.",
        "bans": [
            {"jurisdiction": "EU", "status": "RESTRICTED", "scope": "ALL", "ref": "Reg (EC) No 1333/2008 Annex V", "warning": "May have an adverse effect on activity and attention in children."},
            {"jurisdiction": "UK", "status": "RESTRICTED", "scope": "ALL", "ref": "UK Food Labelling Regs Annex V", "warning": "May have an adverse effect on activity and attention in children."},
            {"jurisdiction": "US", "status": "RESTRICTED", "scope": "ALL", "ref": "21 CFR 74.705", "details": "Requires explicit label declaration due to asthma/urticaria hypersensitivity."},
            {"jurisdiction": "IN", "status": "RESTRICTED", "scope": "FOOD", "max_limit_mg_kg": 100, "ref": "FSSAI Schedule 2.4.5"}
        ],
        "pmid": "17825405",
        "doi": "10.1016/S0140-6736(07)61306-3"
    },
    "110": {
        "cas": "2783-94-0",
        "ci": "CI 15985",
        "name": "Sunset Yellow FCF",
        "fdc_name": "FD&C Yellow No. 6",
        "cspi": "CAUTION",
        "risk": "HIGH",
        "category": "ARTIFICIAL_COLOR",
        "description": "Petroleum-derived orange-yellow azo dye included in the Southampton Six study.",
        "bans": [
            {"jurisdiction": "EU", "status": "RESTRICTED", "scope": "ALL", "ref": "Reg (EC) No 1333/2008 Annex V", "warning": "May have an adverse effect on activity and attention in children."},
            {"jurisdiction": "US", "status": "APPROVED", "scope": "ALL", "ref": "21 CFR 74.706"},
            {"jurisdiction": "IN", "status": "RESTRICTED", "scope": "FOOD", "max_limit_mg_kg": 100, "ref": "FSSAI Schedule 2.4.5"}
        ],
        "pmid": "17825405",
        "doi": "10.1016/S0140-6736(07)61306-3"
    },
    "123": {
        "cas": "915-67-3",
        "ci": "CI 16185",
        "name": "Amaranth",
        "fdc_name": "FD&C Red No. 2",
        "cspi": "AVOID",
        "risk": "HIGH",
        "category": "ARTIFICIAL_COLOR",
        "description": "Dark red azo dye banned in the US since 1976 due to carcinogenic concerns.",
        "bans": [
            {"jurisdiction": "US", "status": "BANNED", "scope": "ALL", "ref": "21 CFR Part 81", "details": "FDA terminated provisional listing in 1976 due to birth defect and tumor risks."},
            {"jurisdiction": "EU", "status": "RESTRICTED", "scope": "CAVIAR_FISH_ROE", "ref": "Reg (EC) No 1333/2008", "details": "Strictly restricted to fish roe."},
            {"jurisdiction": "IN", "status": "BANNED", "scope": "ALL", "ref": "FSSAI Food Regulations 2011", "details": "Excluded from FSSAI permitted colors list."}
        ],
        "pmid": "771408",
        "doi": "10.1016/0015-6264(76)90342-9"
    },
    "124": {
        "cas": "2611-82-7",
        "ci": "CI 16255",
        "name": "Ponceau 4R",
        "fdc_name": "Cochineal Red A / Food Red 7",
        "cspi": "AVOID",
        "risk": "HIGH",
        "category": "ARTIFICIAL_COLOR",
        "description": "Strawberry red azo dye prohibited in the United States and Norway.",
        "bans": [
            {"jurisdiction": "US", "status": "BANNED", "scope": "ALL", "ref": "21 CFR Part 74", "details": "Not authorized for food use by FDA."},
            {"jurisdiction": "EU", "status": "RESTRICTED", "scope": "ALL", "ref": "Reg (EC) No 1333/2008 Annex V", "warning": "May have an adverse effect on activity and attention in children."},
            {"jurisdiction": "IN", "status": "RESTRICTED", "scope": "FOOD", "max_limit_mg_kg": 100, "ref": "FSSAI Schedule 2.4.5"}
        ],
        "pmid": "17825405",
        "doi": "10.1016/S0140-6736(07)61306-3"
    },
    "129": {
        "cas": "25956-17-6",
        "ci": "CI 16035",
        "name": "Allura Red AC",
        "fdc_name": "FD&C Red No. 40",
        "cspi": "CAUTION",
        "risk": "HIGH",
        "category": "ARTIFICIAL_COLOR",
        "description": "Widely used synthetic red colorant associated with behavioral changes in children.",
        "bans": [
            {"jurisdiction": "EU", "status": "RESTRICTED", "scope": "ALL", "ref": "Reg (EC) No 1333/2008 Annex V", "warning": "May have an adverse effect on activity and attention in children."},
            {"jurisdiction": "US", "status": "APPROVED", "scope": "ALL", "ref": "21 CFR 74.340"},
            {"jurisdiction": "IN", "status": "RESTRICTED", "scope": "FOOD", "max_limit_mg_kg": 100, "ref": "FSSAI Schedule 2.4.5"}
        ],
        "pmid": "17825405",
        "doi": "10.1016/S0140-6736(07)61306-3"
    },
    "131": {
        "cas": "3536-49-0",
        "ci": "CI 42051",
        "name": "Patent Blue V",
        "fdc_name": "Food Blue 5",
        "cspi": "AVOID",
        "risk": "HIGH",
        "category": "ARTIFICIAL_COLOR",
        "description": "Dark blue synthetic dye banned in the US, Australia, and Japan due to severe allergic risks.",
        "bans": [
            {"jurisdiction": "US", "status": "BANNED", "scope": "ALL", "ref": "21 CFR Part 74", "details": "Unapproved in the US."},
            {"jurisdiction": "JP", "status": "BANNED", "scope": "ALL", "ref": "Japan Food Sanitation Act", "details": "Prohibited in Japan."},
            {"jurisdiction": "EU", "status": "RESTRICTED", "scope": "ALL", "ref": "Reg (EC) No 1333/2008", "details": "Restricted max limits."}
        ],
        "pmid": "1468267",
        "doi": "10.1016/0015-6264(92)90001-A"
    },
    "133": {
        "cas": "3844-45-9",
        "ci": "CI 42090",
        "name": "Brilliant Blue FCF",
        "fdc_name": "FD&C Blue No. 1",
        "cspi": "CAUTION",
        "risk": "MEDIUM",
        "category": "ARTIFICIAL_COLOR",
        "description": "Synthetic triarylmethane blue dye.",
        "bans": [
            {"jurisdiction": "US", "status": "APPROVED", "scope": "ALL", "ref": "21 CFR 74.101"},
            {"jurisdiction": "EU", "status": "APPROVED", "scope": "ALL", "ref": "Reg (EC) No 1333/2008"},
            {"jurisdiction": "IN", "status": "RESTRICTED", "scope": "FOOD", "max_limit_mg_kg": 100, "ref": "FSSAI Schedule 2.4.5"}
        ],
        "pmid": "12879417",
        "doi": "10.1016/S0278-6915(03)00078-4"
    }
}

def fetch_off_additives():
    print("Downloading Open Food Facts official additives taxonomy (905 KB)...")
    req = urllib.request.Request(OFF_ADDITIVES_URL, headers={"User-Agent": "FoodFactsIndia-IngestionEngine/1.0"})
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            print(f"Successfully fetched {len(data)} taxonomy entries from Open Food Facts!")
            return data
    except Exception as e:
        print("Error downloading OFF taxonomy:", e)
        return {}

def process_and_merge():
    off_data = fetch_off_additives()
    master_additives = {}

    count = 0
    for key, item in off_data.items():
        if not isinstance(item, dict):
            continue
        
        clean_code = key.replace("en:", "").replace("e", "").strip().lower()
        if not clean_code:
            continue

        name_obj = item.get("name", {})
        primary_name = name_obj.get("en") if isinstance(name_obj, dict) else str(name_obj)
        if not primary_name or primary_name.startswith("e") and primary_name[1:].isdigit():
            primary_name = f"Additive INS {clean_code.upper()}"

        wikidata_id = item.get("wikidata", {}).get("en") if isinstance(item.get("wikidata"), dict) else None
        
        synonyms = set()
        if isinstance(name_obj, dict):
            for lang, val in name_obj.items():
                if isinstance(val, str) and len(val) > 1:
                    synonyms.add(val.lower())

        master_additives[clean_code] = {
            "id": f"ing_e{clean_code}",
            "ins_code": clean_code,
            "e_number": f"E{clean_code.upper()}",
            "primary_name": primary_name,
            "wikidata_id": wikidata_id,
            "synonyms": list(synonyms)
        }
        count += 1

    print(f"Parsed {count} taxonomy entries from Open Food Facts.")

    # Overlay evidence-grade regulatory & toxicological master records
    print("Enriching with US FDA 21 CFR, EU EFSA Reg 1333/2008, Japan MHLW, FSSAI Schedule 2.4.5, and PubChem CAS numbers...")
    for code, reg_info in REGULATORY_BANS_MASTER.items():
        clean_code = code.lower()
        existing = master_additives.get(clean_code, {
            "id": f"ing_e{clean_code}",
            "ins_code": clean_code,
            "e_number": f"E{clean_code.upper()}",
            "primary_name": reg_info["name"],
            "synonyms": []
        })

        existing["cas_number"] = reg_info.get("cas")
        existing["ci_number"] = reg_info.get("ci")
        existing["primary_name"] = reg_info["name"]
        existing["fdc_name"] = reg_info.get("fdc_name")
        existing["cspi_rating"] = reg_info.get("cspi")
        existing["risk_level"] = reg_info.get("risk")
        existing["category"] = reg_info.get("category")
        existing["description"] = reg_info.get("description")
        existing["regulatory_bans"] = reg_info.get("bans", [])
        existing["pmid"] = reg_info.get("pmid")
        existing["doi"] = reg_info.get("doi")

        existing_syns = set(existing.get("synonyms", []))
        existing_syns.add(reg_info["name"].lower())
        if reg_info.get("fdc_name"):
            existing_syns.add(reg_info["fdc_name"].lower())
        existing_syns.add(f"ins {clean_code}")
        existing_syns.add(f"e{clean_code}")
        existing["synonyms"] = list(existing_syns)

        master_additives[clean_code] = existing

    # Write output to src/data/global_additives_master.json
    out_dir = os.path.join(os.path.dirname(__file__), "..", "src", "data")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "global_additives_master.json")

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(master_additives, f, indent=2, ensure_ascii=False)

    print(f"Master Global Additives Dataset written to {out_path} ({len(master_additives)} total additives ingested & enriched)!")

if __name__ == "__main__":
    process_and_merge()
