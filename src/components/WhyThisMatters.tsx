import React from 'react';
import { BookOpen, ShieldCheck, Scale } from 'lucide-react';

export const WhyThisMatters: React.FC = () => {
  return (
    <section className="py-10 border-b border-stone-200 dark:border-stone-800/80">
      <div className="max-w-4xl mx-auto px-4">
        <div className="text-center space-y-2 mb-8">
          <h2 className="font-serif text-2xl sm:text-3xl font-semibold text-stone-900 dark:text-stone-100">
            Why Food Label Transparency Matters
          </h2>
          <p className="text-sm text-stone-600 dark:text-stone-400">
            Current front-of-pack labels often obscure nutritional quality, synthetic additives, and processing signals.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="editorial-card p-5 space-y-2">
            <BookOpen className="w-5 h-5 text-teal-700 dark:text-teal-400" />
            <h3 className="font-semibold text-base text-stone-900 dark:text-stone-100">Declared Ingredients</h3>
            <p className="text-xs text-stone-600 dark:text-stone-400 leading-relaxed">
              Decoding hidden sugars, ultra-processed ultra-refined starches, and industrial emulsifiers beyond commercial marketing claims.
            </p>
          </div>

          <div className="editorial-card p-5 space-y-2">
            <ShieldCheck className="w-5 h-5 text-teal-700 dark:text-teal-400" />
            <h3 className="font-semibold text-base text-stone-900 dark:text-stone-100">Regulatory Consistency</h3>
            <p className="text-xs text-stone-600 dark:text-stone-400 leading-relaxed">
              Cross-referencing food additive permissions across FSSAI, US FDA, and EFSA standards to highlight international discrepancies.
            </p>
          </div>

          <div className="editorial-card p-5 space-y-2">
            <Scale className="w-5 h-5 text-teal-700 dark:text-teal-400" />
            <h3 className="font-semibold text-base text-stone-900 dark:text-stone-100">Objective Research</h3>
            <p className="text-xs text-stone-600 dark:text-stone-400 leading-relaxed">
              Empowering consumers and regulatory discussions with independent, evidence-led reporting without brand bias.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
};
