-- 15-food-category matrix for FSSAI Schedule 2.4.5
CREATE TABLE IF NOT EXISTS fssai_category_limits (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    category_code TEXT NOT NULL,                -- e.g. 'CAT_01', 'CAT_14'
    category_name TEXT NOT NULL,
    additive_code TEXT NOT NULL,                -- e.g. '102', '122', '211', '924a'
    status TEXT NOT NULL,                       -- 'BANNED', 'RESTRICTED', 'APPROVED'
    max_limit_mg_kg NUMERIC,                    -- NULL if BANNED, value if RESTRICTED
    regulation_ref TEXT NOT NULL,               -- e.g. 'FSSAI Schedule 2.4.5'
    restriction_details TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT unique_category_additive UNIQUE (category_code, additive_code)
);

CREATE INDEX IF NOT EXISTS idx_fssai_category_limits_lookup ON fssai_category_limits (category_code, additive_code);

-- Seed FSSAI Category-Specific Matrix (Schedule 2.4.5)
-- CAT_01: Dairy products & analogues (0 mg/kg synthetic dyes & preservatives)
INSERT INTO fssai_category_limits (category_code, category_name, additive_code, status, max_limit_mg_kg, regulation_ref, restriction_details) VALUES
('CAT_01', 'Dairy products & analogues', '102', 'BANNED', 0, 'FSSAI Schedule 2.4.5', 'Synthetic colors prohibited in milk, cream, and plain dairy.'),
('CAT_01', 'Dairy products & analogues', '110', 'BANNED', 0, 'FSSAI Schedule 2.4.5', 'Synthetic colors prohibited in milk, cream, and plain dairy.'),
('CAT_01', 'Dairy products & analogues', '122', 'BANNED', 0, 'FSSAI Schedule 2.4.5', 'Synthetic colors prohibited in milk, cream, and plain dairy.'),
('CAT_01', 'Dairy products & analogues', '133', 'BANNED', 0, 'FSSAI Schedule 2.4.5', 'Synthetic colors prohibited in milk, cream, and plain dairy.'),
('CAT_01', 'Dairy products & analogues', '211', 'BANNED', 0, 'FSSAI Schedule 2.4.5', 'Chemical preservatives prohibited in plain dairy products.'),
('CAT_01', 'Dairy products & analogues', '202', 'BANNED', 0, 'FSSAI Schedule 2.4.5', 'Chemical preservatives prohibited in plain dairy products.');

-- CAT_05: Confectionery & Chocolates (Max 100 mg/kg synthetic colors)
INSERT INTO fssai_category_limits (category_code, category_name, additive_code, status, max_limit_mg_kg, regulation_ref, restriction_details) VALUES
('CAT_05', 'Confectionery', '102', 'RESTRICTED', 100, 'FSSAI Schedule 2.4.5', 'Max limit 100 mg/kg for synthetic colors.'),
('CAT_05', 'Confectionery', '110', 'RESTRICTED', 100, 'FSSAI Schedule 2.4.5', 'Max limit 100 mg/kg for synthetic colors.'),
('CAT_05', 'Confectionery', '122', 'RESTRICTED', 100, 'FSSAI Schedule 2.4.5', 'Max limit 100 mg/kg for synthetic colors.'),
('CAT_05', 'Confectionery', '133', 'RESTRICTED', 100, 'FSSAI Schedule 2.4.5', 'Max limit 100 mg/kg for synthetic colors.'),
('CAT_05', 'Confectionery', '124', 'RESTRICTED', 100, 'FSSAI Schedule 2.4.5', 'Max limit 100 mg/kg for synthetic colors.'),
('CAT_05', 'Confectionery', '127', 'RESTRICTED', 100, 'FSSAI Schedule 2.4.5', 'Max limit 100 mg/kg for synthetic colors.');

-- CAT_07: Bakery Wares (Banned Potassium Bromate & Iodate; restricted propionates)
INSERT INTO fssai_category_limits (category_code, category_name, additive_code, status, max_limit_mg_kg, regulation_ref, restriction_details) VALUES
('CAT_07', 'Bakery wares', '924a', 'BANNED', 0, 'FSSAI Ban 2016', 'Potassium Bromate banned in all bakery wares.'),
('CAT_07', 'Bakery wares', '917', 'BANNED', 0, 'FSSAI Ban 2016', 'Potassium Iodate banned in all bakery wares.'),
('CAT_07', 'Bakery wares', '280', 'RESTRICTED', 2000, 'FSSAI Schedule 2.4.5', 'Propionic acid max limit 2000 mg/kg calculated as sodium propionate.'),
('CAT_07', 'Bakery wares', '281', 'RESTRICTED', 2000, 'FSSAI Schedule 2.4.5', 'Sodium propionate max limit 2000 mg/kg.'),
('CAT_07', 'Bakery wares', '282', 'RESTRICTED', 2000, 'FSSAI Schedule 2.4.5', 'Calcium propionate max limit 2000 mg/kg.');

-- CAT_14: Carbonated & Flavoured Beverages (Max 120 mg/kg Benzoates, 100 mg/kg synthetic colors)
INSERT INTO fssai_category_limits (category_code, category_name, additive_code, status, max_limit_mg_kg, regulation_ref, restriction_details) VALUES
('CAT_14', 'Beverages', '211', 'RESTRICTED', 120, 'FSSAI Schedule 2.4.5', 'Sodium benzoate max limit 120 mg/kg in flavoured drinks.'),
('CAT_14', 'Beverages', '202', 'RESTRICTED', 120, 'FSSAI Schedule 2.4.5', 'Sorbates max limit 120 mg/kg in flavoured drinks.'),
('CAT_14', 'Beverages', '102', 'RESTRICTED', 100, 'FSSAI Schedule 2.4.5', 'Synthetic colors max limit 100 mg/kg.'),
('CAT_14', 'Beverages', '110', 'RESTRICTED', 100, 'FSSAI Schedule 2.4.5', 'Synthetic colors max limit 100 mg/kg.'),
('CAT_14', 'Beverages', '122', 'RESTRICTED', 100, 'FSSAI Schedule 2.4.5', 'Synthetic colors max limit 100 mg/kg.'),
('CAT_14', 'Beverages', '133', 'RESTRICTED', 100, 'FSSAI Schedule 2.4.5', 'Synthetic colors max limit 100 mg/kg.');

-- Add all 15 top-level categories mapping rules for standard synthetic colors E102, E110, E122, E133
INSERT INTO fssai_category_limits (category_code, category_name, additive_code, status, max_limit_mg_kg, regulation_ref, restriction_details) VALUES
('CAT_02', 'Fats and oils', '100', 'APPROVED', 200, 'FSSAI Schedule 2.4.5', 'Antioxidants BHA/BHT permitted up to 200 mg/kg.'),
('CAT_03', 'Edible ices', '102', 'RESTRICTED', 100, 'FSSAI Schedule 2.4.5', 'Synthetic colors max limit 100 mg/kg in ice cream and lollies.'),
('CAT_03', 'Edible ices', '110', 'RESTRICTED', 100, 'FSSAI Schedule 2.4.5', 'Synthetic colors max limit 100 mg/kg.'),
('CAT_03', 'Edible ices', '122', 'RESTRICTED', 100, 'FSSAI Schedule 2.4.5', 'Synthetic colors max limit 100 mg/kg.'),
('CAT_03', 'Edible ices', '133', 'RESTRICTED', 100, 'FSSAI Schedule 2.4.5', 'Synthetic colors max limit 100 mg/kg.'),
('CAT_04', 'Fruits & Vegetables', '211', 'RESTRICTED', 200, 'FSSAI Schedule 2.4.5', 'Benzoates in fruit jams/jellies permitted up to 200 mg/kg.'),
('CAT_06', 'Cereals & cereal products', '924a', 'BANNED', 0, 'FSSAI Ban 2016', 'Bromate banned in all flour products.'),
('CAT_08', 'Meat & meat products', '250', 'RESTRICTED', 150, 'FSSAI Schedule 2.4.5', 'Sodium nitrite max limit 150 mg/kg.'),
('CAT_09', 'Fish & fish products', '211', 'BANNED', 0, 'FSSAI Schedule 2.4.5', 'Preservatives prohibited in fresh fish.'),
('CAT_10', 'Eggs & egg products', '102', 'BANNED', 0, 'FSSAI Schedule 2.4.5', 'Synthetic colors prohibited in fresh eggs.'),
('CAT_11', 'Sweeteners', '954', 'RESTRICTED', 500, 'FSSAI Schedule 2.4.5', 'Saccharin permitted in table-top sweeteners up to 500 mg/kg.'),
('CAT_12', 'Salts, spices, soups', '211', 'RESTRICTED', 750, 'FSSAI Schedule 2.4.5', 'Benzoates in sauces/condiments permitted up to 750 mg/kg.'),
('CAT_13', 'Particular nutritional uses', '102', 'BANNED', 0, 'FSSAI Schedule 2.4.5', 'Synthetic colors strictly prohibited in infant food.'),
('CAT_15', 'Ready-to-eat savouries', '621', 'RESTRICTED', 5000, 'FSSAI Schedule 2.4.5', 'MSG permitted up to 5000 mg/kg in extruded snacks.')
ON CONFLICT (category_code, additive_code) DO UPDATE 
SET status = EXCLUDED.status, max_limit_mg_kg = EXCLUDED.max_limit_mg_kg, restriction_details = EXCLUDED.restriction_details;
