import json
import urllib.request
import pandas as pd

# Load products CSV
print("Loading off_india_clean.csv...")
df = pd.read_csv("off_india_clean.csv", encoding="utf-8", encoding_errors="replace")
df = df.where(pd.notnull(df), None)

print(f"Total products to ingest: {len(df)}")

def escape_str(val):
    if val is None or pd.isna(val) or str(val).lower() == 'nan':
        return "NULL"
    s = str(val).replace("'", "''").replace("\\", "\\\\")
    return f"'{s}'"

def escape_num(val):
    if val is None or pd.isna(val) or str(val).lower() == 'nan':
        return "NULL"
    try:
        f = float(val)
        return str(f)
    except:
        return "NULL"

def escape_int(val):
    if val is None or pd.isna(val) or str(val).lower() == 'nan':
        return "NULL"
    try:
        i = int(float(val))
        return str(i)
    except:
        return "NULL"

cols = [
    "barcode", "product_name", "brands", "categories", "countries_tags",
    "ingredients_text", "additives_tags", "allergens_tags", "nova_group",
    "nutriscore_grade", "energy_100g", "sugars_100g", "fat_100g",
    "saturated_fat_100g", "trans_fat_100g", "protein_100g", "fibre_100g",
    "sodium_100g", "salt_100g"
]

BATCH_SIZE = 500
total = len(df)

for start in range(0, total, BATCH_SIZE):
    end = min(start + BATCH_SIZE, total)
    chunk = df.iloc[start:end]
    
    val_tuples = []
    for _, row in chunk.iterrows():
        b = escape_str(row["barcode"])
        pn = escape_str(row["product_name"])
        br = escape_str(row["brands"])
        cat = escape_str(row["categories"])
        ct = escape_str(row["countries_tags"])
        ing = escape_str(row["ingredients_text"])
        add = escape_str(row["additives_tags"])
        allg = escape_str(row["allergens_tags"])
        nova = escape_int(row["nova_group"])
        nutri = escape_str(row["nutriscore_grade"])
        e = escape_num(row["energy_100g"])
        s = escape_num(row["sugars_100g"])
        f = escape_num(row["fat_100g"])
        sf = escape_num(row["saturated_fat_100g"])
        tf = escape_num(row["trans_fat_100g"])
        p = escape_num(row["protein_100g"])
        fib = escape_num(row["fibre_100g"])
        sod = escape_num(row["sodium_100g"])
        slt = escape_num(row["salt_100g"])
        
        t_str = f"({b}, {pn}, {br}, {cat}, {ct}, {ing}, {add}, {allg}, {nova}, {nutri}, {e}, {s}, {f}, {sf}, {tf}, {p}, {fib}, {sod}, {slt})"
        val_tuples.append(t_str)
        
    sql = f"""
    INSERT INTO public.products ({', '.join(cols)})
    VALUES {',\n'.join(val_tuples)}
    ON CONFLICT (barcode) DO UPDATE SET
        product_name = EXCLUDED.product_name,
        brands = EXCLUDED.brands,
        ingredients_text = EXCLUDED.ingredients_text;
    """
    
    filename = f"batch_products_{start}.sql"
    with open(filename, "w", encoding="utf-8") as f_out:
        f_out.write(sql)
        
print(f"Generated product batch files for all {total} products!")
