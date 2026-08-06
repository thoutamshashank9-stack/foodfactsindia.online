import React from 'react';

interface BadgeProps {
  label: string;
  variant: 'success' | 'warning' | 'danger' | 'info' | 'neutral';
  className?: string;
}

export const Badge: React.FC<BadgeProps> = ({ label, variant, className = '' }) => {
  const variantStyles = {
    success: 'bg-emerald-50 text-emerald-850 border-emerald-200 dark:bg-emerald-950/40 dark:text-emerald-300 dark:border-emerald-900/60',
    warning: 'bg-amber-50 text-amber-850 border-amber-200 dark:bg-amber-950/40 dark:text-amber-300 dark:border-amber-900/60',
    danger: 'bg-rose-50 text-rose-855 border-rose-200 dark:bg-rose-950/40 dark:text-rose-300 dark:border-rose-900/60',
    info: 'bg-sky-50 text-sky-850 border-sky-200 dark:bg-sky-950/40 dark:text-sky-300 dark:border-sky-900/60',
    neutral: 'bg-stone-50 text-stone-700 border-stone-200 dark:bg-stone-800 dark:text-stone-300 dark:border-stone-700',
  };

  return (
    <span className={`inline-flex items-center px-2 py-0.5 rounded text-[11px] font-semibold border ${variantStyles[variant]} ${className}`}>
      {label}
    </span>
  );
};
