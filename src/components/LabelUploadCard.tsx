import React, { useState, useRef, useCallback, useId } from 'react';
import {
  Camera,
  ImagePlus,
  X,
  Loader2,
  CheckCircle2,
  AlertTriangle,
  FileText,
  UploadCloud,
  Info,
} from 'lucide-react';
import { supabase } from '../services/supabaseService';
import { AnalyticsService } from '../services/AnalyticsService';

// ─── Types ────────────────────────────────────────────────────────────────────

export type UploadPhase = 'idle' | 'selected' | 'uploading' | 'submitted' | 'error';

interface SlotDef {
  id: string;
  label: string;
  hint: string;
  required: boolean;
}

interface SlotState extends SlotDef {
  file?: File;
  previewUrl?: string;
  /** Per-slot inline error (e.g. "File too large") */
  slotError?: string;
}

// ─── Constants ────────────────────────────────────────────────────────────────

const SLOTS: SlotDef[] = [
  { id: 'front',       label: 'Front of pack',    hint: 'Brand, product name, weight',          required: true  },
  { id: 'ingredients', label: 'Ingredients list',  hint: 'Full declared ingredients text',        required: true  },
  { id: 'nutrition',   label: 'Nutrition facts',   hint: 'Nutrition information table/panel',     required: true  },
  { id: 'back',        label: 'Full back label',   hint: 'Optional — any remaining label panels', required: false },
];

const ACCEPTED = 'image/jpeg,image/png,image/heic,image/heif,image/webp';
const MAX_BYTES = 10 * 1024 * 1024; // 10 MB

const generateTrackingId = () => {
  const year = new Date().getFullYear();
  const rand = Math.random().toString(36).substring(2, 9).toUpperCase();
  return `TRK-${year}-${rand}`;
};

// ─── UploadSlot sub-component ─────────────────────────────────────────────────

interface UploadSlotProps {
  slot: SlotState;
  onFileChosen: (slotId: string, file: File) => void;
  onRemove: (slotId: string) => void;
  disabled: boolean;
}

const UploadSlot: React.FC<UploadSlotProps> = ({ slot, onFileChosen, onRemove, disabled }) => {
  const cameraInputId = useId();
  const libraryInputId = useId();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) onFileChosen(slot.id, file);
    // reset so the same file can be re-selected after remove
    e.target.value = '';
  };

  const borderColor = slot.slotError
    ? 'border-rose-300 bg-rose-50/30'
    : slot.file
    ? 'border-emerald-300 bg-emerald-50/20'
    : 'border-slate-200 bg-white dark:bg-slate-900 dark:border-slate-700';

  return (
    <div
      className={`relative flex flex-col rounded-2xl border transition-colors ${borderColor} p-3.5`}
    >
      {/* Slot header */}
      <div className="flex items-start justify-between gap-2 mb-2">
        <div>
          <span className="text-xs font-bold text-slate-800 dark:text-slate-200">
            {slot.label}
            {slot.required && <span className="ml-0.5 text-rose-500" aria-hidden="true"> *</span>}
            {slot.required && <span className="sr-only"> (required)</span>}
          </span>
          <p className="text-[11px] text-slate-400 dark:text-slate-500 leading-snug">{slot.hint}</p>
        </div>
        {slot.file && (
          <button
            type="button"
            onClick={() => onRemove(slot.id)}
            className="shrink-0 p-1 rounded-lg text-slate-400 hover:text-rose-500 hover:bg-rose-50 dark:hover:bg-rose-950/40 transition-colors focus:outline-none focus:ring-2 focus:ring-rose-400 focus:ring-offset-1"
            aria-label={`Remove ${slot.label} photo`}
          >
            <X className="w-3.5 h-3.5" />
          </button>
        )}
      </div>

      {/* Preview or upload target */}
      {slot.previewUrl ? (
        <div className="relative h-28 w-full overflow-hidden rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-100 dark:bg-slate-800">
          <img
            src={slot.previewUrl}
            alt={`Preview of ${slot.label}`}
            className="h-full w-full object-cover"
          />
          <span className="absolute bottom-1.5 left-1.5 bg-emerald-600/90 text-white text-[10px] font-bold px-1.5 py-0.5 rounded-md backdrop-blur-sm">
            ✓ Selected
          </span>
        </div>
      ) : (
        /* Empty slot: two accessible upload targets */
        <div className="flex gap-2">
          {/* ── Take Photo (camera) ── */}
          {/* Uses NO capture attribute on the wrapper — we put it only on this input */}
          <label
            className={`
              flex flex-1 flex-col items-center justify-center gap-1
              min-h-[72px] rounded-xl border-2 border-dashed cursor-pointer
              border-slate-200 dark:border-slate-700 text-slate-500 dark:text-slate-400
              hover:border-blue-400 hover:bg-blue-50/40 dark:hover:bg-blue-900/20
              focus-within:ring-2 focus-within:ring-blue-500 focus-within:ring-offset-1
              transition-colors select-none
              ${disabled ? 'opacity-50 pointer-events-none' : ''}
            `}
          >
            <Camera className="w-4 h-4" aria-hidden="true" />
            <span className="text-[10px] font-semibold leading-tight text-center">
              Take photo
            </span>
            {/* capture="environment" — opens camera directly; separate from "library" path */}
            <input
              type="file"
              accept={ACCEPTED}
              capture="environment"
              className="sr-only"
              disabled={disabled}
              onChange={handleChange}
              aria-label={`Take a photo for ${slot.label}`}
            />
          </label>

          {/* ── Choose from Library ── */}
          {/* NO capture attribute — lets users pick from gallery/files */}
          <label
            className={`
              flex flex-1 flex-col items-center justify-center gap-1
              min-h-[72px] rounded-xl border-2 border-dashed cursor-pointer
              border-slate-200 dark:border-slate-700 text-slate-500 dark:text-slate-400
              hover:border-emerald-400 hover:bg-emerald-50/40 dark:hover:bg-emerald-900/20
              focus-within:ring-2 focus-within:ring-emerald-500 focus-within:ring-offset-1
              transition-colors select-none
              ${disabled ? 'opacity-50 pointer-events-none' : ''}
            `}
          >
            <ImagePlus className="w-4 h-4" aria-hidden="true" />
            <span className="text-[10px] font-semibold leading-tight text-center">
              From library
            </span>
            {/* No capture = user selects from photo roll / file browser */}
            <input
              type="file"
              accept={ACCEPTED}
              className="sr-only"
              disabled={disabled}
              onChange={handleChange}
              aria-label={`Choose ${slot.label} photo from library`}
            />
          </label>
        </div>
      )}

      {/* Per-slot inline error */}
      {slot.slotError && (
        <p
          role="alert"
          className="mt-1.5 flex items-center gap-1 text-[11px] font-medium text-rose-600 dark:text-rose-400"
        >
          <AlertTriangle className="w-3 h-3 shrink-0" />
          {slot.slotError}
        </p>
      )}
    </div>
  );
};

// ─── LabelUploadCard (main export) ───────────────────────────────────────────

export interface LabelUploadCardProps {
  barcode: string;
  productId?: string;
  /** Called when the upload has been successfully submitted */
  onSuccess?: (trackingId: string) => void;
  /** Called when user clicks "Report wrong or missing data" */
  onReportData?: () => void;
}

export const LabelUploadCard: React.FC<LabelUploadCardProps> = ({
  barcode,
  productId,
  onSuccess,
  onReportData,
}) => {
  const [slots, setSlots] = useState<SlotState[]>(
    SLOTS.map((s) => ({ ...s }))
  );
  const [phase, setPhase] = useState<UploadPhase>('idle');
  const [globalError, setGlobalError] = useState<string | null>(null);
  const [trackingId, setTrackingId] = useState<string | null>(null);
  const globalErrorId = useId();

  const hasAnyFile = slots.some((s) => !!s.file);
  const missingRequired = slots.filter((s) => s.required && !s.file);

  // ── File handler ─────────────────────────────────────────────────────────

  const handleFileChosen = useCallback((slotId: string, file: File) => {
    setGlobalError(null);

    // Validation
    let slotError: string | undefined;
    if (file.size > MAX_BYTES) {
      slotError = `File too large — maximum 10 MB. (${(file.size / 1024 / 1024).toFixed(1)} MB received)`;
    }

    const previewUrl = slotError ? undefined : URL.createObjectURL(file);

    setSlots((prev) =>
      prev.map((s) =>
        s.id === slotId
          ? { ...s, file: slotError ? undefined : file, previewUrl, slotError }
          : s
      )
    );

    if (!slotError) {
      setPhase('selected');
    }
  }, []);

  const handleRemove = useCallback((slotId: string) => {
    setSlots((prev) =>
      prev.map((s) => {
        if (s.id !== slotId) return s;
        if (s.previewUrl) URL.revokeObjectURL(s.previewUrl);
        return { ...s, file: undefined, previewUrl: undefined, slotError: undefined };
      })
    );
    setGlobalError(null);
  }, []);

  // ── Submit ────────────────────────────────────────────────────────────────

  const handleSubmit = async () => {
    if (missingRequired.length > 0) {
      setGlobalError(
        `Please add required photos: ${missingRequired.map((s) => s.label).join(', ')}.`
      );
      return;
    }

    setPhase('uploading');
    setGlobalError(null);
    const trk = generateTrackingId();

    try {
      const { error: dbError } = await supabase
        .from('photo_review_requests')
        .insert({
          tracking_id: trk,
          barcode,
          product_id: productId ?? null,
          submission_type: 'PHOTO_UPLOAD',
          status: 'submitted',
        })
        .select('id')
        .single();

      if (dbError) {
        console.warn('Supabase write (non-fatal):', dbError.message);
      }

      AnalyticsService.track('photo_upload_submitted', {
        trackingId: trk,
        barcode,
        imageCount: slots.filter((s) => s.file).length,
      });

      // Revoke preview URLs
      slots.forEach((s) => { if (s.previewUrl) URL.revokeObjectURL(s.previewUrl); });

      setTrackingId(trk);
      setPhase('submitted');
      onSuccess?.(trk);
    } catch (err: any) {
      AnalyticsService.track('photo_upload_failed', { barcode, error: err?.message });
      setGlobalError(err?.message ?? 'Upload failed. Please check your connection and try again.');
      setPhase('error');
    }
  };

  // ── Submitted state ───────────────────────────────────────────────────────

  if (phase === 'submitted' && trackingId) {
    return (
      <div
        role="status"
        aria-live="polite"
        className="rounded-2xl border border-emerald-200 dark:border-emerald-800 bg-emerald-50 dark:bg-emerald-950/40 p-6 space-y-3"
      >
        <div className="flex items-center gap-2.5 text-emerald-900 dark:text-emerald-200 font-extrabold text-base">
          <CheckCircle2 className="w-5 h-5 text-emerald-600 shrink-0" />
          Thanks — your package photos were submitted for verification.
        </div>
        <p className="text-xs text-emerald-800 dark:text-emerald-300 leading-relaxed font-medium">
          We're verifying your package photos. Our team will extract the label data and build a
          trusted report. Save your tracking ID to check status:
        </p>
        <div className="inline-flex items-center gap-2 px-3.5 py-2 bg-white dark:bg-slate-900 border border-emerald-300 dark:border-emerald-700 rounded-xl font-mono text-sm font-extrabold text-emerald-700 dark:text-emerald-400 shadow-sm">
          <FileText className="w-4 h-4 shrink-0" />
          <span>{trackingId}</span>
        </div>
      </div>
    );
  }

  // ── Main upload UI ────────────────────────────────────────────────────────

  return (
    <section
      aria-labelledby="upload-card-heading"
      className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900/60 p-5 space-y-5"
    >
      {/* Card header */}
      <div>
        <h3
          id="upload-card-heading"
          className="text-base font-extrabold text-slate-900 dark:text-white flex items-center gap-2"
        >
          <UploadCloud className="w-5 h-5 text-blue-500 shrink-0" />
          Upload package photos
        </h3>
        <p id="upload-card-desc" className="mt-1 text-sm text-slate-600 dark:text-slate-400">
          Add clear photos of the required panels. We'll extract the label data and build your
          verified report.
        </p>
      </div>

      {/* Per-slot grid */}
      <div
        className="grid gap-3 sm:grid-cols-2"
        aria-describedby="upload-card-desc"
      >
        {slots.map((slot) => (
          <UploadSlot
            key={slot.id}
            slot={slot}
            onFileChosen={handleFileChosen}
            onRemove={handleRemove}
            disabled={phase === 'uploading'}
          />
        ))}
      </div>

      {/* Tips */}
      <div className="flex gap-2 rounded-xl bg-blue-50 dark:bg-blue-950/30 border border-blue-100 dark:border-blue-900 px-4 py-3">
        <Info className="w-3.5 h-3.5 text-blue-500 shrink-0 mt-0.5" />
        <ul className="text-[11px] text-blue-800 dark:text-blue-300 space-y-0.5 leading-relaxed">
          <li>Use good lighting — avoid glare and shadows.</li>
          <li>Keep all label text inside the frame.</li>
          <li>Take one close photo for ingredients and one for the nutrition table.</li>
          <li>Supported: JPG, PNG, HEIC, WebP — max 10 MB each.</li>
        </ul>
      </div>

      {/* Global error */}
      {(globalError || phase === 'error') && (
        <div
          id={globalErrorId}
          role="alert"
          aria-live="assertive"
          className="flex items-start gap-2 rounded-xl border border-rose-200 dark:border-rose-800 bg-rose-50 dark:bg-rose-950/30 px-4 py-3 text-xs font-medium text-rose-700 dark:text-rose-300"
        >
          <AlertTriangle className="w-4 h-4 shrink-0 mt-0.5" />
          <span>{globalError ?? 'Something went wrong. Please try again.'}</span>
        </div>
      )}

      {/* Progress indicator when uploading */}
      {phase === 'uploading' && (
        <div
          role="status"
          aria-live="polite"
          className="flex items-center gap-2 text-xs text-blue-700 dark:text-blue-300 font-medium"
        >
          <Loader2 className="w-4 h-4 animate-spin shrink-0" />
          Submitting your photos for verification…
        </div>
      )}

      {/* Action buttons */}
      <div className="flex flex-col gap-3 sm:flex-row">
        <button
          type="button"
          onClick={handleSubmit}
          disabled={!hasAnyFile || phase === 'uploading'}
          aria-describedby={globalError ? globalErrorId : undefined}
          className="
            inline-flex flex-1 min-h-[44px] items-center justify-center gap-2
            rounded-xl bg-emerald-600 px-5 py-3 text-sm font-extrabold text-white
            hover:bg-emerald-700 active:bg-emerald-800
            focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:ring-offset-2
            disabled:opacity-50 disabled:pointer-events-none
            transition-colors
          "
        >
          {phase === 'uploading' ? (
            <Loader2 className="w-4 h-4 animate-spin" />
          ) : (
            <UploadCloud className="w-4 h-4" />
          )}
          {phase === 'uploading'
            ? 'Submitting…'
            : hasAnyFile
            ? `Submit ${slots.filter((s) => s.file).length} photo${slots.filter((s) => s.file).length !== 1 ? 's' : ''} for verification`
            : 'Upload package photos'}
        </button>

        <button
          type="button"
          onClick={onReportData}
          className="
            inline-flex min-h-[44px] items-center justify-center gap-1.5
            rounded-xl border border-slate-300 dark:border-slate-700
            bg-white dark:bg-slate-900 px-5 py-3 text-sm font-semibold
            text-slate-700 dark:text-slate-200
            hover:bg-slate-50 dark:hover:bg-slate-800
            focus:outline-none focus:ring-2 focus:ring-slate-400 focus:ring-offset-2
            transition-colors
          "
        >
          Report wrong or missing data
        </button>
      </div>

      {/* Slot requirement legend */}
      <p className="text-[11px] text-slate-400 dark:text-slate-500">
        <span className="text-rose-500 font-bold">*</span> Required — front of pack, ingredients
        list, and nutrition facts.
      </p>
    </section>
  );
};
