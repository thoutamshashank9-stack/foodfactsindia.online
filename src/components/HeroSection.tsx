import React, { useState, useEffect, useMemo } from 'react';
import { Search, Scan, ArrowRight, Loader2, AlertCircle, X } from 'lucide-react';
import { TransparencyReport } from '../types';
import { searchLiveProducts } from '../services/supabaseService';
import { searchTransparencyReports } from '../services/searchService';

interface HeroSectionProps {
  products: TransparencyReport[];
  onSelectProduct: (product: TransparencyReport) => void;
  onOpenScan: () => void;
  onGoToSearch: (query: string) => void;
}

export const HeroSection: React.FC<HeroSectionProps> = ({
  products,
  onSelectProduct,
  onOpenScan,
  onGoToSearch,
}) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [liveSearchResults, setLiveSearchResults] = useState<TransparencyReport[]>([]);
  const [isSearching, setIsSearching] = useState(false);

  // 1. Instant local search (0ms latency, zero lag on keystroke)
  const localSearchResults = useMemo(() => {
    return searchTransparencyReports(products, searchQuery);
  }, [products, searchQuery]);

  // Combine local & live results seamlessly and enforce completeness ranking (full details first)
  const combinedResults = useMemo(() => {
    if (!searchQuery.trim()) return [];
    const list = [...localSearchResults];
    for (const liveP of liveSearchResults) {
      if (!list.some(item => item.barcode === liveP.barcode || item.productId === liveP.productId)) {
        list.push(liveP);
      }
    }
    // Re-rank combined items so full detail products always appear FIRST
    return searchTransparencyReports(list, searchQuery);
  }, [searchQuery, localSearchResults, liveSearchResults]);

  // 2. Background network enrichment (200ms debounce)
  useEffect(() => {
    if (!searchQuery.trim()) {
      setLiveSearchResults([]);
      setIsSearching(false);
      return;
    }

    const timer = setTimeout(async () => {
      setIsSearching(true);
      try {
        const liveMatches = await searchLiveProducts(searchQuery);
        setLiveSearchResults(liveMatches || []);
      } catch (err) {
        console.error('Live search error:', err);
      } finally {
        setIsSearching(false);
      }
    }, 200);

    return () => clearTimeout(timer);
  }, [searchQuery]);

  const getIssuesCount = (p: TransparencyReport) =>
    p.scoreBreakdown ? p.scoreBreakdown.filter((b) => b.type === 'DEDUCTION').length : 0;

  const handleSearchSubmit = () => {
    const q = searchQuery.trim();
    if (!q) return;

    // Direct resolution: If user typed an exact barcode or title match, navigate directly to product
    const cleanDigits = q.replace(/[^0-9]/g, '');
    const exactBarcodeMatch = combinedResults.find(p => p.barcode === cleanDigits || p.barcode === q);
    if (exactBarcodeMatch) {
      onSelectProduct(exactBarcodeMatch);
      setSearchQuery('');
      setLiveSearchResults([]);
      return;
    }

    // Otherwise navigate to products tab search
    onGoToSearch(q);
    setSearchQuery('');
    setLiveSearchResults([]);
  };

  return (
    <section className="pt-12 pb-10 border-b border-stone-200 dark:border-stone-800/80">
      <div className="max-w-3xl mx-auto px-4 text-center space-y-6">
        
        {/* Eyebrow */}
        <p className="text-xs font-semibold uppercase tracking-wider text-teal-800 dark:text-teal-400">
          Evidence-based food transparency
        </p>

        {/* Headline */}
        <h1 className="font-serif text-4xl sm:text-5xl lg:text-6xl font-normal leading-tight text-stone-900 dark:text-stone-100">
          What packaged food labels don't make obvious.
        </h1>

        {/* Body */}
        <p className="text-base sm:text-lg text-stone-600 dark:text-stone-300 max-w-2xl mx-auto leading-relaxed font-normal">
          Declared ingredients, additives, and nutrition facts — reviewed through a clearer public-interest lens.
        </p>

        {/* Search Box */}
        <div className="relative max-w-xl mx-auto pt-2">
          <div className="relative flex items-center">
            <Search className="absolute left-4 w-4 h-4 text-stone-400 pointer-events-none" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter') {
                  e.preventDefault();
                  handleSearchSubmit();
                }
              }}
              placeholder="Search by product name, brand, barcode (e.g. 890...), or additive (e.g. TBHQ, E122)..."
              className="w-full pl-11 pr-10 py-3 rounded-lg bg-white dark:bg-stone-900 border border-stone-300 dark:border-stone-700 text-stone-900 dark:text-stone-100 placeholder-stone-400 focus:outline-none focus:border-teal-700 dark:focus:border-teal-500 text-sm font-normal transition-all shadow-sm"
              aria-label="Search products or ingredients"
            />
            <div className="absolute right-3.5 flex items-center gap-1.5">
              {isSearching && (
                <Loader2 className="w-4 h-4 text-teal-700 animate-spin pointer-events-none" />
              )}
              {searchQuery && (
                <button
                  type="button"
                  onClick={() => {
                    setSearchQuery('');
                    setLiveSearchResults([]);
                  }}
                  className="p-1 rounded-full text-stone-400 hover:text-stone-600 dark:hover:text-stone-200 transition-colors"
                  aria-label="Clear search"
                >
                  <X className="w-4 h-4" />
                </button>
              )}
            </div>
          </div>

          {/* Autocomplete Results Dropdown */}
          {searchQuery.trim() && (
            <div className="absolute top-full left-0 right-0 mt-2 bg-white dark:bg-stone-900 border border-stone-200 dark:border-stone-800 rounded-lg shadow-lg overflow-hidden z-30 max-h-80 overflow-y-auto text-left divide-y divide-stone-100 dark:divide-stone-800">
              {isSearching && combinedResults.length === 0 ? (
                <div className="p-4 text-center text-xs text-stone-500 flex items-center justify-center gap-2">
                  <Loader2 className="w-3.5 h-3.5 text-teal-700 animate-spin" />
                  <span>Searching verified database...</span>
                </div>
              ) : combinedResults.length > 0 ? (
                <>
                  {combinedResults.slice(0, 8).map((product) => {
                    const issues = getIssuesCount(product);
                    return (
                      <div
                        key={product.productId}
                        onClick={() => {
                          onSelectProduct(product);
                          setSearchQuery('');
                          setLiveSearchResults([]);
                        }}
                        className="p-3 hover:bg-stone-50 dark:hover:bg-stone-800/80 cursor-pointer flex items-center justify-between transition-colors"
                      >
                        <div className="flex items-center gap-3 min-w-0">
                          <img
                            src={product.imageUrl}
                            alt={product.productName}
                            className="w-10 h-10 rounded object-cover border border-stone-200 dark:border-stone-700 shrink-0"
                          />
                          <div className="min-w-0">
                            <h4 className="font-semibold text-sm text-stone-900 dark:text-stone-100 truncate">
                              {product.productName || 'Unknown Product'}
                            </h4>
                            <p className="text-xs text-stone-500 dark:text-stone-400 truncate">
                              {[product.brand, product.category, product.barcode].filter(Boolean).join(' • ')}
                            </p>
                          </div>
                        </div>

                        <div className="flex items-center gap-2 shrink-0 ml-2">
                          <span className="text-xs text-stone-500 font-mono">
                            {issues > 0 ? `${issues} signals` : 'Standard'}
                          </span>
                          <ArrowRight className="w-3.5 h-3.5 text-stone-400" />
                        </div>
                      </div>
                    );
                  })}
                  {combinedResults.length > 8 && (
                    <button
                      onClick={handleSearchSubmit}
                      className="w-full p-3 text-center text-xs font-medium text-teal-800 dark:text-teal-400 hover:bg-stone-50 dark:hover:bg-stone-800/80 transition-colors"
                    >
                      View all {combinedResults.length} results →
                    </button>
                  )}
                </>
              ) : (
                <div className="p-4 text-center text-xs text-stone-500 flex flex-col items-center gap-1.5">
                  <AlertCircle className="w-4 h-4 text-stone-400" />
                  <span>No product matches found for "{searchQuery}".</span>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Primary & Secondary Actions */}
        <div className="flex items-center justify-center gap-4 pt-1">
          <button
            onClick={handleSearchSubmit}
            className="px-5 py-2.5 rounded-md bg-teal-800 hover:bg-teal-900 dark:bg-teal-700 dark:hover:bg-teal-600 text-white font-medium text-sm transition-colors shadow-sm"
          >
            Search products
          </button>

          <button
            onClick={onOpenScan}
            className="inline-flex items-center gap-2 px-4 py-2.5 rounded-md bg-stone-100 dark:bg-stone-800 text-stone-800 dark:text-stone-200 hover:bg-stone-200 dark:hover:bg-stone-700 font-medium text-sm transition-colors"
          >
            <Scan className="w-4 h-4 text-stone-500" />
            <span>Scan barcode</span>
          </button>
        </div>

        {/* Method line */}
        <p className="text-xs text-stone-500 dark:text-stone-400 pt-2 font-normal">
          Built to support awareness, public discussion, and better front-of-pack labeling.
        </p>

      </div>
    </section>
  );
};
