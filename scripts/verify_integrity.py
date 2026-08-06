#!/usr/bin/env python3
"""Verify database integrity and completeness after migration."""
import json, sys
from pathlib import Path

def main():
    print('Database Integrity Check (Local JSON validation):')
    print('=' * 60)
    data_dir = Path(__file__).parent.parent / 'src' / 'data'
    expected = {
        'fema_gras_verified.json': ('fema_gras_verified', 48),
        'multilingual_aliases_verified.json': ('aliases', 50),
        'commercial_products_verified.json': ('products', 7),
    }
    for fname, (key, expected_count) in expected.items():
        fpath = data_dir / fname
        if fpath.exists():
            data = json.loads(fpath.read_text(encoding='utf-8'))
            count = len(data.get(key, []))
            status = 'PASS' if count == expected_count else 'FAIL'
            print(f'  {status}: {fname} = {count} records (expected {expected_count})')
        else:
            print(f'  MISSING: {fname}')
    print('=' * 60)
    print('Expected DB counts after SQL migration:')
    print('  additive_regulatory_matrix: ~112')
    print('  fop_warning_thresholds: 17')
    print('  ffindia_scoring_engine_v1: 14')
    print('  toxicology_heuristics: 9')
    print('  nutritional_composition: 50')
    print('  commercial_product_master: 7')
    print('  fssai_category_tree: 35-43')
    print('  ingredient_allergen_matrix: ~81')

if __name__ == '__main__':
    main()
