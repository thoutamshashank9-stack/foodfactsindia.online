import https from 'https';

function validateBarcode(barcode) {
  if (!barcode || typeof barcode !== 'string') return false;
  const clean = barcode.trim();
  return /^[0-9]{8,14}$/.test(clean);
}

export default async function handler(req, res) {
  // 1-Hour Edge Cache TTL for safety and freshness
  const CACHE_HEADERS = 'public, max-age=3600, s-maxage=3600, stale-while-revalidate=7200';

  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');

  if (req.method === 'OPTIONS') {
    res.statusCode = 200;
    res.end();
    return;
  }

  let barcode = (req.query && req.query.barcode) ? req.query.barcode : '';
  if (!barcode && req.url) {
    const parts = req.url.split('?')[0].split('/');
    barcode = parts[parts.length - 1] || '';
  }

  barcode = String(barcode).trim();

  if (!validateBarcode(barcode)) {
    res.statusCode = 400;
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify({ status: 0, error: 'Invalid barcode format. Expected numeric GTIN/EAN string (8-14 digits).' }));
    return;
  }

  const offUrl = `https://world.openfoodfacts.org/api/v2/product/${barcode}.json?fields=product_name,brands,quantity,ingredients_text,nutriments,image_front_url,nova_group,categories`;

  return new Promise((resolve) => {
    const apiReq = https.get(
      offUrl,
      {
        headers: {
          'User-Agent': 'FoodFactsIndiaAI/2.0 (contact@foodfactsindia.online)'
        },
        timeout: 5000
      },
      (apiRes) => {
        let raw = '';
        apiRes.on('data', (chunk) => (raw += chunk));
        apiRes.on('end', () => {
          try {
            res.statusCode = apiRes.statusCode || 200;
            res.setHeader('Content-Type', 'application/json');
            res.setHeader('Cache-Control', CACHE_HEADERS);

            if (apiRes.statusCode === 200) {
              const parsed = JSON.parse(raw);
              res.end(JSON.stringify(parsed));
            } else {
              res.end(JSON.stringify({ status: 0, error: 'Product not found on OFF network' }));
            }
            resolve();
          } catch (e) {
            res.statusCode = 500;
            res.setHeader('Content-Type', 'application/json');
            res.end(JSON.stringify({ status: 0, error: 'Failed to parse Open Food Facts response' }));
            resolve();
          }
        });
      }
    );

    apiReq.on('error', (err) => {
      res.statusCode = 500;
      res.setHeader('Content-Type', 'application/json');
      res.end(JSON.stringify({ status: 0, error: 'Upstream Open Food Facts network error', details: err.message }));
      resolve();
    });

    apiReq.on('timeout', () => {
      apiReq.destroy();
      res.statusCode = 504;
      res.setHeader('Content-Type', 'application/json');
      res.end(JSON.stringify({ status: 0, error: 'Open Food Facts API gateway timeout' }));
      resolve();
    });
  });
}
