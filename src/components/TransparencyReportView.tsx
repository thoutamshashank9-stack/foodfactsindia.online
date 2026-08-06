import React, { useState } from 'react';
import {
  ArrowLeft,
  ChevronRight,
  Share2
} from 'lucide-react';
import { TransparencyReport, Ingredient } from '../types';
import { ScoreBreakdownModal } from './ScoreBreakdownModal';
import { EvidenceDrawerModal } from './EvidenceDrawerModal';
import { InternationalMethodologyModal } from './InternationalMethodologyModal';
import { UnverifiedProductStubView } from './UnverifiedProductStubView';

// Sub-components
import { ProductHeader } from './report/ProductHeader';
import { BannedStatusBanner } from './report/BannedStatusBanner';
import { JurisdictionRatings } from './report/JurisdictionRatings';
import { WarningLabels } from './report/WarningLabels';
import { KeyConcernsList } from './report/KeyConcernsList';
import { IngredientTable } from './report/IngredientTable';
import { Card } from './Card';

interface TransparencyReportViewProps {
  report: TransparencyReport;
  onBackToSearch?: () => void;
  onCategoryFilter?: (category: string) => void;
}

export const TransparencyReportView: React.FC<TransparencyReportViewProps> = ({
  report,
  onBackToSearch,
  onCategoryFilter,
}) => {
  if ((report.pageState && report.pageState !== 'verified_published') || report.isScoreWithheld) {
    return <UnverifiedProductStubView report={report} onBack={onBackToSearch} />;
  }

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

  // Build unified findings
  const unifiedFindings: { id: string; title: string; subtitle: string; severity: 'CRITICAL' | 'WARNING' | 'INFO' }[] = [];

  // 1. Bubbled Banned Additives
  const bannedIngredients = report.ingredientsList.filter((item) =>
    item.ingredient.regulatoryRecords?.some((r) => r.status === 'BANNED')
  );

  const bannedItems = bannedIngredients.map((item) => {
    const ing = item.ingredient;
    const bannedRecords = ing.regulatoryRecords.filter((r) => r.status === 'BANNED');
    const bannedCountries = bannedRecords.map((r) => `${r.flagEmoji || ''} ${r.countryName || r.countryCode}`).join(', ');
    const bannedRefs = bannedRecords.map((r) => r.regulationRef).filter(Boolean).join('; ');
    const harmText = ing.description || 'Prohibited food additive.';
    return {
      name: `${ing.canonicalName}${ing.eNumber ? ` (${ing.eNumber})` : ''}`,
      countries: bannedCountries,
      reason: harmText,
      citations: bannedRefs
    };
  });

  bannedIngredients.forEach((item, idx) => {
    const ing = item.ingredient;
    const bannedRecords = ing.regulatoryRecords.filter((r) => r.status === 'BANNED');
    const bannedCountries = bannedRecords.map((r) => `${r.flagEmoji || ''} ${r.countryName || r.countryCode}`).join(', ');
    const bannedRefs = bannedRecords.map((r) => r.regulationRef).filter(Boolean).join('; ');
    const harmText = ing.description || 'Prohibited food additive.';

    unifiedFindings.push({
      id: `banned_ing_${idx}`,
      title: `Banned Additive: ${ing.canonicalName} (${ing.eNumber || 'No E-Number'})`,
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
    <div className="max-w-3xl mx-auto space-y-6 pb-16">
      
      {/* 1. Toolbar Navigation */}
      <div className="flex items-center justify-between text-xs pt-2">
        <div className="flex items-center gap-2 text-stone-600 dark:text-stone-400">
          {onBackToSearch && (
            <button
              onClick={onBackToSearch}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-md bg-stone-100 dark:bg-stone-850 text-stone-700 dark:text-stone-300 hover:bg-stone-200 dark:hover:bg-stone-800 transition-colors font-medium"
            >
              <ArrowLeft className="w-3.5 h-3.5" strokeWidth={2.5} />
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
          className="px-3 py-1.5 rounded-md bg-stone-100 dark:bg-stone-850 hover:bg-stone-200 dark:hover:bg-stone-800 text-stone-700 dark:text-stone-300 font-medium flex items-center gap-1.5 transition-colors"
        >
          <Share2 className="w-3.5 h-3.5 text-stone-500" />
          <span>{copied ? 'Copied' : 'Share'}</span>
        </button>
      </div>

      {/* 2. Main Redesigned Layout: Single Column Stack */}
      <div className="flex flex-col space-y-4">
        
        {bannedItems.length > 0 && (
          <BannedStatusBanner bannedItems={bannedItems} />
        )}

        <ProductHeader report={report} issuesCount={unifiedFindings.length} />
        
        {/* Unified Key Concerns list */}
        <KeyConcernsList findings={unifiedFindings} />

        {/* Multi-Jurisdiction Front-of-Package Ratings */}
        <JurisdictionRatings
          ratings={report.internationalRatings}
          foodfactsScore={report.deterministicScore}
          onOpenMethodology={() => setIsIntlModalOpen(true)}
        />

        {/* Simulated Warning Labels (NOM-051, Ley 20.606) */}
        {report.internationalRatings?.warningOctagons && (
          <WarningLabels
            warnings={report.internationalRatings.warningOctagons}
            onOpenMethodology={() => setIsIntlModalOpen(true)}
          />
        )}

        {/* Ingredient list and risk matrix analysis */}
        <IngredientTable
          ingredientsList={report.ingredientsList}
          onSelectIngredient={(ing, rawName) => {
            setSelectedDrawerIngredient(ing);
            setDrawerRawName(rawName);
          }}
        />

        {/* Regulatory Citation matrix */}
        <Card className="space-y-3">
          <h4 className="font-serif text-sm font-bold text-stone-900 dark:text-stone-100">
            Regulatory Gazette &amp; Mapping Sources
          </h4>
          <p className="text-xs text-stone-605 dark:text-stone-400 leading-relaxed">
            Findings mapped directly from Schedule 2.4.5 of FSSAI Food Safety and Standards (Food Additives) Regulations, EU Additives Database (EC No 1333/2008), and FDA 21 CFR standards.
          </p>
          <div className="p-3 rounded-lg bg-stone-50 dark:bg-stone-850 border border-stone-200 dark:border-stone-800 space-y-1.5 font-mono text-[10px] text-stone-500 dark:text-stone-400">
            <div>• FSSAI Category: {report.category}</div>
            <div>• EU Commission Regulation (EU) 2022/63: titanium dioxide update</div>
            <div>• Codex General Standard for Food Additives (GSFA Online Database)</div>
          </div>
        </Card>

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
