import React, { useState } from 'react';
import { AccessibleModal } from './AccessibleModal';
import { ShieldCheck, FileText } from 'lucide-react';

interface PrivacyTermsModalProps {
  isOpen: boolean;
  onClose: () => void;
  initialTab?: 'privacy' | 'terms';
}

export const PrivacyTermsModal: React.FC<PrivacyTermsModalProps> = ({
  isOpen,
  onClose,
  initialTab = 'privacy'
}) => {
  const [activeTab, setActiveTab] = useState<'privacy' | 'terms'>(initialTab);

  return (
    <AccessibleModal isOpen={isOpen} onClose={onClose} title="FoodFactsIndia — Privacy & Terms">
      <div className="space-y-4">
        
        {/* Navigation Tabs */}
        <div className="flex border-b border-stone-200 dark:border-stone-800 gap-4">
          <button
            onClick={() => setActiveTab('privacy')}
            className={`pb-2 font-semibold text-xs border-b-2 flex items-center gap-1.5 transition-colors ${
              activeTab === 'privacy'
                ? 'border-teal-700 text-teal-800 dark:border-teal-400 dark:text-teal-300'
                : 'border-transparent text-stone-500 hover:text-stone-900 dark:hover:text-white'
            }`}
          >
            <ShieldCheck className="w-4 h-4" />
            <span>Privacy Policy</span>
          </button>
          <button
            onClick={() => setActiveTab('terms')}
            className={`pb-2 font-semibold text-xs border-b-2 flex items-center gap-1.5 transition-colors ${
              activeTab === 'terms'
                ? 'border-teal-700 text-teal-800 dark:border-teal-400 dark:text-teal-300'
                : 'border-transparent text-stone-500 hover:text-stone-900 dark:hover:text-white'
            }`}
          >
            <FileText className="w-4 h-4" />
            <span>Terms of Service</span>
          </button>
        </div>

        {/* Tab Content */}
        {activeTab === 'privacy' && (
          <div className="space-y-3 leading-relaxed text-sm text-stone-700 dark:text-stone-300">
            <h3 className="font-semibold text-stone-900 dark:text-white">Consumer Privacy Policy (FSSAI & DPDP Act 2023)</h3>
            <p>
              FoodFactsIndia respects consumer privacy rights. We do not sell personal identification information or track browsing habits across third-party networks.
            </p>
            <h4 className="font-semibold text-stone-800 dark:text-stone-200">1. Data Collection & Processing</h4>
            <p>
              Product data is sourced from official regulatory databases (FSSAI, EFSA, US FDA, Codex Alimentarius) and verified package labels. No personal user data is collected beyond anonymous interaction metrics.
            </p>
            <h4 className="font-semibold text-stone-800 dark:text-stone-200">2. Telemetry & Analytics</h4>
            <p>
              Anonymous interaction metrics are logged to improve search accuracy and ingredient parsing reliability. Users may clear local storage buffers at any time.
            </p>
          </div>
        )}

        {activeTab === 'terms' && (
          <div className="space-y-3 leading-relaxed text-sm text-stone-700 dark:text-stone-300">
            <h3 className="font-semibold text-stone-900 dark:text-white">Terms of Use & Scientific Transparency Notice</h3>
            <p>
              FoodFactsIndia provides deterministic ingredient analysis, global regulatory cross-referencing (EU, FDA, FSSAI, MHLW), and mathematical score evaluations for informational purposes.
            </p>
            <h4 className="font-semibold text-stone-800 dark:text-stone-200">1. Medical & Dietary Disclaimer</h4>
            <p>
              Automated ratings and NOVA processing classifications do not constitute medical diagnosis, allergy guarantees, or clinical advice. Consumers with severe food allergies should inspect physical package labels directly.
            </p>
            <h4 className="font-semibold text-stone-800 dark:text-stone-200">2. Independent Methodology</h4>
            <p>
              EU Nutri-Score, Latin American warning octagons, and FoodFactsIndia transparency scores operate on independent, published scientific standards and carry no manufacturer bias.
            </p>
          </div>
        )}

        <div className="pt-3 border-t border-stone-200 dark:border-stone-800 flex justify-end">
          <button
            onClick={onClose}
            className="px-5 py-2 bg-stone-900 dark:bg-stone-100 text-white dark:text-stone-900 font-medium text-xs rounded-md hover:opacity-90 transition"
          >
            Close
          </button>
        </div>

      </div>
    </AccessibleModal>
  );
};
