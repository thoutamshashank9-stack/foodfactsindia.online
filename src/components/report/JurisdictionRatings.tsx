import React from 'react';
import { InternationalRatings } from '../../types';
import { Info } from 'lucide-react';
import { Card } from '../Card';

interface JurisdictionRatingsProps {
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
  LOW: 'bg-emerald-50 dark:bg-emerald-950/30 text-emerald-800 dark:text-emerald-305 border-emerald-250 dark:border-emerald-900/60',
  MED: 'bg-amber-50 dark:bg-amber-950/30 text-amber-800 dark:text-amber-305 border-amber-250 dark:border-amber-900/60',
  HIGH: 'bg-rose-50 dark:bg-rose-950/30 text-rose-800 dark:text-rose-305 border-rose-250 dark:border-rose-900/60',
};

export const JurisdictionRatings: React.FC<JurisdictionRatingsProps> = ({
  ratings,
  foodfactsScore,
  onOpenMethodology,
}) => {
  if (!ratings || !ratings.nutriScore || !ratings.fdaLabel) return null;

  const { nutriScore, fdaLabel } = ratings;
  const grade = nutriScore.grade;

  return (
    <Card className="space-y-4">
      <div className="flex items-center justify-between border-b border-stone-200 dark:border-stone-850 pb-2">
        <div className="flex items-center gap-1.5">
          <span className="text-sm">🌐</span>
          <h3 className="text-xs font-bold uppercase tracking-wider text-stone-800 dark:text-stone-200">
            Multi-Jurisdictional Front-of-Package Ratings
          </h3>
        </div>
        {onOpenMethodology && (
          <button
            onClick={onOpenMethodology}
            className="inline-flex items-center gap-1 text-[11px] font-semibold text-teal-800 dark:text-teal-400 hover:underline focus:outline-none"
          >
            <Info className="w-3.5 h-3.5" />
            <span>Methodology</span>
          </button>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* EU Nutri-Score */}
        <div className="p-3.5 rounded-lg bg-stone-50 dark:bg-stone-850 border border-stone-200 dark:border-stone-800 flex flex-col justify-between min-h-[110px]">
          <div className="flex items-center justify-between pb-1.5 border-b border-stone-200/60 dark:border-stone-700/60">
            <span className="text-[11px] font-bold text-stone-700 dark:text-stone-300">
              🇪🇺 EU Nutri-Score (2024)
            </span>
            <span className="text-[10px] font-mono text-stone-500">
              Score {nutriScore.score}
            </span>
          </div>

          <div className="flex items-center justify-between gap-1 pt-2">
            {['A', 'B', 'C', 'D', 'E'].map((letter) => {
              const isActive = letter === grade;
              const style = NUTRI_SCORE_COLORS[letter];
              return (
                <div
                  key={letter}
                  className={`flex-1 py-1 text-center text-xs font-bold rounded transition-all ${
                    isActive
                      ? `${style.activeBg} scale-105 shadow-sm`
                      : `${style.bg} ${style.text} opacity-50`
                  }`}
                >
                  {letter}
                </div>
              );
            })}
          </div>
        </div>

        {/* FoodFactsIndia Standard */}
        <div className="p-3.5 rounded-lg bg-stone-50 dark:bg-stone-850 border border-stone-200 dark:border-stone-800 flex flex-col justify-between min-h-[110px]">
          <div className="flex items-center justify-between pb-1.5 border-b border-stone-200/60 dark:border-stone-700/60">
            <span className="text-[11px] font-bold text-stone-700 dark:text-stone-300">
              🇮🇳 India Benchmark
            </span>
            <span className="text-[9px] uppercase tracking-wider font-bold text-teal-800 dark:text-teal-400">
              0-100 Scale
            </span>
          </div>
          <div className="flex items-center justify-between pt-1.5">
            <div>
              <div className="text-xl font-bold text-stone-900 dark:text-white font-mono">
                {foodfactsScore}<span className="text-[10px] text-stone-400">/100</span>
              </div>
              <p className="text-[9px] text-stone-500">
                Formula v1.4
              </p>
            </div>
            <div className={`px-2 py-0.5 rounded text-[10px] font-bold ${
              foodfactsScore >= 75 ? 'bg-emerald-50 text-emerald-800 dark:bg-emerald-950/40 dark:text-emerald-300' :
              foodfactsScore >= 50 ? 'bg-amber-50 text-amber-800 dark:bg-amber-950/40 dark:text-amber-300' :
              'bg-rose-50 text-rose-800 dark:bg-rose-950/40 dark:text-rose-300'
            }`}>
              {foodfactsScore >= 75 ? 'Clean' : foodfactsScore >= 50 ? 'Moderate' : 'UPF'}
            </div>
          </div>
        </div>

        {/* US FDA proposed FOP */}
        <div className="p-3.5 rounded-lg bg-stone-50 dark:bg-stone-850 border border-stone-200 dark:border-stone-800 flex flex-col justify-between min-h-[110px]">
          <div className="flex items-center justify-between pb-1.5 border-b border-stone-200/60 dark:border-stone-700/60">
            <span className="text-[11px] font-bold text-stone-700 dark:text-stone-300">
              🇺🇸 US FDA proposed FOP
            </span>
            <span className="text-[9px] text-stone-500 font-mono">
              % DV
            </span>
          </div>
          <div className="grid grid-cols-3 gap-1 pt-1.5">
            <div className={`p-1 rounded border text-center ${FDA_LEVEL_STYLES[fdaLabel.saturatedFat.level]}`}>
              <div className="text-[8px] font-bold uppercase truncate">Fat</div>
              <div className="text-xs font-bold leading-none py-0.5">{fdaLabel.saturatedFat.dvPercentage}%</div>
            </div>
            <div className={`p-1 rounded border text-center ${FDA_LEVEL_STYLES[fdaLabel.sodium.level]}`}>
              <div className="text-[8px] font-bold uppercase truncate">Salt</div>
              <div className="text-xs font-bold leading-none py-0.5">{fdaLabel.sodium.dvPercentage}%</div>
            </div>
            <div className={`p-1 rounded border text-center ${FDA_LEVEL_STYLES[fdaLabel.addedSugar.level]}`}>
              <div className="text-[8px] font-bold uppercase truncate">Sugar</div>
              <div className="text-xs font-bold leading-none py-0.5">{fdaLabel.addedSugar.dvPercentage}%</div>
            </div>
          </div>
        </div>
      </div>
    </Card>
  );
};
