import React from 'react';

export type ProductStatus = 
  | 'unverified' 
  | 'submitted' 
  | 'under_review' 
  | 'needs_more_photos' 
  | 'verified' 
  | 'rejected' 
  | 'duplicate' 
  | 'obsolete';

interface StatusBadgeProps {
  status: ProductStatus;
  completenessScore?: number;
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({ status, completenessScore = 0 }) => {
  switch (status) {
    case 'verified':
      return (
        <span className="inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-extrabold uppercase tracking-wider bg-emerald-100 text-emerald-800 dark:bg-emerald-950/80 dark:text-emerald-300 border border-emerald-300 dark:border-emerald-800">
          Verified
        </span>
      );

    case 'submitted':
      return (
        <span className="inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-extrabold uppercase tracking-wider bg-blue-100 text-blue-800 dark:bg-blue-950/80 dark:text-blue-300 border border-blue-300 dark:border-blue-800">
          Awaiting Review
        </span>
      );

    case 'under_review':
      return (
        <span className="inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-extrabold uppercase tracking-wider bg-purple-100 text-purple-800 dark:bg-purple-950/80 dark:text-purple-300 border border-purple-300 dark:border-purple-800">
          In Verification
        </span>
      );

    case 'needs_more_photos':
      return (
        <span className="inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-extrabold uppercase tracking-wider bg-amber-100 text-amber-800 dark:bg-amber-950/80 dark:text-amber-300 border border-amber-300 dark:border-amber-800">
          Needs More Photos
        </span>
      );

    case 'unverified':
    default:
      return (
        <span className="inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-extrabold uppercase tracking-wider bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300 border border-slate-300 dark:border-slate-700">
          Incomplete Label ({completenessScore}%)
        </span>
      );
  }
};
