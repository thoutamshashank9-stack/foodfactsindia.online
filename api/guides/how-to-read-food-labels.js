import { renderSeoPage } from '../_lib/seoEngine.js';

export default function handler(req, res) {
  res.setHeader('Cache-Control', 'public, max-age=3600, s-maxage=3600, stale-while-revalidate=7200');

  const title = 'How to Read Food Labels in India (2026 FSSAI Guide) | FoodFacts India';
  const description = 'Comprehensive guide on reading packaged food labels in India according to FSSAI regulations. Learn to spot hidden sugars, INS additives, trans fats, and serving size traps.';
  const canonicalUrl = 'https://www.foodfactsindia.online/guides/how-to-read-food-labels';

  const breadcrumbs = [
    { name: 'Home', url: '/' },
    { name: 'Guides', url: '/guides' },
    { name: 'How to Read Food Labels', url: '/guides/how-to-read-food-labels' }
  ];

  const bodyHtml = `
    <article class="max-w-4xl mx-auto px-4 py-8 md:py-12" style="font-family: 'Source Serif 4', Georgia, serif;">
      <nav class="text-sm text-gray-500 mb-6 font-sans">
        <a href="/" class="hover:underline text-[#0f5b3a] font-medium">Home</a> &gt; 
        <span class="text-gray-600">How to Read Food Labels</span>
      </nav>

      <header class="border-b border-gray-200 pb-6 mb-8 font-sans">
        <div class="flex items-center gap-3 text-xs text-gray-500 mb-3">
          <span class="bg-blue-50 text-blue-700 px-2.5 py-0.5 rounded font-semibold uppercase">Pillar Guide</span>
          <span>FSSAI Regulation Checked: 24 March 2026</span>
          <span>•</span>
          <span>Snapshot: DS_SNAP_20260810</span>
        </div>
        <h1 class="text-3xl md:text-5xl font-bold text-gray-900 tracking-tight leading-tight mb-4">
          How to Read Food Labels in India: The Complete Guide
        </h1>
        <p class="text-xl text-gray-600 leading-relaxed font-serif">
          Learn how to decode ingredient declarations, identify hidden INS numbers, evaluate nutrition panels, and understand FSSAI mandatory packaging symbols.
        </p>
      </header>

      <div class="space-y-8 text-gray-800 text-lg leading-relaxed">
        <section class="bg-emerald-50 p-6 rounded-xl border border-emerald-100 font-sans text-base">
          <h2 class="text-lg font-bold text-[#0f5b3a] mb-2">Key Takeaways from 53,000+ Indian Food Labels</h2>
          <ul class="space-y-2 text-gray-700">
            <li>• <strong>Descending Order Rule:</strong> Ingredients are listed in descending order by weight. The first 3 ingredients make up the majority of the product.</li>
            <li>• <strong>Hidden Sugar Names:</strong> Sugar appears under 50+ aliases including maltodextrin, invert sugar syrup, and liquid glucose.</li>
            <li>• <strong>INS Number Codes:</strong> E-numbers / INS numbers indicate functional food additives (colors, preservatives, flavor enhancers).</li>
          </ul>
        </section>

        <section space-y-4>
          <h2 class="text-2xl font-bold text-gray-900 font-sans">1. The Descending Order of Ingredients</h2>
          <p>
            Under FSSAI Food Safety and Standards (Labelling and Display) Regulations 2020, manufacturers must list all declared ingredients in descending order of weight at the time of manufacture. If "Sugar" or "Refined Wheat Flour (Maida)" is listed first, that product consists primarily of maida or sugar.
          </p>
        </section>

        <section space-y-4>
          <h2 class="text-2xl font-bold text-gray-900 font-sans">2. Understanding INS Additive Numbers</h2>
          <p>
            INS (International Numbering System) codes are standardized numbers used for food additives. For example, <strong>INS 621</strong> represents Monosodium Glutamate (MSG), while <strong>INS 102</strong> represents Tartrazine (a synthetic yellow dye subject to mandatory warning labels in the EU).
          </p>
          <p class="text-sm font-sans bg-gray-50 p-4 rounded-xl border border-gray-100">
            Want to look up a specific code? Use our <a href="/guides/what-are-ins-numbers" class="text-blue-600 font-semibold hover:underline">Complete INS Numbers Guide</a> or paste the label into our <a href="/tools/food-label-checker" class="text-[#0f5b3a] font-semibold hover:underline">Food Label Checker Tool</a>.
          </p>
        </section>

        <section space-y-4>
          <h2 class="text-2xl font-bold text-gray-900 font-sans">3. Regulatory Source Provenance & Citations</h2>
          <div class="text-sm font-sans space-y-2 text-gray-600 bg-gray-50 p-4 rounded-xl border border-gray-100">
            <div><strong>Primary Regulatory Source:</strong> FSSAI Food Safety and Standards (Labelling and Display) Regulations, 2020.</div>
            <div><strong>Latest Amendment Checked:</strong> FSSAI Amendment Notification dated 24 March 2026.</div>
            <div><strong>Reviewed By:</strong> FoodFacts India Editorial Team (10 August 2026).</div>
          </div>
        </section>

        <footer class="border-t border-gray-200 pt-6 mt-10 font-sans flex flex-col md:flex-row justify-between items-center gap-4 text-sm">
          <div class="text-gray-500">Analyze any label instantly with our AI engine:</div>
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
