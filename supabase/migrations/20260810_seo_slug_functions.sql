-- Create slug generation and quality scoring functions
CREATE OR REPLACE FUNCTION public.generate_product_slug(name TEXT, barcode_val TEXT)
RETURNS TEXT LANGUAGE plpgsql AS $$
DECLARE
  base TEXT;
  clean_barcode TEXT;
BEGIN
  -- Lowercase, strip special characters, replace spaces with hyphens
  base := lower(regexp_replace(name, '[^a-zA-Z0-9\s-]', '', 'g'));
  base := regexp_replace(trim(base), '\s+', '-', 'g');
  -- Truncate to safe length
  base := substring(base from 1 for 100);
  
  IF base = '' OR base IS NULL THEN
    base := 'product';
  END IF;

  -- Clean barcode (remove leading/trailing spaces)
  clean_barcode := trim(barcode_val);

  -- Return name slug combined with full barcode to ensure 100% uniqueness and support barcode SEO
  IF clean_barcode IS NOT NULL AND clean_barcode != '' THEN
    RETURN base || '-' || clean_barcode;
  ELSE
    RETURN base || '-' || floor(random() * 1000000)::text;
  END IF;
END $$;

-- Calculate SEO quality score (0 to 100) based on fields populated
CREATE OR REPLACE FUNCTION public.calculate_seo_quality_score(
  product_name TEXT,
  ingredients_text TEXT,
  energy_100g DOUBLE PRECISION,
  brands TEXT,
  categories TEXT,
  countries_tags TEXT,
  barcode TEXT,
  nutriscore_grade TEXT,
  nova_group SMALLINT,
  image_front_url TEXT
)
RETURNS INTEGER LANGUAGE plpgsql AS $$
DECLARE
  score INTEGER := 0;
BEGIN
  -- Identity verified / Name (15 pts)
  IF product_name IS NOT NULL AND length(trim(product_name)) > 2 THEN
    score := score + 15;
  END IF;

  -- Ingredients completeness (20 pts)
  IF ingredients_text IS NOT NULL AND length(trim(ingredients_text)) > 10 THEN
    score := score + 20;
  END IF;

  -- Nutrition complete (15 pts)
  IF energy_100g IS NOT NULL THEN
    score := score + 15;
  END IF;

  -- Brand populated (5 pts)
  IF brands IS NOT NULL AND length(trim(brands)) > 1 THEN
    score := score + 5;
  END IF;

  -- Category populated (5 pts)
  IF categories IS NOT NULL AND length(trim(categories)) > 2 THEN
    score := score + 5;
  END IF;

  -- Indian context (15 pts) - check if it has Indian provenance or FSSAI context
  IF countries_tags ILIKE '%india%' OR countries_tags ILIKE '%en:india%' THEN
    score := score + 15;
  END IF;

  -- Barcode exists (10 pts)
  IF barcode IS NOT NULL AND length(trim(barcode)) >= 8 THEN
    score := score + 10;
  END IF;

  -- Image Front exists (10 pts)
  IF image_front_url IS NOT NULL AND length(trim(image_front_url)) > 10 THEN
    score := score + 10;
  END IF;

  -- NutriScore / Nova group metadata (5 pts)
  IF nutriscore_grade IS NOT NULL OR nova_group IS NOT NULL THEN
    score := score + 5;
  END IF;

  RETURN score;
END $$;
