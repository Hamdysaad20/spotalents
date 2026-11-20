/**
 * Unit & Security Test Suite for /api/leads
 * Run with: node scripts/test_lead_api.js
 */

const assert = require('assert');
const handler = require('../api/leads');

// Mock Request & Response helpers
function createMockReqRes(options = {}) {
  const req = {
    method: options.method || 'POST',
    headers: {
      'content-type': 'application/json',
      'user-agent': 'TestAgent/1.0',
      'x-forwarded-for': options.ip || '192.168.1.100',
      origin: options.origin || 'https://spotalents.com',
      ...(options.headers || {})
    },
    body: options.body || {},
    socket: { remoteAddress: options.ip || '192.168.1.100' }
  };

  const headersSent = {};
  let statusCode = 200;
  let responseBody = null;

  const res = {
    setHeader: (key, value) => {
      headersSent[key.toLowerCase()] = value;
    },
    getHeader: (key) => headersSent[key.toLowerCase()],
    status: (code) => {
      statusCode = code;
      return res;
    },
    json: (data) => {
      responseBody = data;
      return res;
    },
    end: () => res
  };

  return {
    req,
    res,
    getStatusCode: () => statusCode,
    getBody: () => responseBody,
    getHeaders: () => headersSent
  };
}

async function runTests() {
  console.log('--- Starting Spotalents Security & API Tests ---\n');

  // Test 1: Method Restriction (GET should be rejected with 405)
  {
    const { req, res, getStatusCode, getBody } = createMockReqRes({ method: 'GET', ip: '10.0.0.1' });
    await handler(req, res);
    assert.strictEqual(getStatusCode(), 405, 'Expected 405 Method Not Allowed for GET');
    assert.strictEqual(getBody().success, false);
    console.log('✓ Test 1 Passed: GET method rejected with 405');
  }

  // Test 2: Validation Check (Missing first name and invalid email)
  {
    const { req, res, getStatusCode, getBody } = createMockReqRes({
      method: 'POST',
      ip: '10.0.0.2',
      body: {
        firstName: '',
        lastName: 'Smith',
        companyName: 'Acme Corp',
        email: 'invalid-email-address',
        _formRenderTime: Date.now() - 5000
      }
    });
    await handler(req, res);
    assert.strictEqual(getStatusCode(), 400, 'Expected 400 Bad Request for invalid inputs');
    assert.strictEqual(getBody().success, false);
    assert(getBody().details.length >= 2, 'Expected at least 2 validation errors');
    console.log('✓ Test 2 Passed: Missing first name & invalid email rejected with 400');
  }

  // Test 3: Anti-Spam Honeypot Trap
  {
    const { req, res, getStatusCode, getBody } = createMockReqRes({
      method: 'POST',
      ip: '10.0.0.3',
      body: {
        firstName: 'BotFirst',
        lastName: 'BotLast',
        companyName: 'Spam Inc',
        email: 'bot@spam.com',
        _hp_company_url: 'http://spam-link.com', // Honeypot filled!
        _formRenderTime: Date.now() - 5000
      }
    });
    await handler(req, res);
    // Honeypot returns silent 200 to trick bot scrapers
    assert.strictEqual(getStatusCode(), 200, 'Expected 200 silent success for honeypot');
    assert.strictEqual(getBody().success, true);
    console.log('✓ Test 3 Passed: Bot honeypot trapped cleanly with silent success');
  }

  // Test 4: Anti-Spam Submission Timing Check (Superhuman speed < 1200ms)
  {
    const { req, res, getStatusCode, getBody } = createMockReqRes({
      method: 'POST',
      ip: '10.0.0.4',
      body: {
        firstName: 'FastBot',
        lastName: 'Speedy',
        companyName: 'Fast Inc',
        email: 'fast@bot.com',
        _formRenderTime: Date.now() - 400 // Submitted in 400ms!
      }
    });
    await handler(req, res);
    assert.strictEqual(getStatusCode(), 200, 'Expected silent drop for sub-second submission');
    assert.strictEqual(getBody().success, true);
    console.log('✓ Test 4 Passed: Sub-human submission speed detected and neutralized');
  }

  // Test 5: Graceful 503 Handling when Supabase is not yet configured
  {
    // Ensure no supabase env vars
    delete process.env.SUPABASE_URL;
    delete process.env.SUPABASE_SERVICE_ROLE_KEY;
    delete process.env.SUPABASE_ANON_KEY;

    const { req, res, getStatusCode, getBody } = createMockReqRes({
      method: 'POST',
      ip: '10.0.0.5',
      body: {
        firstName: 'John',
        lastName: 'Doe',
        companyName: 'Valid Corp',
        email: 'john@validcorp.com',
        projectDetails: 'We need high performance engineering pods.',
        _formRenderTime: Date.now() - 5000
      }
    });
    await handler(req, res);
    assert.strictEqual(getStatusCode(), 503, 'Expected 503 Service Unavailable when DB is unconfigured');
    assert.strictEqual(getBody().success, false);
    console.log('✓ Test 5 Passed: Graceful 503 degradation with clean user message');
  }

  // Test 6: Rate Limiting Enforcement (Exceeding 5 requests from same IP)
  {
    const testIp = '198.51.100.42';
    for (let i = 0; i < 5; i++) {
      const { req, res } = createMockReqRes({
        method: 'POST',
        ip: testIp,
        body: { firstName: '' } // 400 error, but still counted
      });
      await handler(req, res);
    }

    // 6th request from same IP
    const { req, res, getStatusCode } = createMockReqRes({
      method: 'POST',
      ip: testIp,
      body: { firstName: '' }
    });
    await handler(req, res);
    assert.strictEqual(getStatusCode(), 429, 'Expected 429 Too Many Requests after 5 requests');
    console.log('✓ Test 6 Passed: Rate limiter enforced 429 Too Many Requests');
  }

  // Test 7: Security Headers Present
  {
    const { req, res, getHeaders } = createMockReqRes({ method: 'OPTIONS' });
    await handler(req, res);
    const headers = getHeaders();
    assert.strictEqual(headers['x-content-type-options'], 'nosniff');
    assert.strictEqual(headers['cache-control'], 'no-store, no-cache, must-revalidate, proxy-revalidate');
    console.log('✓ Test 7 Passed: Required defensive security headers verified');
  }

  console.log('\n========================================');
  console.log('All 7 Security & API Tests Passed 100%!');
  console.log('========================================\n');
}

runTests().catch(err => {
  console.error('Test Suite Failed:', err);
  process.exit(1);
});
