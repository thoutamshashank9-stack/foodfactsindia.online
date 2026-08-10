import { supabase } from './_lib/supabase.js';
import { renderSeoPage } from './_lib/seoEngine.js';

export default async function handler(req, res) {
  res.setHeader('Cache-Control', 'public, max-age=3600, s-maxage=3600, stale-while-revalidate=7200');

  try {
    // Fetch top verified products for database directory landing page
    const { data: products } = await supabase
      .from('products')
      .select('product_name, brands, categories, slug, barcode, nutriscore_grade, nova_group')
      .eq('seo_status', 'INDEX')
      .order('created_at', { ascending: false })
      .limit(24);

    const title = 'Packaged Food Database India | FoodFacts India Transparency Portal';
    const description = 'Search and analyze 53,000+ Indian packaged foods. Inspect verified ingredients, declared additives, nutrition facts, and regulatory safety markers.';
    const canonicalUrl = 'https://www.foodfactsindia.online/food';

    const breadcrumbs = [
      { name: 'Home', url: '/' },
      { name: 'Food Database', url: '/food' }
    ];

    const bodyHtml = `
      <article class="max-w-5xl mx-auto px-4 py-8 md:py-12" style="font-family: 'Source Serif 4', Georgia, serif;">
        <nav class="text-sm text-gray-500 mb-6 font-sans">
          <a href="/" class="hover:underline text-[#0f5b3a] font-medium">Home</a> &gt; 
          <span class="text-gray-600">Packaged Food Database</span>
        </nav>

        <header class="border-b border-gray-200 pb-6 mb-8 font-sans">
          <span class="inline-block px-3 py-1 bg-[#e8f5e9] text-[#0f5b3a] text-xs font-semibold rounded-full uppercase tracking-wider mb-3">
            Dataset Snapshot: 2026-08-10 (DS_SNAP_20260810)
          </span>
          <h1 class="text-3xl md:text-5xl font-bold text-gray-900 tracking-tight leading-tight mb-3">
            Indian Packaged Food Database
          </h1>
          <p class="text-lg text-gray-600 max-w-3xl leading-relaxed">
            Evidence-based transparency for 53,346 packaged foods sold in India. Filter products by category, inspect declared ingredient lists, and examine FSSAI regulatory compliance.
          </p>
        </header>

        <section class="mb-10 font-sans">
          <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
            <div class="p-4 bg-white rounded-xl border border-gray-100 shadow-sm text-center">
              <div class="text-2xl font-bold text-[#0f5b3a]">53,346</div>
              <div class="text-xs text-gray-500 font-medium">Total Products Evaluated</div>
            </div>
            <div class="p-4 bg-white rounded-xl border border-gray-100 shadow-sm text-center">
              <div class="text-2xl font-bold text-emerald-600">6,217</div>
              <div class="text-xs text-gray-500 font-medium">Verified Indexable Products</div>
            </div>
            <div class="p-4 bg-white rounded-xl border border-gray-100 shadow-sm text-center">
              <div class="text-2xl font-bold text-amber-600">119</div>
              <div class="text-xs text-gray-500 font-medium">FSSAI Category Limits</div>
            </div>
            <div class="p-4 bg-white rounded-xl border border-gray-100 shadow-sm text-center">
              <div class="text-2xl font-bold text-blue-600">678</div>
              <div class="text-xs text-gray-500 font-medium">Global Additives Mapped</div>
            </div>
          </div>
        </section>

        <section class="space-y-6 font-sans">
          <h2 class="text-2xl font-bold text-gray-900">Recently Verified Products</h2>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            ${(products || []).map(p => `
              <a href="/food/${p.slug}" class="block p-5 bg-white rounded-xl border border-gray-100 shadow-sm hover:border-[#0f5b3a] transition-all">
                <span class="text-xs font-semibold text-gray-400 uppercase tracking-wider">${escapeHtml(p.categories || 'Food')}</span>
                <h3 class="font-bold text-gray-900 text-lg mt-1 mb-1 leading-snug">${escapeHtml(p.product_name)}</h3>
                <p class="text-sm text-gray-600 font-medium mb-3">Brand: ${escapeHtml(p.brands || 'Unspecified')}</p>
                <div class="flex items-center justify-between text-xs text-gray-500 border-t pt-3 font-mono">
                  <span>Barcode: ${p.barcode}</span>
                  ${p.nutriscore_grade ? `<span class="px-2 py-0.5 bg-emerald-100 text-emerald-800 font-bold uppercase rounded">${p.nutriscore_grade}</span>` : ''}
                </div>
              </a>
            `).join('')}
          </div>
        </section>
      </article>
    `;

    const html = renderSeoPage({
      title,
      description,
      canonicalUrl,
      pageType: 'database',
      breadcrumbs,
      bodyHtml
    });

    res.statusCode = 200;
    res.setHeader('Content-Type', 'text/html');
    res.end(html);
  } catch (err) {
    console.error('Food database handler error:', err);
    res.statusCode = 500;
    res.setHeader('Content-Type', 'text/html');
    res.end('<h1>500 Internal Server Error</h1>');
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
