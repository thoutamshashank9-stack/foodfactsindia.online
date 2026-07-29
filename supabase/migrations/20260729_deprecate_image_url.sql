-- ==============================================================================
-- FOODLENS AI MIGRATION: Deprecate Static Database image_url & image_front_url
-- DATE: 2026-07-29
-- OBJECTIVE: Shift all image resolution to Edge Dynamic Proxy (/api/img/[barcode])
-- ==============================================================================

-- 1. Add SQL Comment annotations documenting deprecation
COMMENT ON COLUMN public.products.image_url IS 'DEPRECATED (2026-07-29): Static image storage is deprecated. Product photos are dynamically resolved and edge-cached via /api/img/[barcode].';
COMMENT ON COLUMN public.products.image_front_url IS 'DEPRECATED (2026-07-29): Replaced by Edge Image Proxy (/api/img/[barcode]).';

-- 2. Optional: Null out bloated/broken URLs to reclaim database storage space over wire
-- UPDATE public.products SET image_url = NULL, image_front_url = NULL;

-- 3. Create helper view for lean product querying omitting image URLs
CREATE OR REPLACE VIEW public.vw_products_lean AS
SELECT 
  barcode,
  product_name,
  brands,
  categories,
  nova_group,
  nutriscore_grade,
  energy_100g,
  sugars_100g,
  sodium_100g,
  saturated_fat_100g,
  fiber_100g,
  proteins_100g,
  created_at
FROM public.products;

GRANT SELECT ON public.vw_products_lean TO anon, authenticated, service_role;
