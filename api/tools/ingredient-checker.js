import { renderSeoPage } from '../_lib/seoEngine.js';

export default function handler(req, res) {
  res.setHeader('Cache-Control', 'public, max-age=3600, s-maxage=3600, stale-while-revalidate=7200');

  const title = 'Food Ingredient Checker | Analyze Ingredients & Additive Risk Levels';
  const description = 'Parse and evaluate food ingredient lists. Detect high-risk additives, artificial colors, palm oil, refined sugars, and major allergens declared on packaged food labels.';
  const canonicalUrl = 'https://www.foodfactsindia.online/tools/ingredient-checker';

  const breadcrumbs = [
    { name: 'Home', url: '/' },
    { name: 'Tools', url: '/tools' },
    { name: 'Ingredient Checker', url: '/tools/ingredient-checker' }
  ];

  const bodyHtml = `
    <article class="max-w-4xl mx-auto px-4 py-8 md:py-12" style="font-family: 'Source Serif 4', Georgia, serif;">
      <nav class="text-sm text-gray-500 mb-6 font-sans">
        <a href="/" class="hover:underline text-[#0f5b3a] font-medium">Home</a> &gt; 
        <span class="text-gray-600">Ingredient Checker</span>
      </nav>

      <header class="border-b border-gray-200 pb-6 mb-8 font-sans">
        <span class="inline-block px-3 py-1 bg-blue-50 text-blue-800 text-xs font-semibold rounded-full uppercase tracking-wider mb-3">
          Interactive Tool
        </span>
        <h1 class="text-3xl md:text-5xl font-bold text-gray-900 tracking-tight leading-tight mb-3">
          Food Ingredient Checker
        </h1>
        <p class="text-lg text-gray-600 max-w-2xl leading-relaxed">
          Paste any ingredient list to extract functional additives, evaluate NOVA processing levels, and check ingredient risk ratings against scientific monographs.
        </p>
      </header>

      <section class="bg-white p-6 md:p-8 rounded-2xl border border-gray-100 shadow-md font-sans mb-10">
        <h2 class="text-xl font-bold text-gray-900 mb-4">Paste Ingredient List</h2>
        <div class="space-y-4">
          <textarea placeholder="e.g., Refined Wheat Flour (Maida), Sugar, Palm Oil, Cocoa Solids, INS 322, INS 500(ii), Artificial Vanilla Flavour..." class="w-full h-32 p-4 border border-gray-200 rounded-xl focus:ring-2 focus:ring-[#0f5b3a] outline-none text-gray-800"></textarea>
          <button class="px-6 py-3 bg-[#0f5b3a] hover:bg-[#0b442b] text-white font-semibold rounded-xl transition-colors shadow-sm">
            Check Ingredients
          </button>
        </div>
      </section>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-8 font-sans">
        <section class="bg-white p-6 rounded-xl border border-gray-100 shadow-sm">
          <h3 class="text-lg font-bold text-gray-900 mb-3">How Ingredient Extraction Works</h3>
          <ul class="space-y-2 text-sm text-gray-700">
            <li class="flex items-center gap-2"><span class="text-emerald-600 font-bold">✓</span> <strong>Additive Tagging:</strong> Maps INS/E-numbers to canonical risk categories.</li>
            <li class="flex items-center gap-2"><span class="text-emerald-600 font-bold">✓</span> <strong>NOVA Group Analysis:</strong> Identifies NOVA 4 ultra-processed food markers.</li>
            <li class="flex items-center gap-2"><span class="text-emerald-600 font-bold">✓</span> <strong>Allergen Alerts:</strong> Highlights wheat/gluten, milk, soy, nuts, and sulphites.</li>
          </ul>
        </section>

        <section class="bg-white p-6 rounded-xl border border-gray-100 shadow-sm">
          <h3 class="text-lg font-bold text-gray-900 mb-3">Related Guides</h3>
          <ul class="space-y-2 text-sm text-blue-600 font-medium">
            <li><a href="/guides/how-to-read-ingredients" class="hover:underline">&rarr; How to Read an Ingredient List on Food Labels</a></li>
            <li><a href="/guides/food-additives" class="hover:underline">&rarr; Food Additives in India: Safety & Regulations</a></li>
            <li><a href="/guides/what-are-ins-numbers" class="hover:underline">&rarr; Complete INS Numbers Guide</a></li>
          </ul>
        </section>
      </div>
    </article>
  `;

  const html = renderSeoPage({
    title,
    description,
    canonicalUrl,
    pageType: 'tool',
    breadcrumbs,
    toolData: { name: 'Food Ingredient Checker' },
    bodyHtml
  });

  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/html');
  res.end(html);
}
