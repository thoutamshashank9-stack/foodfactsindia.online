import http from 'http';
import { handleImageProxyRequest, validateBarcode, generateSvgFallback, fetchUpstreamOffImage } from '../api/imageProxy.js';

function createMockResponse() {
  let statusCode = 200;
  const headers = {};
  let body = '';

  return {
    get statusCode() { return statusCode; },
    set statusCode(val) { statusCode = val; },
    setHeader(key, val) { headers[key.toLowerCase()] = val; },
    getHeader(key) { return headers[key.toLowerCase()]; },
    end(data) {
      if (data) body += data;
    },
    get body() { return body; },
    get headers() { return headers; }
  };
}

async function runTests() {
  console.log("================================================================================");
  printHeader("FOODLENS AI EDGE IMAGE PROXY AUTOMATED TEST SUITE");
  console.log("================================================================================");

  let passed = 0;
  let failed = 0;

  // Test Case 1: Valid Barcode with Image (5449000000996 - Coca-Cola)
  console.log("\n[TEST 1] Valid Barcode with Image (5449000000996)...");
  try {
    const res1 = createMockResponse();
    await handleImageProxyRequest({}, res1, '5449000000996');

    if (res1.statusCode === 302) {
      const location = res1.getHeader('location');
      const cacheControl = res1.getHeader('cache-control') || '';
      console.log(`  ✓ Status: 302 Found`);
      console.log(`  ✓ Redirect Location: ${location}`);
      console.log(`  ✓ Cache-Control: ${cacheControl}`);

      if (location && location.startsWith('http') && cacheControl.includes('s-maxage=31536000')) {
        console.log("  ✅ TEST 1 PASSED!");
        passed++;
      } else {
        console.log("  ❌ TEST 1 FAILED: Invalid headers or location.");
        failed++;
      }
    } else {
      console.log(`  ❌ TEST 1 FAILED: Expected 302 Found, got ${res1.statusCode}`);
      failed++;
    }
  } catch (e) {
    console.log(`  ❌ TEST 1 EXCEPTION: ${e.message}`);
    failed++;
  }

  // Test Case 2: Valid Barcode without Image (0000000000000)
  console.log("\n[TEST 2] Valid Barcode without Image (0000000000000)...");
  try {
    const res2 = createMockResponse();
    await handleImageProxyRequest({}, res2, '0000000000000');

    const contentType = res2.getHeader('content-type') || '';
    const cacheControl = res2.getHeader('cache-control') || '';
    const hasSvgText = res2.body.includes('<svg') && res2.body.includes('GTIN: 0000000000000');

    console.log(`  ✓ Status: ${res2.statusCode}`);
    console.log(`  ✓ Content-Type: ${contentType}`);
    console.log(`  ✓ Cache-Control: ${cacheControl}`);
    console.log(`  ✓ Contains SVG & GTIN text: ${hasSvgText}`);

    if (res2.statusCode === 200 && contentType.includes('image/svg+xml') && hasSvgText && cacheControl.includes('s-maxage=31536000')) {
      console.log("  ✅ TEST 2 PASSED!");
      passed++;
    } else {
      console.log("  ❌ TEST 2 FAILED: Expected 200 OK with SVG markup.");
      failed++;
    }
  } catch (e) {
    console.log(`  ❌ TEST 2 EXCEPTION: ${e.message}`);
    failed++;
  }

  // Test Case 3: Invalid Barcode Format (abc1234)
  console.log("\n[TEST 3] Invalid Barcode Format (abc1234)...");
  try {
    const res3 = createMockResponse();
    await handleImageProxyRequest({}, res3, 'abc1234');

    console.log(`  ✓ Status: ${res3.statusCode}`);
    console.log(`  ✓ Body: ${res3.body}`);

    if (res3.statusCode === 400 && res3.body.includes('Invalid barcode format')) {
      console.log("  ✅ TEST 3 PASSED!");
      passed++;
    } else {
      console.log(`  ❌ TEST 3 FAILED: Expected 400 Bad Request, got ${res3.statusCode}`);
      failed++;
    }
  } catch (e) {
    console.log(`  ❌ TEST 3 EXCEPTION: ${e.message}`);
    failed++;
  }

  console.log("\n================================================================================");
  console.log(`TEST SUITE SUMMARY: ${passed} Passed, ${failed} Failed`);
  console.log("================================================================================");

  if (failed > 0) {
    process.exit(1);
  }
}

function printHeader(title) {
  console.log(`  ${title}`);
}

runTests();
