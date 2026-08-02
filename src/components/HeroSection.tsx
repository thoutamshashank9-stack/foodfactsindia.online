import React, { useState, useEffect } from 'react';
import { Search, Scan, Sparkles, ShieldCheck, ArrowRight, ShieldAlert, CheckCircle2, AlertCircle, Loader2 } from 'lucide-react';
import { TransparencyReport } from '../types';
import { searchLiveProducts, isNonFoodProduct } from '../services/supabaseService';

interface HeroSectionProps {
  products: TransparencyReport[];
  onSelectProduct: (product: TransparencyReport) => void;
  onOpenScan: () => void;
  onGoToAnalyzer: () => void;
}

export const HeroSection: React.FC<HeroSectionProps> = ({
  products,
  onSelectProduct,
  onOpenScan,
  onGoToAnalyzer,
}) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<TransparencyReport[]>([]);
  const [isSearching, setIsSearching] = useState(false);

  useEffect(() => {
    if (!searchQuery.trim()) {
      setSearchResults([]);
      setIsSearching(false);
      return;
    }

    const timer = setTimeout(async () => {
      setIsSearching(true);
      try {
        // First search local preseeded products & filter non-food items
        const localMatches = products
          .filter(p => !isNonFoodProduct(p))
          .filter(
            (p) =>
              p.productName.toLowerCase().includes(searchQuery.toLowerCase()) ||
              p.brand.toLowerCase().includes(searchQuery.toLowerCase()) ||
              p.category.toLowerCase().includes(searchQuery.toLowerCase())
          );

        // Fetch live matches from Supabase 19,813 products database
        const liveMatches = await searchLiveProducts(searchQuery);

        // Combine local + live results without duplicate barcodes
        const combined = [...localMatches];
        for (const liveP of liveMatches) {
          if (!combined.some(c => c.barcode === liveP.barcode)) {
            combined.push(liveP);
          }
        }

        setSearchResults(combined);
      } catch (err) {
        console.error('Realtime search error:', err);
      } finally {
        setIsSearching(false);
      }
    }, 250);

    return () => clearTimeout(timer);
  }, [searchQuery, products]);

  const getIssuesCount = (p: TransparencyReport) =>
    p.scoreBreakdown ? p.scoreBreakdown.filter((b) => b.type === 'DEDUCTION').length : 0;

  return (
    <section className="relative pt-8 pb-12 overflow-hidden">
      {/* Dynamic Background Mesh Gradients */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full max-w-7xl h-96 bg-gradient-to-b from-blue-500/10 via-emerald-500/5 to-transparent blur-3xl -z-10 pointer-events-none" />

      <div className="max-w-4xl mx-auto px-4 text-center space-y-6">
        
        {/* Trust pill */}
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-blue-50 dark:bg-blue-950/60 border border-blue-200/80 dark:border-blue-800/80 text-blue-700 dark:text-blue-300 text-xs font-semibold shadow-sm">
          <ShieldCheck className="w-4 h-4 text-blue-600 dark:text-blue-400" />
          <span>India's Real-Time Food Transparency Engine (19,813 Products Sync)</span>
        </div>

        {/* Hero Title */}
        <h1 className="text-3xl sm:text-5xl font-extrabold tracking-tight leading-tight text-slate-900 dark:text-white">
          Know Exactly What You're Eating <br className="hidden sm:inline" />
          <span className="bg-gradient-to-r from-blue-600 via-emerald-600 to-teal-500 bg-clip-text text-transparent">
            Before You Buy.
          </span>
        </h1>

        {/* Hero Subtitle */}
        <p className="text-base sm:text-lg text-slate-600 dark:text-slate-300 max-w-2xl mx-auto leading-relaxed">
          Instantly decode ingredient lists, INS/E additive codes, global bans across EU, FDA & FSSAI, and peer-reviewed scientific studies in seconds.
        </p>

        {/* Search Box Component */}
        <div className="relative max-w-2xl mx-auto mt-6">
          <div className="relative flex items-center">
            <Search className="absolute left-4 w-5 h-5 text-slate-400 pointer-events-none" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search 19,800+ products (e.g. Red Bull, Bambino, Maggi, Lays)..."
              className="w-full pl-12 pr-12 py-4 rounded-2xl bg-white dark:bg-slate-900 border-2 border-slate-200 dark:border-slate-700/80 text-slate-900 dark:text-white placeholder-slate-400 focus:outline-none focus:border-blue-600 dark:focus:border-blue-500 shadow-xl shadow-slate-200/50 dark:shadow-none text-sm sm:text-base font-medium transition-all"
            />
            {isSearching && (
              <Loader2 className="absolute right-4 w-5 h-5 text-blue-600 animate-spin pointer-events-none" />
            )}
          </div>

          {/* Autocomplete Results Dropdown */}
          {searchQuery.trim() && (
            <div className="absolute top-full left-0 right-0 mt-2 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-2xl overflow-hidden z-30 max-h-80 overflow-y-auto text-left divide-y divide-slate-100 dark:divide-slate-800">
              {isSearching && searchResults.length === 0 ? (
                <div className="p-4 text-center text-xs text-slate-500 dark:text-slate-400 flex items-center justify-center gap-2">
                  <Loader2 className="w-4 h-4 text-blue-600 animate-spin" />
                  <span>Searching 19,813 live products in Supabase...</span>
                </div>
              ) : searchResults.length > 0 ? (
                searchResults.map((product) => {
                  const issues = getIssuesCount(product);
                  return (
                    <div
                      key={product.productId}
                      onClick={() => {
                        onSelectProduct(product);
                        setSearchQuery('');
                      }}
                      className="p-3.5 hover:bg-blue-50/60 dark:hover:bg-slate-800/80 cursor-pointer flex items-center justify-between transition-colors"
                    >
                      <div className="flex items-center gap-3">
                        <img
                          src={product.imageUrl}
                          alt={product.productName}
                          className="w-12 h-12 rounded-xl object-cover border border-slate-200 dark:border-slate-700"
                        />
                        <div>
                          <h4 className="font-bold text-sm text-slate-900 dark:text-white">
                            {product.productName}
                          </h4>
                          <p className="text-xs text-slate-500 dark:text-slate-400">
                            {product.brand} • {product.category} (Barcode: {product.barcode})
                          </p>
                        </div>
                      </div>

                      <div className="flex items-center gap-2">
                        <span className={`px-2 py-0.5 rounded text-xs font-bold ${
                          issues > 0
                            ? 'bg-rose-100 text-rose-800 dark:bg-rose-950 dark:text-rose-300'
                            : 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300'
                        }`}>
                          {issues > 0 ? `${issues} Issues Flagged` : 'Clean Label'}
                        </span>
                        <ArrowRight className="w-4 h-4 text-slate-400" />
                      </div>
                    </div>
                  );
                })
              ) : (
                <div className="p-4 text-center text-xs text-slate-500 dark:text-slate-400 flex flex-col items-center gap-2">
                  <AlertCircle className="w-5 h-5 text-amber-500" />
                  {/^[0-9]{8,14}$/.test(searchQuery.trim()) ? (
                    <span>Barcode ({searchQuery.trim()}) is not added in our database. We currently only maintain data for verified food products; beauty and non-food items are not in our database.</span>
                  ) : (
                    <span>No matching products found in live database for "{searchQuery}". Try "Red Bull", "Bambino", "Maggi", or "Lay's".</span>
                  )}
                </div>
              )}
            </div>
          )}
        </div>

        {/* Quick Action Badges & Demo Shortcuts */}
        <div className="flex flex-wrap items-center justify-center gap-2 pt-2">
          <span className="text-xs text-slate-500 dark:text-slate-400 font-medium mr-1">Quick Demo Pick:</span>
          <button
            onClick={() => setSearchQuery('Red Bull')}
            className="px-3 py-1 rounded-full bg-slate-100 dark:bg-slate-800/80 hover:bg-blue-100 dark:hover:bg-blue-950 text-slate-700 dark:text-slate-300 hover:text-blue-600 dark:hover:text-blue-400 text-xs font-semibold border border-slate-200 dark:border-slate-700 transition-colors"
          >
            ⚡ Red Bull Green
          </button>
          <button
            onClick={() => setSearchQuery('Good Day')}
            className="px-3 py-1 rounded-full bg-slate-100 dark:bg-slate-800/80 hover:bg-blue-100 dark:hover:bg-blue-950 text-slate-700 dark:text-slate-300 hover:text-blue-600 dark:hover:text-blue-400 text-xs font-semibold border border-slate-200 dark:border-slate-700 transition-colors"
          >
            🍪 Good Day Cookies
          </button>
          <button
            onClick={() => setSearchQuery('Maggi')}
            className="px-3 py-1 rounded-full bg-slate-100 dark:bg-slate-800/80 hover:bg-blue-100 dark:hover:bg-blue-950 text-slate-700 dark:text-slate-300 hover:text-blue-600 dark:hover:text-blue-400 text-xs font-semibold border border-slate-200 dark:border-slate-700 transition-colors"
          >
            🍜 Maggi Noodles
          </button>
          <button
            onClick={() => setSearchQuery('Coca-Cola')}
            className="px-3 py-1 rounded-full bg-slate-100 dark:bg-slate-800/80 hover:bg-blue-100 dark:hover:bg-blue-950 text-slate-700 dark:text-slate-300 hover:text-blue-600 dark:hover:text-blue-400 text-xs font-semibold border border-slate-200 dark:border-slate-700 transition-colors"
          >
            🥤 Coca-Cola
          </button>
        </div>

        <div className="flex flex-wrap items-center justify-center gap-3 pt-3">
          <button
            onClick={onOpenScan}
            className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-bold text-xs shadow-md shadow-blue-500/20 transition-all hover:scale-105"
          >
            <Scan className="w-4 h-4" />
            <span>Scan Product Barcode</span>
          </button>

          <button
            onClick={onGoToAnalyzer}
            className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-slate-700 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-slate-800 font-bold text-xs shadow-sm transition-all hover:scale-105"
          >
            <Sparkles className="w-4 h-4 text-emerald-500" />
            <span>Custom Label OCR Analyzer</span>
          </button>
        </div>
      </div>
    </section>
  );
};
