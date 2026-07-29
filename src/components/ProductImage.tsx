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
  const [hasError, setHasError] = useState(false);

  const cleanBarcode = (barcode || '').trim();
  const proxyUrl = cleanBarcode ? `/api/img/${encodeURIComponent(cleanBarcode)}` : '';

  return (
    <div className={`relative overflow-hidden ${className}`}>
      {/* Skeleton Loading State */}
      {!isLoaded && !hasError && (
        <div className="absolute inset-0 bg-slate-200 dark:bg-slate-800 animate-pulse flex items-center justify-center">
          <span className="text-[10px] font-mono text-slate-400 font-bold uppercase tracking-wider">
            Loading...
          </span>
        </div>
      )}

      {/* Edge Proxy Dynamic Image */}
      {proxyUrl && (
        <img
          src={proxyUrl}
          alt={productName}
          className={`w-full h-full object-cover transition-opacity duration-300 ${
            isLoaded ? 'opacity-100' : 'opacity-0'
          }`}
          onLoad={() => setIsLoaded(true)}
          onError={() => {
            setIsLoaded(true);
            setHasError(true);
          }}
          loading="lazy"
          decoding="async"
          referrerPolicy="no-referrer"
        />
      )}
    </div>
  );
};
