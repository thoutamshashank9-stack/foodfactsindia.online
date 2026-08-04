import React from 'react';
import { TransparencyReport } from '../types';
import { ProductImage } from './ProductImage';
import { ShieldAlert, Upload, Clock, FileSearch, ArrowLeft } from 'lucide-react';

interface UnverifiedProductStubViewProps {
  report: TransparencyReport;
  onBack?: () => void;
}

export const UnverifiedProductStubView: React.FC<UnverifiedProductStubViewProps> = ({
  report,
  onBack
}) => {
  const pageState = report.pageState || (report.isScoreWithheld ? 'insufficient_data' : 'awaiting_images');

  const stateConfig = {
    awaiting_images: {
      badge: 'No Verified Package Evidence',
      color: 'bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 border-slate-300 dark:border-slate-700',
      icon: Upload,
      title: 'Package Label Evidence Needed',
      message: 'We do not have verified physical package label photos for this GTIN. Upload images of the ingredients and nutrition facts panel to initiate analysis.'
    },
    processing: {
      badge: 'OCR & AI Extraction Running',
      color: 'bg-blue-50 dark:bg-blue-950/80 text-blue-800 dark:text-blue-200 border-blue-300 dark:border-blue-800',
      icon: Clock,
      title: 'Label Extraction in Progress',
      message: 'Physical label images have been submitted and are currently undergoing Optical Character Recognition and structured ingredient extraction.'
    },
    insufficient_data: {
      badge: 'Insufficient Source Data — Ratings Withheld',
      color: 'bg-amber-50 dark:bg-amber-950/80 text-amber-900 dark:text-amber-200 border-amber-300 dark:border-amber-800',
      icon: ShieldAlert,
      title: 'Insufficient Verified Package Data',
      message: report.scoreWithheldReason || 'Detailed ingredients list or nutritional facts panel for this product GTIN are unparsed or pending manufacturer verification. Scores and ratings are strictly withheld to prevent false clean ratings.'
    },
    needs_review: {
      badge: 'Under Expert Review',
      color: 'bg-indigo-50 dark:bg-indigo-950/80 text-indigo-900 dark:text-indigo-200 border-indigo-300 dark:border-indigo-800',
      icon: FileSearch,
      title: 'Human Moderation Audit Pending',
      message: 'Structured data has been extracted but flagged for review due to label contradictions or policy checks. Our scientific review team will audit this product shortly.'
    },
    superseded: {
      badge: 'Archived Snapshot',
      color: 'bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 border-slate-300 dark:border-slate-700',
      icon: Clock,
      title: 'Superseded Report Snapshot',
      message: 'This report version has been archived and replaced by a newer verified product snapshot.'
    },
    verified_published: {
      badge: 'Verified Published',
      color: 'bg-emerald-50 text-emerald-800 border-emerald-300',
      icon: ShieldAlert,
      title: 'Verified Published',
      message: 'Verified published report.'
    }
  }[pageState];

  const IconComp = stateConfig.icon;

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      
      {/* Back Button */}
      {onBack && (
        <button
          onClick={onBack}
          className="inline-flex items-center gap-2 text-xs font-bold text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white transition-colors min-h-[44px] px-2"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Product Search</span>
        </button>
      )}

      {/* Product Identity Header Card */}
      <div className="p-6 sm:p-8 rounded-3xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-xl space-y-6">
        
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

            {/* Neutral State Badge */}
            <div className="pt-1">
              <span className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-extrabold border ${stateConfig.color}`}>
                <IconComp className="w-4 h-4 shrink-0" />
                <span>{stateConfig.badge}</span>
              </span>
            </div>
          </div>
        </div>

        {/* State Explanation Banner */}
        <div className={`p-5 rounded-2xl border ${stateConfig.color} space-y-2`}>
          <h3 className="text-sm font-extrabold flex items-center gap-2">
            <IconComp className="w-4 h-4 shrink-0" />
            <span>{stateConfig.title}</span>
          </h3>
          <p className="text-xs leading-relaxed font-medium opacity-90">
            {stateConfig.message}
          </p>
        </div>

        {/* Action CTAs */}
        <div className="pt-2 flex flex-col sm:flex-row gap-3">
          <button className="flex-1 py-3 px-4 rounded-2xl bg-slate-900 dark:bg-slate-100 text-white dark:text-slate-900 font-bold text-xs hover:bg-blue-600 dark:hover:bg-blue-400 transition-colors flex items-center justify-center gap-2 min-h-[44px]">
            <Upload className="w-4 h-4" />
            <span>Upload Package Label Photos</span>
          </button>
          <button className="flex-1 py-3 px-4 rounded-2xl bg-slate-100 dark:bg-slate-800 text-slate-900 dark:text-white font-bold text-xs hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors flex items-center justify-center gap-2 min-h-[44px] border border-slate-200 dark:border-slate-700">
            <FileSearch className="w-4 h-4" />
            <span>Request Fast-Track Audit</span>
          </button>
        </div>

      </div>

    </div>
  );
};
