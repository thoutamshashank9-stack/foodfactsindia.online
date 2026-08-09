# 📊 Full Database Audit & Legal Verification Report
### Platform: **FoodFactsIndia.online** | Date: **2026-08-09**

---

## 📈 1. EXECUTIVE DATABASE METRICS SUMMARY

| Metric Description | Product Count | Unique Barcodes | Percentage | Output CSV File |
| :--- | :--- | :--- | :--- | :--- |
| **Total Products Collected in Database** | **62,864** | **62,864** | `100.00%` | [`all_supabase_products.csv`](file:///c:/Users/thout/Downloads/check%20it/all_supabase_products.csv) |
| **Products WITH Verified Complete Ingredients** | **38,267** | **38,267** | **`60.87%`** | [`products_with_complete_ingredients.csv`](file:///c:/Users/thout/Downloads/check%20it/products_with_complete_ingredients.csv) |
| **Complete Products Verified Sold in India** | **28,419** | **28,419** | **`45.21%`** | [`complete_data_verified_india_products.csv`](file:///c:/Users/thout/Downloads/check%20it/complete_data_verified_india_products.csv) |
| **Products WITH Incomplete/Missing Ingredients** | **24,597** | **24,597** | **`39.13%`** | [`incomplete_data_barcodes_list.csv`](file:///c:/Users/thout/Downloads/check%20it/incomplete_data_barcodes_list.csv) |
| **Domestic Indian Products with Foreign-Banned Additives** | **285** | **`261`** | **`100% GS1 890`** | [`banned_additives_india_vs_global_report.csv`](file:///c:/Users/thout/Downloads/check%20it/banned_additives_india_vs_global_report.csv) |

---

## 🧪 2. PRODUCTS CONTAINING ADDITIVES LEGAL IN INDIA BUT BANNED/RESTRICTED ABROAD

All **285 entries (261 unique GS1 `890` Indian domestic barcodes)** are 100% verified domestic Indian products. They contain additives permitted under FSSAI category limits in India, but banned or restricted in foreign jurisdictions (EU, UK, US, Japan):

| Flagged Additive / Ingredient | Indian Entries Count | Unique Barcodes | Global Regulation Status | Top Indian Brands Using Additive |
| :--- | :--- | :--- | :--- | :--- |
| **TBHQ (E319)** | **118** | **105** | ❌ **Not Approved in Japan**; Permitted under FSSAI (200ppm limit) | Fortune, Saffola, Sundrop, Emami, Dabur, Priya, Nissin, Maggi, Dr. Oetker, Veeba, ACT II, Lay's, Patanjali |
| **Carmoisine / Azorubine (E122)** | **95** | **82** | ❌ **Not Approved in Japan / US**; Permitted under FSSAI | Bovonto, Britannia Bourbon, Britannia Jim Jam, Kissan, Mapro, Campa, Paper Boat, Weikfield, Amul |
| **Ponceau 4R (E124)** | **36** | **22** | ❌ **Not Approved in Japan / US**; Permitted under FSSAI | Britannia, Vadilal, Amul, Havmor, Paper Boat, B Natural |
| **Erythrosine (E127)** | **19** | **19** | ⚠️ **Restricted in EU / FDA phaseout**; Permitted under FSSAI | Amul, Britannia, Kwality Wall's, Havmor, Mother Dairy |
| **Titanium Dioxide (E171)** | **8** | **7** | ❌ **BANNED in EU (2022)**; Permitted under FSSAI | ITC B Natural, Britannia, Girnar, Hostess |
| **Fast Green FCF (E143)** | **4** | **3** | ❌ **Not Authorized in EU / UK**; Permitted under FSSAI | Kwality Wall's, Winkies |
| **Partially Hydrogenated Oils (PHO)** | **4** | **4** | ❌ **BANNED in US & Canada**; FSSAI limits TFA ≤2% | Priya, Sunny |
| **Green S (E142)** | **1** | **1** | ⚠️ **Restricted under FSSAI category limits** | Nafees Cream Roll |

---

## 📋 3. INCOMPLETE DATA BARCODES & PRODUCTS

* **Total Barcodes with Incomplete Data:** **24,597 barcodes** (missing ingredients text or incomplete label scans).
* **Dedicated Export CSV List:** [`incomplete_data_barcodes_list.csv`](file:///c:/Users/thout/Downloads/check%20it/incomplete_data_barcodes_list.csv)
* **Status:** Queued for crowd-sourced label updates via the **"Report a Label Update"** safe harbor button on `foodfactsindia.online`.
