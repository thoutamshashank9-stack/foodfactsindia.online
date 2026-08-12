import React, { useState } from 'react';

export interface ProductImageProps {
  src?: string | null;
  barcode?: string;
  productName: string;
  className?: string;
  size?: 'small' | 'medium' | 'full';
}

export const ProductImage: React.FC<ProductImageProps> = ({
  src,
  barcode,
  productName,
  className = 'w-32 h-32 rounded-2xl object-cover border-2 border-slate-200 dark:border-slate-700 shadow-sm shrink-0',
  size = 'medium'
}) => {
  const [isLoaded, setIsLoaded] = useState(false);
  const [errorStage, setErrorStage] = useState<number>(0);

  const cleanBarcode = (barcode || '').trim();
  const directSrc = (src || '').trim();

  // Sequence:
  // Stage 0: Direct provided URL (if present) or Edge Proxy
  // Stage 1: Direct OFF CDN URL if barcode is valid
  // Stage 2: Fallback SVG placeholder
  const getImageUrl = (): string => {
    if (errorStage === 0) {
      if (directSrc) return directSrc;
      if (cleanBarcode) return `/api/img/${encodeURIComponent(cleanBarcode)}`;
      return '';
    }
    if (errorStage === 1 && cleanBarcode.length >= 8) {
      const codeStr = cleanBarcode.padStart(13, '0');
      if (codeStr.length === 13) {
        const p1 = codeStr.slice(0, 3);
        const p2 = codeStr.slice(3, 6);
        const p3 = codeStr.slice(6, 9);
        const p4 = codeStr.slice(9);
        const sizeSuffix = size === 'small' ? '.200.jpg' : '.400.jpg';
        return `https://images.openfoodfacts.org/images/products/${p1}/${p2}/${p3}/${p4}/front_en.3${sizeSuffix}`;
      }
    }
    return '';
  };

  const currentSrc = getImageUrl();

  return (
    <div className={`relative overflow-hidden ${className}`}>
      {/* Skeleton Loading State */}
      {!isLoaded && errorStage < 2 && currentSrc && (
        <div className="absolute inset-0 bg-slate-100 dark:bg-slate-800 animate-pulse flex items-center justify-center">
          <span className="text-[10px] font-mono text-slate-400 font-bold uppercase tracking-wider">
            Loading...
          </span>
        </div>
      )}

      {/* Render Image if URL exists and has not failed all stages */}
      {currentSrc && errorStage < 2 ? (
        <img
          src={currentSrc}
          alt={productName || 'Food Product'}
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
        /* Vector Placeholder when no image or broken link */
        <div className="w-full h-full bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-800 dark:to-slate-850 flex flex-col items-center justify-center text-slate-400 dark:text-slate-500 p-2 text-center select-none border border-slate-200/50 dark:border-slate-700/50 rounded-2xl">
          <span className="text-2xl mb-1">🍽️</span>
          <span className="text-[10px] font-bold text-slate-500 dark:text-slate-400 line-clamp-1 leading-tight uppercase tracking-wider">
            {productName || 'No Image Yet'}
          </span>
        </div>
      )}
    </div>
  );
};

export default ProductImage;
