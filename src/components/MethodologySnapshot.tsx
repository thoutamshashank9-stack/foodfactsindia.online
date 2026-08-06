import React from 'react';

interface MethodologySnapshotProps {
  onGoToMethodology?: () => void;
}

export const MethodologySnapshot: React.FC<MethodologySnapshotProps> = ({ onGoToMethodology }) => {
  return (
    <section className="py-10 border-b border-stone-200 dark:border-stone-800/80">
      <div className="max-w-3xl mx-auto px-4 text-center space-y-4">
        <h2 className="font-serif text-2xl sm:text-3xl font-semibold text-stone-900 dark:text-stone-100">
          How scoring works
        </h2>

        <p className="text-sm sm:text-base text-stone-600 dark:text-stone-300 leading-relaxed max-w-2xl mx-auto">
          Scores reflect declared nutrition, additive profiles, processing signals, and regulatory context. Incomplete or low-confidence data should not be published as verified reports.
        </p>

        {onGoToMethodology && (
          <div className="pt-2">
            <button
              onClick={onGoToMethodology}
              className="text-xs font-medium text-teal-800 dark:text-teal-400 hover:underline"
            >
              Read full regulatory & scoring methodology &rarr;
            </button>
          </div>
        )}
      </div>
    </section>
  );
};
