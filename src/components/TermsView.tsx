import React from 'react';
import { FileText, ShieldAlert, Scale, AlertTriangle } from 'lucide-react';

export const TermsView: React.FC = () => {
  return (
    <div className="max-w-3xl mx-auto py-10 px-4 space-y-8">
      <div className="space-y-3 text-center sm:text-left border-b border-stone-200 dark:border-stone-800 pb-6">
        <h1 className="font-serif text-3xl sm:text-4xl font-semibold text-stone-900 dark:text-stone-100">
          Terms of Service
        </h1>
        <p className="text-base text-stone-600 dark:text-stone-300 leading-relaxed">
          Legal terms governing the use of FoodFactsIndia.online — a zero-profit public interest research platform.
        </p>
      </div>

      <div className="space-y-6 text-sm text-stone-700 dark:text-stone-300 leading-relaxed">

        <div className="editorial-card p-6 space-y-3">
          <h2 className="font-serif text-xl font-semibold text-stone-900 dark:text-stone-100 flex items-center gap-2">
            <Scale className="w-5 h-5 text-teal-700 dark:text-teal-400" />
            Public Interest Purpose
          </h2>
          <p>
            FoodFactsIndia.online is an independent, citizen-led, non-commercial public health research initiative. We accept no money, run no advertisements, and sell no products. All data, analysis, and opinions published on this platform are provided exclusively for end-consumer education, academic research, and public interest advocacy.
          </p>
        </div>

        <div className="editorial-card p-6 space-y-3">
          <h2 className="font-serif text-xl font-semibold text-stone-900 dark:text-stone-100 flex items-center gap-2">
            <AlertTriangle className="w-5 h-5 text-amber-600 dark:text-amber-400" />
            No B2B Reliance
          </h2>
          <p>
            Data provided on this platform is for end-consumer educational purposes and public interest advocacy only. It must not be used as the sole basis for B2B procurement, supply chain decisions, retail delisting, or commercial defamation. Any commercial party relying on this data for business decisions does so entirely at their own risk.
          </p>
        </div>

        <div className="editorial-card p-6 space-y-3">
          <h2 className="font-serif text-xl font-semibold text-stone-900 dark:text-stone-100 flex items-center gap-2">
            <ShieldAlert className="w-5 h-5 text-teal-700 dark:text-teal-400" />
            Limitation of Liability
          </h2>
          <p>
            FoodFactsIndia.online provides data "as-is" based on global open-source registries and foreign government gazettes. We are not liable for any financial losses incurred by brands due to public awareness of their international formulation divergences. Product formulations change periodically; always verify the physical label.
          </p>
        </div>

        <div className="editorial-card p-6 space-y-3">
          <h2 className="font-serif text-xl font-semibold text-stone-900 dark:text-stone-100 flex items-center gap-2">
            <FileText className="w-5 h-5 text-teal-700 dark:text-teal-400" />
            Safe Harbor (IT Act Section 79)
          </h2>
          <p>
            As an aggregator of publicly available global regulatory data, FoodFactsIndia.online acts as an intermediary under Section 79 of the Information Technology Act, 2000. If a brand has reformulated a product and our legacy database reflects outdated information, brands must use our <strong>Grievance Officer portal</strong> to submit the new physical label for immediate correction.
          </p>
        </div>

        <div className="editorial-card p-6 space-y-3">
          <h2 className="font-serif text-lg font-semibold text-stone-900 dark:text-stone-100">
            Trademark & Fair Use
          </h2>
          <p className="text-xs text-stone-600 dark:text-stone-400 leading-relaxed">
            All trademarks, brand names, product names, and logos appearing on this platform are the property of their respective owners. They are used strictly and solely for product identification purposes under the doctrine of Nominative Fair Use. FoodFactsIndia.online is not affiliated with, endorsed by, or sponsored by any FMCG brand, the FSSAI, or any government body.
          </p>
        </div>

        <div className="editorial-card p-6 space-y-3">
          <h2 className="font-serif text-lg font-semibold text-stone-900 dark:text-stone-100">
            Simulated Warning Labels
          </h2>
          <p className="text-xs text-stone-600 dark:text-stone-400 leading-relaxed">
            Any "warning octagon" or front-of-package label simulations shown on this platform represent the policies of foreign governments (e.g., Mexico NOM-051, Chile Ley 20.606, EU Nutri-Score) and are NOT Indian Government mandates. They are presented solely for academic comparison and to advocate for the adoption of similar labeling standards in India.
          </p>
        </div>

        <div className="p-4 rounded-lg bg-stone-50 dark:bg-stone-850 border border-stone-200 dark:border-stone-800 text-xs text-stone-500 dark:text-stone-400">
          <p>
            <strong>Constitutional Basis:</strong> This platform operates under the protection of the Indian Constitution's Right to Freedom of Speech and Expression (Article 19(1)(a)) and the Right to Health (Article 21). Our work is protected public interest speech as affirmed in <em>Tata Tea Ltd. vs. Greenpeace</em> and related Supreme Court precedents.
          </p>
        </div>

      </div>
    </div>
  );
};
