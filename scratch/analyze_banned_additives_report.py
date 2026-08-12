import os
import sys
import json
import urllib.request
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

SUPABASE_URL = "https://dempjxsrmnzepxbsnwhg.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRlbXBqeHNybW56ZXB4YnNud2hnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODUzMDQ3NzUsImV4cCI6MjEwMDg4MDc3NX0.SO89axui349_3x3zKloLnYD-UGL8vO_p2VR9MCz_xk4"

BASE_DIR = r"c:\Users\thout\Downloads\check it"

def fetch_all_products():
  print("Fetching all products from Supabase REST API...")
  offset = 0
  limit = 1000
  all_rows = []
  
  headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Range": "0-999"
  }
  
  # Use Range header pagination which is fast in PostgREST
  while True:
    headers["Range"] = f"{offset}-{offset + limit - 1}"
    url = f"{SUPABASE_URL}/rest/v1/products?select=barcode,product_name,brands,categories,slug,seo_status,seo_quality_score,ingredients_text,additives_tags,nutriscore_grade,nova_group"
    req = urllib.request.Request(url, headers=headers)
    try:
      with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode('utf-8'))
        if not data:
          break
        all_rows.extend(data)
        print(f"Fetched {len(all_rows)} products...")
        if len(data) < limit:
          break
        offset += limit
    except Exception as e:
      print(f"Error fetching data at offset {offset}: {e}")
      break
      
  return pd.DataFrame(all_rows)

def main():
  df = fetch_all_products()
  print(f"\nTotal records retrieved from database: {len(df)}")
  
  df['ingredients_clean'] = df['ingredients_text'].fillna('').str.strip()
  df['additives_clean'] = df['additives_tags'].fillna('').astype(str).str.lower()
  df['has_ingredients'] = df['ingredients_clean'] != ''
  
  # Banned & Restricted Additives Patterns
  banned_patterns = {
    'Titanium Dioxide (E171 / INS 171 - EU Banned)': r'e171|ins\s*171|titanium\s*dioxide',
    'Tartrazine (INS 102 - EU Warning Label)': r'ins\s*102|tartrazine|e102',
    'Sunset Yellow (INS 110 - EU Warning Label)': r'ins\s*110|sunset\s*yellow|e110',
    'Carmoisine / Azorubine (INS 122 - EU Warning / US Banned)': r'ins\s*122|carmoisine|azorubine|e122',
    'Ponceau 4R (INS 124 - EU Warning / US Banned)': r'ins\s*124|ponceau|e124',
    'Allura Red AC (INS 129 - EU Warning Label)': r'ins\s*129|allura\s*red|e129',
    'Erythrosine (INS 127 - US FDA Food Restricted)': r'ins\s*127|erythrosine|e127|red\s*3',
    'Brominated Vegetable Oil (BVO - Banned US/EU/India)': r'bvo|brominated\s*vegetable\s*oil',
    'Potassium Bromate (Banned EU/India/Canada)': r'potassium\s*bromate',
    'BHA - Butylated Hydroxyanisole (EU/US Restricted)': r'ins\s*320|bha|hydroxyanisole',
    'Cyclamates / INS 952 (US Banned)': r'ins\s*952|cyclamate',
    'Aspartame (INS 951 - IARC Group 2B Carcinogen)': r'ins\s*951|aspartame',
    'MSG / Monosodium Glutamate (INS 621 - Infant Restricted FSSAI)': r'ins\s*621|monosodium\s*glutamate|msg'
  }
  
  df['banned_reasons'] = ""
  banned_counts = {}
  banned_mask = pd.Series(False, index=df.index)
  
  for label, pattern in banned_patterns.items():
    match = df['ingredients_clean'].str.contains(pattern, case=False, regex=True) | df['additives_clean'].str.contains(pattern, case=False, regex=True)
    df.loc[match, 'banned_reasons'] = df.loc[match, 'banned_reasons'].apply(lambda x: x + f"[{label}] " if x else f"[{label}] ")
    banned_mask = banned_mask | match
    banned_counts[label] = match.sum()
    print(f"Products matching '{label}': {match.sum()}")

  df['has_banned_restricted'] = banned_mask
  
  # Metrics breakdown
  total_products = len(df)
  with_ingredients = df['has_ingredients'].sum()
  without_ingredients = total_products - with_ingredients
  verified_indexable = (df['seo_status'] == 'INDEX').sum()
  noindex_shielded = (df['seo_status'] == 'NOINDEX').sum()
  banned_restricted_count = banned_mask.sum()
  
  print("\n" + "="*60)
  print("FULL FOODFACTS INDIA DATABASE AUDIT REPORT")
  print("="*60)
  print(f"Total Products in Database: {total_products}")
  print(f"Products WITH Ingredients: {with_ingredients} ({with_ingredients/total_products*100:.2f}%)")
  print(f"Products WITHOUT Ingredients: {without_ingredients} ({without_ingredients/total_products*100:.2f}%)")
  print(f"Verified Indexable Products (Score >= 80): {verified_indexable} ({verified_indexable/total_products*100:.2f}%)")
  print(f"Noindex Shielded Products (Score < 80): {noindex_shielded} ({noindex_shielded/total_products*100:.2f}%)")
  print(f"Products with Internationally Banned/Restricted Additives: {banned_restricted_count} ({banned_restricted_count/total_products*100:.2f}%)")
  print("="*60)

  # Save CSV Exports
  cols_export = ['barcode', 'product_name', 'brands', 'categories', 'slug', 'seo_status', 'seo_quality_score', 'has_ingredients', 'banned_reasons', 'ingredients_text', 'additives_tags']
  
  df_with = df[df['has_ingredients']][cols_export].copy()
  df_without = df[~df['has_ingredients']][cols_export].copy()
  df_verified = df[df['seo_status'] == 'INDEX'][cols_export].copy()
  df_banned = df[df['has_banned_restricted']][cols_export].copy()
  
  df_with.to_csv(os.path.join(BASE_DIR, "foodfacts_products_with_ingredients.csv"), index=False)
  df_without.to_csv(os.path.join(BASE_DIR, "foodfacts_products_without_ingredients.csv"), index=False)
  df_verified.to_csv(os.path.join(BASE_DIR, "foodfacts_products_verified_indexable.csv"), index=False)
  df_banned.to_csv(os.path.join(BASE_DIR, "foodfacts_products_with_banned_restricted_additives.csv"), index=False)

  # Breakdown CSV
  breakdown_rows = []
  for label, count in banned_counts.items():
    breakdown_rows.append({
      "Additive Category": label,
      "Product Count": count,
      "Percentage of Total Catalog": f"{count/total_products*100:.2f}%" if total_products > 0 else "0%"
    })
  pd.DataFrame(breakdown_rows).to_csv(os.path.join(BASE_DIR, "foodfacts_banned_additives_breakdown.csv"), index=False)

  # Master Summary CSV
  summary_data = [
    {"Metric": "Total Products in Database", "Count": total_products, "Percentage": "100.00%"},
    {"Metric": "Products WITH Declared Ingredients", "Count": with_ingredients, "Percentage": f"{with_ingredients/total_products*100:.2f}%"},
    {"Metric": "Products WITHOUT Declared Ingredients", "Count": without_ingredients, "Percentage": f"{without_ingredients/total_products*100:.2f}%"},
    {"Metric": "Verified Indexable Products (SEO Quality Score >= 80)", "Count": verified_indexable, "Percentage": f"{verified_indexable/total_products*100:.2f}%"},
    {"Metric": "Noindex Shielded Products (SEO Quality Score < 80)", "Count": noindex_shielded, "Percentage": f"{noindex_shielded/total_products*100:.2f}%"},
    {"Metric": "Products Containing Banned or Restricted Additives", "Count": banned_restricted_count, "Percentage": f"{banned_restricted_count/total_products*100:.2f}%"},
  ]
  pd.DataFrame(summary_data).to_csv(os.path.join(BASE_DIR, "foodfacts_master_summary_report.csv"), index=False)
  
  print("\nCSV exports generated successfully in workspace directory!")

if __name__ == "__main__":
  main()
