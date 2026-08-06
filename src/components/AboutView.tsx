import React from 'react';
import { ShieldCheck, FileText, HeartHandshake } from 'lucide-react';

export const AboutView: React.FC = () => {
  return (
    <div className="max-w-3xl mx-auto py-10 px-4 space-y-8">
      <div className="space-y-3 text-center sm:text-left border-b border-stone-200 dark:border-stone-800 pb-6">
        <h1 className="font-serif text-3xl sm:text-4xl font-semibold text-stone-900 dark:text-stone-100">
          About FoodFactsIndia
        </h1>
        <p className="text-base text-stone-600 dark:text-stone-300 leading-relaxed">
          An independent, public-interest research initiative focused on packaged food label transparency and evidence-based nutritional awareness in India.
        </p>
      </div>

      <div className="space-y-6 text-sm text-stone-700 dark:text-stone-300 leading-relaxed">
        <div className="editorial-card p-6 space-y-3">
          <h2 className="font-serif text-xl font-semibold text-stone-900 dark:text-stone-100 flex items-center gap-2">
            <ShieldCheck className="w-5 h-5 text-teal-700 dark:text-teal-400" />
            Our Public Interest Mission
          </h2>
          <p>
            FoodFactsIndia is not built as a commercial app or consumer growth product. Our objective is strictly educational and research-driven: to bring clarity to front-of-pack food labels, ingredient lists, industrial additives, and regulatory standards.
          </p>
          <p>
            We aim to empower citizens, researchers, and public health advocates with objective data showing where current food labeling regulations and manufacturer disclosures under-inform the public.
          </p>
        </div>

        <div className="editorial-card p-6 space-y-3">
          <h2 className="font-serif text-xl font-semibold text-stone-900 dark:text-stone-100 flex items-center gap-2">
            <FileText className="w-5 h-5 text-teal-700 dark:text-teal-400" />
            Data Integrity & Verification
          </h2>
          <p>
            All products listed on our platform are derived strictly from physical product label disclosures and public regulatory gazettes (FSSAI, EU EFSA, US FDA).
          </p>
          <p>
            Synthetic dataset generations, estimated values, or unverified claims are strictly quarantined and never presented as published facts.
          </p>
        </div>

        <div className="editorial-card p-6 space-y-3">
          <h2 className="font-serif text-xl font-semibold text-stone-900 dark:text-stone-100 flex items-center gap-2">
            <HeartHandshake className="w-5 h-5 text-teal-700 dark:text-teal-400" />
            Independence & Neutrality
          </h2>
          <p>
            FoodFactsIndia accepts no corporate sponsorships or advertising from food manufacturers. Our scoring logic operates algorithmically based on declared ingredients and published toxicological literature.
          </p>
        </div>
      </div>
    </div>
  );
};
