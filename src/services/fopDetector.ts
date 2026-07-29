import { NutritionFacts, Ingredient } from '../types';

export interface FopWarningLabel {
  type: 'EXCESS_SUGAR' | 'EXCESS_SODIUM' | 'EXCESS_SAT_FAT' | 'CONTAINS_TRANS_FAT' | 'CONTAINS_SWEETENERS' | 'CONTAINS_CHILD_DYES';
  headline: string;
  bodyText: string;
  badgeStyle: 'OCTAGON_BLACK' | 'WARNING_AMBER' | 'ALERT_RED';
  authoritySource: string;
}

/**
 * Detects Front-of-Pack (FoP) octagonal warning labels according to WHO, FSSAI, Chile & Mexico standards.
 */
export function detectFopWarningLabels(
  nutrition: NutritionFacts,
  ingredients: Ingredient[]
): FopWarningLabel[] {
  const warnings: FopWarningLabel[] = [];

  // 1. EXCESS SUGAR (Added Sugar > 5g per 100g)
  if (nutrition.addedSugarG > 5) {
    warnings.push({
      type: 'EXCESS_SUGAR',
      headline: 'EXCESS ADDED SUGAR',
      bodyText: `Contains ${nutrition.addedSugarG}g added sugar per 100g (exceeds WHO 5g daily limit).`,
      badgeStyle: 'OCTAGON_BLACK',
      authoritySource: 'WHO & Mexico NOM-051 Standard'
    });
  }

  // 2. EXCESS SODIUM (Sodium > 300mg per 100g)
  if (nutrition.sodiumMg > 300) {
    warnings.push({
      type: 'EXCESS_SODIUM',
      headline: 'HIGH SODIUM DENSITY',
      bodyText: `Contains ${nutrition.sodiumMg}mg sodium per 100g (exceeds FSSAI 300mg threshold).`,
      badgeStyle: 'OCTAGON_BLACK',
      authoritySource: 'FSSAI Front-of-Pack Regulations & Chile Law 20.606'
    });
  }

  // 3. EXCESS SATURATED FAT (Saturated Fat > 3g per 100g)
  if (nutrition.saturatedFatG > 3) {
    warnings.push({
      type: 'EXCESS_SAT_FAT',
      headline: 'HIGH SATURATED FAT',
      bodyText: `Contains ${nutrition.saturatedFatG}g saturated fat per 100g.`,
      badgeStyle: 'WARNING_AMBER',
      authoritySource: 'ICMR-NIN Dietary Guidelines'
    });
  }

  // 4. CONTAINS TRANS FATS
  if (nutrition.transFatG > 0) {
    warnings.push({
      type: 'CONTAINS_TRANS_FAT',
      headline: 'CONTAINS TRANS FATS',
      bodyText: `Formulated with ${nutrition.transFatG}g trans fatty acids.`,
      badgeStyle: 'ALERT_RED',
      authoritySource: 'WHO REPLACE Strategy'
    });
  }

  // 5. CONTAINS SYNTHETIC SWEETENERS
  const hasSweetener = ingredients.some((i) => i.category === 'SWEETENER');
  if (hasSweetener) {
    warnings.push({
      type: 'CONTAINS_SWEETENERS',
      headline: 'CONTAINS ARTIFICIAL SWEETENERS',
      bodyText: `Contains non-nutritive artificial sweeteners. Not recommended for children.`,
      badgeStyle: 'WARNING_AMBER',
      authoritySource: 'FSSAI Labelling Standard 2.4.5'
    });
  }

  // 6. CONTAINS SOUTHAMPTON CHILD DYES
  const hasChildDye = ingredients.some(
    (i) => i.canonicalName.includes('Tartrazine') || i.insNumber === '102' || i.eNumber === 'E102'
  );
  if (hasChildDye) {
    warnings.push({
      type: 'CONTAINS_CHILD_DYES',
      headline: 'CHILD ATTENTION WARNING DYE',
      bodyText: `Contains synthetic dyes linked to hyperactivity and attention deficits in children.`,
      badgeStyle: 'ALERT_RED',
      authoritySource: 'EU Regulation 1333/2008 Annex V'
    });
  }

  return warnings;
}
