-- 1. Evidence Submissions Table
CREATE TABLE IF NOT EXISTS public.evidence_submissions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  product_id UUID REFERENCES public.products(id) ON DELETE CASCADE,
  submission_source TEXT NOT NULL DEFAULT 'USER_UPLOAD',
  submitted_by UUID REFERENCES auth.users(id),
  status TEXT NOT NULL DEFAULT 'PROCESSING', -- 'AWAITING_IMAGES', 'PROCESSING', 'NEEDS_REVIEW', 'VERIFIED'
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Evidence Images Table (Secure File Upload Provenance)
CREATE TABLE IF NOT EXISTS public.evidence_images (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  submission_id UUID NOT NULL REFERENCES public.evidence_submissions(id) ON DELETE CASCADE,
  image_type TEXT NOT NULL, -- 'FRONT', 'INGREDIENTS', 'NUTRITION'
  storage_path TEXT NOT NULL,
  sha256 TEXT NOT NULL,
  mime_type TEXT NOT NULL DEFAULT 'image/jpeg',
  width INTEGER,
  height INTEGER,
  raw_ocr_json JSONB,
  confidence NUMERIC(4,3),
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Immutable Extraction Runs Table
CREATE TABLE IF NOT EXISTS public.extraction_runs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  submission_id UUID NOT NULL REFERENCES public.evidence_submissions(id) ON DELETE CASCADE,
  schema_version TEXT NOT NULL DEFAULT 'v2.0',
  extracted_json JSONB NOT NULL,
  normalized_json JSONB NOT NULL,
  validation_passed BOOLEAN NOT NULL DEFAULT FALSE,
  validation_errors JSONB,
  review_required BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. Published Immutable Report Snapshots Table
CREATE TABLE IF NOT EXISTS public.report_snapshots (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  product_id UUID NOT NULL REFERENCES public.products(id) ON DELETE CASCADE,
  extraction_run_id UUID NOT NULL REFERENCES public.extraction_runs(id),
  score_json JSONB NOT NULL,
  methodology_version TEXT NOT NULL DEFAULT 'v1.4',
  published_at TIMESTAMPTZ DEFAULT NOW(),
  is_current_published BOOLEAN NOT NULL DEFAULT TRUE
);

-- Partial Unique Index: Ensures strictly ONLY ONE current published report per product
CREATE UNIQUE INDEX IF NOT EXISTS idx_current_published_report 
ON public.report_snapshots(product_id) 
WHERE is_current_published = true;
