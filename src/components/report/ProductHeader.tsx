import React from 'react';
import { TransparencyReport } from '../../types';
import { ProductImage } from '../ProductImage';
import { Card } from '../Card';

interface ProductHeaderProps {
  report: TransparencyReport;
}

export const ProductHeader: React.FC<ProductHeaderProps> = ({ report }) => {
  return (
    <Card className="space-y-4">
      <div className="flex flex-col md:flex-row gap-5">
        <ProductImage
          barcode={report.barcode}
          productName={report.productName}
          className="w-24 h-24 sm:w-28 sm:h-28 rounded-lg object-cover border border-stone-250 dark:border-stone-800 shrink-0 mx-auto md:mx-0"
        />

        <div className="flex-1 space-y-1.5 text-center md:text-left">
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
      </div>
      
      <div className="text-xs text-stone-700 dark:text-stone-300 leading-relaxed bg-stone-50 dark:bg-stone-850 p-3 rounded-lg border border-stone-200 dark:border-stone-800">
        <strong>Verdict:</strong> {report.executiveSummary.verdictTitle}
      </div>
    </Card>
  );
};
