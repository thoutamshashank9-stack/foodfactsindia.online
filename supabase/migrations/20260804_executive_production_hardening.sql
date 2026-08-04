-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- 1. ENUMS FOR STRICT STATE MACHINES
DO $$ BEGIN
    CREATE TYPE product_verification_status AS ENUM (
        'unverified',
        'submitted',
        'under_review',
        'needs_more_photos',
        'verified',
        'rejected',
        'duplicate',
        'obsolete'
    );
EXCEPTION WHEN duplicate_object THEN null; END $$;

DO $$ BEGIN
    CREATE TYPE variant_type_enum AS ENUM (
        'single_pack',
        'refill',
        'multipack',
        'regional_variant',
        'limited_edition'
    );
EXCEPTION WHEN duplicate_object THEN null; END $$;

DO $$ BEGIN
    CREATE TYPE submission_type_enum AS ENUM (
        'PHOTO_UPLOAD',
        'FAST_TRACK_AUDIT'
    );
EXCEPTION WHEN duplicate_object THEN null; END $$;

-- 2. CANONICAL PRODUCTS TABLE
CREATE TABLE IF NOT EXISTS public.products (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    canonical_product_id UUID NULL REFERENCES public.products(id) ON DELETE SET NULL,
    canonical_name TEXT NOT NULL,
    canonical_brand TEXT NOT NULL,
    category_id TEXT NOT NULL,
    verification_status product_verification_status NOT NULL DEFAULT 'unverified',
    data_completeness_score INT NOT NULL DEFAULT 0 CHECK (data_completeness_score BETWEEN 0 AND 100),
    country_code VARCHAR(3) NOT NULL DEFAULT 'IND',
    last_verified_source TEXT NULL,
    reviewed_at TIMESTAMPTZ NULL,
    reviewed_by UUID NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 3. BARCODE ALIAS MAPPING TABLE
CREATE TABLE IF NOT EXISTS public.product_barcode_aliases (
    barcode TEXT PRIMARY KEY,
    canonical_product_id UUID NOT NULL REFERENCES public.products(id) ON DELETE CASCADE,
    variant_type variant_type_enum NOT NULL DEFAULT 'single_pack',
    variant_description TEXT NULL,
    country_code VARCHAR(3) NOT NULL DEFAULT 'IND',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 4. PHOTO REVIEW & AUDIT REQUESTS (REAL PERSISTENCE)
CREATE TABLE IF NOT EXISTS public.photo_review_requests (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tracking_id VARCHAR(20) UNIQUE NOT NULL,
    barcode TEXT NOT NULL,
    product_id UUID NULL REFERENCES public.products(id) ON DELETE SET NULL,
    user_id UUID NULL,
    email TEXT NULL,
    urgency_note TEXT NULL,
    submission_type submission_type_enum NOT NULL,
    status product_verification_status NOT NULL DEFAULT 'submitted',
    ip_hash TEXT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS public.photo_review_images (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    request_id UUID NOT NULL REFERENCES public.photo_review_requests(id) ON DELETE CASCADE,
    storage_path TEXT NOT NULL,
    file_size_bytes INT NOT NULL CHECK (file_size_bytes <= 10485760), -- 10MB Limit
    mime_type VARCHAR(50) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 5. MODERATION EVENT AUDIT TRAIL
CREATE TABLE IF NOT EXISTS public.product_moderation_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    product_id UUID NOT NULL REFERENCES public.products(id) ON DELETE CASCADE,
    from_status product_verification_status NOT NULL,
    to_status product_verification_status NOT NULL,
    actor_id UUID NOT NULL,
    reason TEXT NOT NULL,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- INDEXES FOR ACCELERATED SEARCH & LOOKUPS
CREATE INDEX IF NOT EXISTS idx_products_search_ranking 
ON public.products (verification_status, data_completeness_score DESC);

CREATE INDEX IF NOT EXISTS idx_photo_review_tracking 
ON public.photo_review_requests (tracking_id);

-- 6. SEARCH & DEDUPLICATION RPC
CREATE OR REPLACE FUNCTION public.search_canonical_products(
    search_term TEXT,
    result_limit INT DEFAULT 20,
    result_offset INT DEFAULT 0
)
RETURNS TABLE (
    product_id UUID,
    matched_barcode TEXT,
    canonical_name TEXT,
    canonical_brand TEXT,
    verification_status product_verification_status,
    data_completeness_score INT,
    is_exact_barcode_match BOOLEAN
) 
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    WITH exact_barcode AS (
        SELECT pba.canonical_product_id, pba.barcode
        FROM public.product_barcode_aliases pba
        WHERE pba.barcode = search_term
    )
    SELECT 
        p.id AS product_id,
        COALESCE(eb.barcode, pba_primary.barcode, 'N/A') AS matched_barcode,
        p.canonical_name,
        p.canonical_brand,
        p.verification_status,
        p.data_completeness_score,
        (eb.canonical_product_id IS NOT NULL) AS is_exact_barcode_match
    FROM public.products p
    LEFT JOIN exact_barcode eb ON p.id = eb.canonical_product_id
    LEFT JOIN LATERAL (
        SELECT barcode FROM public.product_barcode_aliases 
        WHERE canonical_product_id = p.id 
        LIMIT 1
    ) pba_primary ON TRUE
    WHERE 
        p.verification_status != 'duplicate'
        AND p.verification_status != 'obsolete'
        AND (
            eb.canonical_product_id IS NOT NULL
            OR p.canonical_name ILIKE '%' || search_term || '%'
            OR p.canonical_brand ILIKE '%' || search_term || '%'
        )
    ORDER BY 
        -- Priority 1: Exact Barcode Match
        (CASE WHEN eb.canonical_product_id IS NOT NULL THEN 0 ELSE 1 END) ASC,
        -- Priority 2: Verified Products First
        (CASE WHEN p.verification_status = 'verified' THEN 0 ELSE 1 END) ASC,
        -- Priority 3: Data Completeness Score
        p.data_completeness_score DESC,
        -- Priority 4: Alphabetical
        p.canonical_name ASC
    LIMIT result_limit
    OFFSET result_offset;
END;
$$;
