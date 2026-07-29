import React, { useState } from 'react';
import { Sparkles, FileText, ArrowRight, ShieldCheck, RefreshCw, CheckCircle2 } from 'lucide-react';
import { TransparencyReport } from '../types';
import { analyzeRawIngredientLabel } from '../services/aiAnalyzerService';

interface CustomLabelAnalyzerProps {
  onReportGenerated: (report: TransparencyReport) => void;
}

export const CustomLabelAnalyzer: React.FC<CustomLabelAnalyzerProps> = ({ onReportGenerated }) => {
  const [productName, setProductName] = useState('');
  const [brandName, setBrandName] = useState('');
  const [ingredientText, setIngredientText] = useState('');
  const [addedSugarInput, setAddedSugarInput] = useState<string>('');
  const [sodiumInput, setSodiumInput] = useState<string>('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const samplePresets = [
    {
      name: 'Diet Soda Formula',
      brand: 'Zero Soda Co',
      text: 'Carbonated Water, Caramel Color E150d, Phosphoric Acid, Aspartame INS 951, Potassium Benzoate, Caffeine, Natural Flavors, Citric Acid INS 330'
    },
    {
      name: 'Packaged Masala Biscuit',
      brand: 'Bakery Delight',
      text: 'Wheat Flour, Refined Palm Oil, Sugar, Salt, Raising Agents (INS 500ii, INS 503ii), Emulsifier (INS 322), Monosodium Glutamate INS 621, TBHQ INS 319'
    },
    {
      name: 'Organic Whole Oat Granola',
      brand: 'Nature Choice',
      text: 'Whole Rolled Oats, Honey, Dried Cranberries, Almonds, Sunflower Oil, Natural Vanilla Extract, Sea Salt'
    }
  ];

  const handleAnalyze = (e: React.FormEvent) => {
    e.preventDefault();
    if (!ingredientText.trim()) return;

    setIsAnalyzing(true);
    setTimeout(() => {
      setIsAnalyzing(false);
      const report = analyzeRawIngredientLabel(
        ingredientText,
        productName.trim() || 'Custom Analyzed Food Product',
        brandName.trim() || 'Generic Brand',
        {
          addedSugarG: addedSugarInput ? parseFloat(addedSugarInput) : undefined,
          sodiumMg: sodiumInput ? parseFloat(sodiumInput) : undefined
        }
      );
      onReportGenerated(report);
    }, 1500);
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      
      {/* Header Banner */}
      <div className="p-6 rounded-3xl bg-gradient-to-r from-blue-600 via-blue-700 to-indigo-800 text-white shadow-xl">
        <div className="flex items-start gap-4">
          <div className="p-3 rounded-2xl bg-white/10 backdrop-blur-md shrink-0">
            <Sparkles className="w-8 h-8 text-amber-300" />
          </div>
          <div>
            <div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-white/20 text-xs font-semibold text-blue-100 mb-2">
              <ShieldCheck className="w-3.5 h-3.5" />
              <span>AI Ingredient NLP & Deterministic Math Engine</span>
            </div>
            <h2 className="text-2xl font-extrabold tracking-tight">
              Paste Any Ingredient Label
            </h2>
            <p className="text-sm text-blue-100/90 mt-1 max-w-2xl leading-relaxed">
              Don't have a barcode? Copy & paste the ingredient text directly from any food package or online grocery listing to get an instant regulatory & health risk audit.
            </p>
          </div>
        </div>
      </div>

      {/* Preset Quick Fill */}
      <div className="bg-white dark:bg-slate-900 p-5 rounded-2xl border border-slate-200 dark:border-slate-800 space-y-3">
        <span className="text-xs font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider">
          Or test with instant sample ingredient labels:
        </span>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
          {samplePresets.map((preset, idx) => (
            <button
              key={idx}
              type="button"
              onClick={() => {
                setProductName(preset.name);
                setBrandName(preset.brand);
                setIngredientText(preset.text);
              }}
              className="p-3 rounded-xl bg-slate-50 dark:bg-slate-800/60 hover:bg-blue-50 dark:hover:bg-slate-700/60 border border-slate-200 dark:border-slate-700 text-left transition-all text-xs font-medium space-y-1"
            >
              <div className="font-bold text-slate-900 dark:text-white">{preset.name}</div>
              <div className="text-slate-500 dark:text-slate-400 text-[11px] line-clamp-1">{preset.text}</div>
            </button>
          ))}
        </div>
      </div>

      {/* Form */}
      <form onSubmit={handleAnalyze} className="bg-white dark:bg-slate-900 p-6 sm:p-8 rounded-3xl border border-slate-200 dark:border-slate-800 shadow-xl space-y-6">
        
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-700 dark:text-slate-300 mb-1.5">
              Product Name (Optional)
            </label>
            <input
              type="text"
              value={productName}
              onChange={(e) => setProductName(e.target.value)}
              placeholder="e.g. Masala Flavored Chips"
              className="w-full px-4 py-3 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-sm font-medium text-slate-900 dark:text-white focus:outline-none focus:border-blue-600"
            />
          </div>

          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-700 dark:text-slate-300 mb-1.5">
              Brand / Manufacturer (Optional)
            </label>
            <input
              type="text"
              value={brandName}
              onChange={(e) => setBrandName(e.target.value)}
              placeholder="e.g. Snacks India Ltd"
              className="w-full px-4 py-3 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-sm font-medium text-slate-900 dark:text-white focus:outline-none focus:border-blue-600"
            />
          </div>
        </div>

        {/* Main Raw Ingredient Input */}
        <div>
          <label className="block text-xs font-bold uppercase tracking-wider text-slate-700 dark:text-slate-300 mb-1.5 flex items-center justify-between">
            <span>Raw Ingredient List Text *</span>
            <span className="text-[11px] text-slate-400 font-normal">Supports INS/E numbers & codes</span>
          </label>
          <textarea
            rows={5}
            value={ingredientText}
            onChange={(e) => setIngredientText(e.target.value)}
            placeholder="Paste ingredients here... e.g. Wheat Flour, Sugar, Palm Oil, INS 102, INS 150d, Citric Acid, Salt, Monosodium Glutamate E621..."
            required
            className="w-full p-4 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-sm font-mono text-slate-900 dark:text-white focus:outline-none focus:border-blue-600 leading-relaxed"
          />
        </div>

        {/* Optional Nutrition Parameters */}
        <div className="p-4 rounded-2xl bg-slate-50 dark:bg-slate-800/40 border border-slate-200 dark:border-slate-700/60 space-y-3">
          <span className="text-xs font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wider block">
            Optional Nutrition Values (Improves Accuracy)
          </span>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-[11px] font-semibold text-slate-500 dark:text-slate-400 mb-1">
                Added Sugar (grams per 100g)
              </label>
              <input
                type="number"
                step="0.1"
                value={addedSugarInput}
                onChange={(e) => setAddedSugarInput(e.target.value)}
                placeholder="e.g. 12.5"
                className="w-full px-3 py-2 rounded-lg bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-xs font-medium text-slate-900 dark:text-white"
              />
            </div>
            <div>
              <label className="block text-[11px] font-semibold text-slate-500 dark:text-slate-400 mb-1">
                Sodium (mg per 100g)
              </label>
              <input
                type="number"
                step="1"
                value={sodiumInput}
                onChange={(e) => setSodiumInput(e.target.value)}
                placeholder="e.g. 850"
                className="w-full px-3 py-2 rounded-lg bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-xs font-medium text-slate-900 dark:text-white"
              />
            </div>
          </div>
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={isAnalyzing || !ingredientText.trim()}
          className="w-full py-4 rounded-2xl bg-gradient-to-r from-blue-600 via-blue-700 to-indigo-700 hover:from-blue-500 hover:to-indigo-600 text-white font-bold text-base shadow-xl shadow-blue-500/25 transition-all flex items-center justify-center gap-2 active:scale-98 disabled:opacity-50"
        >
          {isAnalyzing ? (
            <>
              <RefreshCw className="w-5 h-5 animate-spin" />
              <span>Analyzing Ingredients & Global DBs...</span>
            </>
          ) : (
            <>
              <Sparkles className="w-5 h-5 text-amber-300" />
              <span>Generate Transparency Report</span>
              <ArrowRight className="w-5 h-5" />
            </>
          )}
        </button>

      </form>
    </div>
  );
};
