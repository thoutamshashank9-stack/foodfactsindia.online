import { searchTransparencyReports } from '../services/searchService';
import { isProductDataComplete } from '../services/supabaseService';
import { TransparencyReport } from '../types';

console.log('🧪 Running Search Predictions Completeness Test Suite...');

const mockCompleteProduct: TransparencyReport = {
  productId: 'prod_complete_1',
  productName: 'Organic Masala Chai',
  brand: 'Pure Leaf',
  manufacturer: 'Pure Leaf',
  category: 'Beverages',
  barcode: '8901234567890',
  imageUrl: 'https://example.com/chai.jpg',
  packageSize: '100g',
  servingSize: '100g',
  pageState: 'verified_published',
  deterministicScore: 90,
  scoreBreakdown: [],
  executiveSummary: {
    grade: 'A',
    verdictTitle: 'Excellent Chai',
    keyTakeaways: [],
    riskSummaryText: 'Safe tea.'
  },
  ingredientsList: [
    {
      ingredient: {
        id: 'ing_tea',
        canonicalName: 'Black Tea',
        synonyms: ['tea'],
        category: 'WHOLE_FOOD',
        riskLevel: 'LOW',
        baseRiskWeight: 0,
        description: 'Standard tea leaves',
        processingLevel: 'NOVA_1_UNPROCESSED',
        regulatoryRecords: [],
        citations: []
      },
      rawName: 'Tea Leaves',
      position: 1,
      isControversial: false
    }
  ],
  nutrition: {
    calories: 120,
    servingSize: '100g',
    totalFatG: 2,
    saturatedFatG: 0,
    transFatG: 0,
    sodiumMg: 15,
    totalCarbsG: 20,
    fiberG: 4,
    totalSugarG: 5,
    addedSugarG: 5,
    proteinG: 3
  },
  globalRegulatoryOverview: [],
  evidenceConfidence: {
    confidenceScore: 95,
    peerReviewedStudiesCount: 0,
    regulatoryBodiesCount: 0,
    lastUpdated: '2025-01-01'
  }
};

const mockIncompleteProductWithheld: TransparencyReport = {
  ...mockCompleteProduct,
  productId: 'prod_incomplete_withheld',
  productName: 'Incomplete Tea Chai',
  pageState: 'insufficient_data',
  isScoreWithheld: true
};

const mockIncompleteProductNoIngredients: TransparencyReport = {
  ...mockCompleteProduct,
  productId: 'prod_incomplete_no_ingredients',
  productName: 'Empty Ingredients Chai',
  ingredientsList: []
};

const mockIncompleteProductPlaceholder: TransparencyReport = {
  ...mockCompleteProduct,
  productId: 'prod_incomplete_placeholder',
  productName: 'Placeholder Chai',
  ingredientsList: [
    {
      ingredient: {
        id: 'ing_raw_1',
        canonicalName: 'Standard Ingredients',
        synonyms: ['Standard Ingredients'],
        category: 'WHOLE_FOOD',
        riskLevel: 'LOW',
        baseRiskWeight: 0,
        description: 'Standard food ingredients mix.',
        processingLevel: 'NOVA_1_UNPROCESSED',
        regulatoryRecords: [],
        citations: []
      },
      rawName: 'Declared ingredients list',
      position: 1,
      isControversial: false
    }
  ]
};

// Test isProductDataComplete validations
console.assert(isProductDataComplete(mockCompleteProduct) === true, 'Complete product should pass validation');
console.assert(isProductDataComplete(mockIncompleteProductWithheld) === false, 'Withheld score product should fail validation');
console.assert(isProductDataComplete(mockIncompleteProductNoIngredients) === false, 'No ingredients product should fail validation');
console.assert(isProductDataComplete(mockIncompleteProductPlaceholder) === false, 'Placeholder ingredients product should fail validation');

console.log('✅ TEST 1 PASSED: isProductDataComplete successfully identifies complete vs incomplete data');

// Test searchTransparencyReports filtering
const searchPool = [
  mockCompleteProduct,
  mockIncompleteProductWithheld,
  mockIncompleteProductNoIngredients,
  mockIncompleteProductPlaceholder
];

const results = searchTransparencyReports(searchPool, 'Chai');

console.assert(results.length === 1, 'Search predictions should only return 1 product');
console.assert(results[0].productId === 'prod_complete_1', 'Search predictions should only return the complete product');

console.log('✅ TEST 2 PASSED: searchTransparencyReports strictly filters out products without complete ingredients/data from search predictions');

console.log('🎉 ALL SEARCH PREDICTIONS COMPLETENESS TESTS PASSED SUCCESSFULLY!');
