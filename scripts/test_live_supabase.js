const fs = require('fs');
const path = require('path');
const assert = require('assert');
const { createClient } = require('@supabase/supabase-js');
const handler = require('../api/leads');

// Load environment variables from .env.local if present
const envLocalPath = path.join(__dirname, '../.env.local');
if (fs.existsSync(envLocalPath)) {
  const envContent = fs.readFileSync(envLocalPath, 'utf8');
  envContent.split('\n').forEach(line => {
    const match = line.match(/^\s*([\w.-]+)\s*=\s*(.*)?\s*$/);
    if (match) {
      let key = match[1];
      let value = (match[2] || '').trim();
      if (value.startsWith('"') && value.endsWith('"')) value = value.slice(1, -1);
      if (!process.env[key]) process.env[key] = value;
    }
  });
}

function createMockReqRes(options = {}) {
  const req = {
    method: options.method || 'POST',
    headers: {
      'content-type': 'application/json',
      'user-agent': 'SpotalentsIntegrationTest/1.0',
      'x-forwarded-for': '203.0.113.195',
      origin: 'https://spotalents.com'
    },
    body: options.body || {},
    socket: { remoteAddress: '203.0.113.195' }
  };

  let statusCode = 200;
  let responseBody = null;

  const res = {
    setHeader: () => {},
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

  return { req, res, getStatusCode: () => statusCode, getBody: () => responseBody };
}

async function testLiveIntegration() {
  console.log('--- Testing Live /api/leads Integration with Supabase ---');

  const testEmail = `lead_test_${Date.now()}@spotalents-verify.com`;
  const { req, res, getStatusCode, getBody } = createMockReqRes({
    body: {
      firstName: 'Hamdy',
      lastName: 'Saad',
      companyName: 'Spotalents Test Engineering',
      email: testEmail,
      projectDetails: 'Automated verification test of live Supabase connection via Vercel.',
      source: 'start_page_lead',
      _formRenderTime: Date.now() - 4000
    }
  });

  await handler(req, res);

  console.log(`Response Code: ${getStatusCode()}`);
  console.log('Response Body:', getBody());

  assert.strictEqual(getStatusCode(), 200, 'Expected HTTP 200 from live lead submission');
  assert.strictEqual(getBody().success, true, 'Expected success: true');
  const insertedLeadId = getBody().leadId;
  assert(insertedLeadId, 'Expected a generated UUID leadId');
  console.log(`✓ Lead successfully inserted into Supabase! ID: ${insertedLeadId}`);

  // Test Row Level Security (RLS):
  // 1. Try reading the record using the PUBLIC ANON KEY (Should fail or return 0 rows)
  const anonClient = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_ANON_KEY);
  const { data: anonData, error: anonError } = await anonClient
    .from('leads')
    .select('*')
    .eq('id', insertedLeadId);

  assert(
    !anonData || anonData.length === 0,
    'RLS VIOLATION: Public anon key was able to read lead data!'
  );
  console.log('✓ Verified Row Level Security: Public anon client is FORBIDDEN from reading leads (returned 0 rows)');

  // 2. Read and clean up the record using SERVICE ROLE KEY
  const adminClient = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY);
  const { data: adminData } = await adminClient
    .from('leads')
    .select('*')
    .eq('id', insertedLeadId)
    .single();

  assert(adminData, 'Admin client should be able to read the lead');
  assert.strictEqual(adminData.email, testEmail);
  console.log('✓ Verified Service Role access: Admin can read lead record');

  // Clean up test record
  await adminClient.from('leads').delete().eq('id', insertedLeadId);
  console.log('✓ Cleaned up test lead from database');

  console.log('\n========================================');
  console.log('Live Supabase Integration is 100% OPERATIONAL & SECURED!');
  console.log('========================================\n');
}

testLiveIntegration().catch(err => {
  console.error('Live Test Failed:', err);
  process.exit(1);
});
