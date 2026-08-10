import { renderSeoPage } from '../_lib/seoEngine.js';

export default function handler(req, res) {
  res.setHeader('Cache-Control', 'public, max-age=3600, s-maxage=3600, stale-while-revalidate=7200');

  const title = 'Food Label Scanner | Camera & OCR Ingredient Scanner India';
  const description = 'Scan food label photos or barcodes instantly. Automated OCR ingredient parser detects hidden sugars, artificial colors, trans fats, and FSSAI safety compliance markers.';
  const canonicalUrl = 'https://www.foodfactsindia.online/tools/food-label-scanner';

  const breadcrumbs = [
    { name: 'Home', url: '/' },
    { name: 'Tools', url: '/tools' },
    { name: 'Food Label Scanner', url: '/tools/food-label-scanner' }
  ];

  const bodyHtml = `
    <article class="max-w-4xl mx-auto px-4 py-8 md:py-12" style="font-family: 'Source Serif 4', Georgia, serif;">
      <nav class="text-sm text-gray-500 mb-6 font-sans">
        <a href="/" class="hover:underline text-[#0f5b3a] font-medium">Home</a> &gt; 
        <span class="text-gray-600">Food Label Scanner</span>
      </nav>

      <header class="border-b border-gray-200 pb-6 mb-8 font-sans">
        <span class="inline-block px-3 py-1 bg-amber-50 text-amber-800 text-xs font-semibold rounded-full uppercase tracking-wider mb-3">
          Interactive OCR Tool
        </span>
        <h1 class="text-3xl md:text-5xl font-bold text-gray-900 tracking-tight leading-tight mb-3">
          Food Label Scanner
        </h1>
        <p class="text-lg text-gray-600 max-w-2xl leading-relaxed">
          Snap a photo of any physical food package or label to extract declared ingredients, parse nutrition facts, and check health scores.
        </p>
      </header>

      <section class="bg-white p-6 md:p-8 rounded-2xl border border-gray-100 shadow-md font-sans mb-10 text-center">
        <h2 class="text-xl font-bold text-gray-900 mb-4">Upload or Snap Food Label Photo</h2>
        <div class="border-2 border-dashed border-gray-300 rounded-xl p-8 hover:border-[#0f5b3a] transition-colors cursor-pointer bg-gray-50">
          <div class="text-4xl mb-3">📷</div>
          <p class="text-sm font-semibold text-gray-700">Click to select photo or use device camera</p>
          <p class="text-xs text-gray-500 mt-1">Supports JPG, PNG, WEBP packaging images</p>
        </div>
      </section>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-8 font-sans">
        <section class="bg-white p-6 rounded-xl border border-gray-100 shadow-sm">
          <h3 class="text-lg font-bold text-gray-900 mb-3">Scanner Capabilities</h3>
          <ul class="space-y-2 text-sm text-gray-700">
            <li class="flex items-center gap-2"><span class="text-emerald-600 font-bold">✓</span> <strong>Automated OCR:</strong> Extracts text from curved packaging and foil bags.</li>
            <li class="flex items-center gap-2"><span class="text-emerald-600 font-bold">✓</span> <strong>Barcode Lookup:</strong> Matches Indian EAN-13 barcodes against 53,000+ database records.</li>
          </ul>
        </section>

        <section class="bg-white p-6 rounded-xl border border-gray-100 shadow-sm">
          <h3 class="text-lg font-bold text-gray-900 mb-3">Related Tools</h3>
          <ul class="space-y-2 text-sm text-blue-600 font-medium">
            <li><a href="/tools/food-label-checker" class="hover:underline">&rarr; Text Food Label Checker</a></li>
            <li><a href="/tools/ingredient-checker" class="hover:underline">&rarr; Ingredient Risk Parser</a></li>
            <li><a href="/food" class="hover:underline">&rarr; Food Database Directory</a></li>
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
    toolData: { name: 'Food Label Scanner' },
    bodyHtml
  });

  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/html');
  res.end(html);
}
