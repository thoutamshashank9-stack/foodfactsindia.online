import { TransparencyReport } from '../types';
import { isNonFoodProduct } from './supabaseService';

export interface SearchMatch {
  product: TransparencyReport;
  score: number;
  matchedField: 'barcode' | 'productName' | 'brand' | 'category' | 'ingredient';
}

/**
 * High-performance, highly accurate search utility for TransparencyReport items.
 * Performs multi-field relevance scoring with 0ms local execution.
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

    // 1. Barcode Matching (Highest Priority)
    if (isBarcodeQuery && cleanDigits) {
      if (pBarcode === cleanDigits) {
        score += 1000;
        matchedField = 'barcode';
      } else if (pBarcode.replace(/^0+/, '') === cleanDigits.replace(/^0+/, '')) {
        score += 900;
        matchedField = 'barcode';
      } else if (pBarcode.includes(cleanDigits)) {
        score += 500;
        matchedField = 'barcode';
      }
    }

    // 2. Product Name Matching
    if (pName === q) {
      score += 850;
      if (score < 850) matchedField = 'productName';
    } else if (pName.startsWith(q)) {
      score += 450;
      if (score < 450) matchedField = 'productName';
    } else if (pName.includes(q)) {
      score += 250;
      if (score < 250) matchedField = 'productName';
    }

    // 3. Brand Matching
    if (pBrand === q) {
      score += 350;
      if (score < 350) matchedField = 'brand';
    } else if (pBrand.startsWith(q)) {
      score += 200;
      if (score < 200) matchedField = 'brand';
    } else if (pBrand.includes(q)) {
      score += 120;
      if (score < 120) matchedField = 'brand';
    }

    // 4. Category Matching
    if (pCat === q) {
      score += 150;
      if (score < 150) matchedField = 'category';
    } else if (pCat.includes(q)) {
      score += 60;
      if (score < 60) matchedField = 'category';
    }

    // 5. Ingredient & Additive Matching (INS / E-Codes / Raw Names)
    if (p.ingredientsList && p.ingredientsList.length > 0) {
      for (const item of p.ingredientsList) {
        const raw = (item.rawName || '').toLowerCase();
        const cName = (item.ingredient?.canonicalName || '').toLowerCase();
        const ins = (item.ingredient?.insNumber || '').toLowerCase();
        const eNum = (item.ingredient?.eNumber || '').toLowerCase();

        if (cName === q || raw === q) {
          score += 180;
          matchedField = 'ingredient';
          break;
        }
        if (cName.includes(q) || raw.includes(q)) {
          score += 90;
          matchedField = 'ingredient';
          break;
        }
        if (ins && (ins === q || `ins ${ins}` === q || `ins${ins}` === q || ins.includes(q))) {
          score += 220;
          matchedField = 'ingredient';
          break;
        }
        if (eNum && (eNum === q || `e ${eNum}` === q || `e${eNum}` === q || eNum.includes(q))) {
          score += 220;
          matchedField = 'ingredient';
          break;
        }
      }
    }

    if (score > 0) {
      seenIds.add(p.productId);
      results.push({ product: p, score, matchedField });
    }
  }

  // Sort descending by relevance score
  results.sort((a, b) => b.score - a.score);
  return results.map(r => r.product);
}
