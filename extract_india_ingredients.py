import duckdb
import json
import os

def main():
    parquet_path = "food.parquet"
    output_path = "indian_products_ingredients.json"
    
    if not os.path.exists(parquet_path):
        print(f"Error: Local {parquet_path} not found.")
        print("Please ensure the 7.7GB Open Food Facts parquet file is located in the root directory.")
        return
        
    print(f"Connecting to DuckDB and querying local {parquet_path}...")
    conn = duckdb.connect()
    
    # Target Indian products (890 EAN prefix or 'en:india' country tag)
    query = """
        SELECT 
            code AS barcode,
            COALESCE(
                list_filter(product_name, x -> x.lang = 'en')[1].text,
                list_filter(product_name, x -> x.lang = 'main')[1].text,
                product_name[1].text
            ) AS product_name,
            brands AS brand,
            COALESCE(
                list_filter(ingredients_text, x -> x.lang = 'en')[1].text,
                list_filter(ingredients_text, x -> x.lang = 'main')[1].text,
                ingredients_text[1].text,
                ingredients
            ) AS ingredients
        FROM read_parquet('food.parquet')
        WHERE 
            (
                list_contains(countries_tags, 'en:india') 
                OR code LIKE '890%'
            )
            AND product_name IS NOT NULL
            AND ingredients IS NOT NULL;
    """
    
    try:
        df = conn.execute(query).fetchdf()
        
        # Clean null values and format as dictionary records
        df = df.where(df.notnull(), None)
        records = []
        for _, row in df.iterrows():
            # Only include if both product_name and ingredients are valid strings
            p_name = str(row['product_name']).strip() if row['product_name'] else ""
            ings = str(row['ingredients']).strip() if row['ingredients'] else ""
            if p_name and ings:
                records.append({
                    "barcode": str(row['barcode']).strip(),
                    "product_name": p_name,
                    "brand": str(row['brand']).strip() if row['brand'] else "Unknown Brand",
                    "ingredients": ings
                })
                
        print(f"Successfully extracted {len(records)} Indian products.")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(records, f, indent=2, ensure_ascii=False)
            
        print(f"JSON registry generated successfully at: {output_path}")
        
    except Exception as e:
        print("Error extracting ingredients:", e)

if __name__ == "__main__":
    main()
