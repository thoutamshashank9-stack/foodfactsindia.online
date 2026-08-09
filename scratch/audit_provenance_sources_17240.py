import os
import sys
import pandas as pd
import json

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"c:\Users\thout\Downloads\check it"

unverified_csv = os.path.join(BASE_DIR, "india_products_needs_verification.csv")

print("=== PROVENANCE & SOURCE AUDIT FOR 17,240 DOMESTIC INDIAN PRODUCTS ===")

df = pd.read_csv(unverified_csv, dtype=str)
total_count = len(df)

print(f"Total Rows Audited: {total_count}")
print(f"Columns Available: {list(df.columns)}")

# Analyze source indicators across columns
sources_breakdown = {}

# 1. Check if 'source' or 'origin' or 'creator' column exists
if 'source' in df.columns:
    sources_breakdown['by_source_col'] = df['source'].value_counts().to_dict()

# 2. Check image URL domains (e.g. images.openfoodfacts.org, supabase storage, bigbasket, blinkit, etc.)
if 'image_url' in df.columns:
    def extract_domain(url):
        if pd.isna(url) or not str(url).startswith('http'):
            return 'No Image / Local Text Entry'
        url_str = str(url)
        if 'openfoodfacts.org' in url_str: return 'OpenFoodFacts Global Open Database'
        if 'supabase.co' in url_str or 'supabase' in url_str: return 'Supabase Storage / User Scans'
        if 'bigbasket' in url_str: return 'BigBasket Retail Catalog'
        if 'blinkit' in url_str: return 'Blinkit Retail Catalog'
        if 'zepto' in url_str: return 'Zepto Retail Catalog'
        if 'amazon' in url_str: return 'Amazon India Catalog'
        return 'Other Web Image Source'
    
    sources_breakdown['by_image_domain'] = df['image_url'].apply(extract_domain).value_counts().to_dict()

# 3. Barcode GS1 Sub-Allocations (Adani/Aditya Birla, Reliance, Parle, ITC, Britannia, HUL, Nestlé, Dabur, Marico, Haldiram, Amul, Regional Indian FMCGs)
def classify_gs1_allocator(barcode):
    b = str(barcode).strip()
    if not b.startswith('890'): return 'Non-890'
    prefix5 = b[:5]
    prefix6 = b[:6]
    
    # Famous GS1 India Brand Prefixes
    if prefix5 in ['89010', '890103']: return 'Hindustan Unilever (HUL) GS1 Block'
    if prefix5 in ['890106']: return 'Britannia Industries GS1 Block'
    if prefix5 in ['890171', '890176']: return 'Parle Products & Coca-Cola India GS1 Block'
    if prefix5 in ['890172', '890908']: return 'ITC Limited GS1 Block'
    if prefix5 in ['890149']: return 'PepsiCo India GS1 Block'
    if prefix5 in ['890126']: return 'Amul / GCMMF GS1 Block'
    if prefix5 in ['890400', '890406']: return 'Haldiram Snacks GS1 Block'
    if prefix5 in ['890120']: return 'Dabur India GS1 Block'
    if prefix5 in ['890108']: return 'Marico Limited GS1 Block'
    if prefix5 in ['890600', '890601']: return 'Adani Wilmar & Fortune GS1 Block'
    if prefix5 in ['890413', '890608']: return 'Reliance Retail / Campa / Paper Boat GS1 Block'
    if prefix5 in ['890611', '890801', '890609', '890802']: return 'D2C Indian Brands (True Elements, Too Yumm, Zoff, Alpino)'
    return 'Regional Indian FMCG Manufacturers & Distributors'

df['gs1_block'] = df['barcode'].apply(classify_gs1_allocator)
sources_breakdown['by_gs1_manufacturer_block'] = df['gs1_block'].value_counts().to_dict()

# 4. Save audit summary to JSON and print results
report_path = os.path.join(BASE_DIR, "provenance_sources_17240_report.json")
with open(report_path, "w", encoding="utf-8") as f:
    json.dump(sources_breakdown, f, indent=2)

print("\n--- PROVENANCE SOURCE AUDIT RESULTS ---")
print("\n1. Breakdown by Image & Data Provider Domain:")
for k, v in sources_breakdown.get('by_image_domain', {}).items():
    print(f" - {k}: {v} records ({v/total_count*100:.2f}%)")

print("\n2. Breakdown by GS1 India Manufacturer Registration Block:")
for k, v in sources_breakdown.get('by_gs1_manufacturer_block', {}).items():
    print(f" - {k}: {v} records ({v/total_count*100:.2f}%)")

print(f"\nSaved detailed JSON audit report to: {report_path}")
