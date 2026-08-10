import { renderSeoPage } from '../_lib/seoEngine.js';

export default function handler(req, res) {
  res.setHeader('Cache-Control', 'public, max-age=3600, s-maxage=3600, stale-while-revalidate=7200');

  const title = 'FSSAI Food Labelling Regulations Guide (2026 Rules) | FoodFacts India';
  const description = 'Official consumer guide to FSSAI Food Safety and Standards (Labelling and Display) Regulations 2020 and 24 March 2026 amendments. Understand mandatory declarations, Veg/Non-Veg symbols, and allergen rules.';
  const canonicalUrl = 'https://www.foodfactsindia.online/fssai/food-labelling';

  const breadcrumbs = [
    { name: 'Home', url: '/' },
    { name: 'FSSAI Regulations', url: '/fssai' },
    { name: 'Food Labelling Rules', url: '/fssai/food-labelling' }
  ];

  const bodyHtml = `
    <article class="max-w-4xl mx-auto px-4 py-8 md:py-12" style="font-family: 'Source Serif 4', Georgia, serif;">
      <nav class="text-sm text-gray-500 mb-6 font-sans">
        <a href="/" class="hover:underline text-[#0f5b3a] font-medium">Home</a> &gt; 
        <span class="text-gray-600">FSSAI Food Labelling Rules</span>
      </nav>

      <header class="border-b border-gray-200 pb-6 mb-8 font-sans">
        <div class="flex items-center gap-3 text-xs text-gray-500 mb-3">
          <span class="bg-red-50 text-red-800 px-2.5 py-0.5 rounded font-semibold uppercase">Regulatory Hub</span>
          <span>Latest FSSAI Amendment Checked: 24 March 2026</span>
          <span>•</span>
          <span>Official Source: FSSAI Gazette</span>
        </div>
        <h1 class="text-3xl md:text-5xl font-bold text-gray-900 tracking-tight leading-tight mb-4">
          FSSAI Food Labelling & Display Regulations: Consumer Guide
        </h1>
        <p class="text-xl text-gray-600 leading-relaxed font-serif">
          Plain-language explanation of mandatory labeling rules established by the Food Safety and Standards Authority of India (FSSAI) under the 2020 Regulations and subsequent amendments.
        </p>
      </header>

      <div class="space-y-8 text-gray-800 text-lg leading-relaxed">
        <section space-y-4>
          <h2 class="text-2xl font-bold text-gray-900 font-sans">1. Mandatory Label Declarations in India</h2>
          <p>
            Under Section 5 of FSSAI Labelling Regulations, every pre-packaged food item sold in India must display:
          </p>
          <ul class="list-disc pl-6 space-y-1 font-sans text-base text-gray-700">
            <li><strong>Name of the Food:</strong> Specific name, not merely a brand or trade name.</li>
            <li><strong>List of Ingredients:</strong> In descending order of weight.</li>
            <li><strong>Nutritional Information:</strong> Per 100g or per serve values for Energy, Protein, Carbohydrates, Total/Added Sugars, Total/Saturated/Trans Fats, and Sodium.</li>
            <li><strong>Veg / Non-Veg Symbol:</strong> Green filled circle inside a green square outline (Vegetarian) or Brown filled triangle inside a brown square outline (Non-Vegetarian).</li>
            <li><strong>FSSAI Logo & License Number:</strong> 14-digit FSSAI license number.</li>
            <li><strong>Date of Manufacture & Best Before / Expiry:</strong> Mandatory date marking.</li>
          </ul>
        </section>

        <section space-y-4>
          <h2 class="text-2xl font-bold text-gray-900 font-sans">2. Mandatory Allergen Warnings</h2>
          <p>
            FSSAI mandates declaring potential food allergens present in the product or processed in the same facility:
          </p>
          <div class="p-4 bg-gray-50 rounded-xl border border-gray-100 font-sans text-sm text-gray-700">
            Cereals containing gluten, Crustaceans, Eggs, Fish, Peanuts & Soybeans, Milk & Dairy, Tree Nuts, and Sulphites in concentrations of 10mg/kg or more.
          </div>
        </section>

        <section space-y-4>
          <h2 class="text-2xl font-bold text-gray-900 font-sans">3. Official FSSAI Provenance & Disclaimer</h2>
          <div class="bg-amber-50 p-5 rounded-xl border border-amber-100 font-sans text-sm text-amber-900">
            <strong>Official Source Reference:</strong> FSSAI Compendium of Food Safety and Standards (Labelling and Display) Regulations, 2020, with amendments up to 24 March 2026.<br/>
            <span class="text-xs text-amber-800 mt-2 block">Disclaimer: This guide is provided for consumer awareness and transparency. For official compliance or legal reference, refer to the original Gazette notifications published on the official FSSAI portal (fssai.gov.in).</span>
          </div>
        </section>

        <footer class="border-t border-gray-200 pt-6 mt-10 font-sans flex flex-col md:flex-row justify-between items-center gap-4 text-sm">
          <div class="text-gray-500">Check any product against FSSAI standards:</div>
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
