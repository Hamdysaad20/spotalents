# Spotalents: Supabase + Vercel Integration & Security Guide

This document explains the standard, bank-grade architecture implemented to connect the `/start` page demo booking form with **Supabase** via **Vercel Serverless Functions**.

---

## 1. Architecture & Security Overview

```
[ User Browser /start page ]
          │
          │ 1. Client-side validation
          │ 2. Invisible Honeypot & Timing checks
          │ 3. POST JSON payload
          ▼
[ Vercel Serverless Function: /api/leads ]
   ├── Method Guard: Restrict to POST only (405 on GET/PUT/DELETE)
   ├── Defensive Headers: no-store, nosniff, CORS restrictions
   ├── Rate Limiter: In-memory sliding window (max 5 submissions / 10m / IP)
   ├── Anti-Bot Layer: Honeypot drop + Sub-human speed rejection (<1.2s)
   ├── Anti-XSS Sanitizer: Strips HTML tags and ASCII control characters
   ├── Strict RFC Email Validation
   │
   │ 4. Authenticated Server-to-Server Request (Secrets never exposed in browser)
   ▼
[ Supabase PostgreSQL Database (Table: public.leads) ]
   ├── Row Level Security (RLS) ENABLED & FORCED
   ├── Revoke Public Reads: Anons cannot read, update, or delete other people's leads
   ├── Check Constraints: Length & RFC email validation at DB level
   └── Performance Indexes: created_at, email, status, company_name
```

---

## 2. Quick Setup Instructions

### Step 1: Run the Database Migration in Supabase
1. Go to your [Supabase Dashboard](https://supabase.com/dashboard).
2. Open your project (or create one).
3. In the left navigation, click **SQL Editor**.
4. Click **New Query**.
5. Copy and paste the contents of `supabase/schema.sql` into the editor.
6. Click **Run**.
   - This creates the `public.leads` table with all indexes, triggers, and Row Level Security policies.

---

### Step 2: Connect Supabase to Vercel

You have two easy ways to connect:

#### Option A: One-Click Vercel Integration (Recommended)
1. Go to your [Vercel Dashboard](https://vercel.com/dashboard).
2. Select your `spotalents` project.
3. Go to the **Integrations** tab.
4. Search for **Supabase** and click **Add Integration** / **Install**.
5. Select your Supabase project — Vercel will automatically configure your environment variables.

#### Option B: Manual Environment Variables in Vercel
1. Go to your [Supabase Dashboard](https://supabase.com/dashboard) → **Project Settings** → **API**.
2. Copy:
   - **Project URL** (`https://xyzcompany.supabase.co`)
   - **service_role secret key** (under *Project API keys* - click reveal)
   - *(Optional)* **anon public key**
3. Go to your **Vercel Project** → **Settings** → **Environment Variables**:
   - Add `SUPABASE_URL` = `https://your-project.supabase.co`
   - Add `SUPABASE_SERVICE_ROLE_KEY` = `your-service-role-secret-key`
   - *(Optional)* Add `SUPABASE_ANON_KEY` = `your-anon-public-key`
4. Select all environments: **Production**, **Preview**, **Development**.
5. Click **Save** and trigger a redeploy (or push to git).

---

## 3. Local Development & Testing

To test locally with environment variables:
1. Create a `.env.local` file in the project root:
   ```bash
   SUPABASE_URL=https://your-project-id.supabase.co
   SUPABASE_SERVICE_ROLE_KEY=your-supabase-service-role-key-here
   ```
2. Run local tests:
   ```bash
   npm test
   ```
3. Run with Vercel CLI locally (if desired):
   ```bash
   vercel dev
   ```

---

## 4. Key Security Controls Implemented

| Security Threat | Mitigation Strategy | Implemented In |
| :--- | :--- | :--- |
| **Credential Scraping** | Database service keys are stored exclusively in Vercel Serverless environment variables; never leaked to frontend JavaScript. | `/api/leads.js` |
| **Data Scraping / Bulk Leakage** | Row Level Security (RLS) is forced. Public/anon `SELECT` permissions are revoked entirely; attackers cannot query the leads table. | `supabase/schema.sql` |
| **Automated Spam Bots** | Dual-layer bot trap: invisible honeypot field (`_hp_company_url`) + submission speed detector (<1.2s). | `start/index.html` & `/api/leads.js` |
| **DoS / Brute Force Spam** | Sliding window rate limiter restricts each IP address to 5 submissions per 10 minutes. | `/api/leads.js` |
| **Stored Cross-Site Scripting (XSS)** | All string inputs are sanitized, tag brackets `<>` and non-printable control characters are stripped. | `/api/leads.js` |
| **Lead Loss Resilience** | If network drops or database maintenance occurs, lead payload is preserved in client `localStorage` (`spotalents_leads_pending`). | `start/index.html` |
| **Information Disclosure** | Generic, safe error messages returned to clients; detailed PostgreSQL stack traces logged only in private Vercel runtime logs. | `/api/leads.js` |
