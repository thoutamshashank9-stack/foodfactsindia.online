import { validateFinalCandidate, canPublishReport } from '../services/validationPipeline';
import { getProductPage } from '../services/supabaseService';

console.log("🧪 Running V2 Validation Regression Test Suite...");

// 1. OCR Corruption: lodised salt
const candidateLodised = {
  productId: 'test_lodised',
  validationPassed: true,
  ingredients: [
    { raw: 'lodised salt', normalized: 'Iodised Salt', confidence: 0.9 }
  ],
  nutrition: {
    energyKcal: 0,
    proteinG: 0,
    totalFatG: 0,
    saturatedFatG: 0,
    transFatG: 0,
    carbohydrateG: 0,
    totalSugarsG: 0,
    addedSugarsG: 0,
    sodiumMg: 38000,
    fiberG: 0,
    basis: 'per_100g' as const
  }
};

const resultLodised = validateFinalCandidate(candidateLodised);
if (resultLodised.valid === false && resultLodised.state === 'needs_review') {
  console.log("✅ REGRESSION TEST 1 PASSED: Successfully flagged 'lodised salt' OCR anomaly!");
} else {
  console.error("❌ REGRESSION TEST 1 FAILED: Allowed 'lodised salt' to publish!", resultLodised);
  process.exit(1);
}

// 2. OCR Corruption: wheat glute
const candidateGlute = {
  ...candidateLodised,
  productId: 'test_glute',
  ingredients: [
    { raw: 'wheat glute liquid glucose', normalized: 'Wheat Gluten', confidence: 0.9 }
  ]
};

const resultGlute = validateFinalCandidate(candidateGlute);
if (resultGlute.valid === false && resultGlute.reasons.some(r => r.includes('SUSPICIOUS_TOKEN'))) {
  console.log("✅ REGRESSION TEST 2 PASSED: Successfully flagged 'wheat glute' anomaly!");
} else {
  console.error("❌ REGRESSION TEST 2 FAILED: Allowed 'wheat glute'!", resultGlute);
  process.exit(1);
}

// 3. OCR Corruption: coco solids
const candidateCoco = {
  ...candidateLodised,
  productId: 'test_coco',
  ingredients: [
    { raw: 'coco solids', normalized: 'Cocoa Solids', confidence: 0.9 }
  ]
};

const resultCoco = validateFinalCandidate(candidateCoco);
if (resultCoco.valid === false && resultCoco.reasons.some(r => r.includes('SUSPICIOUS_TOKEN'))) {
  console.log("✅ REGRESSION TEST 3 PASSED: Successfully flagged 'coco solids' anomaly!");
} else {
  console.error("❌ REGRESSION TEST 3 FAILED: Allowed 'coco solids'!", resultCoco);
  process.exit(1);
}

// 4. Additive Mapping Collapse (322, 471)
const candidateAdditiveCollapse = {
  ...candidateLodised,
  productId: 'test_additive_collapse',
  ingredients: [
    { raw: 'Refined Wheat Flour', normalized: 'Refined Wheat Flour', confidence: 0.95 }
  ],
  additiveMappings: [
    {
      raw: 'Emulsifiers (INS 322, INS 471)',
      extractedCodes: ['322', '471'],
      resolved: [
        { code: 'INS 471', name: 'Soy Lecithin E471', confidence: 0.9 },
        { code: 'INS 471', name: 'Soy Lecithin E471', confidence: 0.9 } // Collapsed duplicate resolution!
      ],
      ambiguous: false
    }
  ]
};

const resultAdditiveCollapse = validateFinalCandidate(candidateAdditiveCollapse);
if (resultAdditiveCollapse.valid === false && resultAdditiveCollapse.reasons.some(r => r.includes('CODE_COUNT_MISMATCH') || r.includes('DUPLICATE_RESOLUTION'))) {
  console.log("✅ REGRESSION TEST 4 PASSED: Successfully flagged emulsifier (322,471) collapse mismatch!");
} else {
  console.error("❌ REGRESSION TEST 4 FAILED: Allowed collapsed emulsifier mapping!", resultAdditiveCollapse);
  process.exit(1);
}

// 5. Contradiction: 0g Sugar with Sugar Finding
const candidateContradiction = {
  ...candidateLodised,
  productId: 'test_contradiction',
  ingredients: [
    { raw: 'Sugar', normalized: 'Sugar', confidence: 0.99 }
  ],
  nutrition: {
    energyKcal: 100,
    proteinG: 0,
    totalFatG: 0,
    saturatedFatG: 0,
    transFatG: 0,
    carbohydrateG: 0,
    totalSugarsG: 0, // 0g declared
    addedSugarsG: 0,
    sodiumMg: 0,
    fiberG: 0,
    basis: 'per_100g' as const
  },
  findings: [
    { type: 'HIGH_SUGAR', severity: 'high' as const, message: 'Contains high refined sugar load.' }
  ]
};

const resultContradiction = validateFinalCandidate(candidateContradiction);
if (resultContradiction.valid === false && resultContradiction.reasons.some(r => r.includes('SUGAR_FINDING_WITH_ZERO_SUGAR_DISPLAY'))) {
  console.log("✅ REGRESSION TEST 5 PASSED: Successfully flagged 0g sugar vs Sugar Finding contradiction!");
} else {
  console.error("❌ REGRESSION TEST 5 FAILED: Allowed 0g sugar contradiction!", resultContradiction);
  process.exit(1);
}

// 6. Discriminated Union Safety: Non-verified page never returns verifiedReport
(async () => {
  const pageRes = await getProductPage("9999999999999"); // Fake unverified GTIN
  if (pageRes.pageState !== 'verified_published') {
    if (!('verifiedReport' in pageRes)) {
      console.log("✅ REGRESSION TEST 6 PASSED: Non-verified ProductPageResponse variant physically lacks verifiedReport!");
    } else {
      console.error("❌ REGRESSION TEST 6 FAILED: Non-verified ProductPageResponse leaked verifiedReport!", pageRes);
      process.exit(1);
    }
  }

  console.log("🎉 ALL V2 VALIDATION REGRESSION TESTS PASSED 100%!");
})();
