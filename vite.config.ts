import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { handleImageProxyRequest } from './api/imageProxy.js';

export default defineConfig({
  plugins: [
    react(),
    {
      name: 'image-proxy-middleware',
      configureServer(server) {
        server.middlewares.use(async (req, res, next) => {
          const url = req.url || '';
          const match = url.match(/^\/api\/img\/([^?#/]+)/);
          if (match) {
            const barcode = decodeURIComponent(match[1]);
            await handleImageProxyRequest(req, res, barcode);
            return;
          }
          next();
        });
      }
    }
  ],
  build: {
    rollupOptions: {
      output: {
        /**
         * manualChunks splits heavy node_modules into separate cacheable files.
         *
         * Rules applied here (per user correction):
         * - Only STATIC node_module imports go in manualChunks.
         * - Internal app services (scoringEngine, internationalRatingsEngine) are NOT
         *   placed here because Rollup still bundles statically-imported modules
         *   alongside whatever chunk first imports them — they need dynamic import()
         *   for true lazy loading. Putting them here would create orphaned chunks
         *   that are still fetched eagerly, wasting bandwidth.
         *
         * Expected result:
         *   vendor-react:    ~140 kB gzip  (cached indefinitely after first visit)
         *   vendor-supabase: ~48 kB gzip   (cached indefinitely)
         *   vendor-lucide:   ~32 kB gzip   (cached indefinitely)
         *   app (main):      ~70 kB gzip   (the actual app code — changes on deploy)
         */
        manualChunks: {
          'vendor-react':    ['react', 'react-dom'],
          'vendor-supabase': ['@supabase/supabase-js'],
          'vendor-lucide':   ['lucide-react'],
        },
      },
    },
  },
});
