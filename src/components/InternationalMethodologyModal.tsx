import React from 'react';
import { X, Globe, CheckCircle2, FileText, AlertCircle } from 'lucide-react';
import { InternationalRatings } from '../types';

interface InternationalMethodologyModalProps {
  isOpen: boolean;
  onClose: () => void;
  ratings?: InternationalRatings;
}

export const InternationalMethodologyModal: React.FC<InternationalMethodologyModalProps> = ({
  isOpen,
  onClose,
  ratings,
}) => {
  if (!isOpen || !ratings) return null;

  const { nutriScore, fdaLabel, warningOctagons } = ratings;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-fade-in">
      <div className="relative w-full max-w-3xl bg-white dark:bg-slate-900 rounded-2xl shadow-2xl border border-slate-200 dark:border-slate-800 overflow-hidden flex flex-col max-h-[90vh]">
        
        {/* Modal Header */}
        <div className="p-5 border-b border-slate-100 dark:border-slate-800 flex items-center justify-between bg-slate-50/50 dark:bg-slate-850/50">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-xl bg-blue-100 dark:bg-blue-900/50 text-blue-600 dark:text-blue-400">
              <Globe className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-lg font-bold text-slate-900 dark:text-white">
                Multi-Country Rating System Methodology
              </h3>
              <p className="text-xs text-slate-500 dark:text-slate-400">
                Official EU Nutri-Score (2024), Mexican NOM-051 Octagons & US FDA %DV Rules
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors min-h-[44px] min-w-[44px]"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Scroll Content */}
        <div className="p-6 overflow-y-auto space-y-6 text-xs leading-relaxed text-slate-700 dark:text-slate-300">
          
          {/* SECTION 1: EU NUTRI-SCORE */}
          <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-850 border border-slate-200 dark:border-slate-800 space-y-3">
            <div className="flex items-center justify-between">
              <h4 className="font-bold text-sm text-slate-900 dark:text-white flex items-center gap-1.5">
                <span>🇪🇺</span> EU Nutri-Score (2023/2024 Revision)
              </h4>
              <span className="font-mono font-bold px-2 py-0.5 rounded bg-blue-100 dark:bg-blue-900/50 text-blue-700 dark:text-blue-300 text-xs">
                Grade: {nutriScore.grade} (Score: {nutriScore.score})
              </span>
            </div>
            <p>
              Calculated using the updated 2023/2024 Scientific Committee algorithm implemented across France, Germany, Spain, and Belgium.
            </p>

            <div className="grid grid-cols-2 gap-3 pt-2">
              <div className="p-3 rounded-lg bg-rose-50 dark:bg-rose-950/30 border border-rose-100 dark:border-rose-900/40">
                <div className="font-bold text-rose-900 dark:text-rose-200 mb-1">
                  Negative Points (N = {nutriScore.negativePoints})
                </div>
                <ul className="space-y-0.5 text-[11px] font-mono">
                  <li>• Energy: +{nutriScore.breakdown.energyPoints} pts</li>
                  <li>• Total Sugars: +{nutriScore.breakdown.sugarsPoints} pts</li>
                  <li>• Saturated Fat: +{nutriScore.breakdown.satFatPoints} pts</li>
                  <li>• Salt: +{nutriScore.breakdown.sodiumPoints} pts</li>
                </ul>
              </div>

              <div className="p-3 rounded-lg bg-emerald-50 dark:bg-emerald-950/30 border border-emerald-100 dark:border-emerald-900/40">
                <div className="font-bold text-emerald-900 dark:text-emerald-200 mb-1">
                  Positive Points (P = {nutriScore.positivePoints})
                </div>
                <ul className="space-y-0.5 text-[11px] font-mono">
                  <li>• Fiber: +{nutriScore.breakdown.fiberPoints} pts</li>
                  <li>• Protein: +{nutriScore.breakdown.proteinPoints} pts</li>
                  <li>• Fruits/Veg/Nuts: +{nutriScore.breakdown.fvlnPoints} pts</li>
                </ul>
              </div>
            </div>

            {nutriScore.negativePoints >= 11 && nutriScore.breakdown.fvlnPoints < 5 && (
              <div className="p-2.5 rounded-lg bg-amber-50 dark:bg-amber-950/40 border border-amber-200 dark:border-amber-900/40 flex items-start gap-2 text-[11px] text-amber-900 dark:text-amber-200">
                <AlertCircle className="w-4 h-4 shrink-0 mt-0.5" />
                <span>
                  <strong>2023 Protein Cap Rule Applied:</strong> Because negative points N ≥ 11 and FVLN ≤ 80%, protein points cannot offset high sugar/salt/fat content.
                </span>
              </div>
            )}
          </div>

          {/* SECTION 2: LATAM OCTAGONS */}
          <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-850 border border-slate-200 dark:border-slate-800 space-y-3">
            <h4 className="font-bold text-sm text-slate-900 dark:text-white flex items-center gap-1.5">
              <span>🇲🇽 🇨🇱</span> Mexican NOM-051 & Chilean Warning Octagons
            </h4>
            <p>
              Front-of-package warning stamps mandated in Mexico and Chile to alert consumers to excessive calories and energy ratios.
            </p>
            {warningOctagons.length > 0 ? (
              <div className="space-y-2 pt-1">
                {warningOctagons.map((w) => (
                  <div key={w.id} className="p-2.5 rounded-lg bg-slate-100 dark:bg-slate-800 flex justify-between items-center text-[11px]">
                    <div>
                      <span className="font-bold text-slate-900 dark:text-white">{w.mexicoLabel} / {w.chileLabel} ({w.englishSubtitle})</span>
                    </div>
                    <span className="font-mono text-slate-500 dark:text-slate-400">{w.thresholdDeclared}</span>
                  </div>
                ))}
              </div>
            ) : (
              <div className="p-3 rounded-lg bg-emerald-50 dark:bg-emerald-950/30 text-emerald-800 dark:text-emerald-300 font-semibold text-center">
                ✅ Zero warning octagons triggered under Latin American regulations.
              </div>
            )}
          </div>

          {/* SECTION 3: US FDA FOP */}
          <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-850 border border-slate-200 dark:border-slate-800 space-y-3">
            <h4 className="font-bold text-sm text-slate-900 dark:text-white flex items-center gap-1.5">
              <span>🇺🇸</span> US FDA Proposed Front-of-Package Scheme (%DV)
            </h4>
            <p>
              Based on the US FDA Proposed FOP Rule evaluating Saturated Fat (20g DV), Sodium (2300mg DV), and Added Sugars (50g DV) per serving.
            </p>
            <div className="grid grid-cols-3 gap-3 pt-1 text-center font-mono text-[11px]">
              <div className="p-2 rounded-lg bg-slate-100 dark:bg-slate-800">
                <div className="font-bold text-slate-700 dark:text-slate-300">Sat Fat</div>
                <div>{fdaLabel.saturatedFat.dvPercentage}% DV ({fdaLabel.saturatedFat.level})</div>
              </div>
              <div className="p-2 rounded-lg bg-slate-100 dark:bg-slate-800">
                <div className="font-bold text-slate-700 dark:text-slate-300">Sodium</div>
                <div>{fdaLabel.sodium.dvPercentage}% DV ({fdaLabel.sodium.level})</div>
              </div>
              <div className="p-2 rounded-lg bg-slate-100 dark:bg-slate-800">
                <div className="font-bold text-slate-700 dark:text-slate-300">Added Sugar</div>
                <div>{fdaLabel.addedSugar.dvPercentage}% DV ({fdaLabel.addedSugar.level})</div>
              </div>
            </div>
          </div>

        </div>

        {/* Modal Footer */}
        <div className="p-4 border-t border-slate-100 dark:border-slate-800 bg-slate-50 dark:bg-slate-850 flex justify-between items-center">
          <div className="text-[11px] text-slate-500 dark:text-slate-400 font-medium">
            FoodFactsIndia Multi-Jurisdictional Intelligence Engine
          </div>
          <button
            onClick={onClose}
            className="px-4 py-2 bg-slate-900 dark:bg-slate-100 text-white dark:text-slate-900 rounded-xl font-semibold text-xs hover:opacity-90 transition-opacity min-h-[44px] min-w-[44px]"
          >
            Close Methodology
          </button>
        </div>

      </div>
    </div>
  );
};
