import React from 'react';
import { Ingredient } from '../../types';
import { Beaker } from 'lucide-react';
import { CollapsibleSection } from '../CollapsibleSection';
import { Badge } from '../Badge';

interface IngredientTableProps {
  ingredientsList: { ingredient: Ingredient; rawName?: string }[];
  onSelectIngredient: (ing: Ingredient, rawName: string) => void;
}

export const IngredientTable: React.FC<IngredientTableProps> = ({
  ingredientsList,
  onSelectIngredient,
}) => {
  const getRiskVariant = (risk: string): 'success' | 'warning' | 'danger' | 'info' | 'neutral' => {
    const r = (risk || '').toLowerCase();
    if (r.includes('high') || r.includes('severe')) return 'danger';
    if (r.includes('medium') || r.includes('moderate')) return 'warning';
    if (r.includes('low') || r.includes('safe') || r.includes('minimal')) return 'success';
    return 'neutral';
  };

  const getRiskScore = (ing: Ingredient) => {
    const isBanned = ing.regulatoryRecords?.some((r) => r.status === 'BANNED');
    if (isBanned) return 4;
    const risk = (ing.riskLevel || '').toUpperCase();
    if (risk.includes('HIGH') || risk.includes('SEVERE')) return 3;
    if (risk.includes('MEDIUM') || risk.includes('MODERATE')) return 2;
    if (risk.includes('LOW') || risk.includes('SAFE') || risk.includes('MINIMAL')) return 1;
    return 0;
  };

  const sortedList = [...ingredientsList].sort((a, b) => {
    return getRiskScore(b.ingredient) - getRiskScore(a.ingredient);
  });

  const bannedCount = sortedList.filter((item) =>
    item.ingredient.regulatoryRecords?.some((r) => r.status === 'BANNED')
  ).length;

  return (
    <div className="w-full">
      <CollapsibleSection
        title={
          <div className="flex items-center gap-2">
            <Beaker className="w-4 h-4 text-teal-600 shrink-0" />
            <span>Ingredient & Additive Analysis</span>
          </div>
        }
        collapsedPreview={
          <div className="flex items-center gap-2 mt-2">
            <div className="px-3 py-1 rounded font-bold text-sm bg-stone-100 dark:bg-stone-800 text-stone-800 dark:text-stone-200">
              {ingredientsList.length} Ingredient{ingredientsList.length !== 1 ? 's' : ''}
            </div>
            {bannedCount > 0 && (
              <Badge label={`${bannedCount} Banned`} variant="danger" />
            )}
            <span className="text-sm font-medium text-stone-600 dark:text-stone-400">
              Click to view table
            </span>
          </div>
        }
      >
        <div className="overflow-x-auto -mx-5 px-5 pt-2">
          <table className="w-full text-left text-xs divide-y divide-stone-200 dark:divide-stone-800">
            <thead>
              <tr className="text-stone-400 font-mono text-[10px] uppercase">
                <th className="py-2.5 font-medium">Ingredient</th>
                <th className="py-2.5 font-medium">INS/E-Code</th>
                <th className="py-2.5 font-medium">Category</th>
                <th className="py-2.5 font-medium">Risk Profile</th>
                <th className="py-2.5 font-medium text-right">Details</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-stone-100 dark:divide-stone-850">
              {sortedList.map((item, idx) => {
                const ing = item.ingredient;
                const isBanned = ing.regulatoryRecords?.some((r) => r.status === 'BANNED');

                return (
                  <tr
                    key={ing.id || `ing_${idx}`}
                    onClick={() => onSelectIngredient(ing, item.rawName || ing.canonicalName)}
                    className={`hover:bg-stone-50 dark:hover:bg-stone-850/40 cursor-pointer transition-colors ${
                      isBanned ? 'bg-rose-50/30 dark:bg-rose-950/10' : ''
                    }`}
                  >
                    <td className="py-3 font-semibold text-stone-900 dark:text-stone-100">
                      <div className="flex items-center gap-1.5 flex-wrap">
                        <span>{ing.canonicalName}</span>
                        {isBanned && <Badge label="BANNED" variant="danger" />}
                      </div>
                    </td>
                    <td className="py-3 font-mono text-stone-500">
                      {ing.eNumber || '—'}
                    </td>
                    <td className="py-3 text-stone-605 dark:text-stone-300">
                      {ing.category}
                    </td>
                    <td className="py-3">
                      <Badge label={ing.riskLevel} variant={getRiskVariant(ing.riskLevel)} />
                    </td>
                    <td className="py-3 text-right text-teal-800 dark:text-teal-400 font-medium">
                      Evidence &rarr;
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </CollapsibleSection>
    </div>
  );
};
