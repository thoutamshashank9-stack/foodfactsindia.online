import { TransparencyReport } from './index';

export interface ProductIdentity {
  productId: string;
  barcode: string;
  productName: string;
  brand: string;
  manufacturer?: string;
  category: string;
  packageSize: string;
  servingSize: string;
  imageUrl?: string;
}

export interface StubData {
  message: string;
  detail?: string;
}

export interface ProgressData {
  percent: number;
  step: string;
}

export type ProductPageResponse = 
  | { pageState: "awaiting_images"; product: ProductIdentity; stub: StubData } 
  | { pageState: "processing"; product: ProductIdentity; progress: ProgressData } 
  | { pageState: "insufficient_data"; product: ProductIdentity; stub: StubData; reviewReasons?: string[] } 
  | { pageState: "needs_review"; product: ProductIdentity; stub: StubData; reviewReasons: string[] } 
  | { pageState: "verified_published"; product: ProductIdentity; verifiedReport: TransparencyReport };
