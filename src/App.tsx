import React, { useState, useEffect, useMemo, useCallback, Suspense, lazy } from 'react';
import { Header } from './components/Header';
import { HeroSection } from './components/HeroSection';
import { WhyThisMatters } from './components/WhyThisMatters';
import { MethodologySnapshot } from './components/MethodologySnapshot';
import { AboutView } from './components/AboutView';
import { TransparencyReportView } from './components/TransparencyReportView';
import { Footer } from './components/Footer';
import { PRESEEDED_PRODUCTS } from './data/productsDatabase';
import { TransparencyReport } from './types';
import { Filter, Grid, ShieldAlert, CheckCircle2, Database, Search, ArrowRight } from 'lucide-react';
import { fetchLiveCatalog } from './services/supabaseService';
import { fetchRawIngredientsTaxonomyAsync } from './services/decoupledAdditiveService';

// Lazy-loaded components for route code-splitting
const ScanScannerModal = lazy(() => import('./components/ScanScannerModal').then(m => ({ default: m.ScanScannerModal })));
const GlobalRegulatoryMatrix = lazy(() => import('./components/GlobalRegulatoryMatrix').then(m => ({ default: m.GlobalRegulatoryMatrix })));
const ProductComparison = lazy(() => import('./components/ProductComparison').then(m => ({ default: m.ProductComparison })));

export function App() {
  const [currentTab, setCurrentTab] = useState<'home' | 'products' | 'methodology' | 'compare' | 'about'>('home');
  const [selectedProduct, setSelectedProduct] = useState<TransparencyReport | null>(null);
  const [darkMode, setDarkMode] = useState<boolean>(false);
  const [isScanOpen, setIsScanOpen] = useState<boolean>(false);
  const [filterCategory, setFilterCategory] = useState<string>('ALL');
  const [catalogProducts, setCatalogProducts] = useState<TransparencyReport[]>(PRESEEDED_PRODUCTS);

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
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, []);

  const handleBackToCatalog = useCallback(() => {
    setSelectedProduct(null);
  }, []);

  // Filtered list for full /products catalog tab
  const filteredCatalog = useMemo(() => {
    return catalogProducts.filter((p) => {
      if (filterCategory === 'ALL') return true;
      if (filterCategory === 'NOODLES') return p.category.toLowerCase().includes('noodle');
      if (filterCategory === 'BEVERAGES') return p.category.toLowerCase().includes('drink') || p.category.toLowerCase().includes('beverage') || p.category.toLowerCase().includes('soft') || p.category.toLowerCase().includes('cola');
      if (filterCategory === 'SNACKS') return p.category.toLowerCase().includes('snack') || p.category.toLowerCase().includes('chip');
      return true;
    });
  }, [catalogProducts, filterCategory]);

  // Featured verified products for homepage (verified published only, max 6)
  const featuredVerifiedProducts = useMemo(() => {
    return catalogProducts
      .filter((p) => (!p.pageState || p.pageState === 'verified_published') && !p.isScoreWithheld)
      .slice(0, 6);
  }, [catalogProducts]);

  return (
    <div className="min-h-screen flex flex-col bg-[#fcfbf9] dark:bg-[#0e1117] text-[#1c2128] dark:text-[#e6edf3] transition-colors duration-200">
      
      {/* Navigation Header */}
      <Header
        currentTab={currentTab}
        setCurrentTab={(tab) => {
          setCurrentTab(tab);
          setSelectedProduct(null);
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
                  onGoToProducts={() => setCurrentTab('products')}
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
                    {featuredVerifiedProducts.map((product) => {
                      const issues = product.scoreBreakdown ? product.scoreBreakdown.filter((b) => b.type === 'DEDUCTION') : [];
                      return (
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
                              />
                            </div>

                            <div>
                              <span className="text-[11px] font-semibold uppercase tracking-wider text-teal-800 dark:text-teal-400">
                                {product.brand}
                              </span>
                              <h3 className="font-serif text-lg font-semibold text-stone-900 dark:text-stone-100 line-clamp-1 group-hover:text-teal-800 dark:group-hover:text-teal-400 transition-colors">
                                {product.productName}
                              </h3>
                              <p className="text-xs text-stone-600 dark:text-stone-400 mt-1 line-clamp-2 leading-relaxed">
                                {product.executiveSummary.verdictTitle}
                              </p>
                            </div>
                          </div>

                          <div className="pt-3 mt-3 border-t border-stone-200 dark:border-stone-800 flex items-center justify-between text-xs">
                            <span className="text-stone-500">
                              Score: <strong className="text-stone-900 dark:text-stone-100 font-semibold">{product.deterministicScore}/100</strong>
                            </span>
                            <span className="text-teal-800 dark:text-teal-400 font-medium group-hover:underline">
                              Read report &rarr;
                            </span>
                          </div>
                        </div>
                      );
                    })}
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
                    <h1 className="font-serif text-2xl sm:text-3xl font-semibold text-stone-900 dark:text-stone-100">
                      Packaged Food Database
                    </h1>
                    <p className="text-xs text-stone-500 dark:text-stone-400 mt-1 flex items-center gap-1.5 font-mono">
                      <Database className="w-3.5 h-3.5 text-teal-700" />
                      <span>19,813 Products Synchronized • Verified Provenance</span>
                    </p>
                  </div>

                  {/* Filter Pills */}
                  <div className="flex items-center gap-2 overflow-x-auto">
                    <Filter className="w-3.5 h-3.5 text-stone-400 shrink-0" />
                    {['ALL', 'NOODLES', 'BEVERAGES', 'SNACKS'].map((cat) => (
                      <button
                        key={cat}
                        onClick={() => setFilterCategory(cat)}
                        className={`px-3 py-1 rounded-md text-xs font-medium transition-colors ${
                          filterCategory === cat
                            ? 'bg-teal-800 text-white'
                            : 'bg-stone-100 dark:bg-stone-800 text-stone-600 dark:text-stone-300 hover:bg-stone-200'
                        }`}
                      >
                        {cat}
                      </button>
                    ))}
                  </div>
                </div>

                {/* Full Database Cards */}
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                  {filteredCatalog.map((product) => {
                    const issues = product.scoreBreakdown ? product.scoreBreakdown.filter((b) => b.type === 'DEDUCTION') : [];
                    return (
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
                            />
                          </div>

                          <div>
                            <span className="text-[11px] font-semibold uppercase tracking-wider text-teal-800 dark:text-teal-400">
                              {product.brand}
                            </span>
                            <h3 className="font-serif text-base font-semibold text-stone-900 dark:text-stone-100 line-clamp-1 group-hover:text-teal-800 dark:group-hover:text-teal-400 transition-colors">
                              {product.productName}
                            </h3>
                            <p className="text-xs text-stone-600 dark:text-stone-400 mt-1 line-clamp-2 leading-relaxed">
                              {product.executiveSummary.verdictTitle}
                            </p>
                          </div>
                        </div>

                        <div className="pt-3 mt-3 border-t border-stone-200 dark:border-stone-800 flex items-center justify-between text-xs">
                          <span className="text-stone-500">
                            Score: <strong className="text-stone-900 dark:text-stone-100 font-semibold">{product.deterministicScore}/100</strong>
                          </span>
                          <span className="text-teal-800 dark:text-teal-400 font-medium group-hover:underline">
                            View details &rarr;
                          </span>
                        </div>
                      </div>
                    );
                  })}
                </div>
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
      <Footer />
    </div>
  );
}
