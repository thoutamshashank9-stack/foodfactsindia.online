/**
  FoodLens AI — Relational PostgreSQL Schema Definition
  Supports Neon / Supabase / Prisma / Drizzle ORM
*/

export interface DbIngredient {
  id: string; // UUID or string PK
  canonical_name: string;
  scientific_name?: string;
  ins_number?: string;
  e_number?: string;
  synonyms: string[]; // JSONB / Array
  category: string;
  base_risk_weight: number;
  processing_level: string; // NOVA 1-4
  created_at: string;
}

export interface DbRegulatoryRecord {
  id: string;
  ingredient_id: string; // FK -> ingredients.id
  country_code: 'IN' | 'EU' | 'US' | 'JP';
  status: 'APPROVED' | 'RESTRICTED' | 'BANNED';
  reason?: string;
  year?: number;
  regulation_ref: string;
  source_url: string;
  verified_at: string;
}

export interface DbEvidenceRecord {
  id: string;
  ingredient_id: string;
  claim_type: 'CARCINOGENICITY' | 'HYPERACTIVITY' | 'IMMUNOTOXICITY' | 'GENOTOXICITY' | 'GENERAL';
  summary: string;
  doi?: string;
  pmid?: string;
  evidence_strength: 'STRONG' | 'MODERATE' | 'PRELIMINARY';
  child_relevant: boolean;
}

export interface DbAdiRecord {
  id: string;
  ingredient_id: string;
  adi_mg_per_kg: number;
  authority: 'JECFA' | 'EFSA' | 'FDA' | 'FSSAI';
  notes?: string;
}

export interface DbProduct {
  id: string;
  barcode: string; // Indexed Unique
  name: string;
  brand: string;
  category: string;
  country: string;
  image_url: string;
  package_size: string;
  serving_size: string;
  nutrition_json: string; // JSONB
  raw_ingredients_text: string;
  last_analyzed_at: string;
}

export interface DbProductIngredient {
  product_id: string;
  ingredient_id: string;
  sequence: number;
  raw_token: string;
}

export interface DbAnalysisReport {
  id: string;
  product_id: string;
  score: number;
  score_engine_version: string;
  breakdown_json: string; // JSONB
  issues_json: string; // JSONB
  created_at: string;
}

export interface DbFopRule {
  id: string;
  country_code: string;
  nutrient: 'SUGAR' | 'SODIUM' | 'SAT_FAT' | 'TRANS_FAT';
  threshold_per_100g: number;
  warning_label_text: string;
  source_url: string;
}

export interface DbGoldenDataset {
  id: string;
  product_id: string;
  expected_score: number;
  expected_flags: string[];
  reviewer: string;
  verified_at: string;
}
