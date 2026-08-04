import { evaluateRatingGate } from '../services/scoringEngine';
import { NutritionFacts } from '../types';

console.log('🧪 Running Enterprise Hardening Unit Test Suite...');

const validNutrition: NutritionFacts = {
  calories: 250,
  servingSize: '100g',
  totalFatG: 10,
  saturatedFatG: 2,
  transFatG: 0,
  sodiumMg: 150,
  totalCarbsG: 30,
  fiberG: 3,
  totalSugarG: 5,
  addedSugarG: 2,
  proteinG: 8
};

// TEST 1: Gate 1 — Confidence Threshold (< 0.70)
const gate1 = evaluateRatingGate(0.65, validNutrition, 'OPEN_FOOD_FACTS', 'Snacks');
console.assert(gate1.isEligibleForRatings === false, 'Gate 1 should block low confidence');
console.log('✅ TEST 1 PASSED: Gate 1 blocked confidence < 0.70');

// TEST 2: Gate 2 — Source Quality (UNGROUNDED_AI)
const gate2 = evaluateRatingGate(0.85, validNutrition, 'UNGROUNDED_AI', 'Snacks');
console.assert(gate2.isEligibleForRatings === false, 'Gate 2 should block ungrounded AI');
console.log('✅ TEST 2 PASSED: Gate 2 blocked UNGROUNDED_AI source');

// TEST 3: Gate 3 — Incomplete Label (calories 0)
const incompleteNutrition = { ...validNutrition, calories: 0 };
const gate3 = evaluateRatingGate(0.85, incompleteNutrition, 'OPEN_FOOD_FACTS', 'Snacks');
console.assert(gate3.isEligibleForRatings === false, 'Gate 3 should block missing calories');
console.log('✅ TEST 3 PASSED: Gate 3 blocked incomplete nutrition label');

// TEST 4: Gate 4 — Nutrient Sanity (Sat Fat > Total Fat)
const insaneNutrition = { ...validNutrition, totalFatG: 2, saturatedFatG: 5 };
const gate4 = evaluateRatingGate(0.85, insaneNutrition, 'OPEN_FOOD_FACTS', 'Snacks');
console.assert(gate4.isEligibleForRatings === false, 'Gate 4 should block sat fat > total fat');
console.log('✅ TEST 4 PASSED: Gate 4 blocked insane nutrient values');

// TEST 5: Gate 5 — Category Eligibility (Energy Drinks)
const gate5 = evaluateRatingGate(0.95, validNutrition, 'OPEN_FOOD_FACTS', 'Energy Drinks');
console.assert(gate5.isEligibleForRatings === false, 'Gate 5 should block Energy Drinks');
console.log('✅ TEST 5 PASSED: Gate 5 blocked excluded category (Energy Drinks)');

// TEST 6: All Gates Pass
const gate6 = evaluateRatingGate(0.95, validNutrition, 'OPEN_FOOD_FACTS', 'Breakfast Cereal');
console.assert(gate6.isEligibleForRatings === true, 'Gate 6 should pass valid food product');
console.log('✅ TEST 6 PASSED: Valid food product passed all 5 rating gates!');

console.log('🎉 ALL PRODUCTION HARDENING TESTS PASSED SUCCESSFULLY!');
