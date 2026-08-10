import { renderSeoPage } from '../_lib/seoEngine.js';

export default function handler(req, res) {
  res.setHeader('Cache-Control', 'public, max-age=3600, s-maxage=3600, stale-while-revalidate=7200');

  const title = 'What Are INS Numbers? Food Additive Codes Explained | FoodFacts India';
  const description = 'Complete guide to INS numbers (International Numbering System) on Indian packaged food labels. Understand flavor enhancers (INS 621), colors (INS 102), emulsifiers, and preservatives.';
  const canonicalUrl = 'https://www.foodfactsindia.online/guides/what-are-ins-numbers';

  const breadcrumbs = [
    { name: 'Home', url: '/' },
    { name: 'Guides', url: '/guides' },
    { name: 'What Are INS Numbers?', url: '/guides/what-are-ins-numbers' }
  ];

  const bodyHtml = `
    <article class="max-w-4xl mx-auto px-4 py-8 md:py-12" style="font-family: 'Source Serif 4', Georgia, serif;">
      <nav class="text-sm text-gray-500 mb-6 font-sans">
        <a href="/" class="hover:underline text-[#0f5b3a] font-medium">Home</a> &gt; 
        <span class="text-gray-600">What Are INS Numbers?</span>
      </nav>

      <header class="border-b border-gray-200 pb-6 mb-8 font-sans">
        <div class="flex items-center gap-3 text-xs text-gray-500 mb-3">
          <span class="bg-blue-50 text-blue-700 px-2.5 py-0.5 rounded font-semibold uppercase">Entity Knowledge Hub</span>
          <span>FSSAI Regulation Checked: 24 March 2026</span>
          <span>•</span>
          <span>Snapshot: DS_SNAP_20260810</span>
        </div>
        <h1 class="text-3xl md:text-5xl font-bold text-gray-900 tracking-tight leading-tight mb-4">
          What Are INS Numbers on Food Labels?
        </h1>
        <p class="text-xl text-gray-600 leading-relaxed font-serif">
          INS (International Numbering System) codes are standardized numeric identifiers assigned to food additives worldwide. Here is how to decode them on Indian packaged foods.
        </p>
      </header>

      <div class="space-y-8 text-gray-800 text-lg leading-relaxed">
        <section space-y-4>
          <h2 class="text-2xl font-bold text-gray-900 font-sans">Understanding INS Number Categories</h2>
          <p>
            The Codex Alimentarius committee and FSSAI categorize INS numbers into functional ranges based on their purpose:
          </p>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 font-sans text-sm mt-4">
            <div class="p-4 bg-white rounded-xl border border-gray-100 shadow-sm">
              <div class="font-bold text-[#0f5b3a]">INS 100 – 199</div>
              <div class="text-gray-600">Food Colors (e.g., INS 102 Tartrazine, INS 150d Caramel IV)</div>
            </div>
            <div class="p-4 bg-white rounded-xl border border-gray-100 shadow-sm">
              <div class="font-bold text-[#0f5b3a]">INS 200 – 299</div>
              <div class="text-gray-600">Preservatives (e.g., INS 211 Sodium Benzoate, INS 202 Potassium Sorbate)</div>
            </div>
            <div class="p-4 bg-white rounded-xl border border-gray-100 shadow-sm">
              <div class="font-bold text-[#0f5b3a]">INS 300 – 399</div>
              <div class="text-gray-600">Antioxidants & Acidity Regulators (e.g., INS 322 Lecithin, INS 330 Citric Acid)</div>
            </div>
            <div class="p-4 bg-white rounded-xl border border-gray-100 shadow-sm">
              <div class="font-bold text-[#0f5b3a]">INS 600 – 699</div>
              <div class="text-gray-600">Flavor Enhancers (e.g., INS 621 MSG, INS 627 Disodium Guanylate)</div>
            </div>
          </div>
        </section>

        <section space-y-4>
          <h2 class="text-2xl font-bold text-gray-900 font-sans">Common INS Additives in Indian Foods</h2>
          <div class="space-y-3 font-sans text-sm">
            <a href="/additive/ins-621" class="block p-4 bg-white rounded-xl border border-gray-100 hover:border-[#0f5b3a] transition-all">
              <div class="font-bold text-gray-900">INS 621 (Monosodium Glutamate / MSG) &rarr;</div>
              <div class="text-gray-600 mt-1">Flavor enhancer used in savory snacks, instant noodles, and soups. Restricted for infant food under FSSAI.</div>
            </a>
            <a href="/additive/ins-102" class="block p-4 bg-white rounded-xl border border-gray-100 hover:border-[#0f5b3a] transition-all">
              <div class="font-bold text-gray-900">INS 102 (Tartrazine / FD&C Yellow No. 5) &rarr;</div>
              <div class="text-gray-600 mt-1">Synthetic lemon yellow azo dye. Subject to mandatory EU warning labels for childhood hyperactivity.</div>
            </a>
          </div>
        </section>

        <footer class="border-t border-gray-200 pt-6 mt-10 font-sans flex flex-col md:flex-row justify-between items-center gap-4 text-sm">
          <div class="text-gray-500">Check any INS code instantly:</div>
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
