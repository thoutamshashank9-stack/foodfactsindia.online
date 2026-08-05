import os
import pandas as pd
import re

def main():
    csv_path = "all_supabase_products.csv"
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found. Please export your Supabase products first.")
        return
        
    print(f"Loading {csv_path} into pandas...")
    df = pd.read_csv(csv_path, dtype={"barcode": str})
    
    # Fill NAs
    df['barcode'] = df['barcode'].fillna('').astype(str).str.strip()
    df['product_name'] = df['product_name'].fillna('').astype(str).str.strip()
    df['brands'] = df['brands'].fillna('').astype(str).str.strip()
    df['ingredients_text'] = df['ingredients_text'].fillna('').astype(str).str.strip()
    
    total_records = len(df)
    
    # 1. Missing Ingredients
    missing_ing_df = df[df['ingredients_text'] == '']
    missing_ing_count = len(missing_ing_df)
    missing_ing_df.to_csv(os.path.join(output_dir, "missing_ingredients.csv"), index=False)
    
    # 2. Duplicate Barcodes
    dup_barcodes_df = df[df.duplicated(subset=['barcode'], keep=False)]
    dup_barcode_count = len(dup_barcodes_df)
    dup_barcodes_df.to_csv(os.path.join(output_dir, "duplicate_barcodes.csv"), index=False)
    
    # 3. Duplicate Product Families (same name and brand under different barcodes)
    # Filter out empty names/brands first
    valid_families = df[(df['product_name'] != '') & (df['brands'] != '')]
    dup_families_df = valid_families[valid_families.duplicated(subset=['product_name', 'brands'], keep=False)]
    dup_families_df = dup_families_df.sort_values(by=['brands', 'product_name'])
    dup_family_count = len(dup_families_df)
    dup_families_df.to_csv(os.path.join(output_dir, "duplicate_families.csv"), index=False)
    
    # 4. Invalid Barcodes (not numeric, or length not between 8 and 14 digits)
    def is_invalid_barcode(b):
        if not b:
            return True
        return not (b.isdigit() and 8 <= len(b) <= 14)
        
    invalid_barcodes_df = df[df['barcode'].apply(is_invalid_barcode)]
    invalid_barcode_count = len(invalid_barcodes_df)
    invalid_barcodes_df.to_csv(os.path.join(output_dir, "invalid_barcodes.csv"), index=False)
    
    # Generate audit summary details
    details_rows = []
    # Save a global details CSV
    df_audit_details = df.copy()
    df_audit_details['has_ingredients'] = df_audit_details['ingredients_text'] != ''
    df_audit_details['is_duplicate_barcode'] = df_audit_details['barcode'].isin(dup_barcodes_df['barcode'])
    df_audit_details['is_duplicate_family'] = df_audit_details.index.isin(dup_families_df.index)
    df_audit_details['is_invalid_barcode'] = df_audit_details['barcode'].isin(invalid_barcodes_df['barcode'])
    df_audit_details.to_csv(os.path.join(output_dir, "barcode_audit_details.csv"), index=False)
    
    # Write Markdown Summary
    summary_path = os.path.join(output_dir, "barcode_audit_summary.md")
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write("# 📊 FoodLens Barcode Dataset Audit Summary Report\n\n")
        f.write(f"This report presents the validation and consistency metrics evaluated on **{total_records:,}** products from the Supabase dataset.\n\n")
        
        f.write("## 📈 Database Completeness & Validation Health\n\n")
        f.write("| Quality Metric | Count | Percentage | Status / Action |\n")
        f.write("| :--- | :--- | :--- | :--- |\n")
        f.write(f"| **Total Products** | {total_records:,} | 100.0% | Master dataset size |\n")
        f.write(f"| **Valid Barcodes** | {total_records - invalid_barcode_count:,} | {(total_records - invalid_barcode_count)/total_records*100:.2f}% | Correct numeric format (8-14 digits) |\n")
        f.write(f"| **Invalid Barcodes** | {invalid_barcode_count:,} | {invalid_barcode_count/total_records*100:.2f}% | Non-numeric or incorrect length | See `invalid_barcodes.csv` |\n")
        f.write(f"| **With Ingredients** | {total_records - missing_ing_count:,} | {(total_records - missing_ing_count)/total_records*100:.2f}% | Complete recipe list for scores |\n")
        f.write(f"| **Missing Ingredients** | {missing_ing_count:,} | {missing_ing_count/total_records*100:.2f}% | Needs OCR/vision fallback or crowdsourcing | See `missing_ingredients.csv` |\n")
        f.write(f"| **Duplicate Barcodes** | {dup_barcode_count:,} | {dup_barcode_count/total_records*100:.2f}% | Identical keys | See `duplicate_barcodes.csv` |\n")
        f.write(f"| **Duplicate Families** | {dup_family_count:,} | {dup_family_count/total_records*100:.2f}% | Same Name + Brand, distinct barcodes | See `duplicate_families.csv` |\n\n")
        
        f.write("## 📂 Generated Audit Artifacts\n\n")
        f.write("- 📊 `output/barcode_audit_details.csv` - Comprehensive validation indicators per row.\n")
        f.write("- 📝 `output/missing_ingredients.csv` - Products without ingredients list.\n")
        f.write("- 👥 `output/duplicate_barcodes.csv` - Redundant barcodes.\n")
        f.write("- 📦 `output/duplicate_families.csv` - Product family packaging variations (cartons, jars, sizes).\n")
        f.write("- ⚠️ `output/invalid_barcodes.csv` - Barcodes failing GTIN formatting check.\n")
        
    print(f"Audit completed successfully! Reports generated in: {output_dir}")

if __name__ == "__main__":
    main()
