const OFF_API = 'https://world.openfoodfacts.org';

export interface OFFProductImageResult {
  barcode: string;
  name: string;
  brand?: string;
  imageSmall: string | null;
  imageMedium: string | null;
  imageFull: string | null;
}

/**
 * Construct Open Food Facts optimized image URL directly from barcode.
 * Uses OFF's built-in image resizing API (100, 200, 400, or full).
 * Barcode is formatted into 3/3/3/remainder path structure.
 */
export function getOptimizedOFFImageUrl(
  barcode: string,
  size: 100 | 200 | 400 | 'full' = 200,
  lang: string = 'en'
): string | null {
  if (!barcode || typeof barcode !== 'string') return null;
  const clean = barcode.trim();
  if (clean.length < 8) return null;

  // Format barcode into 3, 3, 3, and remainder chunks
  const codeStr = clean.length < 13 ? clean.padStart(13, '0') : clean;
  const part1 = codeStr.substring(0, 3);
  const part2 = codeStr.substring(3, 6);
  const part3 = codeStr.substring(6, 9);
  const part4 = codeStr.substring(9);

  const sizeSuffix = size === 'full' ? '' : `.${size}`;
  return `https://images.openfoodfacts.org/images/products/${part1}/${part2}/${part3}/${part4}/front_${lang}${sizeSuffix}.jpg`;
}

/** Fetch one product by barcode → returns ready-to-use image URLs */
export async function getProductByBarcode(barcode: string): Promise<OFFProductImageResult | null> {
  try {
    const cleanBarcode = barcode.trim();
    if (!cleanBarcode) return null;

    // Use optimized direct OFF CDN formula first
    const directSmall = getOptimizedOFFImageUrl(cleanBarcode, 200);
    const directMedium = getOptimizedOFFImageUrl(cleanBarcode, 400);

    const res = await fetch(`${OFF_API}/api/v2/product/${encodeURIComponent(cleanBarcode)}.json?fields=code,product_name,brands,image_front_small_url,image_front_url,image_url`);
    if (!res.ok) {
      return {
        barcode: cleanBarcode,
        name: '',
        imageSmall: directSmall,
        imageMedium: directMedium,
        imageFull: null,
      };
    }
    const json = await res.json();
    if (json.status !== 1 || !json.product) {
      return {
        barcode: cleanBarcode,
        name: '',
        imageSmall: directSmall,
        imageMedium: directMedium,
        imageFull: null,
      };
    }

    const p = json.product;
    return {
      barcode: p.code || cleanBarcode,
      name: p.product_name || '',
      brand: p.brands || '',
      imageSmall: p.image_front_small_url || directSmall,
      imageMedium: p.image_front_url || directMedium,
      imageFull: p.image_url || null,
    };
  } catch (err) {
    console.error('OFF Image Fetch Error:', err);
    return null;
  }
}

/** Search by product name → returns list with images */
export async function searchByName(query: string, limit: number = 24): Promise<Partial<OFFProductImageResult>[]> {
  try {
    if (!query.trim()) return [];
    const url =
      `${OFF_API}/cgi/search.pl?search_terms=${encodeURIComponent(query)}` +
      `&search_simple=1&action=process&json=1&page_size=${limit}` +
      `&fields=code,product_name,brands,image_front_small_url,image_front_url`;
    const res = await fetch(url);
    if (!res.ok) return [];
    const json = await res.json();
    return (json.products || []).map((p: any) => ({
      barcode: p.code,
      name: p.product_name || '',
      brand: p.brands || '',
      imageSmall: p.image_front_small_url || getOptimizedOFFImageUrl(p.code, 200),
      imageMedium: p.image_front_url || getOptimizedOFFImageUrl(p.code, 400),
    }));
  } catch (err) {
    console.error('OFF Search Error:', err);
    return [];
  }
}
