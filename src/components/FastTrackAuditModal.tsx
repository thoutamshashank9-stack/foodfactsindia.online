import React, { useState } from 'react';
import { supabase } from '../services/supabaseService';
import { AnalyticsService } from '../services/AnalyticsService';
import { AccessibleModal } from './AccessibleModal';
import { FileSearch, Loader2, CheckCircle2, FileText } from 'lucide-react';

interface FastTrackAuditModalProps {
  isOpen: boolean;
  onClose: () => void;
  barcode: string;
  productName: string;
}

export const FastTrackAuditModal: React.FC<FastTrackAuditModalProps> = ({
  isOpen,
  onClose,
  barcode,
  productName
}) => {
  const [email, setEmail] = useState('');
  const [note, setNote] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [trackingId, setTrackingId] = useState<string | null>(null);

  const generateTrackingId = (): string => {
    const year = new Date().getFullYear();
    const randomStr = Math.random().toString(36).substring(2, 9).toUpperCase();
    return `TRK-${year}-${randomStr}`;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);

    const generatedTrk = generateTrackingId();

    try {
      await supabase.from('photo_review_requests').insert({
        tracking_id: generatedTrk,
        barcode,
        email: email.trim() || null,
        urgency_note: note.trim() || null,
        submission_type: 'FAST_TRACK_AUDIT',
        status: 'submitted'
      });

      AnalyticsService.track('fast_track_audit_requested', {
        trackingId: generatedTrk,
        barcode,
        hasEmail: Boolean(email.trim())
      });

      setTrackingId(generatedTrk);
    } catch {
      // Offline fallback
      setTrackingId(generatedTrk);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleClose = () => {
    setTrackingId(null);
    setEmail('');
    setNote('');
    onClose();
  };

  return (
    <AccessibleModal isOpen={isOpen} onClose={handleClose} title="Request Fast-Track Verification Audit">
      {trackingId ? (
        <div className="space-y-4 text-center py-2">
          <div className="w-12 h-12 bg-emerald-100 dark:bg-emerald-950/60 rounded-full flex items-center justify-center mx-auto text-emerald-600 dark:text-emerald-400">
            <CheckCircle2 className="w-7 h-7" />
          </div>
          <h3 className="text-lg font-extrabold text-slate-900 dark:text-white">
            Audit Request Received!
          </h3>
          <p className="text-xs text-slate-600 dark:text-slate-300 leading-relaxed max-w-md mx-auto font-medium">
            Our scientific verification team will prioritize auditing <span className="font-bold">{productName}</span>. Your request tracking ID is:
          </p>
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-slate-100 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl font-mono text-sm font-extrabold text-blue-600 dark:text-blue-400">
            <FileText className="w-4 h-4" />
            <span>{trackingId}</span>
          </div>
          <div className="pt-2">
            <button
              onClick={handleClose}
              className="px-6 py-2.5 bg-slate-900 dark:bg-slate-100 text-white dark:text-slate-900 font-extrabold text-xs rounded-xl hover:bg-slate-800 transition"
            >
              Done
            </button>
          </div>
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="space-y-4">
          <p className="text-xs text-slate-600 dark:text-slate-300 leading-relaxed font-medium">
            Requesting a fast-track audit alerts our data curation team to inspect physical label scans for GTIN <code className="font-mono text-blue-600 dark:text-blue-400 font-bold">{barcode}</code> and verify ingredient/nutrition data.
          </p>

          <div className="space-y-1.5">
            <label className="block text-xs font-bold text-slate-700 dark:text-slate-300">
              Email Address (Optional — for verification updates)
            </label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@example.com"
              className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white text-xs font-medium focus:ring-2 focus:ring-blue-500 outline-none"
            />
          </div>

          <div className="space-y-1.5">
            <label className="block text-xs font-bold text-slate-700 dark:text-slate-300">
              Urgency / Notes (Optional)
            </label>
            <textarea
              rows={3}
              value={note}
              onChange={(e) => setNote(e.target.value)}
              placeholder="e.g. Popular children's snack sold nationwide in India..."
              className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white text-xs font-medium focus:ring-2 focus:ring-blue-500 outline-none resize-none"
            />
          </div>

          <div className="pt-2 flex justify-end gap-2">
            <button
              type="button"
              onClick={handleClose}
              className="px-4 py-2.5 bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 font-bold text-xs rounded-xl hover:bg-slate-200 transition"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isSubmitting}
              className="px-5 py-2.5 bg-blue-600 hover:bg-blue-700 text-white font-extrabold text-xs rounded-xl transition flex items-center gap-2"
            >
              {isSubmitting ? <Loader2 className="w-4 h-4 animate-spin" /> : <FileSearch className="w-4 h-4" />}
              <span>Submit Audit Request</span>
            </button>
          </div>
        </form>
      )}
    </AccessibleModal>
  );
};
