-- 1. Canonical SKU Family Table
CREATE TABLE IF NOT EXISTS public.canonical_products (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  sku_family_name TEXT NOT NULL,
  brand_name TEXT NOT NULL,
  category_id TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Barcode Alias Mapping Table (Pack & Country Variants)
CREATE TABLE IF NOT EXISTS public.product_barcode_aliases (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  barcode TEXT NOT NULL UNIQUE,
  canonical_product_id UUID NOT NULL REFERENCES public.canonical_products(id) ON DELETE CASCADE,
  variant_name TEXT,
  country_code TEXT DEFAULT 'IN',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_barcode_aliases_barcode ON public.product_barcode_aliases(barcode);

-- 3. Enhanced Data Governance & Provenance Columns on public.products
ALTER TABLE public.products
ADD COLUMN IF NOT EXISTS canonical_product_id UUID REFERENCES public.canonical_products(id),
ADD COLUMN IF NOT EXISTS source_priority INTEGER DEFAULT 1,
ADD COLUMN IF NOT EXISTS last_verified_source TEXT DEFAULT 'OPEN_FOOD_FACTS',
ADD COLUMN IF NOT EXISTS raw_nutriments_json JSONB,
ADD COLUMN IF NOT EXISTS normalized_nutriments_json JSONB,
ADD COLUMN IF NOT EXISTS conversion_rules_json JSONB,
ADD COLUMN IF NOT EXISTS private_draft_allergens JSONB,
ADD COLUMN IF NOT EXISTS reviewed_by UUID REFERENCES auth.users(id),
ADD COLUMN IF NOT EXISTS reviewed_at TIMESTAMPTZ,
ADD COLUMN IF NOT EXISTS reviewed_role TEXT,
ADD COLUMN IF NOT EXISTS review_notes TEXT,
ADD COLUMN IF NOT EXISTS review_source TEXT;

-- 4. Multi-Factor Edge Abuse Control Table
CREATE TABLE IF NOT EXISTS public.edge_abuse_counters (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  identifier_hash TEXT NOT NULL UNIQUE, -- SHA256(user_id + ip + route)
  request_count INTEGER DEFAULT 1,
  window_start TIMESTAMPTZ DEFAULT NOW()
);
