import { INGREDIENT_DATABASE } from '../src/data/ingredientsDatabase.js';
import { supabase } from './_lib/supabase.js';

export default async function handler(req, res) {
  res.setHeader('Content-Type', 'application/xml');
  res.setHeader('Cache-Control', 'public, max-age=86400, s-maxage=86400'); // Cache for 24 hours

  const name = req.query.name || '';
  const nowStr = new Date().toISOString().split('T')[0];

  try {
    if (name === 'static.xml') {
      const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://www.foodfactsindia.online/</loc>
    <lastmod>${nowStr}</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://www.foodfactsindia.online/food</loc>
    <lastmod>${nowStr}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://www.foodfactsindia.online/tools/food-label-checker</loc>
    <lastmod>${nowStr}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://www.foodfactsindia.online/guides/how-to-read-food-labels</loc>
    <lastmod>${nowStr}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://www.foodfactsindia.online/guides/what-are-ins-numbers</loc>
    <lastmod>${nowStr}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://www.foodfactsindia.online/tools/ingredient-checker</loc>
    <lastmod>${nowStr}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://www.foodfactsindia.online/guides/how-to-read-ingredients</loc>
    <lastmod>${nowStr}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://www.foodfactsindia.online/guides/food-additives</loc>
    <lastmod>${nowStr}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://www.foodfactsindia.online/tools/food-label-scanner</loc>
    <lastmod>${nowStr}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://www.foodfactsindia.online/guides/how-to-read-nutrition-labels</loc>
    <lastmod>${nowStr}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://www.foodfactsindia.online/fssai/food-labelling</loc>
    <lastmod>${nowStr}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://www.foodfactsindia.online/research/most-common-food-additives-in-india</loc>
    <lastmod>${nowStr}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.9</priority>
  </url>
</urlset>`;
      res.statusCode = 200;
      res.end(xml);
      return;
    }

    if (name === 'products.xml') {
      // Fetch all indexed product slugs (up to 10,000 for this single file sitemap)
      const { data: products, error } = await supabase
        .from('products')
        .select('slug, created_at')
        .eq('seo_status', 'INDEX')
        .order('created_at', { ascending: false })
        .limit(10000);

      if (error) throw error;

      const urls = (products || []).map(p => {
        const date = p.created_at ? p.created_at.split('T')[0] : nowStr;
        return `  <url>
    <loc>https://www.foodfactsindia.online/food/${p.slug}</loc>
    <lastmod>${date}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.7</priority>
  </url>`;
      }).join('\n');

      const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls}
</urlset>`;
      res.statusCode = 200;
      res.end(xml);
      return;
    }

    if (name === 'ingredients.xml') {
      const urls = INGREDIENT_DATABASE.map(ing => {
        const slug = ing.canonicalName.toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9-]/g, '');
        return `  <url>
    <loc>https://www.foodfactsindia.online/ingredient/${slug}</loc>
    <lastmod>${nowStr}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>`;
      }).join('\n');

      const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls}
</urlset>`;
      res.statusCode = 200;
      res.end(xml);
      return;
    }

    if (name === 'additives.xml') {
      // Fetch unique additive codes from rulebook
      const { data: additives, error } = await supabase
        .from('additive_rulebook')
        .select('additive_code');

      if (error) throw error;

      const uniqueCodes = Array.from(new Set((additives || []).map(a => a.additive_code.toUpperCase())));
      
      const urls = uniqueCodes.map(code => {
        // Map to format ins-[code], e.g. ins-621
        const num = code.replace(/^E/, '').toLowerCase();
        const slug = `ins-${num}`;
        return `  <url>
    <loc>https://www.foodfactsindia.online/additive/${slug}</loc>
    <lastmod>${nowStr}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>`;
      }).join('\n');

      const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls}
</urlset>`;
      res.statusCode = 200;
      res.end(xml);
      return;
    }

    // Default 404 for other sitemaps
    res.statusCode = 404;
    res.end('<h1>404 Sitemap Not Found</h1>');
  } catch (err) {
    console.error('Sitemap generation error:', err);
    res.statusCode = 500;
    res.end('<h1>500 Internal Server Error</h1>');
  }
}
