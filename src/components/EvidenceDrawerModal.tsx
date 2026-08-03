import React from 'react';
import { X, ExternalLink, ShieldAlert, ShieldCheck, Info, FileText, CheckCircle2, AlertTriangle, BookOpen } from 'lucide-react';
import { Ingredient, ResearchCitation } from '../types';

interface EvidenceDrawerModalProps {
  isOpen: boolean;
  onClose: () => void;
  ingredient: Ingredient | null;
  rawName?: string;
}

export const EvidenceDrawerModal: React.FC<EvidenceDrawerModalProps> = ({
  isOpen,
  onClose,
  ingredient,
  rawName
}) => {
  if (!isOpen || !ingredient) return null;

  const isTier1 = ingredient.riskLevel === 'HIGH' || ingredient.regulatoryRecords.some(r => r.status === 'BANNED');
  const isTier2 = ingredient.riskLevel === 'MEDIUM';
  const isTier3 = ingredient.riskLevel === 'LOW';

  const tierBadge = isTier1 ? (
    <span className="px-3 py-1 rounded-full bg-rose-100 dark:bg-rose-950/80 text-rose-800 dark:text-rose-200 text-xs font-extrabold flex items-center gap-1 border border-rose-300 dark:border-rose-800">
      <AlertTriangle className="w-3.5 h-3.5 text-rose-600" />
      <span>Tier 1: Red Flag (Bold Warning + Proof)</span>
    </span>
  ) : isTier2 ? (
    <span className="px-3 py-1 rounded-full bg-amber-100 dark:bg-amber-950/80 text-amber-800 dark:text-amber-200 text-xs font-extrabold flex items-center gap-1 border border-amber-300 dark:border-amber-800">
      <Info className="w-3.5 h-3.5 text-amber-600" />
      <span>Tier 2: Nuanced Truth (Fact-Checked)</span>
    </span>
  ) : (
    <span className="px-3 py-1 rounded-full bg-emerald-100 dark:bg-emerald-950/80 text-emerald-800 dark:text-emerald-200 text-xs font-extrabold flex items-center gap-1 border border-emerald-300 dark:border-emerald-800">
      <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
      <span>Tier 3: Clean / Natural Ingredient</span>
    </span>
  );

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/70 backdrop-blur-md animate-fade-in">
      <div 
        className="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 w-full max-w-2xl max-h-[90vh] overflow-y-auto shadow-2xl space-y-6 p-6 sm:p-8 relative"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-6 right-6 p-2 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-500 dark:text-slate-400 hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors"
        >
          <X className="w-5 h-5" />
        </button>

        {/* Modal Header */}
        <div className="space-y-3 border-b border-slate-100 dark:border-slate-800 pb-5">
          <div className="flex flex-wrap items-center gap-2">
            {tierBadge}
            {ingredient.eNumber && (
              <span className="px-2.5 py-0.5 rounded-md bg-slate-100 dark:bg-slate-800 font-mono text-xs font-bold text-slate-700 dark:text-slate-300">
                {ingredient.eNumber}
              </span>
            )}
            {ingredient.insNumber && (
              <span className="px-2.5 py-0.5 rounded-md bg-slate-100 dark:bg-slate-800 font-mono text-xs font-bold text-slate-700 dark:text-slate-300">
                INS {ingredient.insNumber}
              </span>
            )}
          </div>

          <h2 className="text-2xl font-extrabold text-slate-900 dark:text-white tracking-tight">
            {ingredient.canonicalName}
          </h2>

          <p className="text-xs text-slate-500 dark:text-slate-400">
            Raw Package Label: <span className="font-semibold text-slate-700 dark:text-slate-300">"{rawName || ingredient.canonicalName}"</span> • Functional Category: <span className="font-semibold text-slate-700 dark:text-slate-300">{ingredient.category}</span>
          </p>
        </div>

        {/* Section 1: Reality & Health Context */}
        <div className="space-y-2">
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400 flex items-center gap-1.5">
            <FileText className="w-4 h-4 text-blue-600 dark:text-blue-400" />
            Reality & Health Context
          </h3>

          <div className="p-4 rounded-2xl bg-slate-50 dark:bg-slate-800/80 border border-slate-200/80 dark:border-slate-700/80 text-xs text-slate-800 dark:text-slate-200 leading-relaxed font-medium">
            {ingredient.description}
          </div>
        </div>

        {/* Section 2: Global Regulatory Status Matrix */}
        <div className="space-y-2">
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400 flex items-center gap-1.5">
            <ShieldCheck className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
            Global Jurisdictional Status (6 Authorities)
          </h3>

          <div className="grid grid-cols-2 sm:grid-cols-3 gap-2.5">
            {ingredient.regulatoryRecords.map((r) => (
              <div
                key={r.countryCode}
                className="p-3 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 space-y-1"
              >
                <div className="flex items-center justify-between">
                  <span className="font-bold text-xs text-slate-900 dark:text-white">
                    {r.flagEmoji} {r.countryName}
                  </span>
                  <span className={`font-extrabold font-mono text-[10px] ${
                    r.status === 'BANNED'
                      ? 'text-rose-600 dark:text-rose-400'
                      : r.status === 'RESTRICTED'
                      ? 'text-amber-600 dark:text-amber-400'
                      : 'text-emerald-600 dark:text-emerald-400'
                  }`}>
                    {r.status}
                  </span>
                </div>
                {r.restrictionDetails && (
                  <p className="text-[10px] text-slate-500 dark:text-slate-400 leading-tight">
                    {r.restrictionDetails}
                  </p>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Section 3: Verified Proof & Direct Citation Links */}
        <div className="space-y-3 pt-2">
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400 flex items-center gap-1.5">
            <BookOpen className="w-4 h-4 text-indigo-600 dark:text-indigo-400" />
            Verified Proof & Official Regulatory Citations
          </h3>

          {ingredient.citations && ingredient.citations.length > 0 ? (
            <div className="space-y-2.5">
              {ingredient.citations.map((c) => (
                <div
                  key={c.id}
                  className="p-4 rounded-2xl bg-blue-50/50 dark:bg-blue-950/30 border border-blue-200/80 dark:border-blue-900/60 space-y-2 text-xs"
                >
                  <div className="flex items-start justify-between gap-3">
                    <div>
                      <h4 className="font-bold text-slate-900 dark:text-white">
                        {c.title}
                      </h4>
                      <p className="text-[11px] text-slate-600 dark:text-slate-300 mt-1">
                        {c.summary}
                      </p>
                    </div>

                    <span className="px-2 py-0.5 rounded bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 font-mono text-[10px] font-bold shrink-0">
                      {c.evidenceStrength}
                    </span>
                  </div>

                  <div className="pt-1 flex items-center justify-between text-[11px]">
                    <span className="text-slate-500 dark:text-slate-400 font-medium">
                      Authority: {c.journal} ({c.year})
                    </span>

                    {c.doi && (
                      <a
                        href={c.doi.startsWith('http') ? c.doi : `https://doi.org/${c.doi}`}
                        target="_blank"
                        rel="noreferrer"
                        className="inline-flex items-center gap-1.5 px-3 py-1 rounded-lg bg-blue-600 hover:bg-blue-700 text-white font-bold text-[11px] shadow-sm transition-all"
                      >
                        <span>Read Official Study</span>
                        <ExternalLink className="w-3 h-3" />
                      </a>
                    )}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="p-4 rounded-2xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-xs text-slate-500 dark:text-slate-400 text-center">
              Standard food ingredient. Approved globally across FSSAI, EFSA, FDA, and Codex Alimentarius.
            </div>
          )}
        </div>

        {/* Modal Footer Action */}
        <div className="pt-4 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between text-xs">
          <span className="text-slate-400 font-mono">FoodFactsIndia Audit ID: {ingredient.id}</span>
          <button
            onClick={onClose}
            className="px-5 py-2 rounded-xl bg-slate-900 dark:bg-white text-white dark:text-slate-900 font-bold text-xs hover:opacity-90 transition-opacity"
          >
            Close Evidence Drawer
          </button>
        </div>

      </div>
    </div>
  );
};
