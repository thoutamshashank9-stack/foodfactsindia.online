import React, { useState } from 'react';
import { getOptimizedOFFImageUrl } from '../services/offImages';

export interface ProductImageProps {
  src?: string | null;
  barcode?: string;
  productName: string;
  className?: string;
  size?: 100 | 200 | 400 | 'full';
}

export const ProductImage: React.FC<ProductImageProps> = ({
  src,
  barcode,
  productName,
  className = 'w-24 h-24 rounded-xl object-cover border border-slate-200 dark:border-slate-700 shadow-sm shrink-0',
  size = 200
}) => {
  const [isLoaded, setIsLoaded] = useState(false);
  const [errorStage, setErrorStage] = useState<number>(0);

  const cleanBarcode = (barcode || '').trim();
  const directSrc = (src || '').trim();
  const formattedSize = typeof size === 'number' ? size : 200;

  // Fallback 1: UI Avatars placeholder
  const avatarFallbackUrl = `https://ui-avatars.com/api/?name=${encodeURIComponent(productName || 'Food Item')}&background=E2E8F0&color=64748B&size=${formattedSize}&bold=true`;

  // Determine current image URL based on error resolution stage
  const getDisplayUrl = (): string => {
    if (errorStage === 0) {
      if (directSrc) return directSrc;
      if (cleanBarcode) {
        const offUrl = getOptimizedOFFImageUrl(cleanBarcode, formattedSize);
        if (offUrl) return offUrl;
      }
      return avatarFallbackUrl;
    }
    if (errorStage === 1) {
      if (cleanBarcode) return `/api/img/${encodeURIComponent(cleanBarcode)}`;
      return avatarFallbackUrl;
    }
    return avatarFallbackUrl;
  };

  const displayUrl = getDisplayUrl();

  return (
    <div className={`relative overflow-hidden ${className} bg-slate-100 dark:bg-slate-800`}>
      {/* Skeleton Loading Spinner */}
      {!isLoaded && errorStage < 2 && (
        <div className="absolute inset-0 flex items-center justify-center bg-slate-100 dark:bg-slate-800">
          <div className="w-6 h-6 border-2 border-emerald-200 border-t-emerald-600 rounded-full animate-spin"></div>
        </div>
      )}

      {/* Optimized Image Tag */}
      <img
        src={displayUrl}
        alt={productName || 'Food Product'}
        loading="lazy"
        decoding="async"
        onLoad={() => setIsLoaded(true)}
        onError={() => {
          setIsLoaded(false);
          setErrorStage(prev => prev + 1);
        }}
        className={`w-full h-full object-cover transition-opacity duration-300 ${
          isLoaded ? 'opacity-100' : 'opacity-0'
        }`}
        referrerPolicy="no-referrer"
      />
    </div>
  );
};

export default ProductImage;
