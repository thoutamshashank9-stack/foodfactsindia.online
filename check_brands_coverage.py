import duckdb

conn = duckdb.connect()

print("Searching ALL Bambino products in food.parquet...\n")

query_bambino = """
SELECT 
    code AS barcode,
    COALESCE(
        list_filter(product_name, x -> x.lang = 'en')[1].text,
        list_filter(product_name, x -> x.lang = 'main')[1].text,
        product_name[1].text
    ) AS product_name_str,
    brands,
    countries_tags,
    (list_contains(countries_tags, 'en:india') OR code LIKE '890%') AS in_current_filter
FROM read_parquet('food.parquet')
WHERE lower(brands) LIKE '%bambino%' OR lower(product_name[1].text) LIKE '%bambino%';
"""

df_b = conn.execute(query_bambino).fetchdf()
print(f"Total Bambino products in OFF dataset: {len(df_b)}")
for idx, row in df_b.iterrows():
    name = str(row['product_name_str']).encode('ascii', 'replace').decode('ascii')
    brand = str(row['brands']).encode('ascii', 'replace').decode('ascii')
    code = row['barcode']
    ctags = row['countries_tags']
    in_filter = row['in_current_filter']
    print(f"  Barcode: {code} | Brand: {brand} | Name: {name} | Countries: {ctags} | In Filter: {in_filter}")

print("\nSearching Global FMCG Brands sold in India (Red Bull, Nutella, Ferrero, Pringles, Lays, Cadbury, Amul)...")

query_global = """
SELECT 
    brands,
    COUNT(*) as total_count,
    COUNT(CASE WHEN list_contains(countries_tags, 'en:india') OR code LIKE '890%' THEN 1 END) as matched_in_filter
FROM read_parquet('food.parquet')
WHERE lower(brands) IN ('red bull', 'bambino', 'amul', 'cadbury', 'nestle', 'britannia', 'parle', 'haldiram''s', 'lays', 'doritos', 'nutella', 'pringles', 'coca-cola', 'pepsi')
GROUP BY brands
ORDER BY total_count DESC;
"""

df_g = conn.execute(query_global).fetchdf()
print("\nBrand Breakdown in OFF Dataset:")
print(df_g.to_string(index=False))
