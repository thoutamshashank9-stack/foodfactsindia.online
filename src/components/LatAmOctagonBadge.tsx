import React from 'react';
import { LatAmOctagonWarning } from '../types';
import { AlertTriangle } from 'lucide-react';

interface LatAmOctagonBadgeProps {
  warnings: LatAmOctagonWarning[];
  showTitle?: boolean;
}

export const LatAmOctagonBadge: React.FC<LatAmOctagonBadgeProps> = ({
  warnings,
  showTitle = true,
}) => {
  if (!warnings || warnings.length === 0) return null;

  return (
    <div className="space-y-2.5">
      {showTitle && (
        <div className="flex items-center gap-2">
          <span className="text-sm">🇲🇽 🇨🇱</span>
          <h4 className="text-xs font-bold text-slate-900 dark:text-white uppercase tracking-wider flex items-center gap-1.5">
            <AlertTriangle className="w-3.5 h-3.5 text-amber-500" />
            Mandatory Front-of-Package Warning Octagons (NOM-051 / Chile)
          </h4>
        </div>
      )}

      {/* Octagons Flex Grid */}
      <div className="flex flex-wrap gap-2.5 items-stretch">
        {warnings.map((w) => {
          const isStopTag = w.id.startsWith('HIGH');
          return (
            <div
              key={w.id}
              className={`relative flex flex-col justify-center items-center px-3.5 py-2.5 rounded-xl border-2 shadow-md transition-transform hover:scale-105 ${
                isStopTag
                  ? 'bg-slate-950 text-white border-white dark:border-slate-800'
                  : 'bg-amber-400 text-slate-950 border-slate-900 font-extrabold'
              }`}
              style={{
                clipPath: isStopTag ? 'polygon(30% 0%, 70% 0%, 100% 30%, 100% 70%, 70% 100%, 30% 100%, 0% 70%, 0% 30%)' : undefined
              }}
            >
              <div className="text-[11px] font-black text-center uppercase tracking-tight leading-none px-1">
                {w.label}
              </div>
              <div className="text-[9px] font-semibold text-slate-300 dark:text-slate-400 mt-1 text-center leading-tight">
                {w.subtitle}
              </div>
              <div className="text-[8px] font-mono text-slate-400 dark:text-slate-500 mt-0.5">
                {w.thresholdDeclared}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
