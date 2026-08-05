import { Ingredient, RegulatoryRecord, ResearchCitation } from '../types';
import { INGREDIENT_DATABASE } from '../data/ingredientsDatabase';

export interface CanonicalAdditive {
  id: string;
  insCode?: string;
  eNumber?: string;
  casNumber?: string;
  ciNumber?: string;
  primaryName: string;
  chemicalName?: string;
  category: 'PRESERVATIVE' | 'ARTIFICIAL_COLOR' | 'SWEETENER' | 'EMULSIFIER' | 'FLAVOR_ENHANCER' | 'THICKENER' | 'WHOLE_FOOD' | 'PROCESSING_AID' | 'RAISING_AGENT' | 'OTHER';
  riskLevel: 'HIGH' | 'MEDIUM' | 'LOW' | 'EXCELLENT';
  baseRiskWeight: number;
  cspiRating?: 'AVOID' | 'CAUTION' | 'CUT_BACK' | 'SAFE';
  description: string;
  processingLevel: 'NOVA_1_UNPROCESSED' | 'NOVA_2_PROCESSED_INGREDIENT' | 'NOVA_3_PROCESSED_FOOD' | 'NOVA_4_ULTRA_PROCESSED';
  regulatoryBans: RegulatoryBanRecord[];
  citations: ResearchCitation[];
}

export interface RegulatoryBanRecord {
  jurisdictionCode: 'US' | 'JP' | 'EU' | 'UK' | 'IN' | 'CODEX';
  status: 'BANNED' | 'RESTRICTED' | 'APPROVED';
  scopeCategory: string; // 'ALL', 'BEVERAGES', 'DAIRY', etc.
  maxLimitMgKg?: number | null;
  restrictionDetails?: string;
  regulationRef: string;
  mandatoryWarningText?: string;
}

// Global Decoupled In-Memory Synonym Hash Table for O(1) matching
const synonymLookupMap = new Map<string, CanonicalAdditive>();

/**
 * Pre-tokenization regex splits code clusters (e.g., "INS 102/110/122", "E-122", "INS 122")
 */
export function tokenizeRawLabelText(rawText: string): string[] {
  if (!rawText) return [];
  const lower = rawText.toLowerCase();

  const tokens = new Set<string>();

  // 1. Extract explicit INS/E code clusters: e.g. "ins 102", "e122", "102/110/122"
  const clusterRegex = /(?:ins|e)?\s*([0-9]{3,4}[a-z]?(?:\s*[\/\&,]\s*[0-9]{3,4}[a-z]?)*)/gi;
  let match: RegExpExecArray | null;

  while ((match = clusterRegex.exec(lower)) !== null) {
    if (match[1]) {
      const parts = match[1].split(/[\/\&,]/).map(p => p.trim());
      parts.forEach(p => {
        const cleanDigits = p.replace(/^(ins|e)/i, '').trim();
        if (cleanDigits && !['100', '200', '500g', '100g'].includes(cleanDigits)) {
          tokens.add(cleanDigits);
          tokens.add(`ins ${cleanDigits}`);
          tokens.add(`e${cleanDigits}`);
        }
      });
    }
  }

  // 2. Add chemical / commercial words
  const words = lower.split(/[\s,();:.\/]+/).map(w => w.trim()).filter(w => w.length > 2);
  words.forEach(w => tokens.add(w));

  return Array.from(tokens);
}

/**
 * Builds the decoupled in-memory database index from master records and taxonomy mappings.
 */
function initializeDecoupledIndex() {
  if (synonymLookupMap.size > 0) return;

  INGREDIENT_DATABASE.forEach(ing => {
    const canonical: CanonicalAdditive = {
      id: ing.id,
      insCode: ing.insNumber,
      eNumber: ing.eNumber,
      casNumber: ing.id === 'ing_e122' ? '3567-69-9' : (ing.id === 'ing_e102' ? '1934-21-0' : undefined),
      ciNumber: ing.id === 'ing_e122' ? 'CI 14720' : (ing.id === 'ing_e102' ? 'CI 19140' : undefined),
      primaryName: ing.canonicalName,
      chemicalName: ing.scientificName,
      category: ing.category,
      riskLevel: ing.riskLevel,
      baseRiskWeight: ing.baseRiskWeight,
      cspiRating: ing.riskLevel === 'HIGH' ? 'AVOID' : (ing.riskLevel === 'MEDIUM' ? 'CAUTION' : 'SAFE'),
      description: ing.description,
      processingLevel: ing.processingLevel,
      regulatoryBans: (ing.regulatoryRecords || []).map(r => ({
        jurisdictionCode: r.countryCode,
        status: r.status,
        scopeCategory: 'ALL',
        restrictionDetails: r.restrictionDetails,
        regulationRef: r.regulationRef
      })),
      citations: ing.citations || []
    };

    // Register all synonyms in the clean lookup map
    const synonymsToRegister = new Set<string>([
      ing.canonicalName.toLowerCase(),
      ...(ing.synonyms || []).map(s => s.toLowerCase()),
      ing.insNumber ? ing.insNumber.toLowerCase() : '',
      ing.insNumber ? `ins ${ing.insNumber.toLowerCase()}` : '',
      ing.insNumber ? `ins${ing.insNumber.toLowerCase()}` : '',
      ing.eNumber ? ing.eNumber.toLowerCase() : '',
      ing.eNumber ? `e-${ing.eNumber.toLowerCase().replace('e', '')}` : ''
    ]);

    synonymsToRegister.forEach(syn => {
      if (syn && syn.length > 0) {
        synonymLookupMap.set(syn, canonical);
      }
    });
  });
}

/**
 * Performs set-based array matching across raw tokens in sub-millisecond O(1) complexity.
 * Returns unique matched canonical additives, sorted by risk severity (HIGH > MEDIUM > LOW).
 */
export function matchDecoupledAdditives(rawText: string): CanonicalAdditive[] {
  initializeDecoupledIndex();
  const tokens = tokenizeRawLabelText(rawText);
  const matchedSet = new Map<string, CanonicalAdditive>();

  for (const token of tokens) {
    const match = synonymLookupMap.get(token);
    if (match) {
      matchedSet.set(match.id, match);
    }
  }

  const results = Array.from(matchedSet.values());
  results.sort((a, b) => {
    const rank = (r: string) => (r === 'HIGH' ? 3 : r === 'MEDIUM' ? 2 : 1);
    return rank(b.riskLevel) - rank(a.riskLevel);
  });

  return results;
}
