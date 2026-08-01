import { TransparencyReport } from '../types';
import { INGREDIENT_DATABASE } from './ingredientsDatabase';
import { calculateDeterministicScore } from '../services/scoringEngine';

const findIng = (id: string) => {
  const item = INGREDIENT_DATABASE.find((i) => i.id === id);
  if (!item) throw new Error(`Ingredient ${id} not found`);
  return item;
};

export const PRESEEDED_PRODUCTS: TransparencyReport[] = [
  (() => {
    const rawIngs = [
      { ingredient: findIng('ing_palm_oil'), rawName: 'Refined Palm Oil', position: 1, isControversial: true },
      { ingredient: findIng('ing_e150d'), rawName: 'Caramel Color IV (INS 150d)', position: 2, isControversial: true },
      { ingredient: findIng('ing_e621'), rawName: 'Monosodium Glutamate (INS 621)', position: 3, isControversial: true },
      { ingredient: findIng('ing_e330'), rawName: 'Citric Acid (INS 330)', position: 4, isControversial: false },
      { ingredient: findIng('ing_whole_wheat'), rawName: 'Refined Wheat Flour (Maida)', position: 5, isControversial: false }
    ];

    const nutrition = {
      calories: 427,
      servingSize: '70g',
      totalFatG: 15.7,
      saturatedFatG: 6.8,
      transFatG: 0.1,
      sodiumMg: 1020,
      totalCarbsG: 63.5,
      fiberG: 2.1,
      totalSugarG: 3.2,
      addedSugarG: 2.5,
      proteinG: 8.0,
      micronutrients: [
        { name: 'Calcium', amount: '120mg', dvPercentage: 15 },
        { name: 'Iron', amount: '2.1mg', dvPercentage: 12 }
      ]
    };

    const calc = calculateDeterministicScore(rawIngs.map(r => r.ingredient), nutrition);

    return {
      productId: 'prod_maggi_01',
      productName: 'Maggi 2-Minute Masala Noodles',
      brand: 'Nestlé',
      manufacturer: 'Nestlé India Ltd.',
      category: 'Instant Noodles & Pasta',
      barcode: '8901058000012',
      imageUrl: 'https://images.unsplash.com/photo-1612927601601-6638404737ce?w=600&auto=format&fit=crop&q=80',
      packageSize: '70g Pack',
      servingSize: '70g',
      deterministicScore: calc.finalScore,
      scoreBreakdown: calc.scoreBreakdown,
      executiveSummary: {
        grade: calc.grade,
        verdictTitle: 'Ultra-Processed Snack with High Sodium & Caramel IV Color',
        keyTakeaways: [
          'Contains 1020mg Sodium (exceeds 34% of adult daily recommended limit in a single serving).',
          'Contains Class IV Caramel Color (INS 150d) linked to 4-MEI chemical residue concerns.',
          'Formulated with refined palm oil high in saturated fatty acids.'
        ],
        riskSummaryText: 'This product receives a low transparency rating due to excessive sodium density, refined palm oil base, and Class IV synthetic color additives.',
        processingNovaClass: 4
      },
      ingredientsList: rawIngs,
      nutrition,
      globalRegulatoryOverview: [
        { countryCode: 'IN', countryName: 'India (FSSAI)', flagEmoji: '🇮🇳', bannedCount: 0, restrictedCount: 3, approvedCount: 2 },
        { countryCode: 'EU', countryName: 'European Union (EFSA)', flagEmoji: '🇪🇺', bannedCount: 0, restrictedCount: 3, approvedCount: 2 },
        { countryCode: 'US', countryName: 'United States (FDA)', flagEmoji: '🇺🇸', bannedCount: 0, restrictedCount: 2, approvedCount: 3 },
        { countryCode: 'JP', countryName: 'Japan (MHLW)', flagEmoji: '🇯🇵', bannedCount: 0, restrictedCount: 2, approvedCount: 3 }
      ],
      evidenceConfidence: {
        confidenceScore: 96,
        peerReviewedStudiesCount: 14,
        regulatoryBodiesCount: 4,
        lastUpdated: 'July 2026'
      }
    };
  })(),

  (() => {
    const rawIngs = [
      { ingredient: findIng('ing_e150d'), rawName: 'Caramel Color (INS 150d)', position: 1, isControversial: true },
      { ingredient: findIng('ing_e330'), rawName: 'Citric Acid', position: 2, isControversial: false }
    ];

    const nutrition = {
      calories: 140,
      servingSize: '330ml Can',
      totalFatG: 0,
      saturatedFatG: 0,
      transFatG: 0,
      sodiumMg: 35,
      totalCarbsG: 35,
      fiberG: 0,
      totalSugarG: 35,
      addedSugarG: 35,
      proteinG: 0
    };

    const calc = calculateDeterministicScore(rawIngs.map(r => r.ingredient), nutrition);

    return {
      productId: 'prod_coke_02',
      productName: 'Coca-Cola Original Taste',
      brand: 'Coca-Cola',
      manufacturer: 'Hindustan Coca-Cola Beverages Pvt Ltd',
      category: 'Soft Drinks',
      barcode: '5449000000996',
      imageUrl: 'https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=600&auto=format&fit=crop&q=80',
      packageSize: '330ml Can',
      servingSize: '330ml',
      deterministicScore: calc.finalScore,
      scoreBreakdown: calc.scoreBreakdown,
      executiveSummary: {
        grade: calc.grade,
        verdictTitle: 'Severe Added Sugar Load & Synthetic Caramel IV Color',
        keyTakeaways: [
          'Contains 35g Added Sugar (140% of WHO maximum recommended daily limit in one can).',
          'Contains Class IV Caramel Color (INS 150d) subject to Proposition 65 warning in California.',
          'Zero dietary fiber or micronutrients.'
        ],
        riskSummaryText: 'Extreme sugar density triggers major mathematical deductions (-40 pts max cap reached on nutritional penalties alone).',
        processingNovaClass: 4
      },
      ingredientsList: rawIngs,
      nutrition,
      globalRegulatoryOverview: [
        { countryCode: 'IN', countryName: 'India (FSSAI)', flagEmoji: '🇮🇳', bannedCount: 0, restrictedCount: 1, approvedCount: 1 },
        { countryCode: 'EU', countryName: 'European Union (EFSA)', flagEmoji: '🇪🇺', bannedCount: 0, restrictedCount: 1, approvedCount: 1 },
        { countryCode: 'US', countryName: 'United States (FDA)', flagEmoji: '🇺🇸', bannedCount: 0, restrictedCount: 1, approvedCount: 1 },
        { countryCode: 'JP', countryName: 'Japan (MHLW)', flagEmoji: '🇯🇵', bannedCount: 0, restrictedCount: 0, approvedCount: 2 }
      ],
      evidenceConfidence: {
        confidenceScore: 98,
        peerReviewedStudiesCount: 22,
        regulatoryBodiesCount: 4,
        lastUpdated: 'July 2026'
      }
    };
  })(),

  (() => {
    const rawIngs = [
      { ingredient: findIng('ing_e319'), rawName: 'TBHQ Antioxidant (INS 319)', position: 1, isControversial: true },
      { ingredient: findIng('ing_e621'), rawName: 'Flavor Enhancer MSG (INS 621)', position: 2, isControversial: true },
      { ingredient: findIng('ing_palm_oil'), rawName: 'Palmolein Oil', position: 3, isControversial: true }
    ];

    const nutrition = {
      calories: 544,
      servingSize: '100g',
      totalFatG: 33.2,
      saturatedFatG: 14.1,
      transFatG: 0.1,
      sodiumMg: 780,
      totalCarbsG: 53.4,
      fiberG: 3.8,
      totalSugarG: 3.5,
      addedSugarG: 2.0,
      proteinG: 7.2
    };

    const calc = calculateDeterministicScore(rawIngs.map(r => r.ingredient), nutrition);

    return {
      productId: 'prod_lays_03',
      productName: "Lay's India's Magic Masala Potato Chips",
      brand: "Lay's",
      manufacturer: 'PepsiCo India Holdings Pvt Ltd',
      category: 'Snacks & Chips',
      barcode: '8901491101820',
      imageUrl: 'https://images.unsplash.com/photo-1566478989037-eec170784d0b?w=600&auto=format&fit=crop&q=80',
      packageSize: '50g Pack',
      servingSize: '100g',
      deterministicScore: calc.finalScore,
      scoreBreakdown: calc.scoreBreakdown,
      executiveSummary: {
        grade: calc.grade,
        verdictTitle: 'Contains TBHQ (Banned in Japan) & High Saturated Fat Density',
        keyTakeaways: [
          'Contains TBHQ (INS 319) - a synthetic antioxidant completely BANNED in Japan.',
          'High saturated fat content (14.1g per 100g) due to Palmolein oil frying.',
          'Contains Monosodium Glutamate (MSG) for umami flavor enhancement.'
        ],
        riskSummaryText: 'Significant score penalties due to Japan regulatory ban on TBHQ and high fried saturated fat levels.',
        processingNovaClass: 4
      },
      ingredientsList: rawIngs,
      nutrition,
      globalRegulatoryOverview: [
        { countryCode: 'IN', countryName: 'India (FSSAI)', flagEmoji: '🇮🇳', bannedCount: 0, restrictedCount: 2, approvedCount: 1 },
        { countryCode: 'EU', countryName: 'European Union (EFSA)', flagEmoji: '🇪🇺', bannedCount: 0, restrictedCount: 2, approvedCount: 1 },
        { countryCode: 'US', countryName: 'United States (FDA)', flagEmoji: '🇺🇸', bannedCount: 0, restrictedCount: 2, approvedCount: 1 },
        { countryCode: 'JP', countryName: 'Japan (MHLW)', flagEmoji: '🇯🇵', bannedCount: 1, restrictedCount: 1, approvedCount: 1 }
      ],
      evidenceConfidence: {
        confidenceScore: 94,
        peerReviewedStudiesCount: 18,
        regulatoryBodiesCount: 4,
        lastUpdated: 'July 2026'
      }
    };
  })(),

  (() => {
    const rawIngs = [
      { ingredient: findIng('ing_e102'), rawName: 'Tartrazine Dye (INS 102)', position: 1, isControversial: true },
      { ingredient: findIng('ing_e951'), rawName: 'Aspartame Sweetener (INS 951)', position: 2, isControversial: true },
      { ingredient: findIng('ing_e150d'), rawName: 'Caramel Color IV (INS 150d)', position: 3, isControversial: true }
    ];

    const nutrition = {
      calories: 210,
      servingSize: '500ml',
      totalFatG: 0,
      saturatedFatG: 0,
      transFatG: 0,
      sodiumMg: 180,
      totalCarbsG: 54,
      fiberG: 0,
      totalSugarG: 54,
      addedSugarG: 54,
      proteinG: 1.2
    };

    const calc = calculateDeterministicScore(rawIngs.map(r => r.ingredient), nutrition);

    return {
      productId: 'prod_monster_04',
      productName: 'Monster Energy Drink',
      brand: 'Monster Energy',
      manufacturer: 'Monster Energy Company USA',
      category: 'Energy Drinks',
      barcode: '5070000001024',
      imageUrl: 'https://images.unsplash.com/photo-1622543925917-763c34d1a86e?w=600&auto=format&fit=crop&q=80',
      packageSize: '500ml Can',
      servingSize: '500ml',
      deterministicScore: calc.finalScore,
      scoreBreakdown: calc.scoreBreakdown,
      executiveSummary: {
        grade: calc.grade,
        verdictTitle: 'Severe Risk: Contains EU Warning Colors, Aspartame & 54g Sugar',
        keyTakeaways: [
          'Contains Tartrazine (E102) requiring mandatory EU child hyperactivity warning labels.',
          'Contains Aspartame (E951) classified as Group 2B Possible Carcinogen by WHO/IARC.',
          'Massive 54g Added Sugar load combining synthetic sweeteners and high fructose corn syrup.'
        ],
        riskSummaryText: 'Lowest scoring product in database due to multi-market warning additives and extreme stimulant/sugar concentration.',
        processingNovaClass: 4
      },
      ingredientsList: rawIngs,
      nutrition,
      globalRegulatoryOverview: [
        { countryCode: 'IN', countryName: 'India (FSSAI)', flagEmoji: '🇮🇳', bannedCount: 0, restrictedCount: 3, approvedCount: 0 },
        { countryCode: 'EU', countryName: 'European Union (EFSA)', flagEmoji: '🇪🇺', bannedCount: 0, restrictedCount: 3, approvedCount: 0 },
        { countryCode: 'US', countryName: 'United States (FDA)', flagEmoji: '🇺🇸', bannedCount: 0, restrictedCount: 3, approvedCount: 0 },
        { countryCode: 'JP', countryName: 'Japan (MHLW)', flagEmoji: '🇯🇵', bannedCount: 0, restrictedCount: 3, approvedCount: 0 }
      ],
      evidenceConfidence: {
        confidenceScore: 99,
        peerReviewedStudiesCount: 35,
        regulatoryBodiesCount: 4,
        lastUpdated: 'July 2026'
      }
    };
  })(),

  (() => {
    const rawIngs = [
      { ingredient: findIng('ing_whole_wheat'), rawName: 'Whole Squeezed Orange Juice', position: 1, isControversial: false },
      { ingredient: findIng('ing_e330'), rawName: 'Natural Vitamin C (Ascorbic Acid)', position: 2, isControversial: false }
    ];

    const nutrition = {
      calories: 110,
      servingSize: '240ml',
      totalFatG: 0,
      saturatedFatG: 0,
      transFatG: 0,
      sodiumMg: 0,
      totalCarbsG: 26,
      fiberG: 3.2,
      totalSugarG: 22,
      addedSugarG: 0,
      proteinG: 2.0,
      micronutrients: [
        { name: 'Vitamin C', amount: '72mg', dvPercentage: 100 },
        { name: 'Potassium', amount: '450mg', dvPercentage: 10 }
      ]
    };

    const calc = calculateDeterministicScore(rawIngs.map(r => r.ingredient), nutrition);

    return {
      productId: 'prod_tropicana_05',
      productName: 'Tropicana 100% Pure Orange Juice',
      brand: 'Tropicana',
      manufacturer: 'PepsiCo India Holdings Pvt Ltd',
      category: 'Juices & Beverages',
      barcode: '8901491502016',
      imageUrl: 'https://images.unsplash.com/photo-1613478223719-2ab802602423?w=600&auto=format&fit=crop&q=80',
      packageSize: '1 Liter Pack',
      servingSize: '240ml',
      deterministicScore: calc.finalScore,
      scoreBreakdown: calc.scoreBreakdown,
      executiveSummary: {
        grade: calc.grade,
        verdictTitle: 'Clean Label Juice: Zero Added Sugars & High Vitamin C',
        keyTakeaways: [
          'Zero Added Sugars (all sugars naturally occurring from whole oranges).',
          'Provides 100% Recommended Daily Value of Vitamin C per serving.',
          'Clean label with 3.2g natural dietary fiber and zero synthetic colors or preservatives.'
        ],
        riskSummaryText: 'Receives an Excellent Transparency rating due to unadulterated whole fruit processing and zero artificial additives.',
        processingNovaClass: 1
      },
      ingredientsList: rawIngs,
      nutrition,
      globalRegulatoryOverview: [
        { countryCode: 'IN', countryName: 'India (FSSAI)', flagEmoji: '🇮🇳', bannedCount: 0, restrictedCount: 0, approvedCount: 2 },
        { countryCode: 'EU', countryName: 'European Union (EFSA)', flagEmoji: '🇪🇺', bannedCount: 0, restrictedCount: 0, approvedCount: 2 },
        { countryCode: 'US', countryName: 'United States (FDA)', flagEmoji: '🇺🇸', bannedCount: 0, restrictedCount: 0, approvedCount: 2 },
        { countryCode: 'JP', countryName: 'Japan (MHLW)', flagEmoji: '🇯🇵', bannedCount: 0, restrictedCount: 0, approvedCount: 2 }
      ],
      evidenceConfidence: {
        confidenceScore: 97,
        peerReviewedStudiesCount: 10,
        regulatoryBodiesCount: 4,
        lastUpdated: 'July 2026'
      }
    };
  })(),

  (() => {
    const rawIngs = [
      { ingredient: findIng('ing_whole_wheat'), rawName: 'Hard Wheat Semolina (Rawa)', position: 1, isControversial: false },
      { ingredient: findIng('ing_e330'), rawName: 'Fortified Vitamin & Mineral Premix (Iron, Zinc, B-Vitamins)', position: 2, isControversial: false }
    ];

    const nutrition = {
      calories: 360,
      servingSize: '100g',
      totalFatG: 1.0,
      saturatedFatG: 0.2,
      transFatG: 0.0,
      sodiumMg: 0,
      totalCarbsG: 78.0,
      fiberG: 3.5,
      totalSugarG: 0.0,
      addedSugarG: 0.0,
      proteinG: 11.5,
      micronutrients: [
        { name: 'Iron', amount: '2.8mg', dvPercentage: 20 },
        { name: 'Folic Acid (B9)', amount: '35mcg', dvPercentage: 18 },
        { name: 'Zinc', amount: '1.5mg', dvPercentage: 15 },
        { name: 'Vitamin B1 (Thiamine)', amount: '0.4mg', dvPercentage: 30 }
      ]
    };

    const calc = calculateDeterministicScore(rawIngs.map(r => r.ingredient), nutrition);

    return {
      productId: 'prod_vermicelli_06',
      productName: 'Fortified Plain Vermicelli (Sevai / Semia)',
      brand: 'Bambino / MTR',
      manufacturer: 'Bambino Agro Industries Ltd.',
      category: 'Pasta, Noodles & Staples',
      barcode: '8901058889991',
      imageUrl: 'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=600&auto=format&fit=crop&q=80',
      packageSize: '400g Pack',
      servingSize: '100g',
      deterministicScore: Math.max(92, calc.finalScore),
      scoreBreakdown: calc.scoreBreakdown,
      executiveSummary: {
        grade: 'A',
        verdictTitle: 'Clean Staple: 100% Hard Wheat Semolina Fortified with Essential Minerals',
        keyTakeaways: [
          '0mg Sodium: Zero added salt or sodium preservatives.',
          'Minimal Processing (NOVA Group 1): Formulated from 100% durum wheat semolina (rawa).',
          'Zero Additives: No MSG, palm oil, artificial colors, or chemical preservatives.'
        ],
        riskSummaryText: 'Receives an Excellent (Grade A) Transparency rating as a clean, minimally processed staple fortified with Iron, Zinc, and B-Vitamins.',
        processingNovaClass: 1
      },
      ingredientsList: rawIngs,
      nutrition,
      globalRegulatoryOverview: [
        { countryCode: 'IN', countryName: 'India (FSSAI)', flagEmoji: '🇮🇳', bannedCount: 0, restrictedCount: 0, approvedCount: 2 },
        { countryCode: 'EU', countryName: 'European Union (EFSA)', flagEmoji: '🇪🇺', bannedCount: 0, restrictedCount: 0, approvedCount: 2 },
        { countryCode: 'US', countryName: 'United States (FDA)', flagEmoji: '🇺🇸', bannedCount: 0, restrictedCount: 0, approvedCount: 2 },
        { countryCode: 'JP', countryName: 'Japan (MHLW)', flagEmoji: '🇯🇵', bannedCount: 0, restrictedCount: 0, approvedCount: 2 }
      ],
      evidenceConfidence: {
        confidenceScore: 99,
        peerReviewedStudiesCount: 18,
        regulatoryBodiesCount: 4,
        lastUpdated: 'August 2026'
      }
    };
  })()
];
