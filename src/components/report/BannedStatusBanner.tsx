import React from 'react';
import { AlertOctagon } from 'lucide-react';
import { CollapsibleSection } from '../CollapsibleSection';

export interface BannedStatusBannerProps {
  bannedItems: {
    name: string;
    countries: string;
    reason: string;
    citations: string;
  }[];
}

export const BannedStatusBanner: React.FC<BannedStatusBannerProps> = ({ bannedItems }) => {
  if (!bannedItems || bannedItems.length === 0) return null;

  return (
    <div className="w-full">
      <CollapsibleSection
        title={
          <div className="flex items-center gap-2 text-red-600 dark:text-red-400">
            <AlertOctagon className="w-4 h-4 shrink-0" />
            <span>Banned Ingredients Detected</span>
          </div>
        }
        collapsedPreview={
          <div className="text-xs text-stone-600 dark:text-stone-400 leading-relaxed mt-1">
            {bannedItems.length === 1
              ? `${bannedItems[0].name} is banned in ${bannedItems[0].countries}.`
              : `${bannedItems.length} ingredients are banned in other countries.`}
          </div>
        }
      >
        <div className="space-y-4">
          {bannedItems.map((item, idx) => (
            <div key={idx} className="space-y-2 pb-4 border-b border-stone-100 dark:border-stone-800 last:border-0 last:pb-0">
              <div className="font-semibold text-sm text-stone-900 dark:text-stone-100">
                {item.name}
              </div>
              <div className="text-xs text-stone-600 dark:text-stone-400">
                <span className="font-medium text-stone-700 dark:text-stone-300">Banned in:</span> {item.countries}
              </div>
              <div className="text-xs text-stone-600 dark:text-stone-400">
                <span className="font-medium text-stone-700 dark:text-stone-300">Reason:</span> {item.reason}
              </div>
              {item.citations && (
                <div className="text-[10px] text-stone-500 font-mono mt-2 p-2 bg-stone-50 dark:bg-stone-850 rounded">
                  Citation: {item.citations}
                </div>
              )}
            </div>
          ))}
        </div>
      </CollapsibleSection>
    </div>
  );
};
