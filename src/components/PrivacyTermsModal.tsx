import React, { useState } from 'react';
import { AccessibleModal } from './AccessibleModal';
import { ShieldCheck, FileText, Lock } from 'lucide-react';

interface PrivacyTermsModalProps {
  isOpen: boolean;
  onClose: () => void;
  initialTab?: 'privacy' | 'terms' | 'retention';
}

export const PrivacyTermsModal: React.FC<PrivacyTermsModalProps> = ({
  isOpen,
  onClose,
  initialTab = 'privacy'
}) => {
  const [activeTab, setActiveTab] = useState<'privacy' | 'terms' | 'retention'>(initialTab);

  return (
    <AccessibleModal isOpen={isOpen} onClose={onClose} title="FoodFactsIndia AI — Privacy, Terms & Data Governance">
      <div className="space-y-4">
        
        {/* Navigation Tabs */}
        <div className="flex border-b border-slate-200 dark:border-slate-800 gap-4">
          <button
            onClick={() => setActiveTab('privacy')}
            className={`pb-2 font-bold text-xs border-b-2 flex items-center gap-1.5 transition-colors ${
              activeTab === 'privacy'
                ? 'border-blue-600 text-blue-600 dark:text-blue-400'
                : 'border-transparent text-slate-500 hover:text-slate-900 dark:hover:text-white'
            }`}
          >
            <ShieldCheck className="w-4 h-4" />
            <span>Privacy Policy</span>
          </button>
          <button
            onClick={() => setActiveTab('terms')}
            className={`pb-2 font-bold text-xs border-b-2 flex items-center gap-1.5 transition-colors ${
              activeTab === 'terms'
                ? 'border-blue-600 text-blue-600 dark:text-blue-400'
                : 'border-transparent text-slate-500 hover:text-slate-900 dark:hover:text-white'
            }`}
          >
            <FileText className="w-4 h-4" />
            <span>Terms of Service</span>
          </button>
          <button
            onClick={() => setActiveTab('retention')}
            className={`pb-2 font-bold text-xs border-b-2 flex items-center gap-1.5 transition-colors ${
              activeTab === 'retention'
                ? 'border-blue-600 text-blue-600 dark:text-blue-400'
                : 'border-transparent text-slate-500 hover:text-slate-900 dark:hover:text-white'
            }`}
          >
            <Lock className="w-4 h-4" />
            <span>Photo Retention</span>
          </button>
        </div>

        {/* Tab Content */}
        {activeTab === 'privacy' && (
          <div className="space-y-3 leading-relaxed">
            <h3 className="font-extrabold text-slate-900 dark:text-white text-sm">Consumer Privacy Policy (FSSAI & DPDP Act 2023)</h3>
            <p>
              FoodFactsIndia AI respects consumer privacy rights. We do not sell personal identification information or track browsing habits across third-party networks.
            </p>
            <h4 className="font-bold text-slate-800 dark:text-slate-200">1. Data Collection & Processing</h4>
            <p>
              When submitting package label photos or audit requests, optional contact information (e.g. email) is used strictly to send status notifications for your audit tracking ID.
            </p>
            <h4 className="font-bold text-slate-800 dark:text-slate-200">2. Telemetry & Analytics</h4>
            <p>
              Anonymous interaction metrics are logged to improve search accuracy and ingredient parsing reliability. Users may clear local storage buffers at any time.
            </p>
          </div>
        )}

        {activeTab === 'terms' && (
          <div className="space-y-3 leading-relaxed">
            <h3 className="font-extrabold text-slate-900 dark:text-white text-sm">Terms of Use & Scientific Transparency Notice</h3>
            <p>
              FoodFactsIndia AI provides deterministic ingredient analysis, global regulatory cross-referencing (EU, FDA, FSSAI, MHLW), and mathematical score evaluations for informational purposes.
            </p>
            <h4 className="font-bold text-slate-800 dark:text-slate-200">1. Medical & Dietary Disclaimer</h4>
            <p>
              Automated ratings and NOVA processing classifications do not constitute medical diagnosis, allergy guarantees, or clinical advice. Consumers with severe food allergies should inspect physical package labels directly.
            </p>
            <h4 className="font-bold text-slate-800 dark:text-slate-200">2. Independent Methodology</h4>
            <p>
              EU Nutri-Score, Latin American warning octagons, and FoodFactsIndia transparency scores operate on independent, published scientific standards and carry no manufacturer bias.
            </p>
          </div>
        )}

        {activeTab === 'retention' && (
          <div className="space-y-3 leading-relaxed">
            <h3 className="font-extrabold text-slate-900 dark:text-white text-sm">Package Photo Evidence Retention Policy</h3>
            <p>
              User-uploaded physical package label photos are stored in secure cold storage to maintain audit trails for crowdsourced product data verification.
            </p>
            <h4 className="font-bold text-slate-800 dark:text-slate-200">1. Retention Duration</h4>
            <p>
              Uploaded evidence photos are retained indefinitely for public regulatory auditing and OCR training unless explicitly deleted via user request.
            </p>
            <h4 className="font-bold text-slate-800 dark:text-slate-200">2. Right to Erasure</h4>
            <p>
              Users may request image deletion within 24 hours of submission using their generated tracking ID (e.g. <code>TRK-2026-XXXXXXX</code>).
            </p>
          </div>
        )}

        <div className="pt-3 border-t border-slate-200 dark:border-slate-800 flex justify-end">
          <button
            onClick={onClose}
            className="px-5 py-2 bg-slate-900 dark:bg-slate-100 text-white dark:text-slate-900 font-extrabold text-xs rounded-xl hover:bg-slate-800 transition"
          >
            Close
          </button>
        </div>

      </div>
    </AccessibleModal>
  );
};
