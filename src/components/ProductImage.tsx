import React, { useState } from 'react';

interface ProductImageProps {
  barcode: string;
  productName: string;
  className?: string;
  fallbackIconSize?: number;
}

export const ProductImage: React.FC<ProductImageProps> = ({
  barcode,
  productName,
  className = 'w-32 h-32 rounded-2xl object-cover border-2 border-slate-200 dark:border-slate-700 shadow-xl shrink-0'
}) => {
  const [isLoaded, setIsLoaded] = useState(false);
  const [errorStage, setErrorStage] = useState<number>(0);

  const cleanBarcode = (barcode || '').trim();
  
  // Construct fallback URLs in sequence if edge proxy returns 404
  const getImageUrl = () => {
    if (errorStage === 0) {
      return cleanBarcode ? `/api/img/${encodeURIComponent(cleanBarcode)}` : '';
    }
    if (errorStage === 1 && cleanBarcode.length >= 8) {
      // Direct Open Food Facts CDN fallback path
      const codeStr = cleanBarcode.padStart(13, '0');
      if (codeStr.length === 13) {
        const p1 = codeStr.slice(0, 3);
        const p2 = codeStr.slice(3, 6);
        const p3 = codeStr.slice(6, 9);
        const p4 = codeStr.slice(9);
        return `https://images.openfoodfacts.org/images/products/${p1}/${p2}/${p3}/${p4}/front_en.3.400.jpg`;
      }
    }
    return '';
  };

  const currentSrc = getImageUrl();

  return (
    <div className={`relative overflow-hidden ${className}`}>
      {/* Skeleton Loading State */}
      {!isLoaded && errorStage < 2 && (
        <div className="absolute inset-0 bg-slate-200 dark:bg-slate-800 animate-pulse flex items-center justify-center">
          <span className="text-[10px] font-mono text-slate-400 font-bold uppercase tracking-wider">
            Loading...
          </span>
        </div>
      )}

      {/* Edge Proxy & CDN Dynamic Image */}
      {currentSrc && errorStage < 2 ? (
        <img
          src={currentSrc}
          alt={productName}
          className={`w-full h-full object-cover transition-opacity duration-300 ${
            isLoaded ? 'opacity-100' : 'opacity-0'
          }`}
          onLoad={() => setIsLoaded(true)}
          onError={() => {
            setIsLoaded(false);
            setErrorStage(prev => prev + 1);
          }}
          loading="lazy"
          decoding="async"
          referrerPolicy="no-referrer"
        />
      ) : (
        /* Final High-End Vector Fallback */
        <div className="w-full h-full bg-gradient-to-br from-slate-100 to-slate-200 dark:from-slate-800 dark:to-slate-850 flex flex-col items-center justify-center text-slate-400 dark:text-slate-500 p-2 text-center select-none">
          <svg className="w-8 h-8 mb-1 opacity-70" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <rect x="3" y="3" width="18" height="18" rx="4" />
            <path d="M7 8h2v8H7zM11 8h1v8h-1zM14 8h3v8h-3z" fill="currentColor" opacity="0.4" />
          </svg>
          <span className="text-[10px] font-bold text-slate-500 dark:text-slate-400 line-clamp-1 leading-tight uppercase tracking-wider">
            {productName || 'Food Item'}
          </span>
        </div>
      )}
    </div>
  );
};
