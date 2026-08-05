# 📊 FoodLens Barcode Dataset Audit Summary Report

This report presents the validation and consistency metrics evaluated on **62,864** products from the Supabase dataset.

## 📈 Database Completeness & Validation Health

| Quality Metric | Count | Percentage | Status / Action |
| :--- | :--- | :--- | :--- |
| **Total Products** | 62,864 | 100.0% | Master dataset size |
| **Valid Barcodes** | 62,159 | 98.88% | Correct numeric format (8-14 digits) |
| **Invalid Barcodes** | 705 | 1.12% | Non-numeric or incorrect length | See `invalid_barcodes.csv` |
| **With Ingredients** | 38,267 | 60.87% | Complete recipe list for scores |
| **Missing Ingredients** | 24,597 | 39.13% | Needs OCR/vision fallback or crowdsourcing | See `missing_ingredients.csv` |
| **Duplicate Barcodes** | 0 | 0.00% | Identical keys | See `duplicate_barcodes.csv` |
| **Duplicate Families** | 13,117 | 20.87% | Same Name + Brand, distinct barcodes | See `duplicate_families.csv` |

## 📂 Generated Audit Artifacts

- 📊 `output/barcode_audit_details.csv` - Comprehensive validation indicators per row.
- 📝 `output/missing_ingredients.csv` - Products without ingredients list.
- 👥 `output/duplicate_barcodes.csv` - Redundant barcodes.
- 📦 `output/duplicate_families.csv` - Product family packaging variations (cartons, jars, sizes).
- ⚠️ `output/invalid_barcodes.csv` - Barcodes failing GTIN formatting check.
