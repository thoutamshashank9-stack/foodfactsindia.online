import { TransparencyReport } from '../types';
import { isNonFoodProduct } from './supabaseService';

export interface SearchMatch {
  product: TransparencyReport;
  score: number;
  matchedField: 'barcode' | 'productName' | 'brand' | 'category' | 'ingredient';
  isCompleteDetails: boolean;
}

/**
 * Fast, highly accurate multi-field search engine for TransparencyReport items.
 * Ranks products with complete ingredient declarations, verified quality scores,
 * and high data completeness FIRST in search results.
 */
export function searchTransparencyReports(
  products: TransparencyReport[],
  query: string
): TransparencyReport[] {
  if (!query || !query.trim()) return [];

  const rawQ = query.trim();
  const q = rawQ.toLowerCase();
  const cleanDigits = rawQ.replace(/[^0-9]/g, '');
  const isBarcodeQuery = cleanDigits.length >= 3;

  const results: SearchMatch[] = [];
  const seenIds = new Set<string>();

  for (const p of products) {
    if (!p || seenIds.has(p.productId)) continue;
    if (isNonFoodProduct(p)) continue;

    let score = 0;
    let matchedField: SearchMatch['matchedField'] = 'productName';

    const pBarcode = (p.barcode || '').toLowerCase();
    const pName = (p.productName || '').toLowerCase();
    const pBrand = (p.brand || '').toLowerCase();
    const pCat = (p.category || '').toLowerCase();
    const hasIngredients = Boolean(
      (p.ingredientsList && p.ingredientsList.length > 0) || 
      (p.rawIngredientsText && p.rawIngredientsText.trim().length > 5)
    );
    const hasImage = Boolean(p.imageUrl || p.imageFrontUrl);
    const isVerified = (p as any).seoStatus === 'INDEX' || (p as any).seoQualityScore >= 80 || (p as any).verificationStatus === 'VERIFIED';
    const isComplete = hasIngredients && hasImage;

    // 1. Barcode Matching (Highest Priority for barcode searches)
    if (isBarcodeQuery && cleanDigits) {
      if (pBarcode === cleanDigits) {
        score += 2000;
        matchedField = 'barcode';
      } else if (pBarcode.replace(/^0+/, '') === cleanDigits.replace(/^0+/, '')) {
        score += 1800;
        matchedField = 'barcode';
      } else if (pBarcode.includes(cleanDigits)) {
        score += 1000;
        matchedField = 'barcode';
      }
    }

    // 2. Product Name Matching
    if (pName === q) {
      score += 1200;
      if (score < 1200) matchedField = 'productName';
    } else if (pName.startsWith(q)) {
      score += 800;
      if (score < 800) matchedField = 'productName';
    } else if (pName.includes(q)) {
      score += 400;
      if (score < 400) matchedField = 'productName';
    } else {
      // Word-level matching for multi-word queries (e.g. "maggi noodles", "amul milk")
      const words = q.split(/\s+/).filter(w => w.length > 1);
      if (words.length > 1) {
        let matchedWordsCount = 0;
        for (const word of words) {
          if (pName.includes(word)) matchedWordsCount++;
        }
        if (matchedWordsCount > 0) {
          score += matchedWordsCount * 250;
        }
      }
    }

    // 3. Brand Matching
    if (pBrand === q) {
      score += 500;
      if (score < 500) matchedField = 'brand';
    } else if (pBrand.startsWith(q)) {
      score += 350;
      if (score < 350) matchedField = 'brand';
    } else if (pBrand.includes(q)) {
      score += 200;
      if (score < 200) matchedField = 'brand';
    }

    // 4. Category Matching
    if (pCat === q) {
      score += 300;
      if (score < 300) matchedField = 'category';
    } else if (pCat.includes(q)) {
      score += 150;
      if (score < 150) matchedField = 'category';
    }

    // 5. Ingredient & Additive Matching (INS / E-Codes / Raw Names)
    if (p.ingredientsList && p.ingredientsList.length > 0) {
      for (const item of p.ingredientsList) {
        const raw = (item.rawName || '').toLowerCase();
        const cName = (item.ingredient?.canonicalName || '').toLowerCase();
        const ins = (item.ingredient?.insNumber || '').toLowerCase();
        const eNum = (item.ingredient?.eNumber || '').toLowerCase();

        if (cName === q || raw === q) {
          score += 300;
          matchedField = 'ingredient';
          break;
        }
        if (cName.includes(q) || raw.includes(q)) {
          score += 150;
          matchedField = 'ingredient';
          break;
        }
        if (ins && (ins === q || `ins ${ins}` === q || `ins${ins}` === q || ins.includes(q))) {
          score += 350;
          matchedField = 'ingredient';
          break;
        }
        if (eNum && (eNum === q || `e ${eNum}` === q || `e${eNum}` === q || eNum.includes(q))) {
          score += 350;
          matchedField = 'ingredient';
          break;
        }
      }
    }

    // 🌟 6. DATA COMPLETENESS BOOST (Developer Requirement: Full Details First)
    // Products with complete ingredient declarations, images, and verified quality scores GET A MAJOR BOOST
    if (score > 0) {
      if (hasIngredients) {
        score += 600; // Strongest boost for full ingredient lists
      }
      if (isVerified) {
        score += 400; // Quality score >= 80 boost
      }
      if (hasImage) {
        score += 200; // Image present boost
      }
      if (pBrand && pBrand !== 'unknown' && pBrand !== 'unspecified') {
        score += 100; // Brand present boost
      }

      seenIds.add(p.productId);
      results.push({ product: p, score, matchedField, isCompleteDetails: isComplete });
    }
  }

  // Sort descending by relevance score (so products with full details rank FIRST)
  results.sort((a, b) => b.score - a.score);
  return results.map(r => r.product);
}
