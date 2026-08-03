import React, { useState, useRef, useEffect } from 'react';
import { ShieldCheck, Scan, Search, Globe, GitCompare, Sun, Moon, Sparkles, ChevronDown, MoreHorizontal } from 'lucide-react';

interface HeaderProps {
  currentTab: 'home' | 'analyzer' | 'regulatory' | 'compare';
  setCurrentTab: (tab: 'home' | 'analyzer' | 'regulatory' | 'compare') => void;
  darkMode: boolean;
  setDarkMode: (val: boolean) => void;
  onOpenScan: () => void;
  onSearchClick: () => void;
}

export const Header: React.FC<HeaderProps> = ({
  currentTab,
  setCurrentTab,
  darkMode,
  setDarkMode,
  onOpenScan,
}) => {
  const [isMoreMenuOpen, setIsMoreMenuOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsMoreMenuOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const isMoreTabActive = currentTab === 'analyzer' || currentTab === 'regulatory';

  return (
    <header className="sticky top-0 z-40 w-full glass-card border-b transition-colors bg-white/80 dark:bg-slate-900/80 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        
        {/* Brand Logo */}
        <div 
          onClick={() => setCurrentTab('home')}
          className="flex items-center gap-3 cursor-pointer group focus:outline-none focus:ring-2 focus:ring-blue-500 rounded-xl p-1"
          role="button"
          tabIndex={0}
          onKeyDown={(e) => e.key === 'Enter' && setCurrentTab('home')}
          aria-label="FoodLens AI Home"
        >
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-600 to-emerald-500 flex items-center justify-center shadow-lg shadow-blue-500/20 group-hover:scale-105 transition-transform">
            <ShieldCheck className="w-6 h-6 text-white" />
          </div>
          <div>
            <div className="flex items-center gap-1.5">
              <span className="font-extrabold text-xl tracking-tight bg-gradient-to-r from-blue-600 via-emerald-600 to-blue-700 bg-clip-text text-transparent">
                FoodLens
              </span>
              <span className="px-1.5 py-0.5 text-[10px] font-bold uppercase tracking-wider bg-blue-100 dark:bg-blue-900/50 text-blue-700 dark:text-blue-300 rounded">
                AI
              </span>
            </div>
            <p className="text-[11px] text-slate-500 dark:text-slate-400 font-medium hidden sm:block">
              Evidence-Based Food Transparency
            </p>
          </div>
        </div>

        {/* Simplified Navigation (Max 2 secondary + 1 More Tools menu) */}
        <nav className="hidden md:flex items-center gap-1 bg-slate-100 dark:bg-slate-800/80 p-1.5 rounded-xl border border-slate-200 dark:border-slate-700/60">
          <button
            onClick={() => setCurrentTab('home')}
            className={`min-h-[44px] flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-semibold transition-all focus:outline-none focus:ring-2 focus:ring-blue-500 ${
              currentTab === 'home'
                ? 'bg-white dark:bg-slate-900 text-blue-600 dark:text-blue-400 shadow-sm'
                : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
            }`}
          >
            <Search className="w-4 h-4" />
            Products
          </button>

          <button
            onClick={() => setCurrentTab('compare')}
            className={`min-h-[44px] flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-semibold transition-all focus:outline-none focus:ring-2 focus:ring-blue-500 ${
              currentTab === 'compare'
                ? 'bg-white dark:bg-slate-900 text-blue-600 dark:text-blue-400 shadow-sm'
                : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
            }`}
          >
            <GitCompare className="w-4 h-4" />
            Compare
          </button>

          {/* More Tools Dropdown Menu */}
          <div className="relative" ref={dropdownRef}>
            <button
              onClick={() => setIsMoreMenuOpen(!isMoreMenuOpen)}
              className={`min-h-[44px] flex items-center gap-1.5 px-3.5 py-2 rounded-lg text-sm font-semibold transition-all focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                isMoreTabActive
                  ? 'bg-white dark:bg-slate-900 text-blue-600 dark:text-blue-400 shadow-sm'
                  : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
              }`}
              aria-expanded={isMoreMenuOpen}
              aria-haspopup="true"
            >
              <MoreHorizontal className="w-4 h-4" />
              <span>More Tools</span>
              <ChevronDown className={`w-3.5 h-3.5 transition-transform ${isMoreMenuOpen ? 'rotate-180' : ''}`} />
            </button>

            {isMoreMenuOpen && (
              <div className="absolute right-0 mt-2 w-56 bg-white dark:bg-slate-900 rounded-2xl shadow-xl border border-slate-200 dark:border-slate-800 p-1.5 z-50 animate-in fade-in zoom-in-95 duration-150">
                <button
                  onClick={() => {
                    setCurrentTab('analyzer');
                    setIsMoreMenuOpen(false);
                  }}
                  className={`w-full flex items-center gap-2.5 px-3.5 py-2.5 rounded-xl text-xs font-semibold text-left transition-colors min-h-[44px] ${
                    currentTab === 'analyzer'
                      ? 'bg-blue-50 dark:bg-blue-950/60 text-blue-600 dark:text-blue-400 font-bold'
                      : 'text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800'
                  }`}
                >
                  <Sparkles className="w-4 h-4 text-emerald-500 shrink-0" />
                  <div>
                    <div className="font-bold">Custom Label AI</div>
                    <div className="text-[10px] text-slate-500 dark:text-slate-400 font-normal">Analyze non-standard labels</div>
                  </div>
                </button>

                <button
                  onClick={() => {
                    setCurrentTab('regulatory');
                    setIsMoreMenuOpen(false);
                  }}
                  className={`w-full flex items-center gap-2.5 px-3.5 py-2.5 rounded-xl text-xs font-semibold text-left transition-colors min-h-[44px] ${
                    currentTab === 'regulatory'
                      ? 'bg-blue-50 dark:bg-blue-950/60 text-blue-600 dark:text-blue-400 font-bold'
                      : 'text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800'
                  }`}
                >
                  <Globe className="w-4 h-4 text-blue-500 shrink-0" />
                  <div>
                    <div className="font-bold">Global Bans DB</div>
                    <div className="text-[10px] text-slate-500 dark:text-slate-400 font-normal">Cross-border additive regulations</div>
                  </div>
                </button>
              </div>
            )}
          </div>
        </nav>

        {/* Right Actions: Single Primary CTA & Icon-Only Theme Toggle (WCAG 44x44 target size) */}
        <div className="flex items-center gap-2 sm:gap-3">
          <button
            onClick={onOpenScan}
            className="min-h-[44px] min-w-[44px] flex items-center gap-2 px-4 py-2.5 rounded-xl bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-500 hover:to-blue-600 text-white font-bold text-xs sm:text-sm shadow-md shadow-blue-500/20 hover:shadow-lg transition-all active:scale-95 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <Scan className="w-4 h-4 shrink-0" />
            <span className="hidden sm:inline">Scan Product</span>
            <span className="sm:hidden">Scan</span>
          </button>

          <button
            onClick={() => setDarkMode(!darkMode)}
            className="min-h-[44px] min-w-[44px] flex items-center justify-center p-2.5 rounded-xl bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500"
            title="Toggle color theme"
            aria-label="Toggle color theme"
          >
            {darkMode ? <Sun className="w-5 h-5 text-amber-400" /> : <Moon className="w-5 h-5 text-slate-600" />}
          </button>
        </div>

      </div>
    </header>
  );
};

