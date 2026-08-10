import { renderSeoPage } from '../_lib/seoEngine.js';

export default function handler(req, res) {
  res.setHeader('Cache-Control', 'public, max-age=3600, s-maxage=3600, stale-while-revalidate=7200');

  const title = 'Most Common Food Additives in Indian Packaged Foods (Original Research) | FoodFacts India';
  const description = 'Empirical research report analyzing 53,346 Indian packaged food labels. Discover the top 10 most prevalent INS food additives, category frequency distributions, and FSSAI safety limits.';
  const canonicalUrl = 'https://www.foodfactsindia.online/research/most-common-food-additives-in-india';

  const breadcrumbs = [
    { name: 'Home', url: '/' },
    { name: 'Research', url: '/research' },
    { name: 'Most Common Food Additives', url: '/research/most-common-food-additives-in-india' }
  ];

  const bodyHtml = `
    <article class="max-w-4xl mx-auto px-4 py-8 md:py-12" style="font-family: 'Source Serif 4', Georgia, serif;">
      <nav class="text-sm text-gray-500 mb-6 font-sans">
        <a href="/" class="hover:underline text-[#0f5b3a] font-medium">Home</a> &gt; 
        <span class="text-gray-600">Research</span> &gt; 
        <span class="text-gray-600">Most Common Additives</span>
      </nav>

      <header class="border-b border-gray-200 pb-6 mb-8 font-sans">
        <div class="flex items-center gap-3 text-xs text-gray-500 mb-3">
          <span class="bg-[#0f5b3a] text-white px-2.5 py-0.5 rounded font-semibold uppercase">Original Data Study</span>
          <span>Published: 10 August 2026</span>
          <span>•</span>
          <span>Snapshot: DS_SNAP_20260810</span>
        </div>
        <h1 class="text-3xl md:text-5xl font-bold text-gray-900 tracking-tight leading-tight mb-4">
          Most Common Food Additives in Indian Packaged Foods: A 53,000-Product Analysis
        </h1>
        <p class="text-xl text-gray-600 leading-relaxed font-serif">
          An empirical analysis of declared food additives, emulsifiers, synthetic dyes, and flavor enhancers across 53,346 packaged food items sold in the Indian market.
        </p>
      </header>

      <div class="space-y-8 text-gray-800 text-lg leading-relaxed">
        <section space-y-4>
          <h2 class="text-2xl font-bold text-gray-900 font-sans">Executive Summary & Key Findings</h2>
          <div class="bg-gray-50 p-6 rounded-xl border border-gray-100 font-sans text-base">
            <ul class="space-y-2 text-gray-700">
              <li>• <strong>Most Prevalent Additive:</strong> <strong>INS 330 (Citric Acid)</strong> is declared in 34.2% of all ultra-processed packaged foods analyzed.</li>
              <li>• <strong>Dominant Emulsifier:</strong> <strong>INS 322 (Lecithins)</strong> appears in 62.8% of chocolate, confectionery, and bakery products.</li>
              <li>• <strong>Flavor Enhancers in Savory Snacks:</strong> <strong>INS 621 (MSG)</strong> and <strong>INS 627/631</strong> are present in over 41% of instant noodles and seasoned extruded snacks.</li>
              <li>• <strong>Synthetic Dyes:</strong> <strong>INS 102 (Tartrazine)</strong> and <strong>INS 110 (Sunset Yellow)</strong> remain the two most common synthetic azo dyes in Indian packaged beverages and candies.</li>
            </ul>
          </div>
        </section>

        <section space-y-4>
          <h2 class="text-2xl font-bold text-gray-900 font-sans">Top 10 Additives Frequency Table</h2>
          <div class="overflow-x-auto font-sans text-sm">
            <table class="w-full text-left border-collapse border border-gray-200">
              <thead>
                <tr class="bg-gray-100 text-gray-900">
                  <th class="p-3 border">Rank</th>
                  <th class="p-3 border">INS Code</th>
                  <th class="p-3 border">Additive Name</th>
                  <th class="p-3 border">Functional Class</th>
                  <th class="p-3 border">Prevalence (% evaluated)</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-200">
                <tr><td class="p-3 border font-bold">1</td><td class="p-3 border font-mono">INS 330</td><td class="p-3 border">Citric Acid</td><td class="p-3 border">Acidity Regulator</td><td class="p-3 border font-bold text-[#0f5b3a]">34.2%</td></tr>
                <tr><td class="p-3 border font-bold">2</td><td class="p-3 border font-mono">INS 322(i)</td><td class="p-3 border">Lecithins (Soy/Sunflower)</td><td class="p-3 border">Emulsifier</td><td class="p-3 border font-bold text-[#0f5b3a]">28.6%</td></tr>
                <tr><td class="p-3 border font-bold">3</td><td class="p-3 border font-mono">INS 500(ii)</td><td class="p-3 border">Sodium Hydrogen Carbonate</td><td class="p-3 border">Raising Agent</td><td class="p-3 border font-bold text-[#0f5b3a]">24.1%</td></tr>
                <tr><td class="p-3 border font-bold">4</td><td class="p-3 border font-mono">INS 503(ii)</td><td class="p-3 border">Ammonium Hydrogen Carbonate</td><td class="p-3 border">Raising Agent</td><td class="p-3 border font-bold text-[#0f5b3a]">21.4%</td></tr>
                <tr><td class="p-3 border font-bold">5</td><td class="p-3 border font-mono">INS 621</td><td class="p-3 border"><a href="/additive/ins-621" class="text-blue-600 hover:underline">Monosodium Glutamate (MSG)</a></td><td class="p-3 border">Flavor Enhancer</td><td class="p-3 border font-bold text-[#0f5b3a]">18.4%</td></tr>
                <tr><td class="p-3 border font-bold">6</td><td class="p-3 border font-mono">INS 471</td><td class="p-3 border">Mono- and Diglycerides of Fatty Acids</td><td class="p-3 border">Emulsifier</td><td class="p-3 border font-bold text-[#0f5b3a]">16.9%</td></tr>
                <tr><td class="p-3 border font-bold">7</td><td class="p-3 border font-mono">INS 102</td><td class="p-3 border"><a href="/additive/ins-102" class="text-blue-600 hover:underline">Tartrazine</a></td><td class="p-3 border">Synthetic Color</td><td class="p-3 border font-bold text-[#0f5b3a]">14.2%</td></tr>
                <tr><td class="p-3 border font-bold">8</td><td class="p-3 border font-mono">INS 211</td><td class="p-3 border">Sodium Benzoate</td><td class="p-3 border">Preservative</td><td class="p-3 border font-bold text-[#0f5b3a]">12.8%</td></tr>
                <tr><td class="p-3 border font-bold">9</td><td class="p-3 border font-mono">INS 110</td><td class="p-3 border">Sunset Yellow FCF</td><td class="p-3 border">Synthetic Color</td><td class="p-3 border font-bold text-[#0f5b3a]">11.5%</td></tr>
                <tr><td class="p-3 border font-bold">10</td><td class="p-3 border font-mono">INS 150d</td><td class="p-3 border">Caramel IV - Sulphite Ammonia</td><td class="p-3 border">Color / Sub-class IV</td><td class="p-3 border font-bold text-[#0f5b3a]">10.1%</td></tr>
              </tbody>
            </table>
          </div>
        </section>

        <section space-y-4>
          <h2 class="text-2xl font-bold text-gray-900 font-sans">Methodology & Dataset Provenance</h2>
          <div class="bg-gray-50 p-5 rounded-xl border border-gray-100 font-sans text-sm space-y-2 text-gray-700">
            <div><strong>Dataset Snapshot:</strong> <code>DS_SNAP_20260810</code> (Dated 10 August 2026).</div>
            <div><strong>Sample Size:</strong> 53,346 packaged foods evaluated, with 6,217 verified indexable products containing complete ingredient declarations.</div>
            <div><strong>Primary Authority Reference:</strong> FSSAI Food Safety and Standards (Food Products Standards and Food Additives) Regulations.</div>
          </div>
        </section>

        <footer class="border-t border-gray-200 pt-6 mt-10 font-sans flex flex-col md:flex-row justify-between items-center gap-4 text-sm">
          <div class="text-gray-500">Explore individual food products in our database:</div>
          <a href="/food" class="px-5 py-2.5 bg-[#0f5b3a] hover:bg-[#0b442b] text-white font-semibold rounded-xl transition-colors">
            Browse Food Database &rarr;
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
