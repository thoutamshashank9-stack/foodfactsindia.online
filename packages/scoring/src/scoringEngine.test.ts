import { calculateDeterministicScore } from '../../../src/services/scoringEngine';
import { Ingredient, NutritionFacts } from '../../../src/types';

// Mock clean whole wheat ingredient
const mockWholeWheat: Ingredient = {
  id: 'ing_wheat',
  canonicalName: 'Whole Wheat Flour',
  synonyms: ['Wheat'],
  category: 'WHOLE_FOOD',
  riskLevel: 'EXCELLENT',
  baseRiskWeight: 5,
  description: 'Whole grain wheat flour',
  processingLevel: 'NOVA_1_UNPROCESSED',
  regulatoryRecords: [],
  citations: []
};

// Mock banned additive in Japan (TBHQ)
const mockTBHQ: Ingredient = {
  id: 'ing_tbhq',
  canonicalName: 'TBHQ',
  synonyms: ['E319', 'INS 319'],
  category: 'PRESERVATIVE',
  riskLevel: 'HIGH',
  baseRiskWeight: -15,
  description: 'Synthetic preservative banned in Japan',
  processingLevel: 'NOVA_4_ULTRA_PROCESSED',
  regulatoryRecords: [
    { countryCode: 'JP', countryName: 'Japan', flagEmoji: '🇯🇵', status: 'BANNED', regulationRef: 'MHLW' }
  ],
  citations: []
};

const cleanNutrition: NutritionFacts = {
  calories: 120,
  servingSize: '100g',
  totalFatG: 1,
  saturatedFatG: 0,
  transFatG: 0,
  sodiumMg: 50,
  totalCarbsG: 22,
  fiberG: 4,
  totalSugarG: 1,
  addedSugarG: 0,
  proteinG: 5
};

// 1. Clean Whole Food Test
const cleanResult = calculateDeterministicScore([mockWholeWheat], cleanNutrition);
console.assert(cleanResult.finalScore >= 90, `Expected clean score >= 90, got ${cleanResult.finalScore}`);
console.assert(cleanResult.scoreBreakdown.some(b => b.type === 'ADDITION'), 'Expected clean label fiber bonus');

// 2. High Sugar Penalty Test (> 5g added sugar)
const highSugarNutrition: NutritionFacts = {
  ...cleanNutrition,
  addedSugarG: 25 // 20g over limit -> -40 cap
};
const sugarResult = calculateDeterministicScore([mockWholeWheat], highSugarNutrition);
console.assert(sugarResult.scoreBreakdown.some(b => b.factor.includes('Added Sugar')), 'Expected added sugar deduction');

// 3. Banned Additive Deduction Test
const bannedResult = calculateDeterministicScore([mockTBHQ], cleanNutrition);
console.assert(bannedResult.scoreBreakdown.some(b => b.factor.includes('Banned Additive')), 'Expected banned additive deduction for TBHQ');

console.log('All Score Engine Deterministic Tests Executed Successfully!');
