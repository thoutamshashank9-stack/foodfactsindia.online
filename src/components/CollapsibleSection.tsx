import React, { useState } from 'react';
import { ChevronDown, ChevronUp } from 'lucide-react';
import { Card } from './Card';

interface CollapsibleSectionProps {
  title?: React.ReactNode;
  collapsedPreview: React.ReactNode;
  children: React.ReactNode;
  defaultOpen?: boolean;
}

export const CollapsibleSection: React.FC<CollapsibleSectionProps> = ({
  title,
  collapsedPreview,
  children,
  defaultOpen = false,
}) => {
  const [isOpen, setIsOpen] = useState(defaultOpen);

  return (
    <Card className="overflow-hidden p-0 border border-stone-200 dark:border-stone-800 bg-white dark:bg-stone-900 transition-colors">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full text-left p-4 focus:outline-none flex flex-col gap-2 hover:bg-stone-50 dark:hover:bg-stone-850/50 transition-colors"
      >
        <div className="flex items-center justify-between w-full">
          <div className="flex-1 pr-4">
            {title && (
              <h3 className="text-sm font-bold text-stone-900 dark:text-stone-100 font-serif mb-1">
                {title}
              </h3>
            )}
            <div className={`transition-all duration-300 ${isOpen ? 'opacity-0 h-0 hidden' : 'opacity-100 h-auto'}`}>
              {collapsedPreview}
            </div>
          </div>
          <div className="shrink-0 text-stone-400 dark:text-stone-500">
            {isOpen ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}
          </div>
        </div>
      </button>

      <div
        className={`grid transition-all duration-300 ease-in-out ${
          isOpen ? 'grid-rows-[1fr] opacity-100' : 'grid-rows-[0fr] opacity-0'
        }`}
      >
        <div className="overflow-hidden">
          <div className="p-4 pt-0 border-t border-stone-100 dark:border-stone-800 mt-2">
            {children}
          </div>
        </div>
      </div>
    </Card>
  );
};
