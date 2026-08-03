import goldenDataset from '../../golden_dataset.json';
import { PRESEEDED_PRODUCTS } from '../data/productsDatabase';
import { calculateDeterministicScore } from '../services/scoringEngine';

let passed = 0;
const total = goldenDataset.length;

console.log(`Starting FoodFactsIndia AI Golden Dataset Regression Suite (${total} SKUs)...`);

goldenDataset.forEach((item) => {
  const prod = PRESEEDED_PRODUCTS.find((p) => p.productId === item.productId || p.barcode === item.barcode);
  if (!prod) {
    throw new Error(`Product ${item.productId} (${item.productName}) missing from database`);
  }

  const result = calculateDeterministicScore(
    prod.ingredientsList.map((i) => i.ingredient),
    prod.nutrition
  );

  const diff = Math.abs(result.finalScore - item.expectedScore);
  const scoreMatches = diff <= 2;

  if (scoreMatches) {
    passed++;
    console.log(`✓ PASS: ${item.productName} -> Score: ${result.finalScore} (Expected: ${item.expectedScore})`);
  } else {
    console.error(`✗ FAIL: ${item.productName} -> Score: ${result.finalScore} (Expected: ${item.expectedScore})`);
  }
});

const passRate = (passed / total) * 100;
console.log(`\n==============================================`);
console.log(`Golden Dataset Pass Rate: ${passRate.toFixed(1)}% (${passed}/${total})`);
console.log(`==============================================`);

if (passRate < 95 && typeof process !== 'undefined') {
  // @ts-ignore
  process.exit(1);
}
