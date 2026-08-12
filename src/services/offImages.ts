const OFF_API = 'https://world.openfoodfacts.org';

export interface OFFProductImageResult {
  barcode: string;
  name: string;
  brand?: string;
  imageSmall: string | null;
  imageMedium: string | null;
  imageFull: string | null;
}

/** Fetch one product by barcode → returns ready-to-use image URLs */
export async function getProductByBarcode(barcode: string): Promise<OFFProductImageResult | null> {
  try {
    const cleanBarcode = barcode.trim();
    if (!cleanBarcode) return null;
    const res = await fetch(`${OFF_API}/api/v2/product/${encodeURIComponent(cleanBarcode)}.json`);
    if (!res.ok) return null;
    const json = await res.json();
    if (json.status !== 1 || !json.product) return null;

    const p = json.product;
    return {
      barcode: p.code || cleanBarcode,
      name: p.product_name || '',
      brand: p.brands || '',
      imageSmall: p.image_front_small_url || null,
      imageMedium: p.image_front_url || null,
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
      imageSmall: p.image_front_small_url || null,
      imageMedium: p.image_front_url || null,
    }));
  } catch (err) {
    console.error('OFF Search Error:', err);
    return [];
  }
}
