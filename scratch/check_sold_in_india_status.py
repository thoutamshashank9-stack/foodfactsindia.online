import pandas as pd

df = pd.read_csv("all_supabase_products.csv", dtype=str)
print("Total rows in master all_supabase_products.csv:", len(df))
print("\nBreakdown by sold_in_india_status:")
print(df['sold_in_india_status'].value_counts(dropna=False))

print("\nBreakdown by GS1 890 Prefix:")
is_890 = df['barcode'].str.startswith('890', na=False)
print("GS1 890 Barcodes (India):", is_890.sum())
print("Non-890 Barcodes (Imported/Foreign):", (~is_890).sum())
