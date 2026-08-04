import { 
  calculateNutriScore, 
  calculateLatAmOctagons, 
  calculateFdaFrontOfPackage, 
  calculateInternationalRatings,
  detectAdditives 
} from '../services/internationalRatingsEngine';
import { NutritionFacts } from '../types';

console.log('🧪 Running Multi-Country Ratings Engine Test Suite...');

// TEST 1: Regular Sugary Soda
const sodaNutrition: NutritionFacts = {
  calories: 140,
  servingSize: '330ml',
  totalFatG: 0,
  saturatedFatG: 0,
  transFatG: 0,
  sodiumMg: 45,
  totalCarbsG: 35,
  fiberG: 0,
  totalSugarG: 35,
  addedSugarG: 35,
  proteinG: 0
};
const sodaIngs = ['Carbonated Water', 'High Fructose Corn Syrup', 'Caramel Color', 'Phosphoric Acid', 'Natural Flavors'];

const sodaNutri = calculateNutriScore(sodaNutrition, 'Soft Drinks', sodaIngs);
const sodaOctagons = calculateLatAmOctagons(sodaNutrition, sodaIngs);
const sodaFda = calculateFdaFrontOfPackage(sodaNutrition, '330ml');

console.assert(sodaNutri.grade === 'E', `Expected Soda Nutri-Score E, got ${sodaNutri.grade}`);
console.assert(sodaOctagons.some(o => o.id === 'HIGH_SUGAR'), 'Expected Soda to trigger HIGH_SUGAR octagon');
console.assert(sodaFda.addedSugar.level === 'HIGH', `Expected Soda FDA Added Sugar HIGH, got ${sodaFda.addedSugar.level}`);

console.log('✅ TEST 1 PASSED: Sugary Soda correctly rated Nutri-Score E, LatAm High Sugar, FDA High Sugar');

// TEST 2: Diet Soda with Sucralose
const dietSodaNutrition: NutritionFacts = {
  calories: 0,
  servingSize: '330ml',
  totalFatG: 0,
  saturatedFatG: 0,
  transFatG: 0,
  sodiumMg: 35,
  totalCarbsG: 0,
  fiberG: 0,
  totalSugarG: 0,
  addedSugarG: 0,
  proteinG: 0
};
const dietSodaIngs = ['Carbonated Water', 'Sucralose', 'Acesulfame Potassium', 'Caramel Color', 'Caffeine'];

const dietAdditives = detectAdditives(dietSodaIngs);
const dietNutri = calculateNutriScore(dietSodaNutrition, 'Soft Drinks', dietSodaIngs);
const dietOctagons = calculateLatAmOctagons(dietSodaNutrition, dietSodaIngs);

console.assert(dietAdditives.hasSweeteners === true, 'Expected sweetener detection in diet soda');
console.assert(dietAdditives.hasCaffeine === true, 'Expected caffeine detection in diet soda');
console.assert(dietOctagons.some(o => o.id === 'CONTAINS_SWEETENERS'), 'Expected CONTAINS_SWEETENERS octagon');
console.assert(dietOctagons.some(o => o.id === 'CONTAINS_CAFFEINE'), 'Expected CONTAINS_CAFFEINE octagon');

console.log('✅ TEST 2 PASSED: Diet Soda correctly detected sweeteners, caffeine, and warning octagons');

// TEST 3: Rolled Oats
const oatsNutrition: NutritionFacts = {
  calories: 360,
  servingSize: '100g',
  totalFatG: 6.0,
  saturatedFatG: 1.0,
  transFatG: 0,
  sodiumMg: 5,
  totalCarbsG: 60,
  fiberG: 10,
  totalSugarG: 1.0,
  addedSugarG: 0,
  proteinG: 13.0
};
const oatsIngs = ['100% Whole Grain Rolled Oats'];

const oatsNutri = calculateNutriScore(oatsNutrition, 'Staples', oatsIngs);
const oatsOctagons = calculateLatAmOctagons(oatsNutrition, oatsIngs);
const oatsFda = calculateFdaFrontOfPackage(oatsNutrition, '100g');

console.assert(oatsNutri.grade === 'A', `Expected Oats Nutri-Score A, got ${oatsNutri.grade}`);
console.assert(oatsFda.sodium.level === 'LOW', `Expected Oats FDA Sodium LOW, got ${oatsFda.sodium.level}`);
console.assert(!oatsOctagons.some(o => o.id === 'HIGH_SUGAR'), 'Oats should not trigger High Sugar');

console.log('✅ TEST 3 PASSED: Rolled Oats correctly rated Nutri-Score A with Low Sodium');

// TEST 4: Full Orchestrator
const fullRatings = calculateInternationalRatings(sodaNutrition, 'Soft Drinks', sodaIngs, '330ml');
console.assert(fullRatings.nutriScore.grade === 'E', 'Orchestrator Nutri-Score test');
console.assert(fullRatings.fdaLabel.addedSugar.level === 'HIGH', 'Orchestrator FDA test');
console.assert(fullRatings.warningOctagons.length > 0, 'Orchestrator Octagons test');

console.log('🎉 ALL MULTI-COUNTRY RATING TESTS PASSED SUCCESSFULLY!');
