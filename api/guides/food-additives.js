import { renderSeoPage } from '../_lib/seoEngine.js';

export default function handler(req, res) {
  res.setHeader('Cache-Control', 'public, max-age=3600, s-maxage=3600, stale-while-revalidate=7200');

  const title = 'Food Additives in India Explained (FSSAI Rules & Safety) | FoodFacts India';
  const description = 'Complete guide to food additives used in Indian packaged foods. Learn about FSSAI permitted limits, EU bans, Southampton artificial colors, preservatives, and MSG.';
  const canonicalUrl = 'https://www.foodfactsindia.online/guides/food-additives';

  const breadcrumbs = [
    { name: 'Home', url: '/' },
    { name: 'Guides', url: '/guides' },
    { name: 'Food Additives', url: '/guides/food-additives' }
  ];

  const bodyHtml = `
    <article class="max-w-4xl mx-auto px-4 py-8 md:py-12" style="font-family: 'Source Serif 4', Georgia, serif;">
      <nav class="text-sm text-gray-500 mb-6 font-sans">
        <a href="/" class="hover:underline text-[#0f5b3a] font-medium">Home</a> &gt; 
        <span class="text-gray-600">Food Additives</span>
      </nav>

      <header class="border-b border-gray-200 pb-6 mb-8 font-sans">
        <div class="flex items-center gap-3 text-xs text-gray-500 mb-3">
          <span class="bg-amber-50 text-amber-800 px-2.5 py-0.5 rounded font-semibold uppercase">Pillar Guide</span>
          <span>FSSAI Regulation Checked: 24 March 2026</span>
          <span>•</span>
          <span>Snapshot: DS_SNAP_20260810</span>
        </div>
        <h1 class="text-3xl md:text-5xl font-bold text-gray-900 tracking-tight leading-tight mb-4">
          Food Additives in Indian Packaged Foods: Safety & Regulations
        </h1>
        <p class="text-xl text-gray-600 leading-relaxed font-serif">
          What are food additives, why are they added, and how do FSSAI regulations compare against global food safety agencies like EFSA and the US FDA?
        </p>
      </header>

      <div class="space-y-8 text-gray-800 text-lg leading-relaxed">
        <section space-y-4>
          <h2 class="text-2xl font-bold text-gray-900 font-sans">Overview of Food Additives in India</h2>
          <p>
            Food additives are substances added to food to preserve flavor, enhance taste, improve appearance, or extend shelf life. FSSAI regulates additives under the Food Safety and Standards (Food Products Standards and Food Additives) Regulations.
          </p>
        </section>

        <section space-y-4>
          <h2 class="text-2xl font-bold text-gray-900 font-sans">High-Vigilance Additive Classes</h2>
          <div class="space-y-4 font-sans text-sm">
            <div class="p-4 bg-white rounded-xl border border-gray-100 shadow-sm">
              <h3 class="font-bold text-gray-900 text-base">1. Synthetic Azo Colors (Southampton Six)</h3>
              <p class="text-gray-600 mt-1">Tartrazine (INS 102), Sunset Yellow (INS 110), Carmoisine (INS 122), Ponceau 4R (INS 124), Allura Red (INS 129). Requires mandatory warnings in the EU due to links with hyperactive behavior in children.</p>
            </div>
            <div class="p-4 bg-white rounded-xl border border-gray-100 shadow-sm">
              <h3 class="font-bold text-gray-900 text-base">2. Flavor Enhancers (MSG / INS 621)</h3>
              <p class="text-gray-600 mt-1">Imparts umami taste. FSSAI mandates warning labels: "NOT RECOMMENDED FOR INFANTS BELOW 12 MONTHS".</p>
            </div>
            <div class="p-4 bg-white rounded-xl border border-gray-100 shadow-sm">
              <h3 class="font-bold text-gray-900 text-base">3. Banned & Revoked Additives (Titanium Dioxide / Erythrosine)</h3>
              <p class="text-gray-600 mt-1">E171 (Titanium Dioxide) was revoked in the EU in 2022 due to genotoxicity concerns. FD&C Red No. 3 authorization was revoked in the US.</p>
            </div>
          </div>
        </section>

        <footer class="border-t border-gray-200 pt-6 mt-10 font-sans flex flex-col md:flex-row justify-between items-center gap-4 text-sm">
          <div class="text-gray-500">Explore specific additives:</div>
          <a href="/guides/what-are-ins-numbers" class="px-5 py-2.5 bg-[#0f5b3a] hover:bg-[#0b442b] text-white font-semibold rounded-xl transition-colors">
            Complete INS Code Guide &rarr;
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
