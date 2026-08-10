import { INGREDIENT_DATABASE } from '../src/data/ingredientsDatabase.js';
import { supabase } from './_lib/supabase.js';
import { renderHtmlPage } from './_lib/html.js';

export default async function handler(req, res) {
  res.setHeader('Cache-Control', 'public, max-age=3600, s-maxage=3600, stale-while-revalidate=7200');

  const slug = req.query.slug || '';
  if (!slug) {
    res.statusCode = 400;
    res.setHeader('Content-Type', 'text/html');
    res.end('<h1>400 Bad Request</h1><p>Missing ingredient slug.</p>');
    return;
  }

  const cleanSlug = slug.toLowerCase().replace(/-/g, ' ');

  // Find in INGREDIENT_DATABASE
  const ingredient = INGREDIENT_DATABASE.find(i => {
    const canonicalLower = i.canonicalName.toLowerCase();
    const idLower = i.id.toLowerCase();
    const synonymMatch = i.synonyms.some(s => s.toLowerCase() === cleanSlug);
    return canonicalLower === cleanSlug || idLower === cleanSlug || synonymMatch;
  });

  if (!ingredient) {
    // If not in database, render a generic page for the ingredient since we want to be indexable
    // for search terms that might not be in our pre-defined high-risk list.
    return renderGenericIngredient(cleanSlug, req, res);
  }

  try {
    // Query products containing this ingredient
    // We search the product_ingredients table for matches
    const { data: products, error } = await supabase
      .from('product_ingredients')
      .select(`
        barcode,
        ingredient_raw,
        products:barcode (
          product_name,
          brands,
          slug,
          seo_status
        )
      `)
      .ilike('ingredient_raw', `%${cleanSlug}%`)
      .limit(15);

    const matchedProducts = (products || [])
      .map(p => p.products)
      .filter(p => p && p.seo_status === 'INDEX')
      .slice(0, 10);

    const title = `${ingredient.canonicalName} in Indian Packaged Foods | FoodFacts India`;
    const description = `Learn about ${ingredient.canonicalName} (${ingredient.category}), its risk level (${ingredient.riskLevel}), health concerns, and which Indian products contain it.`;
    const canonicalUrl = `https://www.foodfactsindia.online/ingredient/${slug}`;

    const breadcrumbSchema = {
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.foodfactsindia.online" },
        { "@type": "ListItem", "position": 2, "name": "Ingredients", "item": "https://www.foodfactsindia.online/ingredients" },
        { "@type": "ListItem", "position": 3, "name": ingredient.canonicalName, "item": canonicalUrl }
      ]
    };

    const bodyHtml = `
      <article class="max-w-4xl mx-auto px-4 py-8 md:py-12" style="font-family: 'Source Serif 4', Georgia, serif;">
        <nav class="text-sm text-gray-500 mb-6 font-sans">
          <a href="/" class="hover:underline text-[#0f5b3a] font-medium">Home</a> &gt; 
          <span class="text-gray-600">Ingredient Details</span>
        </nav>

        <header class="border-b border-gray-200 pb-6 mb-8 font-sans">
          <span class="inline-block px-3 py-1 bg-red-50 text-red-700 text-xs font-semibold rounded-full uppercase tracking-wider mb-3">
            Risk: ${ingredient.riskLevel}
          </span>
          <h1 class="text-3xl md:text-4xl font-bold text-gray-900 tracking-tight leading-tight mb-2">
            ${escapeHtml(ingredient.canonicalName)}
          </h1>
          <p class="text-lg text-gray-600 font-medium">
            Category: <span class="text-gray-900">${escapeHtml(ingredient.category.replace(/_/g, ' '))}</span>
          </p>
        </header>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div class="md:col-span-2 space-y-8">
            <section class="bg-white p-6 rounded-xl border border-gray-100 shadow-sm">
              <h2 class="text-xl font-bold text-gray-900 font-sans mb-3">What is ${escapeHtml(ingredient.canonicalName)}?</h2>
              <p class="text-gray-800 leading-relaxed text-lg mb-4">
                ${escapeHtml(ingredient.description)}
              </p>
              ${ingredient.scientificName ? `
                <div class="text-sm text-gray-600 bg-gray-50 p-3 rounded-lg border border-gray-100 font-sans mt-3">
                  <strong>Scientific Name:</strong> <span class="font-mono text-xs">${escapeHtml(ingredient.scientificName)}</span>
                </div>
              ` : ''}
            </section>

            ${ingredient.citations && ingredient.citations.length > 0 ? `
              <section class="bg-white p-6 rounded-xl border border-gray-100 shadow-sm font-sans">
                <h2 class="text-xl font-bold text-gray-900 mb-4">Scientific Evidence & Citations</h2>
                <div class="space-y-4">
                  ${ingredient.citations.map(c => `
                    <div class="border-l-4 border-blue-500 pl-4 py-1">
                      <h4 class="font-semibold text-gray-900">${escapeHtml(c.title)}</h4>
                      <p class="text-xs text-gray-500 mb-2">${escapeHtml(c.journal)} (${c.year})</p>
                      <p class="text-sm text-gray-700">${escapeHtml(c.summary)}</p>
                      ${c.doi ? `<a href="${escapeHtml(c.doi)}" target="_blank" rel="noopener noreferrer" class="text-xs text-blue-600 hover:underline mt-1 inline-block">View Citation Study &rarr;</a>` : ''}
                    </div>
                  `).join('')}
                </div>
              </section>
            ` : ''}

            <section class="bg-white p-6 rounded-xl border border-gray-100 shadow-sm font-sans">
              <h2 class="text-xl font-bold text-gray-900 mb-4">Regulatory Records</h2>
              <div class="space-y-3">
                ${ingredient.regulatoryRecords && ingredient.regulatoryRecords.length > 0 ? ingredient.regulatoryRecords.map(r => `
                  <div class="p-3 bg-gray-50 rounded-lg border border-gray-100 flex items-start gap-3">
                    <span class="text-2xl">${r.flagEmoji}</span>
                    <div>
                      <div class="font-semibold text-gray-800">${escapeHtml(r.countryName)}: <span class="uppercase text-xs font-bold px-1.5 py-0.5 rounded ${
                        r.status === 'BANNED' ? 'bg-red-100 text-red-800' : r.status === 'RESTRICTED' ? 'bg-amber-100 text-amber-800' : 'bg-emerald-100 text-emerald-800'
                      }">${r.status}</span></div>
                      <p class="text-sm text-gray-600 mt-1">${escapeHtml(r.restrictionDetails || 'Standard approval rules apply.')}</p>
                      <span class="text-[10px] text-gray-400 font-mono">Reference: ${escapeHtml(r.regulationRef)}</span>
                    </div>
                  </div>
                `).join('') : '<p class="text-gray-500 italic">No specific global restrictions identified for this food ingredient.</p>'}
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
    console.error('Ingredient handler exception:', err);
    res.statusCode = 500;
    res.setHeader('Content-Type', 'text/html');
    res.end('<h1>500 Internal Server Error</h1><p>Failed to render ingredient page.</p>');
  }
}

async function renderGenericIngredient(cleanName, req, res) {
  const title = `${cleanName.charAt(0).toUpperCase() + cleanName.slice(1)}: Food Label Details | FoodFacts India`;
  const description = `Information about ${cleanName} on packaged food labels, products containing this ingredient, and safety signals.`;
  const canonicalUrl = `https://www.foodfactsindia.online/ingredient/${req.query.slug}`;

  try {
    // Query products containing this ingredient
    const { data: products } = await supabase
      .from('product_ingredients')
      .select(`
        barcode,
        ingredient_raw,
        products:barcode (
          product_name,
          brands,
          slug,
          seo_status
        )
      `)
      .ilike('ingredient_raw', `%${cleanName}%`)
      .limit(10);

    const matchedProducts = (products || [])
      .map(p => p.products)
      .filter(p => p && p.seo_status === 'INDEX')
      .slice(0, 10);

    const bodyHtml = `
      <article class="max-w-4xl mx-auto px-4 py-8 md:py-12" style="font-family: 'Source Serif 4', Georgia, serif;">
        <nav class="text-sm text-gray-500 mb-6 font-sans">
          <a href="/" class="hover:underline text-[#0f5b3a] font-medium">Home</a> &gt; 
          <span class="text-gray-600">Ingredient Details</span>
        </nav>

        <header class="border-b border-gray-200 pb-6 mb-8 font-sans">
          <h1 class="text-3xl md:text-4xl font-bold text-gray-900 tracking-tight leading-tight mb-2">
            ${cleanName.charAt(0).toUpperCase() + cleanName.slice(1)}
          </h1>
          <p class="text-sm text-gray-500">
            Standard Packaged Food Ingredient
          </p>
        </header>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div class="md:col-span-2 space-y-8">
            <section class="bg-white p-6 rounded-xl border border-gray-100 shadow-sm">
              <h2 class="text-xl font-bold text-gray-900 font-sans mb-3">About this Ingredient</h2>
              <p class="text-gray-800 leading-relaxed text-lg mb-4">
                This ingredient is commonly listed on food product packaging. FoodFacts India compiles label information to make ingredients transparent to consumers.
              </p>
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
      bodyHtml
    });

    res.statusCode = 200;
    res.setHeader('Content-Type', 'text/html');
    res.end(html);
  } catch (err) {
    console.error('Generic ingredient handler error:', err);
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
