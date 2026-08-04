import { NutritionFacts } from '../../types';

export interface NormalizedProductData {
  productName: string;
  brand: string;
  rawIngredientsText: string;
  structuredIngredients?: any[];
  rawNutriments: Record<string, any>;
  normalizedNutrition: NutritionFacts;
  conversionRuleApplied: string;
}

export class OpenFoodFactsAdapter {
  private static BASE_URL = 'https://world.openfoodfacts.org/api/v2/product';

  public static async fetchByBarcode(barcode: string): Promise<NormalizedProductData | null> {
    try {
      const res = await fetch(`${this.BASE_URL}/${barcode}.json?fields=code,product_name,brands,ingredients_text,ingredients,nutriments,serving_size`);
      if (!res.ok) return null;

      const data = await res.json();
      if (!data || data.status !== 1 || !data.product) return null;

      const p = data.product;
      const nut = p.nutriments || {};

      // Traceable Sodium Normalization Rule
      let sodiumMg = 0;
      let rule = 'NO_SODIUM_FOUND';

      if (nut.sodium_100g !== undefined) {
        const unit = (nut.sodium_unit || 'g').toLowerCase();
        if (unit === 'g') {
          sodiumMg = nut.sodium_100g * 1000;
          rule = 'SODIUM_100G_GRAMS_TO_MG';
        } else {
          sodiumMg = nut.sodium_100g;
          rule = 'SODIUM_100G_DIRECT_MG';
        }
      } else if (nut.salt_100g !== undefined) {
        sodiumMg = (nut.salt_100g / 2.54) * 1000;
        rule = 'SALT_100G_CONVERTED_VIA_DIV_2.54';
      }

      return {
        productName: p.product_name || 'Unknown Product',
        brand: p.brands || 'Generic',
        rawIngredientsText: p.ingredients_text || '',
        structuredIngredients: Array.isArray(p.ingredients) ? p.ingredients : undefined,
        rawNutriments: nut,
        normalizedNutrition: {
          calories: nut['energy-kcal_100g'] || nut['energy-kcal'] || 0,
          servingSize: p.serving_size || '100g',
          totalFatG: nut.fat_100g || 0,
          saturatedFatG: nut['saturated-fat_100g'] || 0,
          transFatG: nut['trans-fat_100g'] || 0,
          sodiumMg: Math.round(sodiumMg),
          totalCarbsG: nut.carbohydrates_100g || 0,
          fiberG: nut.fiber_100g || 0,
          totalSugarG: nut.sugars_100g || 0,
          addedSugarG: nut['added-sugars_100g'] || nut.sugars_100g || 0,
          proteinG: nut.proteins_100g || 0,
        },
        conversionRuleApplied: rule
      };
    } catch (e) {
      console.error('OpenFoodFactsAdapter fetch exception:', e);
      return null;
    }
  }
}
