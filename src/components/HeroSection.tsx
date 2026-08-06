import React, { useState, useEffect } from 'react';
import { Search, Scan, ArrowRight, Loader2, AlertCircle } from 'lucide-react';
import { TransparencyReport } from '../types';
import { searchLiveProducts, isNonFoodProduct } from '../services/supabaseService';

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
        const localMatches = products
          .filter(p => !isNonFoodProduct(p))
          .filter(
            (p) =>
              p.productName.toLowerCase().includes(searchQuery.toLowerCase()) ||
              p.brand.toLowerCase().includes(searchQuery.toLowerCase()) ||
              p.category.toLowerCase().includes(searchQuery.toLowerCase())
          );

        const liveMatches = await searchLiveProducts(searchQuery);

        const combined = [...localMatches];
        for (const liveP of liveMatches) {
          if (!combined.some(c => c.barcode === liveP.barcode)) {
            combined.push(liveP);
          }
        }

        setSearchResults(combined);
      } catch (err) {
        console.error('Search error:', err);
      } finally {
        setIsSearching(false);
      }
    }, 250);

    return () => clearTimeout(timer);
  }, [searchQuery, products]);

  const getIssuesCount = (p: TransparencyReport) =>
    p.scoreBreakdown ? p.scoreBreakdown.filter((b) => b.type === 'DEDUCTION').length : 0;

  const handleSearchSubmit = () => {
    if (searchQuery.trim()) {
      onGoToSearch(searchQuery.trim());
      setSearchQuery('');
      setSearchResults([]);
    }
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
              placeholder="Search products or ingredients..."
              className="w-full pl-11 pr-10 py-3 rounded-lg bg-white dark:bg-stone-900 border border-stone-300 dark:border-stone-700 text-stone-900 dark:text-stone-100 placeholder-stone-400 focus:outline-none focus:border-teal-700 dark:focus:border-teal-500 text-sm font-normal transition-all shadow-sm"
              aria-label="Search products or ingredients"
            />
            {isSearching && (
              <Loader2 className="absolute right-3.5 w-4 h-4 text-teal-700 animate-spin pointer-events-none" />
            )}
          </div>

          {/* Autocomplete Results Dropdown */}
          {searchQuery.trim() && (
            <div className="absolute top-full left-0 right-0 mt-2 bg-white dark:bg-stone-900 border border-stone-200 dark:border-stone-800 rounded-lg shadow-lg overflow-hidden z-30 max-h-80 overflow-y-auto text-left divide-y divide-stone-100 dark:divide-stone-800">
              {isSearching && searchResults.length === 0 ? (
                <div className="p-4 text-center text-xs text-stone-500 flex items-center justify-center gap-2">
                  <Loader2 className="w-3.5 h-3.5 text-teal-700 animate-spin" />
                  <span>Searching verified database...</span>
                </div>
              ) : searchResults.length > 0 ? (
                <>
                  {searchResults.slice(0, 8).map((product) => {
                    const issues = getIssuesCount(product);
                    return (
                      <div
                        key={product.productId}
                        onClick={() => {
                          onSelectProduct(product);
                          setSearchQuery('');
                          setSearchResults([]);
                        }}
                        className="p-3 hover:bg-stone-50 dark:hover:bg-stone-800/80 cursor-pointer flex items-center justify-between transition-colors"
                      >
                        <div className="flex items-center gap-3">
                          <img
                            src={product.imageUrl}
                            alt={product.productName}
                            className="w-10 h-10 rounded object-cover border border-stone-200 dark:border-stone-700"
                          />
                          <div>
                            <h4 className="font-semibold text-sm text-stone-900 dark:text-stone-100">
                              {product.productName || 'Unknown Product'}
                            </h4>
                            {(product.brand || product.category) && (
                              <p className="text-xs text-stone-500 dark:text-stone-400">
                                {[product.brand, product.category].filter(Boolean).join(' • ')}
                              </p>
                            )}
                          </div>
                        </div>

                        <div className="flex items-center gap-2">
                          <span className="text-xs text-stone-500 font-mono">
                            {issues > 0 ? `${issues} signals` : 'Standard'}
                          </span>
                          <ArrowRight className="w-3.5 h-3.5 text-stone-400" />
                        </div>
                      </div>
                    );
                  })}
                  {searchResults.length > 8 && (
                    <button
                      onClick={handleSearchSubmit}
                      className="w-full p-3 text-center text-xs font-medium text-teal-800 dark:text-teal-400 hover:bg-stone-50 dark:hover:bg-stone-800/80 transition-colors"
                    >
                      View all {searchResults.length} results →
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
