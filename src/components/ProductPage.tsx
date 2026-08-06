import React from 'react';
import { ProductPageResponse } from '../types/productPageResponse';
import { ProductPageProvider } from '../context/ProductPublicationContext';
import { UnverifiedProductStubView } from './UnverifiedProductStubView';
import { TransparencyReportView } from './TransparencyReportView';

interface ProductPageProps {
  data: ProductPageResponse;
  onBack?: () => void;
  onSelectAlternative?: (barcode: string) => void;
}

export const ProductPage: React.FC<ProductPageProps> = ({ data, onBack, onSelectAlternative }) => {
  return (
    <ProductPageProvider pageState={data.pageState}>
      {(() => {
        switch (data.pageState) {
          case 'processing':
            return (
              <UnverifiedProductStubView
                report={{
                  productId: data.product.productId,
                  productName: data.product.productName,
                  brand: data.product.brand,
                  manufacturer: data.product.manufacturer || '',
                  category: data.product.category,
                  barcode: data.product.barcode,
                  packageSize: data.product.packageSize,
                  servingSize: data.product.servingSize,
                  pageState: data.pageState,
                  stateMessage: `${data.progress.step} (${data.progress.percent}%)`,
                  deterministicScore: 0,
                  scoreBreakdown: [],
                  isScoreWithheld: true,
                  scoreWithheldReason: `${data.progress.step} (${data.progress.percent}%)`,
                  executiveSummary: {
                    grade: 'F',
                    verdictTitle: 'Verification Pending',
                    keyTakeaways: [],
                    riskSummaryText: 'Package evidence pending verification.',
                    processingNovaClass: undefined
                  },
                  ingredientsList: [],
                  nutrition: { servingSize: '100g', calories: 0, totalFatG: 0, saturatedFatG: 0, transFatG: 0, sodiumMg: 0, totalCarbsG: 0, fiberG: 0, totalSugarG: 0, addedSugarG: 0, proteinG: 0 },
                  globalRegulatoryOverview: [],
                  evidenceConfidence: { confidenceScore: 0, peerReviewedStudiesCount: 0, regulatoryBodiesCount: 0, lastUpdated: 'Pending' }
                }}
                onBack={onBack}
                onSelectAlternative={onSelectAlternative}
              />
            );

          case 'awaiting_images':
          case 'insufficient_data':
          case 'needs_review':
            return (
              <UnverifiedProductStubView
                report={{
                  productId: data.product.productId,
                  productName: data.product.productName,
                  brand: data.product.brand,
                  manufacturer: data.product.manufacturer || '',
                  category: data.product.category,
                  barcode: data.product.barcode,
                  packageSize: data.product.packageSize,
                  servingSize: data.product.servingSize,
                  pageState: data.pageState,
                  stateMessage: data.stub.message,
                  deterministicScore: 0,
                  scoreBreakdown: [],
                  isScoreWithheld: true,
                  scoreWithheldReason: data.stub.message,
                  executiveSummary: {
                    grade: 'F',
                    verdictTitle: 'Verification Pending',
                    keyTakeaways: [],
                    riskSummaryText: 'Package evidence pending verification.',
                    processingNovaClass: undefined
                  },
                  ingredientsList: [],
                  nutrition: { servingSize: '100g', calories: 0, totalFatG: 0, saturatedFatG: 0, transFatG: 0, sodiumMg: 0, totalCarbsG: 0, fiberG: 0, totalSugarG: 0, addedSugarG: 0, proteinG: 0 },
                  globalRegulatoryOverview: [],
                  evidenceConfidence: { confidenceScore: 0, peerReviewedStudiesCount: 0, regulatoryBodiesCount: 0, lastUpdated: 'Pending' }
                }}
                onBack={onBack}
                onSelectAlternative={onSelectAlternative}
              />
            );

          case 'verified_published':
            return (
              <TransparencyReportView
                report={data.verifiedReport}
                onBackToSearch={onBack}
              />
            );

          default: {
            const _exhaustive: never = data;
            return null;
          }
        }
      })()}
    </ProductPageProvider>
  );
};
