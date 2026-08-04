import React, { useState } from 'react';
import {
  ShieldCheck,
  CheckCircle2,
  AlertTriangle,
  FileText,
  Globe,
  ExternalLink,
  ChevronDown,
  ChevronUp,
  Share2,
  Calculator,
  Award,
  Sparkles,
  BookOpen,
  ArrowLeft,
  ChevronRight,
  ShieldAlert
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
}

export const TransparencyReportView: React.FC<TransparencyReportViewProps> = ({ report, onBackToSearch }) => {
  // Hard Render Contract: If pageState is not verified_published, render Stub View ONLY
  if (report.pageState && report.pageState !== 'verified_published' || report.isScoreWithheld) {
    return <UnverifiedProductStubView report={report} onBack={onBackToSearch} />;
  }

  const [activeTab, setActiveTab] = useState<'ingredients' | 'nutrition' | 'regulatory' | 'science'>('ingredients');
  const [expandedIngId, setExpandedIngId] = useState<string | null>(null);
  const [isMethodologyOpen, setIsMethodologyOpen] = useState(false);
  const [isIntlModalOpen, setIsIntlModalOpen] = useState(false);
  const [showAllFindings, setShowAllFindings] = useState(false);
  const [isDisclaimerOpen, setIsDisclaimerOpen] = useState(false);
  const [copied, setCopied] = useState(false);

  // Evidence Drawer Modal State
  const [selectedDrawerIngredient, setSelectedDrawerIngredient] = useState<Ingredient | null>(null);
  const [drawerRawName, setDrawerRawName] = useState<string>('');

  const toggleIngExpand = (id: string) => {
    setExpandedIngId(expandedIngId === id ? null : id);
  };

  const handleShare = () => {
    navigator.clipboard?.writeText(window.location.href);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const controversialIngredients = report.ingredientsList.filter((i) => i.isControversial);
  const issues = report.scoreBreakdown.filter((b) => b.type === 'DEDUCTION');

  // Build unified list of plain-language findings (top concerns)
  const unifiedFindings: { id: string; title: string; subtitle: string; severity: 'CRITICAL' | 'WARNING' | 'INFO' }[] = [];

  // Add Label Warnings
  report.labelWarnings?.forEach((w) => {
    unifiedFindings.push({
      id: w.id,
      title: w.title,
      subtitle: w.warningText,
      severity: 'CRITICAL'
    });
  });

  // Add WHO Flags
  report.whoNutritionFlags?.forEach((flag, idx) => {
    unifiedFindings.push({
      id: `who_${idx}`,
      title: flag.label,
      subtitle: `Declared ${flag.valueDeclared} (${flag.whoBenchmark})`,
      severity: flag.severity === 'CRITICAL' ? 'CRITICAL' : 'WARNING'
    });
  });

  // Add Deductions
  issues.forEach((iss, idx) => {
    // Avoid duplication if already in label warnings or WHO flags
    if (!unifiedFindings.some(f => f.title.toLowerCase().includes(iss.factor.toLowerCase()))) {
      unifiedFindings.push({
        id: `deduction_${idx}`,
        title: iss.factor,
        subtitle: iss.rationale,
        severity: 'WARNING'
      });
    }
  });

  const visibleFindings = showAllFindings ? unifiedFindings : unifiedFindings.slice(0, 3);

  return (
    <div className="max-w-5xl mx-auto space-y-6 animate-fade-in pb-16">
      
      {/* 1. Breadcrumb Navigation & Top Toolbar */}
      <div className="flex flex-wrap items-center justify-between gap-3 text-xs">
        <div className="flex items-center gap-2 text-slate-600 dark:text-slate-400 font-medium">
          {onBackToSearch && (
            <button
              onClick={onBackToSearch}
              className="min-h-[44px] min-w-[44px] flex items-center gap-1.5 px-3 py-2 rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors font-bold shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <ArrowLeft className="w-4 h-4 text-blue-600 dark:text-blue-400" />
              <span>Back</span>
            </button>
          )}

          {/* Breadcrumb Trail */}
          <div className="hidden sm:flex items-center gap-1.5 font-semibold text-slate-500 dark:text-slate-400">
            <span>Home</span>
            <ChevronRight className="w-3.5 h-3.5 opacity-50" />
            <span>{report.category}</span>
            <ChevronRight className="w-3.5 h-3.5 opacity-50" />
            <span className="text-slate-900 dark:text-white font-bold truncate max-w-[200px]">{report.productName}</span>
          </div>
        </div>

        <button
          onClick={handleShare}
          className="min-h-[44px] px-4 py-2.5 rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300 font-bold flex items-center gap-2 transition-colors shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <Share2 className="w-4 h-4 text-blue-500" />
          <span>{copied ? 'Link Copied!' : 'Share'}</span>
        </button>
      </div>

      {/* 2. Executive Product Hero */}
      <div className="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 p-6 sm:p-8 shadow-xl relative overflow-hidden">
        <div className="grid grid-cols-1 md:grid-cols-12 gap-8 items-center">
          
          {/* Left Product Info & Title */}
          <div className="md:col-span-7 flex flex-col sm:flex-row items-center sm:items-start gap-6 text-center sm:text-left">
            <ProductImage
              barcode={report.barcode}
              productName={report.productName}
              className="w-32 h-32 sm:w-40 sm:h-40 rounded-2xl object-cover border-2 border-slate-200 dark:border-slate-700 shadow-xl shrink-0"
            />
            <div className="space-y-2">
              <div className="flex items-center justify-center sm:justify-start gap-2">
                <span className="text-xs font-extrabold uppercase tracking-wider text-blue-600 dark:text-blue-400">
                  {report.brand}
                </span>
                <span className="text-[11px] text-slate-400 dark:text-slate-500 font-mono">
                  • GTIN: {report.barcode}
                </span>
              </div>

              <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white tracking-tight leading-tight">
                {report.productName}
              </h1>

              <p className="text-xs text-slate-500 dark:text-slate-400 font-medium">
                {report.manufacturer} • Pack Size: {report.packageSize}
              </p>

              {/* 1-Line Verdict Pill */}
              <div className="pt-2">
                <div className="inline-flex items-start gap-2 p-3 rounded-2xl bg-slate-50 dark:bg-slate-800/70 border border-slate-200/80 dark:border-slate-700/80 text-xs text-slate-700 dark:text-slate-200 text-left">
                  <Sparkles className="w-4 h-4 text-amber-500 shrink-0 mt-0.5" />
                  <span className="font-semibold">{report.executiveSummary.verdictTitle}</span>
                </div>
              </div>
            </div>
          </div>

          {/* Right Standardized Score Gauge & Grade */}
          <div className="md:col-span-5 flex flex-col items-center justify-center p-6 rounded-2xl bg-slate-50/80 dark:bg-slate-850/60 border border-slate-200/60 dark:border-slate-800/80 text-center space-y-3">
            <div className="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">
              Transparency Score & Grade
            </div>
            
            {report.isScoreWithheld ? (
              <div className="p-4 rounded-2xl bg-amber-50 dark:bg-amber-950/50 border border-amber-300 dark:border-amber-800 text-amber-900 dark:text-amber-200 space-y-2 text-center">
                <div className="flex items-center justify-center gap-1.5 text-xs font-extrabold text-amber-700 dark:text-amber-300 uppercase tracking-wider">
                  <ShieldAlert className="w-4 h-4 text-amber-600 dark:text-amber-400" />
                  <span>Score Withheld</span>
                </div>
                <div className="text-2xl font-black text-amber-800 dark:text-amber-200">
                  N/A
                </div>
                <p className="text-[11px] leading-snug font-medium text-amber-800/90 dark:text-amber-300/90">
                  {report.scoreWithheldReason || 'Insufficient label data: Ingredients or nutrition facts are pending manufacturer verification.'}
                </p>
              </div>
            ) : (
              <ScoreGauge
                score={report.deterministicScore}
                grade={report.executiveSummary.grade}
                size="lg"
                issuesCount={unifiedFindings.length}
              />
            )}

            <button
              onClick={() => setIsMethodologyOpen(true)}
              className="min-h-[44px] px-4 py-2 rounded-xl bg-blue-100 dark:bg-blue-950/80 text-blue-700 dark:text-blue-300 font-bold text-xs flex items-center gap-2 hover:bg-blue-200 dark:hover:bg-blue-900 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <Calculator className="w-4 h-4" />
              <span>View Scoring Rules</span>
            </button>
          </div>

        </div>

        {/* 2. Global Ratings Strip (Nutri-Score, FoodFactsIndia, FDA) */}
        <div className="mt-8">
          <GlobalRatingsStrip
            ratings={report.internationalRatings}
            foodfactsScore={report.deterministicScore}
            onOpenMethodology={() => setIsIntlModalOpen(true)}
          />
        </div>

        {/* 3. Mandatory Health Warning Octagons */}
        {report.internationalRatings?.warningOctagons && (
          <div className="mt-8">
            <LatAmOctagonBadge
              warnings={report.internationalRatings.warningOctagons}
              onOpenMethodology={() => setIsIntlModalOpen(true)}
            />
          </div>
        )}

        {/* 4. Unified Key Findings & Concerns (Top 3 + Progressive Disclosure Accordion) */}
        <div className="mt-8 pt-6 border-t border-slate-100 dark:border-slate-800 space-y-4">
          <div className="flex items-center justify-between mb-3">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400 flex items-center gap-1.5">
              <ShieldAlert className="w-4 h-4 text-amber-500" />
              Key Concerns & Findings ({unifiedFindings.length})
            </h3>
            {unifiedFindings.length > 3 && (
              <button
                onClick={() => setShowAllFindings(!showAllFindings)}
                className="text-xs font-bold text-blue-600 dark:text-blue-400 hover:underline flex items-center gap-1 min-h-[44px] px-2"
              >
                <span>{showAllFindings ? 'Show Top 3 Only' : `See all ${unifiedFindings.length} findings`}</span>
                <ChevronDown className={`w-3.5 h-3.5 transition-transform ${showAllFindings ? 'rotate-180' : ''}`} />
              </button>
            )}
          </div>

          {unifiedFindings.length > 0 ? (
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              {visibleFindings.map((finding) => (
                <div
                  key={finding.id}
                  className={`p-3.5 rounded-2xl border text-xs font-medium space-y-1 transition-all shadow-sm ${
                    finding.severity === 'CRITICAL'
                      ? 'bg-rose-50/70 dark:bg-rose-950/30 border-rose-200 dark:border-rose-900/60 text-rose-900 dark:text-rose-200'
                      : 'bg-amber-50/70 dark:bg-amber-950/30 border-amber-200 dark:border-amber-900/60 text-amber-900 dark:text-amber-200'
                  }`}
                >
                  <div className="flex items-center gap-1.5 font-extrabold text-slate-900 dark:text-white">
                    <AlertTriangle className={`w-4 h-4 shrink-0 ${finding.severity === 'CRITICAL' ? 'text-rose-600 dark:text-rose-400' : 'text-amber-600 dark:text-amber-400'}`} />
                    <span className="truncate">{finding.title}</span>
                  </div>
                  <p className="text-[11px] opacity-90 leading-relaxed font-semibold">
                    {finding.subtitle}
                  </p>
                </div>
              ))}
            </div>
          ) : (
            <div className="p-4 rounded-xl bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-900/50 text-xs text-emerald-800 dark:text-emerald-300 font-semibold flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
              <span>Zero critical additives or high sugar/sodium concerns detected. Clean formulation!</span>
            </div>
          )}
        </div>

      </div>

      {/* 4. Tabbed Deep Dive Section with STICKY Tab Navigation */}
      <div className="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 shadow-xl overflow-hidden">
        
        {/* Sticky Tab Navigation (WCAG 44x44 Target Size) */}
        <div className="sticky top-16 z-30 flex border-b border-slate-200 dark:border-slate-800 bg-white/90 dark:bg-slate-900/90 backdrop-blur-md overflow-x-auto">
          <button
            onClick={() => setActiveTab('ingredients')}
            className={`min-h-[44px] flex items-center gap-2 px-6 py-3 font-bold text-xs sm:text-sm border-b-2 whitespace-nowrap transition-all focus:outline-none focus:ring-2 focus:ring-blue-500 ${
              activeTab === 'ingredients'
                ? 'border-blue-600 text-blue-600 dark:text-blue-400 bg-blue-50/40 dark:bg-blue-950/20'
                : 'border-transparent text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
            }`}
          >
            <FileText className="w-4 h-4" />
            Ingredients ({report.ingredientsList.length})
          </button>

          <button
            onClick={() => setActiveTab('nutrition')}
            className={`min-h-[44px] flex items-center gap-2 px-6 py-3 font-bold text-xs sm:text-sm border-b-2 whitespace-nowrap transition-all focus:outline-none focus:ring-2 focus:ring-blue-500 ${
              activeTab === 'nutrition'
                ? 'border-blue-600 text-blue-600 dark:text-blue-400 bg-blue-50/40 dark:bg-blue-950/20'
                : 'border-transparent text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
            }`}
          >
            <Award className="w-4 h-4" />
            Nutritional Profile
          </button>

          <button
            onClick={() => setActiveTab('regulatory')}
            className={`min-h-[44px] flex items-center gap-2 px-6 py-3 font-bold text-xs sm:text-sm border-b-2 whitespace-nowrap transition-all focus:outline-none focus:ring-2 focus:ring-blue-500 ${
              activeTab === 'regulatory'
                ? 'border-blue-600 text-blue-600 dark:text-blue-400 bg-blue-50/40 dark:bg-blue-950/20'
                : 'border-transparent text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
            }`}
          >
            <Globe className="w-4 h-4" />
            Global Regulations
          </button>

          <button
            onClick={() => setActiveTab('science')}
            className={`min-h-[44px] flex items-center gap-2 px-6 py-3 font-bold text-xs sm:text-sm border-b-2 whitespace-nowrap transition-all focus:outline-none focus:ring-2 focus:ring-blue-500 ${
              activeTab === 'science'
                ? 'border-blue-600 text-blue-600 dark:text-blue-400 bg-blue-50/40 dark:bg-blue-950/20'
                : 'border-transparent text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
            }`}
          >
            <BookOpen className="w-4 h-4" />
            Scientific Evidence
          </button>
        </div>

        {/* Tab 1: Ingredients Breakdown */}
        {activeTab === 'ingredients' && (
          <div className="p-6 space-y-4">
            <div className="flex items-center justify-between text-xs text-slate-500 dark:text-slate-400 mb-2">
              <span>Click any ingredient to view toxicology summary, INS codes, & peer-reviewed research.</span>
              <span className="font-semibold text-rose-600 dark:text-rose-400">
                {controversialIngredients.length} Additives Flagged
              </span>
            </div>

            <div className="space-y-3">
              {report.ingredientsList.map(({ ingredient, rawName, position, isControversial }) => {
                const isExpanded = expandedIngId === ingredient.id;

                return (
                  <div
                    key={ingredient.id}
                    className={`rounded-2xl border transition-all overflow-hidden ${
                      isControversial
                        ? 'border-rose-200 dark:border-rose-900/50 bg-rose-50/20 dark:bg-rose-950/10'
                        : 'border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900'
                    }`}
                  >
                    {/* Accordion Header */}
                    <div
                      onClick={() => toggleIngExpand(ingredient.id)}
                      className="p-4 flex items-center justify-between cursor-pointer hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors min-h-[44px]"
                    >
                      <div className="flex items-center gap-3">
                        <span className="w-6 h-6 rounded-full bg-slate-100 dark:bg-slate-800 flex items-center justify-center font-mono text-xs font-bold text-slate-500 shrink-0">
                          {position}
                        </span>

                        <div>
                          <div className="flex items-center gap-2">
                            <span className="font-bold text-sm text-slate-900 dark:text-white">
                              {ingredient.canonicalName}
                            </span>
                            {ingredient.eNumber && (
                              <span className="px-1.5 py-0.5 rounded bg-slate-100 dark:bg-slate-800 font-mono text-[10px] font-bold text-slate-600 dark:text-slate-300">
                                {ingredient.eNumber}
                              </span>
                            )}
                            {ingredient.insNumber && !ingredient.eNumber && (
                              <span className="px-1.5 py-0.5 rounded bg-slate-100 dark:bg-slate-800 font-mono text-[10px] font-bold text-slate-600 dark:text-slate-300">
                                INS {ingredient.insNumber}
                              </span>
                            )}
                          </div>
                          <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
                            Raw label: "{rawName}" • Category: {ingredient.category}
                          </p>
                        </div>
                      </div>

                      <div className="flex items-center gap-3">
                        <span className={`px-2.5 py-1 rounded-full text-xs font-bold ${
                          ingredient.riskLevel === 'HIGH'
                            ? 'bg-rose-100 text-rose-800 dark:bg-rose-950 dark:text-rose-300'
                            : ingredient.riskLevel === 'MEDIUM'
                            ? 'bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300'
                            : 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300'
                        }`}>
                          {ingredient.riskLevel} CONCERN
                        </span>
                        {isExpanded ? <ChevronUp className="w-4 h-4 text-slate-400" /> : <ChevronDown className="w-4 h-4 text-slate-400" />}
                      </div>
                    </div>

                    {/* Accordion Expanded Detail */}
                    {isExpanded && (
                      <div className="p-5 border-t border-slate-100 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-850/50 space-y-4 text-xs">
                        <p className="text-slate-700 dark:text-slate-300 leading-relaxed font-medium">
                          {ingredient.description}
                        </p>

                        {/* Regulatory Matrix preview */}
                        <div>
                          <span className="font-bold text-slate-500 uppercase tracking-wider text-[11px] block mb-2">
                            Global Regulatory Status
                          </span>
                          <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
                            {ingredient.regulatoryRecords.map((r) => (
                              <div
                                key={r.countryCode}
                                className="p-2.5 rounded-xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 flex items-center justify-between"
                              >
                                <span className="font-semibold text-slate-800 dark:text-slate-200">
                                  {r.flagEmoji} {r.countryCode}
                                </span>
                                <span className={`font-bold font-mono text-[10px] ${
                                  r.status === 'BANNED'
                                    ? 'text-rose-600 dark:text-rose-400'
                                    : r.status === 'RESTRICTED'
                                    ? 'text-amber-600 dark:text-amber-400'
                                    : 'text-emerald-600 dark:text-emerald-400'
                                }`}>
                                  {r.status}
                                </span>
                              </div>
                            ))}
                          </div>
                        </div>

                        {/* Research Citations */}
                        {ingredient.citations.length > 0 && (
                          <div className="pt-2">
                            <span className="font-bold text-slate-500 uppercase tracking-wider text-[11px] block mb-2">
                              Peer-Reviewed Clinical Evidence
                            </span>
                            <div className="space-y-2">
                              {ingredient.citations.map((c) => (
                                <div
                                  key={c.id}
                                  className="p-3 rounded-xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 space-y-1"
                                >
                                  <div className="font-semibold text-blue-600 dark:text-blue-400 flex items-center justify-between">
                                    <span>{c.title} ({c.year})</span>
                                    <a
                                      href={`https://doi.org/${c.doi}`}
                                      target="_blank"
                                      rel="noreferrer"
                                      className="hover:underline flex items-center gap-1 text-[10px]"
                                    >
                                      <span>DOI</span>
                                      <ExternalLink className="w-3 h-3" />
                                    </a>
                                  </div>
                                  <p className="text-slate-600 dark:text-slate-300 text-[11px]">
                                    {c.summary}
                                  </p>
                                </div>
                              ))}
                            </div>
                          </div>
                        )}

                        {/* Evidence Drawer Trigger Button */}
                        <div className="pt-2">
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              setSelectedDrawerIngredient(ingredient);
                              setDrawerRawName(rawName);
                            }}
                            className="min-h-[44px] inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs shadow-md transition-all hover:scale-105 focus:outline-none focus:ring-2 focus:ring-blue-500"
                          >
                            <BookOpen className="w-4 h-4" />
                            <span>🔬 Open Evidence & Proof Drawer</span>
                          </button>
                        </div>

                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* Tab 2: Nutritional Profile */}
        {activeTab === 'nutrition' && (
          <div className="p-6 space-y-6">
            <h3 className="font-bold text-sm text-slate-900 dark:text-white uppercase tracking-wider">
              Nutritional Breakdown per Serving ({report.nutrition.servingSize})
            </h3>

            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
              <div className="p-4 rounded-2xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-center">
                <span className="text-xs text-slate-500 font-medium block">Energy</span>
                <span className="text-2xl font-extrabold text-slate-900 dark:text-white font-mono mt-1 block">
                  {report.nutrition.calories} <span className="text-xs font-normal">kcal</span>
                </span>
              </div>

              <div className="p-4 rounded-2xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-center">
                <span className="text-xs text-slate-500 font-medium block">Added Sugars</span>
                <span className={`text-2xl font-extrabold font-mono mt-1 block ${
                  report.nutrition.addedSugarG > 5 ? 'text-rose-600 dark:text-rose-400' : 'text-emerald-600 dark:text-emerald-400'
                }`}>
                  {report.nutrition.addedSugarG} <span className="text-xs font-normal">g</span>
                </span>
                <span className="text-[10px] text-slate-400">WHO Limit: 5g</span>
              </div>

              <div className="p-4 rounded-2xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-center">
                <span className="text-xs text-slate-500 font-medium block">Sodium</span>
                <span className={`text-2xl font-extrabold font-mono mt-1 block ${
                  report.nutrition.sodiumMg > 300 ? 'text-amber-600 dark:text-amber-400' : 'text-emerald-600 dark:text-emerald-400'
                }`}>
                  {report.nutrition.sodiumMg} <span className="text-xs font-normal">mg</span>
                </span>
                <span className="text-[10px] text-slate-400">Baseline: 300mg</span>
              </div>

              <div className="p-4 rounded-2xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-center">
                <span className="text-xs text-slate-500 font-medium block">Dietary Fiber</span>
                <span className="text-2xl font-extrabold text-emerald-600 dark:text-emerald-400 font-mono mt-1 block">
                  {report.nutrition.fiberG} <span className="text-xs font-normal">g</span>
                </span>
                <span className="text-[10px] text-slate-400">Target: ≥3g</span>
              </div>
            </div>

            {/* Comprehensive Table */}
            <div className="border border-slate-200 dark:border-slate-800 rounded-2xl overflow-hidden">
              <table className="w-full text-left text-xs">
                <thead className="bg-slate-50 dark:bg-slate-850 font-bold text-slate-600 dark:text-slate-400 border-b border-slate-200 dark:border-slate-800">
                  <tr>
                    <th className="p-3 pl-4">Nutrient Factor</th>
                    <th className="p-3">Amount per Serving</th>
                    <th className="p-3">Health Impact Assessment</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 dark:divide-slate-800 font-medium">
                  <tr>
                    <td className="p-3 pl-4 font-semibold text-slate-900 dark:text-white">Total Fat</td>
                    <td className="p-3 font-mono">{report.nutrition.totalFatG} g</td>
                    <td className="p-3 text-slate-500">Lipid macro component</td>
                  </tr>
                  <tr>
                    <td className="p-3 pl-4 font-semibold text-slate-900 dark:text-white">Saturated Fat</td>
                    <td className="p-3 font-mono">{report.nutrition.saturatedFatG} g</td>
                    <td className="p-3 text-slate-500">{report.nutrition.saturatedFatG > 3 ? 'Exceeds 3g baseline threshold' : 'Within normal limits'}</td>
                  </tr>
                  <tr>
                    <td className="p-3 pl-4 font-semibold text-slate-900 dark:text-white">Trans Fat</td>
                    <td className="p-3 font-mono text-rose-600 font-bold">{report.nutrition.transFatG} g</td>
                    <td className="p-3 text-slate-500">{report.nutrition.transFatG > 0 ? 'Contains trans fatty acids (-10 pts penalty)' : 'Zero trans fat verified'}</td>
                  </tr>
                  <tr>
                    <td className="p-3 pl-4 font-semibold text-slate-900 dark:text-white">Protein</td>
                    <td className="p-3 font-mono">{report.nutrition.proteinG} g</td>
                    <td className="p-3 text-slate-500">{report.nutrition.proteinG >= 10 ? 'High protein source (+5 pts bonus)' : 'Standard protein'}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Tab 3: Global Regulatory Overview */}
        {activeTab === 'regulatory' && (
          <div className="p-6 space-y-6">
            <h3 className="font-bold text-sm text-slate-900 dark:text-white uppercase tracking-wider">
              Multi-Jurisdictional Regulatory Analysis
            </h3>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {report.globalRegulatoryOverview.map((reg) => (
                <div
                  key={reg.countryCode}
                  className="p-5 rounded-2xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 space-y-3"
                >
                  <div className="flex items-center justify-between">
                    <span className="font-extrabold text-base text-slate-900 dark:text-white">
                      {reg.flagEmoji} {reg.countryName}
                    </span>
                    <span className="text-xs font-mono font-bold text-slate-500">
                      {reg.countryCode}
                    </span>
                  </div>

                  <div className="grid grid-cols-3 gap-2 text-center text-xs">
                    <div className="p-2 rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700">
                      <span className="text-slate-400 text-[10px] block">Approved</span>
                      <span className="font-bold text-emerald-600 dark:text-emerald-400">{reg.approvedCount}</span>
                    </div>
                    <div className="p-2 rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700">
                      <span className="text-slate-400 text-[10px] block">Restricted</span>
                      <span className="font-bold text-amber-600 dark:text-amber-400">{reg.restrictedCount}</span>
                    </div>
                    <div className="p-2 rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700">
                      <span className="text-slate-400 text-[10px] block">Banned</span>
                      <span className="font-bold text-rose-600 dark:text-rose-400">{reg.bannedCount}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Tab 4: Scientific Consensus */}
        {activeTab === 'science' && (
          <div className="p-6 space-y-6">
            <div className="flex items-center justify-between">
              <h3 className="font-bold text-sm text-slate-900 dark:text-white uppercase tracking-wider">
                PubMed & Medical Literature Evidence Base
              </h3>
              <span className="text-xs text-slate-500 font-medium">
                {report.evidenceConfidence.peerReviewedStudiesCount} Peer-Reviewed Studies Indexed
              </span>
            </div>

            <div className="space-y-4">
              {report.ingredientsList.flatMap((i) => i.ingredient.citations).length > 0 ? (
                report.ingredientsList.flatMap((i) => i.ingredient.citations).map((citation) => (
                  <div
                    key={citation.id}
                    className="p-4 rounded-2xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 space-y-2 text-xs"
                  >
                    <div className="flex items-center justify-between font-bold text-slate-900 dark:text-white">
                      <span>{citation.title}</span>
                      <span className="px-2 py-0.5 rounded bg-blue-100 dark:bg-blue-950 text-blue-700 dark:text-blue-300 font-mono text-[10px]">
                        {citation.evidenceStrength} EVIDENCE
                      </span>
                    </div>
                    <p className="text-slate-600 dark:text-slate-300 leading-relaxed font-medium">
                      {citation.summary}
                    </p>
                    <div className="flex items-center gap-2 text-slate-400 text-[11px] pt-1">
                      <span>Journal: {citation.journal} ({citation.year})</span>
                      <span>•</span>
                      <a
                        href={`https://doi.org/${citation.doi}`}
                        target="_blank"
                        rel="noreferrer"
                        className="text-blue-600 dark:text-blue-400 hover:underline flex items-center gap-1 font-mono"
                      >
                        <span>DOI: {citation.doi}</span>
                        <ExternalLink className="w-3 h-3" />
                      </a>
                    </div>
                  </div>
                ))
              ) : (
                <div className="p-8 text-center text-xs text-slate-500 dark:text-slate-400">
                  Standard non-controversial ingredients. No high-concern medical alerts indexed for this formulation.
                </div>
              )}
            </div>
          </div>
        )}
      </div>

      {/* 5. Footer Collapsible Legal & Methodology Accordion */}
      <div className="rounded-2xl bg-slate-100 dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700 overflow-hidden shadow-sm">
        <button
          onClick={() => setIsDisclaimerOpen(!isDisclaimerOpen)}
          className="w-full p-4 flex items-center justify-between text-xs font-bold text-slate-700 dark:text-slate-300 hover:bg-slate-200/50 dark:hover:bg-slate-700/50 transition-colors min-h-[44px] focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <div className="flex items-center gap-2">
            <ShieldCheck className="w-4 h-4 text-blue-600 dark:text-blue-400" />
            <span>FoodFactsIndia AI Methodology & Legal Disclaimer</span>
          </div>
          <ChevronDown className={`w-4 h-4 text-slate-400 transition-transform ${isDisclaimerOpen ? 'rotate-180' : ''}`} />
        </button>

        {isDisclaimerOpen && (
          <div className="p-4 pt-0 text-xs text-slate-600 dark:text-slate-300 space-y-2 border-t border-slate-200/60 dark:border-slate-700/60">
            <p className="leading-relaxed text-[11px] pt-2">
              FoodFactsIndia AI provides verified food information and cross-country regulatory comparisons for consumer awareness. 
              It is not medical advice or legal advice for manufacturers. Regulatory statuses and formulations may change over time. 
              Always verify against the physical product package label and official regulatory authorities (FSSAI, EFSA, FDA, WHO).
            </p>
          </div>
        )}
      </div>

      {/* Score Breakdown Modal */}
      <ScoreBreakdownModal
        isOpen={isMethodologyOpen}
        onClose={() => setIsMethodologyOpen(false)}
        productName={report.productName}
        score={report.deterministicScore}
        breakdown={report.scoreBreakdown}
      />

      {/* Proof-First Evidence Drawer Modal */}
      <EvidenceDrawerModal
        isOpen={selectedDrawerIngredient !== null}
        onClose={() => setSelectedDrawerIngredient(null)}
        ingredient={selectedDrawerIngredient}
        rawName={drawerRawName}
      />

      {/* International Ratings Methodology Modal */}
      <InternationalMethodologyModal
        isOpen={isIntlModalOpen}
        onClose={() => setIsIntlModalOpen(false)}
        ratings={report.internationalRatings}
      />

    </div>
  );
};

