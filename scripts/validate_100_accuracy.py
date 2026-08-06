#!/usr/bin/env python3
"""Validate that all extracted entries meet 100% accuracy criteria."""
import json, sys
from pathlib import Path

def main():
    data_dir = Path(__file__).parent.parent / 'src' / 'data'
    checks_passed = 0
    checks_total = 0
    # Check FEMA GRAS
    fema_path = data_dir / 'fema_gras_verified.json'
    if fema_path.exists():
        data = json.loads(fema_path.read_text(encoding='utf-8'))
        count = len(data.get('fema_gras_verified', []))
        checks_total += 1
        if count == 48:
            print(f'PASS: FEMA GRAS = {count} entries')
            checks_passed += 1
        else:
            print(f'FAIL: FEMA GRAS = {count} (expected 48)')
    # Check multilingual aliases
    alias_path = data_dir / 'multilingual_aliases_verified.json'
    if alias_path.exists():
        data = json.loads(alias_path.read_text(encoding='utf-8'))
        count = len(data.get('aliases', []))
        checks_total += 1
        if count == 50:
            print(f'PASS: Multilingual aliases = {count} entries')
            checks_passed += 1
        else:
            print(f'FAIL: Multilingual aliases = {count} (expected 50)')
    # Check commercial products
    prod_path = data_dir / 'commercial_products_verified.json'
    if prod_path.exists():
        data = json.loads(prod_path.read_text(encoding='utf-8'))
        count = len(data.get('products', []))
        checks_total += 1
        if count == 7:
            print(f'PASS: Commercial products = {count} entries')
            checks_passed += 1
        else:
            print(f'FAIL: Commercial products = {count} (expected 7)')
    print(f'\nResult: {checks_passed}/{checks_total} checks passed')
    sys.exit(0 if checks_passed == checks_total else 1)

if __name__ == '__main__':
    main()
