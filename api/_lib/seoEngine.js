import { renderHtmlPage } from './html.js';

export function renderSeoPage({
  title,
  description,
  canonicalUrl,
  ogImage = 'https://www.foodfactsindia.online/og-default.png',
  pageType = 'article', // 'article' | 'tool' | 'database' | 'webpage'
  breadcrumbs = [],
  articleData = null,
  toolData = null,
  bodyHtml
}) {
  const schemaList = [];

  // 1. Breadcrumb Schema
  if (breadcrumbs.length > 0) {
    schemaList.push({
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": breadcrumbs.map((b, idx) => ({
        "@type": "ListItem",
        "position": idx + 1,
        "name": b.name,
        "item": b.url.startsWith('http') ? b.url : `https://www.foodfactsindia.online${b.url}`
      }))
    });
  }

  // 2. Page Specific Schema
  if (pageType === 'tool' && toolData) {
    schemaList.push({
      "@context": "https://schema.org",
      "@type": "WebApplication",
      "name": toolData.name || title,
      "url": canonicalUrl,
      "description": description,
      "applicationCategory": "HealthApplication",
      "operatingSystem": "All",
      "offers": {
        "@type": "Offer",
        "price": "0",
        "priceCurrency": "INR"
      }
    });
  } else if (pageType === 'article' && articleData) {
    schemaList.push({
      "@context": "https://schema.org",
      "@type": "Article",
      "headline": title,
      "description": description,
      "image": ogImage,
      "datePublished": articleData.publishedDate || "2026-08-10",
      "dateModified": articleData.modifiedDate || "2026-08-10",
      "author": {
        "@type": "Organization",
        "name": "FoodFacts India Editorial Team",
        "url": "https://www.foodfactsindia.online"
      },
      "publisher": {
        "@type": "Organization",
        "name": "FoodFacts India",
        "url": "https://www.foodfactsindia.online",
        "logo": {
          "@type": "ImageObject",
          "url": "https://www.foodfactsindia.online/og-default.png"
        }
      }
    });
  } else if (pageType === 'database') {
    schemaList.push({
      "@context": "https://schema.org",
      "@type": "WebPage",
      "name": title,
      "description": description,
      "url": canonicalUrl
    });
  }

  return renderHtmlPage({
    title,
    description,
    canonicalUrl,
    ogImage,
    schema: schemaList,
    bodyHtml
  });
}
