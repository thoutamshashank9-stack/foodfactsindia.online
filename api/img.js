import https from 'https';

function validateBarcode(barcode) {
  if (!barcode || typeof barcode !== 'string') return false;
  const clean = barcode.trim();
  return /^[0-9]{8,14}$/.test(clean);
}

function generateSvgFallback(barcode) {
  return `<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400" viewBox="0 0 400 400" fill="none">
  <rect width="400" height="400" rx="32" fill="#F8FAFC"/>
  <rect x="40" y="40" width="320" height="320" rx="24" fill="#F1F5F9" stroke="#E2E8F0" stroke-width="2"/>
  <g transform="translate(140, 110)">
    <rect x="0" y="0" width="8" height="80" fill="#64748B" rx="2"/>
    <rect x="14" y="0" width="4" height="80" fill="#64748B" rx="2"/>
    <rect x="24" y="0" width="12" height="80" fill="#64748B" rx="2"/>
    <rect x="42" y="0" width="6" height="80" fill="#64748B" rx="2"/>
    <rect x="54" y="0" width="16" height="80" fill="#64748B" rx="2"/>
    <rect x="76" y="0" width="4" height="80" fill="#64748B" rx="2"/>
    <rect x="86" y="0" width="10" height="80" fill="#64748B" rx="2"/>
    <rect x="102" y="0" width="8" height="80" fill="#64748B" rx="2"/>
    <rect x="116" y="0" width="4" height="80" fill="#64748B" rx="2"/>
  </g>
  <text x="200" y="240" text-anchor="middle" fill="#334155" font-family="system-ui, -apple-system, sans-serif" font-size="20" font-weight="700">No Package Photo</text>
  <text x="200" y="270" text-anchor="middle" fill="#64748B" font-family="ui-monospace, SFMono-Regular, monospace" font-size="14" font-weight="600">GTIN: ${barcode}</text>
  <text x="200" y="310" text-anchor="middle" fill="#94A3B8" font-family="system-ui, -apple-system, sans-serif" font-size="12">FoodLens AI Edge Proxy</text>
</svg>`;
}

async function fetchUpstreamOffImage(barcode) {
  const url = `https://world.openfoodfacts.org/api/v2/product/${barcode}.json?fields=image_front_url,selected_images,code`;
  return new Promise((resolve) => {
    const req = https.get(
      url,
      {
        headers: {
          'User-Agent': 'FoodLensAI/2.0 (contact@foodlens.ai)'
        },
        timeout: 4000
      },
      (res) => {
        let raw = '';
        res.on('data', (chunk) => (raw += chunk));
        res.on('end', () => {
          try {
            if (res.statusCode !== 200) return resolve(null);
            const parsed = JSON.parse(raw);
            if (!parsed || parsed.status !== 1 || !parsed.product) return resolve(null);

            const p = parsed.product;
            if (String(p.code).trim() !== String(barcode).trim()) return resolve(null);

            const imgUrl = p.image_front_url || p.selected_images?.front?.display?.en || p.selected_images?.front?.display?.fr;
            if (imgUrl && typeof imgUrl === 'string' && imgUrl.startsWith('http')) {
              return resolve(imgUrl);
            }
            resolve(null);
          } catch (e) {
            resolve(null);
          }
        });
      }
    );
    req.on('error', () => resolve(null));
    req.on('timeout', () => {
      req.destroy();
      resolve(null);
    });
  });
}

export default async function handler(req, res) {
  const CACHE_HEADERS = 'public, max-age=31536000, s-maxage=31536000, stale-while-revalidate=86400';

  let barcode = (req.query && req.query.barcode) ? req.query.barcode : '';
  if (!barcode && req.url) {
    const parts = req.url.split('?')[0].split('/');
    barcode = parts[parts.length - 1] || '';
  }

  barcode = String(barcode).trim();

  if (!validateBarcode(barcode)) {
    res.statusCode = 400;
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify({ error: 'Invalid barcode format. Expected numeric GTIN/EAN string (8-14 digits).' }));
    return;
  }

  const imageUrl = await fetchUpstreamOffImage(barcode);

  if (imageUrl) {
    res.statusCode = 302;
    res.setHeader('Location', imageUrl);
    res.setHeader('Cache-Control', CACHE_HEADERS);
    res.end();
    return;
  }

  const svg = generateSvgFallback(barcode);
  res.statusCode = 200;
  res.setHeader('Content-Type', 'image/svg+xml');
  res.setHeader('Cache-Control', CACHE_HEADERS);
  res.end(svg);
}
