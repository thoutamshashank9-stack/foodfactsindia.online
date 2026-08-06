import React from 'react';
import { Ingredient } from '../../types';
import { Card } from '../Card';
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

  const sortedList = [...ingredientsList].sort((a, b) => {
    const aBanned = a.ingredient.regulatoryRecords?.some((r) => r.status === 'BANNED') ? 1 : 0;
    const bBanned = b.ingredient.regulatoryRecords?.some((r) => r.status === 'BANNED') ? 1 : 0;
    return bBanned - aBanned;
  });

  return (
    <Card className="space-y-4">
      <h3 className="font-serif text-lg font-bold text-stone-900 dark:text-stone-100">
        Ingredient & Additive Analysis
      </h3>

      <div className="overflow-x-auto -mx-5 px-5">
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
                    isBanned ? 'bg-rose-50/30 dark:bg-rose-955/10' : ''
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
    </Card>
  );
};
