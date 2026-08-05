import React, { useState } from 'react';
import { TransparencyReport } from '../types';
import { ProductImage } from './ProductImage';
import { LabelUploadCard } from './LabelUploadCard';
import { FastTrackAuditModal } from './FastTrackAuditModal';
import { PRESEEDED_PRODUCTS } from '../data/productsDatabase';
import {
  ShieldAlert,
  Clock,
  FileSearch,
  ArrowLeft,
  ArrowRight,
  CheckCircle2,
  Upload,
  MessageSquareWarning,
} from 'lucide-react';

// ─── Props ────────────────────────────────────────────────────────────────────

interface UnverifiedProductStubViewProps {
  report: TransparencyReport;
  onBack?: () => void;
  onSelectAlternative?: (barcode: string) => void;
}

// ─── State configuration map ──────────────────────────────────────────────────

const STATE_CONFIG = {
  awaiting_images: {
    badge: 'Label Photos Needed',
    badgeColor: 'bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 border-slate-300 dark:border-slate-700',
    bannerColor: 'border-amber-200 dark:border-amber-800 bg-amber-50 dark:bg-amber-950/40',
    bannerTitleColor: 'text-amber-900 dark:text-amber-200',
    bannerBodyColor: 'text-amber-800 dark:text-amber-300',
    icon: Upload,
    bannerTitle: "We don't have enough verified package data yet.",
    bannerBody:
      "We found this product barcode, but we can't generate a trusted report until the ingredients list and nutrition panel are verified from the package. Upload clear photos of the package so we can extract the label data and build the report.",
    showUploadCard: true,
  },
  insufficient_data: {
    badge: 'Ratings Withheld',
    badgeColor: 'bg-amber-50 dark:bg-amber-950/80 text-amber-900 dark:text-amber-200 border-amber-300 dark:border-amber-800',
    bannerColor: 'border-amber-200 dark:border-amber-800 bg-amber-50 dark:bg-amber-950/40',
    bannerTitleColor: 'text-amber-900 dark:text-amber-200',
    bannerBodyColor: 'text-amber-800 dark:text-amber-300',
    icon: ShieldAlert,
    bannerTitle: "We don't have enough verified package data yet.",
    bannerBody:
      "Upload ingredients and nutrition label photos to generate or improve this report. All scores and ratings are withheld until we can verify the label data directly from the physical package.",
    showUploadCard: true,
  },
  processing: {
    badge: 'Extracting Label Data',
    badgeColor: 'bg-blue-50 dark:bg-blue-950/80 text-blue-800 dark:text-blue-200 border-blue-300 dark:border-blue-800',
    bannerColor: 'border-blue-200 dark:border-blue-800 bg-blue-50 dark:bg-blue-950/40',
    bannerTitleColor: 'text-blue-900 dark:text-blue-200',
    bannerBodyColor: 'text-blue-800 dark:text-blue-300',
    icon: Clock,
    bannerTitle: 'Label extraction in progress.',
    bannerBody:
      "Your label images are in our verification queue. We're running OCR and structured extraction — we'll update this page once the report is ready.",
    showUploadCard: false,
  },
  needs_review: {
    badge: 'In Moderation Review',
    badgeColor: 'bg-indigo-50 dark:bg-indigo-950/80 text-indigo-900 dark:text-indigo-200 border-indigo-300 dark:border-indigo-800',
    bannerColor: 'border-indigo-200 dark:border-indigo-800 bg-indigo-50 dark:bg-indigo-950/40',
    bannerTitleColor: 'text-indigo-900 dark:text-indigo-200',
    bannerBodyColor: 'text-indigo-800 dark:text-indigo-300',
    icon: FileSearch,
    bannerTitle: 'Human moderation audit pending.',
    bannerBody:
      'Structured data has been extracted but is flagged for review due to label contradictions or policy checks. Our scientific review team is auditing this product.',
    showUploadCard: false,
  },
  superseded: {
    badge: 'Archived Snapshot',
    badgeColor: 'bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 border-slate-300 dark:border-slate-700',
    bannerColor: 'border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-900/60',
    bannerTitleColor: 'text-slate-700 dark:text-slate-300',
    bannerBodyColor: 'text-slate-600 dark:text-slate-400',
    icon: Clock,
    bannerTitle: 'This report snapshot has been superseded.',
    bannerBody:
      'This version has been archived and replaced by a newer verified product snapshot. Use the back button to find the current report.',
    showUploadCard: false,
  },
  verified_published: {
    badge: 'Verified Published',
    badgeColor: 'bg-emerald-50 text-emerald-800 border-emerald-300',
    bannerColor: 'border-emerald-200 bg-emerald-50 dark:bg-emerald-950/40',
    bannerTitleColor: 'text-emerald-900 dark:text-emerald-200',
    bannerBodyColor: 'text-emerald-800 dark:text-emerald-300',
    icon: CheckCircle2,
    bannerTitle: 'Verified published report.',
    bannerBody: 'This report is fully verified from physical package label data.',
    showUploadCard: false,
  },
} as const;

// ─── Component ────────────────────────────────────────────────────────────────

export const UnverifiedProductStubView: React.FC<UnverifiedProductStubViewProps> = ({
  report,
  onBack,
  onSelectAlternative,
}) => {
  const [showAuditModal, setShowAuditModal] = useState(false);
  const [showReportForm, setShowReportForm] = useState(false);
  const [reportFormValue, setReportFormValue] = useState('');
  const [reportFormSubmitted, setReportFormSubmitted] = useState(false);
  const [uploadSuccessId, setUploadSuccessId] = useState<string | null>(null);

  const pageState =
    (report.pageState as keyof typeof STATE_CONFIG) ??
    (report.isScoreWithheld ? 'insufficient_data' : 'awaiting_images');

  const cfg = STATE_CONFIG[pageState] ?? STATE_CONFIG.awaiting_images;
  const IconComp = cfg.icon;

  // Verified alternatives for cross-sell block
  const verifiedAlternatives = PRESEEDED_PRODUCTS.filter(
    (p) => p.barcode !== report.barcode && (!p.pageState || p.pageState === 'verified_published')
  ).slice(0, 3);

  const handleReportSubmit = () => {
    if (!reportFormValue.trim()) return;
    setReportFormSubmitted(true);
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8">

      {/* ── Back navigation ──────────────────────────────────────────────── */}
      {onBack && (
        <button
          onClick={onBack}
          className="inline-flex items-center gap-2 text-xs font-bold text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white transition-colors min-h-[44px] px-2 focus:outline-none focus:ring-2 focus:ring-slate-400 focus:ring-offset-2 rounded-lg"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Product Search</span>
        </button>
      )}

      {/* ── Product identity card ─────────────────────────────────────────── */}
      <div className="p-6 sm:p-8 rounded-3xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-xl space-y-6">

        {/* Product summary block */}
        <div className="flex flex-col sm:flex-row items-center sm:items-start gap-6 text-center sm:text-left">
          <ProductImage
            barcode={report.barcode}
            productName={report.productName}
            className="w-32 h-32 sm:w-36 sm:h-36 rounded-2xl object-cover border-2 border-slate-200 dark:border-slate-700 shadow-md shrink-0"
          />

          <div className="space-y-3 flex-1">
            <div className="flex flex-wrap items-center justify-center sm:justify-start gap-2">
              <span className="text-xs font-extrabold uppercase tracking-wider text-slate-500 dark:text-slate-400">
                {report.brand}
              </span>
              <span className="text-[11px] text-slate-400 dark:text-slate-500 font-mono">
                • GTIN: {report.barcode}
              </span>
            </div>

            <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white tracking-tight">
              {report.productName}
            </h1>

            <p className="text-xs text-slate-500 dark:text-slate-400 font-medium">
              {report.category} • Pack Size: {report.packageSize}
            </p>

            <div className="pt-1">
              <span
                className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-extrabold border ${cfg.badgeColor}`}
              >
                <IconComp className="w-4 h-4 shrink-0" aria-hidden="true" />
                <span>{cfg.badge}</span>
              </span>
            </div>
          </div>
        </div>

        {/* Status banner — exact copy spec */}
        <div className={`p-5 rounded-2xl border space-y-1.5 ${cfg.bannerColor}`} role="status">
          <h2 className={`text-sm font-extrabold flex items-center gap-2 ${cfg.bannerTitleColor}`}>
            <IconComp className="w-4 h-4 shrink-0" aria-hidden="true" />
            {cfg.bannerTitle}
          </h2>
          <p className={`text-xs leading-relaxed font-medium ${cfg.bannerBodyColor}`}>
            {report.stateMessage ?? cfg.bannerBody}
          </p>
        </div>

        {/* Upload success banner (shown after submission) */}
        {uploadSuccessId && (
          <div
            role="status"
            aria-live="polite"
            className="flex items-start gap-3 p-4 rounded-2xl border border-emerald-200 dark:border-emerald-800 bg-emerald-50 dark:bg-emerald-950/40"
          >
            <CheckCircle2 className="w-5 h-5 text-emerald-600 shrink-0 mt-0.5" />
            <div>
              <p className="text-sm font-extrabold text-emerald-900 dark:text-emerald-200">
                Thanks — your package photos were submitted for verification.
              </p>
              <p className="text-xs text-emerald-700 dark:text-emerald-300 mt-0.5">
                Tracking ID:{' '}
                <span className="font-mono font-bold">{uploadSuccessId}</span>
              </p>
            </div>
          </div>
        )}

        {/* ── Upload card (shown for awaiting / insufficient states) ──────── */}
        {cfg.showUploadCard && !uploadSuccessId && (
          <LabelUploadCard
            barcode={report.barcode}
            productId={report.productId}
            onSuccess={(trk) => setUploadSuccessId(trk)}
            onReportData={() => setShowReportForm(true)}
          />
        )}

        {/* ── Fast-Track Audit CTA (for processing / needs_review states) ── */}
        {!cfg.showUploadCard && pageState !== 'verified_published' && pageState !== 'superseded' && (
          <div className="pt-2 flex flex-col sm:flex-row gap-3">
            <button
              onClick={() => setShowAuditModal(true)}
              className="flex-1 inline-flex min-h-[44px] items-center justify-center gap-2 py-3 px-5 rounded-2xl bg-slate-900 dark:bg-slate-100 text-white dark:text-slate-900 font-extrabold text-xs hover:bg-blue-600 dark:hover:bg-blue-400 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
            >
              <FileSearch className="w-4 h-4" />
              Request Fast-Track Audit
            </button>
            <button
              onClick={() => setShowReportForm(true)}
              className="flex-1 inline-flex min-h-[44px] items-center justify-center gap-2 py-3 px-5 rounded-2xl bg-slate-100 dark:bg-slate-800 text-slate-900 dark:text-white font-extrabold text-xs hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors focus:outline-none focus:ring-2 focus:ring-slate-400 focus:ring-offset-2 border border-slate-200 dark:border-slate-700"
            >
              <MessageSquareWarning className="w-4 h-4" />
              Report wrong or missing data
            </button>
          </div>
        )}

        {/* ── Inline "Report wrong data" mini form ─────────────────────── */}
        {showReportForm && (
          <div
            className="mt-1 rounded-2xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 p-5 space-y-3 animate-in fade-in slide-in-from-top-1 duration-150"
            role="region"
            aria-label="Report wrong or missing data"
          >
            {reportFormSubmitted ? (
              <div className="flex items-start gap-2 text-emerald-700 dark:text-emerald-300">
                <CheckCircle2 className="w-4 h-4 shrink-0 mt-0.5" />
                <p className="text-sm font-semibold">
                  Thanks — we'll review your feedback and update this product entry.
                </p>
              </div>
            ) : (
              <>
                <label
                  htmlFor="report-field"
                  className="block text-xs font-bold text-slate-800 dark:text-slate-200"
                >
                  What's wrong or missing?
                </label>
                <textarea
                  id="report-field"
                  rows={3}
                  value={reportFormValue}
                  onChange={(e) => setReportFormValue(e.target.value)}
                  placeholder="Describe the issue — e.g. wrong ingredients, outdated pack size, incorrect barcode mapping…"
                  className="w-full rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 px-3 py-2.5 text-xs text-slate-700 dark:text-slate-200 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-1 resize-none"
                />
                <div className="flex justify-end gap-2">
                  <button
                    type="button"
                    onClick={() => setShowReportForm(false)}
                    className="text-xs font-medium text-slate-500 hover:text-slate-700 dark:hover:text-slate-300 transition-colors min-h-[36px] px-3"
                  >
                    Cancel
                  </button>
                  <button
                    type="button"
                    onClick={handleReportSubmit}
                    disabled={!reportFormValue.trim()}
                    className="inline-flex min-h-[36px] items-center gap-1.5 rounded-xl bg-blue-600 px-4 py-2 text-xs font-bold text-white hover:bg-blue-700 disabled:opacity-50 disabled:pointer-events-none transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-1"
                  >
                    Send report
                  </button>
                </div>
              </>
            )}
          </div>
        )}
      </div>

      {/* ── Verified alternatives block ───────────────────────────────────── */}
      {verifiedAlternatives.length > 0 && (
        <div className="p-6 sm:p-8 rounded-3xl bg-slate-50 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 space-y-4">
          <div>
            <h3 className="text-sm font-extrabold text-slate-900 dark:text-white flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-500" />
              Looking for a verified product?
            </h3>
            <p className="text-xs text-slate-500 dark:text-slate-400 font-medium mt-0.5">
              These products have fully verified label reports available:
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            {verifiedAlternatives.map((alt) => (
              <button
                key={alt.barcode}
                onClick={() => onSelectAlternative?.(alt.barcode)}
                className="text-left p-4 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 hover:border-blue-500 dark:hover:border-blue-500 shadow-sm hover:shadow-md transition-all space-y-3 group focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                aria-label={`View report for ${alt.productName}`}
              >
                <div className="flex items-center gap-3">
                  <ProductImage
                    barcode={alt.barcode}
                    productName={alt.productName}
                    className="w-12 h-12 rounded-xl object-cover border border-slate-200 dark:border-slate-700 shrink-0"
                  />
                  <div className="min-w-0 flex-1">
                    <span className="text-[10px] font-extrabold uppercase tracking-wider text-slate-400 block truncate">
                      {alt.brand}
                    </span>
                    <h4 className="text-xs font-extrabold text-slate-900 dark:text-white truncate group-hover:text-blue-600 transition-colors">
                      {alt.productName}
                    </h4>
                  </div>
                </div>

                <div className="flex items-center justify-between pt-1 border-t border-slate-100 dark:border-slate-800 text-xs">
                  <span className="font-extrabold text-emerald-600 dark:text-emerald-400">
                    Grade {alt.executiveSummary.grade} ({alt.deterministicScore}/100)
                  </span>
                  <ArrowRight className="w-3.5 h-3.5 text-slate-400 group-hover:translate-x-1 transition-transform" />
                </div>
              </button>
            ))}
          </div>
        </div>
      )}

      {/* ── Fast-Track Audit modal ────────────────────────────────────────── */}
      <FastTrackAuditModal
        isOpen={showAuditModal}
        onClose={() => setShowAuditModal(false)}
        barcode={report.barcode}
        productName={report.productName}
      />
    </div>
  );
};
