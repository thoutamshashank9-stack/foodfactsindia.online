import { renderSeoPage } from '../_lib/seoEngine.js';

export default function handler(req, res) {
  res.setHeader('Cache-Control', 'public, max-age=3600, s-maxage=3600, stale-while-revalidate=7200');

  const title = 'Food Label Checker | Free Food Label Analysis & Safety Audit Tool';
  const description = 'Analyze packaged food labels in India. Paste declared ingredients, nutrition facts, or INS numbers to inspect health ratings, hidden sugars, sodium levels, and FSSAI additive restrictions.';
  const canonicalUrl = 'https://www.foodfactsindia.online/tools/food-label-checker';

  const breadcrumbs = [
    { name: 'Home', url: '/' },
    { name: 'Tools', url: '/tools' },
    { name: 'Food Label Checker', url: '/tools/food-label-checker' }
  ];

  const bodyHtml = `
    <article class="max-w-4xl mx-auto px-4 py-8 md:py-12" style="font-family: 'Source Serif 4', Georgia, serif;">
      <nav class="text-sm text-gray-500 mb-6 font-sans">
        <a href="/" class="hover:underline text-[#0f5b3a] font-medium">Home</a> &gt; 
        <span class="text-gray-600">Food Label Checker</span>
      </nav>

      <header class="border-b border-gray-200 pb-6 mb-8 font-sans">
        <span class="inline-block px-3 py-1 bg-emerald-50 text-emerald-800 text-xs font-semibold rounded-full uppercase tracking-wider mb-3">
          Interactive Tool
        </span>
        <h1 class="text-3xl md:text-5xl font-bold text-gray-900 tracking-tight leading-tight mb-3">
          Food Label Checker
        </h1>
        <p class="text-lg text-gray-600 max-w-2xl leading-relaxed">
          Instantly evaluate packaged food labels for hidden additives, trans fats, excessive sodium, and WHO nutrition benchmarks.
        </p>
      </header>

      <section class="bg-white p-6 md:p-8 rounded-2xl border border-gray-100 shadow-md font-sans mb-10">
        <h2 class="text-xl font-bold text-gray-900 mb-4">Paste & Analyze Label Text</h2>
        <div class="space-y-4">
          <textarea placeholder="Paste ingredient list (e.g., Wheat Flour, Palm Oil, INS 621, Salt, Sugar...)" class="w-full h-32 p-4 border border-gray-200 rounded-xl focus:ring-2 focus:ring-[#0f5b3a] outline-none text-gray-800"></textarea>
          <button class="px-6 py-3 bg-[#0f5b3a] hover:bg-[#0b442b] text-white font-semibold rounded-xl transition-colors shadow-sm">
            Analyze Food Label
          </button>
        </div>
      </section>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-8 font-sans">
        <section class="bg-white p-6 rounded-xl border border-gray-100 shadow-sm">
          <h3 class="text-lg font-bold text-gray-900 mb-3">What This Tool Evaluates</h3>
          <ul class="space-y-2 text-sm text-gray-700">
            <li class="flex items-center gap-2"><span class="text-emerald-600 font-bold">✓</span> <strong>INS & E-Number Additives:</strong> Flags artificial colors, preservatives & flavor enhancers.</li>
            <li class="flex items-center gap-2"><span class="text-emerald-600 font-bold">✓</span> <strong>WHO Nutrition Flags:</strong> Detects high sodium (>600mg/100g) & free sugars (>10% energy).</li>
            <li class="flex items-center gap-2"><span class="text-emerald-600 font-bold">✓</span> <strong>FSSAI Compliance:</strong> Compares ingredients against official FSSAI Schedule 2.4.5 restrictions.</li>
          </ul>
        </section>

        <section class="bg-white p-6 rounded-xl border border-gray-100 shadow-sm">
          <h3 class="text-lg font-bold text-gray-900 mb-3">Related Guides</h3>
          <ul class="space-y-2 text-sm text-blue-600 font-medium">
            <li><a href="/guides/how-to-read-food-labels" class="hover:underline">&rarr; How to Read Food Labels in India</a></li>
            <li><a href="/guides/what-are-ins-numbers" class="hover:underline">&rarr; What Are INS Numbers? Complete Additive Code Guide</a></li>
            <li><a href="/food" class="hover:underline">&rarr; Browse 53,000+ Verified Products in Database</a></li>
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
    toolData: { name: 'Food Label Checker' },
    bodyHtml
  });

  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/html');
  res.end(html);
}
