import os
import shutil

BASE_DIR = r"c:\Users\thout\Downloads\check it"

src_confirmed = os.path.join(BASE_DIR, "india_products_confirmed.csv")
src_verification = os.path.join(BASE_DIR, "india_products_needs_verification.csv")

dest_confirmed = os.path.join(BASE_DIR, "verified_products_india.csv")
dest_unverified = os.path.join(BASE_DIR, "unverified_products_india.csv")

# Copy the files to create the dedicated CSV reports
shutil.copy2(src_confirmed, dest_confirmed)
shutil.copy2(src_verification, dest_unverified)

print("Exported verified_products_india.csv successfully.")
print("Exported unverified_products_india.csv successfully.")
