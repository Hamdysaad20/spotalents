/**
 * ==============================================================================
 * Spotalents - Lead Submission & Demo Booking Vercel Serverless Function
 * Path: /api/leads
 * 
 * Standard Security Implementation:
 * - Method Restriction (POST only)
 * - Anti-bot Honeypot Detection
 * - Submission Timing Defense (anti-automation)
 * - Rate Limiting per IP
 * - Strict Server-side Input Validation & Sanitization (Anti-XSS)
 * - Database Row Level Security (RLS) Compatible Integration
 * - Information Leakage Prevention
 * - Dual Engine: Official @supabase/supabase-js with native REST fallback
 * - Branded Founder Email Notifications to hatemalihassan1@gmail.com & contact@jointhedragons.com
 * ==============================================================================
 */

const { sendFounderNotification } = require('./_email');

// 1. In-memory Rate Limiting (Token Bucket per IP)
const RATE_LIMIT_WINDOW_MS = 10 * 60 * 1000; // 10 minutes
const MAX_REQUESTS_PER_WINDOW = 5;
const ipRequestHistory = new Map();

function isRateLimited(clientIp) {
  if (!clientIp || clientIp === 'unknown') return false;
  
  const now = Date.now();
  const clientHistory = ipRequestHistory.get(clientIp) || [];
  
  // Prune requests older than window
  const recentRequests = clientHistory.filter(timestamp => now - timestamp < RATE_LIMIT_WINDOW_MS);
  
  if (recentRequests.length >= MAX_REQUESTS_PER_WINDOW) {
    ipRequestHistory.set(clientIp, recentRequests);
    return true;
  }
  
  recentRequests.push(now);
  ipRequestHistory.set(clientIp, recentRequests);
  
  // Cleanup map occasionally to prevent memory leaks
  if (ipRequestHistory.size > 2000) {
    for (const [ip, timestamps] of ipRequestHistory.entries()) {
      if (timestamps.every(t => now - t >= RATE_LIMIT_WINDOW_MS)) {
        ipRequestHistory.delete(ip);
      }
    }
  }
  
  return false;
}

// 2. Data Sanitizer - Strips HTML/Control characters to prevent Stored XSS
function sanitizeString(input, maxLength = 255) {
  if (typeof input !== 'string') return '';
  return input
    .trim()
    .replace(/[<>]/g, '') // Strip brackets to eliminate tags
    .replace(/[\u0000-\u001F\u007F-\u009F]/g, '') // Strip non-printable ASCII control chars
    .slice(0, maxLength);
}

// 3. Strict RFC Email Validator
function isValidEmail(email) {
  if (typeof email !== 'string') return false;
  const trimmed = email.trim();
  if (trimmed.length < 5 || trimmed.length > 255) return false;
  const emailRegex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+$/;
  return emailRegex.test(trimmed);
}

// 4. Main Serverless Handler
module.exports = async function handler(req, res) {
  // Set standard defensive security headers
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate, proxy-revalidate');
  res.setHeader('Pragma', 'no-cache');
  res.setHeader('Expires', '0');

  // Handle CORS
  const origin = req.headers.origin || '';
  
  // Allow all local development environments (file:// protocol, localhost on any port, 127.0.0.1 on any port)
  const isLocalOrigin = 
    origin === 'null' ||
    /^https?:\/\/localhost(:\d+)?$/.test(origin) ||
    /^https?:\/\/127\.0\.0\.1(:\d+)?$/.test(origin);

  const isProductionOrigin = 
    origin === 'https://spotalents.com' ||
    origin === 'https://www.spotalents.com' ||
    origin.endsWith('.vercel.app');

  if (isLocalOrigin) {
    // When opened from local (file:// sends 'null', or any localhost/127.0.0.1 port)
    res.setHeader('Access-Control-Allow-Origin', origin === 'null' ? '*' : origin);
  } else if (isProductionOrigin || !origin) {
    res.setHeader('Access-Control-Allow-Origin', origin || '*');
  } else {
    res.setHeader('Access-Control-Allow-Origin', 'https://spotalents.com');
  }
  
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Accept');

  // Handle preflight OPTIONS request
  if (req.method === 'OPTIONS') {
    return res.status(204).end();
  }

  // Enforce HTTP Method
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST, OPTIONS');
    return res.status(405).json({
      success: false,
      error: 'Method not allowed. Only POST requests are permitted.'
    });
  }

  // Extract client metadata for audit and rate limiting
  const forwarded = req.headers['x-forwarded-for'];
  const clientIp = typeof forwarded === 'string' 
    ? forwarded.split(',')[0].trim() 
    : (req.socket?.remoteAddress || 'unknown');
  const userAgent = req.headers['user-agent'] || 'unknown';
  const referrer = req.headers['referer'] || req.headers['referrer'] || '';

  // Check Rate Limit
  if (isRateLimited(clientIp)) {
    return res.status(429).json({
      success: false,
      error: 'Too many requests. Please wait a few minutes before submitting again.'
    });
  }

  // Parse payload (Vercel automatically parses JSON bodies, but we safeguard against strings)
  let body = req.body;
  if (typeof body === 'string') {
    try {
      body = JSON.parse(body);
    } catch (e) {
      return res.status(400).json({
        success: false,
        error: 'Malformed JSON payload.'
      });
    }
  }

  if (!body || typeof body !== 'object') {
    return res.status(400).json({
      success: false,
      error: 'Request body must be a valid JSON object.'
    });
  }

  // Anti-Spam Check 1: Honeypot Trap
  // Hidden input '_hp_company_url' that human users never fill. Bots fill all inputs.
  const honeypot = body._hp_company_url || body.website_url || body._hp;
  if (honeypot && String(honeypot).trim().length > 0) {
    // Return silent success to trick bot scrapers into believing they succeeded
    console.warn(`[Anti-Spam] Honeypot triggered by IP: ${clientIp}`);
    return res.status(200).json({
      success: true,
      message: 'Demo request received successfully.'
    });
  }

  // Anti-Spam Check 2: Submission Timing Check
  // Humans take at least 1.2s to fill the form. Instant submissions (< 1200ms) are automated scripts.
  const formRenderTime = Number(body._formRenderTime);
  if (formRenderTime && !isNaN(formRenderTime)) {
    const elapsedMs = Date.now() - formRenderTime;
    if (elapsedMs < 1200) {
      console.warn(`[Anti-Spam] Sub-human submission speed detected (${elapsedMs}ms) by IP: ${clientIp}`);
      return res.status(200).json({
        success: true,
        message: 'Demo request received successfully.'
      });
    }
  }

  // Input Validation & Sanitization
  const firstName = sanitizeString(body.firstName, 100);
  const lastName = sanitizeString(body.lastName, 100);
  const companyName = sanitizeString(body.companyName, 150);
  const email = (body.email || '').trim().toLowerCase();
  const projectDetails = sanitizeString(body.projectDetails, 3000);
  const source = sanitizeString(body.source || 'start_page', 50);

  // Pricing & Plan Metadata
  const plan = sanitizeString(body.plan || '', 50);
  const billing = sanitizeString(body.billing || '', 50);
  const talentComp = body.talentComp || body.comp ? sanitizeString(String(body.talentComp || body.comp), 20) : null;
  const talentFee = body.talentFee || body.fee ? sanitizeString(String(body.talentFee || body.fee), 20) : null;

  const errors = [];
  if (!firstName || firstName.length < 1) errors.push('First name is required.');
  if (!lastName || lastName.length < 1) errors.push('Last name is required.');
  if (!companyName || companyName.length < 1) errors.push('Company name is required.');
  if (!isValidEmail(email)) errors.push('A valid business email address is required.');

  if (errors.length > 0) {
    return res.status(400).json({
      success: false,
      error: 'Validation failed',
      details: errors
    });
  }

  // Prepend structured plan metadata to project_details so it is always preserved in any database/dashboard
  let formattedProjectDetails = projectDetails;
  if (plan && plan !== 'general') {
    const metaParts = [`Plan: ${plan.toUpperCase()}`];
    if (billing && billing !== 'unspecified') metaParts.push(`Billing: ${billing}`);
    if (talentComp) metaParts.push(`Comp: $${talentComp}`);
    if (talentFee) metaParts.push(`Fee: $${talentFee}`);
    const metaHeader = `[${metaParts.join(' | ')}]`;
    formattedProjectDetails = formattedProjectDetails ? `${metaHeader}\n\n${formattedProjectDetails}` : metaHeader;
  }

  // Prepare Record for Supabase
  const leadRecord = {
    first_name: firstName,
    last_name: lastName,
    company_name: companyName,
    email: email,
    project_details: formattedProjectDetails || null,
    source: source,
    plan: plan || null,
    billing: billing || null,
    talent_comp: talentComp || null,
    talent_fee: talentFee || null,
    ip_address: clientIp,
    user_agent: userAgent.slice(0, 500),
    referrer: referrer.slice(0, 500),
    status: 'new'
  };

  // Supabase Configuration
  const supabaseUrl = process.env.SUPABASE_URL || process.env.NEXT_PUBLIC_SUPABASE_URL;
  // Prefer service role key for privileged server-side operations, fall back to anon key
  const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY || 
                      process.env.SUPABASE_ANON_KEY || 
                      process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

  if (!supabaseUrl || !supabaseKey) {
    console.error('[Configuration Error] Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY in environment.');
    // Fail gracefully without leaking environment state details
    return res.status(503).json({
      success: false,
      error: 'Database connection is currently undergoing maintenance. Please try again shortly or contact support@spotalents.com.'
    });
  }

  // Insert Record into Supabase
  try {
    let insertedId = null;

    // Prepare extended payload for when native plan/billing columns exist
    const insertPayload = { ...leadRecord };
    if (plan) insertPayload.plan = plan;
    if (billing) insertPayload.billing = billing;

    // Strategy A: Official @supabase/supabase-js library
    try {
      const { createClient } = require('@supabase/supabase-js');
      const supabase = createClient(supabaseUrl, supabaseKey, {
        auth: {
          persistSession: false,
          autoRefreshToken: false
        }
      });

      let { data, error } = await supabase
        .from('leads')
        .insert([insertPayload])
        .select('id')
        .single();

      // If database table does not yet have plan/billing columns, retry with base leadRecord
      if (error && (error.message?.includes('column') || error.code === 'PGRST204' || error.code === '42703')) {
        console.info('[Supabase] Native plan/billing columns not detected. Inserting base lead record (metadata preserved in project_details)...');
        const retry = await supabase
          .from('leads')
          .insert([leadRecord])
          .select('id')
          .single();
        if (retry.error) throw retry.error;
        data = retry.data;
        error = null;
      } else if (error) {
        throw error;
      }
      insertedId = data ? data.id : null;
    } catch (sdkError) {
      // Fallback Strategy B: Direct Supabase PostgREST API via native fetch
      // Ensures zero failure even if SDK loading experiences unexpected issues
      console.warn('[Supabase SDK fallback to PostgREST HTTP fetch]:', sdkError.message || sdkError);
      
      const restEndpoint = `${supabaseUrl.replace(/\/$/, '')}/rest/v1/leads`;
      let response = await fetch(restEndpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'apikey': supabaseKey,
          'Authorization': `Bearer ${supabaseKey}`,
          'Prefer': 'return=representation'
        },
        body: JSON.stringify(insertPayload)
      });

      if (!response.ok) {
        const errorText = await response.text();
        if (errorText.includes('column') || response.status === 400) {
          console.info('[Supabase REST] Retrying insert with base lead record...');
          response = await fetch(restEndpoint, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'apikey': supabaseKey,
              'Authorization': `Bearer ${supabaseKey}`,
              'Prefer': 'return=representation'
            },
            body: JSON.stringify(leadRecord)
          });
        }
        if (!response.ok) {
          throw new Error(`Supabase REST error (${response.status}): ${await response.text()}`);
        }
      }

      const responseData = await response.json();
      if (Array.isArray(responseData) && responseData.length > 0) {
        insertedId = responseData[0].id;
      }
    }

    // Dispatch Instant Founder Email Notification (to hatemalihassan1@gmail.com & contact@jointhedragons.com)
    let emailStatus = null;
    try {
      emailStatus = await sendFounderNotification({
        ...leadRecord,
        leadId: insertedId,
        plan: plan || 'General',
        billing: billing || 'annual',
        talentComp: talentComp || null,
        talentFee: talentFee || null,
        userTimezone: sanitizeString(body.timezone || body.userTimezone, 100),
        submittedLocalTime: sanitizeString(body.submittedLocalTime, 100),
        pageUrl: sanitizeString(body.pageUrl, 500)
      });
    } catch (emailErr) {
      console.error('[Founder Notification Dispatch Error]:', emailErr.message || emailErr);
      emailStatus = { sent: false, error: emailErr.message };
    }

    // Success response
    return res.status(200).json({
      success: true,
      message: 'Demo request received successfully. Our calibration team will connect with you within 24 hours.',
      leadId: insertedId || undefined,
      notification: {
        sent: Boolean(emailStatus?.sent),
        provider: emailStatus?.provider || null,
        recipients: emailStatus?.recipients || ['hatemalihassan1@gmail.com', 'contact@jointhedragons.com']
      }
    });

  } catch (dbError) {
    // Log complete error internally for Vercel Runtime Logs / Observability
    console.error('[Supabase Insertion Error]:', dbError);

    // Return safe, sanitized error message to client (Prevent Information Disclosure)
    return res.status(500).json({
      success: false,
      error: 'We were unable to save your request due to a server error. Please try again or reach out directly to contact@spotalents.com.'
    });
  }
};
