import React from 'react';
import { ShieldAlert, AlertTriangle, CheckCircle2 } from 'lucide-react';

interface ScoreGaugeProps {
  score: number; // Used to derive issue severity level
  grade: string;
  size?: 'sm' | 'md' | 'lg';
  issuesCount?: number;
}

export const ScoreGauge: React.FC<ScoreGaugeProps> = ({ score, grade, size = 'md', issuesCount }) => {
  // Derive risk level from score without showing the numeric score number
  let severity: 'HIGH' | 'MODERATE' | 'CLEAN' = 'CLEAN';
  let badgeColor = 'bg-emerald-100 text-emerald-800 border-emerald-300 dark:bg-emerald-950 dark:text-emerald-300 dark:border-emerald-800';
  let Icon = CheckCircle2;
  let label = 'Clean Product';

  if (score < 50) {
    severity = 'HIGH';
    badgeColor = 'bg-rose-100 text-rose-800 border-rose-300 dark:bg-rose-950 dark:text-rose-300 dark:border-rose-800';
    Icon = ShieldAlert;
    label = 'High Risk Issues';
  } else if (score < 75) {
    severity = 'MODERATE';
    badgeColor = 'bg-amber-100 text-amber-800 border-amber-300 dark:bg-amber-950 dark:text-amber-300 dark:border-amber-800';
    Icon = AlertTriangle;
    label = 'Moderate Concerns';
  }

  const countText = issuesCount !== undefined ? `${issuesCount} Issues Identified` : label;

  if (size === 'lg') {
    return (
      <div className={`p-5 rounded-2xl border ${badgeColor} flex flex-col items-center justify-center text-center space-y-2`}>
        <Icon className="w-10 h-10 animate-bounce" />
        <span className="font-extrabold text-base tracking-tight">
          {countText}
        </span>
        <span className="text-[11px] font-semibold opacity-80 uppercase tracking-wider">
          {severity === 'HIGH' ? 'Requires Consumer Vigilance' : severity === 'MODERATE' ? 'Nutritional Caution Recommended' : 'Verified Evidence-Based'}
        </span>
      </div>
    );
  }

  return (
    <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-xl border text-xs font-bold ${badgeColor}`}>
      <Icon className="w-3.5 h-3.5" />
      <span>{countText}</span>
    </span>
  );
};
