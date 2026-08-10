import { renderSeoPage } from '../_lib/seoEngine.js';

export default function handler(req, res) {
  res.setHeader('Cache-Control', 'public, max-age=3600, s-maxage=3600, stale-while-revalidate=7200');

  const title = 'How to Read Nutrition Labels in India (FSSAI Panel Guide) | FoodFacts India';
  const description = 'Learn how to read nutrition information panels on Indian packaged food labels. Understand serving size tricks, per 100g vs per serve values, added sugars, sodium, and saturated fats.';
  const canonicalUrl = 'https://www.foodfactsindia.online/guides/how-to-read-nutrition-labels';

  const breadcrumbs = [
    { name: 'Home', url: '/' },
    { name: 'Guides', url: '/guides' },
    { name: 'How to Read Nutrition Labels', url: '/guides/how-to-read-nutrition-labels' }
  ];

  const bodyHtml = `
    <article class="max-w-4xl mx-auto px-4 py-8 md:py-12" style="font-family: 'Source Serif 4', Georgia, serif;">
      <nav class="text-sm text-gray-500 mb-6 font-sans">
        <a href="/" class="hover:underline text-[#0f5b3a] font-medium">Home</a> &gt; 
        <span class="text-gray-600">How to Read Nutrition Labels</span>
      </nav>

      <header class="border-b border-gray-200 pb-6 mb-8 font-sans">
        <div class="flex items-center gap-3 text-xs text-gray-500 mb-3">
          <span class="bg-blue-50 text-blue-800 px-2.5 py-0.5 rounded font-semibold uppercase">Pillar Guide</span>
          <span>FSSAI Regulation Checked: 24 March 2026</span>
          <span>•</span>
          <span>Snapshot: DS_SNAP_20260810</span>
        </div>
        <h1 class="text-3xl md:text-5xl font-bold text-gray-900 tracking-tight leading-tight mb-4">
          How to Read Nutrition Labels in India
        </h1>
        <p class="text-xl text-gray-600 leading-relaxed font-serif">
          Decode nutritional information panels, spot serving size tricks, and evaluate saturated fat, sodium, and added sugar percentages against recommended daily allowances (RDA).
        </p>
      </header>

      <div class="space-y-8 text-gray-800 text-lg leading-relaxed">
        <section space-y-4>
          <h2 class="text-2xl font-bold text-gray-900 font-sans">1. Per 100g vs Per Serving Values</h2>
          <p>
            FSSAI mandates declaring energy, protein, carbohydrates, total sugars, added sugars, total fat, saturated fat, trans fat, and sodium per 100g/100ml. Check whether the declared figures apply to the full pack or a artificially small "serving size".
          </p>
        </section>

        <section space-y-4>
          <h2 class="text-2xl font-bold text-gray-900 font-sans">2. Added Sugar vs Total Sugar</h2>
          <p>
            Under FSSAI 2020 labelling mandates, manufacturers must distinguish naturally occurring sugars (like lactose in milk or fructose in fruit) from <strong>Added Sugars</strong>. Added sugar should contribute less than 10% of daily energy intake (~50g per day for adults).
          </p>
        </section>

        <section space-y-4>
          <h2 class="text-2xl font-bold text-gray-900 font-sans">3. Sodium Limits (Salt Content)</h2>
          <p>
            The WHO recommends limiting sodium intake to 2,000 mg per day (~5g of salt). Foods containing more than 600 mg of sodium per 100g are classified as high-sodium foods.
          </p>
        </section>

        <footer class="border-t border-gray-200 pt-6 mt-10 font-sans flex flex-col md:flex-row justify-between items-center gap-4 text-sm">
          <div class="text-gray-500">Analyze any label instantly:</div>
          <a href="/tools/food-label-checker" class="px-5 py-2.5 bg-[#0f5b3a] hover:bg-[#0b442b] text-white font-semibold rounded-xl transition-colors">
            Try Food Label Checker &rarr;
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
