import re

file_path = "c:\\Users\\thout\\Downloads\\check it\\src\\services\\supabaseService.ts"
with open(file_path, "r", encoding="utf-8") as f:
    c = f.read()

new_c = c.replace("productName: toEnglishOnly(p.product_name || 'Unverified Product'),", "productName: toEnglishOnly(p.product_name || ''),")
new_c = new_c.replace("brand: toEnglishOnly(p.brands || 'Unspecified Brand'),", "brand: toEnglishOnly(p.brands || ''),")
new_c = new_c.replace("manufacturer: toEnglishOnly(p.manufacturer || p.brands || 'Unspecified Manufacturer'),", "manufacturer: toEnglishOnly(p.manufacturer || p.brands || ''),")
new_c = new_c.replace("packageSize: p.quantity ? toEnglishOnly(String(p.quantity)) : 'Unspecified Size',", "packageSize: p.quantity ? toEnglishOnly(String(p.quantity)) : '',")
new_c = new_c.replace("category: toEnglishOnly(p.categories || 'Packaged Food & Beverages'),", "category: toEnglishOnly(p.categories || ''),")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(new_c)

print('Done data truth 1')
