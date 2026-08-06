import React, { useState } from 'react';
import { LatAmOctagonWarning } from '../../types';
import { Info, CheckCircle2, AlertTriangle } from 'lucide-react';
import { Card } from '../Card';

interface WarningLabelsProps {
  warnings: LatAmOctagonWarning[];
  onOpenMethodology?: () => void;
}

export const WarningLabels: React.FC<WarningLabelsProps> = ({
  warnings,
  onOpenMethodology,
}) => {
  if (!warnings) return null;

  const [selectedCountry, setSelectedCountry] = useState<'MX' | 'CL'>('MX');

  const countryInfo = selectedCountry === 'MX'
    ? { name: 'Mexico', flag: '🇲🇽', citation: 'NOM-051-SCFI/SSA1-2010 (Mexico)' }
    : { name: 'Chile', flag: '🇨🇱', citation: 'Ley N° 20.606 (Chile)' };

  return (
    <Card className="space-y-4">
      {/* Header Row */}
      <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-3 pb-3 border-b border-stone-200 dark:border-stone-850">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 text-rose-600 shrink-0" />
            <h3 className="text-xs font-bold text-stone-900 dark:text-white uppercase tracking-wider">
              Health Warning Labels
            </h3>
          </div>
          <p className="text-[11px] text-stone-500 leading-normal max-w-xl">
            Simulated warnings this product would carry under Mexican or Chilean food policy, shown for reference.
          </p>
        </div>

        {onOpenMethodology && (
          <button
            onClick={onOpenMethodology}
            className="inline-flex items-center gap-1 px-2.5 py-1 rounded bg-stone-50 dark:bg-stone-850 border border-stone-250 dark:border-stone-800 text-[10px] font-semibold text-stone-700 dark:text-stone-300 hover:bg-stone-100 transition-colors shrink-0"
          >
            <Info className="w-3.5 h-3.5" />
            <span>Why is this shown?</span>
          </button>
        )}
      </div>

      {/* Country Toggle */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-stone-50 dark:bg-stone-850 p-1.5 rounded-lg border border-stone-200/50 dark:border-stone-800">
        <div className="inline-flex p-0.5 bg-white dark:bg-stone-900 rounded-md border border-stone-200 dark:border-stone-800 shadow-sm shrink-0">
          <button
            onClick={() => setSelectedCountry('MX')}
            className={`px-3 py-1 rounded text-xs font-semibold transition-all flex items-center gap-1.5 ${
              selectedCountry === 'MX'
                ? 'bg-rose-600 text-white shadow-sm'
                : 'text-stone-600 dark:text-stone-400 hover:text-stone-900'
            }`}
          >
            <span>🇲🇽</span>
            <span>Mexico</span>
          </button>
          <button
            onClick={() => setSelectedCountry('CL')}
            className={`px-3 py-1 rounded text-xs font-semibold transition-all flex items-center gap-1.5 ${
              selectedCountry === 'CL'
                ? 'bg-rose-600 text-white shadow-sm'
                : 'text-stone-600 dark:text-stone-400 hover:text-stone-900'
            }`}
          >
            <span>🇨🇱</span>
            <span>Chile</span>
          </button>
        </div>

        <span className="text-[10px] font-mono text-stone-550 dark:text-stone-400">
          {countryInfo.citation}
        </span>
      </div>

      {/* Warnings List */}
      {warnings.length > 0 ? (
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 pt-1">
          {warnings.map((w) => {
            const isStopOctagon = !w.id.includes('SWEETENERS') && !w.id.includes('CAFFEINE');

            return (
              <div key={w.id} className="flex flex-col items-center text-center space-y-2">
                <div
                  className={`relative w-[90px] h-[90px] flex flex-col items-center justify-center p-2 text-center transition-transform hover:scale-105 shadow-sm ${
                    isStopOctagon
                      ? 'bg-black text-white border border-white'
                      : 'bg-amber-400 text-stone-950 border border-stone-900 font-bold'
                  }`}
                  style={{
                    clipPath: isStopOctagon
                      ? 'polygon(30% 0%, 70% 0%, 100% 30%, 100% 70%, 70% 100%, 30% 100%, 0% 70%, 0% 30%)'
                      : undefined,
                    borderRadius: isStopOctagon ? undefined : '8px'
                  }}
                >
                  <div className="text-[8px] sm:text-[9px] font-black uppercase tracking-tight leading-tight px-0.5">
                    {w.englishSubtitle}
                  </div>
                </div>

                <div className="text-[9px] font-mono text-stone-500 bg-stone-50 dark:bg-stone-850 px-2 py-0.5 rounded border border-stone-200/60 dark:border-stone-800">
                  {w.thresholdDeclared}
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        <div className="p-3 rounded-lg bg-emerald-50 dark:bg-emerald-950/20 border border-emerald-200 dark:border-emerald-900/60 text-emerald-800 dark:text-emerald-300 text-xs flex items-center justify-center gap-1.5 font-medium">
          <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
          <span>No health warning labels required under {countryInfo.name} policy.</span>
        </div>
      )}
    </Card>
  );
};
