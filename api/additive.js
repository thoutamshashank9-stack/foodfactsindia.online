import { supabase } from './_lib/supabase.js';
import { renderHtmlPage } from './_lib/html.js';

export default async function handler(req, res) {
  res.setHeader('Cache-Control', 'public, max-age=3600, s-maxage=3600, stale-while-revalidate=7200');

  const slug = req.query.slug || '';
  if (!slug) {
    res.statusCode = 400;
    res.setHeader('Content-Type', 'text/html');
    res.end('<h1>400 Bad Request</h1><p>Missing additive slug.</p>');
    return;
  }

  // Normalize slug to database format (e.g., ins-621 -> E621, e211 -> E211)
  let cleanCode = slug.trim().toUpperCase().replace(/-/g, '');
  if (cleanCode.startsWith('INS')) {
    cleanCode = 'E' + cleanCode.substring(3);
  }

  try {
    // 1. Fetch regulatory details from additive_rulebook
    const { data: rules } = await supabase
      .from('additive_rulebook')
      .select('*')
      .ilike('additive_code', cleanCode);

    // 2. Fetch products containing this additive
    const { data: products } = await supabase
      .from('product_additives')
      .select(`
        barcode,
        additive_code,
        products:barcode (
          product_name,
          brands,
          slug,
          seo_status
        )
      `)
      .ilike('additive_code', `${cleanCode}%`)
      .limit(15);

    const matchedProducts = (products || [])
      .map(p => p.products)
      .filter(p => p && p.seo_status === 'INDEX')
      .slice(0, 10);

    const primaryRule = rules && rules.length > 0 ? rules[0] : null;
    const name = primaryRule ? primaryRule.canonical_name : `INS ${cleanCode.replace(/^E/, '')}`;

    const title = `${name} (${cleanCode}) Uses & Food Label Information | FoodFacts India`;
    const description = `Learn what food additive ${cleanCode} (${name}) is, its FSSAI regulatory status in India, safety risks, and products containing it.`;
    const canonicalUrl = `https://www.foodfactsindia.online/additive/${slug}`;

    const breadcrumbSchema = {
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.foodfactsindia.online" },
        { "@type": "ListItem", "position": 2, "name": "Additives", "item": "https://www.foodfactsindia.online/additives" },
        { "@type": "ListItem", "position": 3, "name": name, "item": canonicalUrl }
      ]
    };

    const bodyHtml = `
      <article class="max-w-4xl mx-auto px-4 py-8 md:py-12" style="font-family: 'Source Serif 4', Georgia, serif;">
        <nav class="text-sm text-gray-500 mb-6 font-sans">
          <a href="/" class="hover:underline text-[#0f5b3a] font-medium">Home</a> &gt; 
          <span class="text-gray-600">Additive Details</span>
        </nav>

        <header class="border-b border-gray-200 pb-6 mb-8 font-sans">
          <span class="inline-block px-3 py-1 bg-amber-50 text-amber-700 text-xs font-semibold rounded-full uppercase tracking-wider mb-3">
            Additive Code: ${cleanCode} / INS ${cleanCode.replace(/^E/, '')}
          </span>
          <h1 class="text-3xl md:text-4xl font-bold text-gray-900 tracking-tight leading-tight mb-2">
            ${escapeHtml(name)}
          </h1>
          <p class="text-lg text-gray-600 font-medium">
            Category: <span class="text-gray-900">Food Additive</span>
          </p>
        </header>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div class="md:col-span-2 space-y-8">
            <section class="bg-white p-6 rounded-xl border border-gray-100 shadow-sm">
              <h2 class="text-xl font-bold text-gray-900 font-sans mb-3">What is ${escapeHtml(name)}?</h2>
              <p class="text-gray-800 leading-relaxed text-lg mb-4">
                ${escapeHtml(name)} (commonly designated as INS ${cleanCode.replace(/^E/, '')} or E${cleanCode.replace(/^E/, '')}) is a food additive used globally. Regulators define usage limits to prevent health impacts.
              </p>
            </section>

            <section class="bg-white p-6 rounded-xl border border-gray-100 shadow-sm font-sans">
              <h2 class="text-xl font-bold text-gray-900 mb-4 font-sans">Regulatory Warnings & Limits</h2>
              <div class="space-y-4">
                ${rules && rules.length > 0 ? rules.map(r => `
                  <div class="p-4 bg-gray-50 rounded-lg border border-gray-100">
                    <div class="flex justify-between items-start gap-4">
                      <div>
                        <h4 class="font-bold text-gray-900">Jurisdiction: ${escapeHtml(r.jurisdiction)}</h4>
                        <p class="text-sm text-gray-700 mt-1">Status: <span class="uppercase text-xs font-bold px-1.5 py-0.5 rounded ${
                          r.status === 'BANNED' ? 'bg-red-100 text-red-800' : r.status === 'RESTRICTED' ? 'bg-amber-100 text-amber-800' : 'bg-emerald-100 text-emerald-800'
                        }">${r.status}</span></p>
                      </div>
                    </div>
                    ${r.label_requirement ? `
                      <div class="mt-3 text-xs bg-amber-50 p-2 border border-amber-100 text-amber-800 rounded font-mono">
                        <strong>Label Requirement:</strong> ${escapeHtml(r.label_requirement)}
                      </div>
                    ` : ''}
                  </div>
                `).join('') : '<p class="text-gray-500 italic">No specific rulebook entries found. Refer to general FSSAI guidelines.</p>'}
              </div>
            </section>
          </div>

          <!-- Sidebar -->
          <div class="space-y-6 font-sans">
            <section class="bg-white p-6 rounded-xl border border-gray-100 shadow-sm">
              <h3 class="text-lg font-bold text-gray-900 mb-4">Products Containing This</h3>
              <ul class="space-y-3">
                ${matchedProducts.length > 0 ? matchedProducts.map(p => `
                  <li>
                    <a href="/food/${p.slug}" class="block p-3 hover:bg-gray-50 rounded-lg border border-gray-100 transition-colors">
                      <div class="font-semibold text-gray-800 text-sm">${escapeHtml(p.product_name)}</div>
                      <div class="text-xs text-gray-500">${escapeHtml(p.brands || 'Unknown Brand')}</div>
                    </a>
                  </li>
                `).join('') : '<li class="text-gray-500 italic text-sm">No verified products currently listed in database.</li>'}
              </ul>
            </section>
          </div>
        </div>
      </article>
    `;

    const html = renderHtmlPage({
      title,
      description,
      canonicalUrl,
      schema: [breadcrumbSchema],
      bodyHtml
    });

    res.statusCode = 200;
    res.setHeader('Content-Type', 'text/html');
    res.end(html);
  } catch (err) {
    console.error('Additive handler exception:', err);
    res.statusCode = 500;
    res.setHeader('Content-Type', 'text/html');
    res.end('<h1>500 Internal Server Error</h1><p>Failed to render additive page.</p>');
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
