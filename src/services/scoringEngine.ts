import { Ingredient, NutritionFacts, ScoreBreakdownItem } from '../types';

export interface ScoringEngineResult {
  finalScore: number;
  grade: 'A+' | 'A' | 'B' | 'C' | 'D' | 'F';
  scoreBreakdown: ScoreBreakdownItem[];
  nutritionalDeductionsTotal: number;
  additiveDeductionsTotal: number;
  positiveAdjustmentsTotal: number;
  novaClass: number; // 1 to 4
}

export interface RatingGateResult {
  isEligibleForRatings: boolean;
  blockReason?: string;
}

/**
 * 🛡️ 5-Layer Multi-Point Production Rating Gate
 * Gating checks:
 * 1. AI Confidence Threshold (>= 0.70)
 * 2. Source Quality (Ungrounded AI estimates prohibited from ratings)
 * 3. Label Field Completeness (Calories and serving size required)
 * 4. Nutrient Sanity Checks (e.g. Saturated Fat cannot exceed Total Fat)
 * 5. Category Eligibility (Energy Drinks & Supplements excluded from standard food models)
 */
export function evaluateRatingGate(
  confidenceScore: number,
  nutrition: NutritionFacts,
  sourceType: string,
  category: string = 'Staples'
): RatingGateResult {
  // Gate 1: Confidence Threshold
  if (confidenceScore < 0.70) {
    return { isEligibleForRatings: false, blockReason: `AI Confidence (${(confidenceScore * 100).toFixed(0)}%) is below minimum production threshold (70%)` };
  }

  // Gate 2: Source Quality Gate
  if (sourceType === 'UNGROUNDED_AI') {
    return { isEligibleForRatings: false, blockReason: 'Ungrounded AI estimation cannot issue public health rating scores' };
  }

  // Gate 3: Field Completeness
  if (!nutrition.servingSize || nutrition.calories === 0) {
    return { isEligibleForRatings: false, blockReason: 'Incomplete nutrition label data (calories or serving size missing)' };
  }

  // Gate 4: Nutrient Sanity Check
  if (nutrition.saturatedFatG > nutrition.totalFatG && nutrition.totalFatG > 0) {
    return { isEligibleForRatings: false, blockReason: 'Nutrient sanity check failed: Saturated fat exceeds total fat' };
  }

  // Gate 5: Category Eligibility (Exclude Energy drinks & Supplements from standard food scoring)
  const EXCLUDED_CATEGORIES = ['Energy Drinks', 'Dietary Supplements', 'Therapeutic Formulas', 'Supplements'];
  if (EXCLUDED_CATEGORIES.some(cat => category.toLowerCase().includes(cat.toLowerCase()))) {
    return { isEligibleForRatings: false, blockReason: `Category '${category}' is excluded from standard food scoring algorithms` };
  }

  return { isEligibleForRatings: true };
}

/**
 * Pure deterministic mathematical calculation engine for food product safety rating.
 * Computes reproducible, audited scores (0-100) and explicit authority-attributed score breakdowns.
 *
 * Distinctly labels FoodLens Single-Serving Product Heuristics vs Official WHO Population Targets.
 */
export function calculateDeterministicScore(
  ingredients: Ingredient[],
  nutrition: NutritionFacts
): ScoringEngineResult {
  let score = 100;
  const scoreBreakdown: ScoreBreakdownItem[] = [];

  // --- 1. NUTRITIONAL DEDUCTIONS ---
  let nutritionalDeductions = 0;

  // A. Added Sugar Penalty (> 5g -> -2 pts per gram over 5g)
  if (nutrition.addedSugarG > 5) {
    const excessSugar = Math.floor(nutrition.addedSugarG - 5);
    const pts = Math.min(40, excessSugar * 2);
    nutritionalDeductions += pts;
    scoreBreakdown.push({
      type: 'DEDUCTION',
      category: 'NUTRITION',
      factor: `Elevated Added Sugar (${nutrition.addedSugarG}g)`,
      points: -pts,
      rationale: `Exceeds FoodFactsIndia single-serving heuristic threshold of 5g by ${excessSugar}g (-2 pts/g). WHO Context: Reduce free sugars to < 10% daily total energy intake.`,
      authoritySource: 'FoodFactsIndia Heuristic (WHO Sugars Guideline 2015 Context)'
    });
  }

  // B. Sodium Penalty (> 300mg -> -1 pt per 50mg over 300mg)
  if (nutrition.sodiumMg > 300) {
    const excessSodium = Math.floor((nutrition.sodiumMg - 300) / 50);
    const pts = Math.min(25, excessSodium * 1);
    if (pts > 0) {
      nutritionalDeductions += pts;
      scoreBreakdown.push({
        type: 'DEDUCTION',
        category: 'NUTRITION',
        factor: `Elevated Sodium (${nutrition.sodiumMg}mg)`,
        points: -pts,
        rationale: `Exceeds FoodFactsIndia single-serving sodium heuristic threshold of 300mg by ${nutrition.sodiumMg - 300}mg (-1 pt / 50mg). WHO Context: Adult daily target < 2,000 mg/day.`,
        authoritySource: 'FoodFactsIndia Heuristic (WHO Sodium Guideline 2012 Context)'
      });
    }
  }

  // C. Saturated Fat Penalty (> 3g -> -1 pt per gram over 3g)
  if (nutrition.saturatedFatG > 3) {
    const excessSatFat = Math.floor(nutrition.saturatedFatG - 3);
    const pts = Math.min(20, excessSatFat * 1);
    if (pts > 0) {
      nutritionalDeductions += pts;
      scoreBreakdown.push({
        type: 'DEDUCTION',
        category: 'NUTRITION',
        factor: `High Saturated Fat (${nutrition.saturatedFatG}g)`,
        points: -pts,
        rationale: `Exceeds FoodFactsIndia single-serving saturated fat heuristic threshold of 3g by ${excessSatFat}g (-1 pt/g). WHO Context: Limit to < 10% daily total energy intake.`,
        authoritySource: 'FoodFactsIndia Heuristic (WHO Saturated Fat Guideline 2023 Context)'
      });
    }
  }

  // D. Trans Fat Penalty (> 0g -> -35 pts flat conservative heuristic deduction)
  if (nutrition.transFatG > 0) {
    const pts = 35;
    nutritionalDeductions += pts;
    scoreBreakdown.push({
      type: 'DEDUCTION',
      category: 'NUTRITION',
      factor: `Contains Industrially Produced Trans Fat (${nutrition.transFatG}g)`,
      points: -pts,
      rationale: `Presence of industrially produced trans fatty acids carries severe cardiovascular risk. WHO Target: Global elimination (< 1% total energy intake).`,
      authoritySource: 'WHO REPLACE Trans Fat Action Package (2018)'
    });
  }

  score -= nutritionalDeductions;

  // --- 2. ADDITIVE & INGREDIENT DEDUCTIONS ---
  let additiveDeductions = 0;

  ingredients.forEach((ing) => {
    const bannedMarkets = ing.regulatoryRecords.filter((r) => r.status === 'BANNED');
    const restrictedMarkets = ing.regulatoryRecords.filter((r) => r.status === 'RESTRICTED');

    if (bannedMarkets.length >= 1) {
      const pts = 25;
      additiveDeductions += pts;
      scoreBreakdown.push({
        type: 'DEDUCTION',
        category: 'ADDITIVE',
        factor: `Banned Additive: ${ing.canonicalName} (${ing.eNumber || ing.insNumber || 'INS'})`,
        points: -pts,
        rationale: ing.description || `Banned or authorisation revoked in ${bannedMarkets.map((b) => b.countryName).join(', ')}. ${bannedMarkets[0]?.restrictionDetails || ''}`,
        authoritySource: ing.citations[0]?.title || 'EFSA / FDA Official Revocation Regulation'
      });
    } else if (ing.riskLevel === 'HIGH' || restrictedMarkets.length >= 2) {
      const pts = 15;
      additiveDeductions += pts;
      scoreBreakdown.push({
        type: 'DEDUCTION',
        category: 'ADDITIVE',
        factor: `High Concern Additive: ${ing.canonicalName}`,
        points: -pts,
        rationale: ing.description || `Subject to mandatory warning labels or ADI restrictions in ${restrictedMarkets.map((r) => r.countryCode).join(', ')}.`,
        authoritySource: ing.citations[0]?.title || 'EFSA / FSSAI Regulatory Review'
      });
    } else if (ing.riskLevel === 'MEDIUM') {
      const pts = 8;
      additiveDeductions += pts;
      scoreBreakdown.push({
        type: 'DEDUCTION',
        category: 'ADDITIVE',
        factor: `Moderate Concern Additive: ${ing.canonicalName}`,
        points: -pts,
        rationale: ing.description || `Functional food additive with specified Acceptable Daily Intake (ADI) boundaries.`,
        authoritySource: ing.citations[0]?.title || 'JECFA / FSSAI Safety Evaluation'
      });
    }
  });

  score -= additiveDeductions;

  // --- 3. POSITIVE NUTRIENT ADJUSTMENTS ---
  let positiveAdjustments = 0;

  if (nutrition.fiberG >= 3) {
    positiveAdjustments += 5;
    scoreBreakdown.push({
      type: 'ADDITION',
      category: 'POSITIVE_NUTRIENT',
      factor: `High Fiber Content (${nutrition.fiberG}g)`,
      points: 5,
      rationale: `Provides dietary fiber supporting gut microbiota and digestive health.`,
      authoritySource: 'WHO Carbohydrate Intake Guideline (2023)'
    });
  }

  if (nutrition.proteinG >= 10) {
    positiveAdjustments += 5;
    scoreBreakdown.push({
      type: 'ADDITION',
      category: 'POSITIVE_NUTRIENT',
      factor: `Good Protein Source (${nutrition.proteinG}g)`,
      points: 5,
      rationale: `High protein density contributing to muscle maintenance and satiety.`,
      authoritySource: 'ICMR-NIN Dietary Guidelines for Indians'
    });
  }

  const ultraProcessedCount = ingredients.filter(
    (i) => i.processingLevel === 'NOVA_4_ULTRA_PROCESSED'
  ).length;

  if (ingredients.length > 0 && ingredients.length <= 5 && ultraProcessedCount === 0) {
    positiveAdjustments += 5;
    scoreBreakdown.push({
      type: 'ADDITION',
      category: 'POSITIVE_NUTRIENT',
      factor: 'Clean Label Whole Food Composition',
      points: 5,
      rationale: 'Minimal ingredient list containing zero synthetic additives or ultra-processed fats.',
      authoritySource: 'NOVA System (FAO / NUPENS)'
    });
  }

  score += positiveAdjustments;

  // Clamp final score between 0 and 100
  const finalScore = Math.max(0, Math.min(100, Math.round(score)));

  // Calculate Letter Grade
  let grade: 'A+' | 'A' | 'B' | 'C' | 'D' | 'F' = 'C';
  if (finalScore >= 90) grade = 'A+';
  else if (finalScore >= 80) grade = 'A';
  else if (finalScore >= 65) grade = 'B';
  else if (finalScore >= 50) grade = 'C';
  else if (finalScore >= 35) grade = 'D';
  else grade = 'F';

  // Determine NOVA Processing Class
  let novaClass = 1;
  if (ultraProcessedCount >= 2) novaClass = 4;
  else if (ultraProcessedCount === 1) novaClass = 3;
  else if (ingredients.some((i) => i.processingLevel === 'NOVA_2_PROCESSED_INGREDIENT')) novaClass = 2;

  return {
    finalScore,
    grade,
    scoreBreakdown,
    nutritionalDeductionsTotal: nutritionalDeductions,
    additiveDeductionsTotal: additiveDeductions,
    positiveAdjustmentsTotal: positiveAdjustments,
    novaClass
  };
}
