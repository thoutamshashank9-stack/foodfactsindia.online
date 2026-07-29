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

/**
 * Pure deterministic mathematical calculation engine for food product safety rating.
 * Returns reproducible scores (0-100) and exact mathematical breakdown items.
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
      factor: `High Added Sugar (${nutrition.addedSugarG}g)`,
      points: -pts,
      rationale: `Exceeds WHO 5g daily baseline limit by ${excessSugar}g (-2 pts/g over 5g).`,
      authoritySource: 'WHO & FSSAI Guidelines'
    });
  }

  // B. Sodium Penalty (> 300mg -> -1 pt per 50mg over 300mg)
  if (nutrition.sodiumMg > 300) {
    const excessSodium = Math.floor((nutrition.sodiumMg - 300) / 50);
    const pts = Math.min(20, excessSodium * 1);
    if (pts > 0) {
      nutritionalDeductions += pts;
      scoreBreakdown.push({
        type: 'DEDUCTION',
        category: 'NUTRITION',
        factor: `Elevated Sodium (${nutrition.sodiumMg}mg)`,
        points: -pts,
        rationale: `Exceeds FSSAI 300mg benchmark by ${nutrition.sodiumMg - 300}mg (-1 pt per 50mg).`,
        authoritySource: 'FSSAI & US FDA Guidelines'
      });
    }
  }

  // C. Saturated Fat Penalty (> 3g -> -1 pt per gram over 3g)
  if (nutrition.saturatedFatG > 3) {
    const excessSatFat = Math.floor(nutrition.saturatedFatG - 3);
    const pts = Math.min(15, excessSatFat * 1);
    if (pts > 0) {
      nutritionalDeductions += pts;
      scoreBreakdown.push({
        type: 'DEDUCTION',
        category: 'NUTRITION',
        factor: `High Saturated Fat (${nutrition.saturatedFatG}g)`,
        points: -pts,
        rationale: `Exceeds 3g baseline limit by ${excessSatFat}g (-1 pt per gram).`,
        authoritySource: 'ICMR-NIN Dietary Guidelines'
      });
    }
  }

  // D. Trans Fat Penalty (> 0g -> -10 pts flat penalty)
  if (nutrition.transFatG > 0) {
    const pts = 10;
    nutritionalDeductions += pts;
    scoreBreakdown.push({
      type: 'DEDUCTION',
      category: 'NUTRITION',
      factor: `Contains Trans Fat (${nutrition.transFatG}g)`,
      points: -pts,
      rationale: `Trans fats carry severe cardiovascular risks. Global ban consensus.`,
      authoritySource: 'WHO REPLACE Trans Fat Strategy'
    });
  }

  score -= nutritionalDeductions;

  // --- 2. ADDITIVE & INGREDIENT DEDUCTIONS ---
  let additiveDeductions = 0;

  ingredients.forEach((ing) => {
    const bannedMarkets = ing.regulatoryRecords.filter((r) => r.status === 'BANNED');
    const restrictedMarkets = ing.regulatoryRecords.filter((r) => r.status === 'RESTRICTED');

    if (bannedMarkets.length >= 1) {
      const pts = 15;
      additiveDeductions += pts;
      scoreBreakdown.push({
        type: 'DEDUCTION',
        category: 'ADDITIVE',
        factor: `Banned Additive: ${ing.canonicalName} (${ing.eNumber || ing.insNumber || 'INS'})`,
        points: -pts,
        rationale: ing.description || `Banned in ${bannedMarkets.map((b) => b.countryName).join(', ')}. ${bannedMarkets[0]?.restrictionDetails || ''}`,
        authoritySource: ing.citations[0]?.title || 'Global Regulatory Intelligence DB'
      });
    } else if (ing.riskLevel === 'HIGH' || restrictedMarkets.length >= 2) {
      const pts = 15;
      additiveDeductions += pts;
      scoreBreakdown.push({
        type: 'DEDUCTION',
        category: 'ADDITIVE',
        factor: `High Concern Additive: ${ing.canonicalName}`,
        points: -pts,
        rationale: ing.description || `Restricted in ${restrictedMarkets.map((r) => r.countryCode).join(', ')}.`,
        authoritySource: ing.citations[0]?.title || 'EFSA / FSSAI Official Review'
      });
    } else if (ing.riskLevel === 'MEDIUM') {
      const pts = 8;
      additiveDeductions += pts;
      scoreBreakdown.push({
        type: 'DEDUCTION',
        category: 'ADDITIVE',
        factor: `Moderate Concern: ${ing.canonicalName}`,
        points: -pts,
        rationale: ing.description || `Functional food additive requiring intake awareness.`,
        authoritySource: ing.citations[0]?.title || 'Official Safety Evaluation'
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
      rationale: `Provides dietary fiber supporting digestive and gut health.`,
      authoritySource: 'Dietary Guidelines'
    });
  }

  if (nutrition.proteinG >= 10) {
    positiveAdjustments += 5;
    scoreBreakdown.push({
      type: 'ADDITION',
      category: 'POSITIVE_NUTRIENT',
      factor: `Good Protein Source (${nutrition.proteinG}g)`,
      points: 5,
      rationale: `High protein content contributing to muscle repair and satiety.`,
      authoritySource: 'ICMR Protein Recommendation'
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
      rationale: 'Minimal ingredient list containing no synthetic additives or ultra-processed fats.',
      authoritySource: 'NOVA Classification System'
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
