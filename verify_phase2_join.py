"""
Phase 2 Verification Script
Tests the SQL join between products, product_additives, and additive_rulebook_seed.csv
Demonstrates how products are enriched with regulatory status and warnings.
"""

import duckdb
import pandas as pd

def test_phase2_join():
    conn = duckdb.connect()
    
    # Load CSV files into DuckDB memory tables
    conn.execute("CREATE TABLE products AS SELECT * FROM read_csv_auto('off_india_clean.csv')")
    conn.execute("CREATE TABLE product_additives AS SELECT * FROM read_csv_auto('product_additives.csv')")
    conn.execute("CREATE TABLE additive_rulebook AS SELECT * FROM read_csv_auto('additive_rulebook_seed.csv')")
    
    print("Executing Phase 2 Regulatory Join Query across India products...\n")
    
    query = """
    SELECT 
        p.barcode,
        p.product_name,
        p.brands,
        pa.additive_code,
        COALESCE(r.canonical_name, 'Unknown Additive') AS canonical_name,
        COALESCE(r.jurisdiction, 'IN') AS jurisdiction,
        COALESCE(r.status, 'not_yet_verified') AS regulatory_status,
        r.label_requirement,
        r.source_url
    FROM products p
    JOIN product_additives pa ON pa.barcode = p.barcode
    LEFT JOIN additive_rulebook r 
        ON r.additive_code = pa.additive_code 
        AND r.jurisdiction = 'IN'
    LIMIT 15;
    """
    
    df_result = conn.execute(query).fetchdf()
    print("Sample Output (Products joined with FSSAI Regulatory Status):")
    print(df_result.to_string(index=False))
    
    # Check coverage of verified vs unverified additives in dataset
    coverage_query = """
    SELECT 
        COALESCE(r.status, 'not_yet_verified') AS status,
        COUNT(DISTINCT pa.barcode) AS product_count,
        COUNT(*) AS total_additive_occurrences
    FROM product_additives pa
    LEFT JOIN additive_rulebook r 
        ON r.additive_code = pa.additive_code 
        AND r.jurisdiction = 'IN'
    GROUP BY COALESCE(r.status, 'not_yet_verified')
    ORDER BY total_additive_occurrences DESC;
    """
    
    df_coverage = conn.execute(coverage_query).fetchdf()
    print("\n--- Regulatory Rulebook Coverage Metrics (India Market) ---")
    print(df_coverage.to_string(index=False))

if __name__ == '__main__':
    test_phase2_join()
