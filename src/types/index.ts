export type RiskLevel = 'LOW' | 'MEDIUM' | 'HIGH' | 'EXCELLENT';

export type RegulatoryStatus = 'APPROVED' | 'RESTRICTED' | 'BANNED';

export interface RegulatoryRecord {
  countryCode: 'IN' | 'EU' | 'UK' | 'US' | 'JP' | 'CODEX';
  countryName: string;
  flagEmoji: string;
  status: RegulatoryStatus;
  year?: number;
  restrictionDetails?: string;
  regulationRef: string;
}

export interface ResearchCitation {
  id: string;
  title: string;
  journal: string;
  year: number;
  doi: string;
  summary: string;
  evidenceStrength: 'STRONG' | 'MODERATE' | 'PRELIMINARY';
}

export interface WhoNutritionFlag {
  nutrient: string;
  flagType: 'HIGH_SODIUM' | 'HIGH_FREE_SUGAR' | 'HIGH_SATURATED_FAT' | 'CONTAINS_TRANS_FAT' | 'LOW_FIBER';
  label: string;
  valueDeclared: string;
  whoBenchmark: string;
  severity: 'CRITICAL' | 'WARNING' | 'INFO';
  citation: string;
}

export interface LabelWarningCard {
  id: string;
  title: string;
  type: 'SOUTHAMPTON_COLOUR' | 'EU_BAN' | 'FDA_REVOCATION' | 'PHENYLALANINE_WARNING' | 'SULPHITE_SENSITIVITY' | 'OTHER';
  appliedAdditives: string[];
  warningText: string;
  jurisdiction: string;
  authorityRef: string;
}

export interface Ingredient {
  id: string;
  canonicalName: string;
  scientificName?: string;
  synonyms: string[];
  insNumber?: string;
  eNumber?: string;
  category: 'PRESERVATIVE' | 'ARTIFICIAL_COLOR' | 'SWEETENER' | 'EMULSIFIER' | 'FLAVOR_ENHANCER' | 'THICKENER' | 'WHOLE_FOOD' | 'PROCESSING_AID' | 'OTHER';
  riskLevel: RiskLevel;
  baseRiskWeight: number; // -15 to +5
  description: string;
  processingLevel: 'NOVA_1_UNPROCESSED' | 'NOVA_2_PROCESSED_INGREDIENT' | 'NOVA_3_PROCESSED_FOOD' | 'NOVA_4_ULTRA_PROCESSED';
  regulatoryRecords: RegulatoryRecord[];
  citations: ResearchCitation[];
}

export interface NutritionFacts {
  calories: number; // kcal
  servingSize: string; // e.g. "100g"
  totalFatG: number;
  saturatedFatG: number;
  transFatG: number;
  sodiumMg: number;
  totalCarbsG: number;
  fiberG: number;
  totalSugarG: number;
  addedSugarG: number;
  proteinG: number;
  micronutrients?: { name: string; amount: string; dvPercentage: number }[];
}

export interface ScoreBreakdownItem {
  type: 'DEDUCTION' | 'ADDITION';
  category: 'NUTRITION' | 'ADDITIVE' | 'PROCESSING' | 'POSITIVE_NUTRIENT';
  factor: string;
  points: number;
  rationale: string;
  authoritySource: string;
}

export type NutriScoreGrade = 'A' | 'B' | 'C' | 'D' | 'E';
export type FdaSeverityLevel = 'LOW' | 'MED' | 'HIGH';

export interface NutriScoreResult {
  grade: NutriScoreGrade;
  score: number; // Raw points (-15 to +40)
  negativePoints: number;
  positivePoints: number;
  isBeverage: boolean;
  breakdown: {
    energyPoints: number;
    sugarsPoints: number;
    satFatPoints: number;
    sodiumPoints: number;
    fiberPoints: number;
    proteinPoints: number;
    fvlnPoints: number; // Fruits, Veggies, Legumes, Nuts %
  };
}

export interface FdaFrontOfPackageResult {
  saturatedFat: { level: FdaSeverityLevel; dvPercentage: number; gramsPerServing: number };
  sodium: { level: FdaSeverityLevel; dvPercentage: number; mgPerServing: number };
  addedSugar: { level: FdaSeverityLevel; dvPercentage: number; gramsPerServing: number };
}

export type LatAmWarningId = 
  | 'HIGH_SUGAR' 
  | 'HIGH_SODIUM' 
  | 'HIGH_SAT_FAT' 
  | 'HIGH_CALORIES' 
  | 'HIGH_TRANS_FAT' 
  | 'CONTAINS_SWEETENERS'
  | 'CONTAINS_CAFFEINE';

export interface LatAmOctagonWarning {
  id: LatAmWarningId;
  mexicoLabel: string; // e.g. "EXCESO SODIO"
  chileLabel: string;  // e.g. "ALTO EN SODIO"
  englishSubtitle: string; // e.g. "High in Sodium"
  thresholdDeclared: string; // e.g. "≥ 1mg/kcal or ≥ 300mg/100g"
}

export interface InternationalRatings {
  nutriScore: NutriScoreResult;
  fdaLabel: FdaFrontOfPackageResult;
  warningOctagons: LatAmOctagonWarning[];
}

export interface TransparencyReport {
  productId: string;
  productName: string;
  brand: string;
  manufacturer: string;
  category: string;
  barcode: string;
  /** @deprecated Image URLs are no longer loaded from DB. Rendered via Edge Proxy /api/img/[barcode] */
  imageUrl?: string;
  /** @deprecated Deprecated in favor of Edge Proxy /api/img/[barcode] */
  imageFrontUrl?: string;
  imageIngredientsUrl?: string;
  imageNutritionUrl?: string;
  packageSize: string;
  servingSize: string;
  
  deterministicScore: number;
  scoreBreakdown: ScoreBreakdownItem[];

  internationalRatings?: InternationalRatings;
  
  executiveSummary: {
    grade: 'A+' | 'A' | 'B' | 'C' | 'D' | 'F';
    verdictTitle: string;
    keyTakeaways: string[];
    riskSummaryText: string;
    processingNovaClass: number; // 1-4
  };

  ingredientsList: {
    ingredient: Ingredient;
    rawName: string;
    position: number;
    isControversial: boolean;
  }[];

  nutrition: NutritionFacts;

  whoNutritionFlags?: WhoNutritionFlag[];
  labelWarnings?: LabelWarningCard[];
  
  globalRegulatoryOverview: {
    countryCode: 'IN' | 'EU' | 'UK' | 'US' | 'JP' | 'CODEX';
    countryName: string;
    flagEmoji: string;
    bannedCount: number;
    restrictedCount: number;
    approvedCount: number;
  }[];

  evidenceConfidence: {
    confidenceScore: number; // 0 - 100%
    peerReviewedStudiesCount: number;
    regulatoryBodiesCount: number;
    lastUpdated: string;
    verificationStatus?: 'verified_official' | 'extracted_needs_review';
  };
}

export interface AnalysisPipelineStep {
  id: number;
  label: string;
  iconName: string;
  status: 'PENDING' | 'RUNNING' | 'COMPLETED';
  detail: string;
}

export type ResolvedItem =
  | { kind: 'food'; product: TransparencyReport }
  | { kind: 'non_food'; category: string; productName?: string; brand?: string; barcode: string }
  | { kind: 'unknown'; barcode: string };

