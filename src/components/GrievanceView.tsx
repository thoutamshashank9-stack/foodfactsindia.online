import React from 'react';
import { ShieldCheck, Mail, Clock, FileText } from 'lucide-react';

export const GrievanceView: React.FC = () => {
  return (
    <div className="max-w-3xl mx-auto py-10 px-4 space-y-8">
      <div className="space-y-3 text-center sm:text-left border-b border-stone-200 dark:border-stone-800 pb-6">
        <h1 className="font-serif text-3xl sm:text-4xl font-semibold text-stone-900 dark:text-stone-100">
          Grievance Redressal
        </h1>
        <p className="text-base text-stone-600 dark:text-stone-300 leading-relaxed">
          In accordance with the Information Technology Act, 2000 and IT (Intermediary Guidelines and Digital Media Ethics Code) Rules, 2021.
        </p>
      </div>

      <div className="space-y-6 text-sm text-stone-700 dark:text-stone-300 leading-relaxed">

        <div className="editorial-card p-6 space-y-4 border-l-4 border-teal-600 dark:border-teal-400">
          <h2 className="font-serif text-xl font-semibold text-stone-900 dark:text-stone-100 flex items-center gap-2">
            <ShieldCheck className="w-5 h-5 text-teal-700 dark:text-teal-400" />
            Grievance Officer
          </h2>
          <p>
            FoodFactsIndia.online has appointed a Grievance Officer to address concerns regarding data accuracy, trademark usage, or content removal requests. We are committed to verifying physical labels and correcting our open-source database promptly upon receiving valid, evidence-based grievances.
          </p>

          <div className="space-y-3 p-4 rounded-lg bg-stone-50 dark:bg-stone-850 border border-stone-200 dark:border-stone-800">
            <div className="flex items-center gap-2">
              <Mail className="w-4 h-4 text-teal-700 dark:text-teal-400" />
              <div>
                <div className="text-xs font-medium text-stone-500 dark:text-stone-400">Contact</div>
                <div className="font-semibold text-stone-900 dark:text-stone-100">
                  <a href="mailto:legal@foodfactsindia.online" className="hover:text-teal-700 dark:hover:text-teal-400 transition-colors underline">
                    legal@foodfactsindia.online
                  </a>
                </div>
              </div>
            </div>

            <div className="flex items-center gap-2">
              <Clock className="w-4 h-4 text-teal-700 dark:text-teal-400" />
              <div>
                <div className="text-xs font-medium text-stone-500 dark:text-stone-400">Response Time</div>
                <div className="font-semibold text-stone-900 dark:text-stone-100">Within 72 hours of receiving a valid grievance</div>
              </div>
            </div>
          </div>
        </div>

        <div className="editorial-card p-6 space-y-3">
          <h2 className="font-serif text-xl font-semibold text-stone-900 dark:text-stone-100 flex items-center gap-2">
            <FileText className="w-5 h-5 text-teal-700 dark:text-teal-400" />
            How to File a Grievance
          </h2>
          <p>
            If you are a brand representative, regulatory official, or consumer and believe any data on this platform is inaccurate or outdated, please email <a href="mailto:legal@foodfactsindia.online" className="text-teal-700 dark:text-teal-400 hover:underline font-medium">legal@foodfactsindia.online</a> with the following:
          </p>
          <ol className="list-decimal pl-5 space-y-2 text-stone-600 dark:text-stone-400">
            <li>The product barcode (GTIN-13) and product name in question.</li>
            <li>A clear photo of the current physical label (ingredients list and nutrition panel).</li>
            <li>A description of the specific data point you believe is incorrect.</li>
            <li>Your name, title, and relationship to the product (brand representative, consumer, etc.).</li>
          </ol>
          <p className="text-xs text-stone-500 dark:text-stone-400 italic">
            We verify physical labels and update our open-source database within 72 hours of receiving a valid, evidence-based grievance.
          </p>
        </div>

        <div className="editorial-card p-6 space-y-3">
          <h2 className="font-serif text-lg font-semibold text-stone-900 dark:text-stone-100">
            Safe Harbor (IT Act Section 79)
          </h2>
          <p className="text-xs text-stone-600 dark:text-stone-400 leading-relaxed">
            As an aggregator of publicly available global regulatory data, FoodFactsIndia.online acts as an intermediary. If a brand has reformulated a product and our legacy database reflects outdated information, brands must use this Grievance Officer portal to submit the new physical label for immediate correction. We will act upon valid takedown or correction requests within the statutory time limits prescribed under the IT Act and Rules.
          </p>
        </div>

      </div>
    </div>
  );
};
