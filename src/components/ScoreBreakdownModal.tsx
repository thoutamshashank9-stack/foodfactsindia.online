import React from 'react';
import { X, ShieldAlert, CheckCircle2, Info, Calculator, FileText } from 'lucide-react';
import { ScoreBreakdownItem } from '../types';

interface ScoreBreakdownModalProps {
  isOpen: boolean;
  onClose: () => void;
  productName: string;
  score: number;
  breakdown: ScoreBreakdownItem[];
}

export const ScoreBreakdownModal: React.FC<ScoreBreakdownModalProps> = ({
  isOpen,
  onClose,
  productName,
  score,
  breakdown,
}) => {
  if (!isOpen) return null;

  const deductions = breakdown.filter((b) => b.type === 'DEDUCTION');
  const additions = breakdown.filter((b) => b.type === 'ADDITION');

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-fade-in">
      <div className="relative w-full max-w-2xl bg-white dark:bg-slate-900 rounded-2xl shadow-2xl border border-slate-200 dark:border-slate-800 overflow-hidden flex flex-col max-h-[90vh]">
        
        {/* Modal Header */}
        <div className="p-5 border-b border-slate-100 dark:border-slate-800 flex items-center justify-between bg-slate-50/50 dark:bg-slate-850/50">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-xl bg-blue-100 dark:bg-blue-900/50 text-blue-600 dark:text-blue-400">
              <Calculator className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-lg font-bold text-slate-900 dark:text-white">
                Deterministic Score Methodology
              </h3>
              <p className="text-xs text-slate-500 dark:text-slate-400">
                {productName} • Base Score 100 → Final Score {score}/100
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Modal Scroll Content */}
        <div className="p-6 overflow-y-auto space-y-6 flex-1 text-sm">
          
          {/* Methodology Info Box */}
          <div className="p-4 rounded-xl bg-blue-50 dark:bg-blue-950/40 border border-blue-200 dark:border-blue-800/50 text-blue-900 dark:text-blue-200 flex gap-3">
            <Info className="w-5 h-5 text-blue-600 dark:text-blue-400 shrink-0 mt-0.5" />
            <div className="text-xs leading-relaxed">
              <span className="font-semibold">Evidence First & Neutrality Guarantee:</span> The FoodFactsIndia score is computed via reproducible mathematical code based on official WHO, FSSAI, EFSA, and US FDA dietary thresholds. LLMs are never asked to guess ratings.
            </div>
          </div>

          {/* Base Score Starting Point */}
          <div className="flex items-center justify-between p-3.5 rounded-xl bg-slate-50 dark:bg-slate-800/60 font-semibold border border-slate-200 dark:border-slate-700">
            <span className="text-slate-700 dark:text-slate-300">Standard Product Starting Point</span>
            <span className="text-blue-600 dark:text-blue-400 font-mono text-base">+100 pts</span>
          </div>

          {/* Deductions Section */}
          {deductions.length > 0 && (
            <div className="space-y-3">
              <h4 className="font-bold text-xs uppercase tracking-wider text-rose-600 dark:text-rose-400 flex items-center gap-1.5">
                <ShieldAlert className="w-4 h-4" />
                Deductions Applied ({deductions.reduce((acc, d) => acc + d.points, 0)} pts)
              </h4>
              <div className="space-y-2.5">
                {deductions.map((item, i) => (
                  <div
                    key={i}
                    className="p-3.5 rounded-xl bg-rose-50/50 dark:bg-rose-950/20 border border-rose-100 dark:border-rose-900/40 flex justify-between items-start gap-4"
                  >
                    <div>
                      <div className="font-semibold text-rose-950 dark:text-rose-200">
                        {item.factor}
                      </div>
                      <p className="text-xs text-rose-800/80 dark:text-rose-300/80 mt-1">
                        {item.rationale}
                      </p>
                      <div className="flex items-center gap-1.5 text-[11px] text-slate-500 dark:text-slate-400 mt-2 font-medium">
                        <FileText className="w-3 h-3" />
                        Authority Source: {item.authoritySource}
                      </div>
                    </div>
                    <span className="font-mono font-bold text-rose-600 dark:text-rose-400 text-sm whitespace-nowrap bg-rose-100 dark:bg-rose-900/60 px-2 py-1 rounded">
                      {item.points} pts
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Additions Section */}
          {additions.length > 0 && (
            <div className="space-y-3">
              <h4 className="font-bold text-xs uppercase tracking-wider text-emerald-600 dark:text-emerald-400 flex items-center gap-1.5">
                <CheckCircle2 className="w-4 h-4" />
                Positive Nutrients & Adjustments (+{additions.reduce((acc, a) => acc + a.points, 0)} pts)
              </h4>
              <div className="space-y-2.5">
                {additions.map((item, i) => (
                  <div
                    key={i}
                    className="p-3.5 rounded-xl bg-emerald-50/50 dark:bg-emerald-950/20 border border-emerald-100 dark:border-emerald-900/40 flex justify-between items-start gap-4"
                  >
                    <div>
                      <div className="font-semibold text-emerald-950 dark:text-emerald-200">
                        {item.factor}
                      </div>
                      <p className="text-xs text-emerald-800/80 dark:text-emerald-300/80 mt-1">
                        {item.rationale}
                      </p>
                      <div className="flex items-center gap-1.5 text-[11px] text-slate-500 dark:text-slate-400 mt-2 font-medium">
                        <FileText className="w-3 h-3" />
                        Authority Source: {item.authoritySource}
                      </div>
                    </div>
                    <span className="font-mono font-bold text-emerald-600 dark:text-emerald-400 text-sm whitespace-nowrap bg-emerald-100 dark:bg-emerald-900/60 px-2 py-1 rounded">
                      +{item.points} pts
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}

        </div>

        {/* Modal Footer */}
        <div className="p-4 border-t border-slate-100 dark:border-slate-800 bg-slate-50 dark:bg-slate-850 flex justify-between items-center">
          <div className="text-xs text-slate-500 dark:text-slate-400 font-medium">
            Calculated by FoodLens Deterministic Math v1.4
          </div>
          <button
            onClick={onClose}
            className="px-4 py-2 bg-slate-900 dark:bg-slate-100 text-white dark:text-slate-900 rounded-xl font-semibold text-xs hover:bg-slate-800 dark:hover:bg-white transition-colors"
          >
            Close Breakdown
          </button>
        </div>

      </div>
    </div>
  );
};
