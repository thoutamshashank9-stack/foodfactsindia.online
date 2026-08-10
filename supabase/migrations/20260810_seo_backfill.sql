-- Backfill existing products with slugs and SEO scores
UPDATE public.products
SET
  slug = COALESCE(generate_product_slug(product_name, barcode), 'product-' || barcode),
  seo_quality_score = calculate_seo_quality_score(
    product_name,
    ingredients_text,
    energy_100g,
    brands,
    categories,
    countries_tags,
    barcode,
    nutriscore_grade,
    nova_group,
    image_front_url
  );

-- Set indexing status based on quality score (80 is the threshold for INDEX)
UPDATE public.products
SET seo_status = CASE
  WHEN seo_quality_score >= 80 THEN 'INDEX'
  ELSE 'NOINDEX'
END;
