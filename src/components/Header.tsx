import React, { useState } from 'react';
import { Search, Sun, Moon, Menu, X, Scan } from 'lucide-react';

interface HeaderProps {
  currentTab: 'home' | 'products' | 'methodology' | 'compare' | 'about' | 'grievance' | 'terms';
  setCurrentTab: (tab: any) => void;
  darkMode: boolean;
  setDarkMode: (val: boolean) => void;
  onOpenScan: () => void;
  onSearchClick: () => void;
}

const NAV_ITEMS: { label: string; tab: 'home' | 'products' | 'methodology' | 'compare' | 'about' }[] = [
  { label: 'Products', tab: 'products' },
  { label: 'Methodology', tab: 'methodology' },
  { label: 'Compare', tab: 'compare' },
  { label: 'About', tab: 'about' },
];

export const Header: React.FC<HeaderProps> = ({
  currentTab,
  setCurrentTab,
  darkMode,
  setDarkMode,
  onOpenScan,
  onSearchClick,
}) => {
  const [isMobileOpen, setIsMobileOpen] = useState(false);

  const handleNav = (tab: typeof currentTab) => {
    setCurrentTab(tab);
    setIsMobileOpen(false);
  };

  return (
    <header className="sticky top-0 z-40 w-full bg-[#fcfbf9]/95 dark:bg-[#0e1117]/95 backdrop-blur-sm border-b border-stone-200 dark:border-stone-800 transition-colors">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 h-14 flex items-center justify-between">
        
        {/* Brand */}
        <div 
          onClick={() => handleNav('home')}
          className="flex items-center gap-2 cursor-pointer group"
          role="button"
          tabIndex={0}
          onKeyDown={(e) => e.key === 'Enter' && handleNav('home')}
          aria-label="FoodFactsIndia Home"
        >
          <span className="font-serif font-bold text-lg tracking-tight text-stone-900 dark:text-stone-100 group-hover:text-teal-700 dark:group-hover:text-teal-400 transition-colors">
            FoodFactsIndia
          </span>
        </div>

        {/* Desktop Nav */}
        <nav className="hidden md:flex items-center gap-1">
          {NAV_ITEMS.map(({ label, tab }) => (
            <button
              key={tab}
              onClick={() => handleNav(tab)}
              className={`px-3 py-1.5 rounded-md text-sm font-medium transition-colors ${
                currentTab === tab
                  ? 'bg-teal-50 dark:bg-teal-950/30 text-teal-800 dark:text-teal-300'
                  : 'text-stone-600 dark:text-stone-400 hover:text-stone-900 dark:hover:text-stone-200 hover:bg-stone-100 dark:hover:bg-stone-800'
              }`}
            >
              {label}
            </button>
          ))}
          <button
            onClick={() => { onOpenScan(); setIsMobileOpen(false); }}
            className="px-3 py-1.5 rounded-md text-sm font-medium text-stone-600 dark:text-stone-400 hover:text-stone-900 dark:hover:text-stone-200 hover:bg-stone-100 dark:hover:bg-stone-800 transition-colors flex items-center gap-1.5"
          >
            <Scan className="w-3.5 h-3.5" />
            Scan Label
          </button>
        </nav>

        {/* Right Utilities */}
        <div className="flex items-center gap-2">
          <button
            onClick={onSearchClick}
            className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-md text-xs font-medium text-stone-600 dark:text-stone-300 bg-stone-100 dark:bg-stone-800/80 hover:bg-stone-200 dark:hover:bg-stone-700 transition-colors"
          >
            <Search className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">Search</span>
          </button>

          <button
            onClick={() => setDarkMode(!darkMode)}
            className="p-1.5 rounded-md text-stone-500 dark:text-stone-400 hover:text-stone-900 dark:hover:text-stone-100 hover:bg-stone-100 dark:hover:bg-stone-800 transition-colors"
            title="Toggle theme"
            aria-label="Toggle theme"
          >
            {darkMode ? <Sun className="w-4 h-4 text-amber-400" /> : <Moon className="w-4 h-4" />}
          </button>

          {/* Mobile hamburger */}
          <button
            onClick={() => setIsMobileOpen(!isMobileOpen)}
            className="md:hidden p-1.5 rounded-md text-stone-600 dark:text-stone-400 hover:bg-stone-100 dark:hover:bg-stone-800 transition-colors"
            aria-label="Toggle menu"
          >
            {isMobileOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>

      </div>

      {/* Mobile Drawer */}
      {isMobileOpen && (
        <div className="md:hidden border-t border-stone-200 dark:border-stone-800 bg-[#fcfbf9] dark:bg-[#0e1117] px-4 pb-4 pt-2 space-y-1">
          {NAV_ITEMS.map(({ label, tab }) => (
            <button
              key={tab}
              onClick={() => handleNav(tab)}
              className={`block w-full text-left px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                currentTab === tab
                  ? 'bg-teal-50 dark:bg-teal-950/30 text-teal-800 dark:text-teal-300'
                  : 'text-stone-700 dark:text-stone-300 hover:bg-stone-100 dark:hover:bg-stone-800'
              }`}
            >
              {label}
            </button>
          ))}
          <button
            onClick={() => { onOpenScan(); setIsMobileOpen(false); }}
            className="block w-full text-left px-3 py-2 rounded-md text-sm font-medium text-stone-700 dark:text-stone-300 hover:bg-stone-100 dark:hover:bg-stone-800 transition-colors flex items-center gap-2"
          >
            <Scan className="w-4 h-4" />
            Scan Label
          </button>
        </div>
      )}
    </header>
  );
};
