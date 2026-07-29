-- =======================================================
-- Supabase / PostgreSQL Schema DDL for FoodLens OFF India
-- Generated to match off_india_clean.csv, product_ingredients.csv,
-- product_additives.csv, and additive_rulebook.
-- =======================================================

-- 1. Main Products Table
CREATE TABLE IF NOT EXISTS public.products (
    barcode VARCHAR(64) PRIMARY KEY,
    product_name TEXT NOT NULL,
    brands TEXT,
    categories TEXT,
    countries_tags TEXT,
    ingredients_text TEXT,
    additives_tags TEXT,
    allergens_tags TEXT,
    nova_group SMALLINT,
    nutriscore_grade VARCHAR(10),
    energy_100g DOUBLE PRECISION,
    sugars_100g DOUBLE PRECISION,
    fat_100g DOUBLE PRECISION,
    saturated_fat_100g DOUBLE PRECISION,
    trans_fat_100g DOUBLE PRECISION,
    protein_100g DOUBLE PRECISION,
    fibre_100g DOUBLE PRECISION,
    sodium_100g DOUBLE PRECISION,
    salt_100g DOUBLE PRECISION,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Tokenized Product Ingredients Table
CREATE TABLE IF NOT EXISTS public.product_ingredients (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    barcode VARCHAR(64) NOT NULL REFERENCES public.products(barcode) ON DELETE CASCADE,
    ingredient_raw TEXT NOT NULL,
    position INT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Extracted Product Additives Table
CREATE TABLE IF NOT EXISTS public.product_additives (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    barcode VARCHAR(64) NOT NULL REFERENCES public.products(barcode) ON DELETE CASCADE,
    additive_code VARCHAR(32) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. Phase 2: Regulatory Rulebook Table
CREATE TABLE IF NOT EXISTS public.additive_rulebook (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    additive_code VARCHAR(32) NOT NULL,        -- e.g. 'E102'
    ins_number VARCHAR(32),
    canonical_name TEXT,
    functional_class TEXT,
    jurisdiction VARCHAR(10) NOT NULL,          -- 'IN', 'EU', 'US', 'UK', 'CODEX'
    status VARCHAR(32) NOT NULL,                -- 'permitted', 'restricted', 'banned', 'requires_warning'
    max_level_value NUMERIC,
    max_level_unit VARCHAR(32),
    label_requirement TEXT,                     -- e.g. Southampton warning text
    regulation_title TEXT,
    source_url TEXT,
    verified_at TIMESTAMPTZ,
    verification_status VARCHAR(32) DEFAULT 'unverified',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(additive_code, jurisdiction)
);

-- =======================================================
-- Performance & Search Indexes
-- =======================================================

-- Fast lookup of ingredients and additives by barcode
CREATE INDEX IF NOT EXISTS idx_product_ingredients_barcode ON public.product_ingredients(barcode);
CREATE INDEX IF NOT EXISTS idx_product_additives_barcode ON public.product_additives(barcode);

-- Fast lookup by additive E-number/INS code for regulatory join rules
CREATE INDEX IF NOT EXISTS idx_product_additives_code ON public.product_additives(additive_code);
CREATE INDEX IF NOT EXISTS idx_rulebook_code_jurisdiction ON public.additive_rulebook(additive_code, jurisdiction);

-- Search indexes
CREATE INDEX IF NOT EXISTS idx_products_name ON public.products(product_name);
CREATE INDEX IF NOT EXISTS idx_product_ingredients_raw ON public.product_ingredients(ingredient_raw);
