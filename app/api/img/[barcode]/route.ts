import { NextResponse } from 'next/server';

function validateBarcode(barcode: string): boolean {
  if (!barcode) return false;
  return /^[0-9]{8,14}$/.test(barcode.trim());
}

function generateSvgFallback(barcode: string): string {
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
  <text x="200" y="310" text-anchor="middle" fill="#94A3B8" font-family="system-ui, -apple-system, sans-serif" font-size="12">FoodFactsIndia AI Edge Proxy</text>
</svg>`;
}

export async function GET(
  request: Request,
  { params }: { params: { barcode: string } }
) {
  const barcode = params.barcode;
  const CACHE_HEADERS = {
    'Cache-Control': 'public, max-age=31536000, s-maxage=31536000, stale-while-revalidate=86400'
  };

  if (!validateBarcode(barcode)) {
    return NextResponse.json(
      { error: 'Invalid barcode format. Expected numeric GTIN/EAN string (8-14 digits).' },
      { status: 400 }
    );
  }

  try {
    const res = await fetch(
      `https://world.openfoodfacts.org/api/v2/product/${barcode}.json?fields=image_front_url,selected_images,code`,
      {
        headers: {
          'User-Agent': 'FoodFactsIndiaAI/2.0 (contact@foodfactsindia.online)'
        },
        next: { revalidate: 86400 }
      }
    );

    if (res.ok) {
      const parsed = await res.json();
      if (parsed && parsed.status === 1 && parsed.product) {
        const p = parsed.product;
        // Strict GTIN verification
        if (String(p.code).trim() === barcode.trim()) {
          const imgUrl = p.image_front_url || p.selected_images?.front?.display?.en || p.selected_images?.front?.display?.fr;
          if (imgUrl && typeof imgUrl === 'string' && imgUrl.startsWith('http')) {
            return NextResponse.redirect(imgUrl, {
              status: 302,
              headers: CACHE_HEADERS
            });
          }
        }
      }
    }
  } catch (e) {
    // Fallthrough to SVG fallback
  }

  const svg = generateSvgFallback(barcode);
  return new Response(svg, {
    status: 200,
    headers: {
      'Content-Type': 'image/svg+xml',
      ...CACHE_HEADERS
    }
  });
}
