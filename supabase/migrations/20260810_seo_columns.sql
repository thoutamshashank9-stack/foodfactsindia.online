-- Add SEO columns to products table
ALTER TABLE public.products
  ADD COLUMN IF NOT EXISTS slug TEXT,
  ADD COLUMN IF NOT EXISTS seo_status TEXT DEFAULT 'NOINDEX'
    CHECK (seo_status IN ('INDEX', 'NOINDEX', 'REDIRECT', 'GONE')),
  ADD COLUMN IF NOT EXISTS seo_quality_score INTEGER DEFAULT 0;

-- Create indexes for performance
CREATE UNIQUE INDEX IF NOT EXISTS idx_products_slug ON public.products(slug) WHERE slug IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_products_seo_status ON public.products(seo_status);
