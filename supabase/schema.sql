-- ==============================================================================
-- Spotalents Lead Management & Demo Request Database Schema
-- Standard Security Architecture for Supabase + Vercel
-- ==============================================================================

-- 1. Enable pgcrypto extension for UUID generation if not already enabled
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- 2. Create the leads table with robust data integrity constraints
CREATE TABLE IF NOT EXISTS public.leads (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    first_name VARCHAR(100) NOT NULL CHECK (char_length(trim(first_name)) >= 1),
    last_name VARCHAR(100) NOT NULL CHECK (char_length(trim(last_name)) >= 1),
    company_name VARCHAR(150) NOT NULL CHECK (char_length(trim(company_name)) >= 1),
    email VARCHAR(255) NOT NULL CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
    project_details TEXT CHECK (char_length(project_details) <= 5000),
    source VARCHAR(50) DEFAULT 'start_page' NOT NULL,
    ip_address VARCHAR(45),
    user_agent TEXT,
    referrer TEXT,
    status VARCHAR(20) DEFAULT 'new' NOT NULL CHECK (status IN ('new', 'contacted', 'qualified', 'disqualified', 'converted')),
    created_at TIMESTAMPTZ DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 3. Automatic updated_at trigger function
CREATE OR REPLACE FUNCTION public.set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = timezone('utc'::text, now());
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trigger_leads_set_updated_at ON public.leads;
CREATE TRIGGER trigger_leads_set_updated_at
    BEFORE UPDATE ON public.leads
    FOR EACH ROW
    EXECUTE FUNCTION public.set_updated_at();

-- 4. High-performance Indexes for queries, reporting, and deduplication
CREATE INDEX IF NOT EXISTS idx_leads_created_at ON public.leads (created_at DESC);
CREATE INDEX IF NOT EXISTS idx_leads_email ON public.leads (email);
CREATE INDEX IF NOT EXISTS idx_leads_status ON public.leads (status);
CREATE INDEX IF NOT EXISTS idx_leads_company ON public.leads (company_name);

-- ==============================================================================
-- 5. ROW LEVEL SECURITY (RLS) & DEFENSE-IN-DEPTH POLICIES
-- ==============================================================================

-- Force enable Row Level Security on the table
ALTER TABLE public.leads ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.leads FORCE ROW LEVEL SECURITY;

-- Revoke default public/anon permissions (Least Privilege Principle)
REVOKE ALL ON TABLE public.leads FROM PUBLIC;
REVOKE ALL ON TABLE public.leads FROM anon;
REVOKE ALL ON TABLE public.leads FROM authenticated;

-- Grant INSERT only to anon and authenticated roles
-- (Note: Reads, Updates, and Deletes remain strictly FORBIDDEN to the public)
GRANT INSERT ON TABLE public.leads TO anon;
GRANT INSERT ON TABLE public.leads TO authenticated;

-- Service role has full administrative access for backend Vercel Functions
GRANT ALL ON TABLE public.leads TO service_role;

-- Drop existing policies if any
DROP POLICY IF EXISTS "Public users can only insert validated leads" ON public.leads;
DROP POLICY IF EXISTS "Deny all public reads" ON public.leads;

-- Policy 1: Allow public/anon to INSERT leads with strict data validation
CREATE POLICY "Public users can only insert validated leads"
    ON public.leads
    FOR INSERT
    TO anon, authenticated
    WITH CHECK (
        char_length(trim(first_name)) >= 1 AND
        char_length(trim(last_name)) >= 1 AND
        char_length(trim(company_name)) >= 1 AND
        email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
    );

-- Notice: NO SELECT, UPDATE, or DELETE policies exist for anon!
-- This ensures:
-- 1. Nobody can scrape or download existing leads using the Supabase API.
-- 2. Nobody can overwrite or delete existing client records.
-- 3. Only backend Vercel Functions with SUPABASE_SERVICE_ROLE_KEY or authenticated staff can access lead data.

-- 6. Add Schema Comments for documentation
COMMENT ON TABLE public.leads IS 'Captures inbound demo requests and leads from Spotalents start page';
COMMENT ON COLUMN public.leads.email IS 'Validated contact email address of the prospective client';
COMMENT ON COLUMN public.leads.status IS 'Lifecycle state of the lead: new, contacted, qualified, disqualified, converted';
