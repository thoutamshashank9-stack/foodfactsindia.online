import React from 'react';
import { TransparencyReport } from '../../types';
import { Card } from '../Card';
import { Calculator } from 'lucide-react';

interface ScoreHeroProps {
  report: TransparencyReport;
  issuesCount: number;
  onOpenRules: () => void;
}

export const ScoreHero: React.FC<ScoreHeroProps> = ({ report, issuesCount, onOpenRules }) => {
  const grade = report.executiveSummary.grade;
  const score = report.deterministicScore;

  // Grade styles
  const gradeColors: Record<string, { bg: string; text: string; border: string }> = {
    A: { bg: 'bg-emerald-50 dark:bg-emerald-950/30', text: 'text-emerald-800 dark:text-emerald-400', border: 'border-emerald-200 dark:border-emerald-900/60' },
    B: { bg: 'bg-lime-50 dark:bg-lime-950/30', text: 'text-lime-800 dark:text-lime-400', border: 'border-lime-200 dark:border-lime-900/60' },
    C: { bg: 'bg-yellow-50 dark:bg-yellow-950/30', text: 'text-yellow-800 dark:text-yellow-405', border: 'border-yellow-200 dark:border-yellow-900/60' },
    D: { bg: 'bg-amber-50 dark:bg-amber-950/30', text: 'text-amber-800 dark:text-amber-405', border: 'border-amber-200 dark:border-amber-900/60' },
    F: { bg: 'bg-rose-50 dark:bg-rose-950/30', text: 'text-rose-800 dark:text-rose-400', border: 'border-rose-200 dark:border-rose-900/60' },
  };

  const style = gradeColors[grade] || gradeColors['C'];

  return (
    <Card className="flex flex-col sm:flex-row items-center gap-6 p-6">
      {/* Dominant Grade/Score circle */}
      <div className={`w-20 h-20 rounded-full flex flex-col items-center justify-center border-2 shrink-0 shadow-sm ${style.bg} ${style.text} ${style.border}`}>
        <span className="font-serif text-3xl font-extrabold leading-none">{grade}</span>
        <span className="text-[10px] font-mono font-bold mt-0.5">{score}/100</span>
      </div>

      <div className="text-center sm:text-left space-y-2 flex-1">
        <div className="flex items-center justify-center sm:justify-start gap-2 flex-wrap">
          <h3 className="font-serif text-lg font-bold text-stone-900 dark:text-stone-100">
            Score: {score}/100
          </h3>
          <span className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold uppercase tracking-wider ${
            score >= 75 ? 'bg-emerald-50 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300' :
            score >= 50 ? 'bg-amber-50 text-amber-800 dark:bg-amber-950 dark:text-amber-300' :
            'bg-rose-50 text-rose-800 dark:bg-rose-950 dark:text-rose-300'
          }`}>
            {issuesCount} Concerns
          </span>
        </div>

        <p className="text-xs text-stone-500 dark:text-stone-400 leading-normal">
          {report.executiveSummary.verdictTitle || 'Product composition rating.'}
        </p>

        <button
          onClick={onOpenRules}
          className="text-xs text-teal-850 dark:text-teal-405 hover:underline inline-flex items-center gap-1 font-medium"
        >
          <Calculator className="w-3.5 h-3.5" />
          <span>View scoring methodology</span>
        </button>
      </div>
    </Card>
  );
};
