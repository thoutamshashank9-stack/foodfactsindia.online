import { handleImageProxyRequest } from '../../imageProxy.js';

export default async function handler(req, res) {
  const barcode = req.query.barcode || (req.url ? req.url.split('?')[0].split('/').pop() : '');
  await handleImageProxyRequest(req, res, barcode);
}
