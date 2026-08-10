import { supabase } from './_lib/supabase.js';
import { renderHtmlPage } from './_lib/html.js';

export default async function handler(req, res) {
  // Set Cache-Control header: 1-hour public cache, stale-while-revalidate
  res.setHeader('Cache-Control', 'public, max-age=3600, s-maxage=3600, stale-while-revalidate=7200');

  const slug = req.query.slug || '';
  if (!slug) {
    res.statusCode = 400;
    res.setHeader('Content-Type', 'text/html');
    res.end('<h1>400 Bad Request</h1><p>Missing product slug.</p>');
    return;
  }

  try {
    // Query product by slug
    const { data: product, error } = await supabase
      .from('products')
      .select('*')
      .eq('slug', slug)
      .maybeSingle();

    if (error || !product) {
      res.statusCode = 404;
      res.setHeader('Content-Type', 'text/html');
      res.end(`<h1>404 Product Not Found</h1><p>The product with slug "${slug}" could not be found.</p>`);
      return;
    }

    const title = `${product.product_name} Ingredients & Nutrition Facts | FoodFacts India`;
    const description = `Explore ingredients, nutritional composition, additives, and safety signals for ${product.product_name} by ${product.brands || 'Unknown Brand'} on FoodFacts India.`;
    const canonicalUrl = `https://www.foodfactsindia.online/food/${product.slug}`;
    const ogImage = product.image_front_url;

    // Build Product Schema
    const productSchema = {
      "@context": "https://schema.org/",
      "@type": "Product",
      "name": product.product_name,
      "image": product.image_front_url || "https://www.foodfactsindia.online/og-default.png",
      "description": description,
      "gtin13": product.barcode,
      "brand": {
        "@type": "Brand",
        "name": product.brands || "Unknown Brand"
      },
      "category": product.categories || "Packaged Food"
    };

    // Build Breadcrumb Schema
    const breadcrumbSchema = {
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        {
          "@type": "ListItem",
          "position": 1,
          "name": "Home",
          "item": "https://www.foodfactsindia.online"
        },
        {
          "@type": "ListItem",
          "position": 2,
          "name": "Food Database",
          "item": "https://www.foodfactsindia.online/food"
        },
        {
          "@type": "ListItem",
          "position": 3,
          "name": product.product_name,
          "item": canonicalUrl
        }
      ]
    };

    // Combine schemas in an array
    const combinedSchema = [productSchema, breadcrumbSchema];

    // Build server-rendered HTML content
    const bodyHtml = `
      <article class="max-w-4xl mx-auto px-4 py-8 md:py-12" style="font-family: 'Source Serif 4', Georgia, serif;">
        <nav class="text-sm text-gray-500 mb-6 font-sans">
          <a href="/" class="hover:underline text-[#0f5b3a] font-medium">Home</a> &gt; 
          <a href="/food" class="hover:underline text-[#0f5b3a] font-medium">Food Database</a> &gt; 
          <span class="text-gray-600">${escapeHtml(product.product_name)}</span>
        </nav>

        <header class="border-b border-gray-200 pb-6 mb-8 font-sans">
          <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <span class="inline-block px-3 py-1 bg-[#e8f5e9] text-[#0f5b3a] text-xs font-semibold rounded-full uppercase tracking-wider mb-3">
                ${escapeHtml(product.categories || 'Packaged Food')}
              </span>
              <h1 class="text-3xl md:text-4xl font-bold text-gray-900 tracking-tight leading-tight mb-2">
                ${escapeHtml(product.product_name)}
              </h1>
              <p class="text-lg text-gray-600 font-medium">
                Brand: <span class="text-gray-900">${escapeHtml(product.brands || 'Unspecified')}</span>
              </p>
            </div>
            <div class="flex items-center gap-4">
              ${product.nova_group ? `
                <div class="text-center p-3 bg-amber-50 border border-amber-200 rounded-lg">
                  <div class="text-xs text-amber-800 font-semibold uppercase tracking-wider">NOVA Group</div>
                  <div class="text-2xl font-bold text-amber-900">NOVA ${product.nova_group}</div>
                </div>
              ` : ''}
              ${product.nutriscore_grade ? `
                <div class="text-center p-3 bg-emerald-50 border border-emerald-200 rounded-lg">
                  <div class="text-xs text-emerald-800 font-semibold uppercase tracking-wider">Nutri-Score</div>
                  <div class="text-2xl font-bold text-emerald-900 uppercase">${product.nutriscore_grade}</div>
                </div>
              ` : ''}
            </div>
          </div>
        </header>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <!-- Main Content -->
          <div class="md:col-span-2 space-y-8">
            <section class="bg-white p-6 rounded-xl border border-gray-100 shadow-sm">
              <h2 class="text-2xl font-bold text-gray-900 font-sans mb-4 border-b pb-2">Ingredients Declared</h2>
              <p class="text-gray-800 leading-relaxed text-lg mb-4">
                ${product.ingredients_text ? escapeHtml(product.ingredients_text) : '<span class="text-gray-500 italic">Ingredient list not declared or not parsed.</span>'}
              </p>
              <div class="text-xs text-gray-500 font-sans mt-4">
                Barcode Identifier: <span class="font-mono bg-gray-100 px-1.5 py-0.5 rounded">${product.barcode}</span>
              </div>
            </section>

            <section class="bg-white p-6 rounded-xl border border-gray-100 shadow-sm">
              <h2 class="text-2xl font-bold text-gray-900 font-sans mb-4 border-b pb-2">Label Transparency & Claims</h2>
              <p class="text-gray-700 leading-relaxed font-sans text-sm">
                FoodFacts India evaluates label accuracy against original packaging evidence and FSSAI standards. Packaged foods are indexed for public safety transparency.
              </p>
            </section>
          </div>

          <!-- Sidebar (Nutrition & Details) -->
          <div class="space-y-6 font-sans">
            ${product.image_front_url ? `
              <div class="bg-white p-4 rounded-xl border border-gray-100 shadow-sm flex justify-center">
                <img src="${escapeHtml(product.image_front_url)}" alt="${escapeHtml(product.product_name)}" class="max-h-64 object-contain rounded-lg" />
              </div>
            ` : ''}

            <section class="bg-white p-6 rounded-xl border border-gray-100 shadow-sm">
              <h3 class="text-lg font-bold text-gray-900 mb-4 border-b pb-2">Nutrition Facts</h3>
              <table class="w-full text-sm text-left">
                <tbody>
                  <tr class="border-b"><th class="py-2 text-gray-600 font-normal">Energy (Calories)</th><td class="py-2 text-right font-semibold">${product.energy_100g != null ? product.energy_100g : '—'} kcal</td></tr>
                  <tr class="border-b"><th class="py-2 text-gray-600 font-normal">Total Fat</th><td class="py-2 text-right font-semibold">${product.fat_100g != null ? product.fat_100g : '—'} g</td></tr>
                  <tr class="border-b"><th class="py-2 text-gray-600 font-normal">Saturated Fat</th><td class="py-2 text-right font-semibold">${product.saturated_fat_100g != null ? product.saturated_fat_100g : '—'} g</td></tr>
                  <tr class="border-b"><th class="py-2 text-gray-600 font-normal">Trans Fat</th><td class="py-2 text-right font-semibold">${product.trans_fat_100g != null ? product.trans_fat_100g : '—'} g</td></tr>
                  <tr class="border-b"><th class="py-2 text-gray-600 font-normal">Total Sugar</th><td class="py-2 text-right font-semibold">${product.sugars_100g != null ? product.sugars_100g : '—'} g</td></tr>
                  <tr class="border-b"><th class="py-2 text-gray-600 font-normal">Protein</th><td class="py-2 text-right font-semibold">${product.protein_100g != null ? product.protein_100g : '—'} g</td></tr>
                  <tr class="border-b"><th class="py-2 text-gray-600 font-normal">Fibre</th><td class="py-2 text-right font-semibold">${product.fibre_100g != null ? product.fibre_100g : '—'} g</td></tr>
                  <tr class="border-b"><th class="py-2 text-gray-600 font-normal">Sodium</th><td class="py-2 text-right font-semibold">${product.sodium_100g != null ? Math.round(product.sodium_100g * 1000) : '—'} mg</td></tr>
                </tbody>
              </table>
              <div class="text-[10px] text-gray-400 mt-3 text-center">All nutritional values correspond to per 100g of product.</div>
            </section>
          </div>
        </div>
      </article>
    `;

    const html = renderHtmlPage({
      title,
      description,
      canonicalUrl,
      ogImage,
      schema: combinedSchema,
      bodyHtml
    });

    res.statusCode = 200;
    res.setHeader('Content-Type', 'text/html');
    res.end(html);
  } catch (err) {
    console.error('Edge function handler exception:', err);
    res.statusCode = 500;
    res.setHeader('Content-Type', 'text/html');
    res.end('<h1>500 Internal Server Error</h1><p>Failed to render product page server-side.</p>');
  }
}

function escapeHtml(unsafe) {
  if (!unsafe) return '';
  return String(unsafe)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}
