import React from 'react';
import { TransparencyReport } from '../../types';
import { ProductImage } from '../ProductImage';
import { Card } from '../Card';

interface ProductHeaderProps {
  report: TransparencyReport;
  issuesCount: number;
}

export const ProductHeader: React.FC<ProductHeaderProps> = ({ report, issuesCount }) => {
  // Determine color based on grade
  const grade = report.executiveSummary.grade;
  const gradeColors: Record<string, string> = {
    'A+': 'bg-green-600 text-white',
    'A': 'bg-green-500 text-white',
    'B': 'bg-green-400 text-white',
    'C': 'bg-yellow-400 text-stone-900',
    'D': 'bg-orange-500 text-white',
    'E': 'bg-red-500 text-white',
    'F': 'bg-stone-500 text-white'
  };
  const gradeColor = gradeColors[grade] || gradeColors['F'];

  return (
    <Card className="space-y-4">
      <div className="flex flex-col sm:flex-row gap-5 items-start">
        <ProductImage
          barcode={report.barcode}
          productName={report.productName}
          className="w-24 h-24 sm:w-28 sm:h-28 rounded-lg object-cover border border-stone-250 dark:border-stone-800 shrink-0 mx-auto sm:mx-0"
        />

        <div className="flex-1 space-y-1.5 text-center sm:text-left">
          {!!(report.brand || report.category) && (
            <div className="text-[10px] font-bold uppercase tracking-wider text-teal-800 dark:text-teal-400">
              {[report.brand, report.category].filter(Boolean).join(' • ')}
            </div>
          )}
          <h1 className="font-serif text-xl sm:text-2xl font-bold text-stone-900 dark:text-stone-100 leading-tight">
            {report.productName || 'Unknown Product'}
          </h1>
          <div className="text-xs text-stone-500 dark:text-stone-400 font-mono">
            {[
              report.packageSize ? `Pack Size: ${report.packageSize}` : null,
              report.barcode ? `GTIN: ${report.barcode}` : null
            ].filter(Boolean).join(' • ')}
          </div>
        </div>

        {/* Right side: Overall grade badge and concerns count */}
        <div className="flex flex-col items-center shrink-0 w-full sm:w-auto mt-4 sm:mt-0 gap-2">
          <div className={`w-16 h-16 rounded-2xl flex flex-col items-center justify-center ${gradeColor} shadow-sm`}>
            <span className="text-2xl font-black">{grade}</span>
            <span className="text-[10px] font-bold opacity-90">{report.deterministicScore}/100</span>
          </div>
          {issuesCount > 0 && (
            <div className="px-2 py-1 rounded-full bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400 text-[10px] font-bold tracking-wide">
              {issuesCount} Concern{issuesCount !== 1 ? 's' : ''}
            </div>
          )}
        </div>
      </div>
    </Card>
  );
};
