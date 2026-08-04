import React, { useState } from 'react';
import { LatAmOctagonWarning } from '../types';
import { Info, CheckCircle2, ShieldAlert } from 'lucide-react';

interface LatAmOctagonBadgeProps {
  warnings: LatAmOctagonWarning[];
  onOpenMethodology?: () => void;
}

export const LatAmOctagonBadge: React.FC<LatAmOctagonBadgeProps> = ({
  warnings,
  onOpenMethodology,
}) => {
  if (!warnings) return null;

  const [selectedCountry, setSelectedCountry] = useState<'MX' | 'CL'>('MX');

  const countryInfo = selectedCountry === 'MX'
    ? { name: 'Mexico', flag: '🇲🇽', citation: 'Official Regulation: NOM-051-SCFI/SSA1-2010 (Mexico)' }
    : { name: 'Chile', flag: '🇨🇱', citation: 'Official Regulation: Ley N° 20.606 de Etiquetado de Alimentos (Chile)' };

  return (
    <div className="w-full rounded-3xl border-2 border-rose-500/80 dark:border-rose-700/80 bg-rose-50/70 dark:bg-[#2A1215]/80 p-6 sm:p-7 shadow-lg space-y-5 transition-colors">
      
      {/* Header Row */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-rose-200/80 dark:border-rose-900/60">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            {/* Solid Dark Octagon Badge Icon */}
            <div className="w-6 h-6 rounded bg-slate-950 dark:bg-black text-white flex items-center justify-center font-mono text-xs font-black shrink-0 border border-white/40">
              🛑
            </div>
            <h3 className="text-sm sm:text-base font-black text-slate-900 dark:text-white uppercase tracking-wider">
              MANDATORY HEALTH WARNING LABELS
            </h3>
          </div>
          <p className="text-xs text-rose-950/80 dark:text-rose-200/80 font-medium leading-relaxed max-w-2xl pt-1">
            India (FSSAI) has no mandatory front-of-package warning label system yet. These are the exact labels this product would carry under Mexican and Chilean law, shown for educational comparison.
          </p>
        </div>

        {onOpenMethodology && (
          <button
            onClick={onOpenMethodology}
            className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-white/80 dark:bg-slate-900/80 border border-rose-200 dark:border-rose-800 text-xs font-bold text-rose-900 dark:text-rose-200 hover:bg-white transition-colors shrink-0 self-start sm:self-center min-h-[44px]"
          >
            <Info className="w-4 h-4 text-rose-600 dark:text-rose-400" />
            <span>Why is this shown?</span>
          </button>
        )}
      </div>

      {/* Country Segmented Control Toggle */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div className="inline-flex p-1 bg-white/90 dark:bg-slate-900/90 rounded-2xl border border-rose-200/80 dark:border-rose-900/60 shadow-sm shrink-0">
          <button
            onClick={() => setSelectedCountry('MX')}
            className={`px-4 py-2 rounded-xl text-xs font-extrabold transition-all flex items-center gap-2 min-h-[44px] ${
              selectedCountry === 'MX'
                ? 'bg-rose-600 text-white shadow-md'
                : 'text-slate-700 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white'
            }`}
          >
            <span>🇲🇽</span>
            <span>Mexico — NOM-051</span>
          </button>
          <button
            onClick={() => setSelectedCountry('CL')}
            className={`px-4 py-2 rounded-xl text-xs font-extrabold transition-all flex items-center gap-2 min-h-[44px] ${
              selectedCountry === 'CL'
                ? 'bg-rose-600 text-white shadow-md'
                : 'text-slate-700 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white'
            }`}
          >
            <span>🇨🇱</span>
            <span>Chile — Ley 20.606</span>
          </button>
        </div>

        <span className="text-[11px] font-semibold text-rose-800/80 dark:text-rose-300/80">
          {countryInfo.citation}
        </span>
      </div>

      {/* Octagons Container or Positive Empty State */}
      {warnings && warnings.length > 0 ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 pt-2">
          {warnings.map((w) => {
            const nativeText = selectedCountry === 'MX' ? w.mexicoLabel : w.chileLabel;
            const isStopOctagon = !w.id.includes('SWEETENERS') && !w.id.includes('CAFFEINE');

            return (
              <div key={w.id} className="flex flex-col items-center text-center space-y-2">
                
                {/* 140px Desktop / 110px Mobile Regular Octagon */}
                <div
                  className={`relative w-[120px] h-[120px] sm:w-[140px] sm:h-[140px] flex flex-col items-center justify-center p-3 text-center transition-transform hover:scale-105 shadow-2xl ${
                    isStopOctagon
                      ? 'bg-black text-white border-2 border-white'
                      : 'bg-amber-400 text-slate-950 border-2 border-slate-900 font-extrabold'
                  }`}
                  style={{
                    clipPath: isStopOctagon
                      ? 'polygon(30% 0%, 70% 0%, 100% 30%, 100% 70%, 70% 100%, 30% 100%, 0% 70%, 0% 30%)'
                      : undefined,
                    borderRadius: isStopOctagon ? undefined : '12px'
                  }}
                >
                  {/* Line 1: Native Warning Label (Max 2 lines inside shape) */}
                  <div className="text-xs sm:text-sm font-black uppercase tracking-tight leading-tight">
                    {nativeText}
                  </div>
                  
                  {/* Line 2: English Translation */}
                  <div className="text-[10px] sm:text-[11px] font-medium opacity-80 mt-1 leading-snug">
                    {w.englishSubtitle}
                  </div>
                </div>

                {/* External Threshold Caption Below Octagon */}
                <div className="text-[10px] font-mono font-medium text-rose-950/80 dark:text-rose-200/80 bg-white/70 dark:bg-slate-900/70 px-2 py-1 rounded-md border border-rose-200/60 dark:border-rose-900/40">
                  Threshold: {w.thresholdDeclared}
                </div>

              </div>
            );
          })}
        </div>
      ) : (
        /* Positive Empty State */
        <div className="p-4 rounded-2xl bg-emerald-100/80 dark:bg-emerald-950/60 border border-emerald-300 dark:border-emerald-800 text-emerald-900 dark:text-emerald-200 font-bold text-xs flex items-center justify-center gap-2">
          <CheckCircle2 className="w-4 h-4 text-emerald-600 dark:text-emerald-400 shrink-0" />
          <span>No mandatory health warning labels apply under {countryInfo.name} regulations for this product.</span>
        </div>
      )}

    </div>
  );
};
