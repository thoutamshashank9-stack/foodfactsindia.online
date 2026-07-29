import glob
import os
import subprocess
import sys
import time
import pandas as pd

# Load generated batch files
files = sorted(glob.glob("batch_products_*.sql"), key=lambda x: int(x.split("_")[2].split(".")[0]))
print(f"Found {len(files)} product batch SQL files to execute...")

# We can execute batches via Python calling the MCP tool wrapper or executing combined SQL
# Let's group files in bundles of 5 (2500 products per MCP execute_sql call)
BUNDLE_SIZE = 5

for i in range(0, len(files), BUNDLE_SIZE):
    bundle = files[i:i+BUNDLE_SIZE]
    combined_sql = ""
    for f_path in bundle:
        with open(f_path, "r", encoding="utf-8") as f:
            combined_sql += f.read() + "\n;"
            
    # Write combined bundle SQL
    bundle_filename = f"combined_bundle_{i}.sql"
    with open(bundle_filename, "w", encoding="utf-8") as bf:
        bf.write(combined_sql)

print("Combined bundle SQL files prepared!")
