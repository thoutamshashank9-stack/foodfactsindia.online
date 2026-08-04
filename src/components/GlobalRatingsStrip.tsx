import React from 'react';
import { InternationalRatings } from '../types';
import { Info } from 'lucide-react';

interface GlobalRatingsStripProps {
  ratings?: InternationalRatings;
  foodfactsScore: number;
  onOpenMethodology?: () => void;
}

const NUTRI_SCORE_COLORS: Record<string, { bg: string; text: string; activeBg: string }> = {
  A: { bg: 'bg-emerald-100 dark:bg-emerald-950/60', text: 'text-emerald-800 dark:text-emerald-300', activeBg: 'bg-[#008752] text-white shadow-emerald-500/30' },
  B: { bg: 'bg-lime-100 dark:bg-lime-950/60', text: 'text-lime-800 dark:text-lime-300', activeBg: 'bg-[#85BB2F] text-white shadow-lime-500/30' },
  C: { bg: 'bg-yellow-100 dark:bg-yellow-950/60', text: 'text-yellow-800 dark:text-yellow-300', activeBg: 'bg-[#FECB02] text-slate-900 shadow-yellow-500/30' },
  D: { bg: 'bg-amber-100 dark:bg-amber-950/60', text: 'text-amber-800 dark:text-amber-300', activeBg: 'bg-[#EE8100] text-white shadow-amber-500/30' },
  E: { bg: 'bg-rose-100 dark:bg-rose-950/60', text: 'text-rose-800 dark:text-rose-300', activeBg: 'bg-[#E63312] text-white shadow-rose-500/30' },
};

const FDA_LEVEL_STYLES = {
  LOW: 'bg-emerald-100 dark:bg-emerald-900/40 text-emerald-800 dark:text-emerald-300 border-emerald-300 dark:border-emerald-800',
  MED: 'bg-amber-100 dark:bg-amber-900/40 text-amber-800 dark:text-amber-300 border-amber-300 dark:border-amber-800',
  HIGH: 'bg-rose-100 dark:bg-rose-900/40 text-rose-800 dark:text-rose-300 border-rose-300 dark:border-rose-800',
};

export const GlobalRatingsStrip: React.FC<GlobalRatingsStripProps> = ({
  ratings,
  foodfactsScore,
  onOpenMethodology,
}) => {
  if (!ratings) return null;

  const { nutriScore, fdaLabel } = ratings;
  const grade = nutriScore.grade;

  return (
    <div className="w-full bg-white dark:bg-slate-900 rounded-2xl p-4 border border-slate-200/80 dark:border-slate-800 shadow-sm space-y-3">
      
      {/* Header Bar */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="text-sm">🌐</span>
          <h3 className="text-xs font-extrabold uppercase tracking-wider text-slate-800 dark:text-slate-200">
            Multi-Jurisdictional Front-of-Package Ratings
          </h3>
        </div>
        {onOpenMethodology && (
          <button
            onClick={onOpenMethodology}
            className="inline-flex items-center gap-1 text-[11px] font-semibold text-blue-600 dark:text-blue-400 hover:underline min-h-[44px] px-2 focus:outline-none focus:ring-2 focus:ring-blue-500 rounded-lg"
          >
            <Info className="w-3.5 h-3.5" />
            <span>Methodology</span>
          </button>
        )}
      </div>

      {/* Main Strip Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-1">
        
        {/* 🇪🇺 1. EU Nutri-Score (2023/2024 Rules) */}
        <div className="p-3.5 rounded-xl bg-slate-50 dark:bg-slate-850 border border-slate-200/70 dark:border-slate-800 flex flex-col justify-between">
          <div className="flex items-center justify-between pb-2 border-b border-slate-200/60 dark:border-slate-700/60">
            <span className="text-xs font-bold text-slate-700 dark:text-slate-300 flex items-center gap-1.5">
              <span>🇪🇺</span> EU Nutri-Score (2024)
            </span>
            <span className="text-[10px] font-mono font-medium text-slate-500 dark:text-slate-400">
              Score {nutriScore.score}
            </span>
          </div>

          {/* Nutri-Score A-E Bar */}
          <div className="flex items-center justify-between gap-1 pt-3">
            {['A', 'B', 'C', 'D', 'E'].map((letter) => {
              const isActive = letter === grade;
              const style = NUTRI_SCORE_COLORS[letter];
              return (
                <div
                  key={letter}
                  className={`flex-1 py-1.5 text-center text-xs font-black rounded-lg transition-all ${
                    isActive
                      ? `${style.activeBg} scale-110 shadow-md ring-2 ring-slate-900/10 dark:ring-white/20`
                      : `${style.bg} ${style.text} opacity-50`
                  }`}
                >
                  {letter}
                </div>
              );
            })}
          </div>
        </div>

        {/* 🇮🇳 2. FoodFactsIndia Score */}
        <div className="p-3.5 rounded-xl bg-gradient-to-br from-blue-50/50 to-emerald-50/50 dark:from-blue-950/20 dark:to-emerald-950/20 border border-blue-200/60 dark:border-blue-900/40 flex flex-col justify-between">
          <div className="flex items-center justify-between pb-2 border-b border-blue-200/50 dark:border-blue-900/40">
            <span className="text-xs font-bold text-slate-800 dark:text-slate-200 flex items-center gap-1.5">
              <span>🇮🇳</span> FoodFactsIndia Standard
            </span>
            <span className="text-[10px] font-bold uppercase tracking-wider text-blue-600 dark:text-blue-400">
              0-100 Gauge
            </span>
          </div>
          <div className="flex items-center justify-between pt-2">
            <div>
              <div className="text-2xl font-black text-slate-900 dark:text-white font-mono">
                {foodfactsScore}<span className="text-xs font-bold text-slate-400">/100</span>
              </div>
              <p className="text-[10px] font-medium text-slate-500 dark:text-slate-400">
                Deterministic Math v1.4
              </p>
            </div>
            <div className={`px-2.5 py-1 rounded-full text-xs font-extrabold ${
              foodfactsScore >= 75 ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300' :
              foodfactsScore >= 50 ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-950 dark:text-yellow-300' :
              'bg-rose-100 text-rose-800 dark:bg-rose-950 dark:text-rose-300'
            }`}>
              {foodfactsScore >= 75 ? 'Clean' : foodfactsScore >= 50 ? 'Moderate' : 'Ultra-Processed'}
            </div>
          </div>
        </div>

        {/* 🇺🇸 3. US FDA Proposed FOP Labels (%DV) */}
        <div className="p-3.5 rounded-xl bg-slate-50 dark:bg-slate-850 border border-slate-200/70 dark:border-slate-800 flex flex-col justify-between">
          <div className="flex items-center justify-between pb-2 border-b border-slate-200/60 dark:border-slate-700/60">
            <span className="text-xs font-bold text-slate-700 dark:text-slate-300 flex items-center gap-1.5">
              <span>🇺🇸</span> US FDA FOP (%DV)
            </span>
            <span className="text-[10px] font-medium text-slate-500 dark:text-slate-400">
              Per Serving
            </span>
          </div>
          <div className="grid grid-cols-3 gap-1.5 pt-2">
            {/* Sat Fat */}
            <div className={`p-1.5 rounded-lg border text-center ${FDA_LEVEL_STYLES[fdaLabel.saturatedFat.level]}`}>
              <div className="text-[9px] font-extrabold uppercase">Sat Fat</div>
              <div className="text-xs font-black">{fdaLabel.saturatedFat.dvPercentage}%</div>
              <div className="text-[8px] font-semibold">{fdaLabel.saturatedFat.level}</div>
            </div>
            {/* Sodium */}
            <div className={`p-1.5 rounded-lg border text-center ${FDA_LEVEL_STYLES[fdaLabel.sodium.level]}`}>
              <div className="text-[9px] font-extrabold uppercase">Sodium</div>
              <div className="text-xs font-black">{fdaLabel.sodium.dvPercentage}%</div>
              <div className="text-[8px] font-semibold">{fdaLabel.sodium.level}</div>
            </div>
            {/* Added Sugar */}
            <div className={`p-1.5 rounded-lg border text-center ${FDA_LEVEL_STYLES[fdaLabel.addedSugar.level]}`}>
              <div className="text-[9px] font-extrabold uppercase">Sugar</div>
              <div className="text-xs font-black">{fdaLabel.addedSugar.dvPercentage}%</div>
              <div className="text-[8px] font-semibold">{fdaLabel.addedSugar.level}</div>
            </div>
          </div>
        </div>

      </div>

    </div>
  );
};
