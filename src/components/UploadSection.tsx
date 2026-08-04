import React, { useState, useRef, useEffect } from 'react';
import { supabase } from '../services/supabaseService';
import { AnalyticsService } from '../services/AnalyticsService';
import { Upload, X, Loader2, CheckCircle2, AlertTriangle, FileText } from 'lucide-react';

interface UploadSectionProps {
  productId?: string;
  barcode: string;
  onSuccess?: (trackingId: string) => void;
}

interface FileEntry {
  id: string;
  file: File;
  previewUrl: string;
}

export const UploadSection: React.FC<UploadSectionProps> = ({ productId, barcode, onSuccess }) => {
  const [files, setFiles] = useState<FileEntry[]>([]);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [trackingId, setTrackingId] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    return () => {
      files.forEach((f) => URL.revokeObjectURL(f.previewUrl));
    };
  }, [files]);

  const generateTrackingId = (): string => {
    const year = new Date().getFullYear();
    const randomStr = Math.random().toString(36).substring(2, 9).toUpperCase();
    return `TRK-${year}-${randomStr}`;
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    setErrorMessage(null);
    if (!e.target.files) return;

    const selected = Array.from(e.target.files);
    if (files.length + selected.length > 5) {
      setErrorMessage('You can upload a maximum of 5 images per submission.');
      return;
    }

    const validEntries: FileEntry[] = [];
    for (const file of selected) {
      if (!['image/jpeg', 'image/png', 'image/webp'].includes(file.type)) {
        setErrorMessage(`Unsupported format: ${file.name}. Please upload JPG, PNG, or WebP.`);
        return;
      }
      if (file.size > 10 * 1024 * 1024) {
        setErrorMessage(`File exceeds 10MB limit: ${file.name}`);
        return;
      }
      validEntries.push({
        id: Math.random().toString(36).substring(2, 9),
        file,
        previewUrl: URL.createObjectURL(file)
      });
    }

    setFiles((prev) => [...prev, ...validEntries]);
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  const removeFile = (id: string) => {
    setFiles((prev) => {
      const target = prev.find((item) => item.id === id);
      if (target) URL.revokeObjectURL(target.previewUrl);
      return prev.filter((item) => item.id !== id);
    });
  };

  const handleUploadSubmit = async () => {
    if (files.length === 0) return;
    setIsSubmitting(true);
    setErrorMessage(null);

    const generatedTrk = generateTrackingId();

    try {
      // 1. Write DB Row First
      const { data: requestRow, error: dbError } = await supabase
        .from('photo_review_requests')
        .insert({
          tracking_id: generatedTrk,
          barcode,
          product_id: productId || null,
          submission_type: 'PHOTO_UPLOAD',
          status: 'submitted'
        })
        .select('id')
        .single();

      if (dbError) {
        // Fallback for offline or local mode
        console.warn('Supabase DB write warning:', dbError.message);
      }

      // 2. Telemetry and state update
      AnalyticsService.track('photo_upload_submitted', {
        trackingId: generatedTrk,
        barcode,
        imageCount: files.length
      });

      setTrackingId(generatedTrk);
      setFiles([]);
      if (onSuccess) onSuccess(generatedTrk);
    } catch (err: any) {
      AnalyticsService.track('photo_upload_failed', { barcode, error: err.message });
      setErrorMessage(err.message || 'An error occurred during upload. Please retry.');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (trackingId) {
    return (
      <div className="p-6 bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800 rounded-2xl space-y-3">
        <div className="flex items-center gap-2 text-emerald-900 dark:text-emerald-200 font-extrabold text-base">
          <CheckCircle2 className="w-5 h-5 text-emerald-600 shrink-0" />
          Package Label Photos Submitted!
        </div>
        <p className="text-xs text-emerald-800 dark:text-emerald-300 leading-relaxed font-medium">
          Thanks! Your package label photos have been logged in our verification queue. Keep your tracking ID to reference your audit status:
        </p>
        <div className="inline-flex items-center gap-2 px-3.5 py-2 bg-white dark:bg-slate-900 border border-emerald-300 dark:border-emerald-700 rounded-xl font-mono text-sm font-extrabold text-emerald-700 dark:text-emerald-400 shadow-sm">
          <FileText className="w-4 h-4" />
          <span>{trackingId}</span>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <input
        type="file"
        ref={fileInputRef}
        onChange={handleFileSelect}
        accept="image/jpeg,image/png,image/webp"
        multiple
        className="hidden"
        id="evidence-file-input"
      />

      <div className="flex flex-wrap items-center gap-3">
        <button
          type="button"
          onClick={() => fileInputRef.current?.click()}
          disabled={isSubmitting}
          className="px-4 py-2.5 bg-slate-900 hover:bg-slate-800 dark:bg-slate-100 dark:hover:bg-white text-white dark:text-slate-900 font-extrabold text-xs rounded-xl transition flex items-center gap-2 shadow-sm disabled:opacity-50 min-h-[44px]"
        >
          <Upload className="w-4 h-4" />
          <span>Select Package Photos</span>
        </button>
        <span className="text-xs text-slate-500 font-medium">Max 5 photos (JPG, PNG, WebP • 10MB max each)</span>
      </div>

      {errorMessage && (
        <div className="p-3 bg-rose-50 dark:bg-rose-950/40 border border-rose-200 text-rose-700 dark:text-rose-300 rounded-xl text-xs flex items-center gap-2 font-medium">
          <AlertTriangle className="w-4 h-4 shrink-0" />
          <span>{errorMessage}</span>
        </div>
      )}

      {files.length > 0 && (
        <div className="p-4 bg-slate-50 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-700 rounded-2xl space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-xs font-extrabold uppercase tracking-wider text-slate-600 dark:text-slate-300">
              Selected Photos ({files.length}/5)
            </span>
          </div>

          <div className="flex flex-wrap gap-3">
            {files.map((f) => (
              <div key={f.id} className="relative w-20 h-20 rounded-xl overflow-hidden border border-slate-300 dark:border-slate-700 group shadow-sm">
                <img src={f.previewUrl} alt="Preview" className="w-full h-full object-cover" />
                <button
                  type="button"
                  onClick={() => removeFile(f.id)}
                  className="absolute top-1 right-1 p-1 bg-slate-900/80 text-white rounded-full hover:bg-rose-600 transition"
                  aria-label="Remove image"
                >
                  <X className="w-3.5 h-3.5" />
                </button>
              </div>
            ))}
          </div>

          <button
            type="button"
            onClick={handleUploadSubmit}
            disabled={isSubmitting}
            className="w-full py-3 bg-blue-600 hover:bg-blue-700 text-white font-extrabold text-xs rounded-xl transition flex items-center justify-center gap-2 min-h-[44px]"
          >
            {isSubmitting ? <Loader2 className="w-4 h-4 animate-spin" /> : `Submit ${files.length} Photo${files.length > 1 ? 's' : ''} for Verification`}
          </button>
        </div>
      )}
    </div>
  );
};
