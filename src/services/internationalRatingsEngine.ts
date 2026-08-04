import { 
  NutritionFacts, 
  Ingredient, 
  NutriScoreResult, 
  NutriScoreGrade, 
  FdaFrontOfPackageResult, 
  FdaSeverityLevel, 
  LatAmOctagonWarning, 
  InternationalRatings 
} from '../types';

const SWEETENER_REGEX = /sucralose|acesulfame|aspartame|stevia|saccharin|erythritol|sorbitol|maltitol|neotame|advantame|cyclamate|isomalt|xylitol|lactitol/i;
const CAFFEINE_REGEX = /caffeine|coffee extract|tea extract|guarana|taurine|maté|kola nut/i;

/**
 * Scans ingredient canonical names, raw names, and descriptions for non-nutritive sweeteners and caffeine.
 */
export function detectAdditives(ingredients: (Ingredient | string)[]): { hasSweeteners: boolean; hasCaffeine: boolean } {
  const textStrings: string[] = ingredients.map((ing) => {
    if (typeof ing === 'string') return ing;
    return `${ing.canonicalName} ${ing.synonyms?.join(' ') || ''} ${ing.description || ''}`;
  });
  const fullText = textStrings.join(' ');
  return {
    hasSweeteners: SWEETENER_REGEX.test(fullText),
    hasCaffeine: CAFFEINE_REGEX.test(fullText),
  };
}

/**
 * Estimates Fruit, Vegetable, Legume, Nut (FVLN) percentage from ingredient list if not explicitly declared.
 */
export function estimateFvlnPercentage(ingredients: (Ingredient | string)[]): number {
  const fvlnKeywords = /fruit|vegetable|legume|nut|apple|banana|berry|orange|mango|tomato|spinach|carrot|pea|bean|lentil|almond|cashew|walnut|hazelnut|peanut/i;
  
  if (ingredients.length === 0) return 0;
  
  const matches = ingredients.filter((ing) => {
    const str = typeof ing === 'string' ? ing : ing.canonicalName;
    return fvlnKeywords.test(str);
  });

  // If top ingredient is FVLN, estimate > 50%. If 1st & 2nd are FVLN, estimate > 80%.
  if (matches.length === 0) return 0;
  const firstIsFvln = typeof ingredients[0] === 'string' ? fvlnKeywords.test(ingredients[0]) : fvlnKeywords.test(ingredients[0].canonicalName);
  const secondIsFvln = ingredients.length > 1 && (typeof ingredients[1] === 'string' ? fvlnKeywords.test(ingredients[1]) : fvlnKeywords.test(ingredients[1].canonicalName));

  if (firstIsFvln && secondIsFvln) return 85;
  if (firstIsFvln) return 50;
  return 25;
}

/**
 * 🇪🇺 EU Nutri-Score Engine (2023/2024 Updated Rules)
 */
export function calculateNutriScore(
  nutrition: NutritionFacts,
  category: string = '',
  ingredients: (Ingredient | string)[] = []
): NutriScoreResult {
  const isBeverage = /beverage|drink|juice|soda|water|tea|coffee|milkshake|syrup/i.test(category);
  const isWater = /water|mineral water|spring water/i.test(category);

  if (isWater) {
    return {
      grade: 'A',
      score: -15,
      negativePoints: 0,
      positivePoints: 15,
      isBeverage: true,
      breakdown: {
        energyPoints: 0,
        sugarsPoints: 0,
        satFatPoints: 0,
        sodiumPoints: 0,
        fiberPoints: 0,
        proteinPoints: 0,
        fvlnPoints: 5
      }
    };
  }

  // Values per 100g / 100ml
  const energyKcal = Math.max(0, nutrition.calories || 0);
  const energyKj = Math.round(energyKcal * 4.184);
  const sugars = Math.max(0, nutrition.totalSugarG || 0);
  const satFat = Math.max(0, nutrition.saturatedFatG || 0);
  const sodiumMg = Math.max(0, nutrition.sodiumMg || 0);
  const saltG = (sodiumMg * 2.5) / 1000;
  const fiberG = Math.max(0, nutrition.fiberG || 0);
  const proteinG = Math.max(0, nutrition.proteinG || 0);
  const fvlnPct = estimateFvlnPercentage(ingredients);
  const { hasSweeteners } = detectAdditives(ingredients);

  // 1. Negative Points (N)
  // A. Energy Points (0-10)
  let energyPts = 0;
  if (energyKj > 3350) energyPts = 10;
  else if (energyKj > 3015) energyPts = 9;
  else if (energyKj > 2680) energyPts = 8;
  else if (energyKj > 2345) energyPts = 7;
  else if (energyKj > 2010) energyPts = 6;
  else if (energyKj > 1675) energyPts = 5;
  else if (energyKj > 1340) energyPts = 4;
  else if (energyKj > 1005) energyPts = 3;
  else if (energyKj > 670) energyPts = 2;
  else if (energyKj > 335) energyPts = 1;

  // B. Sugars Points (0-15 scale for 2023 update)
  let sugarsPts = 0;
  if (sugars > 51) sugarsPts = 15;
  else if (sugars > 48) sugarsPts = 14;
  else if (sugars > 45) sugarsPts = 13;
  else if (sugars > 42) sugarsPts = 12;
  else if (sugars > 38) sugarsPts = 11;
  else if (sugars > 35) sugarsPts = 10;
  else if (sugars > 31) sugarsPts = 9;
  else if (sugars > 28) sugarsPts = 8;
  else if (sugars > 24) sugarsPts = 7;
  else if (sugars > 21) sugarsPts = 6;
  else if (sugars > 17) sugarsPts = 5;
  else if (sugars > 14) sugarsPts = 4;
  else if (sugars > 10) sugarsPts = 3;
  else if (sugars > 6.8) sugarsPts = 2;
  else if (sugars > 3.4) sugarsPts = 1;

  // C. Saturated Fat Points (0-10)
  let satFatPts = 0;
  if (satFat > 10) satFatPts = 10;
  else if (satFat > 9) satFatPts = 9;
  else if (satFat > 8) satFatPts = 8;
  else if (satFat > 7) satFatPts = 7;
  else if (satFat > 6) satFatPts = 6;
  else if (satFat > 5) satFatPts = 5;
  else if (satFat > 4) satFatPts = 4;
  else if (satFat > 3) satFatPts = 3;
  else if (satFat > 2) satFatPts = 2;
  else if (satFat > 1) satFatPts = 1;

  // D. Salt Points (0-20 scale for 2023 update)
  let sodiumPts = 0;
  if (saltG > 4.0) sodiumPts = 20;
  else if (saltG > 3.8) sodiumPts = 19;
  else if (saltG > 3.6) sodiumPts = 18;
  else if (saltG > 3.4) sodiumPts = 17;
  else if (saltG > 3.2) sodiumPts = 16;
  else if (saltG > 3.0) sodiumPts = 15;
  else if (saltG > 2.8) sodiumPts = 14;
  else if (saltG > 2.6) sodiumPts = 13;
  else if (saltG > 2.4) sodiumPts = 12;
  else if (saltG > 2.2) sodiumPts = 11;
  else if (saltG > 2.0) sodiumPts = 10;
  else if (saltG > 1.8) sodiumPts = 9;
  else if (saltG > 1.6) sodiumPts = 8;
  else if (saltG > 1.4) sodiumPts = 7;
  else if (saltG > 1.2) sodiumPts = 6;
  else if (saltG > 1.0) sodiumPts = 5;
  else if (saltG > 0.8) sodiumPts = 4;
  else if (saltG > 0.6) sodiumPts = 3;
  else if (saltG > 0.4) sodiumPts = 2;
  else if (saltG > 0.2) sodiumPts = 1;

  const negativePoints = energyPts + sugarsPts + satFatPts + sodiumPts;

  // 2. Positive Points (P)
  // A. FVLN Points (0, 1, 2, 5)
  let fvlnPts = 0;
  if (fvlnPct > 80) fvlnPts = 5;
  else if (fvlnPct > 60) fvlnPts = 2;
  else if (fvlnPct > 40) fvlnPts = 1;

  // B. Fiber Points (0-5)
  let fiberPts = 0;
  if (fiberG > 4.7) fiberPts = 5;
  else if (fiberG > 3.7) fiberPts = 4;
  else if (fiberG > 2.8) fiberPts = 3;
  else if (fiberG > 1.9) fiberPts = 2;
  else if (fiberG > 0.9) fiberPts = 1;

  // C. Protein Points (0-5)
  let rawProteinPts = 0;
  if (proteinG > 8.0) rawProteinPts = 5;
  else if (proteinG > 6.4) rawProteinPts = 4;
  else if (proteinG > 4.8) rawProteinPts = 3;
  else if (proteinG > 3.2) rawProteinPts = 2;
  else if (proteinG > 1.6) rawProteinPts = 1;

  // ⚠️ CRITICAL PROTEIN CAP RULE (2023 Nutri-Score Update):
  // If negative points N >= 11, protein points CANNOT be subtracted unless FVLN > 80%.
  let proteinPts = rawProteinPts;
  if (negativePoints >= 11 && fvlnPct <= 80) {
    proteinPts = 0;
  }

  const positivePoints = fvlnPts + fiberPts + proteinPts;
  let finalScore = negativePoints - positivePoints;

  // 3. Grade Mapping
  let grade: NutriScoreGrade = 'C';

  if (isBeverage) {
    // Beverage specific scale (Water is ONLY A; artificial sweeteners add +4 penalty)
    let bevScore = finalScore + (hasSweeteners ? 4 : 0);
    if (bevScore <= 1.5) grade = 'B';
    else if (bevScore <= 4.5) grade = 'C';
    else if (bevScore <= 9.0) grade = 'D';
    else grade = 'E';
    finalScore = bevScore;
  } else {
    // Solid Foods scale
    if (finalScore <= -1) grade = 'A';
    else if (finalScore <= 2) grade = 'B';
    else if (finalScore <= 10) grade = 'C';
    else if (finalScore <= 18) grade = 'D';
    else grade = 'E';
  }

  return {
    grade,
    score: finalScore,
    negativePoints,
    positivePoints,
    isBeverage,
    breakdown: {
      energyPoints: energyPts,
      sugarsPoints: sugarsPts,
      satFatPoints: satFatPts,
      sodiumPoints: sodiumPts,
      fiberPoints: fiberPts,
      proteinPoints: proteinPts,
      fvlnPoints: fvlnPts,
    }
  };
}

/**
 * 🇲🇽/🇨🇱 Latin American Warning Octagons Engine (NOM-051 & Chilean Rules)
 */
export function calculateLatAmOctagons(
  nutrition: NutritionFacts,
  ingredients: (Ingredient | string)[] = []
): LatAmOctagonWarning[] {
  const warnings: LatAmOctagonWarning[] = [];
  const { hasSweeteners, hasCaffeine } = detectAdditives(ingredients);

  const calories = Math.max(0, nutrition.calories || 0);
  const totalSugars = Math.max(0, nutrition.totalSugarG || 0);
  const satFat = Math.max(0, nutrition.saturatedFatG || 0);
  const transFat = Math.max(0, nutrition.transFatG || 0);
  const sodium = Math.max(0, nutrition.sodiumMg || 0);

  // Energy contributions
  const sugarCalories = totalSugars * 4;
  const satFatCalories = satFat * 9;
  const transFatCalories = transFat * 9;

  // 1. High Calories (Solid foods >= 275 kcal / 100g)
  if (calories >= 275) {
    warnings.push({
      id: 'HIGH_CALORIES',
      mexicoLabel: 'EXCESO CALORÍAS',
      chileLabel: 'ALTO EN CALORÍAS',
      englishSubtitle: 'High in Calories',
      thresholdDeclared: '≥ 275 kcal / 100g'
    });
  }

  // 2. High Sugar (>= 10% of total energy from free/total sugars OR >= 10g / 100g)
  if (totalSugars >= 10 || (calories > 0 && (sugarCalories / calories) >= 0.10)) {
    warnings.push({
      id: 'HIGH_SUGAR',
      mexicoLabel: 'EXCESO AZÚCARES',
      chileLabel: 'ALTO EN AZÚCARES',
      englishSubtitle: 'High in Sugars',
      thresholdDeclared: '≥ 10% of total energy or ≥ 10g/100g'
    });
  }

  // 3. High Saturated Fat (>= 10% of total energy from sat fat OR >= 4g / 100g)
  if (satFat >= 4 || (calories > 0 && (satFatCalories / calories) >= 0.10)) {
    warnings.push({
      id: 'HIGH_SAT_FAT',
      mexicoLabel: 'EXCESO GRASAS SATURADAS',
      chileLabel: 'ALTO EN GRASAS SATURADAS',
      englishSubtitle: 'High in Saturated Fat',
      thresholdDeclared: '≥ 10% of total energy or ≥ 4g/100g'
    });
  }

  // 4. High Sodium (>= 1mg sodium per 1 kcal OR >= 300mg / 100g)
  if (sodium >= 300 || (calories > 0 && sodium / calories >= 1.0)) {
    warnings.push({
      id: 'HIGH_SODIUM',
      mexicoLabel: 'EXCESO SODIO',
      chileLabel: 'ALTO EN SODIO',
      englishSubtitle: 'High in Sodium',
      thresholdDeclared: '≥ 1mg/kcal or ≥ 300mg/100g'
    });
  }

  // 5. High Trans Fat (>= 1% of total energy from trans fat)
  if (transFat > 0 && (calories > 0 && (transFatCalories / calories) >= 0.01)) {
    warnings.push({
      id: 'HIGH_TRANS_FAT',
      mexicoLabel: 'EXCESO GRASAS TRANS',
      chileLabel: 'ALTO EN GRASAS TRANS',
      englishSubtitle: 'High in Trans Fat',
      thresholdDeclared: '≥ 1% of total energy'
    });
  }

  // 6. Contains Sweeteners
  if (hasSweeteners) {
    warnings.push({
      id: 'CONTAINS_SWEETENERS',
      mexicoLabel: 'CONTIENE EDULCORANTES',
      chileLabel: 'CONTIENE EDULCORANTES',
      englishSubtitle: 'Contains Sweeteners - Avoid in Children',
      thresholdDeclared: 'Presence of non-nutritive artificial sweeteners'
    });
  }

  // 7. Contains Caffeine
  if (hasCaffeine) {
    warnings.push({
      id: 'CONTAINS_CAFFEINE',
      mexicoLabel: 'CONTIENE CAFEÍNA',
      chileLabel: 'CONTIENE CAFEÍNA',
      englishSubtitle: 'Contains Caffeine - Avoid in Children',
      thresholdDeclared: 'Presence of caffeine'
    });
  }

  return warnings;
}

/**
 * 🇺🇸 US FDA Front-of-Package (FOP) %DV Safeguarded Engine
 */
export function calculateFdaFrontOfPackage(
  nutrition: NutritionFacts,
  servingSizeStr: string = '100g'
): FdaFrontOfPackageResult {
  const SAT_FAT_DV = 20; // 20g
  const SODIUM_DV = 2300; // 2300mg
  const ADDED_SUGAR_DV = 50; // 50g

  // Parse serving multiplier if serving size is given (e.g. "30g" vs "100g")
  let servingMultiplier = 1.0;
  const matchGrams = servingSizeStr.match(/(\d+(?:\.\d+)?)\s*g/i);
  if (matchGrams) {
    const g = parseFloat(matchGrams[1]);
    if (g > 0 && g <= 1000) {
      servingMultiplier = g / 100.0;
    }
  }

  const servingSatFat = (nutrition.saturatedFatG || 0) * servingMultiplier;
  const servingSodium = (nutrition.sodiumMg || 0) * servingMultiplier;
  const servingAddedSugar = (nutrition.addedSugarG ?? nutrition.totalSugarG ?? 0) * servingMultiplier;

  const satFatPct = Math.round((servingSatFat / SAT_FAT_DV) * 100);
  const sodiumPct = Math.round((servingSodium / SODIUM_DV) * 100);
  const sugarPct = Math.round((servingAddedSugar / ADDED_SUGAR_DV) * 100);

  const getLevel = (pct: number): FdaSeverityLevel => {
    if (pct <= 5) return 'LOW';
    if (pct >= 20) return 'HIGH';
    return 'MED';
  };

  return {
    saturatedFat: { level: getLevel(satFatPct), dvPercentage: satFatPct, gramsPerServing: Math.round(servingSatFat * 10) / 10 },
    sodium: { level: getLevel(sodiumPct), dvPercentage: sodiumPct, mgPerServing: Math.round(servingSodium) },
    addedSugar: { level: getLevel(sugarPct), dvPercentage: sugarPct, gramsPerServing: Math.round(servingAddedSugar * 10) / 10 },
  };
}

/**
 * 🌍 Main Orchestrator for All International Rating Systems
 */
export function calculateInternationalRatings(
  nutrition: NutritionFacts,
  category: string = '',
  ingredients: (Ingredient | string)[] = [],
  servingSize: string = '100g'
): InternationalRatings {
  return {
    nutriScore: calculateNutriScore(nutrition, category, ingredients),
    fdaLabel: calculateFdaFrontOfPackage(nutrition, servingSize),
    warningOctagons: calculateLatAmOctagons(nutrition, ingredients),
  };
}
