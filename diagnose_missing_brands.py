import duckdb

conn = duckdb.connect()

print("Analyzing Red Bull & Bambino filter conditions in food.parquet...\n")

query = """
SELECT 
    code AS barcode,
    COALESCE(
        list_filter(product_name, x -> x.lang = 'en')[1].text,
        list_filter(product_name, x -> x.lang = 'main')[1].text,
        product_name[1].text
    ) AS product_name_str,
    brands,
    countries_tags,
    (list_contains(countries_tags, 'en:india') OR code LIKE '890%') AS matched_india_filter,
    (
        COALESCE(
            list_filter(ingredients_text, x -> x.lang = 'en')[1].text,
            list_filter(ingredients_text, x -> x.lang = 'main')[1].text,
            ingredients_text[1].text,
            ingredients
        ) IS NOT NULL
    ) AS has_ingredients
FROM read_parquet('food.parquet')
WHERE 
    lower(brands) LIKE '%red bull%' 
    OR lower(brands) LIKE '%bambino%'
    OR lower(product_name[1].text) LIKE '%red bull%'
    OR lower(product_name[1].text) LIKE '%bambino%'
LIMIT 30;
"""

df = conn.execute(query).fetchdf()

for idx, row in df.iterrows():
    name = str(row['product_name_str']).encode('ascii', 'replace').decode('ascii')
    brand = str(row['brands']).encode('ascii', 'replace').decode('ascii')
    code = row['barcode']
    ctags = row['countries_tags']
    india_match = row['matched_india_filter']
    has_ing = row['has_ingredients']
    print(f"Barcode: {code} | Brand: {brand} | Name: {name}")
    print(f"   Countries: {ctags} | India Match: {india_match} | Has Ingredients: {has_ing}")
    print("-" * 75)
