import React, { useState, useEffect, useMemo, useCallback, Suspense, lazy } from 'react';
import { Header } from './components/Header';
import { HeroSection } from './components/HeroSection';
import { TransparencyReportView } from './components/TransparencyReportView';
import { Footer } from './components/Footer';
import { PRESEEDED_PRODUCTS } from './data/productsDatabase';
import { TransparencyReport } from './types';
import { ArrowLeft, Sparkles, Filter, Grid, ShieldAlert, CheckCircle2, Database } from 'lucide-react';
import { fetchLiveCatalog } from './services/supabaseService';
import { fetchRawIngredientsTaxonomyAsync } from './services/decoupledAdditiveService';

// Lazy-loaded components for route code-splitting
const ScanScannerModal = lazy(() => import('./components/ScanScannerModal').then(m => ({ default: m.ScanScannerModal })));
const CustomLabelAnalyzer = lazy(() => import('./components/CustomLabelAnalyzer').then(m => ({ default: m.CustomLabelAnalyzer })));
const GlobalRegulatoryMatrix = lazy(() => import('./components/GlobalRegulatoryMatrix').then(m => ({ default: m.GlobalRegulatoryMatrix })));
const ProductComparison = lazy(() => import('./components/ProductComparison').then(m => ({ default: m.ProductComparison })));

export function App() {
  const [currentTab, setCurrentTab] = useState<'home' | 'analyzer' | 'regulatory' | 'compare'>('home');
  const [selectedProduct, setSelectedProduct] = useState<TransparencyReport | null>(null);
  const [darkMode, setDarkMode] = useState<boolean>(false);
  const [isScanOpen, setIsScanOpen] = useState<boolean>(false);
  const [filterCategory, setFilterCategory] = useState<string>('ALL');
  const [catalogProducts, setCatalogProducts] = useState<TransparencyReport[]>(PRESEEDED_PRODUCTS);
  const [isLiveLoading, setIsLiveLoading] = useState<boolean>(true);

  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [darkMode]);

  // Load initial product catalog from Supabase Realtime Database
  useEffect(() => {
    fetchRawIngredientsTaxonomyAsync();

    async function loadCatalog() {
      try {
        setIsLiveLoading(true);
        const liveData = await fetchLiveCatalog();
        if (liveData && liveData.length > 0) {
          // Merge preseeded + live products without duplication
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
      } finally {
        setIsLiveLoading(false);
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

  const handleReportGenerated = useCallback((report: TransparencyReport) => {
    setSelectedProduct(report);
    setCurrentTab('home');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, []);

  const filteredCatalog = useMemo(() => {
    return catalogProducts.filter((p) => {
      if (filterCategory === 'ALL') return true;
      if (filterCategory === 'NOODLES') return p.category.toLowerCase().includes('noodle');
      if (filterCategory === 'BEVERAGES') return p.category.toLowerCase().includes('drink') || p.category.toLowerCase().includes('beverage') || p.category.toLowerCase().includes('soft') || p.category.toLowerCase().includes('cola');
      if (filterCategory === 'SNACKS') return p.category.toLowerCase().includes('snack') || p.category.toLowerCase().includes('chip');
      return true;
    });
  }, [catalogProducts, filterCategory]);

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100 transition-colors duration-200">
      
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
          setCurrentTab('home');
          setSelectedProduct(null);
        }}
      />

      {/* Main Body Canvas */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        
        {/* If a product report is active */}
        {selectedProduct ? (
          <TransparencyReportView 
            report={selectedProduct} 
            onBackToSearch={handleBackToCatalog} 
          />
        ) : (
          <>
            {/* TAB 1: HOME & EXPLORE */}
            {currentTab === 'home' && (
              <div className="space-y-12">
                <HeroSection
                  products={catalogProducts}
                  onSelectProduct={handleSelectProduct}
                  onOpenScan={() => setIsScanOpen(true)}
                  onGoToAnalyzer={() => setCurrentTab('analyzer')}
                />

                {/* Catalog Grid Section */}
                <div className="space-y-6">
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-200 dark:border-slate-800 pb-4">
                    <div>
                      <h2 className="text-xl font-extrabold text-slate-900 dark:text-white flex items-center gap-2">
                        <Grid className="w-5 h-5 text-blue-600 dark:text-blue-400" />
                        Packaged Food Database & Intelligence Catalog
                      </h2>
                      <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5 flex items-center gap-1.5">
                        <Database className="w-3.5 h-3.5 text-emerald-500" />
                        <span>Connected to Live Supabase Engine • 19,813 Products Synchronized</span>
                      </p>
                    </div>

                    {/* Filter Pills */}
                    <div className="flex items-center gap-2 overflow-x-auto pb-1 sm:pb-0">
                      <Filter className="w-4 h-4 text-slate-400 shrink-0" />
                      {['ALL', 'NOODLES', 'BEVERAGES', 'SNACKS'].map((cat) => (
                        <button
                          key={cat}
                          onClick={() => setFilterCategory(cat)}
                          className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all whitespace-nowrap ${
                            filterCategory === cat
                              ? 'bg-blue-600 text-white shadow-md shadow-blue-500/20'
                              : 'bg-white dark:bg-slate-900 text-slate-600 dark:text-slate-300 border border-slate-200 dark:border-slate-800 hover:bg-slate-100 dark:hover:bg-slate-800'
                          }`}
                        >
                          {cat}
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* Grid Cards */}
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                    {filteredCatalog.map((product) => {
                      const issues = product.scoreBreakdown ? product.scoreBreakdown.filter((b) => b.type === 'DEDUCTION') : [];
                      return (
                        <div
                          key={product.productId}
                          onClick={() => handleSelectProduct(product)}
                          className="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 p-5 shadow-lg hover:shadow-2xl transition-all cursor-pointer group hover:-translate-y-1 flex flex-col justify-between"
                        >
                          <div className="space-y-4">
                            <div className="relative aspect-video rounded-2xl overflow-hidden bg-slate-100 dark:bg-slate-800">
                              <img
                                src={product.imageUrl}
                                alt={product.productName}
                                className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                              />
                              <div className={`absolute top-3 right-3 px-2.5 py-1 rounded-xl text-xs font-extrabold shadow-lg backdrop-blur-md flex items-center gap-1.5 ${
                                issues.length > 0
                                  ? 'bg-rose-950/85 text-rose-200 border border-rose-800'
                                  : 'bg-emerald-950/85 text-emerald-200 border border-emerald-800'
                              }`}>
                                {issues.length > 0 ? (
                                  <>
                                    <ShieldAlert className="w-3.5 h-3.5 text-rose-400" />
                                    <span>{issues.length} Issues</span>
                                  </>
                                ) : (
                                  <>
                                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                                    <span>Clean Product</span>
                                  </>
                                )}
                              </div>
                            </div>

                            <div>
                              <span className="text-[11px] font-bold uppercase tracking-wider text-blue-600 dark:text-blue-400">
                                {product.brand}
                              </span>
                              <h3 className="font-extrabold text-base text-slate-900 dark:text-white line-clamp-1 group-hover:text-blue-600 transition-colors">
                                {product.productName}
                              </h3>
                              <p className="text-xs text-slate-500 dark:text-slate-400 mt-1 line-clamp-2">
                                {product.executiveSummary.verdictTitle}
                              </p>
                            </div>
                          </div>

                          <div className="pt-4 mt-4 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between text-xs font-semibold">
                            <span className="text-slate-500 dark:text-slate-400">
                              Score: <strong className="text-slate-900 dark:text-white font-extrabold">{product.deterministicScore}/100</strong>
                            </span>
                            <span className="text-blue-600 dark:text-blue-400 font-bold group-hover:underline">
                              View Report &rarr;
                            </span>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              </div>
            )}

            {/* TAB 2: CUSTOM OCR ANALYZER */}
            {currentTab === 'analyzer' && (
              <Suspense fallback={<div className="p-12 text-center text-slate-500 font-semibold">Loading Analyzer...</div>}>
                <CustomLabelAnalyzer onReportGenerated={handleReportGenerated} />
              </Suspense>
            )}

            {/* TAB 3: REGULATORY MATRIX */}
            {currentTab === 'regulatory' && (
              <Suspense fallback={<div className="p-12 text-center text-slate-500 font-semibold">Loading Matrix...</div>}>
                <GlobalRegulatoryMatrix />
              </Suspense>
            )}

            {/* TAB 4: PRODUCT COMPARISON */}
            {currentTab === 'compare' && (
              <Suspense fallback={<div className="p-12 text-center text-slate-500 font-semibold">Loading Comparison...</div>}>
                <ProductComparison products={catalogProducts} onSelectProduct={handleSelectProduct} />
              </Suspense>
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
