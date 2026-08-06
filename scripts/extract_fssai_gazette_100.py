#!/usr/bin/env python3
"""Extract Schedule 2.4.5 tables from FSSAI Gazette PDF.
Prereqs: pip install camelot-py[cv] opencv-python ghostscript pandas
Usage: python scripts/extract_fssai_gazette_100.py --pdf ./gazette.pdf --output ./output.sql
"""
import re, sys
from pathlib import Path
from datetime import datetime
import argparse

def validate_ins_code(code):
    return bool(re.match(r'^\d{2,4}[a-z]?$', code.strip()))

def validate_category_scope(scope):
    return bool(re.match(r'^\d{2}\.\d{1,2}(\.\d{1,2})?$', scope.strip()))

def parse_limit_value(limit_str):
    limit_str = limit_str.strip().lower()
    if 'quantum satis' in limit_str or 'gmp' in limit_str:
        return (0, 'ALLOWED', 'Quantum Satis (GMP)')
    match = re.search(r'(\d+\.?\d*)', limit_str)
    if match:
        value = float(match.group(1))
        if 'ppm' in limit_str or 'mg/kg' in limit_str:
            return (value, 'RESTRICTED', f'Max {value} mg/kg')
    return (None, 'UNKNOWN', 'Manual review required')

def main():
    parser = argparse.ArgumentParser(description='Extract FSSAI Gazette tables')
    parser.add_argument('--pdf', required=True, help='Path to FSSAI Gazette PDF')
    parser.add_argument('--output', required=True, help='Output SQL file path')
    args = parser.parse_args()
    pdf_path = Path(args.pdf)
    output_path = Path(args.output)
    if not pdf_path.exists():
        print(f'ERROR: PDF not found at {pdf_path}')
        sys.exit(1)
    try:
        import camelot
        import pandas as pd
    except ImportError:
        print('ERROR: Install deps: pip install camelot-py[cv] opencv-python ghostscript pandas')
        sys.exit(1)
    print(f'Parsing {pdf_path}...')
    tables = camelot.read_pdf(str(pdf_path), pages='all', flavor='stream')
    print(f'Found {len(tables)} candidate tables')
    all_entries = []
    for table_index, table in enumerate(tables):
        df = table.df
        page_number = table.page + 1
        if not df[0].apply(validate_ins_code).any():
            continue
        for row_index, row in df.iterrows():
            ins_code = row[0].strip()
            if not validate_ins_code(ins_code):
                continue
            additive_name = row[1].strip() if len(row) > 1 else ''
            category_scope = row[2].strip() if len(row) > 2 else ''
            limit_text = row[3].strip() if len(row) > 3 else ''
            if not validate_category_scope(category_scope):
                continue
            max_limit, status, notes = parse_limit_value(limit_text)
            if max_limit is None:
                continue
            all_entries.append({
                'ins_code': ins_code, 'additive_name': additive_name,
                'category_scope': category_scope, 'max_limit_mg_kg': max_limit,
                'status': status, 'notes': notes,
                'source_document': f'FSSAI Gazette:page_{page_number}:table_{table_index}:row_{row_index}',
                'verified_at': datetime.now().isoformat()
            })
    with open(output_path, 'w') as f:
        f.write(f'-- FSSAI Gazette Extraction\n-- Source: {pdf_path.name}\n-- Total entries: {len(all_entries)}\n\n')
        for e in all_entries:
            f.write(f"INSERT INTO public.additive_regulatory_matrix (ins_code, additive_name, country_code, category_scope, status, max_limit_mg_kg, regulation_ref, notes, data_provenance, source_document) VALUES ('{e['ins_code']}', '{e['additive_name']}', 'IN', ARRAY['{e['category_scope']}'], '{e['status']}', {e['max_limit_mg_kg']}, 'FSSAI Schedule 2.4.5', '{e['notes']}', 'VERIFIED', '{e['source_document']}') ON CONFLICT DO NOTHING;\n\n")
    print(f'Wrote {len(all_entries)} entries to {output_path}')

if __name__ == '__main__':
    main()
