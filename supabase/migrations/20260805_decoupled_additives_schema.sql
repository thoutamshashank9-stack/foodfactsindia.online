-- 1. Canonical Additives Master Table
CREATE TABLE IF NOT EXISTS canonical_additives (
    id TEXT PRIMARY KEY,                       -- e.g. 'ing_122'
    ins_code TEXT,                             -- Non-unique (allows sub-variants 150a-d)
    e_number TEXT,                             -- e.g. 'E122'
    cas_number TEXT,                            -- e.g. '3567-69-9' (PubChem Key)
    ci_number TEXT,                            -- e.g. 'CI 14720'
    primary_name TEXT NOT NULL,                -- e.g. 'Azorubine (Carmoisine)'
    chemical_name TEXT,
    category TEXT NOT NULL,                    -- 'ARTIFICIAL_COLOR', 'PRESERVATIVE', etc.
    risk_level TEXT NOT NULL CHECK (risk_level IN ('HIGH', 'MEDIUM', 'LOW', 'EXCELLENT')),
    base_risk_weight INT NOT NULL DEFAULT 0,
    cspi_rating TEXT CHECK (cspi_rating IN ('AVOID', 'CAUTION', 'CUT_BACK', 'SAFE')),
    description TEXT NOT NULL,
    processing_level TEXT NOT NULL DEFAULT 'NOVA_4_ULTRA_PROCESSED',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_canonical_ins ON canonical_additives (ins_code);
CREATE INDEX IF NOT EXISTS idx_canonical_cas ON canonical_additives (cas_number);

-- 2. Additive Synonyms & Aliases Table
CREATE TABLE IF NOT EXISTS additive_synonyms (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    additive_id TEXT NOT NULL REFERENCES canonical_additives(id) ON DELETE CASCADE,
    synonym_clean TEXT NOT NULL,                -- Lowercase: 'carmoisine', 'fd&c red no. 3'
    language_code TEXT DEFAULT 'en',
    is_primary BOOLEAN DEFAULT FALSE,
    CONSTRAINT unique_additive_synonym UNIQUE (additive_id, synonym_clean)
);

CREATE INDEX IF NOT EXISTS idx_additive_synonyms_lookup ON additive_synonyms (synonym_clean);

-- 3. Category-Scoped Regulatory Bans & Restrictions Table
CREATE TABLE IF NOT EXISTS regulatory_bans (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    additive_id TEXT NOT NULL REFERENCES canonical_additives(id) ON DELETE CASCADE,
    jurisdiction_code TEXT NOT NULL CHECK (jurisdiction_code IN ('US', 'JP', 'EU', 'UK', 'IN', 'CODEX')),
    status TEXT NOT NULL CHECK (status IN ('BANNED', 'RESTRICTED', 'APPROVED')),
    scope_category TEXT DEFAULT 'ALL',          -- 'ALL', 'DAIRY', 'BEVERAGES', etc.
    max_limit_mg_kg NUMERIC,                    -- NULL if BANNED, value if RESTRICTED
    restriction_details TEXT,
    regulation_ref TEXT NOT NULL,               -- e.g. '21 CFR Part 74'
    mandatory_warning_text TEXT,
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT unique_additive_jurisdiction_scope UNIQUE (additive_id, jurisdiction_code, scope_category)
);

-- 4. PostgreSQL Fast Set-Based Additive Matcher RPC
CREATE OR REPLACE FUNCTION match_product_additives(raw_tokens TEXT[])
RETURNS TABLE (
    additive_id TEXT,
    primary_name TEXT,
    ins_code TEXT,
    e_number TEXT,
    cas_number TEXT,
    risk_level TEXT,
    cspi_rating TEXT,
    matched_synonym TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT ON (ca.id)
        ca.id AS additive_id,
        ca.primary_name,
        ca.ins_code,
        ca.e_number,
        ca.cas_number,
        ca.risk_level,
        ca.cspi_rating,
        s.synonym_clean AS matched_synonym
    FROM additive_synonyms s
    JOIN canonical_additives ca ON ca.id = s.additive_id
    WHERE s.synonym_clean = ANY(raw_tokens)
    ORDER BY ca.id, 
        CASE ca.risk_level 
            WHEN 'HIGH' THEN 1 
            WHEN 'MEDIUM' THEN 2 
            WHEN 'LOW' THEN 3 
            ELSE 4 
        END;
END;
$$ LANGUAGE plpgsql STABLE;
