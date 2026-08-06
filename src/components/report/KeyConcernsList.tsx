import React, { useState } from 'react';
import { ShieldAlert, ChevronDown, ChevronUp, CheckCircle2 } from 'lucide-react';
import { CollapsibleSection } from '../CollapsibleSection';
import { Badge } from '../Badge';

interface Finding {
  id: string;
  title: string;
  subtitle: string;
  severity: 'CRITICAL' | 'WARNING' | 'INFO';
}

interface KeyConcernsListProps {
  findings: Finding[];
}

export const KeyConcernsList: React.FC<KeyConcernsListProps> = ({ findings }) => {
  const [expandedId, setExpandedId] = useState<string | null>(null);

  const getSeverityVariant = (sev: Finding['severity']): 'danger' | 'warning' | 'info' => {
    if (sev === 'CRITICAL') return 'danger';
    if (sev === 'WARNING') return 'warning';
    return 'info';
  };

  const criticalCount = findings.filter(f => f.severity === 'CRITICAL').length;
  const warningCount = findings.filter(f => f.severity === 'WARNING').length;

  return (
    <div className="w-full">
      <CollapsibleSection
        title={
          <div className="flex items-center gap-2">
            <ShieldAlert className="w-4 h-4 text-amber-600 shrink-0" />
            <span>Key Concerns & Findings</span>
          </div>
        }
        collapsedPreview={
          <div className="flex items-center gap-2 mt-2">
            {findings.length > 0 ? (
              <div className="flex items-center gap-2 flex-wrap">
                {criticalCount > 0 && (
                  <Badge label={`${criticalCount} Critical`} variant="danger" />
                )}
                {warningCount > 0 && (
                  <Badge label={`${warningCount} Warning${warningCount !== 1 ? 's' : ''}`} variant="warning" />
                )}
                {criticalCount === 0 && warningCount === 0 && findings.length > 0 && (
                  <Badge label={`${findings.length} Info`} variant="info" />
                )}
                <span className="text-sm font-medium text-stone-600 dark:text-stone-400">
                  Click to view details
                </span>
              </div>
            ) : (
              <div className="px-3 py-1 rounded font-bold text-sm bg-emerald-100 dark:bg-emerald-950/60 text-emerald-800 dark:text-emerald-300 flex items-center gap-1.5">
                <CheckCircle2 className="w-4 h-4" />
                <span>No major concerns found</span>
              </div>
            )}
          </div>
        }
      >
        <div className="pt-2">
          {findings.length === 0 ? (
            <p className="text-xs text-stone-500 dark:text-stone-400">
              No high-risk regulatory concerns or WHO nutrient benchmark violations flagged.
            </p>
          ) : (
            <div className="space-y-2">
              {findings.map((f) => {
                const isExpanded = expandedId === f.id;
                return (
                  <div
                    key={f.id}
                    className="border border-stone-200 dark:border-stone-850 rounded-lg overflow-hidden"
                  >
                    <button
                      onClick={() => setExpandedId(isExpanded ? null : f.id)}
                      className="w-full p-3.5 text-left bg-stone-50/50 dark:bg-stone-850 hover:bg-stone-100/50 transition-colors flex items-start justify-between gap-3"
                    >
                      <div className="space-y-1">
                        <div className="flex items-center gap-2 flex-wrap">
                          <Badge label={f.severity} variant={getSeverityVariant(f.severity)} />
                          <span className="font-serif text-sm font-semibold text-stone-900 dark:text-stone-100 leading-tight">
                            {f.title}
                          </span>
                        </div>
                      </div>
                      <div className="shrink-0 mt-0.5 text-stone-400">
                        {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                      </div>
                    </button>

                    {isExpanded && (
                      <div className="p-3.5 bg-white dark:bg-stone-900 border-t border-stone-200 dark:border-stone-850 text-xs text-stone-600 dark:text-stone-300 leading-relaxed">
                        {f.subtitle}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </CollapsibleSection>
    </div>
  );
};
