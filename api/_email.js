/**
 * ==============================================================================
 * Spotalents - Founder Email Notification Service
 * Module: api/_email.js
 * 
 * Sends executive, branded lead notification emails to Spotalents founders:
 * - hatemalihassan1@gmail.com
 * - contact@jointhedragons.com
 * 
 * Multi-Provider Architecture:
 * 1. Resend API (Official Vercel recommendation, zero-dependency fetch)
 * 2. Nodemailer / SMTP (Gmail, Google Workspace, custom SMTP, AWS SES, Mailgun)
 * 3. SendGrid v3 REST API
 * 4. Postmark REST API
 * 5. Brevo (Sendinblue) REST API
 * 6. Webhook URL (Slack, Discord, Zapier, Make)
 * ==============================================================================
 */

const nodemailer = require('nodemailer');

const DEFAULT_FOUNDER_EMAILS = [
  'hatemalihassan1@gmail.com',
  'contact@jointhedragons.com'
];

/**
 * HTML Escaper to prevent Stored XSS / HTML injection in email clients
 */
function escapeHtml(str) {
  if (!str && str !== 0) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

/**
 * Format human-readable date & time
 */
function formatDateTime(isoString) {
  try {
    const date = isoString ? new Date(isoString) : new Date();
    return date.toUTCString();
  } catch (e) {
    return new Date().toUTCString();
  }
}

/**
 * Retrieve recipient list from environment or default to founder emails
 */
function getRecipients() {
  const envRecipients = process.env.FOUNDER_NOTIFICATION_EMAIL || process.env.NOTIFICATION_RECIPIENTS || process.env.FOUNDER_EMAILS;
  if (envRecipients && typeof envRecipients === 'string') {
    const parsed = envRecipients
      .split(',')
      .map(e => e.trim().toLowerCase())
      .filter(e => e.length > 3 && e.includes('@'));
    if (parsed.length > 0) return parsed;
  }
  return DEFAULT_FOUNDER_EMAILS;
}

/**
 * Generate Spotalents Branded Email Templates (HTML & Plain Text)
 */
function generateEmailTemplates(lead) {
  const firstName = escapeHtml(lead.first_name || lead.firstName || 'Lead');
  const lastName = escapeHtml(lead.last_name || lead.lastName || '');
  const fullName = `${firstName} ${lastName}`.trim();
  const companyName = escapeHtml(lead.company_name || lead.companyName || 'Not specified');
  const email = (lead.email || '').trim().toLowerCase();
  const safeEmail = escapeHtml(email);
  const projectDetails = (lead.project_details || lead.projectDetails || '').trim();
  const safeProjectDetails = projectDetails ? escapeHtml(projectDetails).replace(/\n/g, '<br>') : '<em>No specific project notes provided.</em>';
  const source = escapeHtml(lead.source || 'start_page_lead');
  const plan = escapeHtml(lead.plan || lead.selectedPlan || 'General');
  const billing = escapeHtml(lead.billing || lead.selectedBilling || 'annual');
  const talentComp = escapeHtml(lead.talentComp || lead.comp || '');
  const talentFee = escapeHtml(lead.talentFee || lead.fee || '');
  const ipAddress = escapeHtml(lead.ip_address || lead.ipAddress || 'Not recorded');
  const userAgent = escapeHtml(lead.user_agent || lead.userAgent || 'Standard Browser');
  const submittedAt = formatDateTime(lead.submittedAt || lead.created_at);
  const userTimezone = escapeHtml(lead.userTimezone || lead.timezone || 'Not specified');
  const leadId = escapeHtml(lead.leadId || lead.id || 'N/A');

  // Supabase Dashboard URL helper
  const supabaseProjectUrl = process.env.SUPABASE_URL || '';
  let supabaseProjectId = '';
  const match = supabaseProjectUrl.match(/https:\/\/([a-zA-Z0-9_-]+)\.supabase\.co/);
  if (match) supabaseProjectId = match[1];
  const supabaseDashboardUrl = supabaseProjectId 
    ? `https://supabase.com/dashboard/project/${supabaseProjectId}/editor` 
    : 'https://supabase.com/dashboard';

  // Mailto Quick Reply Link
  const mailtoSubject = encodeURIComponent(`Re: Spotalents Demo Request - ${lead.company_name || lead.companyName || 'Engineering Pods'}`);
  const mailtoBody = encodeURIComponent(
    `Hi ${lead.first_name || lead.firstName || ''},\n\nThank you for requesting a demo with Spotalents. We received your request regarding ${lead.company_name || lead.companyName || 'your engineering requirements'}.\n\nI would love to learn more about your upcoming timeline and show you how our multi-signal intelligence pods can accelerate your team.\n\nAre you available for a brief 20-minute calibration session this week?\n\nBest regards,\nHatem Ali\nSpotalents & Dragons Leadership Team\nhttps://spotalents.com`
  );
  const mailtoUrl = `mailto:${encodeURIComponent(email)}?subject=${mailtoSubject}&body=${mailtoBody}`;

  // Subject line
  const subject = `⚡ New Demo Lead: ${fullName} from ${companyName}`;

  // Plain-Text Version
  const text = `
================================================================================
                     ⚡ SPOTALENTS - NEW INBOUND DEMO LEAD                      
================================================================================

A new prospect has requested a consultation from the Start Page.

LEAD OVERVIEW:
--------------------------------------------------------------------------------
Full Name:        ${fullName}
Company:          ${companyName}
Work Email:       ${email}
Selected Plan:    ${plan.toUpperCase()}${billing ? ' (' + billing + ')' : ''}${talentComp ? ' [Comp: $' + talentComp + ' / Fee: $' + talentFee + ']' : ''}
Lead ID:          ${leadId}
Source:           ${source}
Submission Time:  ${submittedAt} (UTC)
User Timezone:    ${userTimezone}

PROJECT SCOPE & REQUIREMENTS:
--------------------------------------------------------------------------------
${projectDetails || 'No specific notes provided.'}

AUDIT & TECHNICAL INFO:
--------------------------------------------------------------------------------
Client IP:        ${ipAddress}
User Agent:       ${userAgent}

FOUNDER ACTIONS:
--------------------------------------------------------------------------------
1. Reply to Lead directly:
   ${mailtoUrl}

2. View Leads in Supabase Dashboard:
   ${supabaseDashboardUrl}

--------------------------------------------------------------------------------
Delivered automatically to Spotalents Founders:
${DEFAULT_FOUNDER_EMAILS.join(', ')}
© ${new Date().getFullYear()} Spotalents. All rights reserved.
================================================================================
`.trim();

  // High-End Branded Responsive HTML Template
  const html = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="color-scheme" content="light dark">
  <title>${subject}</title>
  <!--[if mso]>
  <style type="text/css">
    body, table, td, p, a { font-family: Arial, Helvetica, sans-serif !important; }
  </style>
  <![endif]-->
</head>
<body style="margin: 0; padding: 0; background-color: #0b0f19; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; color: #1e293b; -webkit-font-smoothing: antialiased;">
  <!-- Preview Preheader Text -->
  <div style="display: none; max-height: 0px; overflow: hidden; mso-hide: all;">
    ⚡ New Demo Request from ${fullName} at ${companyName} via Spotalents Start Page.
    &#847; &zwnj; &nbsp; &#8199; &shy; &#847; &zwnj; &nbsp; &#8199; &shy;
  </div>

  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #0b0f19; width: 100%; margin: 0; padding: 32px 12px 48px 12px;">
    <tr>
      <td align="center">
        
        <!-- Main Card Container -->
        <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="max-width: 620px; background-color: #ffffff; border-radius: 14px; overflow: hidden; box-shadow: 0 20px 40px rgba(0, 0, 0, 0.45); border: 1px solid #1e293b;">
          
          <!-- Top Accent Gradient Line -->
          <tr>
            <td height="5" style="background: linear-gradient(90deg, #013BFF 0%, #2563EB 50%, #00F0FF 100%); line-height: 5px; font-size: 5px;">&nbsp;</td>
          </tr>

          <!-- Header Section -->
          <tr>
            <td style="background-color: #0d121f; padding: 32px 36px 28px 36px; border-bottom: 1px solid #1e293b;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
                <tr>
                  <td valign="middle">
                    <!-- Brand Wordmark -->
                    <div style="font-size: 22px; font-weight: 800; letter-spacing: -0.5px; color: #ffffff; margin: 0 0 4px 0;">
                      <span style="color: #013BFF;">⚡</span> SPOTALENTS
                    </div>
                    <div style="font-size: 13px; color: #94a3b8; font-weight: 500; letter-spacing: 0.2px;">
                      Elite Engineering Pods &middot; Inbound Intelligence
                    </div>
                  </td>
                  <td valign="middle" align="right">
                    <!-- Live Pill Badge -->
                    <span style="display: inline-block; background-color: rgba(1, 59, 255, 0.18); border: 1px solid #013BFF; color: #60a5fa; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.8px; padding: 6px 12px; border-radius: 20px;">
                      New Demo Lead
                    </span>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Hero Headline -->
          <tr>
            <td style="padding: 32px 36px 20px 36px; background-color: #ffffff;">
              <h1 style="margin: 0 0 10px 0; font-size: 22px; line-height: 1.35; color: #0f172a; font-weight: 800; letter-spacing: -0.4px;">
                New Lead: <span style="color: #013BFF;">${companyName}</span>
              </h1>
              <p style="margin: 0; font-size: 15px; line-height: 1.55; color: #475569;">
                A new prospect has submitted their requirements through the <strong>Start Page</strong> demo booking form.
              </p>
            </td>
          </tr>

          <!-- Lead Details Table -->
          <tr>
            <td style="padding: 10px 36px 24px 36px;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; overflow: hidden;">
                
                <!-- Row 1: Full Name -->
                <tr>
                  <td width="35%" style="padding: 14px 18px; font-size: 13px; font-weight: 600; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 1px solid #e2e8f0;">
                    Lead Name
                  </td>
                  <td width="65%" style="padding: 14px 18px; font-size: 15px; font-weight: 700; color: #0f172a; border-bottom: 1px solid #e2e8f0;">
                    ${fullName}
                  </td>
                </tr>

                <!-- Row 2: Company Name -->
                <tr>
                  <td style="padding: 14px 18px; font-size: 13px; font-weight: 600; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 1px solid #e2e8f0;">
                    Company
                  </td>
                  <td style="padding: 14px 18px; font-size: 15px; font-weight: 700; color: #013BFF; border-bottom: 1px solid #e2e8f0;">
                    ${companyName}
                  </td>
                </tr>

                <!-- Row 3: Business Email -->
                <tr>
                  <td style="padding: 14px 18px; font-size: 13px; font-weight: 600; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 1px solid #e2e8f0;">
                    Work Email
                  </td>
                  <td style="padding: 14px 18px; font-size: 15px; font-weight: 600; border-bottom: 1px solid #e2e8f0;">
                    <a href="${mailtoUrl}" style="color: #013BFF; text-decoration: underline;">${safeEmail}</a>
                  </td>
                </tr>

                <!-- Row: Selected Plan & Billing -->
                <tr>
                  <td style="padding: 14px 18px; font-size: 13px; font-weight: 600; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 1px solid #e2e8f0;">
                    Plan Selection
                  </td>
                  <td style="padding: 14px 18px; font-size: 15px; font-weight: 700; color: #0f172a; border-bottom: 1px solid #e2e8f0;">
                    <span style="display: inline-block; background-color: rgba(1, 59, 255, 0.1); color: #013BFF; padding: 3px 8px; border-radius: 6px; font-size: 13px; margin-right: 6px;">${plan.toUpperCase()}</span>
                    <span style="font-size: 13px; font-weight: 600; color: #475569;">${billing ? '(' + billing + ')' : ''}${talentComp ? ' · Comp: $' + talentComp + ' + Fee: $' + talentFee : ''}</span>
                  </td>
                </tr>

                <!-- Row 4: Source & Timezone -->
                <tr>
                  <td style="padding: 14px 18px; font-size: 13px; font-weight: 600; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 1px solid #e2e8f0;">
                    Channel / Source
                  </td>
                  <td style="padding: 14px 18px; font-size: 14px; color: #334155; border-bottom: 1px solid #e2e8f0;">
                    ${source} &middot; <span style="color: #64748b;">${userTimezone}</span>
                  </td>
                </tr>

                <!-- Row 5: Time Received -->
                <tr>
                  <td style="padding: 14px 18px; font-size: 13px; font-weight: 600; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px;">
                    Received (UTC)
                  </td>
                  <td style="padding: 14px 18px; font-size: 14px; color: #334155;">
                    ${submittedAt}
                  </td>
                </tr>

              </table>
            </td>
          </tr>

          <!-- Project Details Callout -->
          <tr>
            <td style="padding: 0 36px 28px 36px;">
              <div style="font-size: 13px; font-weight: 700; color: #334155; text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 8px;">
                Project Context &amp; Requirements
              </div>
              <div style="background-color: #f1f5f9; border-left: 4px solid #013BFF; border-radius: 4px; padding: 18px 20px; font-size: 14px; line-height: 1.6; color: #1e293b;">
                ${safeProjectDetails}
              </div>
            </td>
          </tr>

          <!-- Direct Call-to-Action Buttons -->
          <tr>
            <td style="padding: 0 36px 36px 36px;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
                <tr>
                  <!-- Primary CTA: Reply to Lead -->
                  <td align="left" style="padding-right: 12px;">
                    <a href="${mailtoUrl}" target="_blank" style="display: inline-block; background-color: #013BFF; color: #ffffff; font-size: 14px; font-weight: 700; text-decoration: none; padding: 14px 26px; border-radius: 8px; box-shadow: 0 4px 14px rgba(1, 59, 255, 0.35); text-align: center;">
                      &rarr; Reply to ${firstName}
                    </a>
                  </td>

                  <!-- Secondary CTA: View in Database -->
                  <td align="right">
                    <a href="${supabaseDashboardUrl}" target="_blank" style="display: inline-block; background-color: #ffffff; color: #334155; font-size: 13px; font-weight: 600; text-decoration: none; padding: 13px 20px; border-radius: 8px; border: 1px solid #cbd5e1; text-align: center;">
                      Open Supabase &nearr;
                    </a>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Audit & Device Telemetry (Subtle Collapsible/Footer info) -->
          <tr>
            <td style="background-color: #f8fafc; padding: 20px 36px; border-top: 1px solid #e2e8f0; font-size: 12px; color: #64748b; line-height: 1.6;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
                <tr>
                  <td>
                    <strong>Client IP:</strong> ${ipAddress}<br>
                    <strong>Database Record ID:</strong> ${leadId}
                  </td>
                  <td align="right" valign="top">
                    <strong>Browser:</strong> ${userAgent.slice(0, 40)}...
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Footer Information -->
          <tr>
            <td style="background-color: #0d121f; padding: 24px 36px; border-top: 1px solid #1e293b; text-align: center; color: #94a3b8; font-size: 12px; line-height: 1.6;">
              <p style="margin: 0 0 6px 0; font-weight: 600; color: #cbd5e1;">
                Spotalents &middot; Join The Dragons Executive Lead Notification
              </p>
              <p style="margin: 0; color: #64748b;">
                Delivered automatically to <strong>hatemalihassan1@gmail.com</strong> and <strong>contact@jointhedragons.com</strong>.<br>
                &copy; ${new Date().getFullYear()} Spotalents. All rights reserved.
              </p>
            </td>
          </tr>

        </table>
        
      </td>
    </tr>
  </table>
</body>
</html>`;

  return { subject, html, text };
}

/**
 * Dispatch Founder Notification Email
 * 
 * Supports:
 * - Resend API (Bearer RESEND_API_KEY)
 * - Nodemailer / SMTP (Gmail App Password, Google Workspace, custom SMTP)
 * - SendGrid API (SENDGRID_API_KEY)
 * - Postmark API (POSTMARK_SERVER_TOKEN)
 * - Brevo API (BREVO_API_KEY)
 * - Webhook (FOUNDER_NOTIFICATION_WEBHOOK_URL)
 */
async function sendFounderNotification(leadRecord) {
  const recipients = getRecipients();
  const { subject, html, text } = generateEmailTemplates(leadRecord);

  const fromAddress = process.env.EMAIL_FROM || 'Spotalents Inbound <notifications@spotalents.com>';
  const replyTo = leadRecord.email || (leadRecord.email ? leadRecord.email.trim() : undefined);

  console.log(`[Founder Notification] Initiating dispatch to: ${recipients.join(', ')}`);

  // Provider 1: Resend REST API (Best for Vercel Serverless Functions)
  if (process.env.RESEND_API_KEY) {
    try {
      console.log('[Founder Notification] Using Resend API provider...');
      const resendFrom = process.env.EMAIL_FROM || 'Spotalents <onboarding@resend.dev>';
      const res = await fetch('https://api.resend.com/emails', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${process.env.RESEND_API_KEY}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          from: resendFrom,
          to: recipients,
          reply_to: replyTo,
          subject: subject,
          html: html,
          text: text
        })
      });

      const data = await res.json().catch(() => ({}));
      if (!res.ok) {
        throw new Error(`Resend API error (${res.status}): ${data.message || JSON.stringify(data)}`);
      }

      console.log('[Founder Notification] Successfully sent via Resend API. ID:', data.id);
      return { sent: true, provider: 'resend', id: data.id, recipients };
    } catch (resendErr) {
      console.error('[Founder Notification] Resend provider failed:', resendErr.message);
      // Continue to next provider fallback
    }
  }

  // Provider 2: Nodemailer with SMTP (e.g. Gmail App Password, AWS SES, or custom SMTP)
  const smtpUser = process.env.SMTP_USER || process.env.GMAIL_USER || process.env.EMAIL_USER;
  const smtpPass = process.env.SMTP_PASS || process.env.GMAIL_APP_PASSWORD || process.env.EMAIL_PASS;
  const smtpHost = process.env.SMTP_HOST;

  if ((smtpHost && smtpUser) || (smtpUser && smtpPass)) {
    try {
      console.log('[Founder Notification] Using Nodemailer SMTP provider...');
      let transportOptions;

      if (smtpHost) {
        // Custom SMTP
        transportOptions = {
          host: smtpHost,
          port: parseInt(process.env.SMTP_PORT || '587', 10),
          secure: process.env.SMTP_SECURE === 'true' || process.env.SMTP_PORT === '465',
          auth: {
            user: smtpUser,
            pass: smtpPass
          }
        };
      } else {
        // Gmail or Google Workspace preset
        transportOptions = {
          service: 'gmail',
          auth: {
            user: smtpUser,
            pass: smtpPass
          }
        };
      }

      const transporter = nodemailer.createTransport(transportOptions);
      const info = await transporter.sendMail({
        from: fromAddress,
        to: recipients.join(', '),
        replyTo: replyTo,
        subject: subject,
        text: text,
        html: html
      });

      console.log('[Founder Notification] Successfully sent via Nodemailer SMTP. MessageId:', info.messageId);
      return { sent: true, provider: 'smtp', messageId: info.messageId, recipients };
    } catch (smtpErr) {
      console.error('[Founder Notification] Nodemailer SMTP failed:', smtpErr.message);
      // Continue to next provider fallback
    }
  }

  // Provider 3: SendGrid API
  if (process.env.SENDGRID_API_KEY) {
    try {
      console.log('[Founder Notification] Using SendGrid API provider...');
      const res = await fetch('https://api.sendgrid.com/v3/mail/send', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${process.env.SENDGRID_API_KEY}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          personalizations: [
            {
              to: recipients.map(email => ({ email }))
            }
          ],
          from: {
            email: process.env.SENDGRID_FROM || process.env.EMAIL_FROM || 'notifications@spotalents.com',
            name: 'Spotalents Inbound'
          },
          reply_to: replyTo ? { email: replyTo } : undefined,
          subject: subject,
          content: [
            { type: 'text/plain', value: text },
            { type: 'text/html', value: html }
          ]
        })
      });

      if (!res.ok) {
        const errorText = await res.text();
        throw new Error(`SendGrid API error (${res.status}): ${errorText}`);
      }

      console.log('[Founder Notification] Successfully sent via SendGrid API.');
      return { sent: true, provider: 'sendgrid', recipients };
    } catch (sgErr) {
      console.error('[Founder Notification] SendGrid provider failed:', sgErr.message);
    }
  }

  // Provider 4: Postmark API
  if (process.env.POSTMARK_SERVER_TOKEN) {
    try {
      console.log('[Founder Notification] Using Postmark API provider...');
      const res = await fetch('https://api.postmarkapp.com/email', {
        method: 'POST',
        headers: {
          'X-Postmark-Server-Token': process.env.POSTMARK_SERVER_TOKEN,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          From: process.env.EMAIL_FROM || 'notifications@spotalents.com',
          To: recipients.join(','),
          ReplyTo: replyTo,
          Subject: subject,
          TextBody: text,
          HtmlBody: html
        })
      });

      const postmarkData = await res.json().catch(() => ({}));
      if (!res.ok) {
        throw new Error(`Postmark API error (${res.status}): ${JSON.stringify(postmarkData)}`);
      }

      console.log('[Founder Notification] Successfully sent via Postmark API.');
      return { sent: true, provider: 'postmark', id: postmarkData.MessageID, recipients };
    } catch (pmErr) {
      console.error('[Founder Notification] Postmark provider failed:', pmErr.message);
    }
  }

  // Provider 5: Brevo (Sendinblue) API
  if (process.env.BREVO_API_KEY) {
    try {
      console.log('[Founder Notification] Using Brevo API provider...');
      const res = await fetch('https://api.brevo.com/v3/smtp/email', {
        method: 'POST',
        headers: {
          'api-key': process.env.BREVO_API_KEY,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          sender: { name: 'Spotalents', email: process.env.EMAIL_FROM || 'notifications@spotalents.com' },
          to: recipients.map(email => ({ email })),
          replyTo: replyTo ? { email: replyTo } : undefined,
          subject: subject,
          htmlContent: html,
          textContent: text
        })
      });

      const brevoData = await res.json().catch(() => ({}));
      if (!res.ok) {
        throw new Error(`Brevo API error (${res.status}): ${JSON.stringify(brevoData)}`);
      }

      console.log('[Founder Notification] Successfully sent via Brevo API.');
      return { sent: true, provider: 'brevo', messageId: brevoData.messageId, recipients };
    } catch (brevoErr) {
      console.error('[Founder Notification] Brevo provider failed:', brevoErr.message);
    }
  }

  // Provider 6: Generic Notification Webhook (Slack / Discord / Zapier / Make)
  if (process.env.FOUNDER_NOTIFICATION_WEBHOOK_URL) {
    try {
      console.log('[Founder Notification] Triggering Notification Webhook...');
      const res = await fetch(process.env.FOUNDER_NOTIFICATION_WEBHOOK_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          event: 'new_lead',
          recipients: recipients,
          subject: subject,
          lead: leadRecord,
          submittedAt: new Date().toISOString()
        })
      });

      if (!res.ok) {
        throw new Error(`Webhook failed (${res.status})`);
      }

      console.log('[Founder Notification] Successfully triggered Notification Webhook.');
      return { sent: true, provider: 'webhook', recipients };
    } catch (webhookErr) {
      console.error('[Founder Notification] Webhook trigger failed:', webhookErr.message);
    }
  }

  // Fallback: If no email API keys or SMTP are configured in environment
  console.warn(
    `[Founder Notification] ⚠️ Email delivery skipped: No email provider configured in environment variables.\n` +
    `Recipients configured: ${recipients.join(', ')}\n` +
    `To enable live email dispatch, add RESEND_API_KEY or SMTP_USER/SMTP_PASS in Vercel or .env.local.\n` +
    `Lead data was safely saved to Supabase.`
  );

  return {
    sent: false,
    reason: 'provider_not_configured',
    recipients: recipients,
    message: 'To enable automatic email notifications, set RESEND_API_KEY or SMTP_USER/SMTP_PASS in environment.'
  };
}

module.exports = {
  DEFAULT_FOUNDER_EMAILS,
  escapeHtml,
  generateEmailTemplates,
  sendFounderNotification,
  getRecipients
};
