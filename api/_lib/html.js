import fs from 'fs';
import path from 'path';

export function renderHtmlPage({ title, description, canonicalUrl, ogImage, schema, bodyHtml }) {
  let template = '';
  try {
    const distIndexPath = path.join(process.cwd(), 'dist/index.html');
    const indexPath = path.join(process.cwd(), 'index.html');
    
    if (fs.existsSync(distIndexPath)) {
      template = fs.readFileSync(distIndexPath, 'utf-8');
    } else if (fs.existsSync(indexPath)) {
      template = fs.readFileSync(indexPath, 'utf-8');
    }
  } catch (e) {
    console.error('Failed to read index.html template:', e);
  }

  if (!template) {
    template = `<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>FoodFactsIndia</title>
  </head>
  <body class="bg-[#fcfbf9] text-[#1c2128] font-sans antialiased min-h-screen">
    <div id="root"></div>
  </body>
</html>`;
  }

  // Remove existing title, description, and canonical to avoid duplicates
  template = template.replace(/<title>.*?<\/title>/gi, '');
  template = template.replace(/<meta\s+name="description"\s+content=".*?"\s*\/?>/gi, '');
  template = template.replace(/<link\s+rel="canonical"\s+href=".*?"\s*\/?>/gi, '');

  const headInject = `
    <title>${escapeHtml(title)}</title>
    <meta name="description" content="${escapeHtml(description)}" />
    <link rel="canonical" href="${canonicalUrl}" />
    
    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="website" />
    <meta property="og:title" content="${escapeHtml(title)}" />
    <meta property="og:description" content="${escapeHtml(description)}" />
    <meta property="og:url" content="${canonicalUrl}" />
    <meta property="og:image" content="${ogImage || 'https://www.foodfactsindia.online/og-default.png'}" />

    <!-- Twitter -->
    <meta property="twitter:card" content="summary_large_image" />
    <meta property="twitter:title" content="${escapeHtml(title)}" />
    <meta property="twitter:description" content="${escapeHtml(description)}" />
    <meta property="twitter:image" content="${ogImage || 'https://www.foodfactsindia.online/og-default.png'}" />

    ${schema ? `<script type="application/ld+json">${JSON.stringify(schema)}</script>` : ''}
  `;

  if (template.includes('</head>')) {
    template = template.replace('</head>', `${headInject}\n</head>`);
  } else {
    template = template.replace('<head>', `<head>\n${headInject}`);
  }

  // Inject body html
  if (template.includes('<div id="root"></div>')) {
    template = template.replace('<div id="root"></div>', `<div id="root">${bodyHtml}</div>`);
  } else {
    template = template.replace(/<div id="root">.*?<\/div>/is, `<div id="root">${bodyHtml}</div>`);
  }

  return template;
}

function escapeHtml(unsafe) {
  if (!unsafe) return '';
  return unsafe
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}
