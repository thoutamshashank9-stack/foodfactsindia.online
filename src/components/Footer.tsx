import React from 'react';
import { ShieldCheck, HeartHandshake, Info } from 'lucide-react';

export const Footer: React.FC = () => {
  return (
    <footer className="mt-20 border-t border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 text-slate-600 dark:text-slate-400 py-12 transition-colors">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-8">
        
        {/* Principles Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 pb-8 border-b border-slate-100 dark:border-slate-800 text-xs">
          <div className="flex gap-3">
            <ShieldCheck className="w-5 h-5 text-blue-600 dark:text-blue-400 shrink-0" />
            <div>
              <h4 className="font-bold text-slate-900 dark:text-white text-sm">Evidence First</h4>
              <p className="mt-1 text-slate-500 dark:text-slate-400 leading-relaxed">
                Every rating is grounded strictly in published FSSAI, EFSA, and US FDA scientific literature and toxicological data.
              </p>
            </div>
          </div>

          <div className="flex gap-3">
            <HeartHandshake className="w-5 h-5 text-emerald-600 dark:text-emerald-400 shrink-0" />
            <div>
              <h4 className="font-bold text-slate-900 dark:text-white text-sm">Strict Neutrality</h4>
              <p className="mt-1 text-slate-500 dark:text-slate-400 leading-relaxed">
                FoodFactsIndia AI does not attack food brands. We objectively decode ingredient lists and regulatory statuses using transparent math.
              </p>
            </div>
          </div>

          <div className="flex gap-3">
            <Info className="w-5 h-5 text-amber-500 shrink-0" />
            <div>
              <h4 className="font-bold text-slate-900 dark:text-white text-sm">Medical Disclaimer</h4>
              <p className="mt-1 text-slate-500 dark:text-slate-400 leading-relaxed">
                FoodFactsIndia AI is an educational transparency platform and does not provide medical diagnosis, treatment, or clinical advice.
              </p>
            </div>
          </div>
        </div>

        {/* Footer Bottom */}
        <div className="flex flex-col sm:flex-row items-center justify-between text-xs gap-4 text-slate-500 dark:text-slate-400">
          <div className="flex items-center gap-2">
            <span className="font-bold text-slate-900 dark:text-white">FoodFactsIndia AI</span>
            <span>© {new Date().getFullYear()} FoodFactsIndia Intelligence Platform. All rights reserved.</span>
          </div>
          <div className="flex items-center gap-4">
            <span className="hover:text-slate-900 dark:hover:text-white cursor-pointer">Regulatory Sources</span>
            <span className="hover:text-slate-900 dark:hover:text-white cursor-pointer">Scoring Methodology</span>
            <span className="hover:text-slate-900 dark:hover:text-white cursor-pointer">Privacy & Terms</span>
          </div>
        </div>

      </div>
    </footer>
  );
};
