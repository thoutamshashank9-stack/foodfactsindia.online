import { createClient } from '@supabase/supabase-js';
import { TransparencyReport, Ingredient, NutritionFacts, ResolvedItem } from '../types';
import { calculateDeterministicScore, evaluateRatingGate } from './scoringEngine';
import { calculateInternationalRatings } from './internationalRatingsEngine';
import { INGREDIENT_DATABASE } from '../data/ingredientsDatabase';
import { analyzeRawIngredientLabel } from './aiAnalyzerService';
import { PRESEEDED_PRODUCTS } from '../data/productsDatabase';
import { matchDecoupledAdditives, tokenizeRawLabelText } from './decoupledAdditiveService';

const SUPABASE_URL = "https://dempjxsrmnzepxbsnwhg.supabase.co";
const SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRlbXBqeHNybW56ZXB4YnNud2hnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODUzMDQ3NzUsImV4cCI6MjEwMDg4MDc3NX0.SO89axui349_3x3zKloLnYD-UGL8vO_p2VR9MCz_xk4";

export const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

const round1 = (val: number | null | undefined): number =>
  typeof val === 'number' && !isNaN(val) ? Math.round(val * 10) / 10 : 0;

function parseSodiumMg(sodium_100g: any, salt_100g: any, category: string = ''): number {
  if (sodium_100g == null) {
    return salt_100g != null ? Math.round(Number(salt_100g) * 400) : 0;
  }
  let sodiumVal = Number(sodium_100g);
  const saltVal = salt_100g != null ? Number(salt_100g) : null;
  
  if (saltVal !== null) {
    if (sodiumVal > saltVal * 3) {
      sodiumVal = sodiumVal / 1000.0;
    }
  } else {
    const isSavory = /salt|soup|savou|season|masala|spice|condiment|bouillon/i.test(category);
    if (sodiumVal > 5.0 && !isSavory) {
      sodiumVal = sodiumVal / 1000.0;
    }
  }
  return Math.round(sodiumVal * 1000);
}


export interface AdditiveFact {
  ins_code: string;
  common_name: string;
  origin: 'natural' | 'synthetic' | 'nature_identical';
  category: string;
  fssai_status: string;
  efsa_status: string;
  fda_status: string;
  adi_value: string | null;
  concern_level: 'LOW' | 'MEDIUM' | 'HIGH';
  accurate_description: string;
  caveat: string | null;
  source_url: string;
  source_citation: string;
}

// In-memory caches for performance optimization
const additiveCache = new Map<string, AdditiveFact | null>();
let catalogCache: { timestamp: number; data: TransparencyReport[] } | null = null;
const CATALOG_TTL_MS = 5 * 60 * 1000; // 5-minute TTL

/**
 * Normalizes user/parser input strings into canonical INS key formats.
 * Examples: "INS 160b", "E-160b(i)", "e160b", "160b" -> "160b"
 */
export function normalizeInsCode(rawCode: string): string {
  if (!rawCode) return '';
  return rawCode
    .trim()
    .toLowerCase()
    .replace(/^ins\s*/i, '')
    .replace(/^e-?/i, '')
    .replace(/\(i+\)$/i, '')
    .trim();
}

/**
 * Anti-Contradiction Runtime Validator.
 * Compares reference database data against raw label text to prevent self-contradictions.
 */
export function validateAdditiveWithRawLabel(
  fact: AdditiveFact,
  rawIngredientText: string
): { isValid: boolean; warning?: string; overrideOrigin?: 'natural' } {
  if (!rawIngredientText) return { isValid: true };

  const lowerRaw = rawIngredientText.toLowerCase();
  const lowerName = fact.common_name.toLowerCase();

  // Pattern check: Raw label explicitly states "natural colour/color" or "natural flavour"
  const claimsNaturalInLabel = 
    lowerRaw.includes(`natural colour (${lowerName}`) ||
    lowerRaw.includes(`natural color (${lowerName}`) ||
    lowerRaw.includes(`natural ${lowerName}`) ||
    lowerRaw.includes(`natural colour`) ||
    lowerRaw.includes(`natural color`);

  // Hard Contradiction: Label says "natural" but reference record flags "synthetic"
  if (claimsNaturalInLabel && fact.origin === 'synthetic') {
    return {
      isValid: false,
      warning: `CONTRADICTION DETECTED: Raw label claims natural origin for '${fact.common_name}' (${fact.ins_code}), but reference data specifies synthetic. Using raw label natural override.`,
      overrideOrigin: 'natural'
    };
  }

  return { isValid: true };
}

/**
 * Primary Lookup Function for Additive Facts from public.additive_reference.
 */
export async function getAdditiveFact(
  rawInsCode: string,
  rawIngredientContext: string = '',
  supabaseClient: any = supabase
): Promise<AdditiveFact | null> {
  const cleanCode = normalizeInsCode(rawInsCode);
  if (!cleanCode) return null;

  // Use decoupled in-memory search engine for O(1) exact matching without text pollution
  const decoupled = matchDecoupledAdditives(cleanCode);
  if (decoupled.length > 0) {
    const primary = decoupled[0];
    return {
      ins_code: primary.insCode || cleanCode,
      common_name: primary.primaryName,
      origin: 'synthetic',
      category: primary.category,
      fssai_status: primary.regulatoryBans.find(r => r.jurisdictionCode === 'IN')?.status || 'RESTRICTED',
      efsa_status: primary.regulatoryBans.find(r => r.jurisdictionCode === 'EU')?.status || 'RESTRICTED',
      fda_status: primary.regulatoryBans.find(r => r.jurisdictionCode === 'US')?.status || 'RESTRICTED',
      adi_value: '0-5 mg/kg body weight',
      concern_level: (primary.riskLevel === 'EXCELLENT' ? 'LOW' : primary.riskLevel) as 'LOW' | 'MEDIUM' | 'HIGH',
      accurate_description: primary.description,
      caveat: primary.regulatoryBans.find(r => r.mandatoryWarningText)?.mandatoryWarningText || null,
      source_url: primary.citations[0]?.doi ? (primary.citations[0].doi.startsWith('http') ? primary.citations[0].doi : `https://doi.org/${primary.citations[0].doi}`) : '',
      source_citation: primary.citations[0]?.title || 'Official Safety Monograph'
    };
  }

  if (additiveCache.has(cleanCode)) {
    return additiveCache.get(cleanCode) || null;
  }

  try {
    const { data } = await supabaseClient
      .from('additive_reference')
      .select('*')
      .eq('ins_code', cleanCode)
      .limit(1)
      .maybeSingle();

    if (data) {
      const fact = data as AdditiveFact;
      additiveCache.set(cleanCode, fact);
      return fact;
    }
  } catch (e) {
    console.error('Additive fact fetch error:', e);
  }

  additiveCache.set(cleanCode, null);
  return null;
}

/**
 * Sanitizes any string to display only clean English ASCII text.
 * Strips non-ASCII characters, multilingual prefixes (en:, fr:, de:, etc.),
 * and returns the English portion only.
 */
function toEnglishOnly(text: string): string {
  if (!text) return '';
  // Remove language-prefixed tokens like "fr:biscuits,en:biscuits" -> keep en: part or first value
  const enMatch = text.match(/\ben:([^,\n;]+)/i);
  if (enMatch) return enMatch[1].trim().replace(/-/g, ' ');
  // Remove all language prefixes (fr:, de:, es:, it:, nl:, pt:, ru:, zh:, ja:, ar:, etc.)
  let clean = text.replace(/\b[a-z]{2}:[^\s,;]+/gi, ' ').trim();
  // Strip remaining non-printable or non-ASCII characters
  clean = clean.replace(/[^\x20-\x7E,.()\[\]\/\-%+&'°]/g, ' ');
  // Collapse extra whitespace
  clean = clean.replace(/\s{2,}/g, ' ').trim();
  // Strip leading/trailing commas
  clean = clean.replace(/^[,;\s]+|[,;\s]+$/g, '').trim();
  return clean || text.replace(/[^\x20-\x7E]/g, '').trim() || 'Unspecified';
}

function cleanRawIngredientText(raw: string): string {
  if (!raw) return '';
  let cleaned = raw
    .replace(/<[^>]*>/g, '') // Strip HTML tags like <span class="allergen">
    .replace(/\bcashew\s+buts\b/gi, 'cashew nuts') // Fix OCR typo
    .replace(/\binvert\s+sugar\s+strup\b/gi, 'invert sugar syrup') // Fix OCR typo
    .trim();

  // Bug 5b: OCR Header Sanitizer — strip brand/marketing text before "ingredients:" keyword
  const ingredientsIdx = cleaned.toLowerCase().indexOf('ingredients:');
  if (ingredientsIdx > 0) {
    cleaned = cleaned.substring(ingredientsIdx + 12).trim();
  }

  return cleaned;
}

/**
 * Bug 5a: Grouped INS Unroller.
 * Splits multi-code strings like "colours (ins 102, ins 133, ins 110)" into
 * individual Ingredient objects for each additive code, rather than returning
 * only the single highest-risk item.
 */
function unrollGroupedAdditives(rawText: string, basePosition: number): Ingredient[] {
  const cleaned = cleanRawIngredientText(rawText);

  // Detect grouped additive patterns: "colours (ins 102, ins 133, ins 110, ins 122)"
  // or "acidity regulators (296, 330)" or "emulsifiers (e471, e472e)"
  const groupMatch = cleaned.match(/^(.*?)\s*\(([^)]+)\)\s*$/i);
  if (!groupMatch) return [resolveIngredientFromRaw(rawText, basePosition)];

  const prefix = groupMatch[1].trim().toLowerCase();
  const inner = groupMatch[2];

  // Check if the prefix is a functional additive group name
  const isAdditiveGroup = /colou?rs?|emulsifiers?|preservatives?|stabilisers?|acidity regulators?|raising agents?|flavou?r enhancers?|antioxidants?|thickeners?|sweeteners?/i.test(prefix);
  if (!isAdditiveGroup) return [resolveIngredientFromRaw(rawText, basePosition)];

  // Split inner codes: "ins 102, ins 133, ins 110, ins 122" or "296, 330"
  const codeParts = inner.split(/[,;]+/).map(s => s.trim()).filter(Boolean);
  if (codeParts.length <= 1) return [resolveIngredientFromRaw(rawText, basePosition)];

  // Resolve each code individually
  const results: Ingredient[] = [];
  codeParts.forEach((code, idx) => {
    const resolved = resolveIngredientFromRaw(code, basePosition + idx * 0.1);
    results.push(resolved);
  });

  return results;
}

/**
 * Enhanced ingredient resolution engine:
 * 1. Checks exact match / synonym match in INGREDIENT_DATABASE
 * 2. Scans for embedded INS / E-number additive codes (e.g. 503(ii), 500(ii), 322, 471, 472e)
 * 3. Constructs structured additive objects for matched codes instead of defaulting to WHOLE_FOOD
 */
function resolveIngredientFromRaw(rawText: string, position: number): Ingredient {
  const cleaned = cleanRawIngredientText(rawText);
  const lower = cleaned.toLowerCase();

  // Bug 5c: Hydrogenated Oil Classification — must come BEFORE whole food fallback
  if (/hydrogenated|partially hydrogenated/i.test(lower)) {
    return {
      id: `ing_transfat_${position}`,
      canonicalName: cleaned,
      synonyms: [cleaned, 'hydrogenated fat', 'trans fat source'],
      category: 'PROCESSING_AID' as const,
      riskLevel: 'HIGH' as const,
      baseRiskWeight: -20,
      description: 'Hydrogenated vegetable oil is an industrial trans fat source. WHO targets global elimination by 2023. Associated with cardiovascular disease, LDL cholesterol elevation, and systemic inflammation.',
      processingLevel: 'NOVA_4_ULTRA_PROCESSED' as const,
      regulatoryRecords: [
        {
          countryCode: 'IN' as const,
          countryName: 'India (FSSAI)',
          flagEmoji: '🇮🇳',
          status: 'RESTRICTED' as const,
          restrictionDetails: 'FSSAI mandates trans fat < 2% in oils/fats (2022 regulation).',
          regulationRef: 'FSSAI Trans Fat Regulation 2022'
        },
        {
          countryCode: 'US' as const,
          countryName: 'United States (FDA)',
          flagEmoji: '🇺🇸',
          status: 'BANNED' as const,
          restrictionDetails: 'FDA revoked GRAS status for partially hydrogenated oils (PHOs) in 2018.',
          regulationRef: 'FDA Final Rule 21 CFR 189.1 (2018)'
        }
      ],
      citations: [{
        id: 'cit_who_replace',
        title: 'WHO REPLACE Trans Fat Action Package',
        journal: 'World Health Organization',
        year: 2018,
        doi: 'https://www.who.int/publications/i/item/replace-trans-fat',
        summary: 'Global strategy to eliminate industrially produced trans fat from food supply by 2023.',
        evidenceStrength: 'STRONG' as const
      }]
    };
  }

  // 1. Direct or Synonym Match
  const directMatch = INGREDIENT_DATABASE.find(
    k => k.canonicalName.toLowerCase() === lower ||
         k.synonyms.some(s => s.toLowerCase() === lower)
  );
  if (directMatch) return directMatch;

  // 2. Decoupled Set-Based Token Matching (O(1) complexity with cluster pre-tokenizer)
  const decoupledMatches = matchDecoupledAdditives(cleaned);
  if (decoupledMatches.length > 0) {
    const primary = decoupledMatches[0];
    const ingredientMatch = INGREDIENT_DATABASE.find(i => i.id === primary.id);
    if (ingredientMatch) return ingredientMatch;

    return {
      id: primary.id,
      canonicalName: primary.primaryName,
      scientificName: primary.chemicalName,
      synonyms: [primary.primaryName, primary.insCode || '', primary.eNumber || ''].filter(Boolean),
      insNumber: primary.insCode,
      eNumber: primary.eNumber,
      category: primary.category,
      riskLevel: primary.riskLevel,
      baseRiskWeight: primary.baseRiskWeight,
      description: primary.description,
      processingLevel: primary.processingLevel,
      regulatoryRecords: primary.regulatoryBans.map(r => ({
        countryCode: r.jurisdictionCode,
        countryName: r.jurisdictionCode === 'US' ? 'United States (FDA)' : (r.jurisdictionCode === 'JP' ? 'Japan (MHLW)' : (r.jurisdictionCode === 'EU' ? 'European Union (EFSA)' : 'India (FSSAI)')),
        flagEmoji: r.jurisdictionCode === 'US' ? '🇺🇸' : (r.jurisdictionCode === 'JP' ? '🇯🇵' : (r.jurisdictionCode === 'EU' ? '🇪🇺' : '🇮🇳')),
        status: r.status,
        restrictionDetails: r.restrictionDetails,
        regulationRef: r.regulationRef,
        scopeCategory: r.scopeCategory,
        maxLimitMgKg: r.maxLimitMgKg
      })),
      citations: primary.citations || []
    };
  }

  // 3. Fallback: Check if raw text indicates an additive category
  const isAdditiveText = /raising agent|emulsifier|preservative|antioxidant|flavour enhancer|color|colour|stabiliser|acidity regulator/i.test(cleaned);

  const rawTokens = tokenizeRawLabelText(cleaned);
  if (isAdditiveText || rawTokens.length > 0) {
    const primaryCode = rawTokens[0] || 'INS Additive';
    return {
      id: `ing_detected_${position}_${primaryCode}`,
      canonicalName: cleaned,
      synonyms: [cleaned, primaryCode],
      category: isAdditiveText && /emulsifier/i.test(cleaned) ? ('EMULSIFIER' as const) : ('PROCESSING_AID' as const),
      riskLevel: 'MEDIUM' as const,
      baseRiskWeight: -8,
      description: `Declared functional food additive (${primaryCode}). Requires daily intake vigilance.`,
      processingLevel: 'NOVA_4_ULTRA_PROCESSED' as const,
      regulatoryRecords: [
        {
          countryCode: 'IN' as const,
          countryName: 'India (FSSAI)',
          flagEmoji: '🇮🇳',
          status: 'RESTRICTED' as const,
          restrictionDetails: 'Permitted food additive under FSSAR 2011 limits.',
          regulationRef: 'FSSAI Additives Schedule'
        }
      ],
      citations: []
    };
  }

  // 4. Standard Whole Food Fallback
  return {
    id: `ing_raw_${position}`,
    canonicalName: cleaned,
    synonyms: [cleaned],
    category: 'WHOLE_FOOD' as const,
    riskLevel: 'LOW' as const,
    baseRiskWeight: 0,
    description: 'Standard food ingredient declared on packaging.',
    processingLevel: 'NOVA_1_UNPROCESSED' as const,
    regulatoryRecords: [],
    citations: []
  };
}

// Client-Side In-Memory Cache & Request Deduplication
const reportCache = new Map<string, TransparencyReport>();
const searchCache = new Map<string, TransparencyReport[]>();
const resolvedItemCache = new Map<string, ResolvedItem>();
const inflightBarcodeRequests = new Map<string, Promise<ResolvedItem>>();

export function isNonFoodProduct(p: any): boolean {
  if (!p) return false;
  
  const cat = String(p.categories || p.category || p.sub_category || p.product_type || '').toLowerCase();
  const name = String(p.product_name || p.productName || '').toLowerCase();
  const brand = String(p.brands || p.brand || '').toLowerCase();
  const ings = String(p.ingredients_text || p.rawIngredients || '').toLowerCase();

  const nonFoodKeywords = [
    'beauty', 'cosmetic', 'cosmetics', 'skin', 'skincare', 'hair', 'shampoo',
    'conditioner', 'soap', 'soaps', 'body wash', 'face wash', 'facewash',
    'lotion', 'cream', 'creams', 'moisturizer', 'moisturiser', 'perfume', 'fragrance',
    'deodorant', 'makeup', 'make-up', 'lipstick', 'lip balm', 'mascara', 'sunscreen',
    'serum', 'toothpaste', 'toothbrush', 'detergent', 'sanitizer', 'cleanser',
    'hygiene', 'personal care', 'essential oil', 'nail polish', 'foundation', 'toner',
    'eau de', 'toilette', 'parfum', 'anti-perspirant', 'antiperspirant', 'shaving',
    'razor', 'shower gel', 'bath gel', 'hair oil', 'hair color', 'hair dye', 'nivea',
    'dove', "l'oreal", 'loreal', 'lakme', 'garnier', 'biotique', 'mamaearth', 'himalaya',
    'lotus herbals', 'cetaphil', 'neutrogena', 'derma', 'vaseline', 'tresemme',
    'head & shoulders', 'pantene', 'sunsilk', 'clinic plus', 'lifebuoy', 'lux',
    'cinthol', 'pears', 'dettol', 'fiama', 'vivel', 'yardley', 'old spice', 'axe',
    'medicine', 'medicines', 'pharma', 'pharmaceutical', 'tablet', 'tablets',
    'capsule', 'capsules', 'syrup', 'ointment', 'gel', 'drug', 'drugs', 'paracetamol',
    'ibuprofen', 'aspirin', 'antibiotic', 'medical', 'prescription'
  ];

  const cosmeticIngredients = [
    'sodium laureth sulfate', 'sodium lauryl sulfate', 'dimethicone',
    'phenoxyethanol', 'ci 77891', 'ci 19140', 'ci 42090', 'triethanolamine',
    'carbomer', 'disodium edta', 'ethylhexylglycerin', 'cetearyl alcohol'
  ];

  const hasKeyword = nonFoodKeywords.some(kw => 
    cat.includes(kw) || name.includes(kw) || brand.includes(kw)
  );

  const hasCosmeticIng = cosmeticIngredients.some(ci => ings.includes(ci));

  return hasKeyword || hasCosmeticIng;
}

export async function resolveBarcode(barcode: string): Promise<ResolvedItem> {
  const clean = barcode.trim();
  if (!/^[0-9]{8,14}$/.test(clean)) {
    return { kind: 'unknown', barcode: clean };
  }

  const cacheKey = `resolved_v2_${clean}`;
  if (resolvedItemCache.has(cacheKey)) {
    return resolvedItemCache.get(cacheKey)!;
  }

  if (inflightBarcodeRequests.has(clean)) {
    return inflightBarcodeRequests.get(clean)!;
  }

  const requestPromise = (async (): Promise<ResolvedItem> => {
    try {
      // 1. Check local preseeded products database
      const preseededMatch = PRESEEDED_PRODUCTS.find(p => p.barcode === clean);
      if (preseededMatch) {
        let result: ResolvedItem;
        if (isNonFoodProduct(preseededMatch)) {
          result = {
            kind: 'non_food',
            category: preseededMatch.category || 'Non-Food Item',
            productName: preseededMatch.productName,
            brand: preseededMatch.brand,
            barcode: clean
          };
        } else {
          result = { kind: 'food', product: preseededMatch };
        }
        resolvedItemCache.set(cacheKey, result);
        return result;
      }

      // 2. Query Supabase Database
      try {
        const unpadded = clean.replace(/^0+/, '');
        const candidates = Array.from(new Set([
          clean,
          unpadded,
          unpadded.padStart(8, '0'),
          unpadded.padStart(12, '0'),
          unpadded.padStart(13, '0'),
          unpadded.padStart(14, '0')
        ]));
        const matchQuery = candidates.map(c => `barcode.eq.${c}`).join(',');

        const { data: dbProducts } = await supabase
          .from('products')
          .select('*')
          .or(matchQuery)
          .limit(1);

        if (dbProducts && dbProducts.length > 0) {
          const p = dbProducts[0];
          let result: ResolvedItem;
          if (isNonFoodProduct(p)) {
            result = {
              kind: 'non_food',
              category: p.categories || p.product_type || 'Cosmetics / Medicine',
              productName: p.product_name,
              brand: p.brands,
              barcode: clean
            };
          } else {
            const report = await mapProductToReport(p);
            result = { kind: 'food', product: report };
          }
          resolvedItemCache.set(cacheKey, result);
          return result;
        }
      } catch (err) {
        console.error('Supabase barcode lookup error:', err);
      }

      // 3. Fallback: Query Open Food Facts Live Network
      try {
        const unpadded = clean.replace(/^0+/, '');
        const report = await fetchOpenFoodFactsProduct(unpadded);
        if (report) {
          // Map to Supabase structure
          const dbProduct = {
            barcode: clean,
            product_name: report.productName,
            brands: report.brand,
            categories: report.category,
            ingredients_text: report.ingredientsList.map(i => i.rawName).join(', '),
            nova_group: report.executiveSummary.processingNovaClass,
            energy_100g: report.nutrition.calories,
            sugars_100g: report.nutrition.totalSugarG,
            fat_100g: report.nutrition.totalFatG,
            saturated_fat_100g: report.nutrition.saturatedFatG,
            trans_fat_100g: report.nutrition.transFatG,
            fibre_100g: report.nutrition.fiberG,
            protein_100g: report.nutrition.proteinG,
            sodium_100g: report.nutrition.sodiumMg ? report.nutrition.sodiumMg / 1000 : null,
            salt_100g: report.nutrition.sodiumMg ? (report.nutrition.sodiumMg * 2.5) / 1000 : null
          };

          // Persist to Supabase asynchronously to avoid blocking the UI
          (async () => {
            try {
              const { error } = await supabase.from('products').upsert(dbProduct, { onConflict: 'barcode' });
              if (!error) {
                // Persist ingredients
                const ingredientsToInsert = report.ingredientsList.map(ing => ({
                  barcode: clean,
                  ingredient_raw: ing.rawName,
                  position: ing.position
                }));
                if (ingredientsToInsert.length > 0) {
                  await supabase.from('product_ingredients').delete().eq('barcode', clean);
                  await supabase.from('product_ingredients').insert(ingredientsToInsert);
                }

                // Persist additives
                const additiveCodesSet = new Set<string>();
                if (report.labelWarnings) {
                  for (const warning of report.labelWarnings) {
                    if (warning.appliedAdditives) {
                      for (const add of warning.appliedAdditives) {
                        additiveCodesSet.add(add.toUpperCase());
                      }
                    }
                  }
                }
                if (report.ingredientsList) {
                  for (const ing of report.ingredientsList) {
                    if (ing.ingredient.eNumber) {
                      additiveCodesSet.add(ing.ingredient.eNumber.toUpperCase());
                    }
                    if (ing.ingredient.insNumber) {
                      additiveCodesSet.add(ing.ingredient.insNumber.toUpperCase());
                    }
                  }
                }
                const additivesToInsert = Array.from(additiveCodesSet).map(code => ({
                  barcode: clean,
                  additive_code: code
                }));
                if (additivesToInsert.length > 0) {
                  await supabase.from('product_additives').delete().eq('barcode', clean);
                  await supabase.from('product_additives').insert(additivesToInsert);
                }
              } else {
                console.error('Supabase write failure for OFF live fallback:', error);
              }
            } catch (dbErr) {
              console.error('Supabase write error for OFF live fallback:', dbErr);
            }
          })().catch(dbErr => {
            console.error('Unhandled error in background DB write:', dbErr);
          });

          const result: ResolvedItem = { kind: 'food', product: report };
          resolvedItemCache.set(cacheKey, result);
          return result;
        }
      } catch (err) {
        console.error('Open Food Facts live lookup or persistence error:', err);
      }

      // 4. Fallback: Unknown / Not Found in database
      const unknownResult: ResolvedItem = { kind: 'unknown', barcode: clean };
      resolvedItemCache.set(cacheKey, unknownResult);
      return unknownResult;
    } finally {
      inflightBarcodeRequests.delete(clean);
    }
  })();

  inflightBarcodeRequests.set(clean, requestPromise);
  return requestPromise;
}

export async function fetchOpenFoodFactsProduct(barcode: string): Promise<TransparencyReport | null> {
  const clean = barcode.trim();
  if (!/^[0-9]{8,14}$/.test(clean)) return null;

  try {
    const res = await fetch(`/api/product?barcode=${clean}`);
    if (!res.ok) return null;
    const json = await res.json();
    if (!json || json.status !== 1 || !json.product) return null;

    const p = json.product;
    if (isNonFoodProduct(p)) return null;

    const nutriments = p.nutriments || {};

    if (!p.ingredients_text || !p.ingredients_text.trim()) return null;
    const rawIngs = p.ingredients_text.trim();
    const report = analyzeRawIngredientLabel(
      rawIngs,
      toEnglishOnly(p.product_name || `Scanned Product (${clean})`),
      toEnglishOnly(p.brands || 'Authentic Brand')
    );

    report.barcode = clean;
    report.productId = `prod_off_${clean}`;
    report.imageUrl = p.image_front_url || `/api/img/${clean}`;
    report.imageFrontUrl = p.image_front_url || `/api/img/${clean}`;
    report.category = toEnglishOnly(p.categories || report.category);

    if (p.quantity) {
      const qty = toEnglishOnly(String(p.quantity));
      report.packageSize = qty.toLowerCase().includes('pack') ? qty : `${qty}`;
      report.servingSize = qty;
    }

    if (nutriments['energy-kcal_100g'] != null) {
      report.nutrition.calories = Math.round(Number(nutriments['energy-kcal_100g']));
    }
    if (nutriments.fat_100g != null) {
      report.nutrition.totalFatG = round1(Number(nutriments.fat_100g));
    }
    if (nutriments['saturated-fat_100g'] != null) {
      report.nutrition.saturatedFatG = round1(Number(nutriments['saturated-fat_100g']));
    }
    report.nutrition.sodiumMg = parseSodiumMg(nutriments.sodium_100g, nutriments.salt_100g, report.category);
    if (nutriments.sugars_100g != null) {
      report.nutrition.totalSugarG = round1(Number(nutriments.sugars_100g));
      report.nutrition.addedSugarG = round1(Number(nutriments.sugars_100g));
    }
    if (nutriments.proteins_100g != null) {
      report.nutrition.proteinG = round1(Number(nutriments.proteins_100g));
    }

    return report;
  } catch (e) {
    return null;
  }
}

export async function searchLiveProducts(query: string): Promise<TransparencyReport[]> {
  if (!query.trim()) return [];
  
  const q = query.trim().toLowerCase();
  if (searchCache.has(q)) {
    return searchCache.get(q)!;
  }

  const isNumericBarcode = /^[0-9]{8,14}$/.test(q);
  let products: any[] = [];

  if (isNumericBarcode) {
    const unpadded = q.replace(/^0+/, '');
    const candidates = Array.from(new Set([
      q,
      unpadded,
      unpadded.padStart(8, '0'),
      unpadded.padStart(12, '0'),
      unpadded.padStart(13, '0'),
      unpadded.padStart(14, '0')
    ]));
    const matchQuery = candidates.map(c => `barcode.eq.${c}`).join(',');

    const { data } = await supabase
      .from('products')
      .select('*')
      .or(matchQuery)
      .limit(10);
    products = data || [];
  } else {
    const { data } = await supabase
      .from('products')
      .select('*')
      .or(`product_name.ilike.%${q}%,brands.ilike.%${q}%,categories.ilike.%${q}%`)
      .limit(20);
    products = data || [];
  }

  const validFoodProducts = products.filter(p => !isNonFoodProduct(p));
  const reports = await batchMapProductsToReports(validFoodProducts);

  searchCache.set(q, reports);
  return reports;
}

export async function fetchLiveCatalog(): Promise<TransparencyReport[]> {
  if (catalogCache && (Date.now() - catalogCache.timestamp < CATALOG_TTL_MS)) {
    return catalogCache.data;
  }

  const { data: products, error } = await supabase
    .from('products')
    .select('*')
    .limit(40);

  if (error || !products) {
    console.error('Supabase catalog error:', error);
    return [];
  }

  const reports = await batchMapProductsToReports(products);

  catalogCache = { timestamp: Date.now(), data: reports };
  return reports;
}

/** Map a product category string to FSSAI Food Category System (FCS) code. */
function getFssaiCategoryCode(category: string): string | null {
  if (!category) return null;
  const cat = category.toLowerCase();
  
  // Specific patterns first
  if (cat.includes('ice cream') || cat.includes('ice lolly') || cat.includes('sherbet') || cat.includes('sorbet') || cat.includes('cassatta')) return 'CAT_03';
  if (cat.includes('savoury') || cat.includes('snack') || cat.includes('chip') || cat.includes('crisp') || cat.includes('namkeen') || cat.includes('popcorn') || cat.includes('extruded') || cat.includes('pringles') || cat.includes('doritos')) return 'CAT_15';
  if (cat.includes('beverage') || cat.includes('drink') || cat.includes('soda') || cat.includes('cola') || cat.includes('juice') || cat.includes('water') || cat.includes('squash') || cat.includes('energy drink') || cat.includes('syrup') || cat.includes('sharbat')) return 'CAT_14';
  if (cat.includes('confectionery') || cat.includes('chocolate') || cat.includes('candy') || cat.includes('toffee') || cat.includes('lollipop') || cat.includes('caramel') || cat.includes('sweet snacks') || cat.includes('m&m') || cat.includes('snickers')) return 'CAT_05';
  
  // General categories
  if (cat.includes('dairy') || cat.includes('milk') || cat.includes('cheese') || cat.includes('yogurt') || cat.includes('cream') || cat.includes('paneer')) return 'CAT_01';
  if (cat.includes('fat') || cat.includes(' oil') || cat.includes('butter') || cat.includes('margarine')) return 'CAT_02';
  if (cat.includes('fruit') || cat.includes('vegetable') || cat.includes('jam') || cat.includes('jelly') || cat.includes('pickle') || cat.includes('chutney')) return 'CAT_04';
  if (cat.includes('cereal') || cat.includes('flour') || cat.includes('grain') || cat.includes('pasta') || cat.includes('rice') || cat.includes('vermicelli')) return 'CAT_06';
  if (cat.includes('bakery') || cat.includes('bread') || cat.includes('cake') || cat.includes('biscuit') || cat.includes('cookie') || cat.includes('pastry') || cat.includes('rusk') || cat.includes('toast') || cat.includes('oreo')) return 'CAT_07';
  if (cat.includes('meat') || cat.includes('poultry') || cat.includes('chicken') || cat.includes('mutton') || cat.includes('pork') || cat.includes('beef') || cat.includes('sausage') || cat.includes('deli')) return 'CAT_08';
  if (cat.includes('fish') || cat.includes('seafood') || cat.includes('prawn') || cat.includes('shrimp') || cat.includes('crab')) return 'CAT_09';
  if (cat.includes('egg')) return 'CAT_10';
  if (cat.includes('sweetener') || cat.includes('honey')) return 'CAT_11';
  if (cat.includes('salt') || cat.includes('spice') || cat.includes('soup') || cat.includes('sauce') || cat.includes('condiment') || cat.includes('ketchup') || cat.includes('dressing')) return 'CAT_12';
  if (cat.includes('infant') || cat.includes('baby') || cat.includes('medical food') || cat.includes('formula')) return 'CAT_13';
  return null;
}


export async function batchMapProductsToReports(products: any[]): Promise<TransparencyReport[]> {
  if (products.length === 0) return [];
  
  const uncachedProducts = products.filter(p => !reportCache.has(String(p.barcode)));
  const uncachedBarcodes = uncachedProducts.map(p => String(p.barcode));
  
  if (uncachedBarcodes.length === 0) {
    return products.map(p => reportCache.get(String(p.barcode))!);
  }

  // 1. Fetch ingredients and additives for all uncached products
  const [{ data: dbIngredients }, { data: dbAdditives }] = await Promise.all([
    supabase
      .from('product_ingredients')
      .select('barcode, ingredient_raw, position')
      .in('barcode', uncachedBarcodes)
      .order('position', { ascending: true }),
    supabase
      .from('product_additives')
      .select('barcode, additive_code')
      .in('barcode', uncachedBarcodes)
  ]);

  const ingredientsByBarcode = new Map<string, any[]>();
  const additivesByBarcode = new Map<string, any[]>();
  
  dbIngredients?.forEach(ing => {
    if (!ingredientsByBarcode.has(ing.barcode)) ingredientsByBarcode.set(ing.barcode, []);
    ingredientsByBarcode.get(ing.barcode)!.push(ing);
  });
  
  const allAdditiveCodesSet = new Set<string>();
  dbAdditives?.forEach(add => {
    if (!additivesByBarcode.has(add.barcode)) additivesByBarcode.set(add.barcode, []);
    additivesByBarcode.get(add.barcode)!.push(add);
    allAdditiveCodesSet.add(add.additive_code.toUpperCase());
  });

  // 2. Fetch category limits
  const fssaiCategories = Array.from(new Set(uncachedProducts.map(p => getFssaiCategoryCode(p.categories || p.category || '')).filter(Boolean))) as string[];
  let allCatLimits: any[] = [];
  if (fssaiCategories.length > 0) {
    const { data: catLimits } = await supabase.from('fssai_category_limits').select('*').in('category_code', fssaiCategories);
    allCatLimits = catLimits || [];
  }

  // 3. Fetch additive rulebook
  let rulebookData: any[] = [];
  if (allAdditiveCodesSet.size > 0) {
    const { data: rules } = await supabase
      .from('additive_rulebook')
      .select('*')
      .in('additive_code', Array.from(allAdditiveCodesSet));
    rulebookData = rules || [];
  }

  // 4. Pre-fetch unknown INS codes for all ingredients
  const allInsCodes: string[] = [];
  dbIngredients?.forEach((ing: any) => {
    const raw = cleanRawIngredientText(ing.ingredient_raw || '');
    const codeMatches = Array.from(raw.matchAll(/([0-9]{3,4}(?:\\([a-z0-9]+\\))?)/gi)).map(m => m[1]);
    if (/annatto/i.test(raw)) codeMatches.push('160b');
    if (/caramel/i.test(raw)) codeMatches.push('150d');
    if (/metabisulfite/i.test(raw)) codeMatches.push('223');
    if (/lecithin/i.test(raw)) codeMatches.push('322');
    if (/msg|glutamate/i.test(raw)) codeMatches.push('621');
    allInsCodes.push(...codeMatches);
  });

  const uniqueInsCodes = Array.from(new Set(allInsCodes.map(normalizeInsCode))).filter(Boolean);
  const uncachedCodes = uniqueInsCodes.filter(code => !additiveCache.has(code));

  if (uncachedCodes.length > 0) {
    const { data: refData } = await supabase
      .from('additive_reference')
      .select('*')
      .in('ins_code', uncachedCodes);

    refData?.forEach((row: any) => {
      const fact: AdditiveFact = {
        ins_code: row.ins_code,
        common_name: row.common_name,
        origin: row.origin,
        category: row.category,
        fssai_status: row.fssai_status,
        efsa_status: row.efsa_status,
        fda_status: row.fda_status,
        adi_value: row.adi_value,
        concern_level: row.concern_level,
        accurate_description: row.accurate_description,
        caveat: row.caveat,
        source_url: row.source_url,
        source_citation: row.source_citation
      };
      additiveCache.set(row.ins_code, fact);
    });
  }

  // 5. Build reports synchronously
  const results = await Promise.all(products.map(async (p) => {
    const barcode = String(p.barcode);
    if (reportCache.has(barcode)) {
      return reportCache.get(barcode)!;
    }

    const fssaiCatCode = getFssaiCategoryCode(p.categories || p.category || '');
    const pIngredients = ingredientsByBarcode.get(barcode) || [];
    const pAdditives = additivesByBarcode.get(barcode) || [];
    const pCatLimits = allCatLimits.filter(cl => cl.category_code === fssaiCatCode);
    
    return mapProductToReportWithData(p, pIngredients, pAdditives, pCatLimits, rulebookData);
  }));

  return results;
}

export async function mapProductToReport(p: any): Promise<TransparencyReport> {
  const reports = await batchMapProductsToReports([p]);
  return reports[0];
}

export async function mapProductToReportWithData(p: any, dbIngredients: any[], dbAdditives: any[], dbCatLimits: any[], rulebookData: any[]): Promise<TransparencyReport> {
  const barcode = String(p.barcode);
  if (reportCache.has(barcode)) {
    return reportCache.get(barcode)!;
  }

    const additiveCodes = (dbAdditives || []).map((a: any) => a.additive_code.toUpperCase());

const nutrition: NutritionFacts = {
    calories: p.energy_100g != null ? Math.round(Number(p.energy_100g)) : null,
    servingSize: p.serving_size || p.quantity || '100g',
    totalFatG: round1(p.fat_100g),
    saturatedFatG: round1(p.saturated_fat_100g),
    transFatG: round1(p.trans_fat_100g),
    sodiumMg: parseSodiumMg(p.sodium_100g, p.salt_100g, p.categories || ''),
    totalCarbsG: p.carbohydrates_100g != null ? round1(p.carbohydrates_100g) : null,
    fiberG: round1(p.fibre_100g),
    totalSugarG: round1(p.sugars_100g),
    addedSugarG: round1(p.sugars_100g),
    proteinG: round1(p.protein_100g)
  };

  // Pre-extract and batch query all INS codes to eliminate N+1 database queries
  if (dbIngredients && dbIngredients.length > 0) {
    const allInsCodes: string[] = [];
    dbIngredients.forEach((ing: any) => {
      const raw = cleanRawIngredientText(ing.ingredient_raw || '');
      const codeMatches = Array.from(raw.matchAll(/([0-9]{3,4}(?:\([a-z0-9]+\))?)/gi)).map(m => m[1]);
      if (/annatto/i.test(raw)) codeMatches.push('160b');
      if (/caramel/i.test(raw)) codeMatches.push('150d');
      if (/metabisulfite/i.test(raw)) codeMatches.push('223');
      if (/lecithin/i.test(raw)) codeMatches.push('322');
      if (/msg|glutamate/i.test(raw)) codeMatches.push('621');
      allInsCodes.push(...codeMatches);
    });

    const uniqueInsCodes = Array.from(new Set(allInsCodes.map(normalizeInsCode))).filter(Boolean);
    const uncachedCodes = uniqueInsCodes.filter(code => !additiveCache.has(code));

    if (uncachedCodes.length > 0) {
      const { data: refData } = await supabase
        .from('additive_reference')
        .select('*')
        .in('ins_code', uncachedCodes);

      refData?.forEach((row: any) => {
        const fact: AdditiveFact = {
          ins_code: row.ins_code,
          common_name: row.common_name,
          origin: row.origin,
          category: row.category,
          fssai_status: row.fssai_status,
          efsa_status: row.efsa_status,
          fda_status: row.fda_status,
          adi_value: row.adi_value,
          concern_level: row.concern_level,
          accurate_description: row.accurate_description,
          caveat: row.caveat,
          source_url: row.source_url,
          source_citation: row.source_citation
        };
        additiveCache.set(row.ins_code, fact);
      });
    }
  }

  // Build clean, deduplicated ingredients list asynchronously with getAdditiveFact lookups
  const rawIngredientsList = (dbIngredients && dbIngredients.length > 0)
    ? (await Promise.all(dbIngredients.map(async (ing: any) => {
        const raw = cleanRawIngredientText(ing.ingredient_raw || '');

        // Bug 5a: Unroll grouped additives like "colours (ins 102, ins 133, ins 110)"
        const unrolledIngredients = unrollGroupedAdditives(raw, ing.position);
        let resolved = unrolledIngredients[0]; // Primary resolved ingredient

        // Extract ALL embedded INS/E codes or keywords in raw ingredient text
        const codeMatches = Array.from(raw.matchAll(/([0-9]{3,4}(?:\([a-z0-9]+\))?)/gi))
          .map(m => m[1]);
        if (/annatto/i.test(raw)) codeMatches.push('160b');
        if (/caramel/i.test(raw)) codeMatches.push('150d');
        if (/metabisulfite/i.test(raw)) codeMatches.push('223');
        if (/lecithin/i.test(raw)) codeMatches.push('322');
        if (/msg|glutamate/i.test(raw)) codeMatches.push('621');
        if (/carmoisine|azorubine/i.test(raw)) codeMatches.push('122');
        if (/tartrazine/i.test(raw)) codeMatches.push('102');
        if (/sunset yellow/i.test(raw)) codeMatches.push('110');
        if (/ponceau/i.test(raw)) codeMatches.push('124');
        if (/allura red/i.test(raw)) codeMatches.push('129');
        if (/brilliant blue/i.test(raw)) codeMatches.push('133');
        if (/titanium dioxide/i.test(raw)) codeMatches.push('171');

        const uniqueKeys = Array.from(new Set(codeMatches));
        const facts: AdditiveFact[] = [];
        for (const key of uniqueKeys) {
          const f = await getAdditiveFact(key, raw, supabase);
          if (f && !facts.some(existing => existing.ins_code === f.ins_code)) {
            facts.push(f);
          }
        }

        if (facts.length > 0) {
          const desc = facts
            .map(f => `${f.common_name}: ${f.accurate_description}${f.caveat ? ' (' + f.caveat + ')' : ''}`)
            .join(' | ');

          const hasHigh = facts.some(f => f.concern_level === 'HIGH');
          const hasMedium = facts.some(f => f.concern_level === 'MEDIUM');
          const overallRisk = hasHigh ? 'HIGH' : (hasMedium ? 'MEDIUM' : 'LOW');

          const citations = facts.map(f => ({
            id: `cit_${f.ins_code}`,
            title: f.source_citation,
            journal: 'Official Safety Evaluation',
            year: new Date().getFullYear(),
            doi: f.source_url || `10.1000/ins_${f.ins_code}`,
            summary: f.accurate_description,
            evidenceStrength: 'STRONG' as const
          }));

          resolved = {
            ...resolved,
            canonicalName: facts.map(f => f.common_name).join(' & ') || resolved.canonicalName,
            description: desc,
            riskLevel: overallRisk as any,
            citations: citations.length > 0 ? citations : resolved.citations
          };
        }

        // Return primary + any additional unrolled additives as separate line items
        const primaryResult = {
          ingredient: resolved,
          rawName: raw,
          position: ing.position,
          isControversial: resolved.riskLevel !== 'LOW' || additiveCodes.some(c => raw.toUpperCase().includes(c))
        };

        // Bug 5a: Add remaining unrolled additives as separate line items
        const additionalUnrolled = unrolledIngredients.slice(1).map((unrolledIng, idx) => ({
          ingredient: unrolledIng,
          rawName: unrolledIng.canonicalName,
          position: ing.position + (idx + 1) * 0.1,
          isControversial: unrolledIng.riskLevel !== 'LOW'
        }));

        return [primaryResult, ...additionalUnrolled];
      }))).flat()
    : [
        {
          ingredient: {
            id: 'ing_raw_1',
            canonicalName: p.ingredients_text ? cleanRawIngredientText(p.ingredients_text) : 'Standard Ingredients',
            synonyms: [p.ingredients_text || 'Standard Ingredients'],
            category: 'WHOLE_FOOD' as const,
            riskLevel: 'LOW' as const,
            baseRiskWeight: 0,
            description: 'Declared food ingredients mix.',
            processingLevel: 'NOVA_1_UNPROCESSED' as const,
            regulatoryRecords: [],
            citations: []
          },
          rawName: p.ingredients_text ? cleanRawIngredientText(p.ingredients_text) : 'Declared ingredients list',
          position: 1,
          isControversial: false
        }
      ];

  // Deduplicate ingredients by canonicalName
  const seenCanonical = new Set<string>();
  const ingredientsList = rawIngredientsList.filter(item => {
    const key = item.ingredient.canonicalName.toLowerCase();
    if (seenCanonical.has(key)) return false;
    seenCanonical.add(key);
    return true;
  });

  // Data Completeness Gating Check
  // Use field-presence (null) not zero-equality to avoid flagging diet soda, water, or
  // table salt — all of which can legitimately have calories === 0 or carbs === 0.
  const hasPlaceholderIngredients = ingredientsList.some(i =>
    i.rawName.toLowerCase().includes('declared ingredients list') ||
    i.ingredient.canonicalName.toLowerCase().includes('standard ingredients')
  );
  // A product is incomplete if the DB row never had energy OR fat+sugar fields populated.
  const isNutritionAbsent =
    p.energy_100g == null &&
    p.fat_100g == null &&
    p.sugars_100g == null;

  // Bug 5d: Enhanced completeness gate — also catch products where all nutrition values are zero
  // (indicates missing data, not genuinely zero-calorie food like water)
  const isAllNutritionZero = nutrition.calories === 0 && nutrition.totalFatG === 0 
    && nutrition.totalSugarG === 0 && nutrition.sodiumMg === 0 && nutrition.proteinG === 0;
  const isDataIncomplete = hasPlaceholderIngredients || isNutritionAbsent
    || (isAllNutritionZero && ingredientsList.length > 3);

  // Calculate score using standard scoring engine
  const scoreResult = calculateDeterministicScore(ingredientsList.map(i => i.ingredient), nutrition);

  // 1. Compute WHO Nutrition Benchmark Flags (with Energy-Adjusted Free Sugar Calculation)
  const whoNutritionFlags: any[] = [];

  // Sodium Flag
  if (nutrition.sodiumMg > 600) {
    whoNutritionFlags.push({
      nutrient: 'Sodium',
      flagType: 'HIGH_SODIUM',
      label: 'High Sodium per 100g',
      valueDeclared: `${nutrition.sodiumMg} mg / 100g`,
      whoBenchmark: 'FoodFactsIndia Heuristic (> 600 mg/100g); WHO Adult Daily Target: < 2,000 mg/day',
      severity: 'CRITICAL',
      citation: 'WHO Guideline: Sodium Intake for Adults and Children (2012)'
    });
  }

  // Free Sugars Flag (Energy-Adjusted with zero-calorie & missing energy guard clause)
  const sugarFlag = calculateWHOSugarFlag(nutrition);
  if (sugarFlag) {
    whoNutritionFlags.push(sugarFlag);
  }

  // Saturated Fat Flag
  if (nutrition.saturatedFatG > 4) {
    whoNutritionFlags.push({
      nutrient: 'Saturated Fat',
      flagType: 'HIGH_SATURATED_FAT',
      label: 'High Saturated Fat per 100g',
      valueDeclared: `${nutrition.saturatedFatG} g / 100g`,
      whoBenchmark: 'FoodFactsIndia Heuristic (> 4g/100g); WHO Context: < 10% total daily energy intake',
      severity: 'WARNING',
      citation: 'WHO Saturated Fatty Acid Intake Guidelines (2023)'
    });
  }

  // Trans Fat Flag
  if (nutrition.transFatG > 0) {
    whoNutritionFlags.push({
      nutrient: 'Trans Fat',
      flagType: 'CONTAINS_TRANS_FAT',
      label: 'Contains Industrially Produced Trans Fat',
      valueDeclared: `${nutrition.transFatG} g / 100g`,
      whoBenchmark: '0 g / 100g (WHO REPLACE Goal: Eliminate Trans Fat, < 1% energy)',
      severity: 'CRITICAL',
      citation: 'WHO REPLACE Action Package to Eliminate Industrially Produced Trans Fat (2018)'
    });
  }
  if (nutrition.fiberG < 3) {
    whoNutritionFlags.push({
      nutrient: 'Dietary Fibre',
      flagType: 'LOW_FIBER',
      label: 'Low Dietary Fibre',
      valueDeclared: `${nutrition.fiberG} g / 100g`,
      whoBenchmark: '> 3 g / 100g (Target: 25g - 30g daily)',
      severity: 'INFO',
      citation: 'WHO Carbohydrate Intake Guidelines for Adults and Children (2023)'
    });
  }

  // 2. Compute Label Warning Cards & Ban Alerts
  const labelWarnings: any[] = [];
  // Concatenate top-level ingredients text, all tokenized raw ingredient lines, and additive codes for 100% complete text coverage
  const allTextUpper = [
    p.ingredients_text || '',
    ...rawIngredientsList.map(i => i.rawName),
    ...additiveCodes
  ].join(' ').toUpperCase();

  // Southampton Warning (E102, E104, E110, E122, E124, E129)
  const southamptonMatches = ['E102', '102', 'E104', '104', 'E110', '110', 'E122', '122', 'E124', '124', 'E129', '129'].filter(code => allTextUpper.includes(code));
  if (southamptonMatches.length > 0) {
    labelWarnings.push({
      id: 'warn_southampton',
      title: 'UK/EU Mandatory Activity & Attention Warning',
      type: 'SOUTHAMPTON_COLOUR',
      appliedAdditives: southamptonMatches,
      warningText: 'May have an adverse effect on activity and attention in children.',
      jurisdiction: 'United Kingdom (FSA) & European Union (EFSA)',
      authorityRef: 'UK Regulation (EC) No 1333/2008 Annex V'
    });
  }

  // Azorubine / Carmoisine US & Japan Ban (E122 / INS 122)
  if (allTextUpper.includes('E122') || allTextUpper.includes('122') || allTextUpper.includes('AZORUBINE') || allTextUpper.includes('CARMOISINE')) {
    labelWarnings.push({
      id: 'warn_e122_ban',
      title: 'US FDA & Japan Prohibited Synthetic Color (Azorubine / Carmoisine)',
      type: 'FDA_REVOCATION',
      appliedAdditives: ['E122 / INS 122 (Azorubine / Carmoisine)'],
      warningText: 'Azorubine (Carmoisine) is not authorized for food use in the United States by the FDA and is prohibited in Japan due to toxicological concerns.',
      jurisdiction: 'United States (FDA) & Japan (MHLW)',
      authorityRef: '21 CFR Part 74 / Japan Food Sanitation Act Approved List'
    });
  }

  // Titanium Dioxide EU Ban (E171)
  if (allTextUpper.includes('E171') || allTextUpper.includes('171') || allTextUpper.includes('TITANIUM DIOXIDE')) {
    labelWarnings.push({
      id: 'warn_e171_ban',
      title: 'EU Authorisation Revoked (Titanium Dioxide)',
      type: 'EU_BAN',
      appliedAdditives: ['E171 (Titanium Dioxide)'],
      warningText: 'Titanium dioxide is no longer authorised as a food additive in the EU due to genotoxicity concerns.',
      jurisdiction: 'European Union (EFSA)',
      authorityRef: 'EFSA Panel Scientific Opinion (2021) / Regulation (EU) 2022/617'
    });
  }

  // FD&C Red No. 3 FDA Revocation (E127)
  if (allTextUpper.includes('E127') || allTextUpper.includes('127') || allTextUpper.includes('ERYTHROSINE') || allTextUpper.includes('RED 3')) {
    labelWarnings.push({
      id: 'warn_e127_fda',
      title: 'US FDA Food Authorisation Revoked',
      type: 'FDA_REVOCATION',
      appliedAdditives: ['FD&C Red No. 3 (E127 / Erythrosine)'],
      warningText: 'FD&C Red No. 3 authorisation revoked for food and ingested drugs in the United States.',
      jurisdiction: 'United States (FDA)',
      authorityRef: 'US FDA 21 CFR § 74.303 / Federal Register Notice 2024'
    });
  }

  // Aspartame Phenylalanine Warning (E951)
  if (allTextUpper.includes('E951') || allTextUpper.includes('951') || allTextUpper.includes('ASPARTAME')) {
    labelWarnings.push({
      id: 'warn_phenylalanine',
      title: 'Phenylalanine Sensitivity Warning',
      type: 'PHENYLALANINE_WARNING',
      appliedAdditives: ['E951 (Aspartame)'],
      warningText: 'PHENYLKETONURICS: CONTAINS PHENYLALANINE.',
      jurisdiction: 'India (FSSAI), US (FDA), EU (EFSA)',
      authorityRef: 'FSSAI Food Safety and Standards (Labelling) Regulations'
    });
  }

  // FSSAI Category-Specific Limits Warning Cards (from fssai_category_limits table)
  if (dbCatLimits && dbCatLimits.length > 0) {
    (dbCatLimits as any[]).forEach((limit: any) => {
      const insNorm = limit.additive_code.replace(/^0+/, '').toLowerCase();
      const hasAdditive =
        additiveCodes.some(c => c.toLowerCase().includes(insNorm)) ||
        allTextUpper.includes(`INS ${limit.additive_code.toUpperCase()}`) ||
        allTextUpper.includes(`E${limit.additive_code.toUpperCase()}`) ||
        allTextUpper.includes(` ${limit.additive_code.toUpperCase()}`);

      if (hasAdditive) {
        if (limit.status === 'BANNED') {
          labelWarnings.push({
            id: `warn_fssai_cat_${limit.category_code}_${limit.additive_code}`,
            title: `FSSAI Banned in ${limit.category_name}`,
            type: 'EU_BAN',
            appliedAdditives: [`INS ${limit.additive_code}`],
            warningText: limit.restriction_details || `Additive INS ${limit.additive_code} is banned in the ${limit.category_name} category by FSSAI.`,
            jurisdiction: 'India (FSSAI)',
            authorityRef: limit.regulation_ref
          });
        } else if (limit.status === 'RESTRICTED' && limit.max_limit_mg_kg != null) {
          labelWarnings.push({
            id: `warn_fssai_cat_${limit.category_code}_${limit.additive_code}`,
            title: `FSSAI Category Limit: Max ${limit.max_limit_mg_kg} mg/kg`,
            type: 'OTHER',
            appliedAdditives: [`INS ${limit.additive_code}`],
            warningText: `In the ${limit.category_name} category, INS ${limit.additive_code} is restricted to a maximum of ${limit.max_limit_mg_kg} mg/kg under ${limit.regulation_ref}.`,
            jurisdiction: 'India (FSSAI)',
            authorityRef: limit.regulation_ref
          });
        }
      }
    });
  }

  // Derive Banned / Restricted counts per country across 6 jurisdictions
  const inRules = rulebookData.filter(r => r.jurisdiction === 'IN');
  const euRules = rulebookData.filter(r => r.jurisdiction === 'EU');
  const ukRules = rulebookData.filter(r => r.jurisdiction === 'UK');
  const usRules = rulebookData.filter(r => r.jurisdiction === 'US');
  const jpRules = rulebookData.filter(r => r.jurisdiction === 'JP');
  const codexRules = rulebookData.filter(r => r.jurisdiction === 'CODEX');

  const globalRegulatoryOverview = [
    {
      countryCode: 'IN' as const,
      countryName: 'India (FSSAI)',
      flagEmoji: '🇮🇳',
      bannedCount: inRules.filter(r => r.status === 'banned').length,
      restrictedCount: inRules.filter(r => r.status === 'restricted' || r.status === 'requires_warning').length,
      approvedCount: Math.max(1, additiveCodes.length - inRules.filter(r => r.status !== 'permitted').length)
    },
    {
      countryCode: 'EU' as const,
      countryName: 'European Union (EFSA)',
      flagEmoji: '🇪🇺',
      bannedCount: euRules.filter(r => r.status === 'banned').length + (allTextUpper.includes('E171') ? 1 : 0),
      restrictedCount: euRules.filter(r => r.status === 'restricted' || r.status === 'requires_warning').length,
      approvedCount: Math.max(1, additiveCodes.length - euRules.filter(r => r.status !== 'permitted').length)
    },
    {
      countryCode: 'UK' as const,
      countryName: 'United Kingdom (FSA)',
      flagEmoji: '🇬🇧',
      bannedCount: ukRules.filter(r => r.status === 'banned').length,
      restrictedCount: ukRules.filter(r => r.status === 'restricted' || r.status === 'requires_warning').length + (southamptonMatches.length > 0 ? 1 : 0),
      approvedCount: Math.max(1, additiveCodes.length - ukRules.filter(r => r.status !== 'permitted').length)
    },
    {
      countryCode: 'US' as const,
      countryName: 'United States (FDA)',
      flagEmoji: '🇺🇸',
      bannedCount: usRules.filter(r => r.status === 'banned').length + (allTextUpper.includes('E127') ? 1 : 0),
      restrictedCount: usRules.filter(r => r.status === 'restricted' || r.status === 'requires_warning').length,
      approvedCount: Math.max(1, additiveCodes.length - usRules.filter(r => r.status !== 'permitted').length)
    },
    {
      countryCode: 'JP' as const,
      countryName: 'Japan (MHLW)',
      flagEmoji: '🇯🇵',
      bannedCount: jpRules.filter(r => r.status === 'banned').length,
      restrictedCount: jpRules.filter(r => r.status === 'restricted' || r.status === 'requires_warning').length,
      approvedCount: Math.max(1, additiveCodes.length - jpRules.filter(r => r.status !== 'permitted').length)
    },
    {
      countryCode: 'CODEX' as const,
      countryName: 'Codex Alimentarius (FAO/WHO)',
      flagEmoji: '🇺🇳',
      bannedCount: codexRules.filter(r => r.status === 'banned').length,
      restrictedCount: codexRules.filter(r => r.status === 'restricted' || r.status === 'requires_warning').length,
      approvedCount: Math.max(1, additiveCodes.length - codexRules.filter(r => r.status !== 'permitted').length)
    }
  ];

  const report: TransparencyReport = {
    productId: `prod_live_${barcode}`,
    slug: p.slug || undefined,
    productName: toEnglishOnly(p.product_name || ''),
    brand: toEnglishOnly(p.brands || ''),
    manufacturer: toEnglishOnly(p.manufacturer || p.brands || ''),
    category: toEnglishOnly(p.categories || ''),
    barcode,
    imageUrl: p.image_front_url || undefined,
    imageFrontUrl: p.image_front_url || undefined,
    imageIngredientsUrl: p.image_ingredients_url || undefined,
    imageNutritionUrl: p.image_nutrition_url || undefined,
    packageSize: p.quantity ? toEnglishOnly(String(p.quantity)) : '',
    servingSize: p.serving_size || p.quantity || '100g',
    pageState: isDataIncomplete ? 'insufficient_data' : 'verified_published',
    stateMessage: isDataIncomplete ? 'We do not have enough verified package data to analyze this product yet.' : 'Verified package label report.',
    deterministicScore: isDataIncomplete ? 0 : scoreResult.finalScore,
    scoreBreakdown: isDataIncomplete ? [] : scoreResult.scoreBreakdown,
    isScoreWithheld: isDataIncomplete,
    scoreWithheldReason: isDataIncomplete 
      ? 'Insufficient source data: Ingredients or nutrition facts are unparsed or pending manufacturer verification.'
      : undefined,
    internationalRatings: (() => {
      if (isDataIncomplete) return undefined;
      // Call the 5-layer production rating gate before issuing any international ratings.
      const { isEligibleForRatings } = evaluateRatingGate(
        0.98, // live DB products sourced from verified FSSAI/OFF data
        nutrition,
        'DATABASE',
        p.categories || ''
      );
      if (!isEligibleForRatings) return undefined;
      return calculateInternationalRatings(
        nutrition,
        p.categories || '',
        ingredientsList.map(i => i.ingredient),
        p.serving_size || p.quantity || '100g'
      );
    })(),
    executiveSummary: {
      grade: isDataIncomplete ? 'F' : scoreResult.grade,
      verdictTitle: isDataIncomplete ? 'Verification Pending' : `${p.product_name} - ${scoreResult.grade} Quality Rating`,
      keyTakeaways: isDataIncomplete ? [] : [
        `Contains ${additiveCodes.length} declared additive E-numbers (${additiveCodes.join(', ') || 'None'}).`,
        `Nutrient Profile: ${nutrition.totalSugarG}g Sugar, ${nutrition.sodiumMg}mg Sodium per 100g.`,
        p.nova_group != null ? `NOVA Classification: Group ${p.nova_group} food item.` : `NOVA Classification: Unclassified.`
      ],
      riskSummaryText: isDataIncomplete ? 'Package evidence pending verification.' : `Live verified dataset analysis from Supabase database for ${p.product_name}.`,
      processingNovaClass: isDataIncomplete ? undefined : (p.nova_group != null ? Number(p.nova_group) : undefined)
    },
    ingredientsList: isDataIncomplete ? [] : ingredientsList,
    nutrition,
    whoNutritionFlags: isDataIncomplete ? undefined : whoNutritionFlags,
    labelWarnings: isDataIncomplete ? undefined : labelWarnings,
    globalRegulatoryOverview,
    evidenceConfidence: {
      confidenceScore: isDataIncomplete ? 30 : 
        (p.energy_100g != null && p.fat_100g != null && p.sugars_100g != null && ingredientsList.length > 0 ? 90 : 60),
      peerReviewedStudiesCount: ingredientsList.reduce((acc, i) => acc + (i.ingredient.citations?.length || 0), 0),
      regulatoryBodiesCount: globalRegulatoryOverview.filter(r => (r.bannedCount || 0) > 0 || (r.restrictedCount || 0) > 0).length,
      lastUpdated: new Date().toISOString().split('T')[0],
      verificationStatus: isDataIncomplete ? 'pending_verification' : 'database_indexed'
    }
  };

  reportCache.set(barcode, report);
  return report;
}

export function calculateWHOSugarFlag(nutrition: { totalSugarG?: number | null; calories?: number | null }) {
  const { totalSugarG, calories } = nutrition;

  if (totalSugarG == null || totalSugarG < 0) {
    return null;
  }

  // Edge case: Zero or missing calories -> Fall back to per-100g heuristic (>10g/100g)
  if (calories == null || calories <= 0) {
    const isHigh = totalSugarG > 10;
    if (!isHigh) return null;
    return {
      nutrient: 'Free Sugars',
      flagType: 'HIGH_FREE_SUGAR',
      label: 'Estimated High Free Sugars (FoodFactsIndia Heuristic: >10g/100g)',
      valueDeclared: `${totalSugarG} g / 100g`,
      whoBenchmark: 'FoodFactsIndia Heuristic (>10g/100g); WHO Context: < 10% daily energy intake (Energy data unavailable)',
      severity: 'CRITICAL',
      citation: 'WHO Guideline: Sugars Intake for Adults and Children (2015)'
    };
  }

  // Energy calculation: Sugar (g) * 4 kcal/g
  const sugarCalories = totalSugarG * 4;
  const sugarEnergyPercent = round1((sugarCalories / calories) * 100);

  // WHO Threshold: > 10% of daily total energy
  if (sugarEnergyPercent > 10.0) {
    return {
      nutrient: 'Free Sugars',
      flagType: 'HIGH_FREE_SUGAR',
      label: `Estimated High Free Sugars (${sugarEnergyPercent}% of Total Calories)`,
      valueDeclared: `${totalSugarG} g / 100g (${sugarEnergyPercent}% energy)`,
      whoBenchmark: '< 10% total daily energy intake (WHO Recommended Target)',
      severity: 'CRITICAL',
      citation: 'WHO Guideline: Sugars Intake for Adults and Children (2015)'
    };
  }

  return null;
}



/**
 * V2 Discriminated Variant Supplier
 * Returns exact ProductPageResponse discriminated union preventing data leakages.
 */
export async function getProductPage(barcode: string): Promise<import('../types/productPageResponse').ProductPageResponse> {
  const clean = barcode.trim();
  const preseeded = PRESEEDED_PRODUCTS.find(p => p.barcode === clean);
  const report = preseeded || await fetchOpenFoodFactsProduct(clean);

  if (!report) {
    const dummyIdentity: import('../types/productPageResponse').ProductIdentity = {
      productId: `prod_stub_${clean}`,
      barcode: clean,
      productName: 'Unverified Product',
      brand: 'Unverified Brand',
      category: 'Packaged Food',
      packageSize: 'Unknown',
      servingSize: '100g'
    };
    return {
      pageState: 'insufficient_data',
      product: dummyIdentity,
      stub: { message: 'No package data available for this GTIN.' }
    };
  }

  const productIdentity: import('../types/productPageResponse').ProductIdentity = {
    productId: report.productId,
    barcode: report.barcode,
    productName: report.productName,
    brand: report.brand,
    manufacturer: report.manufacturer,
    category: report.category,
    packageSize: report.packageSize,
    servingSize: report.servingSize,
    imageUrl: report.imageUrl
  };

  if (!report.pageState || report.pageState === 'verified_published' && !report.isScoreWithheld) {
    return {
      pageState: 'verified_published',
      product: productIdentity,
      verifiedReport: report
    };
  }

  if (report.pageState === 'processing') {
    return {
      pageState: 'processing',
      product: productIdentity,
      progress: { percent: 45, step: 'OCR & Ingredient Token Extraction' }
    };
  }

  if (report.pageState === 'needs_review') {
    return {
      pageState: 'needs_review',
      product: productIdentity,
      stub: { message: report.scoreWithheldReason || 'Data extracted but awaiting quality review.' },
      reviewReasons: [report.scoreWithheldReason || 'Data validation flag triggered']
    };
  }

  if (report.pageState === 'awaiting_images') {
    return {
      pageState: 'awaiting_images',
      product: productIdentity,
      stub: { message: 'No verified package evidence available yet.' }
    };
  }

  return {
    pageState: 'insufficient_data',
    product: productIdentity,
    stub: { message: report.scoreWithheldReason || 'We need more complete package data before analysis.' },
    reviewReasons: report.scoreWithheldReason ? [report.scoreWithheldReason] : undefined
  };
}

