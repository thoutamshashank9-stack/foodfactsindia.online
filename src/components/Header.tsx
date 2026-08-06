import React from 'react';
import { Search, Sun, Moon } from 'lucide-react';

interface HeaderProps {
  currentTab: 'home' | 'products' | 'methodology' | 'compare' | 'about';
  setCurrentTab: (tab: 'home' | 'products' | 'methodology' | 'compare' | 'about') => void;
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
  onSearchClick,
}) => {
  return (
    <header className="sticky top-0 z-40 w-full bg-[#fcfbf9]/95 dark:bg-[#0e1117]/95 backdrop-blur-sm border-b border-stone-200 dark:border-stone-800 transition-colors">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        
        {/* Brand Logo & Tagline */}
        <div 
          onClick={() => setCurrentTab('home')}
          className="flex items-center gap-3 cursor-pointer group focus:outline-none rounded-lg py-1"
          role="button"
          tabIndex={0}
          onKeyDown={(e) => e.key === 'Enter' && setCurrentTab('home')}
          aria-label="FoodFactsIndia Home"
        >
          <div>
            <div className="flex items-center gap-2">
              <span className="font-serif font-bold text-xl tracking-tight text-stone-900 dark:text-stone-100 group-hover:text-teal-700 dark:group-hover:text-teal-400 transition-colors">
                FoodFactsIndia
              </span>
            </div>
            <p className="text-xs text-stone-500 dark:text-stone-400 font-normal hidden sm:block -mt-0.5">
              Food label transparency
            </p>
          </div>
        </div>

        {/* Calm 5-Item Editorial Navigation */}
        <nav className="hidden md:flex items-center gap-6">
          <button
            onClick={() => setCurrentTab('products')}
            className={`text-sm font-medium transition-colors py-1.5 border-b-2 ${
              currentTab === 'products'
                ? 'border-teal-700 text-teal-800 dark:border-teal-400 dark:text-teal-300 font-semibold'
                : 'border-transparent text-stone-600 dark:text-stone-400 hover:text-stone-900 dark:hover:text-stone-200'
            }`}
          >
            Products
          </button>

          <button
            onClick={() => setCurrentTab('methodology')}
            className={`text-sm font-medium transition-colors py-1.5 border-b-2 ${
              currentTab === 'methodology'
                ? 'border-teal-700 text-teal-800 dark:border-teal-400 dark:text-teal-300 font-semibold'
                : 'border-transparent text-stone-600 dark:text-stone-400 hover:text-stone-900 dark:hover:text-stone-200'
            }`}
          >
            Methodology
          </button>

          <button
            onClick={() => setCurrentTab('compare')}
            className={`text-sm font-medium transition-colors py-1.5 border-b-2 ${
              currentTab === 'compare'
                ? 'border-teal-700 text-teal-800 dark:border-teal-400 dark:text-teal-300 font-semibold'
                : 'border-transparent text-stone-600 dark:text-stone-400 hover:text-stone-900 dark:hover:text-stone-200'
            }`}
          >
            Compare
          </button>

          <button
            onClick={() => setCurrentTab('about')}
            className={`text-sm font-medium transition-colors py-1.5 border-b-2 ${
              currentTab === 'about'
                ? 'border-teal-700 text-teal-800 dark:border-teal-400 dark:text-teal-300 font-semibold'
                : 'border-transparent text-stone-600 dark:text-stone-400 hover:text-stone-900 dark:hover:text-stone-200'
            }`}
          >
            About
          </button>
        </nav>

        {/* Right Utilities: Search Button & Theme Toggle */}
        <div className="flex items-center gap-3">
          <button
            onClick={onSearchClick}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-medium text-stone-600 dark:text-stone-300 bg-stone-100 dark:bg-stone-800/80 hover:bg-stone-200 dark:hover:bg-stone-700 transition-colors"
          >
            <Search className="w-3.5 h-3.5" />
            <span>Search</span>
          </button>

          <button
            onClick={() => setDarkMode(!darkMode)}
            className="p-1.5 rounded-md text-stone-500 dark:text-stone-400 hover:text-stone-900 dark:hover:text-stone-100 hover:bg-stone-100 dark:hover:bg-stone-800 transition-colors"
            title="Toggle theme"
            aria-label="Toggle theme"
          >
            {darkMode ? <Sun className="w-4 h-4 text-amber-400" /> : <Moon className="w-4 h-4" />}
          </button>
        </div>

      </div>
    </header>
  );
};
