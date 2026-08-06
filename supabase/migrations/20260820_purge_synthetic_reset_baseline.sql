-- Step 1: Add data_provenance and source_document to tables if not exists
DO $$ 
BEGIN
    -- additive_regulatory_matrix
    BEGIN
        ALTER TABLE public.additive_regulatory_matrix ADD COLUMN data_provenance VARCHAR(50) DEFAULT 'QUARANTINED_PENDING_REVIEW';
        ALTER TABLE public.additive_regulatory_matrix ADD COLUMN source_document VARCHAR(255);
    EXCEPTION WHEN duplicate_column THEN END;

    -- fema_flavors_master
    BEGIN
        ALTER TABLE public.fema_flavors_master ADD COLUMN data_provenance VARCHAR(50) DEFAULT 'QUARANTINED_PENDING_REVIEW';
        ALTER TABLE public.fema_flavors_master ADD COLUMN source_document VARCHAR(255);
    EXCEPTION WHEN undefined_table THEN END;
    EXCEPTION WHEN duplicate_column THEN END;

    -- raw_ingredients_taxonomy
    BEGIN
        ALTER TABLE public.raw_ingredients_taxonomy ADD COLUMN data_provenance VARCHAR(50) DEFAULT 'QUARANTINED_PENDING_REVIEW';
        ALTER TABLE public.raw_ingredients_taxonomy ADD COLUMN source_document VARCHAR(255);
    EXCEPTION WHEN undefined_table THEN END;
    EXCEPTION WHEN duplicate_column THEN END;
END $$;

-- Step 2: Purge Synthetic Data
-- Delete synthetic pyrazines from FEMA master (if exists)
DO $$
BEGIN
    DELETE FROM public.fema_flavors_master 
    WHERE cas_number LIKE '18138-__-_%';
EXCEPTION WHEN undefined_table THEN END;
END $$;

-- Delete fabricated rice varieties from raw ingredients (if exists)
DO $$
BEGIN
    DELETE FROM public.raw_ingredients_taxonomy 
    WHERE name ~ '^PR[0-9]{3}$' AND name NOT IN ('PR11','PR14','PR18');
EXCEPTION WHEN undefined_table THEN END;
END $$;

-- Step 3: Set known good baseline to VERIFIED
UPDATE public.additive_regulatory_matrix 
SET data_provenance = 'VERIFIED'
WHERE status IN ('BANNED', 'RESTRICTED');

-- Step 4: Create audit view
CREATE OR REPLACE VIEW public.v_data_integrity_audit AS
SELECT 
    'additive_regulatory_matrix' AS table_name,
    COUNT(*) AS total_rows,
    SUM(CASE WHEN data_provenance = 'VERIFIED' THEN 1 ELSE 0 END) AS verified_rows,
    SUM(CASE WHEN data_provenance = 'QUARANTINED_PENDING_REVIEW' THEN 1 ELSE 0 END) AS quarantined_rows
FROM public.additive_regulatory_matrix;
