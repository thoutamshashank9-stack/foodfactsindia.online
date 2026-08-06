BEGIN;
INSERT INTO canonical_additives (id, ins_code, e_number, cas_number, primary_name, category, risk_level, base_risk_weight, cspi_rating, description)
VALUES ('ing_924a', '924a', 'E924A', '7758-01-2', 'Potassium Bromate', 'FLOUR_TREATMENT_AGENT', 'HIGH', -20, 'AVOID', 'Industrial flour bleaching and dough conditioning agent. Linked to kidney tumors, thyroid cancer, and genotoxicity in animal studies.')
ON CONFLICT (id) DO UPDATE SET risk_level = EXCLUDED.risk_level, cspi_rating = EXCLUDED.cspi_rating;
INSERT INTO additive_synonyms (additive_id, synonym_clean, language_code, is_primary)
VALUES ('ing_924a', 'potassium bromate', 'en', TRUE)
ON CONFLICT DO NOTHING;
INSERT INTO regulatory_bans (additive_id, jurisdiction_code, status, restriction_details, regulation_ref)
VALUES ('ing_924a', 'EU', 'BANNED', 'Prohibited food additive due to carcinogenicity concerns.', 'EU Reg 1333/2008')
ON CONFLICT (additive_id, jurisdiction_code, scope_category) DO NOTHING;
INSERT INTO regulatory_bans (additive_id, jurisdiction_code, status, restriction_details, regulation_ref)
VALUES ('ing_924a', 'IN', 'BANNED', 'Banned in all bakery products by FSSAI in 2016.', 'FSSAI Ban 2016')
ON CONFLICT (additive_id, jurisdiction_code, scope_category) DO NOTHING;
INSERT INTO regulatory_bans (additive_id, jurisdiction_code, status, restriction_details, regulation_ref)
VALUES ('ing_924a', 'US', 'RESTRICTED', 'Allowed up to 50mg/kg in dough, but voluntary reduction requested.', 'FDA 21 CFR 172.730')
ON CONFLICT (additive_id, jurisdiction_code, scope_category) DO NOTHING;
INSERT INTO additive_reference (ins_code, common_name, origin, category, fssai_status, efsa_status, fda_status, adi_value, concern_level, accurate_description, source_url, source_citation)
VALUES ('924a', 'Potassium Bromate', 'synthetic', 'FLOUR_TREATMENT_AGENT', 'BANNED', 'BANNED', 'RESTRICTED', '0-5 mg/kg body weight', 'HIGH', 'Industrial flour bleaching and dough conditioning agent. Linked to kidney tumors, thyroid cancer, and genotoxicity in animal studies.', 'https://www.fssai.gov.in', 'Official Safety Evaluation')
ON CONFLICT (ins_code) DO UPDATE SET concern_level = EXCLUDED.concern_level, accurate_description = EXCLUDED.accurate_description;
INSERT INTO additive_rulebook (additive_code, ins_number, canonical_name, functional_class, jurisdiction, status, label_requirement, regulation_title)
VALUES ('E924A', '924a', 'Potassium Bromate', 'FLOUR_TREATMENT_AGENT', 'EU', 'BANNED', 'Prohibited food additive due to carcinogenicity concerns.', 'EU Reg 1333/2008')
ON CONFLICT DO NOTHING;
INSERT INTO additive_rulebook (additive_code, ins_number, canonical_name, functional_class, jurisdiction, status, label_requirement, regulation_title)
VALUES ('E924A', '924a', 'Potassium Bromate', 'FLOUR_TREATMENT_AGENT', 'IN', 'BANNED', 'Banned in all bakery products by FSSAI in 2016.', 'FSSAI Ban 2016')
ON CONFLICT DO NOTHING;
INSERT INTO additive_rulebook (additive_code, ins_number, canonical_name, functional_class, jurisdiction, status, label_requirement, regulation_title)
VALUES ('E924A', '924a', 'Potassium Bromate', 'FLOUR_TREATMENT_AGENT', 'US', 'RESTRICTED', 'Allowed up to 50mg/kg in dough, but voluntary reduction requested.', 'FDA 21 CFR 172.730')
ON CONFLICT DO NOTHING;
INSERT INTO canonical_additives (id, ins_code, e_number, cas_number, primary_name, category, risk_level, base_risk_weight, cspi_rating, description)
VALUES ('ing_927a', '927a', 'E927A', '123-77-3', 'Azodicarbonamide (ADA)', 'FLOUR_TREATMENT_AGENT', 'HIGH', -18, 'AVOID', 'Chemical foaming agent and dough conditioner. Degrades into semicarbazide (a carcinogen) during baking. Linked to occupational asthma.')
ON CONFLICT (id) DO UPDATE SET risk_level = EXCLUDED.risk_level, cspi_rating = EXCLUDED.cspi_rating;
INSERT INTO additive_synonyms (additive_id, synonym_clean, language_code, is_primary)
VALUES ('ing_927a', 'azodicarbonamide (ada)', 'en', TRUE)
ON CONFLICT DO NOTHING;
INSERT INTO regulatory_bans (additive_id, jurisdiction_code, status, restriction_details, regulation_ref)
VALUES ('ing_927a', 'EU', 'BANNED', 'Banned as food additive due to respiratory asthma concerns.', 'EU Directive 2004/1/EC')
ON CONFLICT (additive_id, jurisdiction_code, scope_category) DO NOTHING;
INSERT INTO regulatory_bans (additive_id, jurisdiction_code, status, restriction_details, regulation_ref)
VALUES ('ing_927a', 'UK', 'BANNED', 'Prohibited in dough treatment.', 'UK Food Additive Regs')
ON CONFLICT (additive_id, jurisdiction_code, scope_category) DO NOTHING;
INSERT INTO regulatory_bans (additive_id, jurisdiction_code, status, restriction_details, regulation_ref)
VALUES ('ing_927a', 'US', 'RESTRICTED', 'Permitted up to 45 ppm.', 'FDA 21 CFR 172.806')
ON CONFLICT (additive_id, jurisdiction_code, scope_category) DO NOTHING;
INSERT INTO additive_reference (ins_code, common_name, origin, category, fssai_status, efsa_status, fda_status, adi_value, concern_level, accurate_description, source_url, source_citation)
VALUES ('927a', 'Azodicarbonamide (ADA)', 'synthetic', 'FLOUR_TREATMENT_AGENT', 'RESTRICTED', 'BANNED', 'RESTRICTED', '0-5 mg/kg body weight', 'HIGH', 'Chemical foaming agent and dough conditioner. Degrades into semicarbazide (a carcinogen) during baking. Linked to occupational asthma.', 'https://www.fssai.gov.in', 'Official Safety Evaluation')
ON CONFLICT (ins_code) DO UPDATE SET concern_level = EXCLUDED.concern_level, accurate_description = EXCLUDED.accurate_description;
INSERT INTO additive_rulebook (additive_code, ins_number, canonical_name, functional_class, jurisdiction, status, label_requirement, regulation_title)
VALUES ('E927A', '927a', 'Azodicarbonamide (ADA)', 'FLOUR_TREATMENT_AGENT', 'EU', 'BANNED', 'Banned as food additive due to respiratory asthma concerns.', 'EU Directive 2004/1/EC')
ON CONFLICT DO NOTHING;
INSERT INTO additive_rulebook (additive_code, ins_number, canonical_name, functional_class, jurisdiction, status, label_requirement, regulation_title)
VALUES ('E927A', '927a', 'Azodicarbonamide (ADA)', 'FLOUR_TREATMENT_AGENT', 'UK', 'BANNED', 'Prohibited in dough treatment.', 'UK Food Additive Regs')
ON CONFLICT DO NOTHING;
INSERT INTO additive_rulebook (additive_code, ins_number, canonical_name, functional_class, jurisdiction, status, label_requirement, regulation_title)
VALUES ('E927A', '927a', 'Azodicarbonamide (ADA)', 'FLOUR_TREATMENT_AGENT', 'US', 'RESTRICTED', 'Permitted up to 45 ppm.', 'FDA 21 CFR 172.806')
ON CONFLICT DO NOTHING;
INSERT INTO canonical_additives (id, ins_code, e_number, cas_number, primary_name, category, risk_level, base_risk_weight, cspi_rating, description)
VALUES ('ing_917', '917', 'E917', '7758-05-6', 'Potassium Iodate', 'FLOUR_TREATMENT_AGENT', 'HIGH', -18, 'AVOID', 'Flour treatment agent and dough conditioner. Linked to iodine toxicity, thyroid function disruption, and cell mutagenicity.')
ON CONFLICT (id) DO UPDATE SET risk_level = EXCLUDED.risk_level, cspi_rating = EXCLUDED.cspi_rating;
INSERT INTO additive_synonyms (additive_id, synonym_clean, language_code, is_primary)
VALUES ('ing_917', 'potassium iodate', 'en', TRUE)
ON CONFLICT DO NOTHING;
INSERT INTO regulatory_bans (additive_id, jurisdiction_code, status, restriction_details, regulation_ref)
VALUES ('ing_917', 'EU', 'BANNED', 'Banned as dough conditioner/food additive in the EU.', 'EU Reg 1333/2008')
ON CONFLICT (additive_id, jurisdiction_code, scope_category) DO NOTHING;
INSERT INTO regulatory_bans (additive_id, jurisdiction_code, status, restriction_details, regulation_ref)
VALUES ('ing_917', 'IN', 'BANNED', 'Prohibited in bread/bakery products by FSSAI.', 'FSSAI 2016 Regulation')
ON CONFLICT (additive_id, jurisdiction_code, scope_category) DO NOTHING;
INSERT INTO regulatory_bans (additive_id, jurisdiction_code, status, restriction_details, regulation_ref)
VALUES ('ing_917', 'US', 'RESTRICTED', 'Restricted to specified food uses.', 'FDA 21 CFR 184.1635')
ON CONFLICT (additive_id, jurisdiction_code, scope_category) DO NOTHING;
INSERT INTO additive_reference (ins_code, common_name, origin, category, fssai_status, efsa_status, fda_status, adi_value, concern_level, accurate_description, source_url, source_citation)
VALUES ('917', 'Potassium Iodate', 'synthetic', 'FLOUR_TREATMENT_AGENT', 'BANNED', 'BANNED', 'RESTRICTED', '0-5 mg/kg body weight', 'HIGH', 'Flour treatment agent and dough conditioner. Linked to iodine toxicity, thyroid function disruption, and cell mutagenicity.', 'https://www.fssai.gov.in', 'Official Safety Evaluation')
ON CONFLICT (ins_code) DO UPDATE SET concern_level = EXCLUDED.concern_level, accurate_description = EXCLUDED.accurate_description;
INSERT INTO additive_rulebook (additive_code, ins_number, canonical_name, functional_class, jurisdiction, status, label_requirement, regulation_title)
VALUES ('E917', '917', 'Potassium Iodate', 'FLOUR_TREATMENT_AGENT', 'EU', 'BANNED', 'Banned as dough conditioner/food additive in the EU.', 'EU Reg 1333/2008')
ON CONFLICT DO NOTHING;
INSERT INTO additive_rulebook (additive_code, ins_number, canonical_name, functional_class, jurisdiction, status, label_requirement, regulation_title)
VALUES ('E917', '917', 'Potassium Iodate', 'FLOUR_TREATMENT_AGENT', 'IN', 'BANNED', 'Prohibited in bread/bakery products by FSSAI.', 'FSSAI 2016 Regulation')
ON CONFLICT DO NOTHING;
INSERT INTO additive_rulebook (additive_code, ins_number, canonical_name, functional_class, jurisdiction, status, label_requirement, regulation_title)
VALUES ('E917', '917', 'Potassium Iodate', 'FLOUR_TREATMENT_AGENT', 'US', 'RESTRICTED', 'Restricted to specified food uses.', 'FDA 21 CFR 184.1635')
ON CONFLICT DO NOTHING;
INSERT INTO canonical_additives (id, ins_code, e_number, cas_number, primary_name, category, risk_level, base_risk_weight, cspi_rating, description)
VALUES ('ing_443', '443', 'E443', '8016-94-2', 'Brominated Vegetable Oil (BVO)', 'EMULSIFIER', 'HIGH', -20, 'AVOID', 'Plant-derived oil reacted with bromine. Accumulates in body fat and organs over time, linked to thyroid toxicity and neurological symptoms.')
ON CONFLICT (id) DO UPDATE SET risk_level = EXCLUDED.risk_level, cspi_rating = EXCLUDED.cspi_rating;
INSERT INTO additive_synonyms (additive_id, synonym_clean, language_code, is_primary)
VALUES ('ing_443', 'brominated vegetable oil (bvo)', 'en', TRUE)
ON CONFLICT DO NOTHING;
INSERT INTO regulatory_bans (additive_id, jurisdiction_code, status, restriction_details, regulation_ref)
VALUES ('ing_443', 'US', 'BANNED', 'FDA revoked authorization for use in food due to thyroid toxicity.', 'FDA Revocation 2024 (21 CFR 184)')
ON CONFLICT (additive_id, jurisdiction_code, scope_category) DO NOTHING;
INSERT INTO regulatory_bans (additive_id, jurisdiction_code, status, restriction_details, regulation_ref)
VALUES ('ing_443', 'EU', 'BANNED', 'Not authorized for food use in the European Union.', 'EU Reg 1333/2008')
ON CONFLICT (additive_id, jurisdiction_code, scope_category) DO NOTHING;
INSERT INTO regulatory_bans (additive_id, jurisdiction_code, status, restriction_details, regulation_ref)
VALUES ('ing_443', 'IN', 'BANNED', 'Prohibited in all beverage products.', 'FSSAI Prohibition Regulations')
ON CONFLICT (additive_id, jurisdiction_code, scope_category) DO NOTHING;
INSERT INTO additive_reference (ins_code, common_name, origin, category, fssai_status, efsa_status, fda_status, adi_value, concern_level, accurate_description, source_url, source_citation)
VALUES ('443', 'Brominated Vegetable Oil (BVO)', 'synthetic', 'EMULSIFIER', 'BANNED', 'BANNED', 'BANNED', '0-5 mg/kg body weight', 'HIGH', 'Plant-derived oil reacted with bromine. Accumulates in body fat and organs over time, linked to thyroid toxicity and neurological symptoms.', 'https://www.fssai.gov.in', 'Official Safety Evaluation')
ON CONFLICT (ins_code) DO UPDATE SET concern_level = EXCLUDED.concern_level, accurate_description = EXCLUDED.accurate_description;
INSERT INTO additive_rulebook (additive_code, ins_number, canonical_name, functional_class, jurisdiction, status, label_requirement, regulation_title)
VALUES ('E443', '443', 'Brominated Vegetable Oil (BVO)', 'EMULSIFIER', 'US', 'BANNED', 'FDA revoked authorization for use in food due to thyroid toxicity.', 'FDA Revocation 2024 (21 CFR 184)')
ON CONFLICT DO NOTHING;
INSERT INTO additive_rulebook (additive_code, ins_number, canonical_name, functional_class, jurisdiction, status, label_requirement, regulation_title)
VALUES ('E443', '443', 'Brominated Vegetable Oil (BVO)', 'EMULSIFIER', 'EU', 'BANNED', 'Not authorized for food use in the European Union.', 'EU Reg 1333/2008')
ON CONFLICT DO NOTHING;
INSERT INTO additive_rulebook (additive_code, ins_number, canonical_name, functional_class, jurisdiction, status, label_requirement, regulation_title)
VALUES ('E443', '443', 'Brominated Vegetable Oil (BVO)', 'EMULSIFIER', 'IN', 'BANNED', 'Prohibited in all beverage products.', 'FSSAI Prohibition Regulations')
ON CONFLICT DO NOTHING;
INSERT INTO canonical_additives (id, ins_code, e_number, cas_number, primary_name, category, risk_level, base_risk_weight, cspi_rating, description)
VALUES ('ing_320', '320', 'E320', '25013-16-5', 'Butylated Hydroxyanisole (BHA)', 'ANTIOXIDANT', 'HIGH', -10, 'CAUTION', 'Synthetic antioxidant used to prevent fat rancidity. Classified as reasonably anticipated to be a human carcinogen by US NTP.')
ON CONFLICT (id) DO UPDATE SET risk_level = EXCLUDED.risk_level, cspi_rating = EXCLUDED.cspi_rating;
INSERT INTO additive_synonyms (additive_id, synonym_clean, language_code, is_primary)
VALUES ('ing_320', 'butylated hydroxyanisole (bha)', 'en', TRUE)
ON CONFLICT DO NOTHING;
INSERT INTO regulatory_bans (additive_id, jurisdiction_code, status, restriction_details, regulation_ref)
VALUES ('ing_320', 'EU', 'RESTRICTED', 'Restricted max limits; under review for endocrine disruption.', 'EU Reg 1333/2008')
ON CONFLICT (additive_id, jurisdiction_code, scope_category) DO NOTHING;
INSERT INTO regulatory_bans (additive_id, jurisdiction_code, status, restriction_details, regulation_ref)
VALUES ('ing_320', 'JP', 'RESTRICTED', 'Strictly limited to specified fats and oils.', 'Japan Food Sanitation Act')
ON CONFLICT (additive_id, jurisdiction_code, scope_category) DO NOTHING;
INSERT INTO regulatory_bans (additive_id, jurisdiction_code, status, restriction_details, regulation_ref)
VALUES ('ing_320', 'US', 'RESTRICTED', 'Max 0.02% of fat content.', 'FDA 21 CFR 172.115')
ON CONFLICT (additive_id, jurisdiction_code, scope_category) DO NOTHING;
INSERT INTO additive_reference (ins_code, common_name, origin, category, fssai_status, efsa_status, fda_status, adi_value, concern_level, accurate_description, source_url, source_citation)
VALUES ('320', 'Butylated Hydroxyanisole (BHA)', 'synthetic', 'ANTIOXIDANT', 'RESTRICTED', 'RESTRICTED', 'RESTRICTED', '0-5 mg/kg body weight', 'HIGH', 'Synthetic antioxidant used to prevent fat rancidity. Classified as reasonably anticipated to be a human carcinogen by US NTP.', 'https://www.fssai.gov.in', 'Official Safety Evaluation')
ON CONFLICT (ins_code) DO UPDATE SET concern_level = EXCLUDED.concern_level, accurate_description = EXCLUDED.accurate_description;
INSERT INTO additive_rulebook (additive_code, ins_number, canonical_name, functional_class, jurisdiction, status, label_requirement, regulation_title)
VALUES ('E320', '320', 'Butylated Hydroxyanisole (BHA)', 'ANTIOXIDANT', 'EU', 'RESTRICTED', 'Restricted max limits; under review for endocrine disruption.', 'EU Reg 1333/2008')
ON CONFLICT DO NOTHING;
INSERT INTO additive_rulebook (additive_code, ins_number, canonical_name, functional_class, jurisdiction, status, label_requirement, regulation_title)
VALUES ('E320', '320', 'Butylated Hydroxyanisole (BHA)', 'ANTIOXIDANT', 'JP', 'RESTRICTED', 'Strictly limited to specified fats and oils.', 'Japan Food Sanitation Act')
ON CONFLICT DO NOTHING;
INSERT INTO additive_rulebook (additive_code, ins_number, canonical_name, functional_class, jurisdiction, status, label_requirement, regulation_title)
VALUES ('E320', '320', 'Butylated Hydroxyanisole (BHA)', 'ANTIOXIDANT', 'US', 'RESTRICTED', 'Max 0.02% of fat content.', 'FDA 21 CFR 172.115')
ON CONFLICT DO NOTHING;
INSERT INTO canonical_additives (id, ins_code, e_number, cas_number, primary_name, category, risk_level, base_risk_weight, cspi_rating, description)
VALUES ('ing_321', '321', 'E321', '128-37-0', 'Butylated Hydroxytoluene (BHT)', 'ANTIOXIDANT', 'MEDIUM', -8, 'CAUTION', 'Synthetic antioxidant closely related to BHA. Linked to liver damage, lung lesions, and suspected endocrine disrupting properties.')
ON CONFLICT (id) DO UPDATE SET risk_level = EXCLUDED.risk_level, cspi_rating = EXCLUDED.cspi_rating;
INSERT INTO additive_synonyms (additive_id, synonym_clean, language_code, is_primary)
VALUES ('ing_321', 'butylated hydroxytoluene (bht)', 'en', TRUE)
ON CONFLICT DO NOTHING;
INSERT INTO regulatory_bans (additive_id, jurisdiction_code, status, restriction_details, regulation_ref)
VALUES ('ing_321', 'EU', 'RESTRICTED', 'Restricted concentration limits in fats.', 'EU Reg 1333/2008')
ON CONFLICT (additive_id, jurisdiction_code, scope_category) DO NOTHING;
INSERT INTO regulatory_bans (additive_id, jurisdiction_code, status, restriction_details, regulation_ref)
VALUES ('ing_321', 'US', 'RESTRICTED', 'Max 0.02% of fat content.', 'FDA 21 CFR 172.115')
ON CONFLICT (additive_id, jurisdiction_code, scope_category) DO NOTHING;
INSERT INTO additive_reference (ins_code, common_name, origin, category, fssai_status, efsa_status, fda_status, adi_value, concern_level, accurate_description, source_url, source_citation)
VALUES ('321', 'Butylated Hydroxytoluene (BHT)', 'synthetic', 'ANTIOXIDANT', 'RESTRICTED', 'RESTRICTED', 'RESTRICTED', '0-5 mg/kg body weight', 'MEDIUM', 'Synthetic antioxidant closely related to BHA. Linked to liver damage, lung lesions, and suspected endocrine disrupting properties.', 'https://www.fssai.gov.in', 'Official Safety Evaluation')
ON CONFLICT (ins_code) DO UPDATE SET concern_level = EXCLUDED.concern_level, accurate_description = EXCLUDED.accurate_description;
INSERT INTO additive_rulebook (additive_code, ins_number, canonical_name, functional_class, jurisdiction, status, label_requirement, regulation_title)
VALUES ('E321', '321', 'Butylated Hydroxytoluene (BHT)', 'ANTIOXIDANT', 'EU', 'RESTRICTED', 'Restricted concentration limits in fats.', 'EU Reg 1333/2008')
ON CONFLICT DO NOTHING;
INSERT INTO additive_rulebook (additive_code, ins_number, canonical_name, functional_class, jurisdiction, status, label_requirement, regulation_title)
VALUES ('E321', '321', 'Butylated Hydroxytoluene (BHT)', 'ANTIOXIDANT', 'US', 'RESTRICTED', 'Max 0.02% of fat content.', 'FDA 21 CFR 172.115')
ON CONFLICT DO NOTHING;
INSERT INTO canonical_additives (id, ins_code, e_number, cas_number, primary_name, category, risk_level, base_risk_weight, cspi_rating, description)
VALUES ('ing_216', '216', 'E216', '94-13-3', 'Propylparaben', 'PRESERVATIVE', 'HIGH', -15, 'AVOID', 'Preservative and antimicrobial agent. Shown to interfere with hormone levels and reproductive systems in laboratory animal models.')
ON CONFLICT (id) DO UPDATE SET risk_level = EXCLUDED.risk_level, cspi_rating = EXCLUDED.cspi_rating;
INSERT INTO additive_synonyms (additive_id, synonym_clean, language_code, is_primary)
VALUES ('ing_216', 'propylparaben', 'en', TRUE)
ON CONFLICT DO NOTHING;
INSERT INTO regulatory_bans (additive_id, jurisdiction_code, status, restriction_details, regulation_ref)
VALUES ('ing_216', 'EU', 'BANNED', 'Banned in EU foods due to endocrine disrupting effects.', 'Directive 2006/52/EC')
ON CONFLICT (additive_id, jurisdiction_code, scope_category) DO NOTHING;
INSERT INTO regulatory_bans (additive_id, jurisdiction_code, status, restriction_details, regulation_ref)
VALUES ('ing_216', 'IN', 'BANNED', 'Not permitted in Indian food products.', 'FSSAI Food Additive Schedule')
ON CONFLICT (additive_id, jurisdiction_code, scope_category) DO NOTHING;
INSERT INTO regulatory_bans (additive_id, jurisdiction_code, status, restriction_details, regulation_ref)
VALUES ('ing_216', 'US', 'RESTRICTED', 'Generally recognized as safe but under review.', 'FDA 21 CFR 184.1670')
ON CONFLICT (additive_id, jurisdiction_code, scope_category) DO NOTHING;
INSERT INTO additive_reference (ins_code, common_name, origin, category, fssai_status, efsa_status, fda_status, adi_value, concern_level, accurate_description, source_url, source_citation)
VALUES ('216', 'Propylparaben', 'synthetic', 'PRESERVATIVE', 'BANNED', 'BANNED', 'RESTRICTED', '0-5 mg/kg body weight', 'HIGH', 'Preservative and antimicrobial agent. Shown to interfere with hormone levels and reproductive systems in laboratory animal models.', 'https://www.fssai.gov.in', 'Official Safety Evaluation')
ON CONFLICT (ins_code) DO UPDATE SET concern_level = EXCLUDED.concern_level, accurate_description = EXCLUDED.accurate_description;
INSERT INTO additive_rulebook (additive_code, ins_number, canonical_name, functional_class, jurisdiction, status, label_requirement, regulation_title)
VALUES ('E216', '216', 'Propylparaben', 'PRESERVATIVE', 'EU', 'BANNED', 'Banned in EU foods due to endocrine disrupting effects.', 'Directive 2006/52/EC')
ON CONFLICT DO NOTHING;
INSERT INTO additive_rulebook (additive_code, ins_number, canonical_name, functional_class, jurisdiction, status, label_requirement, regulation_title)
VALUES ('E216', '216', 'Propylparaben', 'PRESERVATIVE', 'IN', 'BANNED', 'Not permitted in Indian food products.', 'FSSAI Food Additive Schedule')
ON CONFLICT DO NOTHING;
INSERT INTO additive_rulebook (additive_code, ins_number, canonical_name, functional_class, jurisdiction, status, label_requirement, regulation_title)
VALUES ('E216', '216', 'Propylparaben', 'PRESERVATIVE', 'US', 'RESTRICTED', 'Generally recognized as safe but under review.', 'FDA 21 CFR 184.1670')
ON CONFLICT DO NOTHING;
INSERT INTO canonical_additives (id, ins_code, e_number, cas_number, primary_name, category, risk_level, base_risk_weight, cspi_rating, description)
VALUES ('ing_249', '249', 'E249', '7758-09-0', 'Potassium Nitrite', 'PRESERVATIVE', 'HIGH', -15, 'AVOID', 'Curing agent and preservative. Reacts with secondary amines in meat to form carcinogenic nitrosamines during cooking.')
ON CONFLICT (id) DO UPDATE SET risk_level = EXCLUDED.risk_level, cspi_rating = EXCLUDED.cspi_rating;
INSERT INTO additive_synonyms (additive_id, synonym_clean, language_code, is_primary)
VALUES ('ing_249', 'potassium nitrite', 'en', TRUE)
ON CONFLICT DO NOTHING;
INSERT INTO regulatory_bans (additive_id, jurisdiction_code, status, restriction_details, regulation_ref)
VALUES ('ing_249', 'EU', 'RESTRICTED', 'Carcinogenicity risk via nitrosamine formation in meat products.', 'EU Reg 1333/2008')
ON CONFLICT (additive_id, jurisdiction_code, scope_category) DO NOTHING;
INSERT INTO regulatory_bans (additive_id, jurisdiction_code, status, restriction_details, regulation_ref)
VALUES ('ing_249', 'US', 'RESTRICTED', 'Allowed strictly in cured meats under specific PPM limits.', 'FDA 21 CFR 172.160')
ON CONFLICT (additive_id, jurisdiction_code, scope_category) DO NOTHING;
INSERT INTO additive_reference (ins_code, common_name, origin, category, fssai_status, efsa_status, fda_status, adi_value, concern_level, accurate_description, source_url, source_citation)
VALUES ('249', 'Potassium Nitrite', 'synthetic', 'PRESERVATIVE', 'RESTRICTED', 'RESTRICTED', 'RESTRICTED', '0-5 mg/kg body weight', 'HIGH', 'Curing agent and preservative. Reacts with secondary amines in meat to form carcinogenic nitrosamines during cooking.', 'https://www.fssai.gov.in', 'Official Safety Evaluation')
ON CONFLICT (ins_code) DO UPDATE SET concern_level = EXCLUDED.concern_level, accurate_description = EXCLUDED.accurate_description;
INSERT INTO additive_rulebook (additive_code, ins_number, canonical_name, functional_class, jurisdiction, status, label_requirement, regulation_title)
VALUES ('E249', '249', 'Potassium Nitrite', 'PRESERVATIVE', 'EU', 'RESTRICTED', 'Carcinogenicity risk via nitrosamine formation in meat products.', 'EU Reg 1333/2008')
ON CONFLICT DO NOTHING;
INSERT INTO additive_rulebook (additive_code, ins_number, canonical_name, functional_class, jurisdiction, status, label_requirement, regulation_title)
VALUES ('E249', '249', 'Potassium Nitrite', 'PRESERVATIVE', 'US', 'RESTRICTED', 'Allowed strictly in cured meats under specific PPM limits.', 'FDA 21 CFR 172.160')
ON CONFLICT DO NOTHING;
INSERT INTO canonical_additives (id, ins_code, e_number, cas_number, primary_name, category, risk_level, base_risk_weight, cspi_rating, description)
VALUES ('ing_250', '250', 'E250', '7632-00-0', 'Sodium Nitrite', 'PRESERVATIVE', 'HIGH', -15, 'AVOID', 'Widely used meat curing preservative. Precursor to highly carcinogenic nitrosamines; associated with increased gastric cancer risk.')
ON CONFLICT (id) DO UPDATE SET risk_level = EXCLUDED.risk_level, cspi_rating = EXCLUDED.cspi_rating;
INSERT INTO additive_synonyms (additive_id, synonym_clean, language_code, is_primary)
VALUES ('ing_250', 'sodium nitrite', 'en', TRUE)
ON CONFLICT DO NOTHING;
INSERT INTO regulatory_bans (additive_id, jurisdiction_code, status, restriction_details, regulation_ref)
VALUES ('ing_250', 'EU', 'RESTRICTED', 'Carcinogenicity concerns; forming carcinogenic nitrosamines.', 'EU Reg 1333/2008')
ON CONFLICT (additive_id, jurisdiction_code, scope_category) DO NOTHING;
INSERT INTO regulatory_bans (additive_id, jurisdiction_code, status, restriction_details, regulation_ref)
VALUES ('ing_250', 'US', 'RESTRICTED', 'Strictly limited in curing mixtures.', 'FDA 21 CFR 172.170')
ON CONFLICT (additive_id, jurisdiction_code, scope_category) DO NOTHING;
INSERT INTO additive_reference (ins_code, common_name, origin, category, fssai_status, efsa_status, fda_status, adi_value, concern_level, accurate_description, source_url, source_citation)
VALUES ('250', 'Sodium Nitrite', 'synthetic', 'PRESERVATIVE', 'RESTRICTED', 'RESTRICTED', 'RESTRICTED', '0-5 mg/kg body weight', 'HIGH', 'Widely used meat curing preservative. Precursor to highly carcinogenic nitrosamines; associated with increased gastric cancer risk.', 'https://www.fssai.gov.in', 'Official Safety Evaluation')
ON CONFLICT (ins_code) DO UPDATE SET concern_level = EXCLUDED.concern_level, accurate_description = EXCLUDED.accurate_description;
INSERT INTO additive_rulebook (additive_code, ins_number, canonical_name, functional_class, jurisdiction, status, label_requirement, regulation_title)
VALUES ('E250', '250', 'Sodium Nitrite', 'PRESERVATIVE', 'EU', 'RESTRICTED', 'Carcinogenicity concerns; forming carcinogenic nitrosamines.', 'EU Reg 1333/2008')
ON CONFLICT DO NOTHING;
INSERT INTO additive_rulebook (additive_code, ins_number, canonical_name, functional_class, jurisdiction, status, label_requirement, regulation_title)
VALUES ('E250', '250', 'Sodium Nitrite', 'PRESERVATIVE', 'US', 'RESTRICTED', 'Strictly limited in curing mixtures.', 'FDA 21 CFR 172.170')
ON CONFLICT DO NOTHING;
INSERT INTO canonical_additives (id, ins_code, e_number, cas_number, primary_name, category, risk_level, base_risk_weight, cspi_rating, description)
VALUES ('ing_251', '251', 'E251', '7631-99-4', 'Sodium Nitrate', 'PRESERVATIVE', 'HIGH', -12, 'AVOID', 'Preservative and color fixative in cured meats. Converts into nitrites in the body, leading to carcinogen formation.')
ON CONFLICT (id) DO UPDATE SET risk_level = EXCLUDED.risk_level, cspi_rating = EXCLUDED.cspi_rating;
INSERT INTO additive_synonyms (additive_id, synonym_clean, language_code, is_primary)
VALUES ('ing_251', 'sodium nitrate', 'en', TRUE)
ON CONFLICT DO NOTHING;
INSERT INTO regulatory_bans (additive_id, jurisdiction_code, status, restriction_details, regulation_ref)
VALUES ('ing_251', 'EU', 'RESTRICTED', 'Forms nitrites and carcinogenic nitrosamines in food.', 'EU Reg 1333/2008')
ON CONFLICT (additive_id, jurisdiction_code, scope_category) DO NOTHING;
INSERT INTO regulatory_bans (additive_id, jurisdiction_code, status, restriction_details, regulation_ref)
VALUES ('ing_251', 'US', 'RESTRICTED', 'Strict limits applied.', 'FDA 21 CFR 172.170')
ON CONFLICT (additive_id, jurisdiction_code, scope_category) DO NOTHING;
INSERT INTO additive_reference (ins_code, common_name, origin, category, fssai_status, efsa_status, fda_status, adi_value, concern_level, accurate_description, source_url, source_citation)
VALUES ('251', 'Sodium Nitrate', 'synthetic', 'PRESERVATIVE', 'RESTRICTED', 'RESTRICTED', 'RESTRICTED', '0-5 mg/kg body weight', 'HIGH', 'Preservative and color fixative in cured meats. Converts into nitrites in the body, leading to carcinogen formation.', 'https://www.fssai.gov.in', 'Official Safety Evaluation')
ON CONFLICT (ins_code) DO UPDATE SET concern_level = EXCLUDED.concern_level, accurate_description = EXCLUDED.accurate_description;
INSERT INTO additive_rulebook (additive_code, ins_number, canonical_name, functional_class, jurisdiction, status, label_requirement, regulation_title)
VALUES ('E251', '251', 'Sodium Nitrate', 'PRESERVATIVE', 'EU', 'RESTRICTED', 'Forms nitrites and carcinogenic nitrosamines in food.', 'EU Reg 1333/2008')
ON CONFLICT DO NOTHING;
INSERT INTO additive_rulebook (additive_code, ins_number, canonical_name, functional_class, jurisdiction, status, label_requirement, regulation_title)
VALUES ('E251', '251', 'Sodium Nitrate', 'PRESERVATIVE', 'US', 'RESTRICTED', 'Strict limits applied.', 'FDA 21 CFR 172.170')
ON CONFLICT DO NOTHING;
INSERT INTO canonical_additives (id, ins_code, e_number, cas_number, primary_name, category, risk_level, base_risk_weight, cspi_rating, description)
VALUES ('ing_252', '252', 'E252', '7757-79-1', 'Potassium Nitrate', 'PRESERVATIVE', 'HIGH', -12, 'AVOID', 'Naturally occurring nitrate mineral preservative. Associated with blood disorders (methemoglobinemia) in infants, and cancer risk.')
ON CONFLICT (id) DO UPDATE SET risk_level = EXCLUDED.risk_level, cspi_rating = EXCLUDED.cspi_rating;
INSERT INTO additive_synonyms (additive_id, synonym_clean, language_code, is_primary)
VALUES ('ing_252', 'potassium nitrate', 'en', TRUE)
ON CONFLICT DO NOTHING;
INSERT INTO regulatory_bans (additive_id, jurisdiction_code, status, restriction_details, regulation_ref)
VALUES ('ing_252', 'EU', 'RESTRICTED', 'Precursor to carcinogenic nitrosamines.', 'EU Reg 1333/2008')
ON CONFLICT (additive_id, jurisdiction_code, scope_category) DO NOTHING;
INSERT INTO regulatory_bans (additive_id, jurisdiction_code, status, restriction_details, regulation_ref)
VALUES ('ing_252', 'US', 'RESTRICTED', 'Strict limits in cured meats.', 'FDA 21 CFR 172.170')
ON CONFLICT (additive_id, jurisdiction_code, scope_category) DO NOTHING;
INSERT INTO additive_reference (ins_code, common_name, origin, category, fssai_status, efsa_status, fda_status, adi_value, concern_level, accurate_description, source_url, source_citation)
VALUES ('252', 'Potassium Nitrate', 'synthetic', 'PRESERVATIVE', 'RESTRICTED', 'RESTRICTED', 'RESTRICTED', '0-5 mg/kg body weight', 'HIGH', 'Naturally occurring nitrate mineral preservative. Associated with blood disorders (methemoglobinemia) in infants, and cancer risk.', 'https://www.fssai.gov.in', 'Official Safety Evaluation')
ON CONFLICT (ins_code) DO UPDATE SET concern_level = EXCLUDED.concern_level, accurate_description = EXCLUDED.accurate_description;
INSERT INTO additive_rulebook (additive_code, ins_number, canonical_name, functional_class, jurisdiction, status, label_requirement, regulation_title)
VALUES ('E252', '252', 'Potassium Nitrate', 'PRESERVATIVE', 'EU', 'RESTRICTED', 'Precursor to carcinogenic nitrosamines.', 'EU Reg 1333/2008')
ON CONFLICT DO NOTHING;
INSERT INTO additive_rulebook (additive_code, ins_number, canonical_name, functional_class, jurisdiction, status, label_requirement, regulation_title)
VALUES ('E252', '252', 'Potassium Nitrate', 'PRESERVATIVE', 'US', 'RESTRICTED', 'Strict limits in cured meats.', 'FDA 21 CFR 172.170')
ON CONFLICT DO NOTHING;
INSERT INTO canonical_additives (id, ins_code, e_number, cas_number, primary_name, category, risk_level, base_risk_weight, cspi_rating, description)
VALUES ('ing_952', '952', 'E952', '100-88-9', 'Cyclamic Acid & Cyclamates', 'ARTIFICIAL_SWEETENER', 'HIGH', -15, 'AVOID', 'Intense artificial sweetener. Banned in the US since 1969 due to laboratory animal bladder cancer studies.')
ON CONFLICT (id) DO UPDATE SET risk_level = EXCLUDED.risk_level, cspi_rating = EXCLUDED.cspi_rating;
INSERT INTO additive_synonyms (additive_id, synonym_clean, language_code, is_primary)
VALUES ('ing_952', 'cyclamic acid & cyclamates', 'en', TRUE)
ON CONFLICT DO NOTHING;
INSERT INTO regulatory_bans (additive_id, jurisdiction_code, status, restriction_details, regulation_ref)
VALUES ('ing_952', 'US', 'BANNED', 'Banned by US FDA since 1969 due to bladder tumor concerns.', 'FDA 21 CFR 189.135')
ON CONFLICT (additive_id, jurisdiction_code, scope_category) DO NOTHING;
INSERT INTO additive_reference (ins_code, common_name, origin, category, fssai_status, efsa_status, fda_status, adi_value, concern_level, accurate_description, source_url, source_citation)
VALUES ('952', 'Cyclamic Acid & Cyclamates', 'synthetic', 'ARTIFICIAL_SWEETENER', 'RESTRICTED', 'RESTRICTED', 'BANNED', '0-5 mg/kg body weight', 'HIGH', 'Intense artificial sweetener. Banned in the US since 1969 due to laboratory animal bladder cancer studies.', 'https://www.fssai.gov.in', 'Official Safety Evaluation')
ON CONFLICT (ins_code) DO UPDATE SET concern_level = EXCLUDED.concern_level, accurate_description = EXCLUDED.accurate_description;
INSERT INTO additive_rulebook (additive_code, ins_number, canonical_name, functional_class, jurisdiction, status, label_requirement, regulation_title)
VALUES ('E952', '952', 'Cyclamic Acid & Cyclamates', 'ARTIFICIAL_SWEETENER', 'US', 'BANNED', 'Banned by US FDA since 1969 due to bladder tumor concerns.', 'FDA 21 CFR 189.135')
ON CONFLICT DO NOTHING;
INSERT INTO canonical_additives (id, ins_code, e_number, cas_number, primary_name, category, risk_level, base_risk_weight, cspi_rating, description)
VALUES ('ing_951', '951', 'E951', '22839-47-0', 'Aspartame', 'ARTIFICIAL_SWEETENER', 'HIGH', -12, 'CAUTION', 'Synthetic non-nutritive sweetener. Classified as possibly carcinogenic to humans (IARC Group 2B) in 2023.')
ON CONFLICT (id) DO UPDATE SET risk_level = EXCLUDED.risk_level, cspi_rating = EXCLUDED.cspi_rating;
INSERT INTO additive_synonyms (additive_id, synonym_clean, language_code, is_primary)
VALUES ('ing_951', 'aspartame', 'en', TRUE)
ON CONFLICT DO NOTHING;
INSERT INTO regulatory_bans (additive_id, jurisdiction_code, status, restriction_details, regulation_ref)
VALUES ('ing_951', 'CODEX', 'RESTRICTED', 'Classified as Possibly Carcinogenic to Humans (Group 2B) by WHO IARC in 2023.', 'WHO IARC Group 2B 2023')
ON CONFLICT (additive_id, jurisdiction_code, scope_category) DO NOTHING;
INSERT INTO additive_reference (ins_code, common_name, origin, category, fssai_status, efsa_status, fda_status, adi_value, concern_level, accurate_description, source_url, source_citation)
VALUES ('951', 'Aspartame', 'synthetic', 'ARTIFICIAL_SWEETENER', 'RESTRICTED', 'RESTRICTED', 'RESTRICTED', '0-5 mg/kg body weight', 'HIGH', 'Synthetic non-nutritive sweetener. Classified as possibly carcinogenic to humans (IARC Group 2B) in 2023.', 'https://www.fssai.gov.in', 'Official Safety Evaluation')
ON CONFLICT (ins_code) DO UPDATE SET concern_level = EXCLUDED.concern_level, accurate_description = EXCLUDED.accurate_description;
INSERT INTO additive_rulebook (additive_code, ins_number, canonical_name, functional_class, jurisdiction, status, label_requirement, regulation_title)
VALUES ('E951', '951', 'Aspartame', 'ARTIFICIAL_SWEETENER', 'CODEX', 'RESTRICTED', 'Classified as Possibly Carcinogenic to Humans (Group 2B) by WHO IARC in 2023.', 'WHO IARC Group 2B 2023')
ON CONFLICT DO NOTHING;
INSERT INTO canonical_additives (id, ins_code, e_number, cas_number, primary_name, category, risk_level, base_risk_weight, cspi_rating, description)
VALUES ('ing_956', '956', 'E956', '80863-53-8', 'Alitame', 'ARTIFICIAL_SWEETENER', 'HIGH', -15, 'AVOID', 'Second-generation dipeptide artificial sweetener. Withdrawn or not authorized in many Western countries due to liver health questions.')
ON CONFLICT (id) DO UPDATE SET risk_level = EXCLUDED.risk_level, cspi_rating = EXCLUDED.cspi_rating;
INSERT INTO additive_synonyms (additive_id, synonym_clean, language_code, is_primary)
VALUES ('ing_956', 'alitame', 'en', TRUE)
ON CONFLICT DO NOTHING;
INSERT INTO regulatory_bans (additive_id, jurisdiction_code, status, restriction_details, regulation_ref)
VALUES ('ing_956', 'US', 'RESTRICTED', 'Not authorized / approved as a sweetener in the US.', 'FDA Review Status')
ON CONFLICT (additive_id, jurisdiction_code, scope_category) DO NOTHING;
INSERT INTO regulatory_bans (additive_id, jurisdiction_code, status, restriction_details, regulation_ref)
VALUES ('ing_956', 'EU', 'BANNED', 'Withdrawn/not authorized for use in the EU.', 'EU Reg 1333/2008')
ON CONFLICT (additive_id, jurisdiction_code, scope_category) DO NOTHING;
INSERT INTO additive_reference (ins_code, common_name, origin, category, fssai_status, efsa_status, fda_status, adi_value, concern_level, accurate_description, source_url, source_citation)
VALUES ('956', 'Alitame', 'synthetic', 'ARTIFICIAL_SWEETENER', 'RESTRICTED', 'BANNED', 'RESTRICTED', '0-5 mg/kg body weight', 'HIGH', 'Second-generation dipeptide artificial sweetener. Withdrawn or not authorized in many Western countries due to liver health questions.', 'https://www.fssai.gov.in', 'Official Safety Evaluation')
ON CONFLICT (ins_code) DO UPDATE SET concern_level = EXCLUDED.concern_level, accurate_description = EXCLUDED.accurate_description;
INSERT INTO additive_rulebook (additive_code, ins_number, canonical_name, functional_class, jurisdiction, status, label_requirement, regulation_title)
VALUES ('E956', '956', 'Alitame', 'ARTIFICIAL_SWEETENER', 'US', 'RESTRICTED', 'Not authorized / approved as a sweetener in the US.', 'FDA Review Status')
ON CONFLICT DO NOTHING;
INSERT INTO additive_rulebook (additive_code, ins_number, canonical_name, functional_class, jurisdiction, status, label_requirement, regulation_title)
VALUES ('E956', '956', 'Alitame', 'ARTIFICIAL_SWEETENER', 'EU', 'BANNED', 'Withdrawn/not authorized for use in the EU.', 'EU Reg 1333/2008')
ON CONFLICT DO NOTHING;
INSERT INTO canonical_additives (id, ins_code, e_number, cas_number, primary_name, category, risk_level, base_risk_weight, cspi_rating, description)
VALUES ('ing_954', '954', 'E954', '81-07-2', 'Saccharin', 'ARTIFICIAL_SWEETENER', 'HIGH', -15, 'AVOID', 'One of the oldest synthetic sweeteners. Under observation for bladder irritation and tumor promotion risks.')
ON CONFLICT (id) DO UPDATE SET risk_level = EXCLUDED.risk_level, cspi_rating = EXCLUDED.cspi_rating;
INSERT INTO additive_synonyms (additive_id, synonym_clean, language_code, is_primary)
VALUES ('ing_954', 'saccharin', 'en', TRUE)
ON CONFLICT DO NOTHING;
INSERT INTO regulatory_bans (additive_id, jurisdiction_code, status, restriction_details, regulation_ref)
VALUES ('ing_954', 'US', 'RESTRICTED', 'Allowed under strict concentration limits.', 'FDA 21 CFR 180.37')
ON CONFLICT (additive_id, jurisdiction_code, scope_category) DO NOTHING;
INSERT INTO regulatory_bans (additive_id, jurisdiction_code, status, restriction_details, regulation_ref)
VALUES ('ing_954', 'EU', 'RESTRICTED', 'Strict category limits; under monitoring.', 'EU Reg 1333/2008')
ON CONFLICT (additive_id, jurisdiction_code, scope_category) DO NOTHING;
INSERT INTO additive_reference (ins_code, common_name, origin, category, fssai_status, efsa_status, fda_status, adi_value, concern_level, accurate_description, source_url, source_citation)
VALUES ('954', 'Saccharin', 'synthetic', 'ARTIFICIAL_SWEETENER', 'RESTRICTED', 'RESTRICTED', 'RESTRICTED', '0-5 mg/kg body weight', 'HIGH', 'One of the oldest synthetic sweeteners. Under observation for bladder irritation and tumor promotion risks.', 'https://www.fssai.gov.in', 'Official Safety Evaluation')
ON CONFLICT (ins_code) DO UPDATE SET concern_level = EXCLUDED.concern_level, accurate_description = EXCLUDED.accurate_description;
INSERT INTO additive_rulebook (additive_code, ins_number, canonical_name, functional_class, jurisdiction, status, label_requirement, regulation_title)
VALUES ('E954', '954', 'Saccharin', 'ARTIFICIAL_SWEETENER', 'US', 'RESTRICTED', 'Allowed under strict concentration limits.', 'FDA 21 CFR 180.37')
ON CONFLICT DO NOTHING;
INSERT INTO additive_rulebook (additive_code, ins_number, canonical_name, functional_class, jurisdiction, status, label_requirement, regulation_title)
VALUES ('E954', '954', 'Saccharin', 'ARTIFICIAL_SWEETENER', 'EU', 'RESTRICTED', 'Strict category limits; under monitoring.', 'EU Reg 1333/2008')
ON CONFLICT DO NOTHING;
INSERT INTO canonical_additives (id, ins_code, e_number, cas_number, primary_name, category, risk_level, base_risk_weight, cspi_rating, description)
VALUES ('ing_433', '433', 'E433', '9005-65-6', 'Polysorbate 80', 'EMULSIFIER', 'MEDIUM', -8, 'CAUTION', 'Synthetic emulsifier. Linked to intestinal mucosal barrier disruption, low-grade inflammation, and gut microbiome dysbiosis.')
ON CONFLICT (id) DO UPDATE SET risk_level = EXCLUDED.risk_level, cspi_rating = EXCLUDED.cspi_rating;
INSERT INTO additive_synonyms (additive_id, synonym_clean, language_code, is_primary)
VALUES ('ing_433', 'polysorbate 80', 'en', TRUE)
ON CONFLICT DO NOTHING;
INSERT INTO regulatory_bans (additive_id, jurisdiction_code, status, restriction_details, regulation_ref)
VALUES ('ing_433', 'US', 'RESTRICTED', 'Restricted use levels; potential gut health risk.', 'FDA 21 CFR 172.840')
ON CONFLICT (additive_id, jurisdiction_code, scope_category) DO NOTHING;
INSERT INTO regulatory_bans (additive_id, jurisdiction_code, status, restriction_details, regulation_ref)
VALUES ('ing_433', 'EU', 'RESTRICTED', 'Restricted under specified maximum levels.', 'EU Reg 1333/2008')
ON CONFLICT (additive_id, jurisdiction_code, scope_category) DO NOTHING;
INSERT INTO additive_reference (ins_code, common_name, origin, category, fssai_status, efsa_status, fda_status, adi_value, concern_level, accurate_description, source_url, source_citation)
VALUES ('433', 'Polysorbate 80', 'synthetic', 'EMULSIFIER', 'RESTRICTED', 'RESTRICTED', 'RESTRICTED', '0-5 mg/kg body weight', 'MEDIUM', 'Synthetic emulsifier. Linked to intestinal mucosal barrier disruption, low-grade inflammation, and gut microbiome dysbiosis.', 'https://www.fssai.gov.in', 'Official Safety Evaluation')
ON CONFLICT (ins_code) DO UPDATE SET concern_level = EXCLUDED.concern_level, accurate_description = EXCLUDED.accurate_description;
INSERT INTO additive_rulebook (additive_code, ins_number, canonical_name, functional_class, jurisdiction, status, label_requirement, regulation_title)
VALUES ('E433', '433', 'Polysorbate 80', 'EMULSIFIER', 'US', 'RESTRICTED', 'Restricted use levels; potential gut health risk.', 'FDA 21 CFR 172.840')
ON CONFLICT DO NOTHING;
INSERT INTO additive_rulebook (additive_code, ins_number, canonical_name, functional_class, jurisdiction, status, label_requirement, regulation_title)
VALUES ('E433', '433', 'Polysorbate 80', 'EMULSIFIER', 'EU', 'RESTRICTED', 'Restricted under specified maximum levels.', 'EU Reg 1333/2008')
ON CONFLICT DO NOTHING;
INSERT INTO canonical_additives (id, ins_code, e_number, cas_number, primary_name, category, risk_level, base_risk_weight, cspi_rating, description)
VALUES ('ing_435', '435', 'E435', '9005-67-8', 'Polysorbate 60', 'EMULSIFIER', 'MEDIUM', -8, 'CAUTION', 'Synthetic surfactant emulsifier. Associated with gastrointestinal lining irritation and alteration of gut bacteria composition.')
ON CONFLICT (id) DO UPDATE SET risk_level = EXCLUDED.risk_level, cspi_rating = EXCLUDED.cspi_rating;
INSERT INTO additive_synonyms (additive_id, synonym_clean, language_code, is_primary)
VALUES ('ing_435', 'polysorbate 60', 'en', TRUE)
ON CONFLICT DO NOTHING;
INSERT INTO regulatory_bans (additive_id, jurisdiction_code, status, restriction_details, regulation_ref)
VALUES ('ing_435', 'US', 'RESTRICTED', 'Strict usage thresholds.', 'FDA 21 CFR 172.836')
ON CONFLICT (additive_id, jurisdiction_code, scope_category) DO NOTHING;
INSERT INTO regulatory_bans (additive_id, jurisdiction_code, status, restriction_details, regulation_ref)
VALUES ('ing_435', 'EU', 'RESTRICTED', 'Restricted usage limits.', 'EU Reg 1333/2008')
ON CONFLICT (additive_id, jurisdiction_code, scope_category) DO NOTHING;
INSERT INTO additive_reference (ins_code, common_name, origin, category, fssai_status, efsa_status, fda_status, adi_value, concern_level, accurate_description, source_url, source_citation)
VALUES ('435', 'Polysorbate 60', 'synthetic', 'EMULSIFIER', 'RESTRICTED', 'RESTRICTED', 'RESTRICTED', '0-5 mg/kg body weight', 'MEDIUM', 'Synthetic surfactant emulsifier. Associated with gastrointestinal lining irritation and alteration of gut bacteria composition.', 'https://www.fssai.gov.in', 'Official Safety Evaluation')
ON CONFLICT (ins_code) DO UPDATE SET concern_level = EXCLUDED.concern_level, accurate_description = EXCLUDED.accurate_description;
INSERT INTO additive_rulebook (additive_code, ins_number, canonical_name, functional_class, jurisdiction, status, label_requirement, regulation_title)
VALUES ('E435', '435', 'Polysorbate 60', 'EMULSIFIER', 'US', 'RESTRICTED', 'Strict usage thresholds.', 'FDA 21 CFR 172.836')
ON CONFLICT DO NOTHING;
INSERT INTO additive_rulebook (additive_code, ins_number, canonical_name, functional_class, jurisdiction, status, label_requirement, regulation_title)
VALUES ('E435', '435', 'Polysorbate 60', 'EMULSIFIER', 'EU', 'RESTRICTED', 'Restricted usage limits.', 'EU Reg 1333/2008')
ON CONFLICT DO NOTHING;
INSERT INTO canonical_additives (id, ins_code, e_number, cas_number, primary_name, category, risk_level, base_risk_weight, cspi_rating, description)
VALUES ('ing_436', '436', 'E436', '9005-71-4', 'Polysorbate 65', 'EMULSIFIER', 'MEDIUM', -8, 'CAUTION', 'Polyoxyethylene sorbitan emulsifier. Linked to metabolic syndrome and inflammatory bowel diseases in animal models.')
ON CONFLICT (id) DO UPDATE SET risk_level = EXCLUDED.risk_level, cspi_rating = EXCLUDED.cspi_rating;
INSERT INTO additive_synonyms (additive_id, synonym_clean, language_code, is_primary)
VALUES ('ing_436', 'polysorbate 65', 'en', TRUE)
ON CONFLICT DO NOTHING;
INSERT INTO regulatory_bans (additive_id, jurisdiction_code, status, restriction_details, regulation_ref)
VALUES ('ing_436', 'US', 'RESTRICTED', 'Restricted usage levels.', 'FDA 21 CFR 172.838')
ON CONFLICT (additive_id, jurisdiction_code, scope_category) DO NOTHING;
INSERT INTO regulatory_bans (additive_id, jurisdiction_code, status, restriction_details, regulation_ref)
VALUES ('ing_436', 'EU', 'RESTRICTED', 'Restricted max limits.', 'EU Reg 1333/2008')
ON CONFLICT (additive_id, jurisdiction_code, scope_category) DO NOTHING;
INSERT INTO additive_reference (ins_code, common_name, origin, category, fssai_status, efsa_status, fda_status, adi_value, concern_level, accurate_description, source_url, source_citation)
VALUES ('436', 'Polysorbate 65', 'synthetic', 'EMULSIFIER', 'RESTRICTED', 'RESTRICTED', 'RESTRICTED', '0-5 mg/kg body weight', 'MEDIUM', 'Polyoxyethylene sorbitan emulsifier. Linked to metabolic syndrome and inflammatory bowel diseases in animal models.', 'https://www.fssai.gov.in', 'Official Safety Evaluation')
ON CONFLICT (ins_code) DO UPDATE SET concern_level = EXCLUDED.concern_level, accurate_description = EXCLUDED.accurate_description;
INSERT INTO additive_rulebook (additive_code, ins_number, canonical_name, functional_class, jurisdiction, status, label_requirement, regulation_title)
VALUES ('E436', '436', 'Polysorbate 65', 'EMULSIFIER', 'US', 'RESTRICTED', 'Restricted usage levels.', 'FDA 21 CFR 172.838')
ON CONFLICT DO NOTHING;
INSERT INTO additive_rulebook (additive_code, ins_number, canonical_name, functional_class, jurisdiction, status, label_requirement, regulation_title)
VALUES ('E436', '436', 'Polysorbate 65', 'EMULSIFIER', 'EU', 'RESTRICTED', 'Restricted max limits.', 'EU Reg 1333/2008')
ON CONFLICT DO NOTHING;
INSERT INTO canonical_additives (id, ins_code, e_number, cas_number, primary_name, category, risk_level, base_risk_weight, cspi_rating, description)
VALUES ('ing_olestra', 'olestra', '', '118476-30-0', 'Olestra', 'OTHER', 'HIGH', -20, 'AVOID', 'Zero-calorie synthetic fat substitute. Inhibits absorption of fat-soluble vitamins (A, D, E, K) and carotenoids. Linked to severe cramping.')
ON CONFLICT (id) DO UPDATE SET risk_level = EXCLUDED.risk_level, cspi_rating = EXCLUDED.cspi_rating;
INSERT INTO additive_synonyms (additive_id, synonym_clean, language_code, is_primary)
VALUES ('ing_olestra', 'olestra', 'en', TRUE)
ON CONFLICT DO NOTHING;
INSERT INTO regulatory_bans (additive_id, jurisdiction_code, status, restriction_details, regulation_ref)
VALUES ('ing_olestra', 'US', 'RESTRICTED', 'FDA approved but carries warnings of gastrointestinal distress and vitamin depletion.', 'FDA 21 CFR 172.867')
ON CONFLICT (additive_id, jurisdiction_code, scope_category) DO NOTHING;
INSERT INTO regulatory_bans (additive_id, jurisdiction_code, status, restriction_details, regulation_ref)
VALUES ('ing_olestra', 'EU', 'BANNED', 'Not authorized / banned for use in the EU.', 'EU Reg 1333/2008')
ON CONFLICT (additive_id, jurisdiction_code, scope_category) DO NOTHING;
INSERT INTO additive_reference (ins_code, common_name, origin, category, fssai_status, efsa_status, fda_status, adi_value, concern_level, accurate_description, source_url, source_citation)
VALUES ('olestra', 'Olestra', 'synthetic', 'OTHER', 'RESTRICTED', 'BANNED', 'RESTRICTED', '0-5 mg/kg body weight', 'HIGH', 'Zero-calorie synthetic fat substitute. Inhibits absorption of fat-soluble vitamins (A, D, E, K) and carotenoids. Linked to severe cramping.', 'https://www.fssai.gov.in', 'Official Safety Evaluation')
ON CONFLICT (ins_code) DO UPDATE SET concern_level = EXCLUDED.concern_level, accurate_description = EXCLUDED.accurate_description;
INSERT INTO additive_rulebook (additive_code, ins_number, canonical_name, functional_class, jurisdiction, status, label_requirement, regulation_title)
VALUES ('OLESTRA', 'olestra', 'Olestra', 'OTHER', 'US', 'RESTRICTED', 'FDA approved but carries warnings of gastrointestinal distress and vitamin depletion.', 'FDA 21 CFR 172.867')
ON CONFLICT DO NOTHING;
INSERT INTO additive_rulebook (additive_code, ins_number, canonical_name, functional_class, jurisdiction, status, label_requirement, regulation_title)
VALUES ('OLESTRA', 'olestra', 'Olestra', 'OTHER', 'EU', 'BANNED', 'Not authorized / banned for use in the EU.', 'EU Reg 1333/2008')
ON CONFLICT DO NOTHING;
INSERT INTO canonical_additives (id, ins_code, e_number, cas_number, primary_name, category, risk_level, base_risk_weight, cspi_rating, description)
VALUES ('ing_degme', 'degme', '', '111-90-0', 'Diethylene Glycol Monoethyl Ether', 'OTHER', 'HIGH', -20, 'AVOID', 'Synthetic solvent and carrier agent. Suspected kidney/renal and central nervous system toxicant at elevated levels.')
ON CONFLICT (id) DO UPDATE SET risk_level = EXCLUDED.risk_level, cspi_rating = EXCLUDED.cspi_rating;
INSERT INTO additive_synonyms (additive_id, synonym_clean, language_code, is_primary)
VALUES ('ing_degme', 'diethylene glycol monoethyl ether', 'en', TRUE)
ON CONFLICT DO NOTHING;
INSERT INTO regulatory_bans (additive_id, jurisdiction_code, status, restriction_details, regulation_ref)
VALUES ('ing_degme', 'US', 'RESTRICTED', 'Permitted only as solvent/carrier under strict limits.', 'FDA 21 CFR 172.712')
ON CONFLICT (additive_id, jurisdiction_code, scope_category) DO NOTHING;
INSERT INTO regulatory_bans (additive_id, jurisdiction_code, status, restriction_details, regulation_ref)
VALUES ('ing_degme', 'EU', 'BANNED', 'Not authorized for food use in the EU.', 'EU Reg 1333/2008')
ON CONFLICT (additive_id, jurisdiction_code, scope_category) DO NOTHING;
INSERT INTO additive_reference (ins_code, common_name, origin, category, fssai_status, efsa_status, fda_status, adi_value, concern_level, accurate_description, source_url, source_citation)
VALUES ('degme', 'Diethylene Glycol Monoethyl Ether', 'synthetic', 'OTHER', 'RESTRICTED', 'BANNED', 'RESTRICTED', '0-5 mg/kg body weight', 'HIGH', 'Synthetic solvent and carrier agent. Suspected kidney/renal and central nervous system toxicant at elevated levels.', 'https://www.fssai.gov.in', 'Official Safety Evaluation')
ON CONFLICT (ins_code) DO UPDATE SET concern_level = EXCLUDED.concern_level, accurate_description = EXCLUDED.accurate_description;
INSERT INTO additive_rulebook (additive_code, ins_number, canonical_name, functional_class, jurisdiction, status, label_requirement, regulation_title)
VALUES ('DEGME', 'degme', 'Diethylene Glycol Monoethyl Ether', 'OTHER', 'US', 'RESTRICTED', 'Permitted only as solvent/carrier under strict limits.', 'FDA 21 CFR 172.712')
ON CONFLICT DO NOTHING;
INSERT INTO additive_rulebook (additive_code, ins_number, canonical_name, functional_class, jurisdiction, status, label_requirement, regulation_title)
VALUES ('DEGME', 'degme', 'Diethylene Glycol Monoethyl Ether', 'OTHER', 'EU', 'BANNED', 'Not authorized for food use in the EU.', 'EU Reg 1333/2008')
ON CONFLICT DO NOTHING;
COMMIT;