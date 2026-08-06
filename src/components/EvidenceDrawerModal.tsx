import React from 'react';
import { X, ExternalLink, ShieldAlert, ShieldCheck, CheckCircle2, AlertTriangle, BookOpen, FileText } from 'lucide-react';
import { Ingredient } from '../types';

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

  const bannedRecords = ingredient.regulatoryRecords?.filter(r => r.status === 'BANNED') || [];
  const isBanned = bannedRecords.length > 0;

  const tierBadge = isBanned ? (
    <span className="px-2.5 py-1 rounded bg-rose-100 dark:bg-rose-950/80 text-rose-800 dark:text-rose-200 text-xs font-bold flex items-center gap-1 border border-rose-300 dark:border-rose-800">
      <AlertTriangle className="w-3.5 h-3.5 text-rose-600" />
      <span>Banned Additive / High Alert</span>
    </span>
  ) : ingredient.riskLevel === 'MEDIUM' ? (
    <span className="px-2.5 py-1 rounded bg-amber-100 dark:bg-amber-950/80 text-amber-800 dark:text-amber-200 text-xs font-bold flex items-center gap-1 border border-amber-300 dark:border-amber-800">
      <ShieldAlert className="w-3.5 h-3.5 text-amber-600" />
      <span>Restricted / Caution</span>
    </span>
  ) : (
    <span className="px-2.5 py-1 rounded bg-emerald-100 dark:bg-emerald-950/80 text-emerald-800 dark:text-emerald-200 text-xs font-bold flex items-center gap-1 border border-emerald-300 dark:border-emerald-800">
      <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
      <span>Approved / Whole Food</span>
    </span>
  );

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-stone-900/60 dark:bg-black/80 backdrop-blur-sm animate-fade-in">
      <div 
        className="bg-[#fcfbf9] dark:bg-[#161b22] rounded-lg border border-stone-200 dark:border-stone-800 w-full max-w-xl max-h-[90vh] overflow-y-auto shadow-xl space-y-5 p-6 relative text-[#1c2128] dark:text-[#e6edf3]"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-5 right-5 p-1.5 rounded bg-stone-100 dark:bg-stone-800 text-stone-500 hover:text-stone-900 dark:hover:text-stone-100 transition-colors"
        >
          <X className="w-4 h-4" />
        </button>

        {/* Modal Header */}
        <div className="space-y-2 border-b border-stone-200 dark:border-stone-800 pb-4">
          <div className="flex flex-wrap items-center gap-2">
            {tierBadge}
            {ingredient.eNumber && (
              <span className="px-2 py-0.5 rounded bg-stone-100 dark:bg-stone-800 font-mono text-xs font-semibold text-stone-700 dark:text-stone-300">
                {ingredient.eNumber}
              </span>
            )}
            {ingredient.insNumber && (
              <span className="px-2 py-0.5 rounded bg-stone-100 dark:bg-stone-800 font-mono text-xs font-semibold text-stone-700 dark:text-stone-300">
                INS {ingredient.insNumber}
              </span>
            )}
          </div>

          <h2 className="font-serif text-2xl font-semibold text-stone-900 dark:text-stone-100">
            {ingredient.canonicalName}
          </h2>

          <p className="text-xs text-stone-500 dark:text-stone-400">
            Declared Raw Label Name: <span className="font-medium text-stone-700 dark:text-stone-300">"{rawName || ingredient.canonicalName}"</span> • Category: <span className="font-medium text-stone-700 dark:text-stone-300">{ingredient.category}</span>
          </p>
        </div>

        {/* Banned Alert Banner (Bubbled to top) */}
        {isBanned && (
          <div className="p-4 rounded bg-rose-50 dark:bg-rose-950/20 border border-rose-200 dark:border-rose-800 text-xs text-rose-950 dark:text-rose-200 space-y-2">
            <h4 className="font-bold uppercase tracking-wider flex items-center gap-1.5 text-rose-800 dark:text-rose-400 text-[11px]">
              <AlertTriangle className="w-4 h-4 text-rose-600 dark:text-rose-400" />
              Banned Additive Alert
            </h4>
            <p className="leading-relaxed font-medium">
              This ingredient is officially **BANNED** in: {bannedRecords.map(r => `${r.flagEmoji || ''} ${r.countryName || r.countryCode}`).join(', ')}.
            </p>
            <div className="text-[11px] space-y-1 opacity-90">
              {bannedRecords.map((r, idx) => (
                <div key={r.countryCode || idx}>
                  <strong>• {r.countryName || r.countryCode}:</strong> Banned under regulation: <em>{r.regulationRef}</em>. {r.restrictionDetails && `Reason: ${r.restrictionDetails}`}
                </div>
              ))}
            </div>
            <div className="pt-1 text-[11px] border-t border-rose-200 dark:border-rose-800/60 leading-relaxed text-rose-900 dark:text-rose-300">
              <strong>Why it is harmful:</strong> {ingredient.description || 'Prohibited food additive associated with toxicological or carcinogenicity concerns.'}
            </div>
          </div>
        )}

        {/* Section 1: Reality & Health Context */}
        {!isBanned && (
          <div className="space-y-2">
            <h3 className="text-xs font-semibold uppercase tracking-wider text-stone-500 dark:text-stone-400 flex items-center gap-1.5">
              <FileText className="w-3.5 h-3.5 text-teal-800 dark:text-teal-400" />
              Reality & Health Context
            </h3>

            <div className="p-3.5 rounded bg-stone-50 dark:bg-stone-800/40 border border-stone-200 dark:border-stone-800 text-xs leading-relaxed">
              {ingredient.description}
            </div>
          </div>
        )}

        {/* Section 2: Global Regulatory Status Matrix */}
        <div className="space-y-2">
          <h3 className="text-xs font-semibold uppercase tracking-wider text-stone-500 dark:text-stone-400 flex items-center gap-1.5">
            <ShieldCheck className="w-3.5 h-3.5 text-teal-800 dark:text-teal-400" />
            Global Jurisdictional Status (6 Authorities)
          </h3>

          <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
            {ingredient.regulatoryRecords.map((r) => (
              <div
                key={r.countryCode}
                className={`p-2.5 rounded border text-xs space-y-1 ${
                  r.status === 'BANNED'
                    ? 'bg-rose-50/40 dark:bg-rose-950/15 border-rose-200 dark:border-rose-800/80'
                    : r.status === 'RESTRICTED'
                    ? 'bg-amber-50/40 dark:bg-amber-950/15 border-amber-200 dark:border-amber-800/80'
                    : 'bg-stone-50 dark:bg-stone-800/40 border-stone-200 dark:border-stone-800'
                }`}
              >
                <div className="flex items-center justify-between font-semibold">
                  <span>
                    {r.flagEmoji} {r.countryCode}
                  </span>
                  <span className={`text-[10px] uppercase font-bold ${
                    r.status === 'BANNED'
                      ? 'text-rose-700 dark:text-rose-400'
                      : r.status === 'RESTRICTED'
                      ? 'text-amber-700 dark:text-amber-400'
                      : 'text-emerald-700 dark:text-emerald-400'
                  }`}>
                    {r.status}
                  </span>
                </div>
                {r.restrictionDetails && (
                  <p className="text-[10px] text-stone-500 dark:text-stone-400 leading-tight">
                    {r.restrictionDetails}
                  </p>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Section 3: Verified Proof & Citations */}
        <div className="space-y-2 pt-1">
          <h3 className="text-xs font-semibold uppercase tracking-wider text-stone-500 dark:text-stone-400 flex items-center gap-1.5">
            <BookOpen className="w-3.5 h-3.5 text-teal-800 dark:text-teal-400" />
            Verified Regulatory Citations & Scientific Proof
          </h3>

          {ingredient.citations && ingredient.citations.length > 0 ? (
            <div className="space-y-2">
              {ingredient.citations.map((c) => (
                <div
                  key={c.id}
                  className="p-3 rounded bg-stone-50 dark:bg-stone-800/40 border border-stone-200 dark:border-stone-800 space-y-1.5 text-xs"
                >
                  <div className="flex items-start justify-between gap-3">
                    <div>
                      <h4 className="font-semibold text-stone-900 dark:text-stone-100">
                        {c.title}
                      </h4>
                      <p className="text-[11px] text-stone-600 dark:text-stone-400 mt-0.5 leading-relaxed">
                        {c.summary}
                      </p>
                    </div>
                    <span className="px-1.5 py-0.5 rounded bg-stone-200 dark:bg-stone-800 text-stone-700 dark:text-stone-300 font-mono text-[9px] font-semibold shrink-0">
                      {c.evidenceStrength}
                    </span>
                  </div>

                  <div className="pt-1 flex items-center justify-between text-[10px] text-stone-500 dark:text-stone-400">
                    <span>
                      Authority: {c.journal} ({c.year})
                    </span>

                    {c.doi && (
                      <a
                        href={c.doi.startsWith('http') ? c.doi : `https://doi.org/${c.doi}`}
                        target="_blank"
                        rel="noreferrer"
                        className="inline-flex items-center gap-1 text-teal-800 dark:text-teal-400 hover:underline"
                      >
                        <span>Official Study</span>
                        <ExternalLink className="w-2.5 h-2.5" />
                      </a>
                    )}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="p-3 rounded bg-stone-50 dark:bg-stone-800/40 border border-stone-200 dark:border-stone-800 text-xs text-stone-500 dark:text-stone-400 text-center">
              Approved globally across FSSAI, EFSA, FDA, and Codex Alimentarius.
            </div>
          )}
        </div>

        {/* Modal Footer */}
        <div className="pt-3 border-t border-stone-200 dark:border-stone-800 flex items-center justify-between text-[11px] text-stone-400">
          <span>Audit ID: {ingredient.id}</span>
          <button
            onClick={onClose}
            className="px-4 py-1.5 rounded bg-stone-900 dark:bg-stone-100 text-white dark:text-stone-900 font-medium text-xs hover:opacity-90 transition-opacity"
          >
            Close
          </button>
        </div>

      </div>
    </div>
  );
};
