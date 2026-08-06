import React, { useState } from 'react';
import {
  Calculator,
  ArrowLeft,
  ChevronRight,
  ShieldAlert,
  Share2
} from 'lucide-react';
import { TransparencyReport, Ingredient } from '../types';
import { ScoreGauge } from './ScoreGauge';
import { ScoreBreakdownModal } from './ScoreBreakdownModal';
import { EvidenceDrawerModal } from './EvidenceDrawerModal';
import { ProductImage } from './ProductImage';
import { GlobalRatingsStrip } from './GlobalRatingsStrip';
import { LatAmOctagonBadge } from './LatAmOctagonBadge';
import { InternationalMethodologyModal } from './InternationalMethodologyModal';
import { UnverifiedProductStubView } from './UnverifiedProductStubView';

interface TransparencyReportViewProps {
  report: TransparencyReport;
  onBackToSearch?: () => void;
  onCategoryFilter?: (category: string) => void;
}

export const TransparencyReportView: React.FC<TransparencyReportViewProps> = ({ report, onBackToSearch, onCategoryFilter }) => {
  if ((report.pageState && report.pageState !== 'verified_published') || report.isScoreWithheld) {
    return <UnverifiedProductStubView report={report} onBack={onBackToSearch} />;
  }

  const [activeTab, setActiveTab] = useState<'ingredients' | 'regulatory'>('ingredients');
  const [isMethodologyOpen, setIsMethodologyOpen] = useState(false);
  const [isIntlModalOpen, setIsIntlModalOpen] = useState(false);
  const [copied, setCopied] = useState(false);
  const [selectedDrawerIngredient, setSelectedDrawerIngredient] = useState<Ingredient | null>(null);
  const [drawerRawName, setDrawerRawName] = useState<string>('');

  const handleShare = () => {
    navigator.clipboard?.writeText(window.location.href);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const issues = report.scoreBreakdown.filter((b) => b.type === 'DEDUCTION');

  // Build 1-sentence issue summaries
  const unifiedFindings: { id: string; title: string; subtitle: string; severity: 'CRITICAL' | 'WARNING' | 'INFO' }[] = [];

  // 1. Bubbled Banned Additives (placed at the absolute top of the findings)
  const bannedIngredients = report.ingredientsList.filter((item) =>
    item.ingredient.regulatoryRecords?.some((r) => r.status === 'BANNED')
  );

  bannedIngredients.forEach((item, idx) => {
    const ing = item.ingredient;
    const bannedRecords = ing.regulatoryRecords.filter((r) => r.status === 'BANNED');
    const bannedCountries = bannedRecords.map((r) => `${r.flagEmoji || ''} ${r.countryName || r.countryCode}`).join(', ');
    const bannedRefs = bannedRecords.map((r) => r.regulationRef).filter(Boolean).join('; ');
    const harmText = ing.description || 'Prohibited food additive.';

    unifiedFindings.push({
      id: `banned_ing_${idx}`,
      title: `🔴 BANNED ADDITIVE: ${ing.canonicalName} (${ing.eNumber || 'No E-Number'})`,
      subtitle: `Prohibited in: ${bannedCountries}. Regulation: ${bannedRefs || 'Not specified'}. Harmful effect: ${harmText}`,
      severity: 'CRITICAL'
    });
  });

  // 2. Label Warnings
  report.labelWarnings?.forEach((w) => {
    unifiedFindings.push({
      id: w.id,
      title: w.title,
      subtitle: w.warningText,
      severity: 'CRITICAL'
    });
  });

  // 3. WHO Nutrition Flags
  report.whoNutritionFlags?.forEach((flag, idx) => {
    unifiedFindings.push({
      id: `who_${idx}`,
      title: flag.label,
      subtitle: `Declared ${flag.valueDeclared} (${flag.whoBenchmark}).`,
      severity: flag.severity === 'CRITICAL' ? 'CRITICAL' : 'WARNING'
    });
  });

  // 4. Deductions
  issues.forEach((iss, idx) => {
    if (!unifiedFindings.some(f => f.title.toLowerCase().includes(iss.factor.toLowerCase()))) {
      unifiedFindings.push({
        id: `deduction_${idx}`,
        title: iss.factor,
        subtitle: iss.rationale,
        severity: 'WARNING'
      });
    }
  });

  return (
    <div className="max-w-4xl mx-auto space-y-8 pb-16">
      
      {/* 1. Toolbar Navigation */}
      <div className="flex items-center justify-between text-xs pt-2">
        <div className="flex items-center gap-2 text-stone-600 dark:text-stone-400">
          {onBackToSearch && (
            <button
              onClick={onBackToSearch}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-md bg-stone-100 dark:bg-stone-800 text-stone-700 dark:text-stone-300 hover:bg-stone-200 dark:hover:bg-stone-700 transition-colors font-medium"
            >
              <ArrowLeft className="w-3.5 h-3.5 text-stone-500" />
              <span>Back to products</span>
            </button>
          )}

          <div className="hidden sm:flex items-center gap-1.5 text-stone-500">
            <button onClick={onBackToSearch} className="hover:text-teal-800 dark:hover:text-teal-400 hover:underline transition-colors">Products</button>
            <ChevronRight className="w-3 h-3" />
            <button
              onClick={() => onCategoryFilter?.(report.category)}
              className="hover:text-teal-800 dark:hover:text-teal-400 hover:underline transition-colors"
            >
              {report.category}
            </button>
            <ChevronRight className="w-3 h-3" />
            <span className="text-stone-900 dark:text-stone-100 font-medium truncate max-w-[200px]">{report.productName}</span>
          </div>
        </div>

        <button
          onClick={handleShare}
          className="px-3 py-1.5 rounded-md bg-stone-100 dark:bg-stone-800 hover:bg-stone-200 dark:hover:bg-stone-700 text-stone-700 dark:text-stone-300 font-medium flex items-center gap-1.5 transition-colors"
        >
          <Share2 className="w-3.5 h-3.5 text-stone-500" />
          <span>{copied ? 'Copied' : 'Share'}</span>
        </button>
      </div>

      {/* 2. Product Header & Title */}
      <div className="editorial-card p-6 sm:p-8 space-y-6">
        <div className="flex flex-col sm:flex-row items-start gap-6">
          <ProductImage
            barcode={report.barcode}
            productName={report.productName}
            className="w-28 h-28 sm:w-32 sm:h-32 rounded-md object-cover border border-stone-200 dark:border-stone-700 shrink-0"
          />

          <div className="space-y-2 flex-1">
            <div className="text-xs font-semibold uppercase tracking-wider text-teal-800 dark:text-teal-400">
              {report.brand} • {report.category}
            </div>

            <h1 className="font-serif text-2xl sm:text-3xl font-semibold text-stone-900 dark:text-stone-100">
              {report.productName}
            </h1>

            <p className="text-xs text-stone-500 dark:text-stone-400">
              Manufacturer: {report.manufacturer} • Pack Size: {report.packageSize} • GTIN: {report.barcode}
            </p>

            <div className="pt-2">
              <p className="text-sm text-stone-700 dark:text-stone-300 leading-relaxed bg-stone-50 dark:bg-stone-800/60 p-3.5 rounded border border-stone-200 dark:border-stone-700">
                {report.executiveSummary.verdictTitle}
              </p>
            </div>
          </div>
        </div>

        {/* Score Block */}
        <div className="pt-6 border-t border-stone-200 dark:border-stone-800 grid grid-cols-1 sm:grid-cols-2 gap-6 items-center">
          <div className="flex items-center gap-4">
            <ScoreGauge
              score={report.deterministicScore}
              grade={report.executiveSummary.grade}
              size="md"
              issuesCount={unifiedFindings.length}
            />
            <div>
              <h3 className="font-serif text-lg font-semibold text-stone-900 dark:text-stone-100">
                Score: {report.deterministicScore} / 100
              </h3>
              <p className="text-xs text-stone-500 dark:text-stone-400 mt-0.5">
                Grade {report.executiveSummary.grade} based on declared food composition and additives.
              </p>
              <button
                onClick={() => setIsMethodologyOpen(true)}
                className="text-xs text-teal-800 dark:text-teal-400 hover:underline mt-1 inline-flex items-center gap-1 font-medium"
              >
                <Calculator className="w-3 h-3" />
                View score rules
              </button>
            </div>
          </div>

          <div className="space-y-3">
            <GlobalRatingsStrip
              ratings={report.internationalRatings}
              foodfactsScore={report.deterministicScore}
              onOpenMethodology={() => setIsIntlModalOpen(true)}
            />

            {report.internationalRatings?.warningOctagons && (
              <LatAmOctagonBadge
                warnings={report.internationalRatings.warningOctagons}
                onOpenMethodology={() => setIsIntlModalOpen(true)}
              />
            )}
          </div>
        </div>
      </div>

      {/* 3. Key Concerns (1 sentence per finding) */}
      <div className="editorial-card p-6 space-y-4">
        <h2 className="font-serif text-xl font-semibold text-stone-900 dark:text-stone-100 flex items-center gap-2">
          <ShieldAlert className="w-5 h-5 text-amber-700 dark:text-amber-500" />
          Key Concerns & Findings ({unifiedFindings.length})
        </h2>

        {unifiedFindings.length === 0 ? (
          <p className="text-xs text-stone-600 dark:text-stone-400">
            No high-risk regulatory concerns or WHO nutrient benchmark violations flagged for this product.
          </p>
        ) : (
          <div className="space-y-3">
            {unifiedFindings.map((finding) => (
              <div
                key={finding.id}
                className="p-3.5 rounded bg-stone-50 dark:bg-stone-800/60 border border-stone-200 dark:border-stone-700/80 space-y-1"
              >
                <h4 className="font-semibold text-sm text-stone-900 dark:text-stone-100">
                  {finding.title}
                </h4>
                <p className="text-xs text-stone-600 dark:text-stone-300 leading-normal">
                  {finding.subtitle}
                </p>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* 4. Ingredient & Regulatory Tabs */}
      <div className="editorial-card p-6 space-y-6">
        <div className="flex border-b border-stone-200 dark:border-stone-800 gap-6">
          <button
            onClick={() => setActiveTab('ingredients')}
            className={`pb-2.5 text-sm font-medium border-b-2 transition-colors ${
              activeTab === 'ingredients'
                ? 'border-teal-700 text-teal-800 dark:border-teal-400 dark:text-teal-300 font-semibold'
                : 'border-transparent text-stone-500 hover:text-stone-900 dark:hover:text-stone-200'
            }`}
          >
            Ingredient Analysis ({report.ingredientsList.length})
          </button>

          <button
            onClick={() => setActiveTab('regulatory')}
            className={`pb-2.5 text-sm font-medium border-b-2 transition-colors ${
              activeTab === 'regulatory'
                ? 'border-teal-700 text-teal-800 dark:border-teal-400 dark:text-teal-300 font-semibold'
                : 'border-transparent text-stone-500 hover:text-stone-900 dark:hover:text-stone-200'
            }`}
          >
            Regulatory References
          </button>
        </div>

        {activeTab === 'ingredients' && (
          <div className="space-y-4">
            <div className="divide-y divide-stone-200 dark:divide-stone-800">
              {[...report.ingredientsList]
                .sort((a, b) => {
                  const aBanned = a.ingredient.regulatoryRecords?.some((r) => r.status === 'BANNED') ? 1 : 0;
                  const bBanned = b.ingredient.regulatoryRecords?.some((r) => r.status === 'BANNED') ? 1 : 0;
                  return bBanned - aBanned;
                })
                .map((item, idx) => {
                  const ing = item.ingredient;
                  const isBanned = ing.regulatoryRecords?.some((r) => r.status === 'BANNED');
                  return (
                    <div
                      key={ing.id || `ing_${idx}`}
                      className={`py-3 flex items-center justify-between cursor-pointer transition-colors px-2.5 rounded my-1.5 ${
                        isBanned
                          ? 'bg-rose-50/50 dark:bg-rose-950/20 border-l-4 border-rose-500 hover:bg-rose-100/40 dark:hover:bg-rose-900/20'
                          : 'hover:bg-stone-50 dark:hover:bg-stone-800/40'
                      }`}
                      onClick={() => {
                        setSelectedDrawerIngredient(ing);
                        setDrawerRawName(item.rawName || ing.canonicalName);
                      }}
                    >
                      <div className="space-y-0.5">
                        <h4 className="font-semibold text-sm text-stone-900 dark:text-stone-100 flex items-center gap-2">
                          <span>{ing.canonicalName}</span>
                          {ing.eNumber && (
                            <span className="px-1.5 py-0.5 rounded text-[11px] font-mono bg-stone-100 dark:bg-stone-800 text-stone-600 dark:text-stone-400">
                              {ing.eNumber}
                            </span>
                          )}
                          {isBanned && (
                            <span className="px-1.5 py-0.5 rounded text-[10px] uppercase font-bold bg-rose-100 text-rose-800 dark:bg-rose-950 dark:text-rose-200">
                              Banned
                            </span>
                          )}
                        </h4>
                        <p className="text-xs text-stone-500 dark:text-stone-400">
                          Category: {ing.category} • Risk: {ing.riskLevel}
                        </p>
                      </div>

                      <span className="text-xs text-teal-800 dark:text-teal-400 font-medium">
                        Evidence &rarr;
                      </span>
                    </div>
                  );
                })}
            </div>
          </div>
        )}

        {activeTab === 'regulatory' && (
          <div className="space-y-4 text-xs text-stone-700 dark:text-stone-300">
            <h3 className="font-serif text-base font-semibold text-stone-900 dark:text-stone-100">
              Regulatory Gazette & Citation Mapping
            </h3>
            <p className="leading-relaxed">
              Regulatory findings are cross-checked against FSSAI Food Safety and Standards (Food Products Standards and Food Additives) Regulations, EU Regulation (EC) No 1333/2008, and US FDA 21 CFR standards.
            </p>
            <div className="p-4 rounded bg-stone-50 dark:bg-stone-800/60 border border-stone-200 dark:border-stone-700 space-y-2 font-mono">
              <div>• FSSAI Gazette Schedule 2.4.5: Food Additives Authorization Matrix</div>
              <div>• US FDA 21 CFR Part 74/172: Food Additive Permitted Uses</div>
              <div>• EU Commission Regulation (EU) 2022/63: E171 Titanium Dioxide Status</div>
              <div>• WHO Guideline (2015): Sugars Intake for Adults and Children</div>
            </div>
          </div>
        )}
      </div>

      {/* Modals */}
      <ScoreBreakdownModal
        isOpen={isMethodologyOpen}
        onClose={() => setIsMethodologyOpen(false)}
        productName={report.productName}
        score={report.deterministicScore}
        breakdown={report.scoreBreakdown}
      />

      <InternationalMethodologyModal
        isOpen={isIntlModalOpen}
        onClose={() => setIsIntlModalOpen(false)}
      />

      <EvidenceDrawerModal
        isOpen={!!selectedDrawerIngredient}
        onClose={() => setSelectedDrawerIngredient(null)}
        ingredient={selectedDrawerIngredient}
        rawName={drawerRawName}
      />
    </div>
  );
};
