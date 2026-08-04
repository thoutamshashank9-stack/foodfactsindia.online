import React, { useState } from 'react';
import { GitCompare, CheckCircle2, ShieldAlert, AlertTriangle, ArrowRight, Plus, Trash2 } from 'lucide-react';
import { TransparencyReport } from '../types';
import { PRESEEDED_PRODUCTS } from '../data/productsDatabase';
import { ScoreGauge } from './ScoreGauge';

interface ProductComparisonProps {
  products?: TransparencyReport[];
  onSelectProduct: (prod: TransparencyReport) => void;
}

export const ProductComparison: React.FC<ProductComparisonProps> = ({ products = PRESEEDED_PRODUCTS, onSelectProduct }) => {
  const [selectedIds, setSelectedIds] = useState<string[]>([
    products[0]?.productId || PRESEEDED_PRODUCTS[0].productId,
    products[1]?.productId || PRESEEDED_PRODUCTS[1].productId
  ]);

  const selectedProducts = products.filter((p) =>
    selectedIds.includes(p.productId)
  );

  const handleAddProduct = (id: string) => {
    if (!selectedIds.includes(id) && selectedIds.length < 3) {
      setSelectedIds([...selectedIds, id]);
    }
  };

  const handleRemoveProduct = (id: string) => {
    if (selectedIds.length > 1) {
      setSelectedIds(selectedIds.filter((i) => i !== id));
    }
  };

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      
      {/* Header */}
      <div className="p-6 sm:p-8 rounded-3xl bg-gradient-to-r from-blue-700 via-indigo-700 to-purple-800 text-white shadow-xl flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-white/10 text-xs font-semibold text-purple-200 mb-2">
            <GitCompare className="w-4 h-4" />
            <span>Side-by-Side Intelligence Matrix</span>
          </div>
          <h2 className="text-2xl sm:text-3xl font-extrabold tracking-tight">
            Compare Food Products Side-by-Side
          </h2>
          <p className="text-sm text-purple-100/90 mt-1 max-w-xl">
            Evaluate ingredient safety, added sugars, sodium density, and controversial additives across multiple products before purchasing.
          </p>
        </div>

        {/* Add product dropdown */}
        {selectedIds.length < 3 && (
          <div className="flex items-center gap-2 bg-white/10 p-2 rounded-2xl backdrop-blur-md">
            <Plus className="w-4 h-4 text-purple-200" />
            <select
              onChange={(e) => {
                if (e.target.value) handleAddProduct(e.target.value);
              }}
              defaultValue=""
              className="bg-transparent text-xs font-bold text-white focus:outline-none cursor-pointer"
            >
              <option value="" disabled className="text-slate-900">Add Product to Compare...</option>
              {PRESEEDED_PRODUCTS.filter((p) => !selectedIds.includes(p.productId)).map((p) => (
                <option key={p.productId} value={p.productId} className="text-slate-900">
                  {p.productName} (Score {p.deterministicScore})
                </option>
              ))}
            </select>
          </div>
        )}
      </div>

      {/* Comparison Grid */}
      <div className={`grid grid-cols-1 md:grid-cols-${selectedProducts.length} gap-6`}>
        {selectedProducts.map((product) => (
          <div
            key={product.productId}
            className="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 p-6 shadow-xl space-y-6 relative flex flex-col justify-between"
          >
            {/* Top Bar with Delete */}
            <div className="flex justify-between items-start">
              <span className="px-2.5 py-1 rounded-lg bg-blue-50 dark:bg-blue-950 text-blue-700 dark:text-blue-300 text-xs font-semibold">
                {product.category}
              </span>
              {selectedIds.length > 1 && (
                <button
                  onClick={() => handleRemoveProduct(product.productId)}
                  className="p-1.5 text-slate-400 hover:text-rose-500 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
                  title="Remove from comparison"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              )}
            </div>

            {/* Product Hero */}
            <div className="text-center space-y-3">
              <img
                src={product.imageUrl}
                alt={product.productName}
                className="w-24 h-24 mx-auto rounded-2xl object-cover border border-slate-200 dark:border-slate-700 shadow-md"
              />
              <h3 className="font-extrabold text-base text-slate-900 dark:text-white line-clamp-2">
                {product.productName}
              </h3>
              <p className="text-xs text-slate-500 dark:text-slate-400 font-medium">
                {product.brand} • {product.servingSize}
              </p>
            </div>

            {/* Score Gauge */}
            <div className="flex justify-center py-2">
              <ScoreGauge score={product.deterministicScore} grade={product.executiveSummary.grade} size="lg" />
            </div>

            {/* Matrix Breakdown Rows */}
            <div className="space-y-3 text-xs divide-y divide-slate-100 dark:divide-slate-800">
              
              <div className="pt-2 flex justify-between items-center">
                <span className="text-slate-500 dark:text-slate-400 font-medium">EU Nutri-Score (2024)</span>
                <span className="font-mono font-extrabold px-2 py-0.5 rounded bg-slate-100 dark:bg-slate-800 text-slate-900 dark:text-white">
                  Grade {product.internationalRatings?.nutriScore.grade || 'N/A'}
                </span>
              </div>

              <div className="pt-2 flex justify-between items-center">
                <span className="text-slate-500 dark:text-slate-400 font-medium">LatAm Warning Octagons</span>
                <span className="font-mono font-bold text-slate-900 dark:text-white">
                  {product.internationalRatings?.warningOctagons.length || 0} octagons
                </span>
              </div>

              <div className="pt-2 flex justify-between items-center">
                <span className="text-slate-500 dark:text-slate-400 font-medium">Added Sugar</span>
                <span className={`font-mono font-bold ${
                  product.nutrition.addedSugarG > 5 ? 'text-rose-600 dark:text-rose-400' : 'text-emerald-600 dark:text-emerald-400'
                }`}>
                  {product.nutrition.addedSugarG}g per serving
                </span>
              </div>

              <div className="pt-2 flex justify-between items-center">
                <span className="text-slate-500 dark:text-slate-400 font-medium">Sodium Density</span>
                <span className={`font-mono font-bold ${
                  product.nutrition.sodiumMg > 300 ? 'text-amber-600 dark:text-amber-400' : 'text-emerald-600 dark:text-emerald-400'
                }`}>
                  {product.nutrition.sodiumMg}mg
                </span>
              </div>

              <div className="pt-2 flex justify-between items-center">
                <span className="text-slate-500 dark:text-slate-400 font-medium">Controversial Additives</span>
                <span className="font-mono font-bold text-slate-900 dark:text-white">
                  {product.ingredientsList.filter((i) => i.isControversial).length} additives
                </span>
              </div>

              <div className="pt-2 flex justify-between items-center">
                <span className="text-slate-500 dark:text-slate-400 font-medium">NOVA Processing Level</span>
                <span className="font-mono font-bold text-slate-900 dark:text-white">
                  NOVA Class {product.executiveSummary.processingNovaClass}
                </span>
              </div>

            </div>

            {/* View Full Report Button */}
            <button
              onClick={() => onSelectProduct(product)}
              className="w-full py-3 rounded-2xl bg-slate-900 dark:bg-slate-100 text-white dark:text-slate-900 font-bold text-xs hover:bg-blue-600 dark:hover:bg-blue-400 transition-colors flex items-center justify-center gap-1.5"
            >
              <span>View Full Report</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>

          </div>
        ))}
      </div>

    </div>
  );
};
