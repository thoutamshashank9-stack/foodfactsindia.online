import React, { useState } from 'react';
import { Globe, Search, ShieldAlert, CheckCircle2, AlertTriangle, ExternalLink, Info, Filter } from 'lucide-react';
import { INGREDIENT_DATABASE } from '../data/ingredientsDatabase';

export const GlobalRegulatoryMatrix: React.FC = () => {
  const [search, setSearch] = useState('');
  const [filterCategory, setFilterCategory] = useState<string>('ALL');

  const filteredIngredients = INGREDIENT_DATABASE.filter((ing) => {
    const matchesSearch =
      ing.canonicalName.toLowerCase().includes(search.toLowerCase()) ||
      (ing.insNumber && ing.insNumber.includes(search)) ||
      (ing.eNumber && ing.eNumber.toLowerCase().includes(search.toLowerCase())) ||
      ing.description.toLowerCase().includes(search.toLowerCase());

    const matchesCat =
      filterCategory === 'ALL' ||
      (filterCategory === 'BANNED' && ing.regulatoryRecords.some((r) => r.status === 'BANNED')) ||
      (filterCategory === 'HIGH_RISK' && ing.riskLevel === 'HIGH') ||
      (filterCategory === 'COLORS' && ing.category === 'ARTIFICIAL_COLOR');

    return matchesSearch && matchesCat;
  });

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      
      {/* Header */}
      <div className="p-6 sm:p-8 rounded-3xl bg-slate-900 text-white shadow-xl flex flex-col sm:flex-row justify-between items-start sm:items-center gap-6">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-blue-500/20 border border-blue-500/30 text-blue-300 text-xs font-semibold mb-3">
            <Globe className="w-4 h-4 text-blue-400" />
            <span>Cross-Jurisdictional Food Regulation Database</span>
          </div>
          <h2 className="text-2xl sm:text-3xl font-extrabold tracking-tight">
            Global Food Additive Ban & Restriction Matrix
          </h2>
          <p className="text-sm text-slate-400 mt-1 max-w-2xl leading-relaxed">
            Compare food additive regulations side-by-side across India (FSSAI), European Union (EFSA), United States (FDA), and Japan (MHLW).
          </p>
        </div>
      </div>

      {/* Search & Filters */}
      <div className="flex flex-col sm:flex-row items-center gap-4 bg-white dark:bg-slate-900 p-4 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-md">
        <div className="relative flex-1 w-full">
          <Search className="absolute left-3.5 top-3.5 w-4 h-4 text-slate-400" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search by ingredient, INS code, E-number (e.g. E102, TBHQ, Titanium Dioxide)..."
            className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-sm font-medium focus:outline-none focus:border-blue-600"
          />
        </div>

        <div className="flex items-center gap-2 w-full sm:w-auto">
          <Filter className="w-4 h-4 text-slate-400 shrink-0" />
          <select
            value={filterCategory}
            onChange={(e) => setFilterCategory(e.target.value)}
            className="w-full sm:w-auto px-3.5 py-2.5 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-xs font-semibold text-slate-700 dark:text-slate-200 focus:outline-none"
          >
            <option value="ALL">All Additives</option>
            <option value="BANNED">Banned in ≥1 Market</option>
            <option value="HIGH_RISK">High Concern Only</option>
            <option value="COLORS">Artificial Colors</option>
          </select>
        </div>
      </div>

      {/* Database Table */}
      <div className="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 shadow-xl overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-slate-50 dark:bg-slate-850 border-b border-slate-200 dark:border-slate-800 text-xs font-bold text-slate-600 dark:text-slate-400 uppercase tracking-wider">
                <th className="p-4 pl-6">Additive / Ingredient</th>
                <th className="p-4 text-center">🇮🇳 India (FSSAI)</th>
                <th className="p-4 text-center">🇪🇺 EU (EFSA)</th>
                <th className="p-4 text-center">🇺🇸 US (FDA)</th>
                <th className="p-4 text-center">🇯🇵 Japan (MHLW)</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-slate-800 text-sm">
              {filteredIngredients.map((ing) => {
                const inRec = ing.regulatoryRecords.find((r) => r.countryCode === 'IN');
                const euRec = ing.regulatoryRecords.find((r) => r.countryCode === 'EU');
                const usRec = ing.regulatoryRecords.find((r) => r.countryCode === 'US');
                const jpRec = ing.regulatoryRecords.find((r) => r.countryCode === 'JP');

                const renderBadge = (rec?: typeof inRec) => {
                  if (!rec) return <span className="text-slate-400 text-xs">—</span>;
                  if (rec.status === 'BANNED') {
                    return (
                      <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg bg-rose-100 text-rose-800 dark:bg-rose-950 dark:text-rose-300 text-xs font-extrabold uppercase">
                        <ShieldAlert className="w-3.5 h-3.5" /> Banned
                      </span>
                    );
                  }
                  if (rec.status === 'RESTRICTED') {
                    return (
                      <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300 text-xs font-bold">
                        <AlertTriangle className="w-3.5 h-3.5" /> Restricted
                      </span>
                    );
                  }
                  return (
                    <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300 text-xs font-semibold">
                      <CheckCircle2 className="w-3.5 h-3.5" /> Approved
                    </span>
                  );
                };

                return (
                  <tr key={ing.id} className="hover:bg-slate-50/80 dark:hover:bg-slate-800/50 transition-colors">
                    <td className="p-4 pl-6">
                      <div className="flex items-center gap-2">
                        <span className="font-bold text-slate-900 dark:text-white">
                          {ing.canonicalName}
                        </span>
                        {ing.eNumber && (
                          <span className="px-1.5 py-0.5 rounded bg-slate-100 dark:bg-slate-800 font-mono text-[10px] font-bold text-slate-600 dark:text-slate-300">
                            {ing.eNumber}
                          </span>
                        )}
                        {ing.insNumber && !ing.eNumber && (
                          <span className="px-1.5 py-0.5 rounded bg-slate-100 dark:bg-slate-800 font-mono text-[10px] font-bold text-slate-600 dark:text-slate-300">
                            INS {ing.insNumber}
                          </span>
                        )}
                      </div>
                      <p className="text-xs text-slate-500 dark:text-slate-400 mt-1 max-w-md line-clamp-2 leading-relaxed">
                        {ing.description}
                      </p>
                    </td>
                    <td className="p-4 text-center">{renderBadge(inRec)}</td>
                    <td className="p-4 text-center">{renderBadge(euRec)}</td>
                    <td className="p-4 text-center">{renderBadge(usRec)}</td>
                    <td className="p-4 text-center">{renderBadge(jpRec)}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
