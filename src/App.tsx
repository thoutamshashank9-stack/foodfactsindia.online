import React, { useState, useEffect, useMemo, useCallback, useRef, Suspense, lazy } from 'react';
import { Header } from './components/Header';
import { HeroSection } from './components/HeroSection';
import { WhyThisMatters } from './components/WhyThisMatters';
import { MethodologySnapshot } from './components/MethodologySnapshot';
import { AboutView } from './components/AboutView';
import { GrievanceView } from './components/GrievanceView';
import { TermsView } from './components/TermsView';
import { TransparencyReportView } from './components/TransparencyReportView';
import { Footer } from './components/Footer';
import { PRESEEDED_PRODUCTS } from './data/productsDatabase';
import { TransparencyReport } from './types';
import { Grid, ShieldAlert, CheckCircle2, Database, Search, ArrowRight, HelpCircle, ChevronLeft, ChevronRight } from 'lucide-react';
import { fetchLiveCatalog } from './services/supabaseService';
import { fetchRawIngredientsTaxonomyAsync } from './services/decoupledAdditiveService';

// Lazy-loaded components for route code-splitting
const ScanScannerModal = lazy(() => import('./components/ScanScannerModal').then(m => ({ default: m.ScanScannerModal })));
const GlobalRegulatoryMatrix = lazy(() => import('./components/GlobalRegulatoryMatrix').then(m => ({ default: m.GlobalRegulatoryMatrix })));
const ProductComparison = lazy(() => import('./components/ProductComparison').then(m => ({ default: m.ProductComparison })));

// Strict category taxonomy — no fuzzy .includes() matching
const CATEGORY_MAP: Record<string, string[]> = {
  NOODLES:    ['instant noodles', 'noodles', 'pasta', 'vermicelli', 'sevai', 'instant noodles & pasta'],
  BEVERAGES:  ['beverages', 'soft drinks', 'energy drinks', 'juices', 'cola', 'water', 'carbonated drinks', 'fruit juices'],
  SNACKS:     ['snacks', 'chips', 'crisps', 'namkeen', 'potato chips', 'salty snacks'],
  CHOCOLATE:  ['chocolates', 'confectionery', 'candy', 'chocolate'],
};
const CATEGORY_CHIPS = ['ALL', 'NOODLES', 'BEVERAGES', 'SNACKS', 'CHOCOLATE'] as const;
const ITEMS_PER_PAGE = 12;

// ─── Shared tab type ────────────────────────────────────────────────────────
type TabId = 'home' | 'products' | 'methodology' | 'compare' | 'about' | 'grievance' | 'terms';

// ─── History state shape ────────────────────────────────────────────────────
interface HistoryState {
  tab: TabId;
  productId: string | null;
}

export function App() {
  const [currentTab, setCurrentTab] = useState<TabId>('home');
  const [selectedProduct, setSelectedProduct] = useState<TransparencyReport | null>(null);
  const [darkMode, setDarkMode] = useState<boolean>(false);
  const [isScanOpen, setIsScanOpen] = useState<boolean>(false);
  const [filterCategory, setFilterCategory] = useState<string>('ALL');
  const [catalogProducts, setCatalogProducts] = useState<TransparencyReport[]>(PRESEEDED_PRODUCTS);
  const [globalSearchQuery, setGlobalSearchQuery] = useState<string>('');
  const [currentPage, setCurrentPage] = useState<number>(1);

  // ─── Browser History Integration ────────────────────────────────────────────
  // Ref guards prevent infinite loops: pushState → state change → pushState...
  const isRestoringFromHistory = useRef(false);
  const catalogRef = useRef(catalogProducts);
  catalogRef.current = catalogProducts;

  // Replace the initial history entry with our current state on mount
  useEffect(() => {
    const initialState: HistoryState = { tab: 'home', productId: null };
    window.history.replaceState(initialState, '');
  }, []);

  // Listen for browser back/forward button presses
  useEffect(() => {
    const onPopState = (event: PopStateEvent) => {
      const state = event.state as HistoryState | null;
      if (!state) {
        // Fell off the bottom of our history stack — go to home
        isRestoringFromHistory.current = true;
        setCurrentTab('home');
        setSelectedProduct(null);
        isRestoringFromHistory.current = false;
        return;
      }

      isRestoringFromHistory.current = true;
      setCurrentTab(state.tab);

      if (state.productId) {
        const product = catalogRef.current.find(p => p.productId === state.productId) ?? null;
        setSelectedProduct(product);
      } else {
        setSelectedProduct(null);
      }
      isRestoringFromHistory.current = false;
    };

    window.addEventListener('popstate', onPopState);
    return () => window.removeEventListener('popstate', onPopState);
  }, []);

  /** Push a new history entry (skipped when we're restoring from popstate). */
  const pushHistoryState = useCallback((tab: string, productId: string | null) => {
    if (isRestoringFromHistory.current) return;
    const histState: HistoryState = { tab: tab as HistoryState['tab'], productId };
    window.history.pushState(histState, '');
  }, []);

  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [darkMode]);

  // Load product catalog from Supabase
  useEffect(() => {
    fetchRawIngredientsTaxonomyAsync();

    async function loadCatalog() {
      try {
        const liveData = await fetchLiveCatalog();
        if (liveData && liveData.length > 0) {
          const merged = [...PRESEEDED_PRODUCTS];
          for (const item of liveData) {
            if (!merged.some(m => m.barcode === item.barcode)) {
              merged.push(item);
            }
          }
          setCatalogProducts(merged);
        }
      } catch (err) {
        console.error('Failed to load live catalog:', err);
      }
    }

    loadCatalog();
  }, []);

  const handleSelectProduct = useCallback((product: TransparencyReport) => {
    setSelectedProduct(product);
    pushHistoryState(currentTab, product.productId);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, [currentTab, pushHistoryState]);

  const handleBackToCatalog = useCallback(() => {
    // Use the browser's history stack so the native back button stays in sync
    if (window.history.state?.productId) {
      window.history.back();
    } else {
      setSelectedProduct(null);
    }
  }, []);

  // Search handler — wired from HeroSection and Header
  const handleGoToSearch = useCallback((query: string) => {
    setGlobalSearchQuery(query);
    setFilterCategory('ALL');
    setCurrentPage(1);
    setCurrentTab('products');
    setSelectedProduct(null);
  }, []);

  // Breadcrumb category filter handler
  const handleCategoryFilter = useCallback((category: string) => {
    setSelectedProduct(null);
    setGlobalSearchQuery(category);
    setFilterCategory('ALL');
    setCurrentPage(1);
    setCurrentTab('products');
  }, []);

  // Filtered & searched catalog
  const filteredCatalog = useMemo(() => {
    let list = catalogProducts;

    // Apply search query if present
    if (globalSearchQuery.trim()) {
      const q = globalSearchQuery.toLowerCase();
      list = list.filter((p) =>
        p.productName.toLowerCase().includes(q) ||
        p.brand.toLowerCase().includes(q) ||
        p.category.toLowerCase().includes(q)
      );
    }

    // Apply strict category filter
    if (filterCategory !== 'ALL') {
      const allowed = CATEGORY_MAP[filterCategory] ?? [];
      list = list.filter((p) => {
        const cat = p.category.toLowerCase().trim();
        return allowed.some(term => cat === term || cat.startsWith(term));
      });
    }

    return list;
  }, [catalogProducts, filterCategory, globalSearchQuery]);

  // Paginated slice
  const totalPages = Math.max(1, Math.ceil(filteredCatalog.length / ITEMS_PER_PAGE));
  const paginatedCatalog = useMemo(() => {
    const start = (currentPage - 1) * ITEMS_PER_PAGE;
    return filteredCatalog.slice(start, start + ITEMS_PER_PAGE);
  }, [filteredCatalog, currentPage]);

  // Reset page when filters change
  useEffect(() => {
    setCurrentPage(1);
  }, [filterCategory, globalSearchQuery]);

  // Featured verified products for homepage (verified published only, max 6)
  const featuredVerifiedProducts = useMemo(() => {
    return catalogProducts
      .filter((p) => (!p.pageState || p.pageState === 'verified_published') && !p.isScoreWithheld)
      .slice(0, 6);
  }, [catalogProducts]);

  // Render score badge — "Not Yet Rated" for unscored products
  const renderScoreBadge = (product: TransparencyReport) => {
    if (product.isScoreWithheld || (product.pageState && product.pageState !== 'verified_published')) {
      return (
        <span className="text-stone-400 dark:text-stone-500 flex items-center gap-1">
          <HelpCircle className="w-3 h-3" />
          <span>Not Yet Rated</span>
        </span>
      );
    }
    return (
      <span className="text-stone-500">
        Score: <strong className="text-stone-900 dark:text-stone-100 font-semibold">{product.deterministicScore}/100</strong>
      </span>
    );
  };

  return (
    <div className="min-h-screen flex flex-col bg-[#fcfbf9] dark:bg-[#0e1117] text-[#1c2128] dark:text-[#e6edf3] transition-colors duration-200">
      
      {/* Navigation Header */}
      <Header
        currentTab={currentTab}
        setCurrentTab={(tab) => {
          setCurrentTab(tab);
          setSelectedProduct(null);
          setGlobalSearchQuery('');
          pushHistoryState(tab, null);
        }}
        darkMode={darkMode}
        setDarkMode={setDarkMode}
        onOpenScan={() => setIsScanOpen(true)}
        onSearchClick={() => {
          setCurrentTab('products');
          setSelectedProduct(null);
        }}
      />

      {/* Main Content Area */}
      <main className="flex-1 max-w-6xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">
        
        {/* Active Product Report View */}
        {selectedProduct ? (
          <TransparencyReportView 
            report={selectedProduct} 
            onBackToSearch={handleBackToCatalog}
            onCategoryFilter={handleCategoryFilter}
          />
        ) : (
          <>
            {/* 1. HOMEPAGE TAB */}
            {currentTab === 'home' && (
              <div className="space-y-12">
                {/* Hero Section */}
                <HeroSection
                  products={catalogProducts}
                  onSelectProduct={handleSelectProduct}
                  onOpenScan={() => setIsScanOpen(true)}
                  onGoToSearch={handleGoToSearch}
                />

                {/* Why This Matters (Institutional Context) */}
                <WhyThisMatters />

                {/* Featured Verified Reports Grid */}
                <section className="space-y-6 pt-4">
                  <div className="flex items-center justify-between border-b border-stone-200 dark:border-stone-800 pb-3">
                    <div>
                      <h2 className="font-serif text-2xl font-semibold text-stone-900 dark:text-stone-100">
                        Featured verified reports
                      </h2>
                      <p className="text-xs text-stone-500 dark:text-stone-400 mt-0.5">
                        Selected product reports based on declared label data and reviewed scoring logic.
                      </p>
                    </div>

                    <button
                      onClick={() => setCurrentTab('products')}
                      className="text-xs font-medium text-teal-800 dark:text-teal-400 hover:underline flex items-center gap-1"
                    >
                      <span>View full database ({catalogProducts.length})</span>
                      <ArrowRight className="w-3.5 h-3.5" />
                    </button>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                    {featuredVerifiedProducts.map((product) => (
                      <div
                        key={product.productId}
                        onClick={() => handleSelectProduct(product)}
                        className="editorial-card p-5 cursor-pointer group flex flex-col justify-between"
                      >
                        <div className="space-y-3">
                          <div className="aspect-video rounded bg-stone-100 dark:bg-stone-800 overflow-hidden relative">
                            <img
                              src={product.imageUrl}
                              alt={product.productName}
                              className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                              loading="lazy"
                            />
                          </div>

                          <div>
                            <span className="text-[11px] font-semibold uppercase tracking-wider text-teal-800 dark:text-teal-400">
                              {product.brand}
                            </span>
                            <h3
                              className="font-serif text-lg font-semibold text-stone-900 dark:text-stone-100 line-clamp-2 group-hover:text-teal-800 dark:group-hover:text-teal-400 transition-colors"
                              title={product.productName}
                            >
                              {product.productName}
                            </h3>
                            <p className="text-xs text-stone-600 dark:text-stone-400 mt-1 line-clamp-2 leading-relaxed">
                              {product.executiveSummary.verdictTitle}
                            </p>
                          </div>
                        </div>

                        <div className="pt-3 mt-3 border-t border-stone-200 dark:border-stone-800 flex items-center justify-between text-xs">
                          {renderScoreBadge(product)}
                          <span className="text-teal-800 dark:text-teal-400 font-medium group-hover:underline">
                            Read report &rarr;
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>
                </section>

                {/* How Scoring Works (Methodology Snapshot) */}
                <MethodologySnapshot onGoToMethodology={() => setCurrentTab('methodology')} />
              </div>
            )}

            {/* 2. FULL PRODUCTS CATALOG TAB */}
            {currentTab === 'products' && (
              <div className="space-y-6 pt-4">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-stone-200 dark:border-stone-800 pb-4">
                  <div>
                    {globalSearchQuery ? (
                      <>
                        <h1 className="font-serif text-2xl sm:text-3xl font-semibold text-stone-900 dark:text-stone-100">
                          Results for "{globalSearchQuery}"
                        </h1>
                        <p className="text-xs text-stone-500 dark:text-stone-400 mt-1 flex items-center gap-1.5">
                          <Search className="w-3.5 h-3.5 text-teal-700" />
                          <span>{filteredCatalog.length} products found</span>
                          <button
                            onClick={() => setGlobalSearchQuery('')}
                            className="ml-2 text-teal-800 dark:text-teal-400 hover:underline"
                          >
                            Clear search
                          </button>
                        </p>
                      </>
                    ) : (
                      <>
                        <h1 className="font-serif text-2xl sm:text-3xl font-semibold text-stone-900 dark:text-stone-100">
                          Packaged Food Database
                        </h1>
                        <p className="text-xs text-stone-500 dark:text-stone-400 mt-1 flex items-center gap-1.5 font-mono">
                          <Database className="w-3.5 h-3.5 text-teal-700" />
                          <span>{catalogProducts.length} Products Synchronized • Verified Provenance</span>
                        </p>
                      </>
                    )}
                  </div>

                  {/* Category Filter Chips — no dead funnel icon */}
                  <div className="flex items-center gap-2 overflow-x-auto">
                    {CATEGORY_CHIPS.map((cat) => (
                      <button
                        key={cat}
                        onClick={() => {
                          setFilterCategory(cat);
                          setGlobalSearchQuery('');
                        }}
                        className={`px-3 py-1 rounded-md text-xs font-medium transition-colors whitespace-nowrap ${
                          filterCategory === cat && !globalSearchQuery
                            ? 'bg-teal-800 text-white'
                            : 'bg-stone-100 dark:bg-stone-800 text-stone-600 dark:text-stone-300 hover:bg-stone-200'
                        }`}
                      >
                        {cat}
                      </button>
                    ))}
                  </div>
                </div>

                {/* Product Cards Grid */}
                {paginatedCatalog.length > 0 ? (
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                    {paginatedCatalog.map((product) => (
                      <div
                        key={product.productId}
                        onClick={() => handleSelectProduct(product)}
                        className="editorial-card p-5 cursor-pointer group flex flex-col justify-between"
                      >
                        <div className="space-y-3">
                          <div className="aspect-video rounded bg-stone-100 dark:bg-stone-800 overflow-hidden relative">
                            <img
                              src={product.imageUrl}
                              alt={product.productName}
                              className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                              loading="lazy"
                            />
                          </div>

                          <div>
                            <span className="text-[11px] font-semibold uppercase tracking-wider text-teal-800 dark:text-teal-400">
                              {product.brand}
                            </span>
                            <h3
                              className="font-serif text-base font-semibold text-stone-900 dark:text-stone-100 line-clamp-2 group-hover:text-teal-800 dark:group-hover:text-teal-400 transition-colors"
                              title={product.productName}
                            >
                              {product.productName}
                            </h3>
                            <p className="text-xs text-stone-600 dark:text-stone-400 mt-1 line-clamp-2 leading-relaxed">
                              {product.executiveSummary.verdictTitle}
                            </p>
                          </div>
                        </div>

                        <div className="pt-3 mt-3 border-t border-stone-200 dark:border-stone-800 flex items-center justify-between text-xs">
                          {renderScoreBadge(product)}
                          <span className="text-teal-800 dark:text-teal-400 font-medium group-hover:underline">
                            View details &rarr;
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="text-center py-16 space-y-3">
                    <Search className="w-8 h-8 text-stone-300 dark:text-stone-600 mx-auto" />
                    <p className="text-stone-500 dark:text-stone-400 text-sm">
                      No products found{globalSearchQuery ? ` for "${globalSearchQuery}"` : ' in this category'}.
                    </p>
                    <button
                      onClick={() => { setGlobalSearchQuery(''); setFilterCategory('ALL'); }}
                      className="text-xs text-teal-800 dark:text-teal-400 hover:underline"
                    >
                      Show all products
                    </button>
                  </div>
                )}

                {/* Pagination Controls */}
                {totalPages > 1 && (
                  <div className="flex items-center justify-center gap-4 pt-4 pb-2">
                    <button
                      onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
                      disabled={currentPage === 1}
                      className="flex items-center gap-1 px-3 py-1.5 rounded-md text-xs font-medium bg-stone-100 dark:bg-stone-800 text-stone-700 dark:text-stone-300 hover:bg-stone-200 dark:hover:bg-stone-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
                    >
                      <ChevronLeft className="w-3.5 h-3.5" />
                      Previous
                    </button>
                    <span className="text-xs text-stone-500 dark:text-stone-400 font-mono">
                      Page {currentPage} of {totalPages}
                    </span>
                    <button
                      onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
                      disabled={currentPage === totalPages}
                      className="flex items-center gap-1 px-3 py-1.5 rounded-md text-xs font-medium bg-stone-100 dark:bg-stone-800 text-stone-700 dark:text-stone-300 hover:bg-stone-200 dark:hover:bg-stone-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
                    >
                      Next
                      <ChevronRight className="w-3.5 h-3.5" />
                    </button>
                  </div>
                )}
              </div>
            )}

            {/* 3. METHODOLOGY TAB */}
            {currentTab === 'methodology' && (
              <Suspense fallback={<div className="p-12 text-center text-stone-500 font-serif">Loading Regulatory Matrix...</div>}>
                <GlobalRegulatoryMatrix />
              </Suspense>
            )}

            {/* 4. COMPARE TAB */}
            {currentTab === 'compare' && (
              <Suspense fallback={<div className="p-12 text-center text-stone-500 font-serif">Loading Comparison...</div>}>
                <ProductComparison products={catalogProducts} onSelectProduct={handleSelectProduct} />
              </Suspense>
            )}

            {/* 5. ABOUT TAB */}
            {currentTab === 'about' && (
              <AboutView />
            )}

            {/* 6. GRIEVANCE TAB */}
            {currentTab === 'grievance' && (
              <GrievanceView />
            )}

            {/* 7. TERMS TAB */}
            {currentTab === 'terms' && (
              <TermsView />
            )}
          </>
        )}
      </main>

      {/* Barcode Scanner Modal */}
      {isScanOpen && (
        <Suspense fallback={null}>
          <ScanScannerModal
            isOpen={isScanOpen}
            onClose={() => setIsScanOpen(false)}
            onSelectProduct={handleSelectProduct}
          />
        </Suspense>
      )}

      {/* Footer */}
      <Footer
        onOpenGrievance={() => {
          setCurrentTab('grievance');
          setSelectedProduct(null);
          pushHistoryState('grievance', null);
          window.scrollTo({ top: 0, behavior: 'smooth' });
        }}
        onOpenManifesto={() => {
          setCurrentTab('about');
          setSelectedProduct(null);
          pushHistoryState('about', null);
          window.scrollTo({ top: 0, behavior: 'smooth' });
        }}
      />
    </div>
  );
}
