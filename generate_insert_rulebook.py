import pandas as pd

# Load rulebook seed CSV
df = pd.read_csv('additive_rulebook_seed.csv')

def escape_sql_str(val):
    if pd.isna(val) or val is None or str(val).lower() == 'nan':
        return "NULL"
    s = str(val).replace("'", "''")
    return f"'{s}'"

def escape_sql_num(val):
    if pd.isna(val) or val is None or str(val).lower() == 'nan':
        return "NULL"
    return str(val)

values = []
for idx, row in df.iterrows():
    acode = escape_sql_str(row['additive_code'])
    ins = escape_sql_str(row['ins_number'])
    name = escape_sql_str(row['canonical_name'])
    fclass = escape_sql_str(row['functional_class'])
    jur = escape_sql_str(row['jurisdiction'])
    status = escape_sql_str(row['status'])
    mval = escape_sql_num(row['max_level_value'])
    munit = escape_sql_str(row['max_level_unit'])
    lbl = escape_sql_str(row['label_requirement'])
    reg = escape_sql_str(row['regulation_title'])
    src = escape_sql_str(row['source_url'])
    ver = escape_sql_str(row['verification_status'])
    
    val_str = f"({acode}, {ins}, {name}, {fclass}, {jur}, {status}, {mval}, {munit}, {lbl}, {reg}, {src}, {ver})"
    values.append(val_str)

sql = f"""
INSERT INTO public.additive_rulebook (
    additive_code, ins_number, canonical_name, functional_class, 
    jurisdiction, status, max_level_value, max_level_unit, 
    label_requirement, regulation_title, source_url, verification_status
) VALUES 
{',\n'.join(values)}
ON CONFLICT (additive_code, jurisdiction) DO UPDATE SET
    status = EXCLUDED.status,
    canonical_name = EXCLUDED.canonical_name,
    label_requirement = EXCLUDED.label_requirement;
"""

with open('insert_rulebook.sql', 'w', encoding='utf-8') as f:
    f.write(sql)

print("Generated clean insert_rulebook.sql successfully!")
