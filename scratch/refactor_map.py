import re
import sys

file_path = "c:\\Users\\thout\\Downloads\\check it\\src\\services\\supabaseService.ts"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# I need to refactor mapProductToReport into a mapProductToReportWithData function
# and then create batchMapProductsToReports
# and change mapProductToReport to call batchMapProductsToReports with a single element.
# Or, keep mapProductToReport for backwards compatibility (and it just fetches for one element or calls batchMapProductsToReports).

# First, replace `export async function mapProductToReport(p: any): Promise<TransparencyReport> {`
# to `export async function mapProductToReportWithData(p: any, dbIngredients: any[], dbAdditives: any[], dbCatLimits: any[], rulebookData: any[]): Promise<TransparencyReport> {`

new_content = content.replace(
    "export async function mapProductToReport(p: any): Promise<TransparencyReport> {",
    "export async function mapProductToReportWithData(p: any, dbIngredients: any[], dbAdditives: any[], dbCatLimits: any[], rulebookData: any[]): Promise<TransparencyReport> {"
)

# Then we remove the fetching part inside mapProductToReportWithData
fetch_block_start = new_content.find("const fssaiCatCode = getFssaiCategoryCode(p.categories || p.category || '');")
fetch_block_end = new_content.find("const nutrition: NutritionFacts = {", fetch_block_start)

if fetch_block_start == -1 or fetch_block_end == -1:
    print("Could not find fetch block")
    sys.exit(1)

# We want to keep `const fssaiCatCode`? Actually no, `fssaiCatCode` is not needed if `dbCatLimits` is already filtered, but wait, `fssaiCatCode` is used in `pCatLimits` filtering in the caller. No, it's used inside `mapProductToReportWithData` anywhere?
# Let's see if fssaiCatCode is used inside the function after the fetch block.

# Looking at supabaseService.ts:
# fssaiCatCode is used for fetching, then not used again.
# Wait, let's keep fssaiCatCode in case it's used, or let's remove the fetch block.

fetch_block = new_content[fetch_block_start:fetch_block_end]

replacement = """  const additiveCodes = (dbAdditives || []).map((a: any) => a.additive_code.toUpperCase());

"""

new_content = new_content.replace(fetch_block, replacement)

# Now inject the new batchMapProductsToReports and the new mapProductToReport wrapper before mapProductToReportWithData

new_functions = """
export async function batchMapProductsToReports(products: any[]): Promise<TransparencyReport[]> {
  if (products.length === 0) return [];
  
  const uncachedProducts = products.filter(p => !reportCache.has(String(p.barcode)));
  const uncachedBarcodes = uncachedProducts.map(p => String(p.barcode));
  
  if (uncachedBarcodes.length === 0) {
    return products.map(p => reportCache.get(String(p.barcode))!);
  }

  // 1. Fetch ingredients and additives for all uncached products
  const [{ data: dbIngredients }, { data: dbAdditives }] = await Promise.all([
    supabase
      .from('product_ingredients')
      .select('barcode, ingredient_raw, position')
      .in('barcode', uncachedBarcodes)
      .order('position', { ascending: true }),
    supabase
      .from('product_additives')
      .select('barcode, additive_code')
      .in('barcode', uncachedBarcodes)
  ]);

  const ingredientsByBarcode = new Map<string, any[]>();
  const additivesByBarcode = new Map<string, any[]>();
  
  dbIngredients?.forEach(ing => {
    if (!ingredientsByBarcode.has(ing.barcode)) ingredientsByBarcode.set(ing.barcode, []);
    ingredientsByBarcode.get(ing.barcode)!.push(ing);
  });
  
  const allAdditiveCodesSet = new Set<string>();
  dbAdditives?.forEach(add => {
    if (!additivesByBarcode.has(add.barcode)) additivesByBarcode.set(add.barcode, []);
    additivesByBarcode.get(add.barcode)!.push(add);
    allAdditiveCodesSet.add(add.additive_code.toUpperCase());
  });

  // 2. Fetch category limits
  const fssaiCategories = Array.from(new Set(uncachedProducts.map(p => getFssaiCategoryCode(p.categories || p.category || '')).filter(Boolean))) as string[];
  let allCatLimits: any[] = [];
  if (fssaiCategories.length > 0) {
    const { data: catLimits } = await supabase.from('fssai_category_limits').select('*').in('category_code', fssaiCategories);
    allCatLimits = catLimits || [];
  }

  // 3. Fetch additive rulebook
  let rulebookData: any[] = [];
  if (allAdditiveCodesSet.size > 0) {
    const { data: rules } = await supabase
      .from('additive_rulebook')
      .select('*')
      .in('additive_code', Array.from(allAdditiveCodesSet));
    rulebookData = rules || [];
  }

  // 4. Pre-fetch unknown INS codes for all ingredients
  const allInsCodes: string[] = [];
  dbIngredients?.forEach((ing: any) => {
    const raw = cleanRawIngredientText(ing.ingredient_raw || '');
    const codeMatches = Array.from(raw.matchAll(/([0-9]{3,4}(?:\\\\([a-z0-9]+\\\\))?)/gi)).map(m => m[1]);
    if (/annatto/i.test(raw)) codeMatches.push('160b');
    if (/caramel/i.test(raw)) codeMatches.push('150d');
    if (/metabisulfite/i.test(raw)) codeMatches.push('223');
    if (/lecithin/i.test(raw)) codeMatches.push('322');
    if (/msg|glutamate/i.test(raw)) codeMatches.push('621');
    allInsCodes.push(...codeMatches);
  });

  const uniqueInsCodes = Array.from(new Set(allInsCodes.map(normalizeInsCode))).filter(Boolean);
  const uncachedCodes = uniqueInsCodes.filter(code => !additiveCache.has(code));

  if (uncachedCodes.length > 0) {
    const { data: refData } = await supabase
      .from('additive_reference')
      .select('*')
      .in('ins_code', uncachedCodes);

    refData?.forEach((row: any) => {
      const fact: AdditiveFact = {
        ins_code: row.ins_code,
        common_name: row.common_name,
        origin: row.origin,
        category: row.category,
        fssai_status: row.fssai_status,
        efsa_status: row.efsa_status,
        fda_status: row.fda_status,
        adi_value: row.adi_value,
        concern_level: row.concern_level,
        accurate_description: row.accurate_description,
        caveat: row.caveat,
        source_url: row.source_url,
        source_citation: row.source_citation
      };
      additiveCache.set(row.ins_code, fact);
    });
  }

  // 5. Build reports synchronously
  const results = await Promise.all(products.map(async (p) => {
    const barcode = String(p.barcode);
    if (reportCache.has(barcode)) {
      return reportCache.get(barcode)!;
    }

    const fssaiCatCode = getFssaiCategoryCode(p.categories || p.category || '');
    const pIngredients = ingredientsByBarcode.get(barcode) || [];
    const pAdditives = additivesByBarcode.get(barcode) || [];
    const pCatLimits = allCatLimits.filter(cl => cl.category_code === fssaiCatCode);
    
    return mapProductToReportWithData(p, pIngredients, pAdditives, pCatLimits, rulebookData);
  }));

  return results;
}

export async function mapProductToReport(p: any): Promise<TransparencyReport> {
  const reports = await batchMapProductsToReports([p]);
  return reports[0];
}

"""

new_content = new_content.replace(
    "export async function mapProductToReportWithData(",
    new_functions + "export async function mapProductToReportWithData("
)

# And I need to update `searchLiveProducts` to use batchMapProductsToReports instead of Promise.all(mapProductToReport)
search_target = "const reports = await Promise.all(validFoodProducts.map(async (p) => mapProductToReport(p)));"
search_replacement = "const reports = await batchMapProductsToReports(validFoodProducts);"
new_content = new_content.replace(search_target, search_replacement)

# And I need to update `fetchLiveCatalog`
catalog_target = """  const reports: TransparencyReport[] = await Promise.all(
    products.map(async (p) => mapProductToReport(p))
  );"""
catalog_replacement = "  const reports = await batchMapProductsToReports(products);"
new_content = new_content.replace(catalog_target, catalog_replacement)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print("Done refactoring supabaseService.ts")
