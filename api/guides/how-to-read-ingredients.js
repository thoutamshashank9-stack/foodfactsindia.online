import { renderSeoPage } from '../_lib/seoEngine.js';

export default function handler(req, res) {
  res.setHeader('Cache-Control', 'public, max-age=3600, s-maxage=3600, stale-while-revalidate=7200');

  const title = 'How to Read an Ingredient List on Food Labels | FoodFacts India';
  const description = 'Master reading ingredient lists on packaged food labels. Learn how descending order works, spot hidden sugars and refined oils, decode INS numbers, and identify ultra-processed foods.';
  const canonicalUrl = 'https://www.foodfactsindia.online/guides/how-to-read-ingredients';

  const breadcrumbs = [
    { name: 'Home', url: '/' },
    { name: 'Guides', url: '/guides' },
    { name: 'How to Read Ingredients', url: '/guides/how-to-read-ingredients' }
  ];

  const bodyHtml = `
    <article class="max-w-4xl mx-auto px-4 py-8 md:py-12" style="font-family: 'Source Serif 4', Georgia, serif;">
      <nav class="text-sm text-gray-500 mb-6 font-sans">
        <a href="/" class="hover:underline text-[#0f5b3a] font-medium">Home</a> &gt; 
        <span class="text-gray-600">How to Read Ingredients</span>
      </nav>

      <header class="border-b border-gray-200 pb-6 mb-8 font-sans">
        <div class="flex items-center gap-3 text-xs text-gray-500 mb-3">
          <span class="bg-emerald-50 text-emerald-800 px-2.5 py-0.5 rounded font-semibold uppercase">Pillar Guide</span>
          <span>FSSAI Regulation Checked: 24 March 2026</span>
          <span>•</span>
          <span>Snapshot: DS_SNAP_20260810</span>
        </div>
        <h1 class="text-3xl md:text-5xl font-bold text-gray-900 tracking-tight leading-tight mb-4">
          How to Read an Ingredient List on Food Labels
        </h1>
        <p class="text-xl text-gray-600 leading-relaxed font-serif">
          The ingredient list is the single most honest section of any packaged food label. Here is how to evaluate declared ingredients and spot hidden marketing traps.
        </p>
      </header>

      <div class="space-y-8 text-gray-800 text-lg leading-relaxed">
        <section space-y-4>
          <h2 class="text-2xl font-bold text-gray-900 font-sans">1. The Golden Rule: Descending Order by Weight</h2>
          <p>
            Under FSSAI Regulations, every packaged food product in India must declare ingredients in descending order of weight. Whatever appears first is present in the largest quantity.
          </p>
          <div class="bg-gray-50 p-5 rounded-xl border border-gray-100 font-sans text-sm">
            <strong>Example Label Analysis:</strong>
            <p class="text-gray-700 mt-1 italic">"Refined Wheat Flour (Maida), Sugar, Palm Oil, Invert Sugar Syrup, Raising Agents (INS 503ii, INS 500ii)..."</p>
            <p class="text-xs text-gray-500 mt-2">Analysis: The primary ingredient is refined flour, followed directly by added sugar and palm fat.</p>
          </div>
        </section>

        <section space-y-4>
          <h2 class="text-2xl font-bold text-gray-900 font-sans">2. Spotting Hidden Sugars</h2>
          <p>
            Manufacturers often split added sugars into multiple chemical names so no single sugar ingredient appears at the very top of the list. Look out for:
          </p>
          <ul class="list-disc pl-6 space-y-1 font-sans text-base text-gray-700">
            <li>Maltodextrin, Invert Sugar Syrup, Liquid Glucose</li>
            <li>High Fructose Corn Syrup, Dextrose, Fructose, Sucrose</li>
            <li>Rice Syrup, Brown Rice Syrup, Malt Extract</li>
          </ul>
        </section>

        <section space-y-4>
          <h2 class="text-2xl font-bold text-gray-900 font-sans">3. Identifying Additives & INS Numbers</h2>
          <p>
            Additives like preservatives, artificial colors, and flavor enhancers are indicated by INS numbers. Use our <a href="/tools/ingredient-checker" class="text-[#0f5b3a] font-bold hover:underline">Ingredient Checker Tool</a> to instantly parse and verify any list.
          </p>
        </section>

        <footer class="border-t border-gray-200 pt-6 mt-10 font-sans flex flex-col md:flex-row justify-between items-center gap-4 text-sm">
          <div class="text-gray-500">Analyze any ingredient list now:</div>
          <a href="/tools/ingredient-checker" class="px-5 py-2.5 bg-[#0f5b3a] hover:bg-[#0b442b] text-white font-semibold rounded-xl transition-colors">
            Try Ingredient Checker &rarr;
          </a>
        </footer>
      </div>
    </article>
  `;

  const html = renderSeoPage({
    title,
    description,
    canonicalUrl,
    pageType: 'article',
    breadcrumbs,
    articleData: {
      publishedDate: '2026-08-10',
      modifiedDate: '2026-08-10'
    },
    bodyHtml
  });

  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/html');
  res.end(html);
}
