import React, { useState } from 'react';
import { ShieldAlert, ChevronDown, ChevronUp } from 'lucide-react';
import { Card } from '../Card';
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

  return (
    <Card className="space-y-4">
      <h2 className="font-serif text-lg font-bold text-stone-900 dark:text-stone-100 flex items-center gap-2">
        <ShieldAlert className="w-5 h-5 text-amber-700 dark:text-amber-500" />
        <span>Key Concerns & Findings ({findings.length})</span>
      </h2>

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
    </Card>
  );
};
