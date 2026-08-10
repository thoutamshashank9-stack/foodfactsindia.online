export default function handler(req, res) {
  res.setHeader('Content-Type', 'application/xml');
  res.setHeader('Cache-Control', 'public, max-age=86400, s-maxage=86400'); // Cache for 24 hours

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>https://www.foodfactsindia.online/sitemaps/static.xml</loc>
  </sitemap>
  <sitemap>
    <loc>https://www.foodfactsindia.online/sitemaps/products.xml</loc>
  </sitemap>
  <sitemap>
    <loc>https://www.foodfactsindia.online/sitemaps/ingredients.xml</loc>
  </sitemap>
  <sitemap>
    <loc>https://www.foodfactsindia.online/sitemaps/additives.xml</loc>
  </sitemap>
</sitemapindex>`;

  res.statusCode = 200;
  res.end(xml);
}
