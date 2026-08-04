import React, { createContext, useContext } from 'react';
import { ProductPageResponse } from '../types/productPageResponse';

interface ProductContextType {
  pageState: ProductPageResponse["pageState"];
}

const ProductContext = createContext<ProductContextType>({ pageState: 'insufficient_data' });

export const ProductPageProvider: React.FC<{ pageState: ProductPageResponse["pageState"]; children: React.ReactNode }> = ({
  pageState,
  children,
}) => {
  return <ProductContext.Provider value={{ pageState }}>{children}</ProductContext.Provider>;
};

export const useProductPublication = () => useContext(ProductContext);
