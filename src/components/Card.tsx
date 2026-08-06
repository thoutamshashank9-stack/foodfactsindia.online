import React from 'react';

interface CardProps {
  children: React.ReactNode;
  className?: string;
  onClick?: () => void;
}

export const Card: React.FC<CardProps> = ({ children, className = '', onClick }) => {
  return (
    <div
      onClick={onClick}
      className={`bg-white dark:bg-stone-900 border border-stone-200 dark:border-stone-850 rounded-xl p-5 shadow-sm transition-all ${
        onClick ? 'cursor-pointer hover:border-stone-300 dark:hover:border-stone-750' : ''
      } ${className}`}
    >
      {children}
    </div>
  );
};
