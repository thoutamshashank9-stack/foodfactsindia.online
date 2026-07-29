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
});
