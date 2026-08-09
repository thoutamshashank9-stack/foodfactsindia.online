import React, { useState } from 'react';
import { ShieldCheck, HeartHandshake, Info } from 'lucide-react';
import { InternationalMethodologyModal } from './InternationalMethodologyModal';
import { PrivacyTermsModal } from './PrivacyTermsModal';

interface FooterProps {
  onOpenGrievance?: () => void;
  onOpenManifesto?: () => void;
}

export const Footer: React.FC<FooterProps> = ({ onOpenGrievance, onOpenManifesto }) => {
  const [isIntlModalOpen, setIsIntlModalOpen] = useState(false);
  const [isPrivacyModalOpen, setIsPrivacyModalOpen] = useState(false);
  const [privacyTab, setPrivacyTab] = useState<'privacy' | 'terms'>('privacy');

  const openPrivacyModal = (tab: 'privacy' | 'terms') => {
    setPrivacyTab(tab);
    setIsPrivacyModalOpen(true);
  };

  return (
    <footer className="mt-16 border-t border-stone-200 dark:border-stone-800 bg-[#fcfbf9] dark:bg-[#0e1117] text-stone-600 dark:text-stone-400 py-10 transition-colors">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 space-y-8">
        
        {/* Principles Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 pb-8 border-b border-stone-200 dark:border-stone-800 text-xs">
          <div className="space-y-1.5">
            <h4 className="font-serif font-semibold text-stone-900 dark:text-stone-100 text-sm">Evidence First</h4>
            <p className="text-stone-600 dark:text-stone-400 leading-relaxed">
              Every rating is grounded strictly in published FSSAI, EFSA, and US FDA scientific literature and toxicological data.
            </p>
          </div>

          <div className="space-y-1.5">
            <h4 className="font-serif font-semibold text-stone-900 dark:text-stone-100 text-sm">Public Interest Neutrality</h4>
            <p className="text-stone-600 dark:text-stone-400 leading-relaxed">
              FoodFactsIndia objectively decodes declared ingredient lists and regulatory statuses using transparent algorithms.
            </p>
          </div>

          <div className="space-y-1.5">
            <h4 className="font-serif font-semibold text-stone-900 dark:text-stone-100 text-sm">Public Health Disclaimer</h4>
            <p className="text-stone-600 dark:text-stone-400 leading-relaxed">
              FoodFactsIndia is an educational research platform and does not provide clinical, medical, or dietary diagnosis.
            </p>
          </div>
        </div>

        {/* Footer Bottom */}
        <div className="flex flex-col sm:flex-row items-center justify-between text-xs gap-4 text-stone-500 dark:text-stone-400 font-normal">
          <div>
            <span className="font-serif font-bold text-stone-900 dark:text-stone-100 mr-2">FoodFactsIndia</span>
            <span>© {new Date().getFullYear()} FoodFactsIndia Public Research Platform.</span>
          </div>
          <div className="flex items-center gap-4">
            <button
              onClick={() => setIsIntlModalOpen(true)}
              className="hover:text-stone-900 dark:hover:text-stone-100 transition-colors focus:outline-none hover:underline"
            >
              Methodology & Regulatory Sources
            </button>
            <button
              onClick={() => openPrivacyModal('privacy')}
              className="hover:text-stone-900 dark:hover:text-stone-100 transition-colors focus:outline-none hover:underline"
            >
              Privacy Policy
            </button>
            <button
              onClick={() => openPrivacyModal('terms')}
              className="hover:text-stone-900 dark:hover:text-stone-100 transition-colors focus:outline-none hover:underline"
            >
              Terms
            </button>
            <button
              onClick={() => onOpenGrievance?.()}
              className="hover:text-stone-900 dark:hover:text-stone-100 transition-colors focus:outline-none hover:underline"
            >
              Grievance
            </button>
            <button
              onClick={() => onOpenManifesto?.()}
              className="hover:text-stone-900 dark:hover:text-stone-100 transition-colors focus:outline-none hover:underline"
            >
              Manifesto
            </button>
          </div>
        </div>

        {/* Legal & Regulatory Disclaimer */}
        <div className="pt-6 border-t border-stone-200 dark:border-stone-800 text-[10px] text-stone-400 dark:text-stone-500 leading-relaxed space-y-2">
          <p>
            <strong className="text-stone-500 dark:text-stone-400">Data Verification Notice:</strong> Product details are compiled from publicly available labels, brand information, and user-contributed data. Formulations may change over time. Always verify the physical package label before relying on ingredient information. If a brand or consumer finds outdated information, it can be reported for immediate correction.
          </p>
          <p>
            <strong className="text-stone-500 dark:text-stone-400">Open Database License (ODbL) Attribution:</strong> Ingredient and product data sourced in part from Open Food Facts (<a href="https://openfoodfacts.org" target="_blank" rel="noopener noreferrer" className="underline hover:text-stone-600 dark:hover:text-stone-300">openfoodfacts.org</a>), contributed by the global community under the Open Database License (ODbL), as well as official brand publications and physical packaging.
          </p>
          <p>
            <strong className="text-stone-500 dark:text-stone-400">Legal & Regulatory Notice:</strong> FoodFactsIndia.online is an independent educational platform. We are not affiliated with any FMCG brand, the FSSAI, or any government body. All trademarks and brand names are the property of their respective owners and are used strictly for product identification under the doctrine of Nominative Fair Use. Simulated warning labels represent foreign policies and are NOT Indian Government mandates.
          </p>
        </div>

      </div>

      {/* Modals */}
      <InternationalMethodologyModal
        isOpen={isIntlModalOpen}
        onClose={() => setIsIntlModalOpen(false)}
      />

      <PrivacyTermsModal
        isOpen={isPrivacyModalOpen}
        onClose={() => setIsPrivacyModalOpen(false)}
        initialTab={privacyTab}
      />
    </footer>
  );
};
