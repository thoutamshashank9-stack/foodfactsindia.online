import re

file_path = "c:\\Users\\thout\\Downloads\\check it\\src\\services\\supabaseService.ts"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update evidenceConfidence computation.
# Search for:
#     evidenceConfidence: {
#       confidenceScore: isDataIncomplete ? 30 : 90,
#       peerReviewedStudiesCount: ingredientsList.reduce((acc, i) => acc + (i.ingredient.citations?.length || 0), 0),
#       regulatoryBodiesCount: globalRegulatoryOverview.filter(r => (r.bannedCount || 0) > 0 || (r.restrictedCount || 0) > 0).length || 1,
#       lastUpdated: 'Live Supabase Sync',
#       verificationStatus: isDataIncomplete ? 'pending_verification' : 'database_indexed'
#     }

old_confidence = """    evidenceConfidence: {
      confidenceScore: isDataIncomplete ? 30 : 90,
      peerReviewedStudiesCount: ingredientsList.reduce((acc, i) => acc + (i.ingredient.citations?.length || 0), 0),
      regulatoryBodiesCount: globalRegulatoryOverview.filter(r => (r.bannedCount || 0) > 0 || (r.restrictedCount || 0) > 0).length || 1,
      lastUpdated: 'Live Supabase Sync',
      verificationStatus: isDataIncomplete ? 'pending_verification' : 'database_indexed'
    }"""

new_confidence = """    evidenceConfidence: {
      confidenceScore: isDataIncomplete ? 30 : 
        (p.energy_100g != null && p.fat_100g != null && p.sugars_100g != null && ingredientsList.length > 0 ? 90 : 60),
      peerReviewedStudiesCount: ingredientsList.reduce((acc, i) => acc + (i.ingredient.citations?.length || 0), 0),
      regulatoryBodiesCount: globalRegulatoryOverview.filter(r => (r.bannedCount || 0) > 0 || (r.restrictedCount || 0) > 0).length,
      lastUpdated: new Date().toISOString().split('T')[0],
      verificationStatus: isDataIncomplete ? 'pending_verification' : 'database_indexed'
    }"""

content = content.replace(old_confidence, new_confidence)


# 2. Update processingNovaClass missing value handling.
# Search for: processingNovaClass: isDataIncomplete ? 0 : (p.nova_group != null ? Number(p.nova_group) : 0)
old_nova = "processingNovaClass: isDataIncomplete ? 0 : (p.nova_group != null ? Number(p.nova_group) : 0)"
new_nova = "processingNovaClass: isDataIncomplete ? undefined : (p.nova_group != null ? Number(p.nova_group) : undefined)"
content = content.replace(old_nova, new_nova)


# 3. Remove getBrandImage completely and its references.
# It is defined as:
# function getBrandImage(brand?: string, name?: string, category?: string): string | undefined {
# ...
# }
getBrandImage_pattern = re.compile(r'function getBrandImage\(.*?\).*?^}', re.MULTILINE | re.DOTALL)
content = getBrandImage_pattern.sub('', content)

# Remove calls to getBrandImage
# imageUrl: p.image_front_url || getBrandImage(p.brands, p.product_name, p.categories),
content = content.replace(
    "imageUrl: p.image_front_url || getBrandImage(p.brands, p.product_name, p.categories),",
    "imageUrl: p.image_front_url || undefined,"
)
content = content.replace(
    "imageFrontUrl: p.image_front_url || getBrandImage(p.brands, p.product_name, p.categories),",
    "imageFrontUrl: p.image_front_url || undefined,"
)

# 4. Remove fake citations year.
# Search for: year: 2026, inside `unrollGroupedAdditives` where citations are created
content = content.replace("year: 2026,", "year: new Date().getFullYear(),")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Data truth fixes applied")
